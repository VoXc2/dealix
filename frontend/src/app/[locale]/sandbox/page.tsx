import { AppLayout } from "@/components/layout/AppLayout";

export default function SandboxPage() {
  return (
    <AppLayout title="Sandbox" subtitle="Replay and simulation control surface">
      <div className="rounded border p-4 text-sm text-muted-foreground">
        Sandbox run orchestration is enabled in backend schemas. UI replay controls are in MVP mode.
      </div>
    </AppLayout>
  );
}
