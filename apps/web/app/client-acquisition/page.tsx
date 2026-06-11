import { ACQUISITION_FUNNEL } from "@/lib/company-os/company-os";

export const metadata = {
  title: "Client Acquisition OS — Dealix",
  description: "How Dealix turns signal into customers: segment → pain → offer → message → review → proposal → delivery.",
};

export default function ClientAcquisitionPage() {
  return (
    <main className="min-h-screen bg-[#070A12] text-white">
      <div className="mx-auto max-w-6xl px-6 py-12">
        <header className="mb-10">
          <p className="text-xs uppercase tracking-[0.3em] text-amber-300/80">Client Acquisition OS</p>
          <h1 className="mt-3 text-4xl font-semibold leading-tight">
            من الإشارة إلى العميل الموقّع — سبع مراحل فقط
          </h1>
          <p className="mt-3 max-w-2xl text-sm text-white/70">
            Dealix لا يبيع dashboard. يبني طبقة تشغيلية تربط: القطاع → الألم → العرض → الرسالة → المراجعة
            → العرض الرسمي → التسليم. كل مرحلة لها مخرج واضح، ومسؤول واحد، وأداة محددة.
          </p>
        </header>

        <section>
          <ol className="grid gap-4 md:grid-cols-2">
            {ACQUISITION_FUNNEL.map((step, idx) => (
              <li key={step.id} className="rounded-2xl border border-white/10 bg-white/5 p-6">
                <p className="text-xs uppercase tracking-widest text-amber-300/80">
                  Stage {idx + 1} · {step.id}
                </p>
                <h2 className="mt-2 text-lg font-semibold">{step.title}</h2>
                <p className="text-xs text-white/60">{step.titleAr}</p>
                <p className="mt-3 text-sm text-white/80">{step.goal}</p>
                <p className="mt-1 text-xs text-white/60">{step.goalAr}</p>
                <div className="mt-4 text-xs text-white/70">
                  <p>
                    <span className="text-white/50">Owner:</span> {step.owner}
                  </p>
                  <p className="mt-1">
                    <span className="text-white/50">Exit:</span> {step.exitCriteria}
                  </p>
                </div>
                <ul className="mt-3 flex flex-wrap gap-2 text-[10px] text-white/60">
                  {step.tools.map((t) => (
                    <li key={t} className="rounded-full border border-white/10 px-2 py-1">
                      {t}
                    </li>
                  ))}
                </ul>
              </li>
            ))}
          </ol>
        </section>

        <section className="mt-10 rounded-2xl border border-amber-300/20 bg-amber-300/5 p-6">
          <h2 className="text-lg font-semibold text-amber-200">لماذا هذه الطريقة تشتغل</h2>
          <ul className="mt-3 space-y-2 text-sm text-white/80">
            <li>• كل مرحلة لها exit criteria واحدة. لا غموض، لا انزلاق.</li>
            <li>• المسوّدات لا ترسل تلقائياً. المراجعة البشرية هي البوابة الوحيدة للإرسال.</li>
            <li>• العروض مولّدة من قوالب + بيانات الحساب، فالجودة ثابتة والوقت قصير.</li>
            <li>• التسليم ليس وعد — هو OS حقيقي يبدأ من اليوم الأول.</li>
          </ul>
        </section>
      </div>
    </main>
  );
}
