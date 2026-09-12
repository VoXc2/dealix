import type { MetadataRoute } from "next";

const siteUrl = process.env.NEXT_PUBLIC_SITE_URL ?? "https://dealix.me";
const now = new Date();

export default function sitemap(): MetadataRoute.Sitemap {
  const pages: Array<{ path: string; priority: number; changeFrequency: "daily" | "weekly" | "monthly" }> = [
    { path: "", priority: 1.0, changeFrequency: "daily" },
    { path: "/company", priority: 0.95, changeFrequency: "weekly" },
    { path: "/services", priority: 0.95, changeFrequency: "weekly" },
    { path: "/dealix-os", priority: 0.95, changeFrequency: "weekly" },
    { path: "/book", priority: 0.95, changeFrequency: "weekly" },
    { path: "/saudi-opportunity-radar", priority: 0.9, changeFrequency: "weekly" },
    { path: "/proof-vault", priority: 0.85, changeFrequency: "weekly" },
    { path: "/safety", priority: 0.8, changeFrequency: "monthly" },
    { path: "/cases", priority: 0.7, changeFrequency: "weekly" },
    { path: "/pricing", priority: 0.65, changeFrequency: "monthly" },
  ];
  return pages.map(({ path, priority, changeFrequency }) => ({ url: `${siteUrl}${path}`, lastModified: now, changeFrequency, priority }));
}
