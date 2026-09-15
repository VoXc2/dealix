import * as Sentry from "@sentry/nextjs";

function sampleRate(value: string | undefined, fallback = 0.1): number {
  if (!value) return fallback;
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : fallback;
}

export async function register() {
  if (process.env.NEXT_RUNTIME === "nodejs") {
    const dsn = process.env.SENTRY_DSN?.trim();
    if (dsn) {
      Sentry.init({
        dsn,
        tracesSampleRate: sampleRate(process.env.SENTRY_TRACES_SAMPLE_RATE),
        environment: process.env.SENTRY_ENVIRONMENT ?? process.env.NODE_ENV ?? "development",
      });
    }
  }

  if (process.env.NEXT_RUNTIME === "edge") {
    const dsn = process.env.NEXT_PUBLIC_SENTRY_DSN?.trim();
    if (dsn) {
      Sentry.init({
        dsn,
        tracesSampleRate: sampleRate(process.env.NEXT_PUBLIC_SENTRY_TRACES_SAMPLE_RATE),
        environment: process.env.NEXT_PUBLIC_SENTRY_ENVIRONMENT ?? process.env.NODE_ENV ?? "development",
      });
    }
  }
}

export const onRequestError = Sentry.captureRequestError;
