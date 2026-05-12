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

function authHeader(): Record<string, string> {
  const t = typeof window !== "undefined" ? localStorage.getItem("dealix_access_token") : null;
  return t ? { Authorization: `Bearer ${t}` } : {};
}

export default function SupportPage() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const t = (ar: string, en: string) => (isAr ? ar : en);
  const [form, setForm] = useState({ subject: "", body: "", email: "", name: "" });
  const [busy, setBusy] = useState(false);
  const [thread, setThread] = useState<string | null>(null);

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setBusy(true);
    try {
      const r = await fetch(`${API_BASE}/api/v1/support/tickets`, {
        method: "POST",
        headers: { "content-type": "application/json", ...authHeader() },
        body: JSON.stringify(form),
      });
      if (!r.ok) {
        const d = await r.json().catch(() => ({}));
        throw new Error(d?.detail || r.status);
      }
      const data = await r.json();
      setThread(data.thread_id || "(submitted)");
      toast.success(t("تم إنشاء التذكرة", "Ticket created"));
    } catch (err: any) {
      toast.error(err.message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="p-8 max-w-2xl mx-auto space-y-6" data-tour="support">
      <h1 className="text-3xl font-bold">{t("الدعم", "Support")}</h1>
      <p className="text-muted-foreground">
        {t(
          "افتح تذكرة وسيتواصل الفريق خلال يوم عمل واحد.",
          "Open a ticket — we respond within one business day."
        )}
      </p>
      {thread ? (
        <div className="bg-card border border-emerald-500/40 rounded-xl p-6">
          <p className="text-emerald-500 font-semibold">
            {t("تم — معرّف التذكرة:", "Done — ticket id:")} {thread}
          </p>
        </div>
      ) : (
        <form onSubmit={submit} className="space-y-4 bg-card border border-border rounded-xl p-6">
          <div>
            <Label>{t("الاسم", "Your name")}</Label>
            <Input value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} required />
          </div>
          <div>
            <Label>{t("البريد الإلكتروني", "Email")}</Label>
            <Input type="email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} required />
          </div>
          <div>
            <Label>{t("الموضوع", "Subject")}</Label>
            <Input value={form.subject} onChange={(e) => setForm({ ...form, subject: e.target.value })} required />
          </div>
          <div>
            <Label>{t("الوصف", "Description")}</Label>
            <textarea
              className="w-full bg-background border border-border rounded-lg px-3 py-2 text-sm min-h-[140px]"
              value={form.body}
              onChange={(e) => setForm({ ...form, body: e.target.value })}
              required
            />
          </div>
          <Button type="submit" disabled={busy} className="w-full">
            {busy ? "…" : t("أرسل", "Submit")}
          </Button>
        </form>
      )}
    </div>
  );
}
