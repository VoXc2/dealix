import { useEffect, type ReactNode } from "react";
import { useLocation } from "react-router";
import SiteNav from "./SiteNav";
import SiteFooter from "./SiteFooter";

interface SiteLayoutProps {
  children: ReactNode;
}

/** Shared marketing shell: RTL, sticky nav, footer, and scroll-to-top on route change. */
export default function SiteLayout({ children }: SiteLayoutProps) {
  const { pathname } = useLocation();

  useEffect(() => {
    window.scrollTo(0, 0);
  }, [pathname]);

  return (
    <div className="min-h-screen bg-white flex flex-col" dir="rtl">
      <SiteNav />
      <main className="flex-1">{children}</main>
      <SiteFooter />
    </div>
  );
}
