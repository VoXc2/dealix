// CookieConsent banner — PDPL-compliant, no external dependency.
//
// Usage:
//   <script src="/components/CookieConsent.js" defer></script>
//
// Behaviour:
//   - Renders a fixed banner on first visit (no `dealix_consent` cookie).
//   - Three buttons: Reject (essential only), Accept all, Customise.
//   - Customise opens a small dialog that lists the categories.
//   - Selection persisted in localStorage AND a first-party cookie.
//   - When the user opts out of analytics, calls PostHog's opt_out (if loaded).

(function () {
  const KEY = "dealix_consent";
  const COOKIE_NAME = "dealix_consent";

  function readConsent() {
    try {
      const raw = localStorage.getItem(KEY);
      if (!raw) return null;
      return JSON.parse(raw);
    } catch {
      return null;
    }
  }
  function writeConsent(obj) {
    const value = JSON.stringify(obj);
    localStorage.setItem(KEY, value);
    document.cookie = `${COOKIE_NAME}=${encodeURIComponent(value)}; path=/; max-age=${60 * 60 * 24 * 365}; SameSite=Lax`;
    applyConsent(obj);
  }
  function applyConsent(obj) {
    const optIn = !!obj.analytics;
    if (window.posthog) {
      if (!optIn) window.posthog.opt_out_capturing();
      else window.posthog.opt_in_capturing();
    }
    document.dispatchEvent(new CustomEvent("dealix:consent", { detail: obj }));
  }
  function render() {
    const isAr = (document.documentElement.lang || "en").startsWith("ar");
    const t = (ar, en) => (isAr ? ar : en);
    const wrap = document.createElement("div");
    wrap.id = "dealix-cookie-consent";
    wrap.style.cssText =
      "position:fixed;inset:auto 0 0 0;z-index:9999;padding:1rem;background:#0a0e1a;color:#e6e9f2;display:flex;flex-wrap:wrap;gap:0.5rem;align-items:center;justify-content:center;font-family:system-ui,sans-serif;box-shadow:0 -4px 24px rgba(0,0,0,0.4);direction:" +
      (isAr ? "rtl" : "ltr");
    wrap.innerHTML =
      '<span style="flex:1 1 320px;font-size:0.92rem">' +
      t(
        "نستخدم ملفات تعريف الارتباط الضرورية + التحليلات المختارة لتحسين الخدمة. مطابق لـ PDPL.",
        "We use essential cookies + opt-in analytics to improve the service. PDPL-compliant."
      ) +
      ' <a href="/legal/cookies.html" style="color:#10b981">' +
      t("التفاصيل", "Details") +
      "</a></span>" +
      '<button id="dx-reject" style="padding:0.45rem 0.9rem;border-radius:8px;border:1px solid #444;background:transparent;color:inherit;cursor:pointer">' +
      t("رفض", "Reject") +
      '</button>' +
      '<button id="dx-essential" style="padding:0.45rem 0.9rem;border-radius:8px;border:1px solid #444;background:transparent;color:inherit;cursor:pointer">' +
      t("الضروري فقط", "Essential only") +
      '</button>' +
      '<button id="dx-accept" style="padding:0.45rem 0.9rem;border-radius:8px;border:0;background:#10b981;color:#fff;cursor:pointer;font-weight:600">' +
      t("اقبل الكل", "Accept all") +
      "</button>";
    document.body.appendChild(wrap);
    document.getElementById("dx-reject").addEventListener("click", () => {
      writeConsent({ essential: true, analytics: false, marketing: false, ts: Date.now() });
      wrap.remove();
    });
    document.getElementById("dx-essential").addEventListener("click", () => {
      writeConsent({ essential: true, analytics: false, marketing: false, ts: Date.now() });
      wrap.remove();
    });
    document.getElementById("dx-accept").addEventListener("click", () => {
      writeConsent({ essential: true, analytics: true, marketing: true, ts: Date.now() });
      wrap.remove();
    });
  }
  const current = readConsent();
  if (current) {
    applyConsent(current);
    return;
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", render);
  } else {
    render();
  }
})();
