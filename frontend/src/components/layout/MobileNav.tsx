"use client";

import { usePathname } from "next/navigation";
import Link from "next/link";
import {
  LayoutDashboard,
  Target,
  Users,
  BarChart3,
  Settings,
  Bot,
  Shield,
  Handshake,
} from "lucide-react";
import { useLocale } from "next-intl";
import { cn } from "@/lib/utils";

const navItems = [
  {
    href: "/dashboard",
    icon: LayoutDashboard,
    label: "Dashboard",
    labelAr: "الرئيسية",
  },
  {
    href: "/pipeline",
    icon: Target,
    label: "Pipeline",
    labelAr: "المسار",
  },
  {
    href: "/clients",
    icon: Users,
    label: "Clients",
    labelAr: "العملاء",
  },
  {
    href: "/analytics",
    icon: BarChart3,
    label: "Analytics",
    labelAr: "التحليلات",
  },
  {
    href: "/agents",
    icon: Bot,
    label: "Agents",
    labelAr: "الوكلاء",
  },
  {
    href: "/settings",
    icon: Settings,
    label: "Settings",
    labelAr: "الإعدادات",
  },
];

export function MobileNav() {
  const pathname = usePathname();
  const locale = useLocale();
  const isRTL = locale === "ar";

  const isActive = (href: string) => {
    const path = pathname.replace(`/${locale}`, "") || "/";
    return path.startsWith(href);
  };

  return (
    <nav className="fixed bottom-0 left-0 right-0 z-50 border-t border-border bg-background/95 backdrop-blur-lg md:hidden safe-area-bottom">
      <div className="flex items-center justify-around h-16 px-2">
        {navItems.map((item) => {
          const Icon = item.icon;
          const active = isActive(item.href);
          return (
            <Link
              key={item.href}
              href={`/${locale}${item.href}`}
              className={cn(
                "flex flex-col items-center justify-center gap-0.5 rounded-xl px-3 py-1.5 transition-colors min-w-[56px]",
                active
                  ? "text-gold-500"
                  : "text-muted-foreground hover:text-foreground",
              )}
            >
              <Icon className="w-5 h-5" />
              <span className="text-[10px] font-medium leading-tight">
                {isRTL ? item.labelAr : item.label}
              </span>
              {active && (
                <div className="absolute -top-0.5 left-1/2 -translate-x-1/2 h-0.5 w-8 rounded-full bg-gold-500" />
              )}
            </Link>
          );
        })}
      </div>
    </nav>
  );
}
