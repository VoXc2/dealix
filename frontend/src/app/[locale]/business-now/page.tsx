import { getTranslations } from "next-intl/server";
import { AppLayout } from "@/components/layout/AppLayout";
import { BusinessNowContent } from "@/components/business/BusinessNowContent";

interface BusinessNowPageProps {
  params: Promise<{ locale: string }>;
}

export default async function BusinessNowPage({ params }: BusinessNowPageProps) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "businessNow" });

  return (
    <AppLayout title={t("title")} subtitle={t("subtitle")}>
      <BusinessNowContent />
    </AppLayout>
  );
}
