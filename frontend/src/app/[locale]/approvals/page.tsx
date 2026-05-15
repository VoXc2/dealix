import { getTranslations } from "next-intl/server";
import { AppLayout } from "@/components/layout/AppLayout";
import { ApprovalCenter } from "@/components/approvals/ApprovalCenter";
import { ApprovalDecisionModal } from "@/components/approvals/ApprovalDecisionModal";
import { OversightQueue } from "@/components/approvals/OversightQueue";

interface ApprovalsPageProps {
  params: Promise<{ locale: string }>;
}

export default async function ApprovalsPage({ params }: ApprovalsPageProps) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "approvals" });

  return (
    <AppLayout title={t("title")} subtitle={t("subtitle")}>
      <div className="space-y-4">
        <OversightQueue />
        <ApprovalDecisionModal approvalId="demo-approval-id" />
        <ApprovalCenter />
      </div>
    </AppLayout>
  );
}
