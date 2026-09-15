import { redirect } from "next/navigation";

export default function ValueEnginePage() {
  // Retired public demo: synthetic ROI examples are not customer proof or
  // commercial authority. Canonical public proof methodology lives at /cases.
  redirect("/cases");
}
