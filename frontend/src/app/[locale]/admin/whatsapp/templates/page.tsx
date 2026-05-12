"use client";

import { useEffect, useState } from "react";
import { useLocale } from "next-intl";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

const API_BASE =
  (typeof window !== "undefined" && (window as any).__DEALIX_API_BASE__) ||
  process.env.NEXT_PUBLIC_API_BASE ||
  "";

function authHeader(): Record<string, string> {
  const t = typeof window !== "undefined" ? localStorage.getItem("dealix_access_token") : null;
  return t ? { Authorization: `Bearer ${t}` } : {};
}

type Template = { name: string; language: string; category: string; status: string };

export default function WhatsAppTemplatesAdmin() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const t = (ar: string, en: string) => (isAr ? ar : en);
  const [templates, setTemplates] = useState<Template[]>([]);
  const [loading, setLoading] = useState(true);
  const [sendTo, setSendTo] = useState("");
  const [name, setName] = useState("");
  const [language, setLanguage] = useState("ar");

  useEffect(() => {
    fetch(`${API_BASE}/api/v1/admin/whatsapp/templates`, {
      headers: { accept: "application/json", ...authHeader() },
    })
      .then(async (r) => {
        if (r.status === 503) {
          toast.warning(t("واتساب غير مكوّن.", "WhatsApp not configured."));
          throw new Error("not configured");
        }
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        return r.json();
      })
      .then((d) => setTemplates(d.templates || []))
      .catch(() => setTemplates([]))
      .finally(() => setLoading(false));
  }, []);

  async function send() {
    const r = await fetch(`${API_BASE}/api/v1/admin/whatsapp/send`, {
      method: "POST",
      headers: { "content-type": "application/json", ...authHeader() },
      body: JSON.stringify({ to: sendTo, template_name: name, language_code: language, parameters: [] }),
    });
    const data = await r.json();
    if (data.ok) toast.success(t("أُرسل", "Sent"));
    else toast.error(data.error || `HTTP ${r.status}`);
  }

  return (
    <div className="p-8 max-w-4xl mx-auto space-y-6">
      <h1 className="text-3xl font-bold">{t("قوالب واتساب", "WhatsApp templates")}</h1>
      {loading ? (
        <p>{t("جاري التحميل…", "Loading…")}</p>
      ) : templates.length === 0 ? (
        <p className="text-muted-foreground text-sm">{t("لا قوالب معتمدة بعد.", "No approved templates.")}</p>
      ) : (
        <table className="w-full text-sm bg-card border border-border rounded-xl">
          <thead className="bg-muted text-muted-foreground text-left">
            <tr>
              <th className="p-2">{t("الاسم", "Name")}</th>
              <th className="p-2">{t("اللغة", "Language")}</th>
              <th className="p-2">{t("الفئة", "Category")}</th>
              <th className="p-2">{t("الحالة", "Status")}</th>
            </tr>
          </thead>
          <tbody>
            {templates.map((tp) => (
              <tr key={`${tp.name}-${tp.language}`} className="border-t border-border">
                <td className="p-2 font-mono">{tp.name}</td>
                <td className="p-2">{tp.language}</td>
                <td className="p-2">{tp.category}</td>
                <td className="p-2 capitalize">{tp.status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      <section className="bg-card border border-border rounded-xl p-4 space-y-2">
        <h2 className="font-semibold">{t("اختبار إرسال", "Send tester")}</h2>
        <div className="flex gap-2">
          <Input placeholder={t("الرقم", "to phone")} value={sendTo} onChange={(e) => setSendTo(e.target.value)} />
          <Input placeholder={t("اسم القالب", "template")} value={name} onChange={(e) => setName(e.target.value)} />
          <Input placeholder="ar" value={language} onChange={(e) => setLanguage(e.target.value)} className="w-24" />
          <Button onClick={send}>{t("أرسل", "Send")}</Button>
        </div>
      </section>
    </div>
  );
}
