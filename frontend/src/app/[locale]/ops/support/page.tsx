import { getTranslations } from "next-intl/server";

import { AppLayout } from "@/components/layout/AppLayout";
import { SupportQueuePanel } from "@/components/revenue-autopilot/OpsConsoles";

interface Props {
  params: Promise<{ locale: string }>;
}

export default async function OpsSupportPage({ params }: Props) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "nav" });

  return (
    <AppLayout title={t("opsSupport")} subtitle="Governed drafts + escalation">
      <SupportQueuePanel locale={locale} />
    </AppLayout>
  );
}
