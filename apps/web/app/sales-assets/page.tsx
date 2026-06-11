export const metadata = {
  title: "Sales Assets — Dealix",
  description: "Ready-to-use assets: decks, one-pagers, scripts, and proof reports.",
};

const ASSETS = [
  { id: "pitch_deck", name: "Pitch Deck (AR/EN)", format: "PPTX + PDF", size: "1.4 MB" },
  { id: "one_pager_ar", name: "One Pager (AR)", format: "PDF", size: "220 KB" },
  { id: "one_pager_en", name: "One Pager (EN)", format: "PDF", size: "220 KB" },
  { id: "objection_card", name: "Objection Handling Card", format: "PDF", size: "180 KB" },
  { id: "case_card", name: "Industry Case Card", format: "PDF", size: "200 KB" },
  { id: "script_discovery", name: "Discovery Call Script", format: "MD", size: "12 KB" },
  { id: "script_close", name: "Closing Playbook", format: "MD", size: "16 KB" },
  { id: "proof_template", name: "Proof Report Template", format: "MD", size: "10 KB" },
];

export default function SalesAssetsPage() {
  return (
    <main className="min-h-screen bg-[#070A12] text-white">
      <div className="mx-auto max-w-6xl px-6 py-16">
        <header>
          <p className="text-xs uppercase tracking-[0.3em] text-amber-300/80">Sales Assets</p>
          <h1 className="mt-3 text-4xl font-semibold">كل اللي تحتاجه في مكالمة واحدة</h1>
          <p className="mt-3 max-w-2xl text-sm text-white/70">
            8 أصول جاهزة — كلها تتحدث مع نفس التموضع ونفس قواعد الإقناع. ما في رسايل متضاربة.
          </p>
        </header>

        <section className="mt-10 grid gap-3 md:grid-cols-2">
          {ASSETS.map((a) => (
            <article key={a.id} className="flex items-center justify-between rounded-2xl border border-white/10 bg-white/5 p-5">
              <div>
                <p className="font-medium">{a.name}</p>
                <p className="text-xs text-white/60">{a.format} · {a.size}</p>
              </div>
              <span className="rounded-full border border-amber-300/30 bg-amber-300/10 px-3 py-1 text-[11px] text-amber-200">
                draft
              </span>
            </article>
          ))}
        </section>
      </div>
    </main>
  );
}
