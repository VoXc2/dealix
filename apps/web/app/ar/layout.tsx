import { redirect } from "next/navigation";

/**
 * Session 23 public-truth gate.
 *
 * The legacy /ar subtree contains retired P1/P2/P3 pricing and proof-like
 * marketing surfaces. Until those routes are rebuilt from the canonical
 * one-product contract, fail closed to the reviewed public Dealix surface.
 */
export default function ArabicTruthGateLayout({
  children: _children,
}: Readonly<{ children: React.ReactNode }>) {
  redirect("https://dealix.me/");
}
