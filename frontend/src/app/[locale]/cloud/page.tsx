import { getTranslations } from "next-intl/server";
import { AppLayout } from "@/components/layout/AppLayout";
import { CloudHubContent } from "@/components/cloud/CloudHubContent";

interface CloudPageProps {
  params: Promise<{ locale: string }>;
}

export default async function CloudPage({ params }: CloudPageProps) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "cloud" });

  return (
    <AppLayout title={t("title")} subtitle={t("subtitle")}>
      <CloudHubContent />
    </AppLayout>
  );
}
