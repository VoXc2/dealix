import { getTranslations } from "next-intl/server";
import { AppLayout } from "@/components/layout/AppLayout";
import { RevenueOps } from "@/components/ops/RevenueOps";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function RevenueOpsPage({ params }: PageProps) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "ops.revenueOps" });

  return (
    <AppLayout title={t("title")} subtitle={t("subtitle")}>
      <RevenueOps />
    </AppLayout>
  );
}
