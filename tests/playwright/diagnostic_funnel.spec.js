// Diagnostic funnel E2E — Next.js commercial front door (AR/EN).
// Covers: locale render, RTL/LTR, interactive qualifier form (client-side),
// CTA deep-link with company/sector params, offer page landing, overflow.
// Safe: no network sends — the qualifier form is fully client-side; the only
// navigation is an internal link. Base URL comes from PLAYWRIGHT_BASE_URL.

const { test, expect } = require("@playwright/test");

function isMobile(testInfo) {
  return testInfo.project.name === "iphone-se-320";
}

test.describe("Diagnostic funnel AR", () => {
  test("renders Arabic hero, RTL, qualifier form", async ({ page }) => {
    await page.goto("/ar/dealix-diagnostic");
    await expect(page.locator("h1")).toContainText("تشخيص");
    const dir = await page.locator("h1").evaluate((el) =>
      el.closest("[dir]")?.getAttribute("dir")
    );
    expect(dir).toBe("rtl");
    await expect(
      page.getByPlaceholder(/شركة الواحة للاستشارات/)
    ).toBeVisible();
    await expect(
      page.getByRole("link", { name: /احجز جلسة الاكتشاف|Book discovery/ }).first()
    ).toBeVisible();
  });

  test("company input builds CTA deep-link; sector toggles", async ({
    page,
  }) => {
    await page.goto("/ar/dealix-diagnostic");
    await page
      .getByPlaceholder(/شركة الواحة للاستشارات/)
      .fill("شركة اختبار");
    const cta = page
      .locator('a[href*="offer/lead-intelligence-sprint"]')
      .first();
    await expect(cta).toBeVisible();
    const href = await cta.getAttribute("href");
    expect(href).toContain(encodeURIComponent("شركة اختبار"));

    const sectorBtn = page
      .locator("button")
      .filter({ hasText: /تقنية|تجزئة|صحة|تعليم|مالي/ })
      .first();
    if ((await sectorBtn.count()) > 0) {
      await sectorBtn.click();
      const cls = await sectorBtn.getAttribute("class");
      expect(cls).toMatch(/bg-primary|border-primary/);
    }
  });

  test("CTA lands on the offer page", async ({ page }) => {
    await page.goto("/ar/dealix-diagnostic");
    await page
      .locator('a[href*="offer/lead-intelligence-sprint"]')
      .first()
      .click();
    await expect(page).toHaveURL(/\/ar\/offer\/lead-intelligence-sprint/);
    expect(await page.title()).toBeTruthy();
  });

  test("no horizontal overflow", async ({ page }) => {
    await page.goto("/ar/dealix-diagnostic");
    const overflow = await page.evaluate(
      () => document.documentElement.scrollWidth - document.documentElement.clientWidth
    );
    expect(overflow).toBeLessThanOrEqual(32);
  });
});

test.describe("Diagnostic funnel EN", () => {
  test("renders English hero, LTR, qualifier form", async ({ page }) => {
    await page.goto("/en/dealix-diagnostic");
    await expect(page.locator("h1")).toContainText("Diagnostic");
    const dir = await page.locator("h1").evaluate((el) =>
      el.closest("[dir]")?.getAttribute("dir")
    );
    expect(dir).toBe("ltr");
    await expect(
      page.getByPlaceholder(/Horizon Tech Co/)
    ).toBeVisible();
  });

  test("CTA deep-link carries company param", async ({ page }) => {
    await page.goto("/en/dealix-diagnostic");
    await page.getByPlaceholder(/Horizon Tech Co/).fill("Test Co");
    const href = await page
      .locator('a[href*="offer/lead-intelligence-sprint"]')
      .first()
      .getAttribute("href");
    expect(href).toContain("Test%20Co");
  });
});

test.describe("Home entry points", () => {
  test("AR home exposes funnel CTA", async ({ page }, testInfo) => {
    test.skip(isMobile(testInfo), "mobile nav collapses; hero CTA covered on desktop");
    await page.goto("/ar");
    const funnelLink = page
      .locator('a[href*="diagnostic"]')
      .first();
    await expect(funnelLink).toBeVisible();
  });
});
