"use client";

import { useState } from "react";
import { useLocale } from "next-intl";
import { Sidebar } from "./Sidebar";
import { Header } from "./Header";

interface AppLayoutProps {
  children: React.ReactNode;
  title?: string;
  subtitle?: string;
}

export function AppLayout({ children, title, subtitle }: AppLayoutProps) {
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const locale = useLocale();
  const isRTL = locale === "ar";
  const sidebarWidth = sidebarCollapsed ? 72 : 260;

  return (
    <div className="min-h-screen bg-background grid-pattern">
      <Sidebar
        collapsed={sidebarCollapsed}
        onToggle={() => setSidebarCollapsed(!sidebarCollapsed)}
      />
      <main
        className="min-h-screen flex flex-col transition-all duration-200"
        style={{
          [isRTL ? "marginRight" : "marginLeft"]: sidebarWidth,
        }}
      >
        <Header title={title} subtitle={subtitle} />
        <div className="flex-1 p-6">
          {children}
        </div>
      </main>
    </div>
  );
}
