import { describe, it, expect } from "vitest";
import {
  DAILY_DRAFT_TOTAL,
  SEND_DEFAULT_ENABLED,
  DRAFT_DISTRIBUTION,
  SEND_RAMP,
  SEND_SAFETY_GATES,
  PROHIBITED_PRACTICES,
  CLIENT_NEED_CARD_FIELDS,
  APPROVAL_RANKING_SIGNALS,
  totalAllocatedDrafts,
} from "@/data/draftFactory";
import { SYSTEM_BY_SLUG } from "@/data/systems";

describe("Daily 400 draft factory — volume", () => {
  it("produces 400 drafts per day", () => {
    expect(DAILY_DRAFT_TOTAL).toBe(400);
  });

  it("per-system distribution sums to the daily total", () => {
    expect(totalAllocatedDrafts()).toBe(DAILY_DRAFT_TOTAL);
  });

  it("matches the agreed per-system allocation", () => {
    const map = Object.fromEntries(
      DRAFT_DISTRIBUTION.map((d) => [d.slug, d.drafts]),
    );
    expect(map).toEqual({
      "revenue-operating-system": 100,
      "follow-up-recovery-os": 90,
      "executive-command-os": 70,
      "whatsapp-client-os": 70,
      "proposal-proof-os": 70,
    });
  });

  it("only allocates to real systems and mirrors each system's dailyDrafts", () => {
    for (const allocation of DRAFT_DISTRIBUTION) {
      const system = SYSTEM_BY_SLUG[allocation.slug];
      expect(system, `unknown slug ${allocation.slug}`).toBeDefined();
      expect(system.dailyDrafts).toBe(allocation.drafts);
    }
  });
});

describe("Daily 400 draft factory — draft-only safety", () => {
  it("does NOT enable sends by default", () => {
    expect(SEND_DEFAULT_ENABLED).toBe(false);
  });

  it("requires the core send safety gates", () => {
    const gates = SEND_SAFETY_GATES.join(" | ").toLowerCase();
    expect(gates).toContain("approval");
    expect(gates).toContain("unsubscribe");
    expect(gates).toContain("suppression");
    expect(gates).toContain("spf");
    expect(gates).toContain("dkim");
    expect(gates).toContain("dmarc");
    expect(gates).toContain("domain health");
    expect(SEND_SAFETY_GATES.length).toBeGreaterThanOrEqual(5);
  });

  it("keeps drafts constant while ramping sends gradually", () => {
    expect(SEND_RAMP.length).toBeGreaterThanOrEqual(4);
    // The first phase must start with a small send volume, not the full 400.
    const first = SEND_RAMP[0];
    expect(first.sendsPerDay).toMatch(/20|40/);
    expect(first.draftsPerDay).toContain("400");
  });

  it("explicitly prohibits cold WhatsApp, LinkedIn automation, purchased lists and fake Re/Fwd", () => {
    const text = PROHIBITED_PRACTICES.join(" | ");
    expect(text).toMatch(/WhatsApp/i);
    expect(text).toMatch(/LinkedIn/i);
    expect(text).toMatch(/purchased lists/i);
    expect(text).toMatch(/Re:\/Fwd:/i);
  });
});

describe("Daily 400 draft factory — client need card", () => {
  it("requires the full set of personalization + governance fields", () => {
    const required = [
      "company",
      "sector",
      "country",
      "city",
      "signal",
      "likely_pain",
      "recommended_system",
      "why_this_system",
      "first_mission",
      "proof_angle",
      "email_angle",
      "cta",
      "risk_level",
      "evidence_level",
      "approval_status",
      "send_readiness",
    ];
    for (const field of required) {
      expect(CLIENT_NEED_CARD_FIELDS).toContain(field);
    }
  });

  it("ranks the approval queue on clear buying / payment / risk signals", () => {
    expect(APPROVAL_RANKING_SIGNALS.length).toBeGreaterThanOrEqual(4);
  });
});
