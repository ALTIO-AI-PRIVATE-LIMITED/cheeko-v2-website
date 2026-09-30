(() => {
  "use strict";

  const $ = (id) => document.getElementById(id);
  const talkButton = $("ptalk");
  const panel = $("talkpanel");
  if (!talkButton || !panel) return;

  const API_BASE = String(window.CHEEKO_WEB_DEMO_API || "/api/web-demo").replace(/\/$/, "");
  const STORAGE_KEY = "cheeko.webDemoAccess.v2";
  const SESSION_LIMIT_MS = 60_000;
  const FIREBASE_CONFIG = window.CHEEKO_FIREBASE_CONFIG || {
    apiKey: "AIzaSyDIIWOKDcvrEQpIQiu3UNCzSrWhAygVk9I",
    authDomain: "cheekoai.firebaseapp.com",
    projectId: "cheekoai",
    storageBucket: "cheekoai.firebasestorage.app",
    messagingSenderId: "956241760367"
  };
  let room = null;
  let session = null;
  let livekit = null;
  let timer = null;
  let stopping = false;
  let currentCharacter = "";
  let firebasePromise = null;
  let talking = false;
  let attempt = 0;

  const authStep = $("talk-auth-step");
  const liveStep = $("talk-live-step");
  const status = $("talk-status");
  const googleButton = $("talk-google");
  const micButton = $("talk-mic");

  function setTalking(active) {
    talking = active;
    micButton.setAttribute("aria-pressed", String(active));
    micButton.classList.toggle("talking", active);
    micButton.textContent = active ? "■ Done — listen" : "🎙 Tap to talk";
  }

  function setStatus(message, kind = "") {
    status.textContent = message;
    status.className = `talk-status${kind ? ` ${kind}` : ""}`;
  }

  function showStep(step) {
    [authStep, liveStep].forEach((el) => { el.hidden = el !== step; });
  }

  function loadFirebase() {
    if (!firebasePromise) {
      firebasePromise = Promise.all([
        import("https://www.gstatic.com/firebasejs/12.19.0/firebase-app.js"),
        import("https://www.gstatic.com/firebasejs/12.19.0/firebase-auth.js")
      ]).then(async ([appSdk, authSdk]) => {
        const app = appSdk.getApps().find((item) => item.name === "cheeko-web-demo")
          || appSdk.initializeApp(FIREBASE_CONFIG, "cheeko-web-demo");
        const auth = authSdk.getAuth(app);
        await authSdk.setPersistence(auth, authSdk.inMemoryPersistence);
        return { auth, authSdk };
      });
    }
    return firebasePromise;
  }

  async function api(path, options = {}) {
    const response = await fetch(`${API_BASE}${path}`, {
      ...options,
      headers: { "Content-Type": "application/json", ...(options.headers || {}) }
    });
    let body = null;
    try { body = await response.json(); } catch (_) { /* proxy/network response without JSON */ }
    if (!response.ok) {
      const error = new Error(body?.msg || "Cheeko could not connect. Please try again.");
      error.status = response.status;
      throw error;
    }
    return body?.data;
  }

  function access() {
    try {
      const value = JSON.parse(sessionStorage.getItem(STORAGE_KEY) || "null");
      if (!value?.token || !value?.email || Date.parse(value.expiresAt) <= Date.now()) throw new Error("expired");
      return value;
    } catch (_) {
      sessionStorage.removeItem(STORAGE_KEY);
      return null;
    }
  }

  function resetPanel() {
    clearInterval(timer);
    timer = null;
    const verified = access();
    $("talk-live-controls").hidden = true;
    setTalking(false);
    if (verified) {
      showStep(liveStep);
      setStatus("Ready to talk with Cheeko.");
      return;
    }
    showStep(authStep);
    setStatus("Continue with Google to start your one-minute conversation.");
    loadFirebase().catch(() => {});
    setTimeout(() => googleButton.focus(), 30);
  }

  function setPanelOpen(open) {
    if (!open) attempt += 1;
    panel.hidden = !open;
    talkButton.setAttribute("aria-expanded", String(open));
    $("pop")?.classList.toggle("talk-active", open);
    if (open) resetPanel();
  }

  function countdown(expiresAt) {
    clearInterval(timer);
    const hardStopAt = Math.min(Date.parse(expiresAt), Date.now() + SESSION_LIMIT_MS);
    const tick = () => {
      const seconds = Math.max(0, Math.ceil((hardStopAt - Date.now()) / 1000));
      $("talk-time").textContent = `0:${String(seconds).padStart(2, "0")}`;
      if (!seconds) stopConversation(false);
    };
    tick();
    timer = setInterval(tick, 250);
  }

  async function requestMicrophone() {
    if (!window.isSecureContext || !navigator.mediaDevices?.getUserMedia) {
      throw new Error("Microphone access needs HTTPS and a supported browser.");
    }
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    stream.getTracks().forEach((track) => track.stop());
  }

  async function startConversation() {
    const verified = access();
    const currentAttempt = attempt;
    if (!verified) {
      showStep(authStep);
      setStatus("Continue with Google to start your one-minute conversation.");
      return;
    }

    showStep(liveStep);
    setStatus("Allow your microphone to start the demo…");
    $("talk-live-controls").hidden = true;
    try {
      await requestMicrophone();
      if (panel.hidden || currentAttempt !== attempt) return;
      setStatus("Calling Cheeko…");
      session = await api("/voice/start", {
        method: "POST",
        headers: { Authorization: `Bearer ${verified.token}` }
      });
      if (panel.hidden || currentAttempt !== attempt) {
        await stopConversation(false);
        return;
      }
      if (!livekit) livekit = await import("../vendor/livekit-client.esm.mjs");
      if (panel.hidden || currentAttempt !== attempt) {
        await stopConversation(false);
        return;
      }

      room = new livekit.Room({ adaptiveStream: true, dynacast: true });
      room.on(livekit.RoomEvent.TrackSubscribed, (track) => {
        if (track.kind !== livekit.Track.Kind.Audio) return;
        const audio = track.attach();
        audio.autoplay = true;
        $("talk-audio").appendChild(audio);
      });
      room.on(livekit.RoomEvent.ParticipantConnected, () => setStatus("Cheeko is ready. Tap the mic to talk.", "live"));
      room.on(livekit.RoomEvent.ParticipantAttributesChanged, (changed, participant) => {
        if (participant === room?.localParticipant || !changed["lk.agent.state"]) return;
        const states = { listening: "Cheeko is listening…", thinking: "Cheeko is thinking…", speaking: "Cheeko is speaking…" };
        setStatus(states[changed["lk.agent.state"]] || "Connected to Cheeko", "live");
      });
      room.on(livekit.RoomEvent.Disconnected, () => {
        if (!stopping) stopConversation(false);
      });
      await room.connect(session.url, session.token);
      if (panel.hidden || currentAttempt !== attempt) {
        await stopConversation(false);
        return;
      }
      // Keep input closed until the visitor taps the mic, like Persona Admin's Test tab.
      await room.localParticipant.setMicrophoneEnabled(false);
      setTalking(false);
      $("talk-live-controls").hidden = false;
      countdown(session.expiresAt);
      const existingAgent = [...room.remoteParticipants.values()][0];
      setStatus(existingAgent ? "Tap the mic to talk to Cheeko." : "Waiting for Cheeko to join…", "live");
    } catch (error) {
      await stopConversation(false);
      showStep(liveStep);
      setStatus(error.name === "NotAllowedError" ? "Microphone permission was blocked. Please allow it and try again." : error.message, "error");
    }
  }

  async function stopConversation(showEnded = true) {
    if (stopping) return;
    stopping = true;
    clearInterval(timer);
    timer = null;
    const endingSession = session;
    const verified = access();
    session = null;
    try { await room?.disconnect(); } catch (_) { /* already disconnected */ }
    room = null;
    setTalking(false);
    micButton.disabled = false;
    $("talk-audio").replaceChildren();
    if (endingSession?.sessionId && verified?.token) {
      api(`/voice/${encodeURIComponent(endingSession.sessionId)}`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${verified.token}` }
      }).catch(() => {});
    }
    stopping = false;
    if (panel.hidden) return;
    showStep(liveStep);
    $("talk-live-controls").hidden = true;
    setStatus(showEnded ? "Thanks for talking with Cheeko! Close and tap Talk live whenever you want another demo." : "The demo has ended. Close and tap Talk live to try again.");
  }

  function googleErrorMessage(error) {
    if (error?.code === "auth/popup-closed-by-user" || error?.code === "auth/cancelled-popup-request") return "Google sign-in was cancelled.";
    if (error?.code === "auth/popup-blocked") return "Your browser blocked Google sign-in. Allow pop-ups and try again.";
    if (error?.code === "auth/unauthorized-domain") return "This website domain is not authorized for Google sign-in.";
    return error?.message || "Google sign-in could not be completed. Please try again.";
  }

  async function signInWithGoogle() {
    googleButton.disabled = true;
    setStatus("Opening Google sign-in…");
    let firebase = null;
    try {
      firebase = await loadFirebase();
      const provider = new firebase.authSdk.GoogleAuthProvider();
      provider.setCustomParameters({ prompt: "select_account" });
      const credential = await firebase.authSdk.signInWithPopup(firebase.auth, provider);
      const idToken = await credential.user.getIdToken();
      const result = await api("/auth/google", {
        method: "POST",
        headers: { Authorization: `Bearer ${idToken}` }
      });
      sessionStorage.setItem(STORAGE_KEY, JSON.stringify(result));
      setStatus("Google verified. Connecting you to Cheeko…", "live");
      await startConversation();
    } catch (error) {
      showStep(authStep);
      setStatus(googleErrorMessage(error), "error");
    } finally {
      if (firebase) await firebase.authSdk.signOut(firebase.auth).catch(() => {});
      googleButton.disabled = false;
    }
  }

  talkButton.addEventListener("click", () => {
    const opening = panel.hidden;
    if (opening) document.dispatchEvent(new CustomEvent("cheeko:talk-open"));
    setPanelOpen(opening);
    if (!opening) {
      stopConversation(false);
      return;
    }
    if (access()) startConversation();
  });

  googleButton.addEventListener("click", signInWithGoogle);
  micButton.addEventListener("click", async () => {
    if (!room || micButton.disabled) return;
    const activeRoom = room;
    micButton.disabled = true;
    try {
      const next = !talking;
      // Unlock remote audio during a real tap, including on mobile Safari.
      const audioReady = activeRoom.startAudio().then(() => true, () => false);
      await activeRoom.localParticipant.setMicrophoneEnabled(next);
      if (room !== activeRoom) return;
      setTalking(next);
      setStatus(await audioReady
        ? (next ? "Speak now. Tap Done when you finish." : "Cheeko is listening and getting ready to answer…")
        : "Browser audio is blocked. Allow sound playback, then tap the mic again.", "live");
    } catch (error) {
      setStatus(error.name === "NotAllowedError" ? "Please allow microphone access to talk to Cheeko." : error.message, "error");
    } finally {
      micButton.disabled = false;
    }
  });
  $("talk-end").addEventListener("click", () => stopConversation(true));

  document.addEventListener("cheeko:character-change", (event) => {
    currentCharacter = event.detail?.character || "";
    talkButton.hidden = currentCharacter !== "cheeko";
    if (currentCharacter !== "cheeko") {
      setPanelOpen(false);
      stopConversation(false);
    }
  });
  document.addEventListener("cheeko:modal-close", () => {
    setPanelOpen(false);
    stopConversation(false);
  });
  window.addEventListener("pagehide", () => stopConversation(false));
})();
