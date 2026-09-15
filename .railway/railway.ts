import { defineRailway, github, postgres, preserve, project, service, volume } from "railway/iac";

export default defineRailway(() => {
  const Postgres = postgres("Postgres", { region: "us-west2" });
  Postgres.networking = { privateNetworkEndpoint: "postgres", tcpProxies: { "5432": {} } };
  const postgresVolume = volume("postgres-volume", { alerts: { usage: { "100": {}, "80": {}, "95": {} } }, allowOnlineResize: true, region: "us-west2", sizeMB: 5000 });
  const dealix = service("dealix", {
    source: github("Dealix-sa/dealix", { checkSuites: true, rootDirectory: "." }),
    build: { buildEnvironment: "V3", builder: "DOCKERFILE", dockerfilePath: "Dockerfile", watchPatterns: ["/*.py", "/**/*.py", "/Dockerfile", "/railway.json", "/pyproject.toml", "/requirements*.txt", "/scripts/railway_predeploy.sh", "/api/**", "/app/**", "/db/**", "/dealix/**", "/alembic/**", "/alembic.ini", "/config/**", "/templates/**", "/prompts/**"] },
    start: "",
    healthcheck: "/healthz",
    healthcheckTimeout: 300,
    preDeploy: "if [ -f /app/scripts/railway_predeploy.sh ]; then bash /app/scripts/railway_predeploy.sh; else echo 'RAILWAY_PREDEPLOY: no predeploy script'; fi",
    replicas: { "us-west2": 1 },
    deploy: { restartPolicyMaxRetries: 3 },
    domains: ["api.dealix.me"],
    env: { ADMIN_API_KEYS: preserve(), API_KEYS: preserve(), APP_ENV: preserve(), APP_SECRET_KEY: preserve(), APP_URL: preserve(), BASE_URL: preserve(), CALENDLY_URL: preserve(), CALENDLY_WEBHOOK_SECRET: preserve(), CORS_ORIGINS: preserve(), CUSTOMER_PORTAL_SECRET: preserve(), DATABASE_URL: preserve(), DEALIX_ADMIN_API_KEY: preserve(), DEALIX_API_BASE: preserve(), EMAIL_DAILY_LIMIT: preserve(), ENVIRONMENT: preserve(), GIT_SHA: preserve(), GOOGLE_SEARCH_API_KEY: preserve(), GOOGLE_SEARCH_CX: preserve(), GREEN_API_INSTANCE_ID: preserve(), GREEN_API_TOKEN: preserve(), GROQ_API_KEY: preserve(), HUBSPOT_ACCESS_TOKEN: preserve(), JWT_SECRET_KEY: preserve(), MOYASAR_SECRET_KEY: preserve(), OPENAI_API_KEY: preserve(), POSTHOG_HOST: preserve(), RAILWAY_TOKEN: preserve(), RUN_RAILWAY_PRE_DEPLOY_MIGRATE: preserve(), SMTP_PASSWORD: preserve(), SMTP_USER: preserve(), VOICE_AI_ENABLED: preserve(), VOICE_AI_MAX_OUTPUT_TOKENS: preserve(), VOICE_AI_REASONING_EFFORT: preserve(), VOICE_AI_TRACING_ENABLED: preserve(), VOICE_OUTBOUND_ENABLED: preserve(), VOICE_RECORDING_ENABLED: preserve(), WHATSAPP_ALLOW_LIVE_SEND: preserve(), WHATSAPP_DAILY_LIMIT: preserve(), WHATSAPP_MOCK_MODE: preserve() },
  });
  const web = service("web", {
    source: github("Dealix-sa/dealix", { checkSuites: true, rootDirectory: "apps/web" }),
    build: { buildEnvironment: "V3", builder: "DOCKERFILE", dockerfilePath: "Dockerfile" },
    healthcheck: "/healthz",
    healthcheckTimeout: 300,
    replicas: { "us-west2": 1 },
    deploy: { restartPolicyMaxRetries: 3 },
    domains: ["dealix.me", "www.dealix.me"],
    env: { DEALIX_DEPLOY_NONCE: preserve() },
  });

  return project("Dealix", {
    resources: [dealix, web, Postgres, postgresVolume],
  });
});
