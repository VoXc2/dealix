import type { Metadata } from "next";
import { PublicFunnelLayout } from "@/components/gtm/PublicFunnelLayout";
import { ProofPackSampleView } from "@/components/gtm/ProofPackSampleView";
import { buildFunnelMetadata } from "@/lib/gtmMetadata";

type PageProps = { params: Promise<{ locale: string }> };

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { locale } = await params;
  return buildFunnelMetadata(locale, "proof-pack");
}

export default function ProofPackPage() {
  return (
    <PublicFunnelLayout>
      <ProofPackSampleView />
    </PublicFunnelLayout>
  );
}
