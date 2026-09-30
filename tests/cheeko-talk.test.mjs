import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import test from 'node:test';

const root = new URL('../', import.meta.url);
const [html, script, characterScript] = await Promise.all([
  readFile(new URL('index.html', root), 'utf8'),
  readFile(new URL('assets/js/cheeko-talk.js', root), 'utf8'),
  readFile(new URL('assets/js/playbold.js', root), 'utf8')
]);

test('Cheeko alone exposes the live Talk control and Google sign-in step', () => {
  assert.match(html, /id="ptalk"[^>]*hidden/);
  assert.match(html, /id="talk-auth-step"[^>]*hidden/);
  assert.match(html, /id="talk-google"/);
  assert.match(html, /Continue with Google/);
  assert.match(script, /currentCharacter !== "cheeko"/);
});

test('Talk requires Google sign-in instead of requesting temporary guest access', () => {
  assert.doesNotMatch(script, /api\("\/auth\/guest"/);
  assert.doesNotMatch(script, /startGuestConversation/);
  assert.match(script, /cheeko\.webDemoAccess\.v2/);
  assert.match(script, /!value\?\.email/);
  assert.match(script, /showStep\(authStep\)/);
  assert.match(script, /Continue with Google to start your one-minute conversation\./);
  assert.match(script, /loadFirebase\(\)\.catch/);
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
  assert.match(script, /const next = !talking/);
  assert.match(script, /activeRoom\.startAudio\(\)/);
  assert.match(script, /activeRoom\.localParticipant\.setMicrophoneEnabled\(next\)/);
  assert.match(script, /method: "DELETE"/);
});

test('the browser enforces a hard one-minute conversation limit', () => {
  assert.match(script, /const SESSION_LIMIT_MS = 60_000/);
  assert.match(script, /Math\.min\(Date\.parse\(expiresAt\), Date\.now\(\) \+ SESSION_LIMIT_MS\)/);
  assert.match(html, /id="talk-time">1:00</);
});

test('closing the Talk panel ends its voice session', () => {
  assert.match(script, /if \(!opening\) \{\s*stopConversation\(false\)/);
});

test('character popup does not request nonexistent sample audio', () => {
  assert.doesNotMatch(characterScript, /assets\/audio\/voice-/);
  assert.match(characterScript, /pplayer\.hidden = ch\.k === "cheeko"/);
});
