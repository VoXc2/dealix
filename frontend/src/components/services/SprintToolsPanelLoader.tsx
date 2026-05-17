"use client";

import dynamic from "next/dynamic";

const SprintToolsPanel = dynamic(
  () => import("@/components/services/SprintToolsPanel"),
  { ssr: false },
);

export function SprintToolsPanelLoader({ locale }: { locale: string }) {
  return <SprintToolsPanel locale={locale} />;
}
