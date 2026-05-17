import Link from "next/link";

interface PortalPlaceholderProps {
  portal: string;
  title: string;
  subtitle: string;
  phase: string;
  phaseLabel: string;
  scopeLabel: string;
  scope: string[];
  backHref?: string;
  backLabel?: string;
}

/**
 * Route skeleton for the Full Ops 5-portal architecture. Each portal route is
 * real and navigable; business UI lands in its scheduled V-phase.
 */
export function PortalPlaceholder({
  portal,
  title,
  subtitle,
  phase,
  phaseLabel,
  scopeLabel,
  scope,
  backHref,
  backLabel,
}: PortalPlaceholderProps) {
  return (
    <div className="min-h-screen bg-background grid-pattern flex items-center justify-center p-6">
      <div className="w-full max-w-xl rounded-2xl border border-border bg-card/60 p-8">
        <p className="text-xs font-mono uppercase tracking-widest text-gold-500">
          {portal}
        </p>
        <h1 className="mt-2 font-display text-2xl font-semibold">{title}</h1>
        <p className="mt-2 text-sm text-muted-foreground">{subtitle}</p>

        <div className="mt-6 inline-flex items-center gap-2 rounded-full border border-gold-500/40 bg-gold-500/10 px-3 py-1">
          <span className="text-xs font-mono text-gold-500">{phase}</span>
          <span className="text-xs text-muted-foreground">{phaseLabel}</span>
        </div>

        <div className="mt-6">
          <p className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
            {scopeLabel}
          </p>
          <ul className="mt-2 space-y-1">
            {scope.map((item) => (
              <li key={item} className="text-sm text-foreground/80">
                — {item}
              </li>
            ))}
          </ul>
        </div>

        {backHref && backLabel && (
          <Link
            href={backHref}
            className="mt-8 inline-block text-sm text-gold-500 hover:underline"
          >
            ← {backLabel}
          </Link>
        )}
      </div>
    </div>
  );
}
