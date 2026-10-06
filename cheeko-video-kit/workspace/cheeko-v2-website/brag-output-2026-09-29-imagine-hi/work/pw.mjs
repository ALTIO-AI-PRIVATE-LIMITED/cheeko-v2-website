// Load Playwright from the project, a global install, or the cloud container's copy.
export async function chromium() {
  for (const p of ['playwright', '/opt/node22/lib/node_modules/playwright/index.mjs']) {
    try { return (await import(p)).chromium; } catch {}
  }
  throw new Error('Playwright not found: run `npm i -g playwright` (and `npx playwright install chromium` outside the cloud container)');
}
