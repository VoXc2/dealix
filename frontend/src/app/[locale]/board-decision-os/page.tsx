import { getTranslations } from "next-intl/server";
import { AppLayout } from "@/components/layout/AppLayout";
import { BoardDecisionConsole } from "@/components/board-decision-os/BoardDecisionConsole";

interface BoardDecisionOsPageProps {
  params: Promise<{ locale: string }>;
}

export default async function BoardDecisionOsPage({
  params,
}: BoardDecisionOsPageProps) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "boardDecisionOs" });

  return (
    <AppLayout title={t("title")} subtitle={t("subtitle")}>
      <BoardDecisionConsole />
    </AppLayout>
  );
}
