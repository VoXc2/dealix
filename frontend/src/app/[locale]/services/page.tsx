import Link from "next/link";
import SprintToolsPanel from "@/components/services/SprintToolsPanel";

interface ServicesHubProps {
  params: Promise<{ locale: string }>;
}

export default async function ServicesHubPage({ params }: ServicesHubProps) {
  const { locale } = await params;
  const isAr = locale === "ar";

  if (isAr) {
    return (
      <div className="min-h-screen bg-background grid-pattern">
        <div className="mx-auto max-w-4xl px-6 py-16 text-right" dir="rtl">
          <p className="text-sm font-medium text-muted-foreground">
            Dealix — Governed Revenue & AI Operations
          </p>
          <h1 className="mt-3 text-3xl font-bold tracking-tight text-foreground">
            كتالوج الخدمات السبع
          </h1>
          <p className="mt-4 text-muted-foreground leading-relaxed">
            ديالكس تبيع قرارات إيراد وذكاء اصطناعي محكومة بالأدلة — لا روبوتات
            ولا أتمتة. التسعير الكامل في{" "}
            <code className="rounded bg-muted px-1 py-0.5 text-foreground">
              docs/OFFER_LADDER_AND_PRICING.md
            </code>{" "}
            والاستراتيجية في{" "}
            <code className="rounded bg-muted px-1 py-0.5 text-foreground">
              docs/strategy/
            </code>
            .
          </p>

          <ul className="mt-10 space-y-6 text-base leading-relaxed">
            <li className="rounded-lg border border-border bg-card/40 p-5">
              <h2 className="text-lg font-semibold text-foreground">
                0) Governed Revenue Ops Diagnostic — التشخيص
                <span className="ms-2 text-sm font-normal text-emerald-400">مجاني</span>
              </h2>
              <p className="mt-2 text-muted-foreground">
                خريطة سير عمل الإيراد، مراجعة جودة المصدر، فجوات المتابعة،
                وتوصية الخطوة التالية.
              </p>
            </li>
            <li className="rounded-lg border border-border bg-card/40 p-5">
              <h2 className="text-lg font-semibold text-foreground">
                1) Revenue Intelligence Sprint — سبرنت ذكاء الإيراد
                <span className="ms-2 text-sm font-normal text-gold-400">25,000 ر.س</span>
              </h2>
              <p className="mt-2 text-muted-foreground">
                ترتيب الحسابات، تقييم مخاطر الصفقات، مسودات الإجراء التالي،
                سجل الفرص، Decision Passport، وProof Pack.
              </p>
              <Link
                href={`/${locale}/offer/lead-intelligence-sprint`}
                className="mt-3 inline-block text-sm font-medium text-primary hover:underline"
              >
                عرض السبرنت
              </Link>
            </li>
            <li className="rounded-lg border border-border bg-card/40 p-5">
              <h2 className="text-lg font-semibold text-foreground">
                2) Governed Ops Retainer — الاحتفاظ التشغيلي المحكوم
                <span className="ms-2 text-sm font-normal text-gold-400">4,999–35,000 ر.س/شهر</span>
              </h2>
              <p className="mt-2 text-muted-foreground">
                مراجعة إيراد شهرية، مراجعة جودة الأنبوب، مراجعة قرارات الذكاء
                الاصطناعي، قائمة متابعة موافق عليها، سجل مخاطر، ومذكرة مجلس.
              </p>
            </li>
            <li className="rounded-lg border border-border bg-card/40 p-5">
              <h2 className="text-lg font-semibold text-foreground">
                3) AI Governance for Revenue Teams — حوكمة الذكاء الاصطناعي
              </h2>
              <p className="mt-2 text-muted-foreground">
                الإجراءات المسموحة والممنوعة، حدود الموافقة، قواعد المصدر،
                وسياسة منع الإرسال الخارجي التلقائي.
              </p>
            </li>
            <li className="rounded-lg border border-border bg-card/40 p-5">
              <h2 className="text-lg font-semibold text-foreground">
                4) CRM / Data Readiness for AI — جاهزية البيانات
              </h2>
              <p className="mt-2 text-muted-foreground">
                تقرير نظافة الـCRM، خرائط المصادر، الحقول الناقصة، الحسابات
                المكررة، ودرجة جاهزية البيانات للذكاء الاصطناعي.
              </p>
            </li>
            <li className="rounded-lg border border-border bg-card/40 p-5">
              <h2 className="text-lg font-semibold text-foreground">
                5) Board Decision Memo — مذكرة قرارات المجلس
              </h2>
              <p className="mt-2 text-muted-foreground">
                أهم قرارات الإيراد، مخاطر الأنبوب، مخاطر حوكمة الذكاء
                الاصطناعي، وتوصيات ابنِ/ثبّت/أوقِف.
              </p>
            </li>
            <li className="rounded-lg border border-border bg-card/40 p-5">
              <h2 className="text-lg font-semibold text-foreground">
                6) Trust Pack Lite — حزمة الثقة
              </h2>
              <p className="mt-2 text-muted-foreground">
                سياسة إجراءات الذكاء الاصطناعي، مصفوفة الموافقات، الإجراءات
                الممنوعة، وحدود الثقة — تُعرض عند طلب الأمان فقط.
              </p>
            </li>
          </ul>

          <SprintToolsPanel locale={locale} />

          <div className="mt-12">
            <Link
              href={`/${locale}/login`}
              className="inline-flex items-center justify-center rounded-lg bg-primary px-5 py-2.5 text-sm font-medium text-primary-foreground shadow transition hover:opacity-90"
            >
              تسجيل الدخول
            </Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background grid-pattern">
      <div className="mx-auto max-w-4xl px-6 py-16 text-left" dir="ltr">
        <p className="text-sm font-medium text-muted-foreground">
          Dealix — Governed Revenue & AI Operations
        </p>
        <h1 className="mt-3 text-3xl font-bold tracking-tight text-foreground">
          Seven service lines
        </h1>
        <p className="mt-4 text-muted-foreground leading-relaxed">
          Dealix sells governed, evidence-backed revenue &amp; AI decisions —
          not bots, not automation. Full pricing lives in{" "}
          <code className="rounded bg-muted px-1 py-0.5 text-foreground">
            docs/OFFER_LADDER_AND_PRICING.md
          </code>{" "}
          and the strategy in{" "}
          <code className="rounded bg-muted px-1 py-0.5 text-foreground">
            docs/strategy/
          </code>
          .
        </p>

        <ul className="mt-10 space-y-6 text-base leading-relaxed">
          <li className="rounded-lg border border-border bg-card/40 p-5">
            <h2 className="text-lg font-semibold text-foreground">
              0) Governed Revenue Ops Diagnostic
              <span className="ms-2 text-sm font-normal text-emerald-400">Free</span>
            </h2>
            <p className="mt-2 text-muted-foreground">
              Revenue workflow map, source-quality review, follow-up gaps,
              and a recommended next step.
            </p>
          </li>
          <li className="rounded-lg border border-border bg-card/40 p-5">
            <h2 className="text-lg font-semibold text-foreground">
              1) Revenue Intelligence Sprint
              <span className="ms-2 text-sm font-normal text-gold-400">25,000 SAR</span>
            </h2>
            <p className="mt-2 text-muted-foreground">
              Account prioritization, deal-risk scoring, next-best-action
              drafts, opportunity ledger, Decision Passport, and Proof Pack.
            </p>
            <Link
              href={`/${locale}/offer/lead-intelligence-sprint`}
              className="mt-3 inline-block text-sm font-medium text-primary hover:underline"
            >
              View the Sprint offer
            </Link>
          </li>
          <li className="rounded-lg border border-border bg-card/40 p-5">
            <h2 className="text-lg font-semibold text-foreground">
              2) Governed Ops Retainer
              <span className="ms-2 text-sm font-normal text-gold-400">4,999–35,000 SAR/mo</span>
            </h2>
            <p className="mt-2 text-muted-foreground">
              Monthly revenue review, pipeline-quality review, AI decision
              review, approved follow-up queue, risk register, board memo.
            </p>
          </li>
          <li className="rounded-lg border border-border bg-card/40 p-5">
            <h2 className="text-lg font-semibold text-foreground">
              3) AI Governance for Revenue Teams
            </h2>
            <p className="mt-2 text-muted-foreground">
              Allowed and forbidden AI actions, approval boundaries, source
              rules, and a no-autonomous-external-send policy.
            </p>
          </li>
          <li className="rounded-lg border border-border bg-card/40 p-5">
            <h2 className="text-lg font-semibold text-foreground">
              4) CRM / Data Readiness for AI
            </h2>
            <p className="mt-2 text-muted-foreground">
              CRM hygiene report, source mapping, missing fields, duplicate
              accounts, and a data-readiness score.
            </p>
          </li>
          <li className="rounded-lg border border-border bg-card/40 p-5">
            <h2 className="text-lg font-semibold text-foreground">
              5) Board Decision Memo
            </h2>
            <p className="mt-2 text-muted-foreground">
              Top revenue decisions, pipeline risks, AI governance risks,
              and build / hold / kill recommendations.
            </p>
          </li>
          <li className="rounded-lg border border-border bg-card/40 p-5">
            <h2 className="text-lg font-semibold text-foreground">
              6) Trust Pack Lite
            </h2>
            <p className="mt-2 text-muted-foreground">
              AI action policy, approval matrix, forbidden actions, and
              trust boundaries — offered only on a security request.
            </p>
          </li>
        </ul>

        <SprintToolsPanel locale={locale} />

        <div className="mt-12">
          <Link
            href={`/${locale}/login`}
            className="inline-flex items-center justify-center rounded-lg bg-primary px-5 py-2.5 text-sm font-medium text-primary-foreground shadow transition hover:opacity-90"
          >
            Log in
          </Link>
        </div>
      </div>
    </div>
  );
}
