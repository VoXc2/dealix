import Link from "next/link";

interface DealixDiagnosticPageProps {
  params: Promise<{ locale: string }>;
}

const BOOKING_URL =
  process.env.NEXT_PUBLIC_DIAGNOSTIC_BOOKING_URL ||
  "https://calendly.com/sami-assiri11/dealix-demo";

export default async function DealixDiagnosticPage({
  params,
}: DealixDiagnosticPageProps) {
  const { locale } = await params;
  const isAr = locale === "ar";
  const proofPackHref = `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/v1/governed-diagnostic/sample-proof-pack`;

  if (isAr) {
    return (
      <div className="min-h-screen bg-background grid-pattern">
        <main className="mx-auto max-w-5xl px-6 py-16 text-right" dir="rtl">
          <p className="text-sm font-medium text-muted-foreground">Dealix</p>
          <h1 className="mt-3 text-4xl font-bold tracking-tight text-foreground">
            حوّل تجارب AI وعمليات الإيراد إلى workflows محكومة وقابلة للقياس
          </h1>
          <p className="mt-4 text-lg text-muted-foreground leading-relaxed">
            تشخيص لمدة 7 أيام لفرق الخليج التي تحتاج وضوح المصادر، حدود الموافقات،
            مسار أدلة، وإثبات قيمة.
          </p>

          <div className="mt-8 flex flex-wrap justify-end gap-3">
            <Link
              href={BOOKING_URL}
              className="inline-flex items-center justify-center rounded-lg bg-primary px-5 py-2.5 text-sm font-medium text-primary-foreground shadow transition hover:opacity-90"
            >
              Book Diagnostic Review
            </Link>
            <Link
              href={proofPackHref}
              className="inline-flex items-center justify-center rounded-lg border border-border px-5 py-2.5 text-sm font-medium text-foreground transition hover:bg-muted"
            >
              Get Sample Proof Pack
            </Link>
          </div>

          <section className="mt-12 space-y-6">
            <div className="rounded-xl border border-border bg-card/40 p-6">
              <h2 className="text-xl font-semibold">المشكلة</h2>
              <p className="mt-3 text-muted-foreground">
                فرق كثيرة تجرّب AI أو revenue automation بدون حوكمة تشغيلية: مصادر
                غير واضحة، جودة CRM غير موثوقة، موافقات غير منضبطة، وصعوبة ربط
                الجهد بنتيجة عمل.
              </p>
            </div>
            <div className="rounded-xl border border-border bg-card/40 p-6">
              <h2 className="text-xl font-semibold">What you get</h2>
              <ul className="mt-3 list-disc space-y-2 pr-5 text-muted-foreground">
                <li>Workflow Map</li>
                <li>Source Quality Notes</li>
                <li>Approval + AI Risk Notes</li>
                <li>Revenue Leakage Points</li>
                <li>Top 3 Decisions خلال 7 أيام</li>
                <li>Proof Pack draft-first</li>
              </ul>
            </div>
            <div className="rounded-xl border border-border bg-card/40 p-6">
              <h2 className="text-xl font-semibold">Who it is for</h2>
              <p className="mt-3 text-muted-foreground">
                مؤسسون، COO، قادة Revenue/Sales، وفرق B2B في السعودية والخليج
                لديهم CRM/pipeline pain وتجارب AI تحتاج governance.
              </p>
            </div>
            <div className="rounded-xl border border-border bg-card/40 p-6">
              <h2 className="text-xl font-semibold">What we do not do</h2>
              <ul className="mt-3 list-disc space-y-2 pr-5 text-muted-foreground">
                <li>لا spam automation</li>
                <li>لا إرسال خارجي تلقائي بدون موافقة</li>
                <li>لا وعود نتائج مضمونة</li>
                <li>لا نشر case study بدون موافقة مكتوبة</li>
              </ul>
            </div>
            <div className="rounded-xl border border-border bg-card/40 p-6">
              <h2 className="text-xl font-semibold">Sample outputs</h2>
              <p className="mt-3 text-muted-foreground">
                Executive Summary، Workflow Map، Source Quality Snapshot، Top
                Decisions، Evidence Appendix.
              </p>
            </div>
            <div className="rounded-xl border border-border bg-card/40 p-6">
              <h2 className="text-xl font-semibold">Price range</h2>
              <p className="mt-3 text-muted-foreground">
                Starter 4,999 SAR · Standard 9,999 SAR · Executive 15,000 SAR
              </p>
            </div>
            <div className="rounded-xl border border-border bg-card/40 p-6">
              <h2 className="text-xl font-semibold">Book call</h2>
              <p className="mt-3 text-muted-foreground">
                نبدأ بـ workflow واحد فقط، ثم نقرر scope والتسعير والدفع حسب
                الجاهزية.
              </p>
            </div>
          </section>
        </main>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background grid-pattern">
      <main className="mx-auto max-w-5xl px-6 py-16 text-left" dir="ltr">
        <p className="text-sm font-medium text-muted-foreground">Dealix</p>
        <h1 className="mt-3 text-4xl font-bold tracking-tight text-foreground">
          Turn AI experiments and revenue operations into governed, measurable
          workflows.
        </h1>
        <p className="mt-4 text-lg text-muted-foreground leading-relaxed">
          A 7-day diagnostic for GCC teams that need source clarity, approval
          boundaries, evidence trails, and proof of value.
        </p>

        <div className="mt-8 flex flex-wrap gap-3">
          <Link
            href={BOOKING_URL}
            className="inline-flex items-center justify-center rounded-lg bg-primary px-5 py-2.5 text-sm font-medium text-primary-foreground shadow transition hover:opacity-90"
          >
            Book Diagnostic Review
          </Link>
          <Link
            href={proofPackHref}
            className="inline-flex items-center justify-center rounded-lg border border-border px-5 py-2.5 text-sm font-medium text-foreground transition hover:bg-muted"
          >
            Get Sample Proof Pack
          </Link>
        </div>

        <section className="mt-12 space-y-6">
          <div className="rounded-xl border border-border bg-card/40 p-6">
            <h2 className="text-xl font-semibold">Problem</h2>
            <p className="mt-3 text-muted-foreground">
              Teams run AI and revenue workflows with unclear sources, weak CRM
              quality, and undefined approvals. The result is activity with low
              trust and unclear value.
            </p>
          </div>
          <div className="rounded-xl border border-border bg-card/40 p-6">
            <h2 className="text-xl font-semibold">What you get</h2>
            <ul className="mt-3 list-disc space-y-2 pl-5 text-muted-foreground">
              <li>Workflow map</li>
              <li>Source quality notes</li>
              <li>Approval and AI risk notes</li>
              <li>Revenue leakage points</li>
              <li>Top 3 executable decisions in 7 days</li>
              <li>Proof Pack draft-first</li>
            </ul>
          </div>
          <div className="rounded-xl border border-border bg-card/40 p-6">
            <h2 className="text-xl font-semibold">Who it is for</h2>
            <p className="mt-3 text-muted-foreground">
              GCC B2B founders, COOs, revenue leaders, and partners with
              CRM/pipeline pain and active or planned AI usage.
            </p>
          </div>
          <div className="rounded-xl border border-border bg-card/40 p-6">
            <h2 className="text-xl font-semibold">What we do not do</h2>
            <ul className="mt-3 list-disc space-y-2 pl-5 text-muted-foreground">
              <li>No spam automation</li>
              <li>No external sending without founder approval</li>
              <li>No guaranteed outcomes claims</li>
              <li>No case study publishing without written consent</li>
            </ul>
          </div>
          <div className="rounded-xl border border-border bg-card/40 p-6">
            <h2 className="text-xl font-semibold">Sample outputs</h2>
            <p className="mt-3 text-muted-foreground">
              Executive summary, workflow map, source quality snapshot, top
              decisions, and evidence appendix.
            </p>
          </div>
          <div className="rounded-xl border border-border bg-card/40 p-6">
            <h2 className="text-xl font-semibold">Price range</h2>
            <p className="mt-3 text-muted-foreground">
              Starter 4,999 SAR · Standard 9,999 SAR · Executive 15,000 SAR
            </p>
          </div>
          <div className="rounded-xl border border-border bg-card/40 p-6">
            <h2 className="text-xl font-semibold">Book call</h2>
            <p className="mt-3 text-muted-foreground">
              We start with one workflow and align on scope, evidence,
              approvals, and delivery path.
            </p>
          </div>
        </section>
      </main>
    </div>
  );
}
