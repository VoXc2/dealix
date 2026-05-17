import { getTranslations } from "next-intl/server";
import { AppLayout } from "@/components/layout/AppLayout";
import { ProofPack } from "@/components/ops/ProofPack";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function ProofPackPage({ params }: PageProps) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "ops.proofPack" });

  return (
    <AppLayout title={t("title")} subtitle={t("subtitle")}>
      <ProofPack />
    </AppLayout>
  );
}
