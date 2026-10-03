(() => {
  "use strict";

  const $ = (id) => document.getElementById(id);
  const talkButton = $("ptalk");
  const panel = $("talkpanel");
  if (!talkButton || !panel) return;

  const API_BASE = String(window.CHEEKO_WEB_DEMO_API || "/api/web-demo").replace(/\/$/, "");
  const STORAGE_KEY = "cheeko.webDemoAccess.v2";
  const SESSION_LIMIT_MS = 60_000;
  const WEB_TALK_CHARACTERS = new Set([
    "cheeko", "quizzy", "nani", "mitthu",
    // "chanda", "masti", "tara", // Character-card voices stay off the website.
  ]);
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
  let deadlineTimer = null;
  let stopping = false;
  let currentCharacter = "";
  let characterName = "Cheeko";
  let firebasePromise = null;
  let playbackReady = false;
  let attempt = 0;
  let pushToTalk = null;
  let experienceStarted = false;
  let greetingSent = false;
  let countdownStarted = false;

  const authStep = $("talk-auth-step");
  const liveStep = $("talk-live-step");
  const status = $("talk-status");
  const googleButton = $("talk-google");
  const micButton = $("talk-mic");
  function setVoiceState(next) {
    panel.dataset.state = next;
    const recording = next === "recording";
    micButton.disabled = next === "ended" || next === "connecting";
    micButton.setAttribute("aria-pressed", String(recording));
    micButton.setAttribute("aria-label", next === "start" ? "Start" : recording ? "Done talking" : "Talk");
    $("talk-hint").textContent = ({ start: "Tap to start", connecting: "Connecting…", ready: "Tap to talk", recording: "Done talking", thinking: "Tap Talk to ask again", speaking: "Tap Talk to interrupt", ended: "Talk ended" })[next];
    if (next !== "ended") setStatus(({ start: "", connecting: `Calling ${characterName}…`, ready: "", recording: "Listening / recording", thinking: "Getting the answer…", speaking: `${characterName} is speaking` })[next], "live");
  }

  async function publish(payload) {
    if (!room) return;
    await room.localParticipant.publishData(
      new TextEncoder().encode(JSON.stringify(payload)), { reliable: true }
    );
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
      if (!value?.token || !value.email || Date.parse(value.expiresAt) <= Date.now()) throw new Error("expired");
      return value;
    } catch (_) {
      sessionStorage.removeItem(STORAGE_KEY);
      return null;
    }
  }

  function showQuota(quota) {
    if (quota?.remainingSessions > 0) {
      $("talk-timer-ring").hidden = false;
      $("talk-wave").hidden = false;
      setStatus(`${quota.remainingSessions} one-minute Talk ${quota.remainingSessions === 1 ? "session" : "sessions"} left.`, "live");
      return true;
    }
    showStep(liveStep);
    $("talk-live-controls").hidden = true;
    $("talk-timer-ring").hidden = true;
    $("talk-wave").hidden = true;
    setVoiceState("ended");
    setStatus("You have reached your 10-minute Talk live limit. Each one-minute session counts toward this lifetime allowance.", "error");
    return false;
  }

  async function refreshQuota(verified = access()) {
    if (!verified) return;
    try {
      const quota = await api("/quota", { headers: { Authorization: `Bearer ${verified.token}` } });
      if (!panel.hidden && access()?.token === verified.token && !experienceStarted && !session) showQuota(quota);
    } catch (error) {
      if (panel.hidden || access()?.token !== verified.token || experienceStarted) return;
      if (error.status === 401) {
        sessionStorage.removeItem(STORAGE_KEY);
        showStep(authStep);
        setStatus("Continue with Google to start your one-minute conversation.");
      } else setStatus(error.message, "error");
    }
  }

  function resetPanel() {
    clearInterval(timer);
    clearTimeout(deadlineTimer);
    timer = null;
    deadlineTimer = null;
    const verified = access();
    $("talk-live-controls").hidden = false;
    $("talk-timer-ring").hidden = false;
    $("talk-wave").hidden = false;
    playbackReady = false;
    pushToTalk = null;
    experienceStarted = false;
    greetingSent = false;
    countdownStarted = false;
    setVoiceState("start");
    $("talk-time").textContent = "1:00";
    $("talk-timer-ring").style.setProperty("--remaining-angle", "360deg");
    $("talk-greeting").textContent = ({ cheeko: "Hi! I'm Cheeko. Ask me anything!", quizzy: "Hey! I'm Quizzy Bee. Let's take a quiz!", nani: "Hello! I'm Nani. Shall I tell you a story?", mitthu: "Hi! I'm Mitthu. Let's learn spellings!" })[currentCharacter] || `Hi! I'm ${characterName}.`;
    if (verified) {
      showStep(liveStep);
      refreshQuota(verified);
      return;
    }
    showStep(authStep);
    setStatus("Continue with Google to start your one-minute conversation.");
    loadFirebase().catch(() => {});
    setTimeout(() => googleButton.focus(), 30);
  }

  function setPanelOpen(open) {
    attempt += 1;
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
      $("talk-timer-ring").style.setProperty("--remaining-angle", `${seconds * 6}deg`);
      if (!seconds) stopConversation(false);
    };
    tick();
    timer = setInterval(tick, 250);
    deadlineTimer = setTimeout(() => {
      $("talk-time").textContent = "0:00";
      $("talk-timer-ring").style.setProperty("--remaining-angle", "0deg");
      stopConversation(false);
    }, Math.max(0, hardStopAt - Date.now()));
  }

  function startCountdownAtAgentSpeech() {
    if (countdownStarted || !experienceStarted || !session || !room) return;
    countdownStarted = true;
    countdown(session.expiresAt);
  }

  function startCountdownWhenCharacterSpeaks(speakers) {
    if (speakers.some((participant) => participant !== room?.localParticipant)) startCountdownAtAgentSpeech();
  }

  async function requestMicrophone() {
    if (!window.isSecureContext || !navigator.mediaDevices?.getUserMedia) {
      throw new Error("Microphone access needs HTTPS and a supported browser.");
    }
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    stream.getTracks().forEach((track) => track.stop());
  }

  async function startConversation() {
    if (!WEB_TALK_CHARACTERS.has(currentCharacter)) return;
    const verified = access();
    const currentAttempt = attempt;
    if (!verified) {
      showStep(authStep);
      setStatus("Continue with Google to start your one-minute conversation.");
      return;
    }

    showStep(liveStep);
    try {
      const quota = await api("/quota", { headers: { Authorization: `Bearer ${verified.token}` } });
      if (!showQuota(quota)) return;
      setStatus("Allow your microphone to start the demo…");
      await requestMicrophone();
      if (panel.hidden || currentAttempt !== attempt) return;
      setStatus(`Calling ${characterName}…`);
      session = await api("/voice/start", {
        method: "POST",
        headers: { Authorization: `Bearer ${verified.token}` },
        body: JSON.stringify({ character: currentCharacter })
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
        audio.autoplay = pushToTalk?.state !== "recording";
        $("talk-audio").appendChild(audio);
        if (pushToTalk?.state === "recording") audio.pause();
        else if (playbackReady) audio.play().catch(() => setStatus("Sound is blocked. Tap Talk to allow audio.", "error"));
      });
      room.on(livekit.RoomEvent.ParticipantAttributesChanged, (changed, participant) => {
        if (participant === room?.localParticipant || !changed["lk.agent.state"]) return;
        if (changed["lk.agent.state"] === "speaking") startCountdownAtAgentSpeech();
        pushToTalk?.agentState(changed["lk.agent.state"]);
      });
      room.on(livekit.RoomEvent.DataReceived, (payload, participant) => {
        if (participant === room?.localParticipant) return;
        let message;
        try { message = JSON.parse(new TextDecoder().decode(payload)); } catch (_) { return; }
        if (message.type === "agent_state_changed" && message.data?.new_state === "speaking") {
          startCountdownAtAgentSpeech();
        }
      });
      room.on(livekit.RoomEvent.ActiveSpeakersChanged, startCountdownWhenCharacterSpeaks);
      room.on(livekit.RoomEvent.ParticipantConnected, () => { greetIfReady(); });
      room.on(livekit.RoomEvent.Disconnected, () => {
        if (!stopping) stopConversation(false);
      });
      await room.connect(session.url, session.token);
      if (panel.hidden || currentAttempt !== attempt) {
        await stopConversation(false);
        return;
      }
      // The mic stays closed until the visitor taps Talk after the greeting.
      await room.localParticipant.setMicrophoneEnabled(false);
      try {
        await room.startAudio();
        playbackReady = true;
      } catch (_) {
        setStatus("Sound is blocked. Tap Talk to allow audio.", "error");
      }
      pushToTalk = window.createCheekoPushToTalk({
        getRoom: () => room,
        getSession: () => session,
        publish,
        onInterrupt: () => $("talk-audio").querySelectorAll("audio").forEach((audio) => audio.pause()),
        onResumePlayback: () => $("talk-audio").querySelectorAll("audio").forEach((audio) => audio.play().catch(() => setStatus("Sound is blocked. Tap Talk again to allow audio.", "error"))),
        startAudio: async () => {
          const activeRoom = room;
          await activeRoom.startAudio();
          if (room !== activeRoom) return;
          playbackReady = true;
          if (pushToTalk?.state !== "recording") $("talk-audio").querySelectorAll("audio").forEach((audio) => audio.play().catch(() => {}));
        },
        onState: setVoiceState,
        onError: (error) => setStatus(error.name === "NotAllowedError" ? `Please allow microphone access to talk to ${characterName}.` : error.message, "error")
      });
      $("talk-live-controls").hidden = false;
      const existingAgent = [...room.remoteParticipants.values()][0];
      setVoiceState("ready");
      if (existingAgent?.attributes?.["lk.agent.state"]) {
        pushToTalk.agentState(existingAgent.attributes["lk.agent.state"]);
        if (existingAgent.attributes["lk.agent.state"] === "speaking") startCountdownAtAgentSpeech();
      }
      if (existingAgent?.isSpeaking) startCountdownWhenCharacterSpeaks([existingAgent]);
      greetIfReady();
      if (!existingAgent) setStatus(`Waiting for ${characterName} to join…`, "live");
    } catch (error) {
      await stopConversation(false);
      if (error.status === 401) {
        sessionStorage.removeItem(STORAGE_KEY);
        showStep(authStep);
        setStatus("Your Talk access expired. Continue with Google to sign in again.", "error");
        return;
      }
      showStep(liveStep);
      if (error.status === 403) showQuota({ remainingSessions: 0 });
      else setStatus(error.name === "NotAllowedError" ? "Microphone permission was blocked. Please allow it and try again." : error.message, "error");
    }
  }

  function greetIfReady() {
    if (greetingSent || !experienceStarted || !pushToTalk || !room || !session || !room.remoteParticipants.size) return;
    greetingSent = true;
    if (pushToTalk?.state === "ready") setVoiceState("speaking");
    publish({ type: "ready_for_greeting", session_id: session.roomName || session.sessionId, timestamp: Date.now() })
      .catch((error) => setStatus(error.message, "error"));
  }

  async function startExperience() {
    if (stopping || experienceStarted || panel.hidden || !WEB_TALK_CHARACTERS.has(currentCharacter)) return;
    experienceStarted = true;
    setVoiceState("connecting");
    if (access()) await startConversation();
    else {
      experienceStarted = false;
      showStep(authStep);
    }
  }

  async function stopConversation(showEnded = true) {
    if (stopping || (!room && !session && !pushToTalk && !experienceStarted)) return;
    stopping = true;
    attempt += 1;
    const stoppingAttempt = attempt;
    clearInterval(timer);
    clearTimeout(deadlineTimer);
    timer = null;
    deadlineTimer = null;
    const endingSession = session;
    const verified = access();
    const endingPushToTalk = pushToTalk;
    const endingRoom = room;
    pushToTalk = null;
    session = null;
    room = null;
    playbackReady = false;
    experienceStarted = false;
    countdownStarted = false;
    await endingPushToTalk?.stop();
    try { await endingRoom?.disconnect(); } catch (_) { /* already disconnected */ }
    if (endingSession?.sessionId && verified?.token) {
      api(`/voice/${encodeURIComponent(endingSession.sessionId)}`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${verified.token}` }
      }).catch(() => {});
    }
    stopping = false;
    if (panel.hidden || stoppingAttempt !== attempt) return;
    setVoiceState("ended");
    $("talk-audio").replaceChildren();
    showStep(liveStep);
    $("talk-live-controls").hidden = true;
    setStatus(showEnded ? `Thanks for talking with ${characterName}! Close and tap Talk live whenever you want another demo.` : "The one-minute demo has ended. Close and tap Talk live to try again.");
    refreshQuota();
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
      showStep(liveStep);
      if (result.quota?.remainingSessions > 0) {
        setVoiceState("start");
        showQuota(result.quota);
      } else showQuota(result.quota);
    } catch (error) {
      showStep(authStep);
      setStatus(googleErrorMessage(error), "error");
    } finally {
      if (firebase) await firebase.authSdk.signOut(firebase.auth).catch(() => {});
      googleButton.disabled = false;
    }
  }

  talkButton.addEventListener("click", () => {
    if (!WEB_TALK_CHARACTERS.has(currentCharacter)) return;
    const opening = panel.hidden;
    if (opening) document.dispatchEvent(new CustomEvent("cheeko:talk-open"));
    setPanelOpen(opening);
    if (!opening) {
      stopConversation(false);
      return;
    }
  });

  googleButton.addEventListener("click", signInWithGoogle);
  micButton.addEventListener("click", () => {
    if (micButton.disabled) return;
    if (!experienceStarted) startExperience();
    else pushToTalk?.toggle();
  });
  $("talk-end").addEventListener("click", () => stopConversation(true));

  document.addEventListener("cheeko:character-change", (event) => {
    currentCharacter = event.detail?.character || "";
    characterName = $("pname").textContent || "Cheeko";
    talkButton.hidden = !WEB_TALK_CHARACTERS.has(currentCharacter);
    setPanelOpen(false);
    stopConversation(false);
  });
  document.addEventListener("cheeko:modal-close", () => {
    setPanelOpen(false);
    stopConversation(false);
  });
  window.addEventListener("pagehide", () => stopConversation(false));
})();
