import { getTranslations } from "next-intl/server";
import { AppLayout } from "@/components/layout/AppLayout";
import { AnalyticsContent } from "@/components/analytics/AnalyticsContent";

interface AnalyticsPageProps {
  params: Promise<{ locale: string }>;
}

export default async function AnalyticsPage({ params }: AnalyticsPageProps) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "analytics" });

  return (
    <AppLayout title={t("title")} subtitle={t("subtitle")}>
      <AnalyticsContent />
    </AppLayout>
  );
}
