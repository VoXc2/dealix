import type { MetadataRoute } from "next";

const siteUrl = process.env.NEXT_PUBLIC_SITE_URL ?? "https://dealix.me";

const publicRoutes = [
  "/", "/company", "/services", "/sectors", "/products", "/dealix-os", "/book",
  "/saudi-opportunity-radar", "/safety", "/cases", "/pricing", "/client-portal/demo",
];

const privateRoutes = [
  "/crm", "/operator", "/review-queue", "/outreach-lab", "/followups",
  "/command-center", "/war-room", "/pipeline", "/kpi-finance", "/deals",
  "/proof-vault", "/launch", "/approvals", "/founder", "/control-plane",
  "/dashboard", "/data-room", "/delivery-workspace", "/client-success", "/retention",
  "/growth", "/growth-command-center", "/commercial-intelligence", "/evidence", "/go-to-market", "/control-room",
  "/lead-engine", "/hubspot-os", "/automated-sales",
  "/persuasion-room", "/product-network", "/quotes", "/revenue", "/revenue-machine",
  "/sales-agent", "/sales-agent-lab", "/sales-assets", "/sales-machine", "/settings",
  "/client-portal", "/daily-draft", "/sandbox", "/self-evolving",
  "/app", "/cmd-v2", "/dx3", "/iv4", "/rcmax", "/s9", "/t10", "/x5", "/z8", "/a14",
  "/api/", "/healthz",
];

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      { userAgent: "*", allow: publicRoutes, disallow: privateRoutes },
      { userAgent: "OAI-SearchBot", allow: publicRoutes, disallow: privateRoutes },
      { userAgent: "GPTBot", disallow: ["/"] },
      { userAgent: "CCBot", disallow: ["/"] },
      { userAgent: "anthropic-ai", disallow: ["/"] },
    ],
    sitemap: `${siteUrl}/sitemap.xml`,
    host: siteUrl,
  };
}
