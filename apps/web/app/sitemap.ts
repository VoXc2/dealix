import type { MetadataRoute } from "next";
import { sectorCatalog } from "@/lib/public-catalog";

const siteUrl = process.env.NEXT_PUBLIC_SITE_URL ?? "https://dealix.me";
const now = new Date();

export default function sitemap(): MetadataRoute.Sitemap {
  const pages: Array<{ path: string; priority: number; changeFrequency: "daily" | "weekly" | "monthly" }> = [
    { path: "", priority: 1.0, changeFrequency: "daily" },
    { path: "/company", priority: 0.95, changeFrequency: "weekly" },
    { path: "/services", priority: 0.98, changeFrequency: "weekly" },
    { path: "/sectors", priority: 0.98, changeFrequency: "weekly" },
    { path: "/products", priority: 0.94, changeFrequency: "weekly" },
    { path: "/dealix-os", priority: 0.95, changeFrequency: "weekly" },
    { path: "/book", priority: 0.98, changeFrequency: "weekly" },
    { path: "/saudi-opportunity-radar", priority: 0.9, changeFrequency: "weekly" },
    { path: "/safety", priority: 0.82, changeFrequency: "monthly" },
    { path: "/cases", priority: 0.68, changeFrequency: "weekly" },
    { path: "/pricing", priority: 0.7, changeFrequency: "monthly" },
  ];

  const staticPages = pages.map(({ path, priority, changeFrequency }) => ({
    url: `${siteUrl}${path}`,
    lastModified: now,
    changeFrequency,
    priority,
  }));

  const sectors = sectorCatalog.map((sector) => ({
    url: `${siteUrl}/sectors/${sector.slug}`,
    lastModified: now,
    changeFrequency: "weekly" as const,
    priority: 0.82,
  }));

  return [...staticPages, ...sectors];
}
