const { withSentryConfig } = require("@sentry/nextjs");

const dealixApiBase = (
  process.env.NEXT_PUBLIC_DEALIX_API_BASE ||
  process.env.NEXT_PUBLIC_API_URL ||
  "https://api.dealix.me"
).replace(/\/$/, "");

/** @type {import('next').NextConfig} */
const nextConfig = {
  output: "standalone",
  // Pin tracing to the Next application itself. The repository intentionally
  // contains lockfiles both at the repo root and under apps/web, so leaving
  // tracing-root inference implicit can make a direct VPS build select the
  // repository root and nest the standalone entrypoint. Railway builds this
  // service with apps/web as its build root. __dirname makes both environments
  // resolve the same contract: .next/standalone/server.js -> /app/server.js.
  outputFileTracingRoot: __dirname,
  poweredByHeader: false,
  reactStrictMode: true,
  compress: true,

  // Keep the legacy client variable working while the canonical deployment
  // contract moves to NEXT_PUBLIC_DEALIX_API_BASE.
  env: {
    NEXT_PUBLIC_API_URL: dealixApiBase,
    NEXT_PUBLIC_DEALIX_API_BASE: dealixApiBase,
  },

  // Existing pages that still call relative /api/v1 paths are proxied to the
  // canonical Railway API. Browser Authorization headers remain intact and no
  // platform API key is embedded in the frontend bundle.
  async rewrites() {
    return [
      {
        source: "/api/v1/:path*",
        destination: `${dealixApiBase}/api/v1/:path*`,
      },
    ];
  },

  // Security & performance headers
  async headers() {
    return [
      {
        source: "/:path*",
        headers: [
          { key: "X-DNS-Prefetch-Control", value: "on" },
          { key: "X-Frame-Options", value: "SAMEORIGIN" },
          { key: "X-Content-Type-Options", value: "nosniff" },
          { key: "Referrer-Policy", value: "strict-origin-when-cross-origin" },
          { key: "Permissions-Policy", value: "camera=(), microphone=(), geolocation=()" },
          {
            key: "Strict-Transport-Security",
            value: "max-age=63072000; includeSubDomains; preload",
          },
          {
            key: "Content-Security-Policy",
            value: [
              "default-src 'self'",
              "script-src 'self' 'unsafe-inline' https://fonts.googleapis.com",
              "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://fonts.gstatic.com",
              "font-src 'self' https://fonts.gstatic.com",
              "img-src 'self' data: https:",
              "connect-src 'self' https://api.dealix.me https://us.i.posthog.com",
              "frame-ancestors 'none'",
            ].join("; "),
          },
        ],
      },
      {
        source: "/_next/static/:path*",
        headers: [
          { key: "Cache-Control", value: "public, max-age=31536000, immutable" },
        ],
      },
    ];
  },

  // Canonical Company OS pages. Self-serve /signup is intentionally active;
  // the previous redirect to /book belonged to the older service-only flow.
  async redirects() {
    return [
      { source: "/landing", destination: "/", permanent: true },
      { source: "/ar", destination: "/", permanent: true },
      { source: "/ar/pricing", destination: "/pricing", permanent: true },
      { source: "/ar/offers", destination: "/offers", permanent: true },
      { source: "/ar/p1", destination: "/offers", permanent: true },
      { source: "/ar/p2", destination: "/offers", permanent: true },
      { source: "/ar/p3", destination: "/offers", permanent: true },
      { source: "/ar/diagnostic-sprint", destination: "/offers", permanent: true },
      { source: "/ar/demo", destination: "/book", permanent: true },
      { source: "/ar/intake", destination: "/book", permanent: true },
      { source: "/ar/case-studies", destination: "/cases", permanent: true },
      { source: "/ar/company-os", destination: "/brain", permanent: true },
      { source: "/ar/control-room", destination: "/command-center", permanent: true },
      { source: "/ar/transformation", destination: "/services", permanent: true },
      { source: "/ar/trust", destination: "/safety", permanent: true },
      { source: "/ar/zatca-readiness", destination: "/services", permanent: true },
    ];
  },

  images: {
    formats: ["image/avif", "image/webp"],
    minimumCacheTTL: 86400,
    remotePatterns: [
      { protocol: "https", hostname: "dealix.me" },
      { protocol: "https", hostname: "api.dealix.me" },
    ],
  },

  experimental: {
    optimizeCss: true,
    optimizePackageImports: ["react", "react-dom"],
  },
};

module.exports = withSentryConfig(
  nextConfig,
  {
    silent: true,
    org: process.env.SENTRY_ORG,
    project: process.env.SENTRY_PROJECT,
    authToken: process.env.SENTRY_AUTH_TOKEN,
    disableServerWebpackPlugin: !process.env.SENTRY_DSN && !process.env.NEXT_PUBLIC_SENTRY_DSN,
    disableClientWebpackPlugin: !process.env.SENTRY_DSN && !process.env.NEXT_PUBLIC_SENTRY_DSN,
  },
);
