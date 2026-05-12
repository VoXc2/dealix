"use client";

import { useEffect, useState } from "react";
import { useLocale } from "next-intl";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";

type AuditRow = {
  id: string;
  tenant_id: string;
  user_id: string | null;
  action: string;
  entity_type: string;
  entity_id: string | null;
  status: string;
  ip_address: string | null;
  request_id: string | null;
  created_at: string;
};

const API_BASE =
  (typeof window !== "undefined" && (window as any).__DEALIX_API_BASE__) ||
  process.env.NEXT_PUBLIC_API_BASE ||
  "";

function authHeader(): Record<string, string> {
  const token =
    typeof window !== "undefined"
      ? localStorage.getItem("dealix_access_token")
      : null;
  return token ? { Authorization: `Bearer ${token}` } : {};
}

export default function AuditLogPage() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const [rows, setRows] = useState<AuditRow[]>([]);
  const [loading, setLoading] = useState(true);
  const [action, setAction] = useState("");
  const [entityType, setEntityType] = useState("");

  const t = (ar: string, en: string) => (isAr ? ar : en);

  async function load() {
    setLoading(true);
    const params = new URLSearchParams();
    if (action) params.set("action", action);
    if (entityType) params.set("entity_type", entityType);
    try {
      const r = await fetch(`${API_BASE}/api/v1/audit-logs?${params}`, {
        headers: { accept: "application/json", ...authHeader() },
      });
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      const data = await r.json();
      setRows(data.items || []);
    } catch (err: any) {
      toast.error(err.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  function exportCsv() {
    const params = new URLSearchParams();
    if (action) params.set("action", action);
    if (entityType) params.set("entity_type", entityType);
    const token =
      typeof window !== "undefined"
        ? localStorage.getItem("dealix_access_token")
        : null;
    // Streaming endpoint — open via fetch + blob to attach the bearer.
    fetch(`${API_BASE}/api/v1/audit-logs/export.csv?${params}`, {
      headers: { ...authHeader() },
    })
      .then(async (r) => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        const blob = await r.blob();
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = `dealix-audit-${new Date().toISOString().slice(0, 10)}.csv`;
        a.click();
        URL.revokeObjectURL(url);
      })
      .catch((err) => toast.error(err.message));
  }

  return (
    <div className="p-8 max-w-6xl mx-auto space-y-6">
      <header className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">{t("سجل التدقيق", "Audit log")}</h1>
        <Button onClick={exportCsv}>{t("تصدير CSV", "Export CSV")}</Button>
      </header>

      <div className="flex gap-2 flex-wrap">
        <input
          className="bg-card border border-border rounded-lg px-3 py-2 text-sm"
          placeholder={t("الإجراء (مثال: lead.create)", "Action (e.g. lead.create)")}
          value={action}
          onChange={(e) => setAction(e.target.value)}
        />
        <input
          className="bg-card border border-border rounded-lg px-3 py-2 text-sm"
          placeholder={t("النوع (مثال: lead)", "Entity type (e.g. lead)")}
          value={entityType}
          onChange={(e) => setEntityType(e.target.value)}
        />
        <Button variant="outline" onClick={load}>
          {t("تطبيق", "Apply")}
        </Button>
      </div>

      {loading ? (
        <p>{t("جاري التحميل…", "Loading…")}</p>
      ) : rows.length === 0 ? (
        <p className="text-muted-foreground">
          {t("لا توجد أحداث في النافذة المختارة.", "No events in window.")}
        </p>
      ) : (
        <div className="overflow-x-auto bg-card border border-border rounded-xl">
          <table className="w-full text-sm">
            <thead className="text-muted-foreground text-left bg-muted">
              <tr>
                <th className="p-2">{t("التاريخ", "When")}</th>
                <th className="p-2">{t("الإجراء", "Action")}</th>
                <th className="p-2">{t("النوع", "Type")}</th>
                <th className="p-2">{t("المعرّف", "ID")}</th>
                <th className="p-2">{t("المستخدم", "User")}</th>
                <th className="p-2">{t("الحالة", "Status")}</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((r) => (
                <tr key={r.id} className="border-t border-border">
                  <td className="p-2 whitespace-nowrap">
                    {new Date(r.created_at).toLocaleString(isAr ? "ar-SA" : "en-US")}
                  </td>
                  <td className="p-2 font-mono">{r.action}</td>
                  <td className="p-2">{r.entity_type}</td>
                  <td className="p-2 font-mono">{r.entity_id || "—"}</td>
                  <td className="p-2 font-mono">{r.user_id || "—"}</td>
                  <td
                    className={`p-2 capitalize ${
                      r.status === "ok"
                        ? "text-emerald-500"
                        : r.status === "denied"
                        ? "text-amber-500"
                        : "text-rose-500"
                    }`}
                  >
                    {r.status}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
