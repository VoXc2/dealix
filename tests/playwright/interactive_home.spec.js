const { test, expect } = require("@playwright/test");

test.describe("Dealix V2 interactive front door", () => {
  test("renders the executable hero, V2 logo, and governed execution loop", async ({ page }) => {
    await page.goto("/", { waitUntil: "domcontentloaded" });

    await expect(page.locator(".dx-home")).toBeVisible();
    await expect(page.locator("h1#dx-hero-title")).toContainText("تنفيذ حقيقي يمكن إثباته");
    await expect(page.locator('img.dx-logo[src="/dealix-logo.svg"]').first()).toBeVisible();

    const diagnostic = page.locator('.dx-actions a[href="/book"]').first();
    await expect(diagnostic).toBeVisible();
    await expect(diagnostic).toContainText("workflow");

    await expect(page.locator(".dx-flow-row")).toHaveCount(4);
    await expect(page.locator(".dx-truth-card")).toHaveCount(6);
    await expect(page.locator(".dx-path-item")).toHaveCount(5);
  });

  test("keeps the primary front door usable without horizontal overflow", async ({ page }) => {
    await page.goto("/", { waitUntil: "domcontentloaded" });
    const overflow = await page.evaluate(
      () => document.documentElement.scrollWidth > document.documentElement.clientWidth,
    );
    expect(overflow).toBe(false);
  });

  test("exposes the current RTL V2 manifest and safe metadata", async ({ page }) => {
    const response = await page.request.get("/manifest.webmanifest");
    expect(response.ok()).toBe(true);

    const manifest = await response.json();
    expect(manifest.name).toBe("Dealix — AI Business Operating System");
    expect(manifest.lang).toBe("ar-SA");
    expect(manifest.dir).toBe("rtl");
    expect(manifest.start_url).toBe("/");
    expect(manifest.icons.map((icon) => icon.src)).toContain("/dealix-mark.svg");
  });
});
