import { getTranslations } from "next-intl/server";
import { AppLayout } from "@/components/layout/AppLayout";
import { OpsEvidenceLedger } from "@/components/gtm/OpsEvidenceLedger";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function OpsEvidencePage({ params }: PageProps) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "nav" });

  return (
    <AppLayout title={t("opsEvidence")} subtitle="Evidence events trail">
      <OpsEvidenceLedger />
    </AppLayout>
  );
}
