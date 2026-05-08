import { getTranslations } from "next-intl/server";
import { AppLayout } from "@/components/layout/AppLayout";
import { ApprovalCenter } from "@/components/approvals/ApprovalCenter";

interface ApprovalsPageProps {
  params: Promise<{ locale: string }>;
}

export default async function ApprovalsPage({ params }: ApprovalsPageProps) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "approvals" });

  return (
    <AppLayout title={t("title")} subtitle={t("subtitle")}>
      <ApprovalCenter />
    </AppLayout>
  );
}
