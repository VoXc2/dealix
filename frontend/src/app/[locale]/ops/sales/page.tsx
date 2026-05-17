import { AppLayout } from "@/components/layout/AppLayout";
import { SalesPipelineConsole } from "@/components/ops/SalesPipelineConsole";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function SalesOpsPage({ params }: PageProps) {
  const { locale } = await params;
  const isAr = locale === "ar";
  return (
    <AppLayout
      title={isAr ? "كونسول المبيعات" : "Sales Pipeline Console"}
      subtitle={isAr ? "المهام والأتمتة" : "Tasks and automations"}
    >
      <SalesPipelineConsole />
    </AppLayout>
  );
}
