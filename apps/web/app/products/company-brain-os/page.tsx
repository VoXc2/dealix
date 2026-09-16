import Link from "next/link";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Company Brain OS — Dealix",
  description:
    "ذاكرة موحّدة للشركة: قرارات، سياسات، سياق، تاريخ — في مصدر واحد قابل للبحث.",
};

const features = [
  { en: "Unified company memory", ar: "ذاكرة موحّدة لكل قرارات وسياسات الشركة" },
  { en: "Searchable decision log", ar: "سجل قرارات قابل للبحث مع السياق والسبب" },
  { en: "Policy & playbook store", ar: "مخزن سياسات و playbooks قابل للتحديث" },
  { en: "Context per account/deal", ar: "سياق محفوظ لكل حساب وصفقة" },
  { en: "Handover-ready records", ar: "سجلات جاهزة للتسليم عند مغادرة موظف" },
  { en: "Weekly knowledge review", ar: "مراجعة معرفية أسبوعية للفجوات" },
];

export default function CompanyBrainOSPage() {
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
            Company Brain OS
          </p>
          <h1 className="mt-3 text-4xl font-semibold leading-tight">
            نظام عقل الشركة
          </h1>
          <p className="mt-2 text-sm text-white/60">
            Company Brain OS — a unified memory layer for Saudi B2B teams
          </p>
          <p className="mt-4 max-w-2xl text-sm text-white/70">
            ذاكرة موحّدة للشركة: قرارات، سياسات، سياق، تاريخ. بدلاً من أن تكون
            المعرفة محبوسة في رؤوس الأفراد وملفات مبعثرة، يصبح لديك مصدر واحد
            قابل للبحث والتسليم.
          </p>
        </header>

        <section className="mt-10 rounded-2xl border border-white/10 bg-white/5 p-6">
          <p className="text-xs uppercase tracking-widest text-amber-300/80">
            المشكلة
          </p>
          <p className="mt-2 text-sm text-white/80">
            عندما يغادر موظف، تغادر معرفته. القرارات تتكرر لأن السياق ضاع،
            والسياسات مبعثرة بين ملفات ورسائل. الفريق يعيد اختراع العجلة في كل
            صفقة جديدة.
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
              كل يوم تتأخر فيه، معرفة أهم قرار في الشركة تبقى محبوسة برأس فرد
              واحد. النطاق والسعر يُحددان بعد تشخيص لحجم شركتك.
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
            href="/brain"
            className="rounded-full border border-white/20 px-6 py-3 text-sm font-medium text-white transition hover:border-white/40"
          >
            شاهد نموذج عقل الشركة
          </Link>
          <Link
            href="/war-room"
            className="rounded-full border border-white/20 px-6 py-3 text-sm font-medium text-white transition hover:border-white/40"
          >
            شاهد غرفة القيادة
          </Link>
        </section>
      </div>
    </main>
  );
}