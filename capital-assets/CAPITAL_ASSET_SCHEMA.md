# مرجع المخطط — Capital Asset Schema Reference

> مصدر الحقيقة: [`auto_client_acquisition/capital_os/capital_asset.py`](../auto_client_acquisition/capital_os/capital_asset.py)
> آخر مراجعة: 2026-05-14

---

## ١. حقول `CapitalAsset` (AR)

| الحقل | النوع | التعريف |
|---|---|---|
| `asset_id` | `str` | معرّف فريد بصيغة `CAP-NNN` (مثلاً `CAP-001`). |
| `name` | `str` | الاسم القانوني للأصل كما يظهر في الواجهة العامة. |
| `type` | `AssetType` | واحد من ١١ نوعاً استراتيجياً (trust، sales، product، doctrine، proof، partner، investor، hiring، standard، market، revenue_ops). |
| `strategic_role` | `str` | جملة واحدة تشرح لماذا هذا الأصل موجود — الدور الذي يلعبه في حلقة القيمة. |
| `file_paths` | `tuple[str, ...]` | مسارات ملفات حقيقية في المستودع. المُدقِّق يرفض الإدخال إن لم تكن موجودة. |
| `buyer_relevance` | `tuple[str, ...]` | الأرشيتايبات التي يهمّها هذا الأصل (CISO، DPO، Big 4، VC، إلخ). |
| `commercial_use` | `tuple[str, ...]` | كيف يُستخدم الأصل تجارياً (إثبات ثقة، توليد عرض، فتح صفقة، إلخ). |
| `maturity` | `AssetMaturity` | `live` أو `draft` أو `planned` أو `deprecated`. |
| `linked_non_negotiables` | `tuple[str, ...]` | معرّفات الخطوط الحمراء الـ١١ التي يُنفِّذها هذا الأصل. |
| `proof_level` | `ProofLevel` | `test-backed` (الأقوى) أو `code-backed` أو `doc-backed` أو `process-backed`. |
| `last_reviewed` | `str` | تاريخ ISO (YYYY-MM-DD) لآخر مراجعة. |
| `public` | `bool` | افتراضي `False`. عند `True` فقط يظهر الأصل على `/api/v1/capital-assets/public`. |

## 2. `CapitalAsset` fields (EN)

| Field | Type | Definition |
|---|---|---|
| `asset_id` | `str` | Unique id in `CAP-NNN` form (e.g. `CAP-001`). |
| `name` | `str` | Canonical asset name as it surfaces on the public API. |
| `type` | `AssetType` | One of 11 strategic types (trust, sales, product, doctrine, proof, partner, investor, hiring, standard, market, revenue_ops). |
| `strategic_role` | `str` | One-sentence statement of why the asset exists — the role it plays in the value loop. |
| `file_paths` | `tuple[str, ...]` | Real repo paths. The validator rejects entries whose paths don't resolve. |
| `buyer_relevance` | `tuple[str, ...]` | Archetypes that care about this asset (CISO, DPO, Big 4, VC, etc). |
| `commercial_use` | `tuple[str, ...]` | How the asset is used commercially (trust proof, proposal generation, deal unlock, etc). |
| `maturity` | `AssetMaturity` | `live`, `draft`, `planned`, or `deprecated`. |
| `linked_non_negotiables` | `tuple[str, ...]` | Ids of the 11 non-negotiables this asset enforces. |
| `proof_level` | `ProofLevel` | `test-backed` (strongest), `code-backed`, `doc-backed`, or `process-backed`. |
| `last_reviewed` | `str` | ISO date (YYYY-MM-DD) of the last review. |
| `public` | `bool` | Default `False`. Only `True` exposes the asset on `/api/v1/capital-assets/public`. |

---

## ٣. مثال محلول — Worked example

```python
CapitalAsset(
    asset_id="CAP-001",
    name="Dealix Promise API",
    type="trust_asset",
    strategic_role=(
        "public doctrine verification surface — any CISO can "
        "curl-verify the 11 commitments against the test files "
        "that enforce each"
    ),
    file_paths=(
        "api/routers/dealix_promise.py",
        "auto_client_acquisition/governance_os/non_negotiables.py",
        "tests/test_dealix_promise.py",
        "landing/promise.html",
    ),
    buyer_relevance=("CISO", "DPO", "regulated buyer", "Big 4 advisory", "VC due diligence"),
    commercial_use=("trust proof", "partner diligence", "investor evidence", "procurement bypass"),
    maturity="live",
    linked_non_negotiables=(
        "no_scraping", "no_cold_whatsapp", "no_linkedin_automation",
        "no_unsourced_claims", "no_guaranteed_outcomes", "no_pii_in_logs",
        "no_sourceless_ai", "no_external_action_without_approval",
        "no_agent_without_identity", "no_project_without_proof_pack",
        "no_project_without_capital_asset",
    ),
    proof_level="test-backed",
    last_reviewed="2026-05-14",
    public=True,
)
```

## ٤. قواعد المُدقِّق (AR) / Validator rules (EN)

- **AR:** كل أصل يجب أن يحمل (١) مسارات ملفات حقيقية، (٢) خطاً أحمر واحداً على الأقل مرتبطاً به، (٣) تاريخ مراجعة ISO، (٤) `proof_level` صريحاً.
- **EN:** Every asset must carry (1) real file paths, (2) at least one linked non-negotiable, (3) an ISO `last_reviewed` date, (4) an explicit `proof_level`.

---

*Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة.*
