"use client";

import Link from "next/link";
import posthog from "posthog-js";
import type { CSSProperties, ReactNode } from "react";

import { analyticsConsentGranted } from "@/lib/analytics/posthog";

export function TrackedLink({
  href,
  children,
  ctaId,
  surface,
  className,
  style,
}: {
  href: string;
  children: ReactNode;
  ctaId: string;
  surface: string;
  className?: string;
  style?: CSSProperties;
}) {
  return (
    <Link
      href={href}
      className={className}
      style={style}
      onClick={() => {
        if (!analyticsConsentGranted()) return;
        try {
          posthog.capture("dealix_gtm_cta_clicked", {
            cta_id: ctaId,
            surface,
            target_path: href,
            brand_architecture_version: "corporate_brand_gtm_v1",
          });
        } catch {
          // Analytics must never block navigation or the commercial experience.
        }
      }}
    >
      {children}
    </Link>
  );
}
