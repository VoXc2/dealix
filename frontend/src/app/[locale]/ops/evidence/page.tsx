import { AppLayout } from "@/components/layout/AppLayout";
import { EvidenceLedger } from "@/components/ops/EvidenceLedger";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function EvidenceOpsPage({ params }: PageProps) {
  const { locale } = await params;
  const isAr = locale === "ar";
  return (
    <AppLayout
      title={isAr ? "سجل الأدلة" : "Evidence Ledger"}
      subtitle={isAr ? "كل إجراء مُسجّل ومصدره" : "Every action, logged with its source"}
    >
      <EvidenceLedger />
    </AppLayout>
  );
}
