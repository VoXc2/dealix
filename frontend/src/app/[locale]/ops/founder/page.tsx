import { getTranslations } from "next-intl/server";
import { AppLayout } from "@/components/layout/AppLayout";
import { FounderCommandCenter } from "@/components/ops/FounderCommandCenter";

interface OpsFounderPageProps {
  params: Promise<{ locale: string }>;
}

export default async function OpsFounderPage({ params }: OpsFounderPageProps) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "opsFounder" });

  return (
    <AppLayout title={t("title")} subtitle={t("subtitle")}>
      <FounderCommandCenter />
    </AppLayout>
  );
}
