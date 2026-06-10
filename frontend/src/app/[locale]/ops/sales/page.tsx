import { getTranslations } from "next-intl/server";
import { AppLayout } from "@/components/layout/AppLayout";
import { OpsSalesPipeline } from "@/components/gtm/OpsSalesPipeline";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function OpsSalesPage({ params }: PageProps) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "nav" });

  return (
    <AppLayout title={t("opsSales")} subtitle="Autopilot pipeline stages">
      <OpsSalesPipeline />
    </AppLayout>
  );
}
