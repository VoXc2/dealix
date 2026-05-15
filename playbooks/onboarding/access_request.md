# العربية

# طلب الصلاحيات — Layer 10 / مرحلة التهيئة

**المالك:** قائد التسليم (Delivery Lead)
**الجمهور:** عضو الفريق الذي ينسّق صلاحيات الأنظمة قبل التسليم
**المراجع:** `playbooks/onboarding/data_request.md` · `playbooks/onboarding/kickoff.md` · `clients/_TEMPLATE/02_data_request.md` · `docs/PILOT_DELIVERY_SOP.md`

> الغرض: طلب موحّد لأقل صلاحية لازمة، بمبدأ «الحد الأدنى من الصلاحيات» — حتى لا يعتمد التسليم على وصول مفتوح أو غير موثَّق.

## 1. متى يُستخدم هذا الدليل

بعد اجتماع الانطلاق، بالتوازي مع طلب البيانات. يُستخدم فقط عندما يتطلب المخرَج وصولاً لنظام يملكه العميل.

## 2. مبدأ الحد الأدنى من الصلاحيات

اطلب أدنى مستوى وصول يكفي للمخرَج (قراءة فقط حيثما أمكن). لا تطلب صلاحية إدارية إذا كان التصدير يكفي.

## 3. أنواع الصلاحيات الشائعة

| النوع | المستوى المفضّل | البديل الأبسط |
|---|---|---|
| نظام إدارة العملاء (CRM) | قراءة فقط | تصدير CSV من العميل |
| بريد / قنوات الرسائل | لا وصول | العميل يرسل بنفسه |
| لوحات البيانات | قراءة فقط | لقطات شاشة مرسلة |

## 4. خطوات الطلب (خطوة بخطوة)

1. حدّد المخرَج الذي يتطلب وصولاً والنظام المعني فقط.
2. اطلب أدنى مستوى وصول كافٍ، مع تاريخ انتهاء واضح.
3. وثّق من منح الصلاحية ومتى ولأي غرض.
4. فضّل التصدير اليدوي من العميل بدلاً من الوصول المباشر متى أمكن.
5. سجّل منح الصلاحية في سجل حوكمة العميل.
6. جدول إلغاء الصلاحية عند انتهاء الارتباط.

## 5. القواعد الحاكمة (Non-negotiables)

- لا أتمتة على LinkedIn ولا وصول لقنوات الرسائل لإرسال نيابة عن العميل.
- لا صلاحيات إدارية ما لم يكن المخرَج يتطلبها صراحةً.
- لا مشاركة بيانات الدخول عبر قنوات غير آمنة.
- كل صلاحية لها تاريخ انتهاء وتُلغى عند الإنهاء.
- العميل وحده يرسل أي رسالة خارجية — Dealix لا يرسل تلقائياً.

## 6. معايير القبول (قائمة الجاهزية)

- [ ] كل صلاحية مربوطة بمخرَج محدد.
- [ ] مستوى الوصول هو الأدنى الكافي.
- [ ] منح الصلاحية موثَّق في `governance_events.md`.
- [ ] تاريخ انتهاء/إلغاء محدد لكل صلاحية.
- [ ] بيانات الدخول نُقلت عبر قناة آمنة.

## 7. المقاييس

- زمن منح الصلاحيات: من الطلب إلى التفعيل (الهدف ≤ 24 ساعة).
- نسبة الصلاحيات بمستوى «قراءة فقط» أو أدنى.
- نسبة الصلاحيات المُلغاة في موعدها بعد الإنهاء.

## 8. خطافات المراقبة (Observability)

- سجّل حالة كل صلاحية: `requested` / `granted` / `revoked`.
- مراجعة أسبوعية للصلاحيات النشطة وتواريخ انتهائها.
- تنبيه عند تجاوز صلاحية تاريخ انتهائها دون إلغاء.

## 9. إجراء التراجع (Rollback)

إذا مُنحت صلاحية أوسع من اللازم أو لم تُلغَ في موعدها:
1. اطلب من العميل خفض أو إلغاء الصلاحية فوراً.
2. سجّل الحادثة في سجل الحوكمة.
3. راجع الطلب لتحديد سبب الإفراط قبل العميل التالي.

# English

# Access Request — Layer 10 / Onboarding Stage

**Owner:** Delivery Lead
**Audience:** Team member coordinating system access before delivery
**References:** `playbooks/onboarding/data_request.md` · `playbooks/onboarding/kickoff.md` · `clients/_TEMPLATE/02_data_request.md` · `docs/PILOT_DELIVERY_SOP.md`

> Purpose: a standard request for the minimum access needed, on a least-privilege principle — so delivery never depends on open or undocumented access.

## 1. When to use this playbook

After the Kick-off meeting, in parallel with the data request. Use it only when a deliverable requires access to a system the client owns.

## 2. Least-privilege principle

Request the lowest access level sufficient for the deliverable (read-only wherever possible). Do not request admin rights when an export will do.

## 3. Common access types

| Type | Preferred level | Simpler alternative |
|---|---|---|
| CRM | Read-only | Client-supplied CSV export |
| Email / messaging channels | No access | Client sends themselves |
| Dashboards | Read-only | Screenshots supplied |

## 4. Request steps (step by step)

1. Identify only the deliverable that needs access and the system involved.
2. Request the lowest sufficient access level, with a clear expiry date.
3. Document who granted access, when, and for what purpose.
4. Prefer a manual export from the client over direct access where possible.
5. Log the access grant in the client governance log.
6. Schedule access revocation at the end of the engagement.

## 5. Governance rules (non-negotiables)

- No LinkedIn automation and no messaging-channel access to send on the client's behalf.
- No admin rights unless the deliverable explicitly requires them.
- No login credentials shared over insecure channels.
- Every grant has an expiry date and is revoked on offboarding.
- The client alone sends any external message — Dealix never sends automatically.

## 6. Acceptance criteria (readiness checklist)

- [ ] Every grant tied to a specific deliverable.
- [ ] Access level is the lowest sufficient.
- [ ] Grant documented in `governance_events.md`.
- [ ] Expiry/revocation date set for every grant.
- [ ] Credentials transferred over a secure channel.

## 7. Metrics

- Access grant time: request to activation (target ≤ 24 hours).
- Share of grants at "read-only" level or lower.
- Share of grants revoked on time after offboarding.

## 8. Observability hooks

- Log each access state: `requested` / `granted` / `revoked`.
- Weekly review of active grants and their expiry dates.
- Alert when a grant passes its expiry date without revocation.

## 9. Rollback procedure

If access broader than needed was granted, or not revoked on time:
1. Ask the client to reduce or revoke the access immediately.
2. Record the incident in the governance log.
3. Review the request to find the cause of over-provisioning before the next client.
