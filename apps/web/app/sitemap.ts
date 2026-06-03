import type { MetadataRoute } from "next";

const siteUrl = process.env.NEXT_PUBLIC_SITE_URL ?? "https://dealix.me";
const now = new Date();

export default function sitemap(): MetadataRoute.Sitemap {
  const pages: Array<{
    path: string;
    priority: number;
    changeFrequency: "always" | "hourly" | "daily" | "weekly" | "monthly" | "yearly" | "never";
  }> = [
    // ── English / Internal ──────────────────────────────────────────
    { path: "",                priority: 1.0,  changeFrequency: "daily"   },
    { path: "/status",         priority: 0.8,  changeFrequency: "daily"   },
    { path: "/control-plane",  priority: 0.6,  changeFrequency: "weekly"  },
    { path: "/agents",         priority: 0.6,  changeFrequency: "weekly"  },
    { path: "/approvals",      priority: 0.6,  changeFrequency: "weekly"  },
    { path: "/safety",         priority: 0.7,  changeFrequency: "weekly"  },
    { path: "/sandbox",        priority: 0.5,  changeFrequency: "weekly"  },
    { path: "/value-engine",   priority: 0.7,  changeFrequency: "weekly"  },
    { path: "/self-evolving",  priority: 0.6,  changeFrequency: "weekly"  },
    { path: "/revenue-os",     priority: 0.7,  changeFrequency: "weekly"  },
    { path: "/go-to-market",   priority: 0.6,  changeFrequency: "weekly"  },
    { path: "/product-network",priority: 0.6,  changeFrequency: "weekly"  },

    // ── Arabic — Main ───────────────────────────────────────────────
    { path: "/ar",                        priority: 0.95, changeFrequency: "daily"  },
    { path: "/ar/pricing",                priority: 0.90, changeFrequency: "weekly" },
    { path: "/ar/demo",                   priority: 0.85, changeFrequency: "weekly" },

    // ── Arabic — Products ───────────────────────────────────────────
    { path: "/ar/p1",                     priority: 0.90, changeFrequency: "weekly" },
    { path: "/ar/p2",                     priority: 0.88, changeFrequency: "weekly" },
    { path: "/ar/p3",                     priority: 0.85, changeFrequency: "weekly" },

    // ── Arabic — Trust & Compliance ─────────────────────────────────
    { path: "/ar/zatca-readiness",        priority: 0.80, changeFrequency: "weekly" },
    { path: "/ar/control-room",           priority: 0.70, changeFrequency: "weekly" },
  ];

  return pages.map(({ path, priority, changeFrequency }) => ({
    url: `${siteUrl}${path}`,
    lastModified: now,
    changeFrequency,
    priority,
    alternates: path.startsWith("/ar")
      ? { languages: { "ar-SA": `${siteUrl}${path}` } }
      : { languages: { "ar-SA": `${siteUrl}/ar`, "en-US": `${siteUrl}${path}` } },
  }));
}
