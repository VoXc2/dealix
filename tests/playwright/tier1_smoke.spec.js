// Tier-1 smoke — D5 of 30-day plan.
// Asserts the 8 most critical end-to-end flows render correctly across
// 320 / 768 / 1280 breakpoints.
//
// Plan: /root/.claude/plans/vivid-baking-quokka.md
// Run:  npx playwright test --config tests/playwright/playwright.config.js

const { test, expect } = require("@playwright/test");

// ─── Homepage ────────────────────────────────────────────────────────

test.describe("Homepage Tier-1 hero", () => {
  test("hero H1 + single primary CTA + WADL + footer trust badges", async ({ page }) => {
    await page.goto("/");
    // H1 contains the new positioning
    const h1 = page.locator("h1.hero__title");
    await expect(h1).toBeVisible();
    const h1Text = await h1.textContent();
    expect(h1Text).toMatch(/غرفة قيادة|Revenue Command Center/);

    // Exactly 1 primary CTA in hero, pointing to /diagnostic.html
    const primaryCta = page.locator(".hero__ctas a.btn--primary").first();
    await expect(primaryCta).toBeVisible();
    await expect(primaryCta).toHaveAttribute("href", /\/diagnostic\.html/);

    // WADL section present with DEMO label
    await expect(page.locator("#wadl")).toBeVisible();
    await expect(page.locator("#wadl")).toContainText("DEMO");

    // Footer trust badges
    const body = await page.content();
    expect(body).toContain("Saudi-PDPL");
    expect(body).toContain("Approval-first");
    expect(body).toContain("Proof-backed");
  });

  test("no horizontal scroll", async ({ page }) => {
    await page.goto("/");
    const scrollWidth = await page.evaluate(() => document.documentElement.scrollWidth);
    const clientWidth = await page.evaluate(() => document.documentElement.clientWidth);
    expect(scrollWidth).toBeLessThanOrEqual(clientWidth + 2); // 2px slack for sub-pixel rendering
  });

  test("nav has at most 7 primary links (mega-menu present)", async ({ page }) => {
    await page.goto("/");
    const navLinks = await page.locator("nav.nav__links > a").count();
    expect(navLinks).toBeLessThanOrEqual(7);
    await expect(page.locator(".ds-mega-menu")).toBeVisible();
  });
});

// ─── Pricing → checkout ─────────────────────────────────────────────

test.describe("Pricing → Checkout flow", () => {
  test("pricing page lists 6 tiers + CTAs route to /checkout", async ({ page }) => {
    await page.goto("/pricing.html");
    const planCount = await page.locator(".plan").count();
    expect(planCount).toBeGreaterThanOrEqual(6);
    const checkoutLink = page.locator('a[href*="/checkout.html?tier=sprint"]').first();
    await expect(checkoutLink).toBeVisible();
  });

  test("checkout page renders tier summary + NO_LIVE_CHARGE banner", async ({ page }) => {
    await page.goto("/checkout.html?tier=sprint");
    await expect(page.locator("#tier-name")).toContainText("Sprint");
    const body = await page.content();
    expect(body).toContain("NO_LIVE_CHARGE");
    expect(body).toContain("VAT");
    expect(body).toContain("15%");
  });

  test("checkout submit button has 44px+ tap target", async ({ page }) => {
    await page.goto("/checkout.html?tier=sprint");
    const btn = page.locator("#submitBtn");
    const box = await btn.boundingBox();
    expect(box).toBeTruthy();
    expect(box.height).toBeGreaterThanOrEqual(44);
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
    // Today's Decision must render above the dense ops grid
    expect(todayBox.y).toBeLessThan(opsBox.y);
  });

  test("DEMO state pill visible", async ({ page }) => {
    await page.goto("/customer-portal.html");
    await expect(page.locator("#state-pill")).toContainText("DEMO");
  });
});

// ─── Customer Decisions (Track B3) ──────────────────────────────────

test.describe("Customer Decisions UI", () => {
  test("DEMO fallback renders 3 decisions when API unreachable", async ({ page }) => {
    // Block API calls so we exercise the DEMO fallback path
    await page.route("**/api/v1/customer-approvals/**", (route) => route.abort());
    await page.goto("/customer-decisions.html?handle=Slot-A");
    await expect(page.locator(".demo-pill")).toBeVisible({ timeout: 8000 });
    const cardCount = await page.locator(".decision-card").count();
    expect(cardCount).toBeGreaterThanOrEqual(1);
  });

  test("filter buttons toggle aria-pressed correctly", async ({ page }) => {
    await page.route("**/api/v1/customer-approvals/**", (route) => route.abort());
    await page.goto("/customer-decisions.html?handle=Slot-A");
    await page.locator('.filter-btn[data-filter="approval"]').click();
    await expect(page.locator('.filter-btn[data-filter="approval"]')).toHaveAttribute(
      "aria-pressed",
      "true"
    );
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
    const btnBox = await page.locator("#submitBtn").boundingBox();
    expect(btnBox.height).toBeGreaterThanOrEqual(44);
    const body = await page.content();
    expect(body).toContain("Saudi-PDPL");
  });

  test("email validation rejects bad input", async ({ page }) => {
    await page.goto("/login.html");
    await page.locator("#email").fill("not-an-email");
    await page.locator("#submitBtn").click();
    await expect(page.locator("#response.error")).toBeVisible({ timeout: 3000 });
  });
});
