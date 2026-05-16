import { getTranslations } from "next-intl/server";
import { AppLayout } from "@/components/layout/AppLayout";
import { EvidenceLedger } from "@/components/revenue-ops/RevenueOpsScreens";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function EvidenceLedgerPage({ params }: PageProps) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "revenueOps" });

  return (
    <AppLayout title={t("evidence.title")} subtitle={t("evidence.subtitle")}>
      <EvidenceLedger />
    </AppLayout>
  );
}
