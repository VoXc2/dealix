'use strict';
/*
 * Dealix Market + Commercial shared library (dependency-free).
 * Loads canonical data and applies the draft/compliance gates. Used by the
 * commercial:* npm scripts. Mirrors the rules encoded in tests/ (pytest) and
 * docs/gtm/MARKET_PRODUCTION_NAMING_CONVENTIONS.md.
 *
 * Safety defaults everywhere: dry_run=true, approval_required=true, send_enabled=false.
 * These helpers are READ-ONLY: they never send, never write data, never touch secrets.
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..', '..');
const p = (rel) => path.join(ROOT, rel);
const readText = (rel) => fs.readFileSync(p(rel), 'utf8');
const readJson = (rel) => JSON.parse(readText(rel));
function readJsonl(rel) {
  return readText(rel)
    .split('\n')
    .map((s) => s.trim())
    .filter(Boolean)
    .map((l, i) => {
      try { return JSON.parse(l); }
      catch (e) { throw new Error(`Invalid JSON in ${rel} line ${i + 1}: ${e.message}`); }
    });
}

/*
 * Minimal extractor for a FLAT list of strings under a top-level key in our
 * simple YAML (e.g. forbidden_claims.yaml). Not a general YAML parser; it only
 * understands `key:` followed by `  - value` / `  - "value"` lines. A pytest
 * test cross-checks this against PyYAML so the two views never drift.
 */
function yamlStringList(rel, key) {
  const out = [];
  let inKey = false;
  for (const raw of readText(rel).split('\n')) {
    const line = raw.replace(/\s+$/, '');
    if (/^[A-Za-z0-9_]+:\s*$/.test(line)) { inKey = line.replace(/:\s*$/, '') === key; continue; }
    if (/^[A-Za-z0-9_]+:/.test(line)) { inKey = false; continue; }
    if (inKey) {
      const m = line.match(/^\s+-\s+(.*)$/);
      if (m) {
        let v = m[1].trim();
        if ((v.startsWith('"') && v.endsWith('"')) || (v.startsWith("'") && v.endsWith("'"))) v = v.slice(1, -1);
        out.push(v);
      }
    }
  }
  return out;
}

function forbiddenClaims() {
  const f = 'data/commercial/forbidden_claims.yaml';
  return {
    phrases: [...yamlStringList(f, 'forbidden_ar'), ...yamlStringList(f, 'forbidden_en')]
      .map((s) => s.toLowerCase()),
    subjectPrefixes: yamlStringList(f, 'forbidden_subject_prefixes').map((s) => s.toLowerCase()),
  };
}

function suppressionSet(rel = 'data/outreach/suppression_list.jsonl') {
  const s = new Set();
  for (const r of readJsonl(rel)) s.add(String(r.value).toLowerCase());
  return s;
}

const REQUIRED_DRAFT_FIELDS = [
  'prospect_id', 'company', 'sector', 'pain_hypothesis', 'offer_match',
  'personalization_score', 'evidence_level', 'risk_level', 'opt_out',
  'approval_status', 'send_status',
];
const COLD_TYPES = new Set(['first_touch', 'follow_up_1', 'follow_up_2']);
const DRAFT_MIX_TARGET = { first_touch: 100, follow_up_1: 75, follow_up_2: 50, proposal_intro: 15, close_loop: 10 };
const SENDABLE_VERDICTS = new Set(['LIMITED_SEND_READY', 'RAMP_READY']);

/* Apply all draft gates. Returns {ok, reasons[]}. Never sends. */
function gateDraft(d, ctx) {
  const reasons = [];
  const subj = String(d.subject || '').toLowerCase();
  const body = String(d.body || '').toLowerCase();

  for (const f of REQUIRED_DRAFT_FIELDS) {
    if (!(f in d) || d[f] === undefined || d[f] === null) { reasons.push('missing_required_field'); break; }
  }
  for (const ph of ctx.forbidden.phrases) {
    if (ph && (subj.includes(ph) || body.includes(ph))) { reasons.push('forbidden_claim'); break; }
  }
  for (const pre of ctx.forbidden.subjectPrefixes) {
    if (pre && subj.startsWith(pre)) { reasons.push('fake_thread'); break; }
  }
  if (d.personalization_score === 'P0') reasons.push('below_p1');
  if (COLD_TYPES.has(d.draft_type)) {
    const opt = d.opt_out || {};
    if (!opt.included) reasons.push('missing_unsubscribe');
  }
  const dom = String(d.recipient_domain || '').toLowerCase();
  const comp = String(d.company || '').toLowerCase();
  if ((dom && ctx.suppression.has(dom)) || (comp && ctx.suppression.has(comp))) reasons.push('suppressed');

  return { ok: reasons.length === 0, reasons: [...new Set(reasons)] };
}

function gateContext() {
  return { forbidden: forbiddenClaims(), suppression: suppressionSet() };
}

export {
  ROOT, p, readText, readJson, readJsonl, yamlStringList,
  forbiddenClaims, suppressionSet, gateDraft, gateContext,
  REQUIRED_DRAFT_FIELDS, COLD_TYPES, DRAFT_MIX_TARGET, SENDABLE_VERDICTS,
};
