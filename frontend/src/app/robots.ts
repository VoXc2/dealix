import type { MetadataRoute } from "next";
import { INTERNAL_API_PREFIXES, INTERNAL_PAGE_PREFIXES } from "@/lib/internalSurfaces";

const BASE = process.env.NEXT_PUBLIC_SITE_URL || "https://dealix.me";

export default function robots(): MetadataRoute.Robots {
  // Crawl hygiene only — robots/noindex is NOT access control. Enforcement is
  // the fail-closed server-side gate in `src/middleware.ts` backed by
  // `src/lib/internalSurfaces.ts`.
  return {
    rules: {
      userAgent: "*",
      allow: "/",
      disallow: ["/api/", "/ops/", ...INTERNAL_PAGE_PREFIXES, ...INTERNAL_API_PREFIXES],
    },
    sitemap: `${BASE}/sitemap.xml`,
  };
}
