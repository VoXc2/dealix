import * as Sentry from "@sentry/nextjs";

const dsn = process.env.NEXT_PUBLIC_SENTRY_DSN?.trim();

if (dsn) {
  const configuredRate = Number(process.env.NEXT_PUBLIC_SENTRY_TRACES_SAMPLE_RATE ?? 0.1);
  Sentry.init({
    dsn,
    tracesSampleRate: Number.isFinite(configuredRate) ? configuredRate : 0.1,
    environment: process.env.NEXT_PUBLIC_SENTRY_ENVIRONMENT ?? process.env.NODE_ENV ?? "development",
    denyUrls: [/localhost/, /127\.0\.0\.1/],
  });
}

export const onRouterTransitionStart = Sentry.captureRouterTransitionStart;
