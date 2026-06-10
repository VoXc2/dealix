import type { Metadata } from "next";
import Link from "next/link";
import { PublicLaunchShell } from "@/components/brand/PublicLaunchShell";
import { buildFunnelMetadata } from "@/lib/gtmMetadata";

type Props = { params: Promise<{ locale: string }> };

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { locale } = await params;
  return buildFunnelMetadata(locale, "privacy");
}

export default async function PrivacyPage({ params }: Props) {
  const { locale } = await params;
  const isAr = locale === "ar";
  const base = `/${locale}`;

  return (
    <PublicLaunchShell compactNav>
      <main className="mx-auto max-w-3xl px-6 py-16" dir={isAr ? "rtl" : "ltr"}>

        {/* Header */}
        <header className={`mb-10 ${isAr ? "text-right" : ""}`}>
          <span className="inline-block rounded-full bg-emerald-100 dark:bg-emerald-950/30 text-emerald-700 dark:text-emerald-300 text-xs font-medium px-3 py-1 mb-4">
            {isAr ? "PDPL أصيل" : "PDPL Native"}
          </span>
          <h1 className="text-4xl font-bold">
            {isAr ? "سياسة الخصوصية وحماية البيانات" : "Privacy & Data Protection Policy"}
          </h1>
          <p className="mt-4 text-muted-foreground leading-relaxed text-lg">
            {isAr
              ? "Dealix مبني أصلاً على نظام حماية البيانات الشخصية (PDPL) — لا outreach بارد، لا scraping، موافقة قبل أي إرسال خارجي."
              : "Dealix is built natively on PDPL — no cold outreach, no scraping, approval before any external send."}
          </p>
          <p className="mt-2 text-sm text-muted-foreground">
            {isAr ? "آخر تحديث: مايو 2026" : "Last updated: May 2026"}
          </p>
        </header>

        <div className={`space-y-10 ${isAr ? "text-right" : ""}`}>

          {/* What we collect */}
          <section>
            <h2 className="text-2xl font-bold mb-4">{isAr ? "ما نجمعه" : "What We Collect"}</h2>
            <div className="rounded-xl border border-border/60 bg-card/50 p-5 space-y-3">
              {(isAr ? [
                { title: "بيانات التشخيص", desc: "اسم الشركة، القطاع، المشكلة التشغيلية — يُستخدم فقط لإنتاج Proof Pack." },
                { title: "بيانات التواصل", desc: "الاسم، البريد الإلكتروني — للتواصل البشري المباشر فقط. لا أتمتة." },
                { title: "بيانات الاستخدام", desc: "صفحات المُشاهَدة، مدة الجلسة — عبر PostHog مع إعدادات خصوصية مشدّدة." },
              ] : [
                { title: "Diagnostic data", desc: "Company name, sector, operational challenge — used only to produce Proof Pack." },
                { title: "Contact data", desc: "Name, email — for direct human communication only. No automation." },
                { title: "Usage data", desc: "Pages viewed, session duration — via PostHog with strict privacy settings." },
              ]).map((item) => (
                <div key={item.title} className="flex items-start gap-3">
                  <span className="text-emerald-500 mt-0.5 flex-shrink-0">✓</span>
                  <div>
                    <span className="font-medium">{item.title}: </span>
                    <span className="text-muted-foreground">{item.desc}</span>
                  </div>
                </div>
              ))}
            </div>
          </section>

          {/* What we do NOT do */}
          <section>
            <h2 className="text-2xl font-bold mb-4">{isAr ? "ما لا نفعله — مطلقاً" : "What We Never Do"}</h2>
            <div className="rounded-xl border border-red-500/20 bg-red-50/30 dark:bg-red-950/10 p-5 space-y-3">
              {(isAr ? [
                "لا نشتري قوائم leads أو بيانات جهات اتصال",
                "لا نُرسل واتساب أو LinkedIn آلي للعملاء المحتملين",
                "لا نُشارك بياناتك مع طرف ثالث بدون موافقة صريحة",
                "لا نُنشئ ملفاً شخصياً من بيانات عامة بدون علمك",
                "لا نُرسل أي تواصل تجاري دون إذن مسبق",
              ] : [
                "We do not buy lead lists or contact databases",
                "We do not send automated WhatsApp or LinkedIn to prospects",
                "We do not share your data with third parties without explicit consent",
                "We do not build profiles from public data without your knowledge",
                "We do not send any commercial communication without prior permission",
              ]).map((item) => (
                <div key={item} className="flex items-start gap-3">
                  <span className="text-red-500 mt-0.5 flex-shrink-0">✗</span>
                  <span className="text-muted-foreground">{item}</span>
                </div>
              ))}
            </div>
          </section>

          {/* Your rights */}
          <section>
            <h2 className="text-2xl font-bold mb-4">{isAr ? "حقوقك (PDPL)" : "Your Rights (PDPL)"}</h2>
            <div className="grid gap-3 sm:grid-cols-2">
              {(isAr ? [
                { right: "الوصول", desc: "طلب نسخة من بياناتك المحفوظة" },
                { right: "التصحيح", desc: "تصحيح أي بيانات غير دقيقة" },
                { right: "الحذف", desc: "طلب حذف بياناتك — خلال 30 يوماً" },
                { right: "التصدير", desc: "تصدير بياناتك بصيغة قابلة للقراءة" },
                { right: "سحب الموافقة", desc: "إلغاء الموافقة فوراً عند الطلب" },
                { right: "الاعتراض", desc: "الاعتراض على معالجة بعينها" },
              ] : [
                { right: "Access", desc: "Request a copy of your stored data" },
                { right: "Correction", desc: "Correct any inaccurate data" },
                { right: "Deletion", desc: "Request deletion of your data — within 30 days" },
                { right: "Export", desc: "Export your data in a readable format" },
                { right: "Withdraw consent", desc: "Cancel consent immediately upon request" },
                { right: "Object", desc: "Object to specific processing" },
              ]).map((item) => (
                <div key={item.right} className="rounded-lg border border-border/50 bg-card/50 p-3">
                  <p className="font-semibold text-sm">{item.right}</p>
                  <p className="text-xs text-muted-foreground mt-0.5">{item.desc}</p>
                </div>
              ))}
            </div>
            <p className="mt-4 text-sm text-muted-foreground">
              {isAr
                ? "لممارسة أي حق: راسلنا عبر البريد الإلكتروني. سنرد خلال 72 ساعة."
                : "To exercise any right: contact us by email. We respond within 72 hours."}
            </p>
          </section>

          {/* Data retention */}
          <section>
            <h2 className="text-2xl font-bold mb-4">{isAr ? "الاحتفاظ بالبيانات" : "Data Retention"}</h2>
            <div className="rounded-xl border border-border/60 bg-card/50 p-5 space-y-2 text-sm">
              {(isAr ? [
                "بيانات التشخيص: تُحتفظ 12 شهراً من تاريخ الإنشاء",
                "بيانات التواصل: تُحذف فور طلب صاحبها",
                "سجلات Audit Trail: تُحتفظ 36 شهراً للامتثال القانوني",
                "Soft deletes: لا حذف مادي — بيانات تُعلَّم محذوفة وتُعزل",
              ] : [
                "Diagnostic data: retained 12 months from creation date",
                "Contact data: deleted on owner's request",
                "Audit Trail logs: retained 36 months for legal compliance",
                "Soft deletes: no physical deletion — data marked deleted and isolated",
              ]).map((item) => (
                <div key={item} className="flex items-start gap-2">
                  <span className="text-primary mt-0.5 flex-shrink-0">•</span>
                  <span>{item}</span>
                </div>
              ))}
            </div>
          </section>

          {/* Approval-first */}
          <section>
            <h2 className="text-2xl font-bold mb-4">
              {isAr ? "Approval-First Architecture" : "Approval-First Architecture"}
            </h2>
            <p className="text-muted-foreground leading-relaxed">
              {isAr
                ? "كل إجراء حرج في Dealix — إرسال بريد، مسودة واتساب، تحليل بيانات عميل — يمر عبر Approval Center قبل التنفيذ. لا أتمتة بلا مراجعة بشرية. هذا المبدأ مُضمَّن في البنية التقنية، لا فقط في السياسة."
                : "Every critical action in Dealix — sending email, WhatsApp draft, client data analysis — goes through the Approval Center before execution. No automation without human review. This principle is embedded in the technical architecture, not just policy."}
            </p>
          </section>

          {/* Contact */}
          <section className="rounded-xl border border-border/60 bg-card/50 p-6">
            <h2 className="text-xl font-bold mb-3">{isAr ? "تواصل معنا" : "Contact Us"}</h2>
            <p className="text-sm text-muted-foreground">
              {isAr
                ? "لأي استفسار عن خصوصيتك أو لممارسة حقوقك PDPL، تواصل معنا مباشرة."
                : "For any privacy inquiry or to exercise your PDPL rights, contact us directly."}
            </p>
            <div className="mt-4 flex flex-wrap gap-3">
              <Link
                href={`${base}/dealix-diagnostic`}
                className="inline-flex items-center rounded-lg bg-primary text-primary-foreground px-4 py-2 text-sm font-medium hover:bg-primary/90 transition-colors"
              >
                {isAr ? "تواصل معنا" : "Contact Us"}
              </Link>
              <Link
                href={base}
                className="inline-flex items-center rounded-lg border border-border bg-card px-4 py-2 text-sm font-medium hover:bg-muted/30 transition-colors"
              >
                {isAr ? "← الرئيسية" : "← Home"}
              </Link>
            </div>
          </section>

        </div>
      </main>
    </PublicLaunchShell>
  );
}
