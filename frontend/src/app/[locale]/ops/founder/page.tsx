import { getTranslations } from "next-intl/server";
import { AppLayout } from "@/components/layout/AppLayout";
import { OpsFounderCommandCenter } from "@/components/gtm/OpsFounderCommandCenter";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function OpsFounderPage({ params }: PageProps) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "nav" });

  return (
    <AppLayout title={t("opsFounder")} subtitle="Revenue War Room — 30/90 day GTM">
      <OpsFounderCommandCenter />
    </AppLayout>
  );
}
