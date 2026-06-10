import type { Metadata } from "next";
import { AboutPage } from "@/components/company/AboutPage";

type Props = { params: Promise<{ locale: string }> };

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { locale } = await params;
  const isAr = locale === "ar";
  return {
    title: isAr
      ? "عن Dealix — عمليات AI محكومة للسوق السعودي"
      : "About Dealix — Governed AI Operations for Saudi Market",
    description: isAr
      ? "رسالتنا، قيمنا، والتزامنا بـ PDPL و ZATCA. Dealix مبني للثقة والامتثال في السوق السعودي."
      : "Our mission, values, and commitment to PDPL & ZATCA. Dealix is built for trust and compliance in the Saudi market.",
    alternates: { canonical: `https://dealix.me/${locale}/about` },
  };
}

export default function AboutPageRoute() {
  return <AboutPage />;
}
