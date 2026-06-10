import { AppLayout } from "@/components/layout/AppLayout";
import { CRMDashboard } from "@/components/crm/CRMDashboard";

interface CRMPageProps {
  params: Promise<{ locale: string }>;
}

export default async function CRMPage({ params }: CRMPageProps) {
  const { locale } = await params;
  const isAr = locale === "ar";

  return (
    <AppLayout
      title={isAr ? "نظام إدارة العملاء (CRM)" : "CRM — Customer Relationship Management"}
      subtitle={isAr ? "إدارة العملاء المحتملين، خط الصفقات، والنشاطات" : "Manage leads, deal pipeline, and activities"}
    >
      <CRMDashboard />
    </AppLayout>
  );
}
