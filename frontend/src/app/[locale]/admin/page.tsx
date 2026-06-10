import { AppLayout } from "@/components/layout/AppLayout";
import { AdminConsole } from "@/components/admin/AdminConsole";

interface AdminPageProps {
  params: Promise<{ locale: string }>;
}

export default async function AdminPage({ params }: AdminPageProps) {
  const { locale } = await params;
  return (
    <AppLayout
      title={locale === "ar" ? "لوحة الإدارة" : "Admin Console"}
      subtitle={
        locale === "ar" ? "إدارة المستخدمين والإعدادات" : "Manage users and settings"
      }
    >
      <AdminConsole />
    </AppLayout>
  );
}
