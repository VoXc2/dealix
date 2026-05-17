import { getTranslations } from "next-intl/server";
import { AppLayout } from "@/components/layout/AppLayout";
import { EvidenceLedger } from "@/components/ops/EvidenceLedger";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function EvidenceLedgerPage({ params }: PageProps) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "ops.evidenceLedger" });

  return (
    <AppLayout title={t("title")} subtitle={t("subtitle")}>
      <EvidenceLedger />
    </AppLayout>
  );
}
