import { AppLayout } from "@/components/layout/AppLayout";
import { AgentScoreCard } from "@/components/agents/AgentScoreCard";
import { AgentTrustBoundaryEditor } from "@/components/agents/AgentTrustBoundaryEditor";

interface AgentDetailPageProps {
  params: Promise<{ agentId: string }>;
}

export default async function AgentDetailPage({ params }: AgentDetailPageProps) {
  const { agentId } = await params;
  return (
    <AppLayout title={`Agent ${agentId}`} subtitle="Trust and autonomy controls">
      <div className="space-y-4">
        <AgentScoreCard />
        <AgentTrustBoundaryEditor />
      </div>
    </AppLayout>
  );
}
