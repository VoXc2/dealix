import { describe, it, expect } from "vitest";
import { readFileSync, existsSync } from "node:fs";
import { resolve } from "node:path";

const repoRoot = resolve(import.meta.dirname, "..");

// Every doc + report that the Focus 5 market-entry layer must ship.
const DELIVERABLES = [
  "docs/commercial/FOCUS_5_SYSTEMS_MARKET_ENTRY_AR.md",
  "docs/commercial/SYSTEM_PRICING_STARTER_AR.md",
  "docs/commercial/SYSTEM_DELIVERY_PACKS_AR.md",
  "docs/outreach/DAILY_400_SYSTEM_DRAFT_FACTORY_AR.md",
  "docs/outreach/SYSTEM_BASED_CLIENT_NEED_CARD_AR.md",
  "docs/outreach/FOCUS_5_COLD_EMAIL_LIBRARY_AR.md",
  "docs/gtm/FOCUS_5_SAUDI_LAUNCH_PLAN_AR.md",
  "reports/commercial/FOCUS_5_SYSTEMS_REVIEW.md",
  "reports/outreach/DAILY_400_SYSTEM_DRAFT_PRODUCTION.md",
  "reports/outreach/TOP_100_SYSTEM_APPROVAL_QUEUE.md",
  "reports/outreach/SYSTEM_BASED_CLIENT_NEED_CARDS.md",
  "reports/gtm/FOCUS_5_LAUNCH_READINESS.md",
  "reports/gtm/FOCUS_5_MARKET_LAUNCH_FINAL_REPORT.md",
];

// Frontend artifacts that must exist for the systems + pricing surface.
const FRONTEND_FILES = [
  "src/data/systems.ts",
  "src/data/draftFactory.ts",
  "src/pages/Systems.tsx",
  "src/pages/SystemDetail.tsx",
  "src/pages/Pricing.tsx",
  "src/components/systems/SystemCard.tsx",
  "src/components/systems/SystemHero.tsx",
  "src/components/systems/SystemBenefits.tsx",
  "src/components/systems/SystemPricing.tsx",
  "src/components/systems/SystemDeliveryPack.tsx",
];

describe("Focus 5 deliverables — docs & reports", () => {
  for (const relative of DELIVERABLES) {
    it(`${relative} exists and has real content`, () => {
      const full = resolve(repoRoot, relative);
      expect(existsSync(full), `missing ${relative}`).toBe(true);
      const content = readFileSync(full, "utf8");
      expect(content.length).toBeGreaterThan(400);
    });
  }
});

describe("Focus 5 deliverables — frontend files", () => {
  for (const relative of FRONTEND_FILES) {
    it(`${relative} exists`, () => {
      expect(existsSync(resolve(repoRoot, relative)), `missing ${relative}`).toBe(
        true,
      );
    });
  }
});
