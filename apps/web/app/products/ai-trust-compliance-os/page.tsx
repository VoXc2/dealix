import Link from "next/link";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "AI Trust & Compliance OS — Dealix",
  description:
    "بوابات موافقة بشرية، سجلات تدقيق، حماية بيانات PDPL — امتثال سعودي أولاً.",
};

const features = [
  { en: "Human approval gates", ar: "بوابات موافقة بشرية على كل خروج" },
  { en: "Audit trail logging", ar: "سجل تدقيق كامل لكل إجراء" },
  { en: "PDPL-aware controls", ar: "ضوابط مبنية على PDPL السعودي" },
  { en: "Evidence packs", ar: "حزم أدلة جاهزة للمراجعة والجهات" },
  { en: "Circuit breakers", ar: "قواطع دوارة توقف العمليات تلقائياً عند الخطر" },
  { en: "Quarterly compliance review", ar: "مراجعة امتثال ربع سنوية موثّقة" },
];

export default function AITrustComplianceOSPage() {
  return (
    <main className="min-h-screen bg-[#070A12] text-white">
      <div className="mx-auto max-w-5xl px-6 py-16">
        <nav className="mb-8 text-xs text-white/50">
          <Link href="/products" className="hover:text-amber-300">
            ← المنتجات
          </Link>
        </nav>

        <header>
          <p className="text-xs uppercase tracking-[0.3em] text-amber-300/80">
            AI Trust & Compliance OS
          </p>
          <h1 className="mt-3 text-4xl font-semibold leading-tight">
            نظام الثقة والامتثال
          </h1>
          <p className="mt-2 text-sm text-white/60">
            AI Trust & Compliance OS — approval-first AI for Saudi B2B
          </p>
          <p className="mt-4 max-w-2xl text-sm text-white/70">
            كل خروج تلقائي يحمل خطر امتثال وإجراء قانوني. هذا النظام يضع بوابة
            موافقة بشرية على كل إجراء، ويحفظ سجل تدقيق كامل، ويربط الضوابط
            بـ PDPL السعودي.
          </p>
        </header>

        <section className="mt-10 rounded-2xl border border-white/10 bg-white/5 p-6">
          <p className="text-xs uppercase tracking-widest text-amber-300/80">
            المشكلة
          </p>
          <p className="mt-2 text-sm text-white/80">
            الأتمتة بدون ضوابط تُنتج إرسالاً غير مصرّح به، بيانات تتسرب، وقرارات
            لا أحد يملك سجلها. في بيئة PDPL السعودية، أي خطأ خارجي قد يكلّف
            غرامة وثقة.
          </p>
        </section>

        <section className="mt-8">
          <h2 className="text-lg font-semibold text-amber-300">
            الميزات الأساسية
          </h2>
          <ul className="mt-4 grid gap-3 md:grid-cols-2">
            {features.map((f) => (
              <li
                key={f.en}
                className="rounded-xl border border-white/10 bg-white/5 p-4"
              >
                <p className="text-sm font-medium text-white">{f.ar}</p>
                <p className="text-xs text-white/50">{f.en}</p>
              </li>
            ))}
          </ul>
        </section>

        <section className="mt-8 grid gap-4 md:grid-cols-2">
          <div className="rounded-2xl border border-white/10 bg-white/5 p-6">
            <p className="text-xs uppercase tracking-widest text-amber-300/80">
              نطاق ومدة التنفيذ
            </p>
            <p className="mt-2 text-sm text-white/80">
              النطاق والمدة ومعايير القبول ووتيرة التدقيق تُحدد بعد التشخيص المجاني وQualified Discovery
            </p>
          </div>
          <div className="rounded-2xl border border-amber-300/20 bg-amber-300/5 p-6">
            <p className="text-xs uppercase tracking-widest text-amber-300/80">
              لماذا لا تؤجله
            </p>
            <p className="mt-2 text-sm text-white/80">
              أول خروج AI بدون سياسة أو approval gate هو أول حادثة امتثال حقيقية.
              هذا نظام حماية، لا رفاهية — والنطاق والسعر يُحددان بعد تشخيص سريع.
            </p>
          </div>
        </section>

        <section className="mt-8 rounded-2xl border border-amber-300/20 bg-amber-300/5 p-6 text-sm text-white/80">
          <p className="font-medium text-amber-200">الوضع الافتراضي</p>
          <p className="mt-2">
            كل القنوات الخارجية معطّلة افتراضياً (draft_only). لا إرسال واتساب،
            لا إرسال إيميل، لا تحديث CRM تلقائي — حتى يُفعّل صراحة بموافقة
            بشرية. راجع
            <Link href="/settings/outbound-safety" className="mx-1 text-amber-300 hover:underline">
              إعدادات السلامة
            </Link>
            .
          </p>
        </section>

        <section className="mt-10 flex flex-wrap gap-3">
          <Link
            href="/book"
            className="rounded-full bg-amber-300 px-6 py-3 text-sm font-semibold text-black transition hover:bg-amber-200"
          >
            احجز تشخيص
          </Link>
          <Link
            href="/safety"
            className="rounded-full border border-white/20 px-6 py-3 text-sm font-medium text-white transition hover:border-white/40"
          >
            شاهد غرفة القيادة
          </Link>
          <Link
            href="/settings/outbound-safety"
            className="rounded-full border border-white/20 px-6 py-3 text-sm font-medium text-white transition hover:border-white/40"
          >
            راجع إعدادات السلامة
          </Link>
        </section>
      </div>
    </main>
  );
}