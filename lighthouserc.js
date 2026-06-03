// Lighthouse CI config — Track D4 of 30-day plan.
// Runs against 10 highest-impact Tier-1 pages.
// Score thresholds: 75 in May-Jun 2026 (ramp-up), 85 by Wave 4, 90 thereafter.
// Plan: /root/.claude/plans/vivid-baking-quokka.md

module.exports = {
  ci: {
    collect: {
      // Built by GitHub Actions: python3 -m http.server 8765 inside landing/
      url: [
        "http://localhost:8765/",
        "http://localhost:8765/pricing.html",
        "http://localhost:8765/customer-portal.html",
        "http://localhost:8765/proof.html",
        "http://localhost:8765/trust-center.html",
        "http://localhost:8765/diagnostic.html",
        "http://localhost:8765/agency-partner.html",
        "http://localhost:8765/checkout.html?tier=sprint",
        "http://localhost:8765/customer-decisions.html",
        "http://localhost:8765/login.html",
      ],
      numberOfRuns: 1,
      settings: {
        // Mobile-first per Tier-1 research (58% of pricing traffic mobile)
        preset: "desktop", // run desktop + mobile separately if needed
        chromeFlags: "--no-sandbox --headless",
      },
    },
    assert: {
      preset: "lighthouse:no-pwa",
      assertions: {
        "categories:performance":      ["warn", { minScore: 0.75 }],
        "categories:accessibility":    ["error", { minScore: 0.85 }],
        "categories:best-practices":   ["warn", { minScore: 0.80 }],
        "categories:seo":              ["error", { minScore: 0.85 }],
        // Hard-fail on a11y critical
        "color-contrast":              ["error", { minScore: 1 }],
        "image-alt":                   ["error", { minScore: 1 }],
        "link-name":                   ["error", { minScore: 1 }],
        "html-has-lang":               ["error", { minScore: 1 }],
        "html-lang-valid":             ["error", { minScore: 1 }],
        // Soft-fail on perf during ramp-up
        "first-contentful-paint":      ["warn", { maxNumericValue: 2500 }],
        "largest-contentful-paint":    ["warn", { maxNumericValue: 4000 }],
        "cumulative-layout-shift":     ["warn", { maxNumericValue: 0.1 }],
      },
    },
    upload: {
      target: "temporary-public-storage",
    },
  },
};
