import { AppLayout } from "@/components/layout/AppLayout";
import { ImprovementProposalTable } from "@/components/self-evolving/ImprovementProposalTable";

export default function SelfEvolvingPage() {
  return (
    <AppLayout title="Self Evolving" subtitle="Proposals only, approval required before apply">
      <ImprovementProposalTable />
    </AppLayout>
  );
}
