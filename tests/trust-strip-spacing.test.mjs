import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import test from 'node:test';

const site = new URL('../', import.meta.url);
const [html, css] = await Promise.all([
  readFile(new URL('index.html', site), 'utf8'),
  readFile(new URL('assets/css/premium.css', site), 'utf8')
]);

test('trust and backer content has its own padded white band', () => {
  assert.match(html, /<!-- trust row \+ backers -->\s*<div class="wrap trust-backers">/);
  assert.match(css, /\.trust-backers\s*\{[^}]*padding-block:\s*clamp\(32px,/);
});

test('all benefit details stay readable in a mobile-first layout', () => {
  assert.match(css, /\.tstrip\s*\{[^}]*display:grid;[^}]*grid-template-columns:1fr/);
  assert.match(css, /\.tstrip span\s*\{[^}]*display:grid;[^}]*grid-template-columns:/);
  assert.match(css, /@media\s*\(min-width:760px\)\s*\{\s*\.tstrip\s*\{[^}]*grid-template-columns:repeat\(3,minmax\(0,1fr\)\)/);
  assert.doesNotMatch(css, /\.tstrip small\s*\{\s*display:none\s*\}/);
});

test('backer row has breathing room under the benefits', () => {
  assert.match(css, /\.backline\s*\{[^}]*margin-top:clamp\(24px,/);
  assert.match(css, /\.backline\s*\{[^}]*padding-top:clamp\(24px,/);
});
