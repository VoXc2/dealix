import Link from "next/link";

export const metadata = {
  title: "مسار الشراء — Dealix",
  description:
    "Dealix تبدأ بـMini Diagnostic مجاني، ثم Qualified Discovery، ثم عرض مخصص لـRevenue Command Pilot لمدة 30 يومًا. لا سعر عام ولا Checkout عام.",
};

const buyingPath = [
  {
    step: "01",
    title: "Free Mini Diagnostic",
    text: "نحدد مشكلة تشغيلية واحدة قابلة للقياس، صاحب القرار، والبيانات المتاحة. لا بطاقة ولا التزام شراء.",
  },
  {
    step: "02",
    title: "Qualified Discovery",
    text: "إذا كانت المشكلة مؤهلة، نثبت baseline، نطاق المسؤولية، مصدر البيانات، وطريقة قياس القيمة قبل أي عرض.",
  },
  {
    step: "03",
    title: "Customer-Specific Quote",
    text: "السعر والنطاق يحددان لشركة محددة بعد Discovery. لا توجد قائمة أسعار عامة أو خصومات آلية أو Checkout عام.",
  },
  {
    step: "04",
    title: "Revenue Command Pilot — 30 Days",
    text: "Pilot محكوم لمدة 30 يومًا، يبدأ بعد قبول العرض وإثبات الدفع. AI يقترح، والتنفيذ الحساس يبقى بموافقة بشرية.",
  },
  {
    step: "05",
    title: "Proof → Stop / Expand / Redesign",
    text: "نقيس النتيجة مقابل baseline. التوسع لا يحدث تلقائيًا؛ يُبنى فقط على Proof مقبول من العميل.",
  },
];

export default function PricingPage() {
  return (
    <main className="min-h-screen bg-[#070A12] text-white">
      <div className="mx-auto max-w-5xl px-6 py-16">
        <header>
          <p className="text-xs uppercase tracking-[0.3em] text-amber-300/80">Revenue + Proof + Command</p>
          <h1 className="mt-3 text-4xl font-semibold">مسار شراء واحد، بدون باقات عامة</h1>
          <p className="mt-4 max-w-3xl text-base leading-8 text-white/70">
            Dealix لا تبيع سبع باقات ولا اشتراكًا ذاتي التسجيل في مرحلة التدشين. نبدأ بمشكلة حقيقية،
            نثبتها، ثم نحدد نطاقًا وسعرًا خاصين بالعميل إذا كان Pilot لمدة 30 يومًا هو الخطوة الصحيحة.
          </p>
        </header>

        <section className="mt-10 grid gap-4">
          {buyingPath.map((item) => (
            <article key={item.step} className="rounded-2xl border border-white/10 bg-white/[0.03] p-6">
              <div className="flex gap-4">
                <span className="text-sm font-semibold text-amber-300">{item.step}</span>
                <div>
                  <h2 className="text-xl font-semibold">{item.title}</h2>
                  <p className="mt-2 leading-7 text-white/70">{item.text}</p>
                </div>
              </div>
            </article>
          ))}
        </section>

        <section className="mt-10 rounded-2xl border border-amber-300/20 bg-amber-300/5 p-6">
          <h2 className="text-lg font-semibold text-amber-200">قواعد Dealix التجارية</h2>
          <ul className="mt-3 space-y-2 text-sm leading-6 text-white/75">
            <li>• Mini Diagnostic مجاني ولا يحتاج بطاقة.</li>
            <li>• لا سعر عام ولا Checkout عام للـRevenue Command Pilot.</li>
            <li>• كل عرض مرتبط بعميل محدد وبعد Qualified Discovery.</li>
            <li>• Invoice ليست Payment، وبدء التسليم المدفوع يحتاج إثبات دفع مستقل.</li>
            <li>• لا ضمان ROI أو نتيجة مالية محددة مسبقًا.</li>
            <li>• أي توسع أو Retainer يأتي بعد Proof، وليس قبلها.</li>
          </ul>
        </section>

        <section className="mt-10 text-center">
          <h2 className="text-2xl font-semibold">ابدأ بالمشكلة، لا بالباقـة</h2>
          <p className="mx-auto mt-3 max-w-2xl text-sm leading-7 text-white/65">
            إذا عندك تسريب إيراد أو متابعة متقطعة أو قرار يومي مبني على أدوات متفرقة، ابدأ بـMini Diagnostic.
          </p>
          <Link
            href="/book"
            className="mt-6 inline-block rounded-full bg-amber-300 px-8 py-3 text-sm font-semibold text-black transition hover:bg-amber-200"
          >
            اطلب Mini Diagnostic مجاني
          </Link>
        </section>
      </div>
    </main>
  );
}
