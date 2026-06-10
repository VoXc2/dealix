module.exports = {
  ci: {
    collect: {
      url: [
        "http://localhost:3000/ar/dashboard",
        "http://localhost:3000/ar/pipeline",
        "http://localhost:3000/ar/pricing",
        "http://localhost:3000/ar/trust-center",
        "http://localhost:3000/ar/ops/war-room",
        "http://localhost:3000/ar/partners/dashboard",
      ],
      numberOfRuns: 3,
      settings: {
        preset: "desktop",
        throttling: {
          cpuSlowdownMultiplier: 1,
        },
        screenEmulation: {
          width: 1440,
          height: 900,
        },
      },
    },
    assert: {
      assertions: {
        "categories:performance": ["error", { minScore: 0.85 }],
        "categories:accessibility": ["error", { minScore: 0.90 }],
        "categories:best-practices": ["error", { minScore: 0.90 }],
        "categories:seo": ["error", { minScore: 0.90 }],
        "categories:performance": [
          "warn",
          { minScore: 0.80 },
        ],
        "uses-responsive-images": "warn",
        "uses-webp-images": "warn",
        "csp-xss": "warn",
      },
    },
    upload: {
      target: "filesystem",
      outputDir: "./lighthouse-reports",
      reportFilenamePattern: "lhr-%%DATETIME%%-%%URL%%-%%SITE%%-%%RUN%%-%%SCORE%%",
    },
  },
};
