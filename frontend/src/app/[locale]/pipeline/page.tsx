import { getTranslations } from "next-intl/server";
import { AppLayout } from "@/components/layout/AppLayout";
import { KanbanBoard } from "@/components/pipeline/KanbanBoard";

interface PipelinePageProps {
  params: Promise<{ locale: string }>;
}

export default async function PipelinePage({ params }: PipelinePageProps) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "pipeline" });

  return (
    <AppLayout title={t("title")} subtitle={t("subtitle")}>
      <KanbanBoard />
    </AppLayout>
  );
}
