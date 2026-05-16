import { getTranslations } from "next-intl/server";
import { AppLayout } from "@/components/layout/AppLayout";
import { FounderCommandCenter } from "@/components/revenue-ops/RevenueOpsScreens";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function FounderCommandCenterPage({ params }: PageProps) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "revenueOps" });

  return (
    <AppLayout title={t("command.title")} subtitle={t("command.subtitle")}>
      <FounderCommandCenter />
    </AppLayout>
  );
}
