"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { Check, Rocket, Settings, Users, ArrowRight, Sparkles } from "lucide-react";
import { useLocale } from "next-intl";
import { useRouter } from "next/navigation";
import type { Route } from "next";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";

interface QuickAction {
  id: string;
  icon: React.ElementType;
  label: string;
  labelAr: string;
  description: string;
  descriptionAr: string;
  href: Route<string>;
}

const quickActions: QuickAction[] = [
  {
    id: "dashboard",
    icon: Rocket,
    label: "Go to Dashboard",
    labelAr: "اذهب إلى لوحة التحكم",
    description: "Start exploring your new workspace",
    descriptionAr: "ابدأ في استكشاف مساحة عملك الجديدة",
    href: "/dashboard",
  },
  {
    id: "pipeline",
    icon: Users,
    label: "Set Up Pipeline",
    labelAr: "إعداد مسار الصفقات",
    description: "Configure your deal stages",
    descriptionAr: "تكوين مراحل صفقاتك",
    href: "/pipeline",
  },
  {
    id: "settings",
    icon: Settings,
    label: "Configure Settings",
    labelAr: "تكوين الإعدادات",
    description: "Customize your experience",
    descriptionAr: "تخصيص تجربتك",
    href: "/settings",
  },
];

interface PostPurchaseProps {
  planName: string;
  planNameAr: string;
  onStartOnboarding?: () => void;
}

export function PostPurchase({ planName, planNameAr, onStartOnboarding }: PostPurchaseProps) {
  const [showDetails, setShowDetails] = useState(false);
  const locale = "ar";
  const isRTL = locale === "ar";
  const router = useRouter();

  return (
    <div className="mx-auto max-w-lg text-center">
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
      >
        {/* Success animation */}
        <div className="relative mx-auto mb-6 flex h-20 w-20 items-center justify-center">
          <div className="absolute inset-0 rounded-full bg-emerald-500/20 animate-ping" />
          <div className="relative flex h-20 w-20 items-center justify-center rounded-full bg-emerald-500/10 border-2 border-emerald-500/30">
            <Check className="w-10 h-10 text-emerald-500" />
          </div>
        </div>

        <h2 className="text-2xl font-bold text-foreground mb-2">
          {isRTL ? `اشتراك ${planNameAr} نشط!` : `${planName} Subscription Active!`}
        </h2>
        <p className="text-sm text-muted-foreground mb-8">
          {isRTL
            ? "تم تفعيل اشتراكك. يمكنك الآن الاستفادة من جميع ميزات ديليكس."
            : "Your subscription is now active. Enjoy all Dealix features."}
        </p>

        {/* Quick actions */}
        <div className="grid gap-3 mb-8">
          {quickActions.map((action, idx) => {
            const Icon = action.icon;
            return (
              <motion.div
                key={action.id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 + idx * 0.1 }}
              >
                <button
                  onClick={() => router.push(action.href)}
                  className="flex w-full items-center gap-4 rounded-xl border border-border bg-card p-4 text-left hover:bg-accent/50 hover:border-gold-500/30 transition-all group"
                >
                  <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-gold-500/10">
                    <Icon className="w-5 h-5 text-gold-500" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-semibold text-foreground">
                      {isRTL ? action.labelAr : action.label}
                    </p>
                    <p className="text-xs text-muted-foreground">
                      {isRTL ? action.descriptionAr : action.description}
                    </p>
                  </div>
                  <ArrowRight className={cn("w-4 h-4 text-muted-foreground group-hover:text-foreground transition-colors", isRTL && "rotate-180")} />
                </button>
              </motion.div>
            );
          })}
        </div>

        {/* Onboarding prompt */}
        {onStartOnboarding && (
          <Card className="bg-gradient-to-br from-gold-500/5 to-transparent border-gold-500/20 mb-4">
            <CardContent className="p-5">
              <div className="flex items-start gap-3">
                <Sparkles className="w-5 h-5 text-gold-500 shrink-0 mt-0.5" />
                <div className="text-left">
                  <p className="text-sm font-semibold text-foreground mb-1">
                    {isRTL ? "هل تريد مساعدة في الإعداد؟" : "Need help setting up?"}
                  </p>
                  <p className="text-xs text-muted-foreground mb-3">
                    {isRTL
                      ? "جولة إرشادية سريعة لمساعدتك على البدء"
                      : "A quick guided tour to get you started"}
                  </p>
                  <Button size="sm" onClick={onStartOnboarding}>
                    {isRTL ? "ابدأ الجولة" : "Start Tour"}
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        )}

        <Button variant="ghost" onClick={() => setShowDetails(!showDetails)} className="text-xs">
          {isRTL ? "عرض تفاصيل الاشتراك" : "View subscription details"}
        </Button>
      </motion.div>
    </div>
  );
}
