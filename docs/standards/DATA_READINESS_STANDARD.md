# Data Readiness Standard

**مصدر الحقيقة التفصيلي:** [`../data/DATA_READINESS_STANDARD.md`](../data/DATA_READINESS_STANDARD.md)

**عنصر مرتبط:** [`SOURCE_PASSPORT_STANDARD.md`](SOURCE_PASSPORT_STANDARD.md) · [`../architecture/SOURCE_PASSPORT.md`](../architecture/SOURCE_PASSPORT.md)

## مقاييس

source clarity · completeness · duplicates · missing fields · PII status · allowed use · format quality · update frequency.

## Data Readiness Score (تفسير)

- **85–100:** Ready for AI workflow  
- **70–84:** usable with cleanup  
- **50–69:** diagnostic only  
- **‏‏<50:** data readiness sprint first  

## القاعدة

```text
No AI workflow on unclear data.
```

**سياق سعودي:** **31%** فقط من عينة تجارة إلكترونية أعلنت كل العناصر الأربعة في سياسات الخصوصية — [arXiv:2602.18616](https://arxiv.org/abs/2602.18616).

**الكود:** `data_readiness_score_band` — `standards_os/data_readiness_standard.py`

**صعود:** [`DEALIX_GOVERNED_AI_OPERATIONS_STANDARD.md`](DEALIX_GOVERNED_AI_OPERATIONS_STANDARD.md)