import "./globals.css";
import type { Metadata, Viewport } from "next";
import type { ReactNode } from "react";

const siteUrl = process.env.NEXT_PUBLIC_SITE_URL ?? "https://dealix.me";

export const metadata: Metadata = {
  metadataBase: new URL(siteUrl),
  title: {
    default: "Dealix — نظام إيراد AI للشركات السعودية",
    template: "%s | Dealix"
  },
  description:
    "Dealix يحوّل بيانات المبيعات والمتابعات إلى Revenue OS عملي خلال أسبوع واحد. تشخيص مدفوع، تشغيل شهري، غرفة قيادة تنفيذية للشركات B2B السعودية.",
  applicationName: "Dealix",
  keywords: [
    "Dealix", "Revenue OS", "نظام إيراد", "شركات سعودية",
    "B2B سعودي", "AI مبيعات", "PDPL", "ZATCA",
    "متابعة عملاء", "تشغيل مبيعات", "Saudi Arabia",
    "Saudi B2B", "AI revenue engine", "sales automation"
  ],
  authors: [{ name: "Dealix", url: siteUrl }],
  creator: "Dealix",
  publisher: "Dealix",
  alternates: {
    canonical: "/",
    languages: {
      "ar-SA": "/ar",
      "en-US": "/",
    },
  },
  openGraph: {
    type: "website",
    locale: "ar_SA",
    alternateLocale: ["en_US"],
    url: siteUrl,
    siteName: "Dealix",
    title: "Dealix — نظام إيراد AI للشركات السعودية",
    description:
      "Dealix يحوّل بيانات المبيعات إلى Revenue OS خلال أسبوع واحد. تشغيل مدفوع، Proof Pack، حوكمة AI.",
    images: [
      {
        url: `${siteUrl}/og-image.png`,
        width: 1200,
        height: 630,
        alt: "Dealix — Revenue OS للشركات السعودية",
      }
    ],
  },
  twitter: {
    card: "summary_large_image",
    site: "@dealixsa",
    creator: "@dealixsa",
    title: "Dealix — نظام إيراد AI للشركات السعودية",
    description:
      "Dealix يحوّل بيانات المبيعات إلى Revenue OS خلال أسبوع. AI يكتب، أنت ترسل.",
    images: [`${siteUrl}/og-image.png`],
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
    { media: "(prefers-color-scheme: dark)",  color: "#001F3F" },
    { media: "(prefers-color-scheme: light)", color: "#001F3F" },
  ],
  colorScheme: "dark",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="ar" dir="rtl">
      <head>
        {/* Preconnect to Google Fonts for performance */}
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="" />
      </head>
      <body>{children}</body>
    </html>
  );
}
