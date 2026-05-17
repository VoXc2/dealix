import { AppLayout } from "@/components/layout/AppLayout";
import { FounderCommandCenter } from "@/components/ops/FounderCommandCenter";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function FounderOpsPage({ params }: PageProps) {
  const { locale } = await params;
  const isAr = locale === "ar";
  return (
    <AppLayout
      title={isAr ? "مركز قيادة المؤسس" : "Founder Command Center"}
      subtitle={isAr ? "ما يحتاج قرارك اليوم" : "What needs your decision today"}
    >
      <FounderCommandCenter />
    </AppLayout>
  );
}
