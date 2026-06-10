"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { CreditCard, Banknote, Smartphone, Loader2, ChevronLeft } from "lucide-react";
import { useLocale } from "next-intl";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";

type PaymentMethod = "mada" | "stcpay" | "moyasar" | "card";

interface PaymentFormProps {
  amount: number;
  currency: string;
  description: string;
  planId: string;
  billing: "monthly" | "yearly";
  onSuccess: () => void;
  onBack: () => void;
}

const methods: Array<{
  id: PaymentMethod;
  icon: React.ElementType;
  label: string;
  labelAr: string;
  description: string;
  descriptionAr: string;
}> = [
  { id: "mada", icon: CreditCard, label: "Mada", labelAr: "مدى", description: "Debit card", descriptionAr: "بطاقة مدى" },
  { id: "stcpay", icon: Smartphone, label: "STC Pay", labelAr: "إس تي سي باي", description: "Mobile wallet", descriptionAr: "محفظة جوال" },
  { id: "moyasar", icon: Banknote, label: "Moyasar", labelAr: "مياسر", description: "Credit/debit card", descriptionAr: "بطاقة ائتمانية" },
  { id: "card", icon: CreditCard, label: "Visa/Mastercard", labelAr: "فيزا/ماستركارد", description: "International card", descriptionAr: "بطاقة دولية" },
];

export function PaymentForm({ amount, currency, description, planId, billing, onSuccess, onBack }: PaymentFormProps) {
  const [selectedMethod, setSelectedMethod] = useState<PaymentMethod | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [cardInfo, setCardInfo] = useState({ number: "", exp: "", cvc: "", name: "" });
  const locale = "ar";
  const isRTL = locale === "ar";

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedMethod) return;
    setIsProcessing(true);
    try {
      await new Promise((r) => setTimeout(r, 1500));
      toast.success(isRTL ? "تم الدفع بنجاح" : "Payment successful");
      onSuccess();
    } catch {
      toast.error(isRTL ? "فشلت عملية الدفع" : "Payment failed");
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-5">
      {/* Payment method selection */}
      <div className="space-y-2">
        <label className="text-sm font-medium text-foreground">
          {isRTL ? "طريقة الدفع" : "Payment Method"}
        </label>
        <div className="grid grid-cols-2 gap-2">
          {methods.map((method) => {
            const Icon = method.icon;
            const isSelected = selectedMethod === method.id;
            return (
              <button
                key={method.id}
                type="button"
                onClick={() => setSelectedMethod(method.id)}
                className={cn(
                  "flex flex-col items-center gap-1.5 rounded-xl border p-3 transition-all text-center",
                  isSelected
                    ? "border-gold-500 bg-gold-500/10"
                    : "border-border hover:border-foreground/30",
                )}
              >
                <Icon className={cn("w-5 h-5", isSelected ? "text-gold-500" : "text-muted-foreground")} />
                <span className="text-xs font-medium">{isRTL ? method.labelAr : method.label}</span>
                <span className="text-[10px] text-muted-foreground">
                  {isRTL ? method.descriptionAr : method.description}
                </span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Card details */}
      {(selectedMethod === "mada" || selectedMethod === "card" || selectedMethod === "moyasar") && (
        <motion.div
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: "auto" }}
          className="space-y-3 overflow-hidden"
        >
          <div>
            <label className="block text-xs font-medium text-muted-foreground mb-1">
              {isRTL ? "رقم البطاقة" : "Card Number"}
            </label>
            <input
              type="text"
              value={cardInfo.number}
              onChange={(e) => setCardInfo((p) => ({ ...p, number: e.target.value }))}
              placeholder="4111 1111 1111 1111"
              maxLength={19}
              className="w-full rounded-lg border border-border bg-background px-3 py-2.5 text-sm font-mono"
              dir="ltr"
              required
            />
          </div>
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-medium text-muted-foreground mb-1">MM/YY</label>
              <input
                type="text"
                value={cardInfo.exp}
                onChange={(e) => setCardInfo((p) => ({ ...p, exp: e.target.value }))}
                placeholder="12/28"
                maxLength={5}
                className="w-full rounded-lg border border-border bg-background px-3 py-2.5 text-sm font-mono"
                dir="ltr"
                required
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-muted-foreground mb-1">CVC</label>
              <input
                type="text"
                value={cardInfo.cvc}
                onChange={(e) => setCardInfo((p) => ({ ...p, cvc: e.target.value }))}
                placeholder="123"
                maxLength={4}
                className="w-full rounded-lg border border-border bg-background px-3 py-2.5 text-sm font-mono"
                dir="ltr"
                required
              />
            </div>
          </div>
          <div>
            <label className="block text-xs font-medium text-muted-foreground mb-1">
              {isRTL ? "اسم حامل البطاقة" : "Cardholder Name"}
            </label>
            <input
              type="text"
              value={cardInfo.name}
              onChange={(e) => setCardInfo((p) => ({ ...p, name: e.target.value }))}
              placeholder="John Doe"
              className="w-full rounded-lg border border-border bg-background px-3 py-2.5 text-sm"
              dir="ltr"
              required
            />
          </div>
        </motion.div>
      )}

      {/* Summary */}
      <div className="rounded-lg border border-border bg-accent/30 p-3 space-y-1 text-sm">
        <div className="flex justify-between text-muted-foreground">
          <span>{description}</span>
          <span>{new Intl.NumberFormat(isRTL ? "ar-SA" : "en-US", { style: "currency", currency }).format(amount)}</span>
        </div>
        <div className="flex justify-between font-semibold text-foreground border-t border-border pt-1 mt-1">
          <span>{isRTL ? "المجموع" : "Total"}</span>
          <span>{new Intl.NumberFormat(isRTL ? "ar-SA" : "en-US", { style: "currency", currency }).format(amount)}</span>
        </div>
      </div>

      {/* Actions */}
      <div className="flex items-center gap-3">
        <Button type="button" variant="ghost" onClick={onBack}>
          <ChevronLeft className="w-4 h-4 mr-1" />
          {isRTL ? "رجوع" : "Back"}
        </Button>
        <Button type="submit" disabled={!selectedMethod || isProcessing} className="flex-1">
          {isProcessing ? (
            <Loader2 className="w-4 h-4 animate-spin mr-1" />
          ) : null}
          {isProcessing
            ? (isRTL ? "جاري المعالجة..." : "Processing...")
            : (isRTL ? "تأكيد الدفع" : "Confirm Payment")}
        </Button>
      </div>
    </form>
  );
}
