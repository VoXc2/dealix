import { getTranslations } from "next-intl/server";
import { AppLayout } from "@/components/layout/AppLayout";
import { BillingConsole } from "@/components/billing/BillingConsole";

interface BillingPageProps {
  params: Promise<{ locale: string }>;
}

export default async function BillingPage({ params }: BillingPageProps) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "billing" });

  return (
    <AppLayout title={t("title")} subtitle={t("subtitle")}>
      <BillingConsole />
    </AppLayout>
  );
}
