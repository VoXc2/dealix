"use client";

import { useEffect, useState } from "react";
import { useLocale } from "next-intl";
import { toast } from "sonner";

const API_BASE =
  (typeof window !== "undefined" && (window as any).__DEALIX_API_BASE__) ||
  process.env.NEXT_PUBLIC_API_BASE ||
  "";

function adminHeader(): Record<string, string> {
  const k =
    typeof window !== "undefined"
      ? localStorage.getItem("dealix_admin_key") || ""
      : "";
  return k ? { "x-api-key": k } : {};
}

function tenantIdFromStorage(): string {
  if (typeof window === "undefined") return "";
  const raw = localStorage.getItem("dealix_user");
  if (!raw) return "";
  try {
    return JSON.parse(raw).tenant_id ?? "";
  } catch {
    return "";
  }
}

export default function IPAllowlistPage() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const t = (ar: string, en: string) => (isAr ? ar : en);
  const [cidrs, setCidrs] = useState("");
  const [saving, setSaving] = useState(false);
  const [tenant, setTenant] = useState("");

  useEffect(() => {
    setTenant(tenantIdFromStorage());
  }, []);

  async function save() {
    if (!tenant) {
      toast.error(t("لا يوجد مستأجر", "No tenant"));
      return;
    }
    setSaving(true);
    try {
      const list = cidrs
        .split(/[\n,]/g)
        .map((s) => s.trim())
        .filter(Boolean);
      const r = await fetch(
        `${API_BASE}/api/v1/admin/tenant/${tenant}/ip-allowlist`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            ...adminHeader(),
          },
          body: JSON.stringify({ cidrs: list }),
        }
      );
      const body = await r.json();
      if (!r.ok) throw new Error(body.detail || `HTTP ${r.status}`);
      toast.success(t("تم الحفظ", "Saved"));
    } catch (e: any) {
      toast.error(e.message);
    } finally {
      setSaving(false);
    }
  }

  async function clearAll() {
    if (!tenant) return;
    if (!window.confirm(t("متأكد؟", "Are you sure?"))) return;
    try {
      const r = await fetch(
        `${API_BASE}/api/v1/admin/tenant/${tenant}/ip-allowlist`,
        { method: "DELETE", headers: { ...adminHeader() } }
      );
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      setCidrs("");
      toast.success(t("تم المسح", "Cleared"));
    } catch (e: any) {
      toast.error(e.message);
    }
  }

  return (
    <div className="p-8 max-w-3xl mx-auto space-y-5">
      <header>
        <h1 className="text-3xl font-bold">
          {t("قائمة عناوين IP المسموحة", "IP allowlist")}
        </h1>
        <p className="text-muted-foreground mt-2">
          {t(
            "العناوين خارج هذه القائمة تُرفض بـ 403 ip_not_allowlisted. المسارات العامة (/api/v1/public/*) لا تتأثر.",
            "Requests from outside these CIDRs are blocked with 403 ip_not_allowlisted. Public paths (/api/v1/public/*) are exempt."
          )}
        </p>
      </header>
      <textarea
        rows={8}
        value={cidrs}
        onChange={(e) => setCidrs(e.target.value)}
        placeholder={"10.0.0.0/24\n203.0.113.5/32"}
        className="w-full font-mono text-sm p-3 border border-border rounded-lg bg-card"
        spellCheck={false}
      />
      <p className="text-xs text-muted-foreground">
        {t(
          "افصل العناوين بفاصلة أو سطر جديد. كل CIDR يتحقق منه بـ ipaddress.ip_network.",
          "Comma- or newline-separated. Each CIDR is validated via ipaddress.ip_network."
        )}
      </p>
      <div className="flex gap-2">
        <button
          onClick={save}
          disabled={saving}
          className="px-4 py-2 bg-emerald-600 hover:bg-emerald-700 disabled:bg-emerald-300 text-white rounded-lg font-medium"
        >
          {saving ? t("جاري الحفظ…", "Saving…") : t("حفظ", "Save")}
        </button>
        <button
          onClick={clearAll}
          className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg font-medium"
        >
          {t("مسح الكل", "Clear all")}
        </button>
      </div>
    </div>
  );
}
