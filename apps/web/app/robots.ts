import type { MetadataRoute } from "next";

const siteUrl = process.env.NEXT_PUBLIC_SITE_URL ?? "https://dealix.me";

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      {
        userAgent: "*",
        allow: [
          "/",
          "/ar/",
          "/ar/p1",
          "/ar/p2",
          "/ar/p3",
          "/ar/pricing",
          "/ar/demo",
          "/ar/zatca-readiness",
          "/status",
          "/revenue-os",
          "/go-to-market",
          "/product-network",
          "/safety",
          "/value-engine",
        ],
        // Block internal ops surfaces from indexing
        disallow: [
          "/control-plane",
          "/agents",
          "/approvals",
          "/sandbox",
          "/self-evolving",
          "/ar/control-room",
          "/_next/",
          "/api/",
          "/healthz",
        ],
      },
      // Block AI training crawlers
      {
        userAgent: "GPTBot",
        disallow: ["/"],
      },
      {
        userAgent: "CCBot",
        disallow: ["/"],
      },
      {
        userAgent: "anthropic-ai",
        disallow: ["/"],
      },
    ],
    sitemap: `${siteUrl}/sitemap.xml`,
    host: siteUrl,
  };
}
