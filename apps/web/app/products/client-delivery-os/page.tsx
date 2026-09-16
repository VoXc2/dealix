import Link from "next/link";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Client Delivery OS — Dealix",
  description:
    "من اليوم صفر إلى التوسعة: خريطة عمل، أتمتة، احتفاظ، مراجعة شهرية مع proof report.",
};

const features = [
  { en: "Workflow map", ar: "خريطة عمل واضحة من اليوم صفر" },
  { en: "Automation build", ar: "بناء أتمتة بموافقة بشرية على كل خطوة" },
  { en: "Retention engine", ar: "محرك احتفاظ بمراجعات دورية" },
  { en: "Proof report", ar: "تقرير إثبات يُرسل للعميل في كل أسبوع" },
  { en: "Owner per metric", ar: "owner واحد على كل مؤشر و cadence محدد" },
  { en: "Expansion trigger map", ar: "خريطة محفّزات التوسعة عند تحقق الشروط" },
];

export default function ClientDeliveryOSPage() {
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
            Client Delivery OS
          </p>
          <h1 className="mt-3 text-4xl font-semibold leading-tight">
            نظام تسليم العملاء
          </h1>
          <p className="mt-2 text-sm text-white/60">
            Client Delivery OS — from day zero to expansion
          </p>
          <p className="mt-4 max-w-2xl text-sm text-white/70">
            منهج واحد لكل عميل: استلام → خريطة عمل → غرفة قيادة → أتمتة →
            مراجعة أسبوعية → توسعة. لا تسليم بدون proof report، ولا توسعة
            بدون دليل.
          </p>
        </header>

        <section className="mt-10 rounded-2xl border border-white/10 bg-white/5 p-6">
          <p className="text-xs uppercase tracking-widest text-amber-300/80">
            المشكلة
          </p>
          <p className="mt-2 text-sm text-white/80">
            التسليم يعتمد على مجهود فردي بدون دليل أو proof report. كل عميل
            يُسلّم بطريقة مختلفة، فتتشتت الجودة، ويصبح التوسعة مقامرة بدل قرار.
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
              كل عميل تسلّمه بدون دليل أو proof pack هو تجديد تخسره لاحقاً بصمت.
              النطاق والسعر يُحددان بعد تشخيص لحجم عملياتك الحالية.
            </p>
          </div>
        </section>

        <section className="mt-8 rounded-2xl border border-amber-300/20 bg-amber-300/5 p-6 text-sm text-white/80">
          <p className="font-medium text-amber-200">القاعدة الذهبية</p>
          <p className="mt-2">
            لا تُسلم dashboard فارغ. كل تسليم له owner واحد على كل مؤشر، و
            cadence محدد (يومي / أسبوعي / شهري)، و proof report يُرسل للعميل
            في كل أسبوع.
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
            href="/delivery-os"
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