"use client";

import { useLocale } from "next-intl";
import { useEffect } from "react";

/**
 * Syncs <html lang/dir> with the active next-intl locale.
 * Root layout owns a single <html>; locale lives under [locale] without nesting html/body.
 */
export function HtmlLangDir() {
  const locale = useLocale();

  useEffect(() => {
    document.documentElement.lang = locale;
    document.documentElement.dir = locale === "ar" ? "rtl" : "ltr";
  }, [locale]);

  return null;
}
