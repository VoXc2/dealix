import { AppLayout } from "@/components/layout/AppLayout";
import { RunTraceTimeline } from "@/components/control-plane/RunTraceTimeline";

interface RunDetailPageProps {
  params: Promise<{ runId: string }>;
}

export default async function RunDetailPage({ params }: RunDetailPageProps) {
  const { runId } = await params;
  return (
    <AppLayout title={`Run ${runId}`} subtitle="Trace timeline and state history">
      <RunTraceTimeline customerId={runId} />
    </AppLayout>
  );
}
