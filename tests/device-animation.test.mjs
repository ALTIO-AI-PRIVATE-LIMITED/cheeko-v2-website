import assert from 'node:assert/strict';
import { access, readFile } from 'node:fs/promises';
import test from 'node:test';
import { runInNewContext } from 'node:vm';

const site = new URL('../', import.meta.url);
const html = await readFile(new URL('index.html', site), 'utf8');
const section = html.split('<!-- meet the device -->')[1]?.split('<!-- everything it comes with -->')[0];

test('Meet the device uses the supplied interactive widget instead of the static image', () => {
  assert.ok(section, 'device section must exist');
  assert.match(section, /class="devmap dm" id="devanim"/);
  assert.match(section, /<button class="dm-knob"[^>]*type="button"/);
  assert.equal((section.match(/class="dm-scr(?: on)?"/g) || []).length, 6);
  assert.equal((section.match(/class="dm-lab"/g) || []).length, 7);
  assert.doesNotMatch(section, /hero-image-labels\.png/);
});

test('the page loads the local animation styles, script, and existing image assets', async () => {
  assert.match(html, /assets\/cheeko-device-animation\/device-anim\.css\?v=\d+/);
  assert.match(html, /assets\/cheeko-device-animation\/device-anim\.js\?v=\d+/);
  assert.match(html, /Gochi\+Hand/);
  assert.match(html, /Patrick\+Hand/);

  const images = [...section.matchAll(/src="(assets\/cheeko-device-animation\/img\/[^\"]+)"/g)];
  assert.equal(images.length, 8);
  await Promise.all(images.map(([, path]) => access(new URL(path, site))));
});

test('the supplied animation responds to a dial tap and respects narrow screens and reduced motion', async () => {
  const [script, stylesheet] = await Promise.all([
    readFile(new URL('assets/cheeko-device-animation/device-anim.js', site), 'utf8'),
    readFile(new URL('assets/cheeko-device-animation/device-anim.css', site), 'utf8')
  ]);
  assert.match(script, /knob\.addEventListener\('click'/);
  assert.match(script, /IntersectionObserver/);
  assert.match(script, /prefers-reduced-motion: reduce/);
  assert.match(stylesheet, /@container \(max-width:640px\)/);
  assert.match(stylesheet, /@media \(prefers-reduced-motion:reduce\)/);
});

test('turning the dial advances the real screen and autoplay runs only while visible', async () => {
  const script = await readFile(new URL('assets/cheeko-device-animation/device-anim.js', site), 'utf8');
  const screens = ['Talk', 'Imagine', 'Games', 'Funny Voice', 'Radio', 'Settings'].map((name, index) => ({
    className: index === 0 ? 'dm-scr on' : 'dm-scr',
    getAttribute: () => name
  }));
  const styles = new Map();
  const timeoutQueue = [];
  let click;
  let intersection;
  let interval;
  let clock = 0;
  let stopped = false;
  let label;
  const root = {
    classList: { add() {} },
    querySelector(selector) {
      if (selector === '.dm-dev') return {};
      if (selector === '.dm-stage') return { getBoundingClientRect: () => ({ width: 1120 }) };
      if (selector === '.dm-arrows') return {};
      if (selector === '.dm-knob') return {
        style: { setProperty: (name, value) => styles.set(name, value) },
        setAttribute: (name, value) => { if (name === 'aria-label') label = value; },
        addEventListener: (name, callback) => { if (name === 'click') click = callback; }
      };
      if (selector === '.dm-body') return { addEventListener() {} };
      return null;
    },
    querySelectorAll(selector) { return selector === '.dm-scr' ? screens : []; }
  };
  const context = {
    document: { getElementById: () => root, hidden: false },
    window: {
      matchMedia: () => ({ matches: false }),
      addEventListener() {},
      IntersectionObserver: class { constructor(callback) { intersection = callback; } observe() {} }
    },
    getComputedStyle: () => ({ display: 'none' }),
    requestAnimationFrame: (callback) => { callback(); return 1; },
    cancelAnimationFrame() {},
    setTimeout: (callback) => { timeoutQueue.push(callback); },
    setInterval: (callback) => { interval = callback; return 1; },
    clearInterval: () => { stopped = true; interval = null; },
    Date: { now: () => clock }
  };
  context.IntersectionObserver = context.window.IntersectionObserver;

  runInNewContext(script, context);
  intersection([{ isIntersecting: true }]);
  assert.equal(typeof interval, 'function');
  click();
  timeoutQueue.shift()();
  assert.equal(styles.get('--rot'), '30deg');
  assert.equal(screens[1].className, 'dm-scr on');
  assert.equal(label, 'Turn the dial. Showing Imagine');

  clock = 5001;
  interval();
  timeoutQueue.splice(0).forEach((callback) => callback());
  assert.equal(screens[2].className, 'dm-scr on');
  intersection([{ isIntersecting: false }]);
  assert.equal(stopped, true);
  assert.equal(interval, null);
});
