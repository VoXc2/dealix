"use client";

import { useLocale } from "next-intl";

interface TrustItem {
  id: string;
  titleAr: string;
  titleEn: string;
  statusAr: string;
  statusEn: string;
  bodyAr: string;
  bodyEn: string;
}

const TRUST_ITEMS: TrustItem[] = [
  {
    id: "pdpl",
    titleAr: "ضوابط حماية البيانات الشخصية",
    titleEn: "Personal Data Protection Controls",
    statusAr: "دعم امتثال — ليس شهادة",
    statusEn: "Compliance Support — Not a Certification",
    bodyAr:
      "تتضمن Dealix ضوابط للموافقة، السجلات، الحذف، التصدير، وحوكمة معالجة البيانات. حالة الامتثال لنظام PDPL تعتمد على الجهة، الغرض، البيانات، الموردين، العقود، والنشر الفعلي، لذلك لا نستخدم ادعاء امتثال شامل بدون دليل خاص بالنطاق.",
    bodyEn:
      "Dealix includes consent, audit, erasure, export, and processing-governance controls. PDPL compliance depends on the entity, purpose, data, vendors, contracts, and actual deployment, so we do not claim blanket compliance without scope-specific evidence.",
  },
  {
    id: "zatca",
    titleAr: "جاهزية الفوترة الإلكترونية",
    titleEn: "E-Invoicing Readiness",
    statusAr: "دعم جاهزية — تحقق لكل عميل",
    statusEn: "Readiness Support — Verify per Customer",
    bodyAr:
      "يمكن لـ Dealix دعم تدفقات الجاهزية والتكامل والأدلة المرتبطة بالفوترة الإلكترونية. أهلية الموجة، متطلبات التكامل، وحالة الامتثال لا تُفترض تلقائياً وتُتحقق للعميل والنشر المعني.",
    bodyEn:
      "Dealix can support e-invoicing readiness, integration, and evidence workflows. Wave eligibility, integration requirements, and compliance status are not assumed and must be verified for the specific customer and deployment.",
  },
  {
    id: "cyber",
    titleAr: "حوكمة وأمن AI",
    titleEn: "AI Governance & Cybersecurity",
    statusAr: "ضوابط وتقييم فجوات",
    statusEn: "Controls & Gap Assessment",
    bodyAr:
      "نستخدم حدود صلاحية، موافقات، عزل تنفيذ، وسجلات أدلة لدعم المراجعة الأمنية وحوكمة الوكلاء. مواءمة الضوابط لا تعني اعتماداً أو شهادة من NCA أو أي جهة أخرى.",
    bodyEn:
      "We use authority boundaries, approvals, isolated execution, and evidence trails to support security review and agent governance. Control mapping does not imply NCA or other regulator certification.",
  },
  {
    id: "assurance",
    titleAr: "الشهادات والضمانات",
    titleEn: "Certifications & Assurance",
    statusAr: "الدليل قبل الادعاء",
    statusEn: "Evidence Before Claims",
    bodyAr:
      "أي شهادة، إقامة بيانات، SLO، نتيجة أمنية، أو ادعاء امتثال يُعرض فقط عندما توجد أدلة حديثة ومحددة للنطاق. البنود غير المثبتة تبقى UNKNOWN/HOLD ولا تتحول إلى علامة ثقة تسويقية.",
    bodyEn:
      "Any certification, data-residency, SLO, security-result, or compliance claim is shown only when current scope-specific evidence exists. Unverified items remain UNKNOWN/HOLD rather than becoming marketing trust badges.",
  },
];

const OPERATING_RULES = [
  {
    ar: "الموافقة أولاً للأفعال الخارجية والمادية",
    en: "Approval-first for external and material effects",
  },
  {
    ar: "لا WhatsApp بارد ولا scraping لبيانات شخصية",
    en: "No cold WhatsApp and no personal-data scraping",
  },
  {
    ar: "Draft ≠ Sent · Quote ≠ Invoice · Payment ≠ Revenue",
    en: "Draft ≠ Sent · Quote ≠ Invoice · Payment ≠ Revenue",
  },
  {
    ar: "HTTP 200 ≠ هوية الإصدار أو Production Green",
    en: "HTTP 200 ≠ release identity or Production Green",
  },
];

const DEPLOYMENT_EVIDENCE = [
  {
    ar: "هوية الإصدار المنشور: تُتحقق من SHA الفعلي لكل خدمة",
    en: "Deployed release identity: verify the actual SHA for each service",
  },
  {
    ar: "إقامة البيانات والتشفير والنسخ الاحتياطي: تُثبت من النشر الفعلي، لا من كود المصدر وحده",
    en: "Residency, encryption, and backup posture: prove from the actual deployment, not source code alone",
  },
  {
    ar: "الحوادث ووقت التشغيل: تحتاج قياسات حديثة؛ لا نعرض أرقاماً ثابتة بلا telemetry",
    en: "Incidents and uptime require current measurements; we do not publish static numbers without telemetry",
  },
  {
    ar: "الشهادات: لا تُعرض كشهادة حالية إلا مع وثيقة صالحة وقابلة للتحقق",
    en: "Certifications are shown as current only with a valid, verifiable document",
  },
];

export function TrustCenter() {
  const locale = useLocale();
  const isAr = locale === "ar";

  return (
    <div className="mx-auto max-w-6xl space-y-10 px-4 py-8" dir={isAr ? "rtl" : "ltr"}>
      <section className="rounded-3xl border border-border/60 bg-card/70 p-7 sm:p-10">
        <div className="max-w-3xl">
          <p className="mb-3 text-xs font-semibold uppercase tracking-[0.18em] text-emerald-600 dark:text-emerald-400">
            {isAr ? "الثقة = دليل قابل للمراجعة" : "Trust = Reviewable Evidence"}
          </p>
          <h1 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
            {isAr ? "مركز الثقة والضوابط" : "Trust & Controls Center"}
          </h1>
          <p className="mt-4 text-sm leading-7 text-muted-foreground sm:text-base">
            {isAr
              ? "هذه الصفحة لا تمنح Dealix شهادة امتثال تلقائية. تعرض طريقة عمل الضوابط وحدود الادعاءات وما يجب التحقق منه في كل نشر أو عميل قبل تحويله إلى حقيقة تجارية."
              : "This page does not grant Dealix an automatic compliance certification. It explains the control model, claim boundaries, and what must be verified for each deployment or customer before it becomes commercial truth."}
          </p>
        </div>
      </section>

      <section className="grid gap-4 md:grid-cols-2">
        {TRUST_ITEMS.map((item) => (
          <article key={item.id} className="rounded-2xl border border-border/60 bg-card p-6">
            <div className="flex flex-wrap items-start justify-between gap-3">
              <h2 className="text-lg font-semibold text-foreground">
                {isAr ? item.titleAr : item.titleEn}
              </h2>
              <span className="rounded-full border border-amber-500/30 bg-amber-500/10 px-3 py-1 text-xs font-medium text-amber-700 dark:text-amber-300">
                {isAr ? item.statusAr : item.statusEn}
              </span>
            </div>
            <p className="mt-4 text-sm leading-7 text-muted-foreground">
              {isAr ? item.bodyAr : item.bodyEn}
            </p>
          </article>
        ))}
      </section>

      <section className="grid gap-5 lg:grid-cols-2">
        <article className="rounded-2xl border border-border/60 bg-card p-6">
          <h2 className="text-lg font-semibold text-foreground">
            {isAr ? "قوانين الحقيقة التشغيلية" : "Operating Truth Rules"}
          </h2>
          <ul className="mt-4 space-y-3">
            {OPERATING_RULES.map((rule) => (
              <li key={rule.en} className="flex gap-3 text-sm leading-6 text-muted-foreground">
                <span aria-hidden="true" className="mt-2 h-2 w-2 shrink-0 rounded-full bg-emerald-500" />
                <span>{isAr ? rule.ar : rule.en}</span>
              </li>
            ))}
          </ul>
        </article>

        <article className="rounded-2xl border border-border/60 bg-card p-6">
          <h2 className="text-lg font-semibold text-foreground">
            {isAr ? "ما يحتاج دليل نشر حي" : "What Requires Live Deployment Evidence"}
          </h2>
          <ul className="mt-4 space-y-3">
            {DEPLOYMENT_EVIDENCE.map((item) => (
              <li key={item.en} className="flex gap-3 text-sm leading-6 text-muted-foreground">
                <span aria-hidden="true" className="mt-2 h-2 w-2 shrink-0 rounded-full bg-blue-500" />
                <span>{isAr ? item.ar : item.en}</span>
              </li>
            ))}
          </ul>
        </article>
      </section>

      <section className="rounded-2xl border border-border/60 bg-muted/30 p-6">
        <h2 className="text-lg font-semibold text-foreground">
          {isAr ? "حالة الأدلة" : "Evidence Status"}
        </h2>
        <p className="mt-3 text-sm leading-7 text-muted-foreground">
          {isAr
            ? "قدرات الكود، اختبارات المصدر، قبول الـruntime، وهوية الإصدار المنشور هي طبقات مختلفة. لا نستخدم نجاح طبقة واحدة كدليل على طبقة أخرى. عند غياب دليل حديث تبقى الحالة UNKNOWN أو HOLD."
            : "Code capability, source tests, runtime acceptance, and deployed release identity are separate evidence layers. Passing one layer is not proof of another. When current evidence is missing, the status remains UNKNOWN or HOLD."}
        </p>
      </section>
    </div>
  );
}
