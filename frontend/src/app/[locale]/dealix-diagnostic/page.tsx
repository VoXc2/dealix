import type { Metadata } from "next";
import { PublicFunnelLayout } from "@/components/gtm/PublicFunnelLayout";
import { DealixDiagnosticLanding } from "@/components/gtm/DealixDiagnosticLanding";
import { buildFunnelMetadata } from "@/lib/gtmMetadata";

type PageProps = { params: Promise<{ locale: string }> };

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { locale } = await params;
  return buildFunnelMetadata(locale, "diagnostic");
}

export default function DealixDiagnosticPage() {
  return (
    <PublicFunnelLayout>
      <DealixDiagnosticLanding />
    </PublicFunnelLayout>
  );
}
