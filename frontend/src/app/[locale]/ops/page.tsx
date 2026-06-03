import { AppLayout } from "@/components/layout/AppLayout";
import { OpsHubHealthCards } from "@/components/gtm/OpsHubHealthCards";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function OpsHubPage({ params }: PageProps) {
  const { locale } = await params;
  const isAr = locale === "ar";

  return (
    <AppLayout
      title={isAr ? "تشغيل المؤسس" : "Founder Ops"}
      subtitle={isAr ? "غرفة واحدة لكل مسارات /ops" : "Single hub for all /ops routes"}
    >
      <OpsHubHealthCards />
    </AppLayout>
  );
}
