import Link from "next/link";

export const metadata = {
  title: "Proof Vault — Dealix",
  description:
    "سجل إثبات قائم على الأدلة. لا تنشر Dealix حالات أو نتائج عامة قبل التحقق والموافقة المناسبة.",
};

export default function CaseStudiesPage() {
  return (
    <main dir="rtl" className="min-h-screen bg-[#06111f] text-white">
      <section className="mx-auto max-w-4xl px-6 py-20">
        <p className="mb-5 inline-flex rounded-full border border-cyan-300/30 px-4 py-2 text-sm text-cyan-100">
          Proof Vault · Evidence-only
        </p>
        <h1 className="max-w-3xl text-4xl font-black leading-[1.15] md:text-6xl">
          لا ننشر نتائج بلا دليل وموافقة.
        </h1>
        <p className="mt-7 max-w-3xl text-xl leading-9 text-slate-300">
          لا تحتوي هذه الصفحة على أرقام أو شهادات عملاء عامة. أي Customer Proof يجب أن يرتبط
          بـbaseline ومصادر ونتيجة قابلة للمراجعة وموافقة مناسبة للنشر.
        </p>
        <div className="mt-8 rounded-2xl border border-white/10 bg-white/[0.03] p-6 text-slate-300">
          <h2 className="text-xl font-semibold text-white">ما الذي نتحقق منه؟</h2>
          <ul className="mt-4 space-y-3 text-sm leading-7">
            <li>• الفرق بين demo أو synthetic evidence وبين Customer Proof.</li>
            <li>• baseline وowner ومرجع المصدر ومعيار القبول.</li>
            <li>• موافقة العميل على أي استخدام خارجي قبل النشر.</li>
          </ul>
        </div>
        <div className="mt-8 flex flex-wrap gap-4">
          <Link
            href="/cases"
            className="rounded-2xl bg-cyan-400 px-8 py-3 font-semibold text-[#06111f] hover:bg-cyan-300"
          >
            شاهد Proof Vault
          </Link>
          <Link
            href="/book"
            className="rounded-2xl border border-white/20 px-8 py-3 font-semibold hover:bg-white/10"
          >
            ابدأ التشخيص المجاني
          </Link>
        </div>
      </section>
    </main>
  );
}
