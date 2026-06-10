"use client";

import { useTranslations, useLocale } from "next-intl";
import { useTheme } from "next-themes";
import { useRouter, usePathname } from "next/navigation";
import { Sun, Moon, Bell, Search, LogOut, User, Globe } from "lucide-react";
import { cn } from "@/lib/utils";
import { useAuth } from "@/lib/hooks/useAuth";
import { useState } from "react";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

interface HeaderProps {
  title?: string;
  subtitle?: string;
}

export function Header({ title, subtitle }: HeaderProps) {
  const t = useTranslations();
  const locale = useLocale();
  const { theme, setTheme } = useTheme();
  const { user, logout } = useAuth();
  const router = useRouter();
  const pathname = usePathname();
  const [searchOpen, setSearchOpen] = useState(false);

  const isRTL = locale === "ar";

  const switchLocale = () => {
    const newLocale = locale === "ar" ? "en" : "ar";
    // Replace locale segment in current path
    const segments = pathname.split("/");
    segments[1] = newLocale;
    router.push(segments.join("/"));
  };

  const handleLogout = async () => {
    await logout();
    router.push(`/${locale}/login`);
  };

  return (
    <header className="h-16 flex items-center px-6 border-b border-border/50 bg-background/95 backdrop-blur-sm sticky top-0 z-30">
      {/* Title */}
      <div className="flex-1 min-w-0">
        {title && (
          <h1 className="text-lg font-bold text-foreground truncate">{title}</h1>
        )}
        {subtitle && (
          <p className="text-xs text-muted-foreground mt-0.5 hidden sm:block">{subtitle}</p>
        )}
      </div>

      {/* Actions */}
      <div className={cn("flex items-center gap-2", isRTL ? "flex-row-reverse" : "")}>
        {/* Search */}
        <button
          onClick={() => setSearchOpen(!searchOpen)}
          className="w-9 h-9 rounded-xl flex items-center justify-center text-muted-foreground hover:text-foreground hover:bg-muted transition-colors"
          aria-label="Search"
        >
          <Search className="w-4 h-4" />
        </button>

        {/* Notifications */}
        <button className="relative w-9 h-9 rounded-xl flex items-center justify-center text-muted-foreground hover:text-foreground hover:bg-muted transition-colors">
          <Bell className="w-4 h-4" />
          <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-gold-400 rounded-full ring-2 ring-background" />
        </button>

        {/* Language Toggle */}
        <button
          onClick={switchLocale}
          className="flex items-center gap-1.5 h-9 px-3 rounded-xl text-muted-foreground hover:text-foreground hover:bg-muted transition-colors text-sm font-medium"
        >
          <Globe className="w-3.5 h-3.5" />
          <span>{locale === "ar" ? "EN" : "عربي"}</span>
        </button>

        {/* Theme Toggle */}
        <button
          onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
          className="w-9 h-9 rounded-xl flex items-center justify-center text-muted-foreground hover:text-foreground hover:bg-muted transition-colors"
        >
          {theme === "dark" ? (
            <Sun className="w-4 h-4" />
          ) : (
            <Moon className="w-4 h-4" />
          )}
        </button>

        {/* User Menu */}
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <button className="flex items-center gap-2 h-9 px-2 rounded-xl hover:bg-muted transition-colors">
              <div className="w-7 h-7 rounded-full bg-gradient-to-br from-gold-400 to-emerald-600 flex items-center justify-center text-white text-xs font-bold">
                {user?.fullName?.[0] ?? "D"}
              </div>
              <div className="hidden md:block text-start">
                <p className="text-sm font-medium leading-none">{user?.fullName ?? "Dealix User"}</p>
                <p className="text-xs text-muted-foreground mt-0.5">{user?.company ?? "Enterprise"}</p>
              </div>
            </button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align={isRTL ? "start" : "end"} className="w-52">
            <DropdownMenuItem>
              <User className="w-4 h-4 me-2" />
              {t("settings.profile")}
            </DropdownMenuItem>
            <DropdownMenuSeparator />
            <DropdownMenuItem
              className="text-destructive focus:text-destructive"
              onClick={handleLogout}
            >
              <LogOut className="w-4 h-4 me-2" />
              {t("nav.logout")}
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>
    </header>
  );
}
