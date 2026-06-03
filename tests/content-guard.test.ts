import { describe, it, expect } from "vitest";
import { SYSTEMS, type BusinessSystem } from "@/data/systems";

// Flatten every customer-facing string of a system into one searchable blob.
function customerCopy(system: BusinessSystem): string {
  return [
    system.name,
    system.nameAr,
    system.tagline,
    system.pain,
    system.bestIf,
    system.firstResult,
    system.priceIncludes,
    system.cta,
    system.sevenDayOutcome,
    ...system.whoFor,
    ...system.benefits,
    ...system.deliveryPack,
    system.email.subject,
    system.email.body,
    ...system.faq.flatMap((f) => [f.q, f.a]),
  ].join("\n");
}

// Phrases that would constitute a guaranteed-result claim.
const GUARANTEE_TOKENS = [
  "نضمن",
  "مضمون", // covers مضمونة / مضمونه
  "ضمان",
  "guarantee",
  "guaranteed",
  "100%",
];

// Internal module / agent / file identifiers that must never reach customers.
const INTERNAL_IDENTIFIERS = [
  "prospect_research",
  "war_room",
  "war room",
  "ai_action_ledger",
  "approval_queue",
  "agent_permissions",
  "outreach_queue",
  "pending_approval",
  "draft_body",
  "draft_subject",
  "company_os",
  "revenue_scorecard",
  "governance_check",
];

describe("Customer copy — no guaranteed claims", () => {
  for (const system of SYSTEMS) {
    it(`${system.slug} makes no guaranteed-result claim`, () => {
      const copy = customerCopy(system).toLowerCase();
      for (const token of GUARANTEE_TOKENS) {
        expect(
          copy.includes(token.toLowerCase()),
          `"${token}" found in ${system.slug} copy`,
        ).toBe(false);
      }
    });
  }
});

describe("Customer copy — no internal module names leaked", () => {
  for (const system of SYSTEMS) {
    it(`${system.slug} exposes no internal identifiers`, () => {
      const copy = customerCopy(system).toLowerCase();
      for (const token of INTERNAL_IDENTIFIERS) {
        expect(
          copy.includes(token.toLowerCase()),
          `"${token}" found in ${system.slug} copy`,
        ).toBe(false);
      }
    });
  }
});
