import { permanentRedirect } from "next/navigation";

export const metadata = { title: "Agents — Dealix" };

export default function AgentsPage() {
  permanentRedirect("/dealix-os");
}
