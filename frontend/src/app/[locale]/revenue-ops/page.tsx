import { getTranslations } from "next-intl/server";
import { AppLayout } from "@/components/layout/AppLayout";
import { RevenueOpsConsole } from "@/components/revenue-ops/RevenueOpsConsole";

interface RevenueOpsPageProps {
  params: Promise<{ locale: string }>;
}

export default async function RevenueOpsPage({ params }: RevenueOpsPageProps) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "revenueOps" });

  return (
    <AppLayout title={t("title")} subtitle={t("subtitle")}>
      <RevenueOpsConsole />
    </AppLayout>
  );
}
