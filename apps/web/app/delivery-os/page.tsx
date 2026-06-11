import { DELIVERY_PIPELINE } from "@/lib/company-os/company-os";

export const metadata = {
  title: "Delivery OS — Dealix",
  description: "How Dealix delivers a real operating system to the client in 30 days, with proof, governance, and expansion.",
};

export default function DeliveryOsPage() {
  return (
    <main className="min-h-screen bg-[#070A12] text-white">
      <div className="mx-auto max-w-6xl px-6 py-12">
        <header className="mb-10">
          <p className="text-xs uppercase tracking-[0.3em] text-amber-300/80">Delivery OS</p>
          <h1 className="mt-3 text-4xl font-semibold leading-tight">
            تسليم احترافي، من اليوم صفر إلى التوسعة
          </h1>
          <p className="mt-3 max-w-2xl text-sm text-white/70">
            المنهج نفسه لكل عميل: استلام → خريطة عمل → غرفة قيادة → أتمتة → مراجعة أسبوعية → توسعة.
            لا يوجد تسليم بدون proof report، ولا توسعة بدون دليل.
          </p>
        </header>

        <section>
          <ol className="space-y-4">
            {DELIVERY_PIPELINE.map((stage, idx) => (
              <li key={stage.id} className="rounded-2xl border border-white/10 bg-white/5 p-6">
                <p className="text-xs uppercase tracking-widest text-amber-300/80">
                  Stage {idx + 1} · {stage.dayRange}
                </p>
                <h2 className="mt-2 text-lg font-semibold">{stage.title}</h2>
                <p className="text-xs text-white/60">{stage.titleAr}</p>
                <div className="mt-4 grid gap-4 md:grid-cols-2">
                  <div>
                    <p className="text-xs uppercase text-white/50">Deliverables</p>
                    <ul className="mt-2 space-y-1 text-sm text-white/80 list-disc list-inside">
                      {stage.deliverables.map((d) => (
                        <li key={d}>{d}</li>
                      ))}
                    </ul>
                  </div>
                  <div>
                    <p className="text-xs uppercase text-white/50">المخرجات بالعربي</p>
                    <ul className="mt-2 space-y-1 text-sm text-white/80 list-disc list-inside">
                      {stage.deliverablesAr.map((d) => (
                        <li key={d}>{d}</li>
                      ))}
                    </ul>
                  </div>
                </div>
                <p className="mt-3 text-xs text-rose-200/80">
                  <span className="text-rose-300/80">Risk:</span> {stage.risk} · {stage.riskAr}
                </p>
              </li>
            ))}
          </ol>
        </section>

        <section className="mt-10 rounded-2xl border border-amber-300/20 bg-amber-300/5 p-6">
          <h2 className="text-lg font-semibold text-amber-200">قاعدة ذهبية</h2>
          <p className="mt-2 text-sm text-white/80">
            لا تُسلم dashboard فارغ. كل تسليم له owner واحد على كل مؤشر، و cadence محدد (يومي / أسبوعي /
            شهري)، و proof report يُرسل للعميل في كل أسبوع.
          </p>
        </section>
      </div>
    </main>
  );
}
