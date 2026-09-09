import type { MetadataRoute } from "next";

export default function manifest(): MetadataRoute.Manifest {
  return {
    name: "Dealix — AI Business Operating System",
    short_name: "Dealix",
    description:
      "Dealix يربط إشارات الشركة بالقرار والتنفيذ والإثبات فوق أدواتها الحالية، مع حوكمة للأفعال الحساسة.",
    start_url: "/",
    scope: "/",
    display: "standalone",
    orientation: "portrait",
    background_color: "#F8FAFC",
    theme_color: "#0F172A",
    lang: "ar-SA",
    dir: "rtl",
    categories: ["business", "productivity"],
    icons: [
      {
        src: "/dealix-mark.svg",
        sizes: "64x64",
        type: "image/svg+xml",
        purpose: "any maskable",
      },
      {
        src: "/dealix-logo.svg",
        sizes: "400x96",
        type: "image/svg+xml",
        purpose: "any",
      },
    ],
    shortcuts: [
      {
        name: "التشخيص المجاني",
        url: "/book",
        description: "ابدأ بخريطة تنفيذ أولية مجانية.",
      },
      {
        name: "الخدمات",
        url: "/services",
        description: "استكشف مسارات التنفيذ المتاحة.",
      },
    ],
    prefer_related_applications: false,
  };
}
