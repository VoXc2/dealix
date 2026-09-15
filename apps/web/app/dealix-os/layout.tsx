import type { Metadata } from "next";
import type { ReactNode } from "react";

export const metadata: Metadata = {
  title: "Dealix OS — AI Business Operating System",
  description: "Dealix OS طبقة تشغيل AI Business Operating System تربط Signal → Decision → Action → Proof فوق CRM وERP والبريد والأنظمة الحالية بحوكمة وموافقات وأدلة.",
  alternates: { canonical: "/dealix-os" },
};

export default function RouteLayout({ children }: { children: ReactNode }) {
  return children;
}
