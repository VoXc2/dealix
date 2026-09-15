import type { Metadata } from "next";
import type { ReactNode } from "react";

export const metadata: Metadata = {
  title: "Company — Dealix",
  alternates: { canonical: "/company" },
};

export default function RouteLayout({ children }: { children: ReactNode }) {
  return children;
}
