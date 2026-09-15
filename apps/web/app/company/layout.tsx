import type { Metadata } from "next";
import type { ReactNode } from "react";

export const metadata: Metadata = {
  title: "Dealix Company — Saudi B2B Strategy, Systems & AI",
  description: "Dealix شركة B2B سعودية تجمع الاستراتيجية، الأنظمة، الذكاء، الأتمتة والمنتجات في Company Machine واحدة مع تنفيذ محكوم وProof قابل للمراجعة.",
  alternates: { canonical: "/company" },
};

export default function RouteLayout({ children }: { children: ReactNode }) {
  return children;
}
