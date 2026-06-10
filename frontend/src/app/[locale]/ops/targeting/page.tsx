import { getTranslations } from "next-intl/server";
import { AppLayout } from "@/components/layout/AppLayout";
import { OpsTargetingPanel } from "@/components/gtm/OpsTargetingPanel";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function OpsTargetingPage({ params }: PageProps) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "nav" });

  return (
    <AppLayout
      title={t("opsTargeting")}
      subtitle="P0 rotation · agency seed CSV · War Room import"
    >
      <OpsTargetingPanel />
    </AppLayout>
  );
}
