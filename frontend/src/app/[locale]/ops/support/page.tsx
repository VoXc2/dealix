import { AppLayout } from "@/components/layout/AppLayout";
import { SupportConsole } from "@/components/ops/SupportConsole";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function SupportOpsPage({ params }: PageProps) {
  const { locale } = await params;
  const isAr = locale === "ar";
  return (
    <AppLayout
      title={isAr ? "كونسول الدعم" : "Support Console"}
      subtitle={isAr ? "التذاكر وقاعدة المعرفة" : "Tickets and knowledge base"}
    >
      <SupportConsole />
    </AppLayout>
  );
}
