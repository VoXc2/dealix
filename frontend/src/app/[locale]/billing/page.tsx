import { getTranslations } from "next-intl/server";
import { AppLayout } from "@/components/layout/AppLayout";
import { Billing } from "@/components/ops/Billing";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function BillingPage({ params }: PageProps) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "ops.billing" });

  return (
    <AppLayout title={t("title")} subtitle={t("subtitle")}>
      <Billing />
    </AppLayout>
  );
}
