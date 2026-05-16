import AxeBuilder from "@axe-core/playwright";
import { test, expect } from "@playwright/test";

test.describe("Next app smoke", () => {
  test("root redirects to a localized dashboard", async ({ page }) => {
    await page.goto("/");
    await expect(page).toHaveURL(/\/(ar|en)\/dashboard/);
  });

  test("login page renders", async ({ page }) => {
    await page.goto("/ar/login");
    await expect(page.locator("body")).toBeVisible();
  });

  test("Arabic dashboard has rtl on documentElement", async ({ page }) => {
    await page.goto("/ar/dashboard");
    const dir = await page.evaluate(() => document.documentElement.getAttribute("dir"));
    expect(dir).toBe("rtl");
  });

  test("no critical or serious axe violations on login", async ({ page }) => {
    await page.goto("/ar/login");
    const results = await new AxeBuilder({ page })
      .disableRules(["color-contrast"])
      .analyze();
    const bad = results.violations.filter((v) =>
      ["critical", "serious"].includes(v.impact ?? ""),
    );
    expect(bad, JSON.stringify(bad, null, 2)).toEqual([]);
  });
});
