# Data Lifecycle Policy (AR)

---

## 1. Stages

```
[COLLECT] → [CLASSIFY] → [STORE] → [USE] → [SHARE] → [ARCHIVE] → [DELETE]
   ↓           ↓            ↓        ↓        ↓          ↓           ↓
 validate    tag D-class  encrypt  purpose  allowlist  retention  audit + 
 intent                  at-rest   limited             timer      confirm
```

## 2. Collection Principles

- **Minimum necessary:** نجمع فقط ما نحتاج للمهمة
- **Purpose declared:** لماذا نجمع، يُسجّل
- **Consent:** حيث يلزم (D2+)
- **Validation:** على الـ intake (regex, type)
- **No forbidden:** D6 blocked at intake

## 3. Storage Principles

- **At-rest encryption:** default (provider-managed)
- **Field-level encryption:** D4+ (E4+)
- **Tenant scoping:** enforced at DB level
- **Backups:** encrypted, tested restore

## 4. Use Principles

- **Purpose limitation:** لا استخدام خارج الغرض المُعلن
- **Least privilege:** access only لما يحتاج
- **Audit:** كل privileged access
- **Cache:** لا تخزين طويل لـ PII في cache

## 5. Share Principles

- **Sub-processor allowlist:** DPA-signed فقط
- **Cross-tenant:** forbidden بدون approval
- **Public reports:** aggregated, anonymized
- **Client data export:** with purpose + audit

## 6. Archive Principles

- **Inactive data:** moved to cold storage بعد 12 شهر
- **Hot data:** active client + recent prospects
- **Retrieval:** time-bound, audited

## 7. Deletion Principles

- **Soft delete default:** 30-day window
- **Hard delete:** via retention policy OR PDPL request
- **Cascade:** delete children when parent deleted
- **Backup deletion:** within backup retention
- **Audit:** deletion event recorded

## 8. Subject Rights (PDPL/GDPR-style)

- **Access:** export within 30 days
- **Rectification:** update via portal
- **Erasure:** "right to be forgotten" workflow
- **Restriction:** opt-out flag
- **Portability:** JSON/CSV export
- **Objection:** suppression list
- **Withdraw consent:** opt-out

## 9. Cross-Border Transfers

- **KSA default:** البيانات تبقى في KSA حيث ممكن
- **Sub-processor outside KSA:** with DPA + redaction + SCCs
- **Adequacy:** respect NDMO decisions
- **Logging:** every cross-border transfer logged

## 10. Honesty Statement

- لا نبيع بيانات
- لا نشارك مع غير مذكورين
- لا نستخدم لتدريب بدون موافقة
- نحذف عند الطلب

---

> **Owner:** Data Lead + Privacy Officer · **Review:** كل 90 يوم
