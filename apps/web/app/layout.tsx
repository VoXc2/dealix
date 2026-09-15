import "./globals.css";
import "./interactive-home.css";
import "./corporate-pages.css";
import type { Metadata, Viewport } from "next";
import type { ReactNode } from "react";
import { PostHogProviderWithInit } from "@/lib/analytics/posthog"; // posthog.tsx (JSX)
import TopInfoBar from "@/components/TopInfoBar";

const siteUrl = process.env.NEXT_PUBLIC_SITE_URL ?? "https://dealix.me";

export const metadata: Metadata = {
  metadataBase: new URL(siteUrl),
  title: {
    default: "Dealix — AI Business Operating System | Strategy, Systems & Proof",
    template: "%s | Dealix"
  },
  description:
    "Dealix شركة B2B سعودية للاستراتيجية والأنظمة والذكاء والمنتجات. نحول إشارات الأعمال إلى تنفيذ محكوم ونتائج قابلة للقياس، وDealix OS هو منتجنا الرئيسي للـAI Business Operating System.",
  applicationName: "Dealix",
  keywords: [
    "Dealix", "Saudi B2B", "B2B Strategy", "AI Systems", "Business Automation",
    "Saudi Market Intelligence", "Governed AI Execution", "AI Business Operating System",
    "Dealix OS", "Revenue Operations", "AI governance", "Operational Proof",
    "شركات سعودية", "استراتيجية الأعمال", "أتمتة الأعمال", "حوكمة الذكاء الاصطناعي"
  ],
  authors: [{ name: "Dealix", url: siteUrl }],
  creator: "Dealix",
  publisher: "Dealix",
  alternates: {
    canonical: "/",
  },
  openGraph: {
    type: "website",
    locale: "ar_SA",
    url: siteUrl,
    siteName: "Dealix",
    title: "Dealix — AI Business Operating System | Strategy, Systems & Proof",
    description:
      "Saudi B2B strategy and systems company. From business signal to governed execution and measurable proof.",
    images: [
      {
        url: `${siteUrl}/dealix-og.svg`,
        width: 1200,
        height: 630,
        alt: "Dealix — AI Business Operating System",
      }
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "Dealix — AI Business Operating System | Strategy, Systems & Proof",
    description:
      "Saudi B2B strategy and systems company. Dealix OS is the flagship AI Business Operating System.",
    images: [`${siteUrl}/dealix-og.svg`],
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      "max-snippet": -1,
      "max-image-preview": "large",
      "max-video-preview": -1,
    },
  },
  verification: {
    google: process.env.GOOGLE_SITE_VERIFICATION ?? "",
  },
  category: "business",
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  maximumScale: 5,
  themeColor: [
    { media: "(prefers-color-scheme: dark)", color: "#0F172A" },
    { media: "(prefers-color-scheme: light)", color: "#F8FAFC" },
  ],
  colorScheme: "light dark",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="ar" dir="rtl">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="" />
        <link
          href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;500;600;700&display=swap"
          rel="stylesheet"
        />
      </head>
      <body>
        <a
          href="#main-content"
          className="sr-only focus:not-sr-only focus:absolute focus:top-2 focus:z-[100] focus:px-4 focus:py-2 focus:bg-[#001F3F] focus:text-white focus:rounded-lg focus:right-4"
        >
          تخطي إلى المحتوى · Skip to content
        </a>
        <TopInfoBar />
        <PostHogProviderWithInit>{children}</PostHogProviderWithInit>
      </body>
    </html>
  );
}