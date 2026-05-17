import { getTranslations } from "next-intl/server";
import { AppLayout } from "@/components/layout/AppLayout";
import { CommandCenter } from "@/components/ops/CommandCenter";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function CommandCenterPage({ params }: PageProps) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "ops.commandCenter" });

  return (
    <AppLayout title={t("title")} subtitle={t("subtitle")}>
      <CommandCenter />
    </AppLayout>
  );
}
