import Link from "next/link";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Revenue Command Room OS — Dealix",
  description:
    "صفحة قرار واحدة للمؤسس السعودي، تتحدث يومياً بأرقام محققة ومُراجعة بشرياً.",
};

const features = [
  { en: "Daily revenue snapshot", ar: "لقطة إيراد يومية بأرقام محققة ومُحقّق منها بشرياً" },
  { en: "Pipeline & lead flow", ar: "خط أنابيب وتدفّق ليدز بمراحل واضحة" },
  { en: "Founder decision log", ar: "سجل قرارات المؤسس مع سبب كل قرار" },
  { en: "Weekly proof report", ar: "تقرير إثبات أسبوعي يُرسل للعميل" },
  { en: "Risk & watch indicators", ar: "مؤشرات خطر ومراقبة على كل مؤشر" },
  { en: "Expansion trigger map", ar: "خريطة محفّزات التوسعة عند تحقق الشروط" },
];

export default function RevenueCommandRoomOSPage() {
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
            Revenue Command Room OS
          </p>
          <h1 className="mt-3 text-4xl font-semibold leading-tight">
            نظام غرفة قيادة الإيراد
          </h1>
          <p className="mt-2 text-sm text-white/60">
            Revenue Command Room OS — for founder-led Saudi B2B operators
          </p>
          <p className="mt-4 max-w-2xl text-sm text-white/70">
            صفحة قرار واحدة للمؤسس، تتحدث يومياً بأرقام محققة ومُراجعة بشرياً.
            لا dashboards فارغة، لا أرقام تقديرية بدون مصدر. كل مؤشر له owner
            وcadence ودليل.
          </p>
        </header>

        <section className="mt-10 rounded-2xl border border-white/10 bg-white/5 p-6">
          <p className="text-xs uppercase tracking-widest text-amber-300/80">
            المشكلة
          </p>
          <p className="mt-2 text-sm text-white/80">
            القرارات المالية والإيرادية متفرقة على ملفات Excel ورسائل واتساب
            وذاكرة أفراد. المؤسس لا يملك مصدراً واحداً يثق به لاتخاذ قرار يومي
            أو أسبوعي، فيتأخر التصحيح ويفقد الثقة في الأرقام.
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
              كل أسبوع بدون مصدر قرار واحد هو أسبوع تتضاعف فيه فرصة القرار
              المتأخر. النطاق والسعر يُحددان بعد تشخيص لحجم عملياتك.
            </p>
          </div>
        </section>

        <section className="mt-10 flex flex-wrap gap-3">
          <Link
            href="/book"
            className="rounded-full bg-amber-300 px-6 py-3 text-sm font-semibold text-black transition hover:bg-amber-200"
          >
            احجز تشخيص
          </Link>
          <Link
            href="/command-center"
            className="rounded-full border border-white/20 px-6 py-3 text-sm font-medium text-white transition hover:border-white/40"
          >
            شاهد غرفة القيادة
          </Link>
          <Link
            href="/delivery-os"
            className="rounded-full border border-white/20 px-6 py-3 text-sm font-medium text-white transition hover:border-white/40"
          >
            شاهد نموذج التسليم
          </Link>
        </section>
      </div>
    </main>
  );
}