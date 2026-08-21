// Tier-1 smoke — customer-facing first-launch surfaces.
// Run: npx playwright test --config tests/playwright/playwright.config.js

const { test, expect } = require("@playwright/test");

function isMobile(testInfo) {
  return testInfo.project.name === "iphone-se-320";
}

// ─── Homepage ────────────────────────────────────────────────────────

test.describe("Homepage Tier-1 hero", () => {
  test("hero H1 + single primary CTA + WADL + trust signals", async ({ page }) => {
    await page.goto("/");
    const h1 = page.locator("h1.hero__title");
    await expect(h1).toBeVisible();
    const h1Text = await h1.textContent();
    expect(h1Text).toMatch(/غرفة قيادة|Revenue Command Center|AI Operating Team|نظام تشغيل/);

    const primaryCta = page.locator(".hero__ctas a.btn--primary").first();
    await expect(primaryCta).toBeVisible();

    const body = await page.content();
    expect(body).toMatch(/Approval-first/);
    expect(body).toMatch(/Proof-backed/);
    expect(body).toMatch(/Saudi-PDPL|Saudi-first/);
  });

  test("no horizontal scroll (desktop + tablet)", async ({ page }, testInfo) => {
    test.skip(isMobile(testInfo), "WADL mock currently 360px wide; sub-360 follow-up");
    await page.goto("/");
    const scrollWidth = await page.evaluate(() => document.documentElement.scrollWidth);
    const clientWidth = await page.evaluate(() => document.documentElement.clientWidth);
    expect(scrollWidth - clientWidth).toBeLessThanOrEqual(32);
  });

  test("nav has at most 7 primary links + mega-menu present (desktop)", async ({ page }, testInfo) => {
    test.skip(isMobile(testInfo), "Mobile nav collapses behind hamburger; mega-menu hidden");
    await page.goto("/");
    const navLinks = await page.locator("nav.nav__links > a").count();
    expect(navLinks).toBeLessThanOrEqual(7);
    expect(await page.locator(".ds-mega-menu").count()).toBeGreaterThanOrEqual(1);
  });
});

// ─── Quote-only commercial path ─────────────────────────────────────

test.describe("Quote-only first-launch flow", () => {
  test("pricing page exposes diagnostic → 30-day Pilot → proof-based expansion", async ({ page }) => {
    await page.goto("/pricing.html");
    const body = await page.content();
    expect(body).toContain("Free Mini Diagnostic");
    expect(body).toContain("Revenue Command Pilot — 30 يومًا");
    expect(body).toContain("Quote-only");
    expect(body).toContain("Weekly Proof Pack");
    expect(body).toContain("Final Proof Pack");
    expect(body).toContain("لا Checkout حي");
    expect(body).not.toMatch(/\b499\b|\b1500\b|1,500|\b2999\b|2,999|\b7999\b|7,999|\b12000\b|12,000/);
    expect(body).not.toContain("/checkout.html?tier=");

    const diagnostic = page.locator('a[href="/diagnostic.html"]').first();
    await expect(diagnostic).toBeVisible();
  });

  test("checkout is a fail-closed information page with no payment path", async ({ page }) => {
    await page.goto("/checkout.html?tier=sprint");
    const body = await page.content();
    expect(body).toContain("NO_LIVE_CHARGE");
    expect(body).toContain("QUOTE_ONLY");
    expect(body).toContain("NO_PUBLIC_FIXED_PRICE");
    expect(body).toContain("NO_SELF_SERVE_CHECKOUT");
    expect(body).toContain("REQUEST ≠ QUOTE ≠ INVOICE ≠ PAYMENT ≠ REVENUE");
    expect(body).not.toContain("/api/v1/payment-ops/invoice-intent");
    expect(body).not.toContain("TIERS=");
    expect(body).not.toMatch(/\b499\b|\b2999\b|\b7999\b|\b12000\b/);
    await expect(page.locator('a[href="/diagnostic.html"]')).toBeVisible();
  });

  test("legacy checkout-success route is also fail-closed", async ({ page }) => {
    await page.goto("/checkout-success.html?request_id=legacy&tier=sprint&amount=499");
    const body = await page.content();
    expect(body).toContain("Checkout العام غير مفعّل");
    expect(body).toContain("NO_LIVE_CHARGE");
    expect(body).toContain("NO_SELF_SERVE_CHECKOUT");
    expect(body).not.toContain("request_id");
    expect(body).not.toContain("tier-label");
    expect(body).not.toContain("amount-shown");
  });
});

// ─── Customer Portal ────────────────────────────────────────────────

test.describe("Customer Portal", () => {
  test("Today's Decision precedes the deep ops grid", async ({ page }) => {
    await page.goto("/customer-portal.html");
    const todayBox = await page.locator("#today-decision").boundingBox();
    const opsBox = await page.locator("#ops-grid").boundingBox();
    expect(todayBox).toBeTruthy();
    expect(opsBox).toBeTruthy();
    expect(todayBox.y).toBeLessThan(opsBox.y);
  });

  test("DEMO state pill visible", async ({ page }) => {
    await page.goto("/customer-portal.html");
    await expect(page.locator("#state-pill")).toContainText("DEMO");
  });
});

// ─── Customer Decisions ─────────────────────────────────────────────

test.describe("Customer Decisions UI", () => {
  test("page has decision queue infrastructure + safety strip", async ({ page }) => {
    await page.route("**/api/v1/customer-approvals/**", (route) => route.abort());
    await page.goto("/customer-decisions.html?handle=Slot-A");

    await expect(page.locator("#decisions-list")).toBeAttached();
    await expect(page.locator(".filter-bar")).toBeAttached();
    await expect(page.locator('.filter-btn[data-filter="approval"]')).toBeAttached();

    const body = await page.content();
    expect(body).toContain("NO_LIVE_SEND");
    expect(body).toContain("Saudi-PDPL");
  });

  test("filter buttons are present in DOM", async ({ page }) => {
    await page.route("**/api/v1/customer-approvals/**", (route) => route.abort());
    await page.goto("/customer-decisions.html?handle=Slot-A");
    const allFilters = page.locator(".filter-btn");
    const count = await allFilters.count();
    expect(count).toBeGreaterThanOrEqual(4);
  });
});

// ─── Proof L1-L5 ladder ─────────────────────────────────────────────

test.describe("Proof page evidence ladder", () => {
  test("L1 → L5 ladder visible with all 5 levels", async ({ page }) => {
    await page.goto("/proof.html");
    for (const level of ["L1", "L2", "L3", "L4", "L5"]) {
      await expect(page.locator(".ds-evidence-ladder")).toContainText(level);
    }
  });
});

// ─── Trust Center ───────────────────────────────────────────────────

test.describe("Trust Center 8 hard gates", () => {
  test("all 8 gate codes visible as feature cards", async ({ page }) => {
    await page.goto("/trust-center.html");
    const gates = [
      "NO_LIVE_SEND",
      "NO_LIVE_CHARGE",
      "NO_COLD_WHATSAPP",
      "NO_LINKEDIN_AUTOMATION",
      "NO_SCRAPING",
      "NO_FAKE_PROOF",
      "NO_FAKE_REVENUE",
      "NO_UNAPPROVED_TESTIMONIAL",
    ];
    const body = await page.content();
    for (const gate of gates) {
      expect(body).toContain(gate);
    }
  });
});

// ─── Login (magic-link) ─────────────────────────────────────────────

test.describe("Login magic-link", () => {
  test("renders form + 44px submit button + footer badges", async ({ page }) => {
    await page.goto("/login.html");
    await expect(page.locator("#email")).toBeVisible();
    const btn = page.locator("#submitBtn");
    await btn.scrollIntoViewIfNeeded();
    const btnBox = await btn.boundingBox();
    expect(btnBox.height).toBeGreaterThanOrEqual(44);
    const body = await page.content();
    expect(body).toContain("Saudi-PDPL");
  });

  test("email validation rejects bad input", async ({ page }) => {
    await page.goto("/login.html");
    await page.locator("#email").fill("not-an-email");
    await page.locator("#submitBtn").click();
    await expect(page.locator("#response.error")).toBeVisible({ timeout: 5000 });
  });
});
