import { getTranslations } from "next-intl/server";
import { AppLayout } from "@/components/layout/AppLayout";
import { RevenueWarRoomTable } from "@/components/gtm/RevenueWarRoomTable";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function OpsWarRoomPage({ params }: PageProps) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "warRoom" });

  return (
    <AppLayout title={t("title")} subtitle={t("subtitle")}>
      <RevenueWarRoomTable />
    </AppLayout>
  );
}
