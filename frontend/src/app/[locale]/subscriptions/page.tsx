import { getTranslations } from "next-intl/server";
import { AppLayout } from "@/components/layout/AppLayout";
import { SubscriptionManager } from "@/components/subscriptions/SubscriptionManager";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function SubscriptionsPage({ params }: PageProps) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "subscriptions" });

  return (
    <AppLayout
      title={t("title")}
      subtitle={t("subtitle")}
    >
      <SubscriptionManager />
    </AppLayout>
  );
}
