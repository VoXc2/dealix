import Link from "next/link";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "WhatsApp / Inbox Follow-up OS — Dealix",
  description:
    "طوابير متابعة منظمة من واتساب وإيميل — بدون ضياع رسالة أو نسيان عميل.",
};

const features = [
  { en: "Unified inbox queue", ar: "طابور وارد موحّد من واتساب وإيميل" },
  { en: "Follow-up reminders", ar: "تذكيرات متابعة مرتبطة بكل محادثة" },
  { en: "Human-approved drafts", ar: "مسوّدات رد بموافقة بشرية قبل الإرسال" },
  { en: "Status & SLA tracking", ar: "تتبع حالة و SLA لكل رسالة" },
  { en: "Daily follow-up report", ar: "تقرير متابعة يومي للرسائل المعلقة" },
  { en: "No auto-send by default", ar: "لا إرسال تلقائي افتراضياً — draft_only" },
];

export default function WhatsAppInboxFollowupOSPage() {
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
            WhatsApp / Inbox Follow-up OS
          </p>
          <h1 className="mt-3 text-4xl font-semibold leading-tight">
            نظام متابعة الواتساب والوارد
          </h1>
          <p className="mt-2 text-sm text-white/60">
            WhatsApp / Inbox Follow-up OS — never lose a follow-up again
          </p>
          <p className="mt-4 max-w-2xl text-sm text-white/70">
            طوابير متابعة منظمة من واتساب وإيميل. كل رسالة لها حالة و owner
            و SLA. لا ضياع رسالة في الإشعارات، ولا نسيان عميل منتظر رداً.
          </p>
        </header>

        <section className="mt-10 rounded-2xl border border-white/10 bg-white/5 p-6">
          <p className="text-xs uppercase tracking-widest text-amber-300/80">
            المشكلة
          </p>
          <p className="mt-2 text-sm text-white/80">
            متابعات تضيع بين إشعارات واتساب والإيميل. لا أحد يملك طابور المتابعة
            بشكل واضح، فينسى العملاء، وتطول أوقات الرد، وتُفقد صفقات بسبب تأخر
            غير مُراقب.
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
              النطاق والمدة ومعايير القبول ووتيرة المراجعة تُحدد بعد التشخيص المجاني وQualified Discovery
            </p>
          </div>
          <div className="rounded-2xl border border-amber-300/20 bg-amber-300/5 p-6">
            <p className="text-xs uppercase tracking-widest text-amber-300/80">
              لماذا لا تؤجله
            </p>
            <p className="mt-2 text-sm text-white/80">
              كل يوم بدون queue واضحة هو فرصة تضيع في واتساب أو إيميل بصمت.
              النطاق والسعر يُحددان بعد تشخيص لحجم المحادثات عندك.
            </p>
          </div>
        </section>

        <section className="mt-8 rounded-2xl border border-amber-300/20 bg-amber-300/5 p-6 text-sm text-white/80">
          <p className="font-medium text-amber-200">السلامة أولاً</p>
          <p className="mt-2">
            الوضع الافتراضي: draft_only — لا إرسال تلقائي. كل مسوّد رد يحتاج
            موافقة بشرية قبل أي قناة خارجية. راجع إعدادات السلامة في
            <Link href="/settings/outbound-safety" className="mx-1 text-amber-300 hover:underline">
              /settings/outbound-safety
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
            href="/followups"
            className="rounded-full border border-white/20 px-6 py-3 text-sm font-medium text-white transition hover:border-white/40"
          >
            شاهد نموذج المتابعة
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