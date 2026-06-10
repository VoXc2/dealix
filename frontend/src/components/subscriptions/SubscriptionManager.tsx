"use client";

import { useState } from "react";
import { Check, CreditCard, ArrowRight, Loader2, RefreshCw } from "lucide-react";
import { useLocale } from "next-intl";
import { cn, formatCurrency } from "@/lib/utils";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { useSubscription, useUpdateSubscription, useCancelSubscription } from "@/lib/hooks/usePayments";
import { usePlans, type PlanData } from "@/lib/hooks/usePricing";
import { CheckoutPanel } from "./CheckoutPanel";
import { PostPurchase } from "./PostPurchase";

export function SubscriptionManager() {
  const [billing, setBilling] = useState<"monthly" | "yearly">("monthly");
  const [selectedPlan, setSelectedPlan] = useState<PlanData | null>(null);
  const [showCheckout, setShowCheckout] = useState(false);
  const [showSuccess, setShowSuccess] = useState(false);
  const locale = useLocale();
  const isRTL = locale === "ar";

  const { data: subscription, isLoading: subLoading } = useSubscription();
  const { data: plansData, isLoading: plansLoading } = usePlans();
  const updateSub = useUpdateSubscription();
  const cancelSub = useCancelSubscription();

  const plans = plansData ?? [];

  const handleSelectPlan = (plan: PlanData) => {
    setSelectedPlan(plan);
    setShowCheckout(true);
    setShowSuccess(false);
  };

  const handleCheckoutSuccess = () => {
    setShowCheckout(false);
    setShowSuccess(true);
  };

  const handleCancel = async () => {
    await cancelSub.mutateAsync({ cancelAtPeriodEnd: true });
  };

  if (showSuccess && selectedPlan) {
    return (
      <PostPurchase
        planName={selectedPlan.name}
        planNameAr={selectedPlan.nameAr}
      />
    );
  }

  if (showCheckout && selectedPlan) {
    return (
      <CheckoutPanel
        plan={selectedPlan}
        billing={billing}
        onSuccess={handleCheckoutSuccess}
        onCancel={() => setShowCheckout(false)}
      />
    );
  }

  return (
    <div className="space-y-8">
      {/* Current subscription */}
      {subscription && (
        <Card>
          <CardContent className="p-5">
            <div className="flex items-start justify-between">
              <div>
                <p className="text-xs text-muted-foreground mb-1">
                  {isRTL ? "الاشتراك الحالي" : "Current Subscription"}
                </p>
                <p className="text-lg font-bold text-foreground">{subscription.planName}</p>
                <p className="text-sm text-muted-foreground">
                  {formatCurrency(subscription.amount, locale)}/{subscription.interval === "monthly" ? (isRTL ? "شهر" : "mo") : (isRTL ? "سنة" : "yr")}
                </p>
              </div>
              <Badge
                variant="outline"
                className={cn(
                  subscription.status === "active"
                    ? "bg-emerald-500/10 text-emerald-500 border-emerald-500/20"
                    : subscription.status === "trialing"
                      ? "bg-blue-500/10 text-blue-500 border-blue-500/20"
                      : "bg-amber-500/10 text-amber-500 border-amber-500/20",
                )}
              >
                {subscription.status === "active"
                  ? isRTL ? "نشط" : "Active"
                  : subscription.status === "trialing"
                    ? isRTL ? "تجريبي" : "Trial"
                    : subscription.status}
              </Badge>
            </div>
            {subscription.cancelAtPeriodEnd && (
              <p className="mt-2 text-xs text-amber-500">
                {isRTL
                  ? "سيتم إلغاء الاشتراك في نهاية الفترة الحالية"
                  : "Subscription will be canceled at end of current period"}
              </p>
            )}
          </CardContent>
        </Card>
      )}

      {/* Billing toggle */}
      <div className="flex items-center justify-center gap-2">
        <button
          onClick={() => setBilling("monthly")}
          className={cn(
            "rounded-lg px-4 py-2 text-sm font-medium transition-colors",
            billing === "monthly"
              ? "bg-accent text-foreground"
              : "text-muted-foreground hover:text-foreground",
          )}
        >
          {isRTL ? "شهري" : "Monthly"}
        </button>
        <button
          onClick={() => setBilling("yearly")}
          className={cn(
            "rounded-lg px-4 py-2 text-sm font-medium transition-colors",
            billing === "yearly"
              ? "bg-accent text-foreground"
              : "text-muted-foreground hover:text-foreground",
          )}
        >
          {isRTL ? "سنوي" : "Yearly"}
          <Badge className="ml-1.5 bg-gold-500/10 text-gold-500 border-gold-500/20 text-[10px]">
            {isRTL ? "وفر 20%" : "Save 20%"}
          </Badge>
        </button>
      </div>

      {/* Plans grid */}
      {plansLoading ? (
        <div className="flex items-center justify-center py-12">
          <Loader2 className="w-5 h-5 animate-spin text-muted-foreground" />
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {plans.map((plan) => {
            const price = billing === "monthly" ? plan.monthlyPrice : plan.yearlyPrice;
            return (
              <Card
                key={plan.id}
                className={cn(
                  "relative flex flex-col transition-all hover:border-gold-500/30",
                  plan.highlighted && "border-gold-500/50 shadow-lg shadow-gold-500/5",
                )}
              >
                {plan.highlighted && (
                  <div className="absolute -top-3 left-1/2 -translate-x-1/2">
                    <Badge className="bg-gold-500 text-white border-0 text-xs">
                      {isRTL ? "الأكثر طلباً" : "Most Popular"}
                    </Badge>
                  </div>
                )}
                <CardContent className="p-6 flex flex-col flex-1">
                  <h3 className="text-lg font-bold text-foreground mb-1">
                    {isRTL ? plan.nameAr : plan.name}
                  </h3>
                  <p className="text-xs text-muted-foreground mb-4">
                    {isRTL ? plan.descriptionAr : plan.description}
                  </p>
                  <div className="mb-4">
                    <span className="text-3xl font-bold text-foreground">
                      {formatCurrency(price, locale)}
                    </span>
                    <span className="text-sm text-muted-foreground ml-1">
                      /{billing === "monthly" ? (isRTL ? "شهر" : "mo") : (isRTL ? "سنة" : "yr")}
                    </span>
                  </div>
                  <div className="space-y-2 mb-6 flex-1">
                    {plan.features.map((feat, idx) => (
                      <div key={idx} className="flex items-center gap-2 text-xs">
                        <div
                          className={cn(
                            "flex h-4 w-4 items-center justify-center rounded-full",
                            feat.included ? "bg-emerald-500/10 text-emerald-500" : "bg-muted text-muted-foreground",
                          )}
                        >
                          <Check className="w-2.5 h-2.5" />
                        </div>
                        <span className={feat.included ? "text-foreground" : "text-muted-foreground line-through"}>
                          {isRTL ? feat.textAr : feat.text}
                        </span>
                      </div>
                    ))}
                  </div>
                  <Button
                    onClick={() => handleSelectPlan(plan)}
                    className={cn(
                      "w-full",
                      plan.highlighted
                        ? "bg-gold-500 hover:bg-gold-400 text-white"
                        : "",
                    )}
                    variant={plan.highlighted ? "default" : "outline"}
                  >
                    {isRTL ? plan.ctaAr : plan.cta}
                    <ArrowRight className={cn("w-4 h-4 ml-1", isRTL && "rotate-180")} />
                  </Button>
                </CardContent>
              </Card>
            );
          })}
        </div>
      )}
    </div>
  );
}
