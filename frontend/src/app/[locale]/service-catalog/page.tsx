import { getTranslations } from "next-intl/server";
import { AppLayout } from "@/components/layout/AppLayout";
import { ServiceCatalog } from "@/components/ops/ServiceCatalog";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function ServiceCatalogPage({ params }: PageProps) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "ops.serviceCatalog" });

  return (
    <AppLayout title={t("title")} subtitle={t("subtitle")}>
      <ServiceCatalog />
    </AppLayout>
  );
}
