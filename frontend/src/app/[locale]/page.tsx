import type { Metadata } from "next";
import { buildHomeMetadata } from "@/lib/gtmMetadata";
import { CommercialLaunchHome } from "@/components/gtm/CommercialLaunchHome";

type PageProps = { params: Promise<{ locale: string }> };

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { locale } = await params;
  return buildHomeMetadata(locale);
}

export default function HomePage() {
  return <CommercialLaunchHome />;
}
