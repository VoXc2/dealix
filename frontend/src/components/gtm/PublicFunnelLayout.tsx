"use client";
import type { ReactNode } from "react";
import { PublicGtmShell } from "@/components/gtm/PublicGtmShell";

export function PublicFunnelLayout({ children }: { children: ReactNode }) {
  return <PublicGtmShell compactNav><div className="mx-auto max-w-4xl px-6 py-12 grid-pattern">{children}</div></PublicGtmShell>;
}
