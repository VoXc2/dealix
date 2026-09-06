import Link from "next/link";

export const metadata = {
  title: "Engagement Path — Dealix",
  description:
    "Dealix تبدأ بـExecution Diagnostic، ثم Qualified Discovery وعرض خاص بالعميل، ثم Outcome Sprint وDealix Runtime عند ثبوت القيمة. لا سعر عام ولا Checkout عام.",
};

const buyingPath = [
  {
    step: "01",
    title: "Execution Diagnostic",
    text: "نحدد workflow واحدًا قابلًا للتنفيذ والقياس، baseline وصاحب قرار وحدود البيانات. لا بطاقة ولا التزام شراء.",
  },
  {
    step: "02",
    title: "Qualified Discovery + Customer-Specific Quote",
    text: "نثبت المشكلة والنطاق ومعايير الإثبات، ثم نحدد السعر والنطاق لشركة محددة فقط. لا قائمة أسعار عامة أو خصومات آلية أو Checkout عام.",
  },
  {
    step: "03",
    title: "Outcome Sprint",
    text: "تنفيذ محكوم يركز على نتيجة محددة قابلة للقياس. المدة والنطاق وشروط البدء تحدد فقط في العرض الخاص بالعميل بعد Qualified Discovery؛ لا توجد مدة عامة ملزمة.",
  },
  {
    step: "04",
    title: "Proof Review",
    text: "نقارن النتيجة بالـbaseline ونفصل activity عن value. لا synthetic/demo evidence يتحول إلى Customer Proof.",
  },
  {
    step: "05",
    title: "Dealix Runtime",
    text: "إذا أثبت الـSprint قيمة قابلة للتكرار، يمكن توسيع Dealix إلى Runtime مستمر للمراقبة والتنفيذ والإثبات. التوسع ليس تلقائيًا.",
  },
];

export default function PricingPage() {
  return (
    <main className="min-h-screen bg-[#070A12] text-white">
      <div className="mx-auto max-w-5xl px-6 py-16">
        <header>
          <p className="text-xs uppercase tracking-[0.3em] text-cyan-300/80">Signal → Decision → Action → Proof</p>
          <h1 className="mt-3 text-4xl font-semibold">مسار تنفيذ واحد، بدون باقات عامة</h1>
          <p className="mt-4 max-w-3xl text-base leading-8 text-white/70">
            Dealix لا تبيع قائمة خدمات أو اشتراكًا ذاتي التسجيل في مرحلة التدشين. نبدأ بحالة تنفيذ حقيقية،
            نثبتها، ثم نحدد نطاقًا وسعرًا خاصين بالعميل إذا كان Outcome Sprint هو الخطوة الصحيحة.
          </p>
        </header>

        <section className="mt-10 grid gap-4">
          {buyingPath.map((item) => (
            <article key={item.step} className="rounded-2xl border border-white/10 bg-white/[0.03] p-6">
              <div className="flex gap-4">
                <span className="text-sm font-semibold text-cyan-300">{item.step}</span>
                <div>
                  <h2 className="text-xl font-semibold">{item.title}</h2>
                  <p className="mt-2 leading-7 text-white/70">{item.text}</p>
                </div>
              </div>
            </article>
          ))}
        </section>

        <section className="mt-10 rounded-2xl border border-cyan-300/20 bg-cyan-300/5 p-6">
          <h2 className="text-lg font-semibold text-cyan-200">قواعد Dealix التجارية</h2>
          <ul className="mt-3 space-y-2 text-sm leading-6 text-white/75">
            <li>• Execution Diagnostic لا يمنح أي سلطة إرسال أو دفع.</li>
            <li>• لا سعر عام ولا Checkout عام للـOutcome Sprint أو Dealix Runtime.</li>
            <li>• كل عرض مرتبط بعميل محدد وبعد Qualified Discovery.</li>
            <li>• Quote ليست Invoice، وInvoice ليست Payment، وبدء التسليم المدفوع يحتاج إثبات دفع مستقل.</li>
            <li>• لا ضمان ROI أو نتيجة مالية أو مدة ثابتة لكل عميل.</li>
            <li>• Dealix Runtime يأتي بعد Proof مناسب، وليس قبلها.</li>
          </ul>
        </section>

        <section className="mt-10 text-center">
          <h2 className="text-2xl font-semibold">ابدأ بالـworkflow، لا بالباقـة</h2>
          <p className="mx-auto mt-3 max-w-2xl text-sm leading-7 text-white/65">
            إذا عندك قرار أو workflow مهم لا يتحول اليوم إلى تنفيذ محكوم ونتيجة قابلة للإثبات، ابدأ بـExecution Diagnostic.
          </p>
          <Link
            href="/book"
            className="mt-6 inline-block rounded-full bg-cyan-300 px-8 py-3 text-sm font-semibold text-black transition hover:bg-cyan-200"
          >
            اطلب Execution Diagnostic
          </Link>
        </section>
      </div>
    </main>
  );
}
