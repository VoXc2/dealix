"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { Check, Loader2, Shield, CreditCard, ArrowRight } from "lucide-react";
import { useLocale } from "next-intl";
import { cn } from "@/lib/utils";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { PaymentForm } from "./PaymentForm";

export interface PlanOption {
  id: string;
  name: string;
  nameAr: string;
  description: string;
  descriptionAr: string;
  monthlyPrice: number;
  yearlyPrice: number;
  features: Array<{ text: string; textAr: string; included: boolean }>;
  highlighted: boolean;
  cta: string;
  ctaAr: string;
}

interface CheckoutPanelProps {
  plan: PlanOption;
  billing: "monthly" | "yearly";
  onSuccess?: () => void;
  onCancel?: () => void;
}

export function CheckoutPanel({ plan, billing, onSuccess, onCancel }: CheckoutPanelProps) {
  const [step, setStep] = useState<"plan" | "payment" | "confirming">("plan");
  const [isProcessing, setIsProcessing] = useState(false);
  const locale = "ar";
  const isRTL = locale === "ar";
  const price = billing === "monthly" ? plan.monthlyPrice : plan.yearlyPrice;

  const handlePay = async () => {
    setStep("payment");
  };

  const handlePaymentSuccess = () => {
    setStep("confirming");
    setIsProcessing(false);
    onSuccess?.();
  };

  return (
    <Card className="max-w-lg mx-auto">
      <CardHeader>
        <div className="flex items-center justify-between mb-2">
          <CardTitle className="text-lg font-bold">
            {isRTL ? plan.nameAr : plan.name}
          </CardTitle>
          {plan.highlighted && (
            <Badge variant="default" className="bg-gold-500/10 text-gold-500 border-gold-500/20">
              {isRTL ? "الأكثر طلباً" : "Most Popular"}
            </Badge>
          )}
        </div>
        <CardDescription>
          {isRTL ? plan.descriptionAr : plan.description}
        </CardDescription>
        <div className="mt-4">
          <span className="text-3xl font-bold text-foreground">
            {new Intl.NumberFormat(isRTL ? "ar-SA" : "en-US", {
              style: "currency",
              currency: "SAR",
              minimumFractionDigits: 0,
            }).format(price)}
          </span>
          <span className="text-sm text-muted-foreground ml-1">
            /{billing === "monthly" ? (isRTL ? "شهر" : "mo") : (isRTL ? "سنة" : "yr")}
          </span>
        </div>
      </CardHeader>
      <CardContent className="space-y-6">
        {step === "plan" && (
          <>
            <div className="space-y-2">
              {plan.features.map((feat, idx) => (
                <div key={idx} className="flex items-center gap-2 text-sm">
                  <div
                    className={cn(
                      "flex h-5 w-5 items-center justify-center rounded-full",
                      feat.included ? "bg-emerald-500/10 text-emerald-500" : "bg-muted text-muted-foreground",
                    )}
                  >
                    <Check className="w-3 h-3" />
                  </div>
                  <span className={feat.included ? "text-foreground" : "text-muted-foreground line-through"}>
                    {isRTL ? feat.textAr : feat.text}
                  </span>
                </div>
              ))}
            </div>

            <div className="flex items-center gap-3 rounded-lg border border-border bg-accent/30 p-3 text-xs text-muted-foreground">
              <Shield className="w-4 h-4 text-emerald-500 shrink-0" />
              <span>
                {isRTL
                  ? "مدفوعات آمنة عبر Moyasar. لا نشارك معلومات بطاقتك."
                  : "Secure payments via Moyasar. We don't share your card info."}
              </span>
            </div>

            <div className="flex items-center gap-3">
              {onCancel && (
                <Button variant="ghost" onClick={onCancel} className="flex-1">
                  {isRTL ? "إلغاء" : "Cancel"}
                </Button>
              )}
              <Button onClick={handlePay} className="flex-1">
                {isRTL ? "متابعة للدفع" : "Proceed to Payment"}
                <ArrowRight className={cn("w-4 h-4 ml-1", isRTL && "rotate-180")} />
              </Button>
            </div>
          </>
        )}

        {step === "payment" && (
          <PaymentForm
            amount={price}
            currency="SAR"
            description={`${plan.name} - ${billing}`}
            planId={plan.id}
            billing={billing}
            onSuccess={handlePaymentSuccess}
            onBack={() => setStep("plan")}
          />
        )}

        {step === "confirming" && (
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="flex flex-col items-center py-8 text-center"
          >
            <div className="flex h-16 w-16 items-center justify-center rounded-full bg-emerald-500/10 mb-4">
              <Check className="w-8 h-8 text-emerald-500" />
            </div>
            <h3 className="text-lg font-bold text-foreground mb-2">
              {isRTL ? "تم الدفع بنجاح!" : "Payment Successful!"}
            </h3>
            <p className="text-sm text-muted-foreground mb-6">
              {isRTL
                ? `اشتراكك في ${plan.nameAr} نشط الآن`
                : `Your ${plan.name} subscription is now active`}
            </p>
            {isProcessing && <Loader2 className="w-5 h-5 animate-spin text-muted-foreground" />}
          </motion.div>
        )}
      </CardContent>
    </Card>
  );
}
