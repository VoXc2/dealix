"use client";

import { useState } from "react";
import { useLocale } from "next-intl";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

const API_BASE =
  (typeof window !== "undefined" && (window as any).__DEALIX_API_BASE__) ||
  process.env.NEXT_PUBLIC_API_BASE ||
  "";

export default function TrialPage() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const t = (ar: string, en: string) => (isAr ? ar : en);
  const [form, setForm] = useState({
    email: "",
    company: "",
    name: "",
    phone: "",
    sector: "",
    use_case: "",
    consent: false,
  });
  const [busy, setBusy] = useState(false);
  const [tenantId, setTenantId] = useState<string | null>(null);
  const [apiKey, setApiKey] = useState<string | null>(null);

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setBusy(true);
    try {
      const r = await fetch(`${API_BASE}/api/v1/trial/start`, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify(form),
      });
      if (!r.ok) {
        const d = await r.json().catch(() => ({}));
        throw new Error(d?.detail || r.status);
      }
      const data = await r.json();
      setTenantId(data.tenant_id);
      setApiKey(data.api_key);
      toast.success(t("تجربتك جاهزة!", "Your trial is ready!"));
    } catch (err: any) {
      toast.error(err.message);
    } finally {
      setBusy(false);
    }
  }

  if (tenantId && apiKey) {
    return (
      <div className="p-8 max-w-xl mx-auto space-y-6">
        <h1 className="text-3xl font-bold">
          {t("جاهز! تجربتك المجانية 14 يوم بدأت", "You're in — 14-day free trial started")}
        </h1>
        <div className="bg-card border border-emerald-500/40 rounded-xl p-6 space-y-3">
          <div>
            <div className="text-muted-foreground text-sm">{t("Tenant ID", "Tenant ID")}</div>
            <code className="block bg-muted p-2 rounded text-sm">{tenantId}</code>
          </div>
          <div>
            <div className="text-muted-foreground text-sm">
              {t("مفتاح API (يُعرض مرة واحدة)", "API key (shown once)")}
            </div>
            <code className="block bg-muted p-2 rounded text-sm break-all">{apiKey}</code>
          </div>
          <p className="text-xs text-muted-foreground">
            {t(
              "احفظ المفتاح الآن — لن يُعرض مرة أخرى.",
              "Save this key now — it will not be shown again."
            )}
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="p-8 max-w-xl mx-auto">
      <h1 className="text-3xl font-bold mb-2">{t("تجربة مجانية 14 يوم", "Free 14-day trial")}</h1>
      <p className="text-muted-foreground mb-6">
        {t("لا حاجة لبطاقة. ابدأ الآن.", "No card needed. Start now.")}
      </p>
      <form onSubmit={submit} className="space-y-4 bg-card border border-border rounded-xl p-6">
        <div>
          <Label>{t("الشركة", "Company")}</Label>
          <Input value={form.company} onChange={(e) => setForm({ ...form, company: e.target.value })} required />
        </div>
        <div>
          <Label>{t("اسمك", "Your name")}</Label>
          <Input value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} required />
        </div>
        <div>
          <Label>{t("البريد الإلكتروني", "Work email")}</Label>
          <Input type="email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} required />
        </div>
        <div>
          <Label>{t("القطاع", "Sector")}</Label>
          <Input value={form.sector} onChange={(e) => setForm({ ...form, sector: e.target.value })} />
        </div>
        <label className="flex items-center gap-2 text-sm">
          <input
            type="checkbox"
            checked={form.consent}
            onChange={(e) => setForm({ ...form, consent: e.target.checked })}
          />
          {t("أوافق على شروط الخدمة وسياسة PDPL", "I accept the Terms and PDPL policy")}
        </label>
        <Button type="submit" disabled={busy} className="w-full">
          {busy ? "…" : t("ابدأ الآن", "Start now")}
        </Button>
      </form>
    </div>
  );
}
