import { getTranslations } from "next-intl/server";
import { AppLayout } from "@/components/layout/AppLayout";
import { RevenueOpsConsole } from "@/components/revenue-ops/RevenueOpsConsole";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function RevenueOpsConsolePage({ params }: PageProps) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "revenueOps" });

  return (
    <AppLayout title={t("console.title")} subtitle={t("console.subtitle")}>
      <RevenueOpsConsole />
    </AppLayout>
  );
}
