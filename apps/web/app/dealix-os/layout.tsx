import type { Metadata } from "next";
import type { ReactNode } from "react";

export const metadata: Metadata = {
  title: "Dealix OS — AI Business Operating System",
  alternates: { canonical: "/dealix-os" },
};

export default function RouteLayout({ children }: { children: ReactNode }) {
  return children;
}
