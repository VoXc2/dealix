export const metadata = {
  title: "Dealix Control Room | غرفة التحكم",
  description: "غرفة تحكم Dealix للمؤسس: إنتاج، أوامر المخ، المبيعات، العروض، والمراقبة.",
};

const links = [
  { title: "Production Demo", href: "/ar/demo", desc: "افتح الديمو أمام العميل." },
  { title: "Revenue OS", href: "/revenue-os", desc: "رواية المنتج الأساسية." },
  { title: "Go To Market", href: "/go-to-market", desc: "خطة التصريف والسوق." },
  { title: "ZATCA Readiness", href: "/ar/zatca-readiness", desc: "مدخل امتثال + إيراد." },
];

const commands = [
  'python scripts/dealix_brain_control.py status',
  'python scripts/dealix_brain_control.py ask "وش تشتغل عليه الشركة اليوم؟"',
  'python scripts/dealix_brain_control.py ask "جهز خطة اليوم لتصريف P1 وفتح 3 مكالمات"',
  'python scripts/dealix_brain_control.py ask "راجع صفحات الموقع والعروض وحدد أهم 3 تحسينات تزيد التحويل"',
  'python scripts/dealix_brain_control.py tick',
  'cat reports/company_os/control/latest_response.md',
  'python scripts/dealix_brain_control.py doctor',
];

export default function ControlRoomPage() {
  return (
    <main dir="rtl" className="min-h-screen bg-[#06111f] px-6 py-12 text-white">
      <section className="mx-auto max-w-7xl">
        <p className="mb-4 inline-flex rounded-full border border-cyan-300/30 px-4 py-2 text-sm text-cyan-100">
          Dealix Founder Control Room
        </p>

        <h1 className="max-w-5xl text-4xl font-black leading-tight md:text-6xl">
          غرفة تحكم Dealix: المخ الداخلي، الإنتاج، المبيعات، والتشغيل من مكان واحد.
        </h1>

        <p className="mt-6 max-w-4xl text-lg leading-8 text-slate-300">
          هذه الصفحة هي بوابة المؤسس. منها تفتح الديمو، تراجع صفحات البيع، وتستخدم GitHub Actions لإرسال أوامر للمخ الداخلي من الجوال. القاعدة: AI drafts → Founder approves → Human sends.
        </p>

        <div className="mt-10 grid gap-5 md:grid-cols-4">
          {links.map((x) => (
            <a key={x.href} href={x.href} className="rounded-3xl border border-white/10 bg-white/[0.06] p-6 transition hover:bg-white/[0.10]">
              <h2 className="text-xl font-black text-cyan-100">{x.title}</h2>
              <p className="mt-3 leading-7 text-slate-300">{x.desc}</p>
            </a>
          ))}
        </div>

        <section className="mt-10 rounded-3xl border border-emerald-300/20 bg-emerald-400/10 p-8">
          <h2 className="text-3xl font-black text-emerald-100">كيف تكلم المخ من الجوال؟</h2>
          <ol className="mt-5 space-y-3 leading-8 text-slate-200">
            <li>1. افتح GitHub من الجوال.</li>
            <li>2. ادخل الريبو Dealix-sa/dealix.</li>
            <li>3. افتح Actions.</li>
            <li>4. اختر Brain Control Command.</li>
            <li>5. اضغط Run workflow واكتب الأمر.</li>
            <li>6. بعد التشغيل افتح Artifacts وشوف الرد.</li>
          </ol>
        </section>

        <section className="mt-10 rounded-3xl border border-white/10 bg-black/30 p-8">
          <h2 className="text-3xl font-black">أوامر جاهزة للمخ</h2>
          <div className="mt-5 grid gap-4">
            {commands.map((cmd) => (
              <code key={cmd} className="block overflow-x-auto rounded-2xl border border-white/10 bg-slate-950 p-4 text-left text-sm text-cyan-100" dir="ltr">
                {cmd}
              </code>
            ))}
          </div>
        </section>

        <section className="mt-10 rounded-3xl border border-amber-300/20 bg-amber-400/10 p-8">
          <h2 className="text-3xl font-black text-amber-100">ماذا يفعل 24/7؟</h2>
          <ul className="mt-5 space-y-3 leading-8 text-slate-200">
            <li>• يفحص الإنتاج: API/Web/Demo/Revenue OS.</li>
            <li>• يولد CEO brief وGrowth scorecard.</li>
            <li>• يحفظ أوامر المؤسس في inbox.</li>
            <li>• يحول الأوامر إلى actions قابلة للتنفيذ.</li>
            <li>• يمنع auto-send وscraping والنشر الخارجي بدون موافقة.</li>
          </ul>
        </section>
      </section>
    </main>
  );
}
