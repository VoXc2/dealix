import type { Metadata } from "next";
import { Noto_Sans_Arabic } from "next/font/google";
import "./globals.css";

const notoArabic = Noto_Sans_Arabic({
  subsets: ["arabic"],
  variable: "--font-arabic",
  weight: ["300", "400", "500", "600", "700", "800"],
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
  return (
    <html suppressHydrationWarning>
      <head>
        <link
          href="https://fonts.googleapis.com/css2?family=Noto+Sans+Arabic:wght@300;400;500;600;700;800&family=IBM+Plex+Arabic:wght@300;400;500;600;700&display=swap"
          rel="stylesheet"
        />
      </head>
      <body className={`${notoArabic.variable} antialiased`}>{children}</body>
    </html>
  );
}
