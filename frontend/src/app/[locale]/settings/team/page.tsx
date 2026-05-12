"use client";

import { useEffect, useState } from "react";
import { useLocale } from "next-intl";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

const API_BASE =
  (typeof window !== "undefined" && (window as any).__DEALIX_API_BASE__) ||
  process.env.NEXT_PUBLIC_API_BASE ||
  "";

type Member = {
  id: string;
  email: string;
  name: string;
  is_active: boolean;
  mfa_enabled: boolean;
  last_login_at: string | null;
};

type Pending = { id: string; email: string; expires_at: string };

function tenantIdFromStorage(): string | null {
  if (typeof window === "undefined") return null;
  const raw = localStorage.getItem("dealix_user");
  if (!raw) return null;
  try {
    return JSON.parse(raw).tenant_id ?? null;
  } catch {
    return null;
  }
}

function authHeader(): Record<string, string> {
  const t = typeof window !== "undefined" ? localStorage.getItem("dealix_access_token") : null;
  return t ? { Authorization: `Bearer ${t}` } : {};
}

export default function TeamSettingsPage() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const t = (ar: string, en: string) => (isAr ? ar : en);
  const [members, setMembers] = useState<Member[]>([]);
  const [pending, setPending] = useState<Pending[]>([]);
  const [email, setEmail] = useState("");
  const [busy, setBusy] = useState(false);
  const tid = tenantIdFromStorage();

  async function load() {
    if (!tid) return;
    try {
      const r = await fetch(`${API_BASE}/api/v1/customers/${tid}/team/members`, {
        headers: { accept: "application/json", ...authHeader() },
      });
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      const data = await r.json();
      setMembers(data.members || []);
      setPending(data.pending_invites || []);
    } catch (err: any) {
      toast.error(err.message);
    }
  }

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [tid]);

  async function invite(e: React.FormEvent) {
    e.preventDefault();
    if (!tid) return;
    setBusy(true);
    try {
      const r = await fetch(`${API_BASE}/api/v1/customers/${tid}/team/invite`, {
        method: "POST",
        headers: { "content-type": "application/json", ...authHeader() },
        body: JSON.stringify({ email, role: "user" }),
      });
      if (!r.ok) {
        const d = await r.json().catch(() => ({}));
        throw new Error(d?.detail?.error || d?.detail || r.status);
      }
      const data = await r.json();
      toast.success(t("تم إرسال الدعوة", "Invite sent"));
      navigator.clipboard?.writeText(data.invite_url).catch(() => {});
      setEmail("");
      load();
    } catch (err: any) {
      toast.error(err.message);
    } finally {
      setBusy(false);
    }
  }

  async function revoke(userId: string) {
    if (!tid) return;
    if (!confirm(t("تأكيد الإلغاء؟", "Revoke this member?"))) return;
    const r = await fetch(`${API_BASE}/api/v1/customers/${tid}/team/members/${userId}`, {
      method: "DELETE",
      headers: { ...authHeader() },
    });
    if (!r.ok) {
      toast.error(`HTTP ${r.status}`);
      return;
    }
    toast.success(t("تم الإلغاء", "Revoked"));
    load();
  }

  return (
    <div className="p-8 max-w-3xl mx-auto space-y-6">
      <h1 className="text-3xl font-bold">{t("الفريق", "Team")}</h1>
      <form onSubmit={invite} className="flex gap-2 bg-card border border-border rounded-xl p-4">
        <Input
          type="email"
          placeholder={t("بريد المستخدم", "User email")}
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <Button type="submit" disabled={busy}>
          {busy ? "…" : t("ادعُ", "Invite")}
        </Button>
      </form>
      <section>
        <h2 className="font-semibold mb-2">{t("الأعضاء النشطون", "Active members")}</h2>
        {members.length === 0 ? (
          <p className="text-muted-foreground text-sm">{t("لا أعضاء بعد.", "No members yet.")}</p>
        ) : (
          <table className="w-full text-sm bg-card border border-border rounded-xl">
            <thead className="bg-muted text-muted-foreground text-left">
              <tr>
                <th className="p-2">{t("البريد", "Email")}</th>
                <th className="p-2">{t("الاسم", "Name")}</th>
                <th className="p-2">MFA</th>
                <th className="p-2">{t("آخر دخول", "Last login")}</th>
                <th className="p-2"></th>
              </tr>
            </thead>
            <tbody>
              {members.map((m) => (
                <tr key={m.id} className="border-t border-border">
                  <td className="p-2">{m.email}</td>
                  <td className="p-2">{m.name}</td>
                  <td className="p-2">{m.mfa_enabled ? "✓" : "—"}</td>
                  <td className="p-2">
                    {m.last_login_at ? new Date(m.last_login_at).toLocaleDateString(isAr ? "ar-SA" : "en-US") : "—"}
                  </td>
                  <td className="p-2 text-right">
                    <button onClick={() => revoke(m.id)} className="text-rose-500 hover:underline text-xs">
                      {t("إلغاء", "Revoke")}
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </section>
      <section>
        <h2 className="font-semibold mb-2">{t("دعوات قيد الانتظار", "Pending invites")}</h2>
        {pending.length === 0 ? (
          <p className="text-muted-foreground text-sm">{t("لا دعوات.", "No pending invites.")}</p>
        ) : (
          <ul className="space-y-1 text-sm">
            {pending.map((p) => (
              <li key={p.id} className="bg-card border border-border rounded-lg p-2 flex justify-between">
                <span>{p.email}</span>
                <span className="text-muted-foreground">
                  {t("تنتهي:", "expires:")} {new Date(p.expires_at).toLocaleDateString()}
                </span>
              </li>
            ))}
          </ul>
        )}
      </section>
    </div>
  );
}
