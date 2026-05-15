import { getTranslations } from "next-intl/server";
import { AppLayout } from "@/components/layout/AppLayout";
import { KnowledgeContent } from "@/components/knowledge/KnowledgeContent";

interface KnowledgePageProps {
  params: Promise<{ locale: string }>;
}

export default async function KnowledgePage({ params }: KnowledgePageProps) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "knowledge" });

  return (
    <AppLayout title={t("title")} subtitle={t("subtitle")}>
      <KnowledgeContent />
    </AppLayout>
  );
}
