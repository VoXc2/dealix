import { NextIntlClientProvider } from "next-intl";
import { getMessages } from "next-intl/server";
import { notFound } from "next/navigation";
import { ThemeProvider } from "next-themes";
import { HtmlLangDir } from "@/components/HtmlLangDir";
import { QueryProvider } from "@/components/providers/QueryProvider";
import { routing } from "@/i18n/routing";
import { AuthProvider } from "@/lib/hooks/useAuth";
import { Toaster } from "sonner";

interface LocaleLayoutProps {
  children: React.ReactNode;
  params: Promise<{ locale: string }>;
}

export default async function LocaleLayout({
  children,
  params,
}: LocaleLayoutProps) {
  const { locale } = await params;

  if (!routing.locales.includes(locale as "ar" | "en")) {
    notFound();
  }

  const messages = await getMessages();
  const isRTL = locale === "ar";

  return (
    <ThemeProvider
      attribute="class"
      defaultTheme="dark"
      enableSystem
      disableTransitionOnChange={false}
    >
      <NextIntlClientProvider messages={messages}>
        <HtmlLangDir />
        <QueryProvider>
          <AuthProvider>
            {children}
            <Toaster
            position={isRTL ? "bottom-left" : "bottom-right"}
            toastOptions={{
              style: {
                fontFamily: "var(--font-noto-arabic), sans-serif",
              },
            }}
            />
          </AuthProvider>
        </QueryProvider>
      </NextIntlClientProvider>
    </ThemeProvider>
  );
}
