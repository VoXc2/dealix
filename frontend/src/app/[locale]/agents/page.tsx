import { getTranslations } from "next-intl/server";
import { AppLayout } from "@/components/layout/AppLayout";
import { ActivityFeed } from "@/components/agents/ActivityFeed";

interface AgentsPageProps {
  params: Promise<{ locale: string }>;
}

export default async function AgentsPage({ params }: AgentsPageProps) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "agents" });

  return (
    <AppLayout title={t("title")} subtitle={t("subtitle")}>
      <ActivityFeed />
    </AppLayout>
  );
}
