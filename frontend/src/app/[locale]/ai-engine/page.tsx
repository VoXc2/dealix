import { AppLayout } from "@/components/layout/AppLayout";
import { AIRevenueEngine } from "@/components/ai/AIRevenueEngine";

export default async function AIEnginePage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  return (
    <AppLayout
      title={locale === "ar" ? "محرك الإيرادات الذكي" : "AI Revenue Engine"}
      subtitle={
        locale === "ar"
          ? "توصيات ذكية لزيادة إيراداتك"
          : "Smart recommendations to grow revenue"
      }
    >
      <AIRevenueEngine />
    </AppLayout>
  );
}
