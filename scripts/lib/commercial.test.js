/**
 * Tests for the commercial safety library.
 * Dependency-free — run with:  node --test scripts/lib/
 */

import { test } from "node:test";
import assert from "node:assert/strict";

import {
  evaluateDraft,
  detectGuaranteedClaims,
  isFakeReplySubject,
  mentionsKnownOffer,
  isSuppressed,
} from "./commercial.js";

const OFFER_KEYWORDS = ["Revenue Intelligence Sprint", "Sprint", "Retainer"];
const NO_SUPPRESSION = { suppressed: [] };

function baseDraft(overrides = {}) {
  return {
    id: "OUT-T",
    company: "Test Co",
    pain: "Leads not converting",
    draft_subject: "وين تضيع فرص عملائك؟",
    draft_body: "السلام عليكم [الاسم]،\nنسوي Revenue Intelligence Sprint خلال 5 أيام.",
    status: "pending_approval",
    ...overrides,
  };
}

test("clean draft passes the gate", () => {
  const r = evaluateDraft(baseDraft(), {
    suppression: NO_SUPPRESSION,
    offerKeywords: OFFER_KEYWORDS,
  });
  assert.equal(r.pass, true);
  assert.equal(r.failures.length, 0);
});

test('Arabic guaranteed claim "نضمن زيادة المبيعات" fails', () => {
  const r = evaluateDraft(
    baseDraft({ draft_body: "نضمن زيادة المبيعات خلال شهر مع Sprint." }),
    { suppression: NO_SUPPRESSION, offerKeywords: OFFER_KEYWORDS },
  );
  assert.equal(r.pass, false);
  assert.ok(r.failures.some((f) => f.code === "QG-CLAIM" && f.severity === "CRITICAL"));
});

test('English "10x revenue" overclaim fails', () => {
  assert.ok(detectGuaranteedClaims("We deliver 10x revenue, guaranteed").length >= 1);
});

test('"risk-free" overclaim is detected', () => {
  assert.ok(detectGuaranteedClaims("a risk-free engagement").length >= 1);
});

test("fake Re:/Fwd: subjects are rejected", () => {
  assert.equal(isFakeReplySubject("Re: عرضنا"), true);
  assert.equal(isFakeReplySubject("FWD: proposal"), true);
  assert.equal(isFakeReplySubject("رد: المتابعة"), true);
  assert.equal(isFakeReplySubject("وين تضيع فرص عملائك؟"), false);
});

test("fake reply subject fails the full gate as CRITICAL", () => {
  const r = evaluateDraft(baseDraft({ draft_subject: "Re: متابعة" }), {
    suppression: NO_SUPPRESSION,
    offerKeywords: OFFER_KEYWORDS,
  });
  assert.ok(r.failures.some((f) => f.code === "QG-FAKE-REPLY" && f.severity === "CRITICAL"));
});

test("suppressed recipient can never be send-ready", () => {
  const suppression = {
    suppressed: [{ company: "Test Co", reason: "do_not_contact" }],
  };
  assert.ok(isSuppressed(baseDraft(), suppression));
  const r = evaluateDraft(baseDraft(), { suppression, offerKeywords: OFFER_KEYWORDS });
  assert.equal(r.pass, false);
  assert.equal(r.sendReady, false);
  assert.ok(r.failures.some((f) => f.code === "QG-SUPPRESSION"));
});

test("draft must map to a known offer", () => {
  assert.equal(mentionsKnownOffer("just a hello with no product", OFFER_KEYWORDS), false);
  const r = evaluateDraft(
    baseDraft({ draft_body: "السلام عليكم [الاسم]، مرحبا فقط." }),
    { suppression: NO_SUPPRESSION, offerKeywords: OFFER_KEYWORDS },
  );
  assert.ok(r.failures.some((f) => f.code === "QG-OFFER"));
});

test("already-sent draft is not approval-gated → CRITICAL", () => {
  const r = evaluateDraft(baseDraft({ status: "sent" }), {
    suppression: NO_SUPPRESSION,
    offerKeywords: OFFER_KEYWORDS,
  });
  assert.ok(r.failures.some((f) => f.code === "QG-APPROVAL" && f.severity === "CRITICAL"));
  assert.equal(r.sendReady, false);
});

test("missing personalization yields a warning, not a failure", () => {
  const r = evaluateDraft(
    baseDraft({ company: "", pain: "", draft_body: "نسوي Sprint للشركات." }),
    { suppression: NO_SUPPRESSION, offerKeywords: OFFER_KEYWORDS },
  );
  assert.ok(r.warnings.some((w) => w.code === "QG-PERSONALIZATION"));
});
