import { AppLayout } from "@/components/layout/AppLayout";
import { TrustCenter } from "@/components/trust/TrustCenter";

interface TrustCenterPageProps {
  params: Promise<{ locale: string }>;
}

export default async function TrustCenterPage({
  params,
}: TrustCenterPageProps) {
  const { locale } = await params;
  const isAr = locale === "ar";

  return (
    <AppLayout
      title={isAr ? "مركز الثقة" : "Trust Center"}
      subtitle={
        isAr
          ? "شهادات الامتثال وسياسات الأمان"
          : "Compliance certificates and security policies"
      }
    >
      <TrustCenter />
    </AppLayout>
  );
}
