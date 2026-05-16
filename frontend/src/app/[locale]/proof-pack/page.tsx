import { getTranslations } from "next-intl/server";
import { AppLayout } from "@/components/layout/AppLayout";
import { ProofPackGenerator } from "@/components/proof-pack/ProofPackGenerator";

interface ProofPackPageProps {
  params: Promise<{ locale: string }>;
}

export default async function ProofPackPage({ params }: ProofPackPageProps) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "proofPack" });

  return (
    <AppLayout title={t("title")} subtitle={t("subtitle")}>
      <ProofPackGenerator />
    </AppLayout>
  );
}
