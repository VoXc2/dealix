import type { Metadata } from "next";
import type { ReactNode } from "react";

export const metadata: Metadata = {
  title: "Book a Free Execution Diagnostic — Dealix",
  alternates: { canonical: "/book" },
};

export default function RouteLayout({ children }: { children: ReactNode }) {
  return children;
}
