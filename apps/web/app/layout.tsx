import "./globals.css";
import "./interactive-home.css";
import type { Metadata, Viewport } from "next";
import type { ReactNode } from "react";
import { PostHogProviderWithInit } from "@/lib/analytics/posthog"; // posthog.tsx (JSX)

const siteUrl = process.env.NEXT_PUBLIC_SITE_URL ?? "https://dealix.me";

export const metadata: Metadata = {
  metadataBase: new URL(siteUrl),
  title: {
    default: "Dealix — AI Business Operating System",
    template: "%s | Dealix"
  },
  description:
    "Dealix يحوّل إشارات الشركة إلى تنفيذ محكوم ونتائج قابلة للقياس، مع ربط القرارات والإجراءات والأدلة فوق الأدوات التي تستخدمها الشركة بالفعل.",
  applicationName: "Dealix",
  keywords: [
    "Dealix", "AI Business Operating System", "Revenue + Proof + Command",
    "حوكمة الذكاء الاصطناعي", "تنفيذ الأعمال", "إثبات النتائج",
    "شركات سعودية", "B2B سعودي", "Saudi Arabia", "Saudi B2B",
    "Revenue Operations", "AI governance", "governed execution"
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
    title: "Dealix — AI Business Operating System",
    description:
      "Signals into Action. Execution with Governance. Measurable Outcomes.",
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
    title: "Dealix — AI Business Operating System",
    description:
      "Signals into Action. Execution with Governance. Measurable Outcomes.",
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
        <PostHogProviderWithInit>{children}</PostHogProviderWithInit>
      </body>
    </html>
  );
}
