import type { MetadataRoute } from "next";
import { LEARN_ARTICLES } from "@/content/learn/articles";

const BASE = process.env.NEXT_PUBLIC_SITE_URL || "https://dealix.me";

export default function sitemap(): MetadataRoute.Sitemap {
  const locales = ["ar", "en"] as const;

  const staticRoutes: { path: string; freq: MetadataRoute.Sitemap[number]["changeFrequency"]; priority: number }[] = [
    { path: "", freq: "weekly", priority: 1.0 },
    { path: "/dealix-diagnostic", freq: "weekly", priority: 0.95 },
    { path: "/services", freq: "monthly", priority: 0.9 },
    { path: "/risk-score", freq: "weekly", priority: 0.9 },
    { path: "/proof-pack", freq: "monthly", priority: 0.85 },
    { path: "/partners", freq: "monthly", priority: 0.8 },
    { path: "/learn", freq: "weekly", priority: 0.8 },
    { path: "/privacy", freq: "yearly", priority: 0.4 },
  ];

  const entries: MetadataRoute.Sitemap = [];

  for (const locale of locales) {
    for (const route of staticRoutes) {
      entries.push({
        url: `${BASE}/${locale}${route.path}`,
        changeFrequency: route.freq,
        priority: locale === "ar" ? route.priority : route.priority * 0.95,
        lastModified: new Date(),
      });
    }
    for (const article of LEARN_ARTICLES) {
      entries.push({
        url: `${BASE}/${locale}/learn/${article.slug}`,
        changeFrequency: "monthly",
        priority: locale === "ar" ? 0.75 : 0.70,
        lastModified: new Date(),
      });
    }
  }

  return entries;
}
