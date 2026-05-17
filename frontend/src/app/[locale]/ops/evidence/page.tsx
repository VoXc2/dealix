import { AppLayout } from "@/components/layout/AppLayout";
import { EvidenceLedgerConsole } from "@/components/ops/EvidenceLedgerConsole";

export default function OpsEvidencePage() {
  return (
    <AppLayout title="Evidence Ledger" subtitle="Traceable event stream for every AI action">
      <EvidenceLedgerConsole />
    </AppLayout>
  );
}

