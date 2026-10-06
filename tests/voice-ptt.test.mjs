import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import test from 'node:test';
import { runInNewContext } from 'node:vm';

const site = new URL('../', import.meta.url);
const source = await readFile(new URL('assets/js/voice-ptt.js', site), 'utf8');

function setup(audioStart) {
  const actions = [];
  const states = [];
  const room = {
    localParticipant: {
      async setMicrophoneEnabled(enabled) { actions.push(enabled ? 'mic-on' : 'mic-off'); }
    }
  };
  const window = {};
  runInNewContext(source, { window });
  const control = window.createCheekoPushToTalk({
    getRoom: () => room,
    getSession: () => ({ sessionId: 'test-session' }),
    startAudio: audioStart || (async () => { actions.push('audio-start'); }),
    publish: async (message) => { actions.push(`${message.type}:${message.action || ''}`); },
    onInterrupt: () => { actions.push('interrupt-playback'); },
    onResumePlayback: () => { actions.push('resume-playback'); },
    onState: (state) => { states.push(state); },
    onError: (error) => { throw error; }
  });
  return { actions, states, control };
}

test('tapping Talk and then Done records one turn and plays the response', async () => {
  const { actions, states, control } = setup();
  await control.toggle();
  assert.equal(control.state, 'recording');
  await control.toggle();
  assert.equal(control.state, 'thinking');
  assert.deepEqual(actions, ['interrupt-playback', 'audio-start', 'ptt_event:press', 'mic-on', 'mic-off', 'speech_end:', 'resume-playback']);
  assert.deepEqual(states, ['recording', 'thinking']);
});

test('Cheeko greeting or speaking never locks Talk, and a new tap interrupts him', async () => {
  const { actions, control } = setup();
  control.agentState('speaking');
  assert.equal(control.state, 'speaking');
  await control.toggle();
  assert.equal(control.state, 'recording');
  control.agentState('speaking');
  assert.equal(control.state, 'recording', 'agent speaking updates must not cancel the user');
  await control.toggle();
  control.agentState('speaking');
  await control.toggle();
  assert.equal(control.state, 'recording');
  assert.equal(actions.filter((action) => action === 'interrupt-playback').length, 2);
  assert.equal(actions.filter((action) => action === 'mic-on').length, 2);
});

test('Talk remains available while the previous answer is pending without a listening event', async () => {
  const { actions, control } = setup();
  await control.toggle();
  await control.toggle();
  assert.equal(control.state, 'thinking');
  await control.toggle();
  assert.equal(control.state, 'recording');
  assert.equal(actions.filter((action) => action === 'mic-on').length, 2);
});

test('slow audio startup does not delay opening the microphone', async () => {
  let finishAudio;
  const { actions, control } = setup(() => new Promise((resolve) => { finishAudio = resolve; }));
  const started = await Promise.race([control.toggle().then(() => true), new Promise((resolve) => setTimeout(() => resolve(false), 30))]);
  assert.equal(started, true);
  assert.ok(actions.includes('mic-on'));
  await control.toggle();
  finishAudio();
});

test('ending a session closes the microphone and ignores later taps', async () => {
  const { actions, control } = setup();
  await control.toggle();
  await control.stop();
  await control.toggle();
  assert.equal(control.state, 'ended');
  assert.equal(actions.at(-1), 'mic-off');
  assert.equal(actions.filter((action) => action === 'mic-on').length, 1);
});
