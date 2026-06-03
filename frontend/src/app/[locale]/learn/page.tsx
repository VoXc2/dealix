import type { Metadata } from "next";
import { PublicGtmShell } from "@/components/gtm/PublicGtmShell";
import { LearnHub } from "@/components/learn/LearnHub";
import { buildFunnelMetadata } from "@/lib/gtmMetadata";

type PageProps = { params: Promise<{ locale: string }> };

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { locale } = await params;
  return buildFunnelMetadata(locale, "learn");
}

export default async function LearnIndexPage({ params }: PageProps) {
  const { locale } = await params;

  return (
    <PublicGtmShell compactNav>
      <main
        className={`mx-auto max-w-4xl px-6 py-12 ${locale === "ar" ? "text-right" : "text-left"}`}
        dir={locale === "ar" ? "rtl" : "ltr"}
      >
        <LearnHub />
      </main>
    </PublicGtmShell>
  );
}
