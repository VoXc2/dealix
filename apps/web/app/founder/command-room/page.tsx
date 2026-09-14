"use client";

import { useCallback, useEffect, useState } from "react";

import MetricCard from "@/components/MetricCard";
import { StageBadge } from "@/components/crm/StageBadge";
import { useAdminKey } from "@/hooks/useAdminKey";
import { api } from "@/lib/api";

// ── Types (mirror GET /api/v1/founder/command-room) ──────────────────────────

interface WarRoomRow {
  lead_id: string;
  target: string;
  segment: string;
  offer: string;
  next_action: string;
  next_action_due: string | null;
  status: string;
  stage: string;
  lead_score: number;
}

interface CommandRoom {
  generated_at: string;
  mode: string;
  launch: {
    status: string;
    paid: number;
    article13_target: number;
    founder_actions: { ar: string; en: string }[];
  };
  offer_ladder: { name: string; detail: string }[];
  summary: {
    today: {
      approved_touches_target: number;
      follow_ups_target: number;
      top_targets_count: number;
      follow_ups_due: number;
    };
    revenue: {
      conversations: number;
      meetings: number;
      scopes: number;
      invoices: number;
      paid: number;
    };
    queues: Record<string, number>;
    risks: Record<string, boolean>;
    top_targets: WarRoomRow[];
  };
}

const QUEUE_LABELS: Record<string, { ar: string; en: string }> = {
  needs_proof: { ar: "بحاجة إثبات", en: "Needs proof" },
  ready_meeting: { ar: "جاهز لاجتماع", en: "Ready for meeting" },
  needs_scope: { ar: "بحاجة نطاق", en: "Needs scope" },
  needs_invoice: { ar: "بحاجة فاتورة", en: "Needs invoice" },
  needs_delivery: { ar: "بحاجة تسليم", en: "Needs delivery" },
  upsell: { ar: "فرصة توسعة", en: "Upsell" },
};

const RISK_LABELS: Record<string, { ar: string; en: string }> = {
  no_live_auto_send: { ar: "لا إرسال تلقائي", en: "No auto-send" },
  no_cold_whatsapp: { ar: "لا واتساب بارد", en: "No cold WhatsApp" },
  no_fake_proof: { ar: "لا إثبات زائف", en: "No fake proof" },
  no_revenue_claim_before_payment: {
    ar: "لا ادعاء إيراد قبل الدفع",
    en: "No revenue claim before payment",
  },
};

// ── Page ─────────────────────────────────────────────────────────────────────

export default function FounderCommandRoomPage() {
  const { adminKey, setAdminKey, clearAdminKey, ready } = useAdminKey();
  const [keyInput, setKeyInput] = useState("");
  const [data, setData] = useState<CommandRoom | null>(null);
  const [pendingApprovals, setPendingApprovals] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [lastRefreshed, setLastRefreshed] = useState<string>("");

  const load = useCallback(async () => {
    if (!adminKey) return;
    setLoading(true);
    setError(null);
    try {
      const res = await api.getFounderCommandRoom(adminKey);
      setData(res.data as CommandRoom);
      setLastRefreshed(new Date().toLocaleTimeString("ar-SA"));
      // Best-effort: surface the approvals queue depth, but never block on it.
      try {
        const ap = await api.getApprovalsPending();
        const body = ap.data as { items?: unknown[]; pending?: unknown[] } | unknown[];
        const items = Array.isArray(body) ? body : (body.items ?? body.pending ?? []);
        setPendingApprovals(Array.isArray(items) ? items.length : null);
      } catch {
        setPendingApprovals(null);
      }
    } catch (e: unknown) {
      const status = (e as { response?: { status?: number } })?.response?.status;
      if (status === 401 || status === 403) {
        setError("مفتاح الأدمن غير صالح — Invalid admin key.");
        clearAdminKey();
        setData(null);
      } else {
        setError("تعذّر تحميل غرفة القيادة — Could not load the command room.");
      }
    } finally {
      setLoading(false);
    }
  }, [adminKey, clearAdminKey]);

  // Initial load + auto-refresh every 60s while a key is present.
  useEffect(() => {
    if (!adminKey) return;
    load();
    const id = setInterval(load, 60_000);
    return () => clearInterval(id);
  }, [adminKey, load]);

  // ── Admin-key gate ──────────────────────────────────────────────────────
  if (ready && !adminKey) {
    return (
      <main>
        <section className="card" style={{ maxWidth: 480, margin: "0 auto" }}>
          <p className="eyebrow">Founder Command Room</p>
          <h1>غرفة قيادة المؤسس</h1>
          <p className="stat-label" style={{ marginBottom: "var(--sp-3)" }}>
            أدخل مفتاح الأدمن للوصول · Enter your admin key
          </p>
          <input
            type="password"
            value={keyInput}
            onChange={(e) => setKeyInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && setAdminKey(keyInput)}
            placeholder="X-Admin-API-Key"
            style={{
              width: "100%",
              padding: "12px 14px",
              borderRadius: 10,
              border: "1px solid rgba(6,182,212,0.3)",
              background: "rgba(255,255,255,0.04)",
              color: "inherit",
              marginBottom: "var(--sp-4)",
            }}
          />
          <div className="actions">
            <button className="btn btn-primary" onClick={() => setAdminKey(keyInput)}>
              دخول · Enter
            </button>
          </div>
          <p className="stat-label" style={{ marginTop: "var(--sp-4)", opacity: 0.7 }}>
            يُحفظ على جهازك فقط (localStorage) ولا يُرسل إلا لواجهة Dealix.
          </p>
        </section>
      </main>
    );
  }

  const s = data?.summary;
  const paidPct = data
    ? Math.min(100, Math.round((data.launch.paid / data.launch.article13_target) * 100))
    : 0;
  const maxQueue = s ? Math.max(1, ...Object.values(s.queues)) : 1;

  return (
    <main>
      {/* Header */}
      <section style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", flexWrap: "wrap", gap: "var(--sp-4)" }}>
        <div>
          <p className="eyebrow">Founder Command Room</p>
          <h1>غرفة قيادة المؤسس</h1>
          <p className="stat-label">
            كل نواحي الإطلاق التجاري · One live view {lastRefreshed && `· آخر تحديث ${lastRefreshed}`}
          </p>
        </div>
        <div className="actions" style={{ marginTop: 0 }}>
          <button className="btn btn-primary" onClick={load} disabled={loading}>
            {loading ? "تحديث…" : "تحديث · Refresh"}
          </button>
          <button className="btn btn-ghost" onClick={clearAdminKey}>تبديل المفتاح</button>
        </div>
      </section>

      {error && (
        <section className="card" style={{ borderColor: "rgba(239,68,68,0.4)" }}>
          <p style={{ color: "#f87171" }}>{error}</p>
        </section>
      )}

      {!data && loading && (
        <section className="card"><p>جارٍ التحميل… · Loading…</p></section>
      )}

      {data && s && (
        <>
          {/* Launch readiness banner */}
          <section className="card card-cyan" style={{ display: "flex", alignItems: "center", flexWrap: "wrap", gap: "var(--sp-4)" }}>
            <span className={`badge ${data.launch.status === "READY" ? "badge-emerald" : "badge-amber"}`}>
              {data.launch.status === "READY" ? "جاهز للإطلاق · Launch ready" : "جاهزية جزئية · Partial readiness"}
            </span>
            <span style={{ flex: 1, minWidth: 220 }}>
              عملاء مدفوعون نحو البوابة التجارية (Article 13): <b>{data.launch.paid}/{data.launch.article13_target}</b> · Paid customers
            </span>
            <span style={{ flex: "0 0 160px", background: "rgba(255,255,255,0.08)", borderRadius: 8, height: 12, overflow: "hidden", display: "block" }}>
              <span style={{ width: `${paidPct}%`, height: "100%", background: "linear-gradient(90deg,#10B981,#06B6D4)", display: "block" }} />
            </span>
          </section>

          {/* KPI cards */}
          <section className="grid-3">
            <MetricCard value={String(s.revenue.conversations)} label="محادثات · Conversations" />
            <MetricCard value={String(s.revenue.meetings)} label="اجتماعات · Meetings" />
            <MetricCard value={String(s.revenue.scopes)} label="نطاقات · Scopes" />
            <MetricCard value={String(s.revenue.invoices)} label="فواتير · Invoices" />
            <MetricCard value={String(s.revenue.paid)} label="مدفوع · Paid" />
            <MetricCard value={String(s.today.follow_ups_due)} label="متابعات مستحقة · Follow-ups due" />
          </section>

          <section className="grid-2">
            {/* Today's priority actions */}
            <article className="card">
              <h3>إجراءات اليوم · Today&apos;s priority actions</h3>
              {s.top_targets.length === 0 ? (
                <p className="stat-label" style={{ marginTop: "var(--sp-4)" }}>
                  لا أهداف بعد — أضف أول هدف من غرفة الحرب. · No targets yet — add your first in the War Room.
                </p>
              ) : (
                <ul style={{ marginTop: "var(--sp-4)", listStyle: "none", padding: 0 }}>
                  {s.top_targets.slice(0, 10).map((t) => (
                    <li key={t.lead_id} style={{ padding: "10px 0", borderBottom: "1px solid rgba(255,255,255,0.07)" }}>
                      <div style={{ display: "flex", justifyContent: "space-between", gap: 8, alignItems: "center" }}>
                        <b>{t.target}</b>
                        <StageBadge stage={t.stage || t.status} />
                      </div>
                      <div className="stat-label">{t.next_action || "—"}{t.next_action_due ? ` · ${t.next_action_due}` : ""}</div>
                    </li>
                  ))}
                </ul>
              )}
              <div className="actions">
                <a href="/war-room">غرفة الحرب · War Room</a>
                <a href="/operator">لوحة المشغّل · Operator</a>
                <a href="/commercial-intelligence">الذكاء التجاري · Intelligence</a>
              </div>
            </article>

            {/* Queues */}
            <article className="card">
              <h3>الطوابير · Pipeline queues</h3>
              <div style={{ marginTop: "var(--sp-4)" }}>
                {Object.entries(s.queues).map(([k, v]) => (
                  <div key={k} style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 10 }}>
                    <span style={{ flex: "0 0 42%", fontSize: ".88rem" }}>
                      {(QUEUE_LABELS[k]?.ar ?? k)} · {(QUEUE_LABELS[k]?.en ?? k)}
                    </span>
                    <span style={{ flex: 1, background: "rgba(255,255,255,0.08)", borderRadius: 8, height: 16, overflow: "hidden", display: "block" }}>
                      <span style={{ display: "block", height: "100%", width: `${Math.round((v / maxQueue) * 100)}%`, background: "linear-gradient(90deg,#0066FF,#10B981)" }} />
                    </span>
                    <b style={{ flex: "0 0 28px", textAlign: "left" }}>{v}</b>
                  </div>
                ))}
              </div>
            </article>
          </section>

          <section className="grid-2">
            {/* Launch readiness actions */}
            <article className="card">
              <h3>إجراءات الإطلاق العالقة · Pending launch actions</h3>
              <ol style={{ marginTop: "var(--sp-4)", paddingInlineStart: 20 }}>
                {data.launch.founder_actions.map((a, i) => (
                  <li key={i} style={{ marginBottom: 10 }}>
                    <b>{a.ar}</b>
                    <div className="stat-label">{a.en}</div>
                  </li>
                ))}
              </ol>
              {pendingApprovals !== null && (
                <div className="actions">
                  <a href="/approvals">طابور الموافقات · Approvals ({pendingApprovals})</a>
                </div>
              )}
            </article>

            {/* Offer ladder */}
            <article className="card">
              <h3>سلّم العروض · Offer ladder</h3>
              <div style={{ marginTop: "var(--sp-4)" }}>
                {data.offer_ladder.map((o, i) => (
                  <div key={i} style={{ display: "flex", alignItems: "center", gap: 12, padding: "8px 0", borderBottom: "1px solid rgba(255,255,255,0.06)" }}>
                    <span className="badge badge-cyan" style={{ flex: "0 0 28px", justifyContent: "center" }}>{i + 1}</span>
                    <span style={{ flex: 1 }}>{o.name}</span>
                    <span className="stat-label">{o.detail}</span>
                  </div>
                ))}
              </div>
            </article>
          </section>

          {/* Doctrine footer */}
          <section className="card">
            <h3>حدود العقيدة · Doctrine guardrails</h3>
            <div style={{ display: "flex", flexWrap: "wrap", gap: "var(--sp-3)", marginTop: "var(--sp-4)" }}>
              {Object.entries(s.risks).map(([k, ok]) => (
                <span key={k} className={`badge ${ok ? "badge-emerald" : "badge-coral"}`}>
                  {ok ? "✓" : "✗"} {(RISK_LABELS[k]?.ar ?? k)} · {(RISK_LABELS[k]?.en ?? k)}
                </span>
              ))}
            </div>
            <p className="stat-label" style={{ marginTop: "var(--sp-4)" }}>
              وضع القراءة فقط ({data.mode}) — كل المسودات تنتظر موافقتك، لا إرسال تلقائي.
            </p>
          </section>
        </>
      )}
    </main>
  );
}
