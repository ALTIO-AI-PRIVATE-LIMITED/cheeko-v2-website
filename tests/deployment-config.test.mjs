import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import test from 'node:test';

const root = new URL('../', import.meta.url);
const config = await readFile(new URL('netlify.toml', root), 'utf8');

test('Netlify proxies the voice demo to the current Cheeko Manager API', () => {
  assert.match(config, /https:\/\/ota\.cheekoai\.in\/toy\/web-demo\/:splat/);
  assert.doesNotMatch(config, /manager-api-production-e079\.up\.railway\.app/);
});
