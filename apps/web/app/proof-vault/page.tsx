import { loadDemoWorkspaces, loadWorkspaces } from "@/lib/client/portal";
import { ProofTimeline } from "@/components/client/ProofTimeline";

export const metadata = {
  title: "Proof Vault — Dealix",
  robots: { index: false, follow: false },
};
export const dynamic = "force-static";

export default function ProofVaultPage() {
  const workspaces = [...loadDemoWorkspaces(), ...loadWorkspaces()];
  return (
    <main className="mx-auto max-w-5xl px-6 py-12">
      <h1 className="text-3xl font-semibold tracking-tight">Proof Vault</h1>
      <p className="mt-2 text-sm text-neutral-600">Evidence-only. Demo items labeled. No fake testimonials.</p>
      <div className="mt-8 space-y-8">
        {workspaces.map((w) => (
          <section key={w.id}>
            <h2 className="text-lg font-semibold">{w.clientName}</h2>
            <p className="text-sm text-neutral-500">{w.offer}</p>
            <div className="mt-3"><ProofTimeline items={w.proofItems} /></div>
          </section>
        ))}
      </div>
    </main>
  );
}
