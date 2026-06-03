"use client";
import { useLocale } from "next-intl";
import { usePathname } from "next/navigation";
import { Button } from "@/components/ui/button";

export function LocaleToggle() {
  const locale = useLocale();
  const pathname = usePathname();
  const next = locale === "ar" ? "en" : "ar";
  return (
    <Button type="button" variant="ghost" size="sm" onClick={() => {
      const s = pathname.split("/"); s[1] = next; window.location.href = s.join("/") || `/${next}`;
    }}>{locale === "ar" ? "EN" : "عربي"}</Button>
  );
}
