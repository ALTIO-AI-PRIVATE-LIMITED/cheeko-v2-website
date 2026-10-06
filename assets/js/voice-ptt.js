// One tap opens the mic; the next tap closes it and asks the agent to answer.
window.createCheekoPushToTalk = function ({ getRoom, getSession, startAudio, publish, onInterrupt, onResumePlayback, onState, onError }) {
  let state = "ready";
  let activeRoom = null;
  let operations = Promise.resolve();
  let generation = 0;
  let audioStarted = false;
  let audioStarting = null;

  function update(next) {
    if (state === next) return;
    state = next;
    onState(next);
  }

  function enqueue(work) {
    operations = operations.then(work).catch((error) => {
      if (state === "ended") return;
      update("ready");
      onError(error);
    });
    return operations;
  }

  function unlockAudio(room, turn) {
    if (audioStarted || audioStarting) return;
    try {
      // This call starts inside the click gesture so remote audio can play.
      audioStarting = Promise.resolve(startAudio()).then(() => {
        if (generation === turn && getRoom() === room) audioStarted = true;
      }).catch((error) => {
        if (generation === turn && state !== "ended") onError(error);
      }).finally(() => { audioStarting = null; });
    } catch (error) {
      onError(error);
    }
  }

  function talk() {
    const room = getRoom();
    if (!room || state === "ended" || state === "recording") return Promise.resolve();
    const turn = generation;
    activeRoom = room;
    update("recording");
    onInterrupt();
    unlockAudio(room, turn);
    return enqueue(async () => {
      if (generation !== turn || getRoom() !== room) return;
      await publish({ type: "ptt_event", action: "press", state: "start", mode: "manual" });
      if (generation !== turn || getRoom() !== room) return;
      await room.localParticipant.setMicrophoneEnabled(true);
      if (generation !== turn) await room.localParticipant.setMicrophoneEnabled(false);
    });
  }

  function done() {
    if (state !== "recording") return Promise.resolve();
    const room = activeRoom;
    const turn = generation;
    update("thinking");
    return enqueue(async () => {
      if (generation !== turn || getRoom() !== room) return;
      await room.localParticipant.setMicrophoneEnabled(false);
      if (generation !== turn || getRoom() !== room) return;
      const session = getSession();
      await publish({ type: "speech_end", session_id: session?.roomName || session?.sessionId });
      if (generation === turn) onResumePlayback();
    });
  }

  function toggle() {
    return state === "recording" ? done() : talk();
  }

  function agentState(next) {
    if (state === "ended" || state === "recording") return;
    if (next === "speaking") update("speaking");
    else if (next === "thinking") update("thinking");
    else if (next === "listening" || next === "idle") update("ready");
  }

  function stop() {
    generation += 1;
    update("ended");
    const room = activeRoom;
    return enqueue(async () => {
      try { await room?.localParticipant.setMicrophoneEnabled(false); } catch (_) { /* disconnected */ }
    });
  }

  return { toggle, agentState, stop, get state() { return state; } };
};
