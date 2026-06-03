"use client";
import type { ReactNode } from "react";
import { PublicLaunchShell } from "@/components/brand/PublicLaunchShell";
import { LaunchStatusBanner } from "@/components/gtm/LaunchStatusBanner";

export function PublicGtmShell({ children, compactNav = false, showLaunchBanner = true }: { children: ReactNode; compactNav?: boolean; showLaunchBanner?: boolean }) {
  return (
    <PublicLaunchShell compactNav={compactNav}>
      {showLaunchBanner ? <div className="mx-auto max-w-5xl px-6 pt-6"><LaunchStatusBanner /></div> : null}
      {children}
    </PublicLaunchShell>
  );
}
