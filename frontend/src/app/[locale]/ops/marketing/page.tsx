import { getTranslations } from "next-intl/server";
import { AppLayout } from "@/components/layout/AppLayout";
import { OpsMarketingHub } from "@/components/gtm/OpsMarketingHub";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function OpsMarketingPage({ params }: PageProps) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "nav" });

  return (
    <AppLayout title={t("opsMarketing")} subtitle="Social drafts — governed publish">
      <OpsMarketingHub />
    </AppLayout>
  );
}
