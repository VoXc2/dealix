// Vitest unit tests for frontend/src/lib/hijri.ts (T3e).
//
// Run via: cd frontend && npx vitest run tests/hijri.test.ts

import { describe, expect, it } from "vitest";
import { dualCalendar, formatHijriLong, formatHijriShort, hijriFromGregorian } from "../src/lib/hijri";

describe("hijri helpers", () => {
  it("returns numeric day/month/year + Arabic month name", () => {
    const out = hijriFromGregorian("2026-05-12");
    expect(out.day).toBeGreaterThan(0);
    expect(out.day).toBeLessThanOrEqual(30);
    expect(out.month).toBeGreaterThan(0);
    expect(out.month).toBeLessThanOrEqual(12);
    expect(out.year).toBeGreaterThan(1400);
    expect(out.monthNameAr).not.toBe("");
  });

  it("short format ends with hijri marker", () => {
    expect(formatHijriShort("2026-05-12")).toMatch(/هـ$/);
  });

  it("long format contains the Arabic month name", () => {
    const long = formatHijriLong("2026-05-12");
    expect(long).toMatch(/[؀-ۿ]/);
  });

  it("dualCalendar contains the separator", () => {
    expect(dualCalendar("2026-05-12", "en")).toContain("·");
  });
});
