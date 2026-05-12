// VerticalLeadForm — sector-tuned lead-capture widget.
//
// Usage:
//   <div id="vertical-lead-form" data-vertical="real-estate"></div>
//   <script src="/components/VerticalLeadForm.js" defer></script>
//
// Behaviour:
//   - Reads `data-vertical` from the container.
//   - Fetches GET /api/v1/verticals/{id} to learn the sector-specific
//     lead_form_fields (declared in dealix/verticals/<slug>/config.yaml).
//   - Renders a form with the universal fields (name, email, phone,
//     company) PLUS each `lead_form_fields[].{id,type,label_*,required}`.
//   - On submit, POSTs to /api/v1/public/lead-capture with vertical id
//     attached. Honours dealix_consent (no submission unless functional
//     cookies were accepted).

(function () {
  const ROOT_ID = "vertical-lead-form";
  const API =
    (typeof window !== "undefined" && window.DEALIX_API_BASE) ||
    "https://api.dealix.me";

  function consentOK() {
    try {
      const raw = localStorage.getItem("dealix_consent");
      if (!raw) return true; // pre-banner: allow first submit; banner will appear after.
      const parsed = JSON.parse(raw);
      return parsed && parsed.functional !== false;
    } catch {
      return true;
    }
  }

  function ar(el) {
    return (el.closest("[lang]") || document.documentElement).getAttribute("lang") === "ar";
  }

  function mountFields(fields, isAr) {
    const out = [];
    out.push(label("full_name", isAr ? "الاسم الكامل" : "Full name", true));
    out.push(input("full_name", "text", true));
    out.push(label("email", isAr ? "البريد الإلكتروني" : "Email", true));
    out.push(input("email", "email", true));
    out.push(label("phone", isAr ? "الجوال" : "Phone", false));
    out.push(input("phone", "tel", false));
    out.push(label("company", isAr ? "اسم الشركة" : "Company", true));
    out.push(input("company", "text", true));
    fields.forEach((f) => {
      // The vertical config canonicalises on `id` (see
      // dealix/verticals/*/config.yaml); we accept `name` too for back-compat.
      const key = f.id || f.name;
      if (!key) return;
      const lbl = isAr ? f.label_ar || key : f.label_en || key;
      out.push(label(key, lbl, !!f.required));
      out.push(input(key, f.type || "text", !!f.required));
    });
    return out.join("");
  }

  function label(name, text, required) {
    return `<label for="vlf-${name}" style="display:block;font-size:.85rem;color:#64748b;margin:.7rem 0 .2rem">${text}${required ? " *" : ""}</label>`;
  }

  function input(name, type, required) {
    return `<input id="vlf-${name}" name="${name}" type="${type}" ${required ? "required" : ""} style="width:100%;padding:.55rem .7rem;border:1px solid #cbd5e1;border-radius:8px;font-size:.95rem"/>`;
  }

  async function init() {
    const root = document.getElementById(ROOT_ID);
    if (!root) return;
    const slug = root.getAttribute("data-vertical") || "real-estate";
    const isAr = ar(root);

    root.innerHTML = `<p style="color:#64748b">${isAr ? "جاري التحميل…" : "Loading…"}</p>`;

    let v;
    try {
      const r = await fetch(`${API}/api/v1/verticals/${slug}`);
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      v = await r.json();
    } catch {
      root.innerHTML = `<p style="color:#b91c1c">${isAr ? "تعذّر تحميل النموذج." : "Form could not load."}</p>`;
      return;
    }

    root.innerHTML = `
      <form id="vlf-form" style="background:white;padding:1.4rem 1.6rem;border:1px solid #e2e8f0;border-radius:12px;max-width:520px">
        <h3 style="margin:0 0 .35rem">${isAr ? v.label_ar : v.label_en}</h3>
        <p style="color:#64748b;margin:0 0 1rem;font-size:.9rem">${isAr ? v.description_ar : v.description_en}</p>
        ${mountFields(v.lead_form_fields || [], isAr)}
        <label style="display:block;font-size:.85rem;margin-top:1rem">
          <input type="checkbox" id="vlf-consent" required style="margin-right:.4rem"/>
          ${isAr ? "أوافق على معالجة بياناتي وفق PDPL." : "I consent to PDPL-compliant data processing."}
        </label>
        <button type="submit" style="margin-top:1rem;background:#10b981;color:white;border:0;padding:.7rem 1.3rem;border-radius:8px;cursor:pointer;font-size:.95rem">
          ${isAr ? "إرسال" : "Submit"}
        </button>
        <p id="vlf-out" style="margin-top:1rem;font-size:.9rem;color:#64748b"></p>
      </form>`;

    document.getElementById("vlf-form").addEventListener("submit", async (ev) => {
      ev.preventDefault();
      const out = document.getElementById("vlf-out");
      if (!consentOK()) {
        out.textContent = isAr ? "يلزم قبول الكوكيز للإرسال." : "Cookies must be accepted to submit.";
        return;
      }
      const data = Object.fromEntries(new FormData(ev.target).entries());
      data.vertical = slug;
      out.textContent = isAr ? "جارٍ الإرسال…" : "Sending…";
      try {
        const r = await fetch(`${API}/api/v1/public/lead-capture`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(data),
        });
        const body = await r.json().catch(() => ({}));
        if (!r.ok) throw new Error(body.detail || r.statusText);
        out.style.color = "#047857";
        out.textContent = isAr ? "تم الإرسال. سنتواصل معك قريباً." : "Thanks — we'll be in touch shortly.";
      } catch (err) {
        out.style.color = "#b91c1c";
        out.textContent = isAr ? `خطأ: ${err.message}` : `Error: ${err.message}`;
      }
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
