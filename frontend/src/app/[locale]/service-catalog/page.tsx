import { getTranslations } from "next-intl/server";
import { AppLayout } from "@/components/layout/AppLayout";
import { ServiceCatalog } from "@/components/revenue-ops/RevenueOpsScreens";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function ServiceCatalogPage({ params }: PageProps) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "revenueOps" });

  return (
    <AppLayout title={t("catalog.title")} subtitle={t("catalog.subtitle")}>
      <ServiceCatalog />
    </AppLayout>
  );
}
