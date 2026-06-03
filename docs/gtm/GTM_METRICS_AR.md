# مقاييس GTM — Metric Definitions

تعريفات موحّدة للمقاييس حتى تعني الأرقام نفس الشيء في كل تقرير. كل مقياس له:
الاسم، التعريف، المصدر، والهدف الأوّلي (قابل للتعديل بموافقة المؤسّس).

## مقاييس الإنتاج (Production)
| المقياس | التعريف | المصدر | هدف أوّلي |
|---------|---------|--------|-----------|
| `drafts_produced` | عدد المسودّات المنتَجة اليوم | `data/outreach/drafts.jsonl` | 250/يوم |
| `draft_mix_compliance` | مطابقة المزيج (100/75/50/15/10) | gate | 100% |
| `gate_pass_rate` | نسبة المسودّات التي اجتازت كل البوّابات | `DRAFT_GATE_REVIEW.md` | ≥ 80% |
| `personalization_floor` | نسبة المسودّات ≥ P1 | gate | 100% |

## مقاييس الجودة والأمان (Quality & Safety)
| المقياس | التعريف | الهدف |
|---------|---------|-------|
| `forbidden_claim_hits` | عدد الـ claims الممنوعة المكتشفة | **0** (إلزامي) |
| `missing_unsubscribe` | مسودّات cold بلا opt-out | **0** (إلزامي) |
| `suppression_violations` | محاولات إرسال لمستلم مكتوم | **0** (إلزامي) |
| `pii_in_reports` | كشف PII في التقارير | **0** (إلزامي) |

## مقاييس قابلية التسليم (Deliverability)
| المقياس | التعريف | الهدف |
|---------|---------|-------|
| `deliverability_verdict` | الحُكم الحالي | ≥ `DRY_RUN_ONLY` |
| `bounce_rate` | الارتداد | < 2% |
| `spam_complaint_rate` | الشكاوى | < 0.1% |
| `domain_health` | SPF/DKIM/DMARC | كلها PASS قبل أي إرسال |

## مقاييس خط الأنابيب (Pipeline)
| المقياس | التعريف |
|---------|---------|
| `reply_rate` | الردود ÷ المُرسَل (بعد بدء الإرسال) |
| `positive_reply_rate` | الردود الإيجابية ÷ المُرسَل |
| `discovery_booked` | عدد جلسات الاكتشاف المحجوزة |
| `proposal_sent` | العروض المُرسَلة (بعد الموافقة) |
| `win_rate` | المكسوبة ÷ العروض |
| `pipeline_value_sar` | قيمة خط الأنابيب بالريال |

## مقاييس القنوات (Channel ROI)
`content_engagement` · `press_mentions` (عند توفّر proof) · `partner_sourced_pipeline`.

## قواعد القياس
- لا قياس لمعدّلات الإرسال/الرد قبل تفعيل الإرسال المعتمد — تبقى "غير مفعّلة" في التقارير.
- المقاييس الإلزامية (forbidden_claim_hits, missing_unsubscribe, suppression_violations,
  pii_in_reports) هي **بوّابات صفرية**: أي قيمة > 0 توقف خطة الإرسال.
