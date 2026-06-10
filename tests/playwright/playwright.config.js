// Playwright config — Track D5 of 30-day plan.
// Smoke tests on Tier-1 conversion pages at 320px / 768px / 1280px.
// Confined to tests/playwright/ to avoid Node.js sprawl across the
// Python repo. Plan: /root/.claude/plans/vivid-baking-quokka.md

const { defineConfig, devices } = require("@playwright/test");

module.exports = defineConfig({
  testDir: ".",
  testMatch: "*.spec.js",
  timeout: 30000,
  expect: { timeout: 5000 },
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 1 : 0,
  workers: process.env.CI ? 2 : undefined,
  reporter: process.env.CI ? [["github"], ["html", { outputFolder: "playwright-report" }]] : "list",
  use: {
    baseURL: process.env.PLAYWRIGHT_BASE_URL || "http://localhost:8765",
    trace: "on-first-retry",
    screenshot: "only-on-failure",
  },
  // Confined to Chromium only — workflow installs `--with-deps chromium`.
  // Viewport-based emulation covers all 3 breakpoints without requiring
  // WebKit / Firefox binaries.
  projects: [
    {
      name: "iphone-se-320",
      use: {
        ...devices["Desktop Chrome"],
        viewport: { width: 320, height: 568 },
        userAgent:
          "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
      },
    },
    {
      name: "tablet-768",
      use: { ...devices["Desktop Chrome"], viewport: { width: 768, height: 1024 } },
    },
    {
      name: "desktop-1280",
      use: { ...devices["Desktop Chrome"], viewport: { width: 1280, height: 800 } },
    },
  ],
});
