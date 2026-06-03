"use client";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

export function CheckoutPanel({
  plan,
  planLabel,
  priceHint,
  isAr,
  customerName = "",
}: {
  plan: string;
  planLabel: string;
  priceHint: string;
  isAr: boolean;
  customerName?: string;
}) {
  const [email, setEmail] = useState("");
  const [name, setName] = useState(customerName);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  const pay = async () => {
    if (!name.trim() || !email.trim()) return;
    setBusy(true);
    setError("");
    try {
      const base = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const adminKey = process.env.NEXT_PUBLIC_DEALIX_ADMIN_API_KEY || "";
      // Use the governed commercial payment route (approval_required gate, Moyasar invoice)
      const res = await fetch(`${base}/api/v1/commercial/payment/link`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...(adminKey ? { "X-Admin-API-Key": adminKey } : {}),
        },
        body: JSON.stringify({
          service_tier: plan,
          customer_name: name,
          customer_email: email,
        }),
      });
      const data = await res.json();
      if (data.payment_url) {
        window.location.href = data.payment_url;
      } else {
        setError(data.detail || (isAr ? "حدث خطأ — حاول لاحقاً" : "Error — try again"));
      }
    } catch {
      setError(isAr ? "تعذّر الاتصال بالخادم" : "Could not reach server");
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="mt-4 space-y-2 rounded border p-3 text-sm">
      <p className="font-medium">{planLabel} — {priceHint}</p>
      <Input
        type="text"
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder={isAr ? "اسمك أو اسم الشركة" : "Your name or company"}
      />
      <Input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="you@company.sa"
      />
      {error && <p className="text-red-600 text-xs">{error}</p>}
      <Button
        className="w-full"
        disabled={busy || !email.trim() || !name.trim()}
        onClick={pay}
      >
        {busy
          ? (isAr ? "جارٍ المعالجة…" : "Processing…")
          : (isAr ? "ادفع عبر Moyasar" : "Pay via Moyasar")}
      </Button>
    </div>
  );
}
