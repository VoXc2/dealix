import type { ReactNode } from "react";

interface DiagnosticLayoutProps {
  children: ReactNode;
}

export default function DiagnosticLayout({ children }: DiagnosticLayoutProps) {
  return (
    <div className="min-h-screen bg-background">{children}</div>
  );
}
