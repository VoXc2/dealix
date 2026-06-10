import { getTranslations } from "next-intl/server";
import { AppLayout } from "@/components/layout/AppLayout";
import { OpsPartnersPanel } from "@/components/gtm/OpsPartnersPanel";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function OpsPartnersPage({ params }: PageProps) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "nav" });

  return (
    <AppLayout title={t("opsPartners")} subtitle="Partner pipeline & CSV import">
      <OpsPartnersPanel />
    </AppLayout>
  );
}
