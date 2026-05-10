import type { Metadata } from "next";
import {
  IBM_Plex_Sans_Arabic,
  JetBrains_Mono,
  Noto_Sans_Arabic,
  Syne,
} from "next/font/google";
import "./globals.css";

const notoArabic = Noto_Sans_Arabic({
  subsets: ["arabic"],
  variable: "--font-noto-arabic",
  weight: ["300", "400", "500", "600", "700", "800"],
  display: "swap",
});

const ibmPlexArabic = IBM_Plex_Sans_Arabic({
  subsets: ["arabic"],
  variable: "--font-ibm-plex-arabic",
  weight: ["300", "400", "500", "600", "700"],
  display: "swap",
});

const syne = Syne({
  subsets: ["latin"],
  variable: "--font-syne",
  weight: ["400", "500", "600", "700", "800"],
  display: "swap",
});

const jetbrainsMono = JetBrains_Mono({
  subsets: ["latin"],
  variable: "--font-jetbrains-mono",
  weight: ["400", "500"],
  display: "swap",
});

export const metadata: Metadata = {
  title: {
    default: "Dealix - منصة الذكاء الاصطناعي للإيرادات",
    template: "%s | Dealix",
  },
  description: "AI-powered RevOps platform for Saudi enterprise clients",
  keywords: ["RevOps", "AI", "Saudi Arabia", "CRM", "Revenue", "Dealix"],
  icons: {
    icon: "/favicon.ico",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const fontVars = [
    notoArabic.variable,
    ibmPlexArabic.variable,
    syne.variable,
    jetbrainsMono.variable,
  ].join(" ");

  return (
    <html lang="ar" dir="rtl" suppressHydrationWarning>
      <body className={`${fontVars} antialiased`}>{children}</body>
    </html>
  );
}
