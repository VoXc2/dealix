import { AppLayout } from "@/components/layout/AppLayout";
import { ActivityFeed } from "@/components/agents/ActivityFeed";
import { AgentRegistryTable } from "@/components/agents/AgentRegistryTable";
import { AgentScoreCard } from "@/components/agents/AgentScoreCard";
import { AgentTrustBoundaryEditor } from "@/components/agents/AgentTrustBoundaryEditor";

export default function AgentsPage() {
  return (
    <AppLayout title="Agents" subtitle="Registry, trust boundaries, and routing posture">
      <div className="space-y-4">
        <AgentScoreCard />
        <AgentRegistryTable />
        <AgentTrustBoundaryEditor />
        <ActivityFeed />
      </div>
    </AppLayout>
  );
}
