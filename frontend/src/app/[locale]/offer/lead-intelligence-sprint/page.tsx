import Link from "next/link";

interface OfferPageProps {
  params: Promise<{ locale: string }>;
}

export default async function LeadIntelligenceSprintOfferPage({
  params,
}: OfferPageProps) {
  const { locale } = await params;
  const isAr = locale === "ar";

  if (isAr) {
    return (
      <div className="min-h-screen bg-background grid-pattern">
        <div className="mx-auto max-w-3xl px-6 py-16 text-right" dir="rtl">
          <p className="text-sm font-medium text-muted-foreground">
            Dealix — Revenue Operations + AI Implementation
          </p>
          <h1 className="mt-3 text-3xl font-bold tracking-tight text-foreground">
            Lead Intelligence Sprint
          </h1>
          <p className="mt-2 text-2xl font-semibold text-primary">9,500 ريال</p>
          <p className="mt-1 text-sm text-muted-foreground">
            حتى 10 أيام عمل · حتى 500 صف حساب (افتراضي في العقد)
          </p>

          <section className="mt-10 space-y-3 text-base leading-relaxed text-foreground/90">
            <h2 className="text-lg font-semibold text-foreground">المشكلة</h2>
            <p>
              بيانات العملاء والحسابات مبعثرة، فيها تكرار، وصعب تحديد من
              نتصل به أولاً وبأي دليل — دون أن نخرق الامتثال أو نبيع «ذكاءً
              عاماً» بلا مخرجات.
            </p>

            <h2 className="pt-4 text-lg font-semibold text-foreground">
              ماذا تستلم
            </h2>
            <ul className="list-inside list-disc space-y-2 marker:text-primary">
              <li>قائمة منظّمة بعد التحقق الأولي من الحقول</li>
              <li>Dedupe مع اقتراحات واضحة</li>
              <li>Scoring وترتيب — Top 50 حساباً</li>
              <li>خطة 10 إجراءات فورية</li>
              <li>حتى 20 مسودة outreach — مسودات فقط، بموافقة لاحقة للإرسال</li>
              <li>لوحة pipeline مصغّرة + تقرير تنفيذي</li>
            </ul>

            <h2 className="pt-4 text-lg font-semibold text-foreground">
              ما لا نشمله
            </h2>
            <p className="text-sm text-muted-foreground">
              لا إرسال بارد، لا أتمتة LinkedIn، لا قوائم مشتراة، لا scraping
              إنتاجي — وفق سياسات Dealix وPDPL.
            </p>
          </section>

          <div className="mt-12 flex flex-wrap gap-4 justify-end">
            <Link
              href={`/${locale}/login`}
              className="inline-flex items-center justify-center rounded-lg bg-primary px-5 py-2.5 text-sm font-medium text-primary-foreground shadow transition hover:opacity-90"
            >
              تسجيل الدخول / البدء
            </Link>
          </div>

          <p className="mt-10 text-xs text-muted-foreground">
            للتفاصيل الكاملة والعقود: راجع مستندات{' '}
            <code className="rounded bg-muted px-1 py-0.5">docs/commercial/</code>{' '}
            في المستودع.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background grid-pattern">
      <div className="mx-auto max-w-3xl px-6 py-16 text-left" dir="ltr">
        <p className="text-sm font-medium text-muted-foreground">
          Dealix — Revenue Operations + AI Implementation
        </p>
        <h1 className="mt-3 text-3xl font-bold tracking-tight text-foreground">
          Lead Intelligence Sprint
        </h1>
        <p className="mt-2 text-2xl font-semibold text-primary">SAR 9,500</p>
        <p className="mt-1 text-sm text-muted-foreground">
          Up to 10 business days · up to 500 account rows (default in SOW)
        </p>

        <section className="mt-10 space-y-3 text-base leading-relaxed text-foreground/90">
          <h2 className="text-lg font-semibold text-foreground">Problem</h2>
          <p>
            Account lists are messy and duplicated. Teams struggle to decide
            who to contact first and why — without breaking compliance or
            selling generic AI with no measurable output.
          </p>

          <h2 className="pt-4 text-lg font-semibold text-foreground">
            Deliverables
          </h2>
          <ul className="list-inside list-disc space-y-2 marker:text-primary">
            <li>Structured list after initial field validation</li>
            <li>Dedupe suggestions</li>
            <li>Scoring and ranking — Top 50 accounts</li>
            <li>Top 10 action plan</li>
            <li>Up to 20 outreach drafts — draft-only</li>
            <li>Mini pipeline board + executive report</li>
          </ul>

          <h2 className="pt-4 text-lg font-semibold text-foreground">
            Out of scope
          </h2>
          <p className="text-sm text-muted-foreground">
            No cold outbound automation, no purchased lists, no scraping for
            production — per Dealix and PDPL-aligned policies.
          </p>
        </section>

        <div className="mt-12 flex flex-wrap gap-4">
          <Link
            href={`/${locale}/login`}
            className="inline-flex items-center justify-center rounded-lg bg-primary px-5 py-2.5 text-sm font-medium text-primary-foreground shadow transition hover:opacity-90"
          >
            Log in / Get started
          </Link>
        </div>

        <p className="mt-10 text-xs text-muted-foreground">
          Contracts and checklists live under{' '}
          <code className="rounded bg-muted px-1 py-0.5">docs/commercial/</code>{' '}
          in the repository.
        </p>
      </div>
    </div>
  );
}
