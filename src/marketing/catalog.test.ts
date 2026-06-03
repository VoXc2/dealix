import { describe, it, expect } from "vitest";
import { coreSystems, sectorSolutions } from "./catalog";

// These tests guard the public/internal boundary: the website must expose the
// 5 core systems + 20 sectors, and must never leak internal system ids.
const INTERNAL_SYSTEM_IDS = [
  "sales-process-os", "customer-data-os", "revenue-leak-map", "pricing-os",
  "speed-to-lead-os", "whatsapp-inbox-os", "proposal-builder-os",
];

describe("public marketing catalog", () => {
  it("exposes exactly the 5 core systems", () => {
    expect(coreSystems).toHaveLength(5);
    for (const c of coreSystems) {
      expect(c.id).toBeTruthy();
      expect(c.nameAr).toBeTruthy();
      expect(c.promiseAr.length).toBeGreaterThan(10);
    }
  });

  it("exposes 20 sector solutions, each with needs and core systems", () => {
    expect(sectorSolutions).toHaveLength(20);
    for (const s of sectorSolutions) {
      expect(s.needs.length).toBeGreaterThan(0);
      expect(s.coreSystems.length).toBeGreaterThan(0);
      for (const c of s.coreSystems) {
        expect(coreSystems.map((x) => x.id)).toContain(c);
      }
    }
  });

  it("maps every sector need to a valid core system", () => {
    const coreIds = new Set(coreSystems.map((c) => c.id));
    for (const s of sectorSolutions) {
      for (const n of s.needs) {
        expect(coreIds.has(n.coreSystem)).toBe(true);
      }
    }
  });

  it("never leaks internal system ids into the public catalog", () => {
    const blob = JSON.stringify({ coreSystems, sectorSolutions });
    for (const id of INTERNAL_SYSTEM_IDS) {
      expect(blob).not.toContain(id);
    }
  });
});
