import type { Metadata } from "next";
import type { ReactNode } from "react";

export const metadata: Metadata = {
  title: "Free Execution Diagnostic — Dealix",
  description: "ابدأ تشخيص تنفيذ مجاني لشركتك في السعودية: workflow واحد، baseline، owner، evidence gaps وKPI واضح قبل أي نطاق أو سعر مدفوع. بدون بطاقة وبدون التزام شراء.",
  alternates: { canonical: "/book" },
  openGraph: {
    title: "Free Execution Diagnostic — Dealix",
    description: "تشخيص مجاني يبدأ من workflow حقيقي وbaseline وأدلة قبل أي عرض خاص بالعميل.",
    url: "/book",
    type: "website",
  },
};

export default function RouteLayout({ children }: { children: ReactNode }) {
  return children;
}
