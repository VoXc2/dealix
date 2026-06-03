import { describe, it, expect } from "vitest";
import {
  SYSTEMS,
  SYSTEM_BY_SLUG,
  getSystem,
  startingPriceLabel,
  type SystemSlug,
} from "@/data/systems";

// The exact five market-entry systems and their opening prices (SAR).
const EXPECTED_PRICES: Record<SystemSlug, number> = {
  "revenue-operating-system": 4500,
  "executive-command-os": 5500,
  "follow-up-recovery-os": 3500,
  "whatsapp-client-os": 4500,
  "proposal-proof-os": 3000,
};

describe("Focus 5 systems — catalog", () => {
  it("ships exactly five systems", () => {
    expect(SYSTEMS).toHaveLength(5);
  });

  it("contains the five expected slugs", () => {
    const slugs = SYSTEMS.map((s) => s.slug).sort();
    expect(slugs).toEqual(
      [
        "executive-command-os",
        "follow-up-recovery-os",
        "proposal-proof-os",
        "revenue-operating-system",
        "whatsapp-client-os",
      ].sort(),
    );
  });

  it("has no duplicate slugs", () => {
    const slugs = SYSTEMS.map((s) => s.slug);
    expect(new Set(slugs).size).toBe(slugs.length);
  });

  it("resolves every slug via getSystem and the lookup map", () => {
    for (const system of SYSTEMS) {
      expect(getSystem(system.slug)).toBe(system);
      expect(SYSTEM_BY_SLUG[system.slug]).toBe(system);
    }
    expect(getSystem("does-not-exist")).toBeUndefined();
    expect(getSystem(undefined)).toBeUndefined();
  });
});

describe("Focus 5 systems — pricing", () => {
  it("each system has the exact opening price", () => {
    for (const system of SYSTEMS) {
      expect(system.startingPrice).toBe(EXPECTED_PRICES[system.slug]);
    }
  });

  it("formats a 'starts at' label with the SAR amount", () => {
    const revenue = getSystem("revenue-operating-system");
    expect(revenue).toBeDefined();
    expect(startingPriceLabel(revenue!)).toBe("يبدأ من 4,500 ر.س");
  });

  it("every price is a positive number and has an includes summary", () => {
    for (const system of SYSTEMS) {
      expect(system.startingPrice).toBeGreaterThan(0);
      expect(system.priceIncludes.trim().length).toBeGreaterThan(0);
    }
  });
});

describe("Focus 5 systems — required content", () => {
  it("each system has a non-empty delivery pack (>= 3 items)", () => {
    for (const system of SYSTEMS) {
      expect(system.deliveryPack.length).toBeGreaterThanOrEqual(3);
      for (const item of system.deliveryPack) {
        expect(item.trim().length).toBeGreaterThan(0);
      }
    }
  });

  it("each system has benefits, who-for, sprint outcome, CTA and FAQ", () => {
    for (const system of SYSTEMS) {
      expect(system.benefits.length).toBeGreaterThanOrEqual(3);
      expect(system.whoFor.length).toBeGreaterThanOrEqual(1);
      expect(system.sevenDayOutcome.trim().length).toBeGreaterThan(0);
      expect(system.pain.trim().length).toBeGreaterThan(0);
      expect(system.tagline.trim().length).toBeGreaterThan(0);
      expect(system.cta.trim().length).toBeGreaterThan(0);
      expect(system.sprintDuration.trim().length).toBeGreaterThan(0);
      expect(system.faq.length).toBeGreaterThanOrEqual(2);
      for (const entry of system.faq) {
        expect(entry.q.trim().length).toBeGreaterThan(0);
        expect(entry.a.trim().length).toBeGreaterThan(0);
      }
    }
  });

  it("each system has a reference cold-email angle", () => {
    for (const system of SYSTEMS) {
      expect(system.email.subject.trim().length).toBeGreaterThan(0);
      expect(system.email.body.trim().length).toBeGreaterThan(40);
    }
  });
});
