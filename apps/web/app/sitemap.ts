import type { MetadataRoute } from "next";

const siteUrl = process.env.NEXT_PUBLIC_SITE_URL ?? "https://dealix.me";
const now = new Date();

export default function sitemap(): MetadataRoute.Sitemap {
  const pages: Array<{
    path: string;
    priority: number;
    changeFrequency: "always" | "hourly" | "daily" | "weekly" | "monthly" | "yearly" | "never";
  }> = [
    // Canonical public conversion and trust surfaces only. Internal operating
    // surfaces are intentionally excluded because robots.ts blocks them from
    // indexing. Sitemap and robots must never send contradictory index signals.
    //
    // The old /ar/* subtree redirects to the canonical paths in next.config.js.
    // Do not emit hreflang alternates until independently served locale URLs
    // exist; a redirect target is not a separate language landing page.
    { path: "",                 priority: 1.0,  changeFrequency: "daily"  },
    { path: "/pricing",         priority: 0.95, changeFrequency: "weekly" },
    { path: "/services",        priority: 0.85, changeFrequency: "weekly" },
    { path: "/cases",           priority: 0.75, changeFrequency: "weekly" },
    { path: "/book",            priority: 0.85, changeFrequency: "weekly" },
    { path: "/products",        priority: 0.75, changeFrequency: "weekly" },
    { path: "/status",          priority: 0.80, changeFrequency: "daily"  },
    { path: "/safety",          priority: 0.70, changeFrequency: "weekly" },
    { path: "/value-engine",    priority: 0.70, changeFrequency: "weekly" },
    { path: "/revenue-os",      priority: 0.70, changeFrequency: "weekly" },
    { path: "/go-to-market",    priority: 0.60, changeFrequency: "weekly" },
    { path: "/product-network", priority: 0.60, changeFrequency: "weekly" },
  ];

  return pages.map(({ path, priority, changeFrequency }) => ({
    url: `${siteUrl}${path}`,
    lastModified: now,
    changeFrequency,
    priority,
  }));
}
