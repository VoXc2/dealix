"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useTranslations, useLocale } from "next-intl";
import { motion, AnimatePresence } from "framer-motion";
import {
  LayoutDashboard,
  GitBranch,
  Bot,
  CheckSquare,
  Users,
  BarChart3,
  Settings,
  ChevronLeft,
  ChevronRight,
  Zap,
  Shield,
  Building2,
  Cloud,
  Briefcase,
  Sparkles,
  ClipboardList,
  Layers,
  FileText,
  Megaphone,
  Cpu,
  BrainCircuit,
  ShieldCheck,
  CreditCard,
  UserCog,
  Contact2,
} from "lucide-react";
import { cn } from "@/lib/utils";
import { useState } from "react";

interface NavItem {
  key: string;
  href: string;
  icon: React.ComponentType<{ className?: string }>;
}

interface NavGroup {
  groupKey: string;
  groupLabelAr: string;
  groupLabelEn: string;
  items: NavItem[];
}

const navGroups: NavGroup[] = [
  {
    groupKey: "main",
    groupLabelAr: "الرئيسية",
    groupLabelEn: "Main",
    items: [
      { key: "dashboard", href: "/dashboard", icon: LayoutDashboard },
      { key: "aiEngine", href: "/ai-engine", icon: BrainCircuit },
      { key: "analytics", href: "/analytics", icon: BarChart3 },
    ],
  },
  {
    groupKey: "commercial",
    groupLabelAr: "التجاري",
    groupLabelEn: "Commercial",
    items: [
      { key: "crm", href: "/crm", icon: Contact2 },
      { key: "pipeline", href: "/pipeline", icon: GitBranch },
      { key: "clients", href: "/clients", icon: Users },
      { key: "customerPortal", href: "/customer-portal", icon: Building2 },
      { key: "pricing", href: "/pricing", icon: CreditCard },
    ],
  },
  {
    groupKey: "operations",
    groupLabelAr: "العمليات",
    groupLabelEn: "Operations",
    items: [
      { key: "businessNow", href: "/business-now", icon: Briefcase },
      { key: "opsHub", href: "/ops", icon: Layers },
      { key: "opsWarRoom", href: "/ops/war-room", icon: Briefcase },
      { key: "opsSales", href: "/ops/sales", icon: Layers },
      { key: "opsMarketing", href: "/ops/marketing", icon: Megaphone },
      { key: "approvals", href: "/approvals", icon: CheckSquare },
      { key: "agents", href: "/agents", icon: Bot },
    ],
  },
  {
    groupKey: "compliance",
    groupLabelAr: "الامتثال والأمان",
    groupLabelEn: "Compliance",
    items: [
      { key: "trustCenter", href: "/trust-center", icon: ShieldCheck },
      { key: "zatcaReadiness", href: "/zatca-readiness", icon: Shield },
      { key: "trustCheck", href: "/trust-check", icon: Shield },
      { key: "dealixDiagnostic", href: "/dealix-diagnostic", icon: Sparkles },
    ],
  },
  {
    groupKey: "admin",
    groupLabelAr: "الإدارة",
    groupLabelEn: "Admin",
    items: [
      { key: "adminConsole", href: "/admin", icon: UserCog },
      { key: "settings", href: "/settings", icon: Settings },
    ],
  },
];

interface SidebarProps {
  collapsed?: boolean;
  onToggle?: () => void;
}

export function Sidebar({ collapsed = false, onToggle }: SidebarProps) {
  const t = useTranslations("nav");
  const locale = useLocale();
  const pathname = usePathname();
  const isRTL = locale === "ar";

  return (
    <motion.aside
      animate={{ width: collapsed ? 72 : 260 }}
      transition={{ duration: 0.2, ease: "easeInOut" }}
      className={cn(
        "fixed top-0 h-screen z-40 flex flex-col",
        "bg-sidebar border-border/50",
        isRTL ? "right-0 border-l" : "left-0 border-r"
      )}
    >
      {/* Logo area */}
      <div className="flex items-center h-16 px-4 border-b border-sidebar-border">
        <div className="flex items-center gap-3 flex-1 min-w-0">
          <div className="flex-shrink-0 w-9 h-9 rounded-xl bg-gradient-to-br from-gold-400 to-gold-600 flex items-center justify-center shadow-lg">
            <Zap className="w-5 h-5 text-white" strokeWidth={2.5} />
          </div>
          <AnimatePresence>
            {!collapsed && (
              <motion.div
                initial={{ opacity: 0, x: isRTL ? 10 : -10 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: isRTL ? 10 : -10 }}
                transition={{ duration: 0.15 }}
                className="overflow-hidden"
              >
                <span className="text-sidebar-foreground font-display font-bold text-lg tracking-tight whitespace-nowrap">
                  Dealix
                </span>
                <p className="text-gold-500 text-[10px] font-medium tracking-widest uppercase mt-0.5 whitespace-nowrap">
                  AI RevOps
                </p>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
        <button
          onClick={onToggle}
          className="flex-shrink-0 w-7 h-7 rounded-lg flex items-center justify-center text-sidebar-foreground/50 hover:text-sidebar-foreground hover:bg-sidebar-accent transition-colors"
        >
          {isRTL
            ? collapsed
              ? <ChevronLeft className="w-4 h-4" />
              : <ChevronRight className="w-4 h-4" />
            : collapsed
            ? <ChevronRight className="w-4 h-4" />
            : <ChevronLeft className="w-4 h-4" />
          }
        </button>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-3 py-4 overflow-y-auto overflow-x-hidden space-y-4">
        {navGroups.map((group) => (
          <div key={group.groupKey}>
            <AnimatePresence>
              {!collapsed && (
                <motion.p
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 0.4 }}
                  exit={{ opacity: 0 }}
                  className="text-sidebar-foreground text-[10px] font-semibold uppercase tracking-widest px-3 mb-1"
                >
                  {isRTL ? group.groupLabelAr : group.groupLabelEn}
                </motion.p>
              )}
            </AnimatePresence>
            <div className="space-y-0.5">
              {group.items.map((item) => {
                const Icon = item.icon;
                const href = `/${locale}${item.href}`;
                const isActive = pathname === href || pathname.startsWith(`${href}/`);

                return (
                  <Link key={item.key} href={href}>
                    <motion.div
                      whileHover={{ x: isRTL ? -2 : 2 }}
                      className={cn(
                        "flex items-center gap-3 px-3 py-2.5 rounded-xl transition-all duration-150 group relative",
                        isActive
                          ? "bg-sidebar-primary/15 text-gold-400"
                          : "text-sidebar-foreground/60 hover:text-sidebar-foreground hover:bg-sidebar-accent"
                      )}
                    >
                      {isActive && (
                        <motion.div
                          layoutId="activeIndicator"
                          className={cn(
                            "absolute top-1/2 -translate-y-1/2 w-0.5 h-6 rounded-full bg-gold-400",
                            isRTL ? "right-0" : "left-0"
                          )}
                        />
                      )}
                      <Icon className={cn("flex-shrink-0 w-4 h-4", isActive && "text-gold-400")} />
                      <AnimatePresence>
                        {!collapsed && (
                          <motion.span
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            exit={{ opacity: 0 }}
                            className={cn(
                              "text-sm font-medium whitespace-nowrap",
                              isActive ? "text-gold-400" : ""
                            )}
                          >
                            {t(item.key as Parameters<typeof t>[0])}
                          </motion.span>
                        )}
                      </AnimatePresence>
                    </motion.div>
                  </Link>
                );
              })}
            </div>
          </div>
        ))}
      </nav>

      {/* Bottom section - version */}
      <div className="px-4 py-3 border-t border-sidebar-border">
        <AnimatePresence>
          {!collapsed && (
            <motion.p
              initial={{ opacity: 0 }}
              animate={{ opacity: 0.4 }}
              exit={{ opacity: 0 }}
              className="text-sidebar-foreground text-[10px] text-center"
            >
              Dealix v3.0 — AI RevOps Platform
            </motion.p>
          )}
        </AnimatePresence>
      </div>
    </motion.aside>
  );
}
