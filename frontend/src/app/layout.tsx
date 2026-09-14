import type { Metadata } from "next";
import { Noto_Sans_Arabic, IBM_Plex_Sans_Arabic } from "next/font/google";
import "./globals.css";
import "@/styles/dealix-system.css";

const notoArabic = Noto_Sans_Arabic({
  subsets: ["arabic"],
  variable: "--font-arabic",
  weight: ["300", "400", "500", "600", "700", "800"],
  display: "swap",
});

const ibmArabic = IBM_Plex_Sans_Arabic({
  subsets: ["arabic"],
  variable: "--font-ibm-arabic",
  weight: ["300", "400", "500", "600", "700"],
  display: "swap",
});

export const metadata: Metadata = {
  metadataBase: new URL(process.env.NEXT_PUBLIC_SITE_URL || "https://dealix.me"),
  title: {
    default: "Dealix - منصة الذكاء الاصطناعي للإيرادات",
    template: "%s | Dealix",
  },
  description: "AI-powered RevOps platform for Saudi enterprise clients",
  keywords: ["RevOps", "AI", "Saudi Arabia", "CRM", "Revenue", "Dealix"],
  icons: {
    icon: "/brand/logo-mark.svg",
    apple: "/brand/logo-mark.svg",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html suppressHydrationWarning>
      <body className={`${notoArabic.variable} ${ibmArabic.variable} antialiased`}>{children}</body>
    </html>
  );
}
