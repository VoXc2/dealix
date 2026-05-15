import { AppLayout } from "@/components/layout/AppLayout";

export default function OrgGraphPage() {
  return (
    <AppLayout title="Org Graph" subtitle="Impact map and dependency visibility">
      <div className="rounded border p-4 text-sm text-muted-foreground">
        Org graph tenant-aware schema is enabled. Visual relationship explorer will be wired to graph APIs.
      </div>
    </AppLayout>
  );
}
