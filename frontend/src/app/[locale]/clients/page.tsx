import { getTranslations } from "next-intl/server";
import { AppLayout } from "@/components/layout/AppLayout";
import { ClientManagementContent } from "@/components/clients/ClientManagementContent";

interface ClientsPageProps {
  params: Promise<{ locale: string }>;
}

export default async function ClientsPage({ params }: ClientsPageProps) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "clients" });

  return (
    <AppLayout title={t("title")} subtitle={t("subtitle")}>
      <ClientManagementContent />
    </AppLayout>
  );
}
