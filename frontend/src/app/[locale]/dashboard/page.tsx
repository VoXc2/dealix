import { getTranslations } from "next-intl/server";
import { AppLayout } from "@/components/layout/AppLayout";
import { DashboardContent } from "@/components/dashboard/DashboardContent";

interface DashboardPageProps {
  params: Promise<{ locale: string }>;
}

export default async function DashboardPage({ params }: DashboardPageProps) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "dashboard" });

  return (
    <AppLayout title={t("title")} subtitle={t("subtitle")}>
      <DashboardContent />
    </AppLayout>
  );
}
