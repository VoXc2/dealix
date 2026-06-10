import type { MetadataRoute } from "next";

const siteUrl = process.env.NEXT_PUBLIC_SITE_URL ?? "https://dealix.me";

export default function manifest(): MetadataRoute.Manifest {
  return {
    name: "Dealix — نظام إيراد AI للشركات السعودية",
    short_name: "Dealix",
    description:
      "Dealix يحوّل بيانات المبيعات والمتابعات إلى Revenue OS عملي. AI يكتب، أنت ترسل.",
    start_url: "/ar",
    scope: "/",
    display: "standalone",
    orientation: "portrait",
    background_color: "#001228",
    theme_color: "#001F3F",
    lang: "ar-SA",
    dir: "rtl",
    categories: ["business", "productivity", "finance"],
    icons: [
      { src: "/icon-192.png",  sizes: "192x192",  type: "image/png", purpose: "maskable" },
      { src: "/icon-512.png",  sizes: "512x512",  type: "image/png", purpose: "any"      },
      { src: "/favicon.ico",   sizes: "any",       type: "image/x-icon"                   },
    ],
    screenshots: [
      {
        src: `${siteUrl}/screenshot-wide.png`,
        sizes: "1280x720",
        type: "image/png",
        form_factor: "wide",
        label: "Dealix Revenue OS Dashboard",
      },
      {
        src: `${siteUrl}/screenshot-mobile.png`,
        sizes: "390x844",
        type: "image/png",
        form_factor: "narrow",
        label: "Dealix على الجوال",
      },
    ],
    shortcuts: [
      {
        name: "P1 — تشخيص الإيراد",
        url: "/ar/p1",
        description: "ابدأ تشخيص Revenue Intelligence Sprint",
      },
      {
        name: "الأسعار",
        url: "/ar/pricing",
        description: "عرض خيارات الباقات والأسعار",
      },
    ],
    prefer_related_applications: false,
  };
}
