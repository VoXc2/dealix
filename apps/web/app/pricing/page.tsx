import { PREMIUM_OFFERS } from "@/lib/sales-machine/ultimate-sales-os";

export const metadata = {
  title: "Pricing — Dealix",
  description: "Transparent pricing for every offer, with a free 20-min diagnostic as the entry point.",
};

export default function PricingPage() {
  return (
    <main className="min-h-screen bg-[#070A12] text-white">
      <div className="mx-auto max-w-6xl px-6 py-16">
        <header>
          <p className="text-xs uppercase tracking-[0.3em] text-amber-300/80">Pricing</p>
          <h1 className="mt-3 text-4xl font-semibold">شفاف، بدون فخ</h1>
          <p className="mt-3 max-w-2xl text-sm text-white/70">
            سبع عروض، كل واحد له setup + monthly واضح. لا عقود طويلة، لا auto-renewals خفية، لا
            رسوم إعداد مخفية.
          </p>
        </header>

        <section className="mt-10 overflow-hidden rounded-2xl border border-white/10">
          <table className="w-full text-sm">
            <thead className="bg-white/5 text-xs uppercase tracking-widest text-amber-300/80">
              <tr>
                <th className="px-4 py-3 text-left">Offer</th>
                <th className="px-4 py-3 text-left">Setup (SAR)</th>
                <th className="px-4 py-3 text-left">Monthly (SAR)</th>
                <th className="px-4 py-3 text-left">Best for</th>
              </tr>
            </thead>
            <tbody>
              {PREMIUM_OFFERS.map((o) => (
                <tr key={o.id} className="border-t border-white/10">
                  <td className="px-4 py-3 align-top">
                    <p className="font-medium">{o.name}</p>
                    <p className="text-xs text-white/60">{o.nameAr}</p>
                  </td>
                  <td className="px-4 py-3 align-top">{o.setup}</td>
                  <td className="px-4 py-3 align-top">{o.monthly}</td>
                  <td className="px-4 py-3 align-top text-xs text-white/60">{o.bestFor.join(", ")}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>

        <section className="mt-8 rounded-2xl border border-amber-300/20 bg-amber-300/5 p-6 text-sm text-white/80">
          <p className="font-medium text-amber-200">قواعد التسعير</p>
          <ul className="mt-2 space-y-1">
            <li>• ما في setup fee مخفي، وكل setup قابل للاسترداد خلال 14 يوم.</li>
            <li>• الاشتراك الشهري قابل للإلغاء بإشعار 30 يوم.</li>
            <li>• التوسعة (Command Center → Custom Enterprise) تتبع نفس قواعد الإلغاء.</li>
            <li>• لا auto-renewal بصمت — نرسل تذكير قبل 14 يوم من تاريخ التجديد.</li>
          </ul>
        </section>
      </div>
    </main>
  );
}
