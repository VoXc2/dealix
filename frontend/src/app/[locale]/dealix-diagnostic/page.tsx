import Link from "next/link";
import type { ReactNode } from "react";
import { DiagnosticRiskScoreForm } from "@/components/offers/DiagnosticRiskScoreForm";

interface DealixDiagnosticPageProps {
  params: Promise<{ locale: string }>;
}

const BOOKING_URL = process.env.NEXT_PUBLIC_DIAGNOSTIC_BOOKING_URL || "#book-diagnostic-review";
const PROOF_PACK_URL = process.env.NEXT_PUBLIC_SAMPLE_PROOF_PACK_URL || "#sample-proof-pack";

export default async function DealixDiagnosticPage({ params }: DealixDiagnosticPageProps) {
  const { locale } = await params;
  const isAr = locale === "ar";

  const copy = isAr
    ? {
        title: "حوّل تجارب AI وعمليات الإيراد إلى Workflow محكوم وقابل للقياس",
        subtitle:
          "تشخيص خلال 7 أيام لفرق GCC التي تحتاج وضوح المصادر، حدود الموافقات، Evidence trails، وإثبات قيمة قبل التوسّع.",
        ctaPrimary: "Get Sample Proof Pack",
        ctaSecondary: "Book Diagnostic Review",
        problemTitle: "The Problem",
        problemText:
          "تجارب AI وأنشطة RevOps غالباً تتوسع قبل تثبيت الحوكمة، فتظهر فجوات في source clarity، approvals، والمتابعة بالأدلة.",
        whoTitle: "Who It Is For",
        whoItems: [
          "B2B service firms التي تعمل بمبيعات يقودها المؤسس",
          "فرق لديها CRM لكن الجودة والمتابعة غير منضبطة",
          "الفرق التي تستخدم AI داخلياً وتحتاج boundaries واضحة قبل الأتمتة",
        ],
        getTitle: "What You Get",
        getItems: [
          "Revenue Workflow Map",
          "CRM / Source Quality Review",
          "AI Usage Risk Review",
          "Approval Boundaries",
          "Evidence Trail Gaps",
          "Top 3 Revenue Decisions",
          "Proof Pack",
          "Recommended Sprint / Retainer",
        ],
        outputsTitle: "Sample Outputs",
        outputsItems: [
          "Decision Passport snapshot",
          "Risk-based next action plan",
          "Evidence event log (who approved what)",
        ],
        notDoTitle: "What We Do Not Do",
        notDoItems: [
          "We do not send autonomous AI messages.",
          "We do not claim revenue without evidence.",
          "We do not replace your CRM.",
          "We do not publish case studies without approval.",
          "We do not sell generic chatbot automation.",
        ],
        pricingTitle: "Pricing Range",
        pricingItems: [
          "Starter — 4,999 SAR",
          "Standard — 9,999 SAR",
          "Executive — 15,000 SAR",
        ],
        bookTitle: "Book Review",
        bookText:
          "ابدأ بطلب Sample Proof Pack. بعدها نراجع workflow واحد ونحدّد إن كان التشخيص 7 أيام هو الخطوة الأنسب.",
      }
    : {
        title: "Turn AI experiments and revenue operations into governed, measurable workflows.",
        subtitle:
          "A 7-day diagnostic for GCC teams that need source clarity, approval boundaries, evidence trails, and proof of value.",
        ctaPrimary: "Get Sample Proof Pack",
        ctaSecondary: "Book Diagnostic Review",
        problemTitle: "The Problem",
        problemText:
          "Most AI and RevOps initiatives scale before governance is ready, creating weak source clarity, unclear approvals, and non-auditable follow-up.",
        whoTitle: "Who It Is For",
        whoItems: [
          "Founder-led B2B service firms",
          "Teams with CRM but inconsistent quality and follow-up",
          "Organizations using AI internally and needing approval boundaries",
        ],
        getTitle: "What You Get",
        getItems: [
          "Revenue Workflow Map",
          "CRM / Source Quality Review",
          "AI Usage Risk Review",
          "Approval Boundaries",
          "Evidence Trail Gaps",
          "Top 3 Revenue Decisions",
          "Proof Pack",
          "Recommended Sprint / Retainer",
        ],
        outputsTitle: "Sample Outputs",
        outputsItems: [
          "Decision Passport snapshot",
          "Risk-based next action plan",
          "Evidence event log (who approved what)",
        ],
        notDoTitle: "What We Do Not Do",
        notDoItems: [
          "We do not send autonomous AI messages.",
          "We do not claim revenue without evidence.",
          "We do not replace your CRM.",
          "We do not publish case studies without approval.",
          "We do not sell generic chatbot automation.",
        ],
        pricingTitle: "Pricing Range",
        pricingItems: [
          "Starter — 4,999 SAR",
          "Standard — 9,999 SAR",
          "Executive — 15,000 SAR",
        ],
        bookTitle: "Book Review",
        bookText:
          "Start by requesting the Sample Proof Pack. Then review one workflow and decide if the 7-day diagnostic is the right next step.",
      };

  return (
    <div className="min-h-screen bg-background grid-pattern">
      <div className="mx-auto max-w-5xl px-6 py-16 space-y-12" dir={isAr ? "rtl" : "ltr"}>
        <section className="rounded-2xl border border-border bg-card p-8 shadow-sm">
          <p className="text-sm text-muted-foreground">Dealix — Founder-Led Revenue Machine</p>
          <h1 className="mt-3 text-3xl md:text-4xl font-bold tracking-tight text-foreground">
            {copy.title}
          </h1>
          <p className="mt-4 text-base text-foreground/90">{copy.subtitle}</p>
          <div className="mt-8 flex flex-wrap gap-3">
            <Link
              href={PROOF_PACK_URL}
              className="inline-flex items-center justify-center rounded-lg bg-primary px-5 py-2.5 text-sm font-medium text-primary-foreground shadow transition hover:opacity-90"
            >
              {copy.ctaPrimary}
            </Link>
            <Link
              href={BOOKING_URL}
              className="inline-flex items-center justify-center rounded-lg border border-border px-5 py-2.5 text-sm font-medium text-foreground transition hover:border-primary/50 hover:bg-primary/5"
            >
              {copy.ctaSecondary}
            </Link>
          </div>
        </section>

        <section className="grid gap-6 md:grid-cols-2">
          <Block title={copy.problemTitle}>
            <p className="text-sm text-foreground/90">{copy.problemText}</p>
          </Block>
          <Block title={copy.whoTitle}>
            <ul className="list-inside list-disc space-y-2 text-sm text-foreground/90 marker:text-primary">
              {copy.whoItems.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </Block>
          <Block title={copy.getTitle}>
            <ul className="list-inside list-disc space-y-2 text-sm text-foreground/90 marker:text-primary">
              {copy.getItems.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </Block>
          <Block title={copy.outputsTitle}>
            <ul className="list-inside list-disc space-y-2 text-sm text-foreground/90 marker:text-primary">
              {copy.outputsItems.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </Block>
          <Block title={copy.notDoTitle}>
            <ul className="list-inside list-disc space-y-2 text-sm text-foreground/90 marker:text-primary">
              {copy.notDoItems.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </Block>
          <Block title={copy.pricingTitle}>
            <ul className="list-inside list-disc space-y-2 text-sm text-foreground/90 marker:text-primary">
              {copy.pricingItems.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </Block>
        </section>

        <section id="sample-proof-pack" className="space-y-3">
          <h2 className="text-2xl font-semibold text-foreground">{copy.bookTitle}</h2>
          <p className="text-sm text-foreground/90">{copy.bookText}</p>
          <div id="book-diagnostic-review" className="flex flex-wrap gap-3">
            <Link
              href={PROOF_PACK_URL}
              className="inline-flex items-center justify-center rounded-lg bg-primary px-5 py-2.5 text-sm font-medium text-primary-foreground shadow transition hover:opacity-90"
            >
              {copy.ctaPrimary}
            </Link>
            <Link
              href={BOOKING_URL}
              className="inline-flex items-center justify-center rounded-lg border border-border px-5 py-2.5 text-sm font-medium text-foreground transition hover:border-primary/50 hover:bg-primary/5"
            >
              {copy.ctaSecondary}
            </Link>
          </div>
        </section>

        <section>
          <DiagnosticRiskScoreForm locale={isAr ? "ar" : "en"} />
        </section>
      </div>
    </div>
  );
}

function Block({ title, children }: { title: string; children: ReactNode }) {
  return (
    <div className="rounded-2xl border border-border bg-card p-6 shadow-sm">
      <h2 className="text-xl font-semibold text-foreground">{title}</h2>
      <div className="mt-4">{children}</div>
    </div>
  );
}
