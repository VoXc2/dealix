/* Dealix Service Activation Console
 * Renders the bilingual service-readiness page from
 * landing/assets/data/service-readiness.json.
 *
 * Source of truth: docs/registry/SERVICE_READINESS_MATRIX.yaml
 * Regenerate JSON: python scripts/export_service_readiness_json.py
 */
(function () {
  "use strict";

  var DATA_URL = "assets/data/service-readiness.json";

  var STATUS_LABELS = {
    live:    { ar: "حيّ",         en: "Live"    },
    pilot:   { ar: "تجربة شريك",  en: "Pilot"   },
    partial: { ar: "قيد الاستكمال", en: "Partial" },
    target:  { ar: "في خارطة الطريق", en: "Target"  },
    blocked: { ar: "محظور",       en: "Blocked" },
    backlog: { ar: "في القائمة",   en: "Backlog" }
  };

  var STATUS_ORDER = ["live", "pilot", "partial", "target", "blocked", "backlog"];

  var STATUS_CTA = {
    live:    { label_ar: "جرّب الآن",                    label_en: "Try it now",         href: "/#pilot" },
    pilot:   { label_ar: "اختبر مع مؤسس Dealix",          label_en: "Pilot with the founder", href: "/#pilot" },
    partial: { label_ar: "شاهد خطة التفعيل",              label_en: "See the activation plan", href: null },
    target:  { label_ar: "في خارطة الطريق",                label_en: "On the roadmap",      href: null },
    blocked: { label_ar: "محظور حتى يزول السبب",          label_en: "Blocked until the cause clears", href: null },
    backlog: { label_ar: "في القائمة",                    label_en: "In the backlog",      href: null }
  };

  function el(tag, attrs, children) {
    var node = document.createElement(tag);
    if (attrs) {
      Object.keys(attrs).forEach(function (k) {
        if (k === "class") node.className = attrs[k];
        else if (k === "text") node.textContent = attrs[k];
        else if (k === "html") node.innerHTML = attrs[k];
        else if (k === "dataset") {
          Object.keys(attrs.dataset).forEach(function (dk) {
            node.dataset[dk] = attrs.dataset[dk];
          });
        } else node.setAttribute(k, attrs[k]);
      });
    }
    (children || []).forEach(function (child) {
      if (child == null) return;
      if (typeof child === "string") node.appendChild(document.createTextNode(child));
      else node.appendChild(child);
    });
    return node;
  }

  function fmtList(items) {
    return (items || []).filter(function (i) { return i != null && i !== ""; });
  }

  function statusBadge(status) {
    var label = (STATUS_LABELS[status] || STATUS_LABELS.target);
    return el("span", { class: "service-card__badge service-card__badge--" + status },
      [label.ar + " · " + label.en]);
  }

  function bundleLabel(bundle, bundles) {
    for (var i = 0; i < bundles.length; i++) {
      if (bundles[i].id === bundle) return bundles[i];
    }
    return { id: bundle, name_ar: bundle, name_en: bundle };
  }

  function renderSection(title, items) {
    if (!items || !items.length) return null;
    var ul = el("ul", { class: "service-card__list" }, items.map(function (it) {
      return el("li", { text: String(it) });
    }));
    return el("div", { class: "service-card__section" }, [
      el("h4", { class: "service-card__h4", text: title }),
      ul
    ]);
  }

  function renderCta(status) {
    var cta = STATUS_CTA[status] || STATUS_CTA.target;
    var attrs = {
      class: "service-card__cta service-card__cta--" + status,
      role: "button"
    };
    if (cta.href) {
      attrs.href = cta.href;
      var a = el("a", attrs, [
        el("span", { class: "service-card__cta-ar", text: cta.label_ar }),
        el("span", { class: "service-card__cta-en", text: " · " + cta.label_en })
      ]);
      return a;
    }
    var span = el("span", { class: attrs.class + " is-disabled", "aria-disabled": "true" }, [
      el("span", { class: "service-card__cta-ar", text: cta.label_ar }),
      el("span", { class: "service-card__cta-en", text: " · " + cta.label_en })
    ]);
    return span;
  }

  function renderCard(svc, bundles) {
    var bundle = bundleLabel(svc.bundle, bundles);
    var card = el("article", {
      class: "service-card service-card--" + svc.status,
      dataset: { status: svc.status, bundle: svc.bundle, sid: svc.service_id }
    });

    var header = el("header", { class: "service-card__header" }, [
      el("div", { class: "service-card__title-block" }, [
        el("h3", { class: "service-card__title", text: svc.name_ar }),
        el("p", { class: "service-card__title-en", text: svc.name_en })
      ]),
      statusBadge(svc.status)
    ]);

    var bundleRow = el("div", { class: "service-card__bundle" }, [
      el("span", { class: "service-card__bundle-ar", text: bundle.name_ar }),
      el("span", { class: "service-card__bundle-en", text: " · " + bundle.name_en })
    ]);

    var value = el("div", { class: "service-card__value" }, [
      el("p", { class: "service-card__value-ar", text: svc.customer_value_ar }),
      el("p", { class: "service-card__value-en", text: svc.customer_value_en })
    ]);

    var sections = [];

    var ready = fmtList(svc.deliverables).concat(fmtList(svc.proof_metrics).map(function (m) {
      return "proof: " + m;
    }));
    var readySection = renderSection("ما هو جاهز · What's ready", ready);
    if (readySection) sections.push(readySection);

    var missing = fmtList(svc.required_inputs).concat(
      (svc.tests_required || []).map(function (t) { return "test: " + t; })
    );
    var missingSection = renderSection("ما الناقص · What's missing", missing);
    if (missingSection) sections.push(missingSection);

    var nextStep = el("div", { class: "service-card__section" }, [
      el("h4", { class: "service-card__h4", text: "خطوة التفعيل التالية · Next activation step" }),
      el("p", { class: "service-card__next-ar", text: svc.next_activation_step_ar || "" }),
      el("p", { class: "service-card__next-en", text: svc.next_activation_step_en || "" })
    ]);
    sections.push(nextStep);

    var safety = renderSection(
      "السلامة · Safety",
      fmtList(svc.safe_action_policy).concat(
        fmtList(svc.blocked_actions).map(function (b) { return "blocked: " + b; })
      )
    );
    if (safety) sections.push(safety);

    var meta = el("div", { class: "service-card__meta" }, [
      el("span", { class: "service-card__meta-item", text: "SLA: " + (svc.sla || "—") }),
      el("span", { class: "service-card__meta-item",
        text: "approval: " + (svc.approval_required ? "required" : "not required") }),
      el("span", { class: "service-card__meta-item",
        text: "verified: " + (svc.last_verified_at || "—") })
    ]);

    var footer = el("footer", { class: "service-card__footer" }, [renderCta(svc.status)]);

    card.appendChild(header);
    card.appendChild(bundleRow);
    card.appendChild(value);
    sections.forEach(function (s) { card.appendChild(s); });
    card.appendChild(meta);
    card.appendChild(footer);
    return card;
  }

  function statusRank(status) {
    var idx = STATUS_ORDER.indexOf(status);
    return idx === -1 ? 999 : idx;
  }

  function buildFilterBar(payload, onChange) {
    var bar = el("div", { class: "service-filter-bar" });

    var statusGroup = el("div", { class: "service-filter-group" }, [
      el("span", { class: "service-filter-group__label", text: "الحالة · Status" })
    ]);
    var statuses = ["all"].concat(STATUS_ORDER);
    statuses.forEach(function (s) {
      var label;
      if (s === "all") label = "الكل · All";
      else label = (STATUS_LABELS[s].ar + " · " + STATUS_LABELS[s].en);
      var chip = el("button", {
        class: "service-filter-chip" + (s === "all" ? " is-active" : ""),
        type: "button",
        dataset: { filterType: "status", filterValue: s },
        text: label
      });
      statusGroup.appendChild(chip);
    });

    var bundleGroup = el("div", { class: "service-filter-group" }, [
      el("span", { class: "service-filter-group__label", text: "الباقة · Bundle" })
    ]);
    var bundles = [{ id: "all", name_ar: "الكل", name_en: "All" }].concat(payload.bundles);
    bundles.forEach(function (b) {
      var chip = el("button", {
        class: "service-filter-chip" + (b.id === "all" ? " is-active" : ""),
        type: "button",
        dataset: { filterType: "bundle", filterValue: b.id },
        text: b.name_ar + " · " + b.name_en
      });
      bundleGroup.appendChild(chip);
    });

    bar.appendChild(statusGroup);
    bar.appendChild(bundleGroup);
    bar.addEventListener("click", function (e) {
      var target = e.target;
      if (!target || !target.dataset || !target.dataset.filterType) return;
      var group = target.parentNode;
      Array.prototype.slice.call(group.querySelectorAll(".service-filter-chip"))
        .forEach(function (c) { c.classList.remove("is-active"); });
      target.classList.add("is-active");
      onChange(currentFilters(bar));
    });
    return bar;
  }

  function currentFilters(bar) {
    var status = bar.querySelector('[data-filter-type="status"].is-active');
    var bundle = bar.querySelector('[data-filter-type="bundle"].is-active');
    return {
      status: status ? status.dataset.filterValue : "all",
      bundle: bundle ? bundle.dataset.filterValue : "all"
    };
  }

  function applyFilters(services, filters) {
    return services.filter(function (s) {
      if (filters.status !== "all" && s.status !== filters.status) return false;
      if (filters.bundle !== "all" && s.bundle !== filters.bundle) return false;
      return true;
    });
  }

  function groupByBundle(services, bundles) {
    var groups = {};
    bundles.forEach(function (b) { groups[b.id] = []; });
    services.forEach(function (s) {
      if (!groups[s.bundle]) groups[s.bundle] = [];
      groups[s.bundle].push(s);
    });
    Object.keys(groups).forEach(function (bid) {
      groups[bid].sort(function (a, b) {
        var d = statusRank(a.status) - statusRank(b.status);
        if (d !== 0) return d;
        return (a.name_en || "").localeCompare(b.name_en || "");
      });
    });
    return groups;
  }

  function renderGrid(payload, mount, filters) {
    mount.innerHTML = "";
    var filtered = applyFilters(payload.services, filters);
    if (!filtered.length) {
      mount.appendChild(el("div", { class: "service-empty" }, [
        el("p", { text: "لا توجد خدمات بهذا الفلتر." }),
        el("p", { text: "No services match this filter." })
      ]));
      return;
    }
    var groups = groupByBundle(filtered, payload.bundles);
    payload.bundles.forEach(function (bundle) {
      var list = groups[bundle.id] || [];
      if (!list.length) return;
      var section = el("section", {
        class: "service-bundle-section",
        dataset: { bundle: bundle.id }
      });
      var head = el("header", { class: "service-bundle-section__header" }, [
        el("h2", { class: "service-bundle-section__title", text: bundle.name_ar }),
        el("p", { class: "service-bundle-section__title-en", text: bundle.name_en }),
        bundle.summary_ar ? el("p", { class: "service-bundle-section__summary", text: bundle.summary_ar }) : null,
        bundle.summary_en ? el("p", { class: "service-bundle-section__summary-en", text: bundle.summary_en }) : null
      ]);
      var grid = el("div", { class: "service-card-grid" });
      list.forEach(function (svc) { grid.appendChild(renderCard(svc, payload.bundles)); });
      section.appendChild(head);
      section.appendChild(grid);
      mount.appendChild(section);
    });
  }

  function renderCounts(payload, container) {
    if (!container) return;
    var c = payload.counts || {};
    var rows = [
      { label_ar: "حيّ",            label_en: "Live",    value: c.live    || 0, mod: "live" },
      { label_ar: "تجربة شريك",      label_en: "Pilot",   value: c.pilot   || 0, mod: "pilot" },
      { label_ar: "قيد الاستكمال",   label_en: "Partial", value: c.partial || 0, mod: "partial" },
      { label_ar: "في خارطة الطريق", label_en: "Target",  value: c.target  || 0, mod: "target" },
      { label_ar: "محظور",          label_en: "Blocked", value: c.blocked || 0, mod: "blocked" },
      { label_ar: "إجمالي الخدمات",  label_en: "Total",   value: c.total   || 0, mod: "total" }
    ];
    container.innerHTML = "";
    rows.forEach(function (r) {
      container.appendChild(el("div", { class: "status-sum-card status-sum-card--" + r.mod }, [
        el("div", { class: "status-sum-card__num", text: String(r.value) }),
        el("div", { class: "status-sum-card__label", text: r.label_ar + " · " + r.label_en })
      ]));
    });
  }

  function renderError(mount, message) {
    mount.innerHTML = "";
    mount.appendChild(el("div", { class: "service-error" }, [
      el("p", { text: message || "تعذّر تحميل مصفوفة الخدمات." }),
      el("p", { text: "Could not load the service readiness matrix." }),
      el("p", { class: "service-error__source",
        text: "المصدر · Source: docs/registry/SERVICE_READINESS_MATRIX.yaml" })
    ]));
  }

  function init() {
    var mount = document.getElementById("services-mount");
    var filterMount = document.getElementById("services-filter-mount");
    var countsMount = document.getElementById("services-counts-mount");
    if (!mount) return;

    fetch(DATA_URL, { cache: "no-cache" })
      .then(function (r) {
        if (!r.ok) throw new Error("HTTP " + r.status);
        return r.json();
      })
      .then(function (payload) {
        if (!payload || !payload.services) {
          renderError(mount);
          return;
        }
        renderCounts(payload, countsMount);
        var filters = { status: "all", bundle: "all" };
        if (filterMount) {
          var bar = buildFilterBar(payload, function (f) {
            filters = f;
            renderGrid(payload, mount, filters);
          });
          filterMount.innerHTML = "";
          filterMount.appendChild(bar);
        }
        renderGrid(payload, mount, filters);

        var lu = document.getElementById("services-last-updated");
        if (lu && payload.last_updated) lu.textContent = payload.last_updated;
      })
      .catch(function () { renderError(mount); });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }

  // Export for tests/inspection
  if (typeof window !== "undefined") {
    window.DealixServiceConsole = {
      renderGrid: renderGrid,
      renderCard: renderCard,
      renderCounts: renderCounts,
      applyFilters: applyFilters,
      STATUS_LABELS: STATUS_LABELS,
      STATUS_ORDER: STATUS_ORDER,
      STATUS_CTA: STATUS_CTA
    };
  }
})();
