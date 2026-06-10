"use client";

import { useState } from "react";
import { Check, ArrowRight, HelpCircle, Loader2, TrendingUp, DollarSign } from "lucide-react";
import { useLocale } from "next-intl";
import { cn, formatCurrency, formatNumber } from "@/lib/utils";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { usePricing } from "@/lib/hooks/usePricing";

export default function PricingPage() {
  const [billing, setBilling] = useState<"monthly" | "yearly">("monthly");
  const [employees, setEmployees] = useState(20);
  const [dealsPerMonth, setDealsPerMonth] = useState(50);
  const locale = useLocale();
  const isRTL = locale === "ar";
  const { data, isLoading } = usePricing();

  const plans = data?.plans ?? [];
  const estimatedSavings = Math.round(employees * dealsPerMonth * 0.15);

  return (
    <div className="min-h-screen bg-background">
      {/* Hero */}
      <section className="relative overflow-hidden border-b border-border bg-gradient-to-b from-background to-accent/30">
        <div className="mx-auto max-w-6xl px-4 py-20 text-center">
          <Badge className="mb-4 bg-gold-500/10 text-gold-500 border-gold-500/20">
            {isRTL ? "أسعار شفافة" : "Transparent Pricing"}
          </Badge>
          <h1 className="text-4xl sm:text-5xl font-bold text-foreground mb-4">
            {isRTL ? "اختر الخطة المناسبة لعملك" : "Choose the Right Plan for Your Business"}
          </h1>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto mb-8">
            {isRTL
              ? "جميع الخطط تتضمن نسخة تجريبية مجانية لمدة 14 يوماً"
              : "All plans include a 14-day free trial"}
          </p>
        </div>
      </section>

      <div className="mx-auto max-w-6xl px-4 py-12 space-y-12">
        {/* Billing toggle */}
        <div className="flex items-center justify-center">
          <Tabs
            value={billing}
            onValueChange={(v) => setBilling(v as "monthly" | "yearly")}
            className="w-auto"
          >
            <TabsList className="rounded-xl p-1">
              <TabsTrigger value="monthly" className="rounded-lg text-sm">
                {isRTL ? "شهري" : "Monthly"}
              </TabsTrigger>
              <TabsTrigger value="yearly" className="rounded-lg text-sm">
                {isRTL ? "سنوي" : "Yearly"}
                <Badge className="ml-1.5 bg-emerald-500/10 text-emerald-500 border-emerald-500/20 text-[10px]">
                  {isRTL ? "وفر 20%" : "Save 20%"}
                </Badge>
              </TabsTrigger>
            </TabsList>
          </Tabs>
        </div>

        {/* Plans */}
        {isLoading ? (
          <div className="flex items-center justify-center py-20">
            <Loader2 className="w-6 h-6 animate-spin text-muted-foreground" />
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {plans.map((plan) => {
              const price = billing === "monthly" ? plan.monthlyPrice : plan.yearlyPrice;
              return (
                <Card
                  key={plan.id}
                  className={cn(
                    "relative flex flex-col transition-all duration-200 hover:border-gold-500/30 hover:shadow-lg",
                    plan.highlighted && "border-gold-500/50 shadow-xl shadow-gold-500/5 scale-105 md:scale-110",
                  )}
                >
                  {plan.highlighted && (
                    <div className="absolute -top-3 left-1/2 -translate-x-1/2 z-10">
                      <Badge className="bg-gold-500 text-white border-0 text-xs px-4 py-1">
                        {isRTL ? "الأكثر طلباً" : "Most Popular"}
                      </Badge>
                    </div>
                  )}
                  <CardHeader className={cn("pb-0", plan.highlighted && "pt-8")}>
                    <CardTitle className="text-xl font-bold">
                      {isRTL ? plan.nameAr : plan.name}
                    </CardTitle>
                    <CardDescription>
                      {isRTL ? plan.descriptionAr : plan.description}
                    </CardDescription>
                    <div className="mt-4">
                      <span className="text-4xl font-bold text-foreground">
                        {formatCurrency(price, locale)}
                      </span>
                      <span className="text-sm text-muted-foreground ml-1">
                        /{billing === "monthly" ? (isRTL ? "شهر" : "mo") : (isRTL ? "سنة" : "yr")}
                      </span>
                    </div>
                  </CardHeader>
                  <CardContent className="flex flex-col flex-1 pt-6">
                    <div className="space-y-3 flex-1 mb-6">
                      {plan.features.map((feat, idx) => (
                        <div key={idx} className="flex items-start gap-2">
                          <div
                            className={cn(
                              "flex h-5 w-5 shrink-0 items-center justify-center rounded-full mt-0.5",
                              feat.included ? "bg-emerald-500/10" : "bg-muted",
                            )}
                          >
                            <Check
                              className={cn(
                                "w-3 h-3",
                                feat.included ? "text-emerald-500" : "text-muted-foreground",
                              )}
                            />
                          </div>
                          <span
                            className={cn(
                              "text-sm",
                              feat.included ? "text-foreground" : "text-muted-foreground line-through",
                            )}
                          >
                            {isRTL ? feat.textAr : feat.text}
                          </span>
                        </div>
                      ))}
                    </div>
                    <Button
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

        {/* ROI Calculator */}
        <Card className="border-gold-500/20 bg-gradient-to-br from-gold-500/5 to-transparent">
          <CardHeader>
            <div className="flex items-center gap-2">
              <TrendingUp className="w-5 h-5 text-gold-500" />
              <CardTitle className="text-lg font-bold">
                {isRTL ? "حاسبة العائد على الاستثمار" : "ROI Calculator"}
              </CardTitle>
            </div>
            <CardDescription>
              {isRTL
                ? "احسب كم ستوفر باستخدام ديليكس"
                : "Calculate how much you'll save with Dealix"}
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div>
                <label className="block text-sm font-medium text-foreground mb-2">
                  {isRTL ? "عدد الموظفين" : "Number of Employees"}
                </label>
                <input
                  type="range"
                  min={5}
                  max={500}
                  value={employees}
                  onChange={(e) => setEmployees(Number(e.target.value))}
                  className="w-full"
                />
                <span className="text-sm font-semibold text-foreground">{employees}</span>
              </div>
              <div>
                <label className="block text-sm font-medium text-foreground mb-2">
                  {isRTL ? "الصفقات شهرياً" : "Deals per Month"}
                </label>
                <input
                  type="range"
                  min={10}
                  max={500}
                  value={dealsPerMonth}
                  onChange={(e) => setDealsPerMonth(Number(e.target.value))}
                  className="w-full"
                />
                <span className="text-sm font-semibold text-foreground">{formatNumber(dealsPerMonth)}</span>
              </div>
              <div className="flex flex-col items-center justify-center bg-accent/30 rounded-xl p-4 text-center">
                <DollarSign className="w-6 h-6 text-gold-500 mb-1" />
                <p className="text-xs text-muted-foreground">
                  {isRTL ? "التوفير المقدر شهرياً" : "Estimated Monthly Savings"}
                </p>
                <p className="text-2xl font-bold text-gold-500">
                  {formatCurrency(estimatedSavings, locale)}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* FAQ */}
        <Card>
          <CardHeader>
            <div className="flex items-center gap-2">
              <HelpCircle className="w-5 h-5 text-gold-500" />
              <CardTitle className="text-lg font-bold">
                {isRTL ? "الأسئلة الشائعة" : "Frequently Asked Questions"}
              </CardTitle>
            </div>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {[
                {
                  q: "هل يمكنني الترقية أو تخفيض الخطط؟",
                  qEn: "Can I upgrade or downgrade my plan?",
                  a: "نعم، يمكنك الترقية أو تخفيض خطتك في أي وقت. سيتم تطبيق التغيير في الفترة التالية.",
                  aEn: "Yes, you can upgrade or downgrade your plan at any time. Changes apply next billing period.",
                },
                {
                  q: "هل توجد رسوم إعداد؟",
                  qEn: "Are there any setup fees?",
                  a: "لا، لا توجد رسوم إعداد. يتم الدفع شهرياً أو سنوياً حسب اختيارك.",
                  aEn: "No, there are no setup fees. Pay monthly or yearly as you choose.",
                },
                {
                  q: "ماذا يحدث بعد انتهاء الفترة التجريبية؟",
                  qEn: "What happens after the trial ends?",
                  a: "يمكنك الاشتراك في أي خطة مدفوعة. إذا لم تختر، سينتقل حسابك إلى الخطة المجانية.",
                  aEn: "Subscribe to any paid plan. If you don't, your account will move to the free plan.",
                },
              ].map((faq, idx) => (
                <details key={idx} className="group rounded-lg border border-border [&_summary]:open:rounded-b-none">
                  <summary className="flex items-center justify-between px-4 py-3 cursor-pointer text-sm font-medium text-foreground hover:bg-accent/30 rounded-lg transition-colors">
                    {isRTL ? faq.q : faq.qEn}
                    <ChevronRightIcon className="w-4 h-4 text-muted-foreground group-open:rotate-90 transition-transform" />
                  </summary>
                  <div className="px-4 py-3 text-sm text-muted-foreground border-t border-border">
                    {isRTL ? faq.a : faq.aEn}
                  </div>
                </details>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

function ChevronRightIcon({ className }: { className?: string }) {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="16"
      height="16"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      className={className}
    >
      <path d="m9 18 6-6-6-6" />
    </svg>
  );
}
