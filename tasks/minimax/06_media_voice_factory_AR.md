# MiniMax Sub-prompt 06 — Sales Media Factory (deferred, drafts only)

> **Scope:** List the *drafts* the founder can request MiniMax to produce in v0. No video / voice / music production in this PR.
> **Branch:** `feature/minimax-factory-p0-hardening`

---

## 1. Objective

MiniMax's full media surface (text-to-video, TTS, music, image) is a P3 concern. In this PR we ship the **draft catalog** so the founder can request the right artifact on the right channel without having to remember the menu.

We do **not** wire any media generation API in this PR. We only:
- enumerate the 15 drafts MiniMax can produce on demand,
- define the schema for each (title, length, channel, language, evidence_level, approval_required),
- put them under `data/ai_ops/media_drafts_catalog.yaml`.

---

## 2. Files to Create

### 2.1 `data/ai_ops/media_drafts_catalog.yaml`

15 entries. Each:

```yaml
- id: explainer_30s
  title: "وش Dealix؟ 30 ثانية"
  channel: linkedin_video
  language: ar
  length_seconds: 30
  evidence_level: L2
  approval_required: true
  format: script_only
  notes: "نص فقط، لا فيديو في هذا الـ PR"
```

(Include all 15 from the master brief: explainer 30s/60s/90s, voiceover AR, sales explainer, demo walkthrough, landing copy AR/EN, case study template, founder LinkedIn posts, cold email variants, WhatsApp consent onboarding copy, webinar outline, investor one-pager, client FAQ, objection handling cards.)

### 2.2 `docs/ai/MEDIA_DRAFTS_CATALOG_AR.md`

Short doc explaining how to use the catalog:
1. How to pick an entry by id.
2. How to feed it to MiniMax (text-only, no media APIs yet).
3. Where the output lands (`reports/media_drafts/<id>_<date>.md`).
4. What `evidence_level` and `approval_required` mean.

---

## 3. Constraints

- No media generation API in this PR. Drafts only.
- No real video/voice/music files committed.
- Under 120 lines per file.

---

## 4. Acceptance

```bash
test -f data/ai_ops/media_drafts_catalog.yaml
test -f docs/ai/MEDIA_DRAFTS_CATALOG_AR.md
python -c "import yaml; d=yaml.safe_load(open('data/ai_ops/media_drafts_catalog.yaml')); assert len(d) >= 15, 'must have at least 15 entries'"
```

---

## 5. Future Work (Not in This PR)

When the founder explicitly enables media generation (e.g. sets `MINIMAX_VIDEO_API_KEY` and approves a cost guard), the next sub-prompt will:
- Wire `dealix/hermes/providers/minimax_video_provider.py`.
- Add cost guard (per-video cap).
- Add approval queue for video generation requests.
- Add eval dataset for video safety (no PII, no medical/legal/financial claims).
