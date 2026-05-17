import { getTranslations } from "next-intl/server";
import { AppLayout } from "@/components/layout/AppLayout";
import { BoardDecisions } from "@/components/ops/BoardDecisions";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function BoardDecisionsPage({ params }: PageProps) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "ops.boardDecisions" });

  return (
    <AppLayout title={t("title")} subtitle={t("subtitle")}>
      <BoardDecisions />
    </AppLayout>
  );
}
