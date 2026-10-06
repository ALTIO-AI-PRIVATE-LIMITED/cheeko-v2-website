import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import test from 'node:test';
import vm from 'node:vm';

const root = new URL('../', import.meta.url);
const [html, script, characterScript, pttScript, voiceCss] = await Promise.all([
  readFile(new URL('index.html', root), 'utf8'),
  readFile(new URL('assets/js/cheeko-talk.js', root), 'utf8'),
  readFile(new URL('assets/js/playbold.js', root), 'utf8'),
  readFile(new URL('assets/js/voice-ptt.js', root), 'utf8'),
  readFile(new URL('assets/css/voice-card.css', root), 'utf8')
]);

test('the four web-demo characters expose Talk and retain the Google sign-in step for later', () => {
  assert.match(html, /id="ptalk"[^>]*hidden/);
  assert.match(html, /id="talk-auth-step"[^>]*hidden/);
  assert.match(html, /id="talk-google"/);
  assert.match(html, /Continue with Google/);
  for (const character of ['cheeko', 'quizzy', 'nani', 'mitthu', 'chanda', 'masti', 'tara']) {
    assert.match(html, new RegExp(`data-char="${character}"`));
  }
  assert.match(script, /talkButton\.hidden = !WEB_TALK_CHARACTERS\.has\(currentCharacter\)/);
});

test('Chanda, Masti, and Tara stay visible with a store path but cannot open web voice', () => {
  for (const character of ['chanda', 'masti', 'tara']) {
    assert.match(html, new RegExp(`data-char="${character}"`));
    assert.match(script, new RegExp(`//.*"${character}"`));
  }
  assert.match(html, /id="pcard-store-note"[^>]*hidden/);
  assert.match(html, /id="pcard-store-link"[^>]*href="https:\/\/shop\.cheekoai\.in\/"[^>]*hidden/);
  assert.match(characterScript, /storeNote\.hidden = !cardShopCharacter/);
  assert.match(characterScript, /storeLink\.hidden = !cardShopCharacter/);

  const elements = new Map();
  const listeners = new Map();
  const element = (id) => {
    if (!elements.has(id)) elements.set(id, {
      hidden: id === 'talkpanel', textContent: '', dataset: {}, style: { setProperty() {} },
      classList: { toggle() {} }, setAttribute() {}, querySelectorAll() { return []; },
      replaceChildren() {},
      addEventListener(type, callback) { this[`on${type}`] = callback; }
    });
    return elements.get(id);
  };
  vm.runInNewContext(script, {
    document: { getElementById: element, addEventListener(type, callback) { listeners.set(type, callback); }, dispatchEvent() {} },
    window: { addEventListener() {} },
    sessionStorage: { getItem() { return null; }, removeItem() {} },
    setTimeout, clearTimeout, setInterval, clearInterval
  });
  for (const character of ['chanda', 'masti', 'tara']) {
    listeners.get('cheeko:character-change')({ detail: { character } });
    assert.equal(element('ptalk').hidden, true, `${character} should not show Talk live`);
    element('ptalk').onclick();
    assert.equal(element('talkpanel').hidden, true, `${character} should not open the voice card`);
  }
  listeners.get('cheeko:character-change')({ detail: { character: 'cheeko' } });
  assert.equal(element('ptalk').hidden, false);
});

test('the selected persona is sent to the voice API', () => {
  assert.match(script, /body: JSON\.stringify\(\{ character: currentCharacter \}\)/);
  assert.match(script, /currentCharacter = event\.detail\?\.character/);
  assert.doesNotMatch(html, /id="talk-listen"/);
});

test('the shared voice card starts with one Start control, waveform, timer, and end control', () => {
  assert.match(html, /id="talk-wave"/);
  assert.match(html, /id="talk-timer-ring"/);
  assert.match(html, /id="talk-mic"[^>]*aria-label="Start"/);
  assert.match(html, /id="talk-end"/);
  assert.match(html, /assets\/js\/voice-ptt\.js/);
  for (const character of ['cheeko', 'quizzy', 'nani', 'mitthu']) {
    assert.match(characterScript, new RegExp(`char-" \\+ ch\\.k \\+ "\\.png"`));
    assert.match(characterScript, new RegExp(`k:"${character}"`));
  }
});

test('opening Talk requires Google and never requests guest access', async () => {
  const elements = new Map();
  const listeners = new Map();
  const storage = new Map();
  const requests = [];
  let intervals = 0;
  const element = (id) => {
    if (!elements.has(id)) elements.set(id, {
      hidden: id === 'talkpanel',
      disabled: false,
      textContent: '',
      className: '',
      dataset: {},
      style: { setProperty() {} },
      classList: { toggle() {} },
      focus() {},
      querySelectorAll() { return []; },
      replaceChildren() {},
      setAttribute() {},
      addEventListener(type, callback) { this[`on${type}`] = callback; }
    });
    return elements.get(id);
  };
  vm.runInNewContext(script, {
    document: { getElementById: element, addEventListener(type, callback) { listeners.set(type, callback); }, dispatchEvent() {} },
    window: { isSecureContext: false, addEventListener() {} },
    sessionStorage: {
      getItem: (key) => storage.get(key) ?? null,
      setItem: (key, value) => storage.set(key, value),
      removeItem: (key) => storage.delete(key)
    },
    fetch: async (url) => {
      requests.push(url);
      return { ok: true, json: async () => ({ data: { token: 'guest-token', expiresAt: new Date(Date.now() + 60_000).toISOString() } }) };
    },
    CustomEvent: class { constructor(name) { this.type = name; } },
    setTimeout,
    clearTimeout,
    clearInterval,
    setInterval: () => { intervals += 1; return intervals; }
  });

  listeners.get('cheeko:character-change')({ detail: { character: 'cheeko' } });
  await new Promise((resolve) => setTimeout(resolve, 0));
  element('ptalk').onclick();
  await new Promise((resolve) => setTimeout(resolve, 0));

  assert.deepEqual(requests, []);
  assert.equal(intervals, 0);
  assert.equal(element('talk-time').textContent, '1:00');
  assert.equal(element('talk-mic').disabled, false);
  assert.equal(element('talk-mic').getAttribute?.('aria-label') ?? element('talk-hint').textContent, 'Tap to start');
  assert.equal(element('talk-auth-step').hidden, false);
  assert.equal(element('talk-live-step').hidden, true);
  if (element('talk-mic').onclick) element('talk-mic').onclick();
  await new Promise((resolve) => setTimeout(resolve, 0));

  assert.deepEqual(requests, []);
  assert.equal(intervals, 0);
  assert.equal(element('talk-time').textContent, '1:00');
  assert.equal(storage.has('cheeko.webDemoAccess.v2'), false);
});

test('an exhausted signed-in visitor sees the lifetime limit and cannot start Talk', async () => {
  const elements = new Map();
  const listeners = new Map();
  const requests = [];
  const element = (id) => {
    if (!elements.has(id)) elements.set(id, {
      hidden: id === 'talkpanel', disabled: false, textContent: '', className: '', dataset: {},
      style: { setProperty() {} }, classList: { toggle() {} }, focus() {}, replaceChildren() {},
      setAttribute() {}, addEventListener(type, callback) { this[`on${type}`] = callback; }
    });
    return elements.get(id);
  };
  vm.runInNewContext(script, {
    document: { getElementById: element, addEventListener(type, callback) { listeners.set(type, callback); }, dispatchEvent() {} },
    window: { addEventListener() {} },
    sessionStorage: { getItem: () => JSON.stringify({ token: 'google-token', email: 'parent@example.com', expiresAt: new Date(Date.now() + 60_000).toISOString() }), removeItem() {} },
    fetch: async (url) => {
      requests.push(url);
      return { ok: true, json: async () => ({ data: { limitSessions: 10, usedSessions: 10, remainingSessions: 0 } }) };
    },
    CustomEvent: class { constructor(name) { this.type = name; } },
    setTimeout, clearTimeout, setInterval, clearInterval
  });

  listeners.get('cheeko:character-change')({ detail: { character: 'cheeko' } });
  element('ptalk').onclick();
  await new Promise((resolve) => setTimeout(resolve, 0));

  assert.deepEqual(requests, ['/api/web-demo/quota']);
  assert.match(element('talk-status').textContent, /reached your 10-minute/i);
  assert.equal(element('talk-live-controls').hidden, true);
  assert.equal(element('talk-timer-ring').hidden, true);
  assert.equal(element('talk-wave').hidden, true);
});

test('a server-rejected website token returns the visitor to Google sign-in', async () => {
  const elements = new Map();
  const listeners = new Map();
  const storage = new Map([['cheeko.webDemoAccess.v2', JSON.stringify({
    token: 'old-token', email: 'parent@example.com', expiresAt: new Date(Date.now() + 60_000).toISOString()
  })]]);
  let requests = 0;
  const element = (id) => {
    if (!elements.has(id)) elements.set(id, {
      hidden: id === 'talkpanel', disabled: false, textContent: '', className: '', dataset: {},
      style: { setProperty() {} }, classList: { toggle() {} }, focus() {}, replaceChildren() {},
      setAttribute() {}, addEventListener(type, callback) { this[`on${type}`] = callback; }
    });
    return elements.get(id);
  };
  vm.runInNewContext(script, {
    document: { getElementById: element, addEventListener(type, callback) { listeners.set(type, callback); }, dispatchEvent() {} },
    window: { addEventListener() {} },
    sessionStorage: {
      getItem: (key) => storage.get(key) ?? null,
      setItem: (key, value) => storage.set(key, value),
      removeItem: (key) => storage.delete(key)
    },
    fetch: async () => {
      requests += 1;
      if (requests === 1) return { ok: true, json: async () => ({ data: { limitSessions: 10, usedSessions: 0, remainingSessions: 10 } }) };
      if (requests === 2) return { ok: false, status: 401, json: async () => ({ msg: 'Website demo access has expired' }) };
      return new Promise(() => {});
    },
    CustomEvent: class { constructor(name) { this.type = name; } },
    setTimeout, clearTimeout, setInterval, clearInterval
  });
  listeners.get('cheeko:character-change')({ detail: { character: 'cheeko' } });
  element('ptalk').onclick();
  await new Promise((resolve) => setTimeout(resolve, 0));
  element('talk-mic').onclick();
  await new Promise((resolve) => setTimeout(resolve, 20));

  assert.equal(storage.has('cheeko.webDemoAccess.v2'), false);
  assert.equal(element('talk-auth-step').hidden, false);
  assert.equal(element('talk-live-step').hidden, true);
});

test('the removed email-code flow is absent from the website', () => {
  for (const removed of ['talk-email', 'talk-code', 'talk-resend', '/email/request', '/email/verify']) {
    assert.equal(html.includes(removed) || script.includes(removed), false, `${removed} should be removed`);
  }
});

test('Google identity is exchanged only for a short-lived demo token', () => {
  assert.match(script, /GoogleAuthProvider/);
  assert.match(script, /signInWithPopup/);
  assert.match(script, /getIdToken\(\)/);
  assert.match(script, /api\("\/auth\/google"/);
  assert.match(script, /sessionStorage\.setItem\(STORAGE_KEY/);
  assert.match(script, /signOut\(firebase\.auth\)/);
});

test('the verified demo token starts and stops the LiveKit conversation', () => {
  assert.match(script, /api\("\/voice\/start"/);
  assert.match(script, /room\.connect\(session\.url, session\.token\)/);
  assert.match(html, /id="talk-mic"/);
  assert.match(script, /setMicrophoneEnabled\(false\)/);
  assert.match(script, /await activeRoom\.startAudio\(\)/);
  assert.match(pttScript, /type: "ptt_event"/);
  assert.match(pttScript, /type: "speech_end"/);
  assert.match(script, /micButton\.addEventListener\("click"/);
  assert.match(script, /micButton\.disabled = next === "ended" \|\| next === "connecting"/);
  assert.doesNotMatch(html, /id="talk-listen"/);
  assert.match(script, /method: "DELETE"/);
});

test('Start requests the character greeting; later Talk uses push-to-talk', () => {
  assert.match(script, /ready_for_greeting/);
  assert.match(script, /pushToTalk\?\.toggle\(\)/);
});

test('the countdown is gated on remote voice activity and uses the server expiry', () => {
  assert.match(script, /changed\["lk\.agent\.state"\] === "speaking"\) startCountdownAtAgentSpeech/);
  assert.match(script, /RoomEvent\.DataReceived/);
  assert.match(script, /message\.type === "agent_state_changed" && message\.data\?\.new_state === "speaking"/);
  assert.doesNotMatch(script, /if \(!participant \|\| participant === room\?\.localParticipant\) return/);
  assert.match(script, /RoomEvent\.ActiveSpeakersChanged/);
  assert.match(script, /countdown\(session\.expiresAt\)/);
  assert.doesNotMatch(script, /countdown\(new Date\(Date\.now\(\) \+ SESSION_LIMIT_MS\)/);
});

test('hidden voice steps and controls stay hidden in the active card', () => {
  assert.match(voiceCss, /\.pop\.talk-active \.talk-step\[hidden\],\s*\.pop\.talk-active \.talk-live-controls\[hidden\]\s*\{\s*display:\s*none/);
});

test('voice card centers the character name without the role or redundant ready status', () => {
  assert.match(voiceCss, /\.pop\.talk-active \.pmeta \.role\{display:none\}/);
  assert.match(voiceCss, /\.pop\.talk-active \.talk-status:empty\{display:none\}/);
  assert.doesNotMatch(script, /start: `Ready to start with \$\{characterName\}`/);
  assert.doesNotMatch(script, /ready: "Ready"/);
});

test('the browser enforces a hard one-minute conversation limit', () => {
  assert.match(script, /const SESSION_LIMIT_MS = 60_000/);
  assert.match(script, /Math\.min\(Date\.parse\(expiresAt\), Date\.now\(\) \+ SESSION_LIMIT_MS\)/);
  assert.match(script, /deadlineTimer = setTimeout\(\(\) => \{\s*\$\("talk-time"\)\.textContent = "0:00";/);
  assert.match(script, /stopConversation\(false\);\s*\}, Math\.max\(0, hardStopAt - Date\.now\(\)\)\)/);
  assert.match(html, /id="talk-time">1:00</);
});

test('closing the Talk panel ends its voice session', () => {
  assert.match(script, /if \(!opening\) \{\s*stopConversation\(false\)/);
});

test('character popup uses the live voice controls instead of nonexistent sample audio', () => {
  assert.doesNotMatch(characterScript, /assets\/audio\/voice-/);
  assert.match(characterScript, /pplayer\.hidden = true/);
});
