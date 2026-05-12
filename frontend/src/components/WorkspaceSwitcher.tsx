"use client";

/**
 * Workspace switcher — for users (typically agency partners) who
 * belong to multiple tenants. Reads the list from localStorage
 * `dealix_workspaces` (the auth flow pushes one entry per login).
 *
 * Selecting a workspace replaces `dealix_user.tenant_id` and reloads.
 */

import { useEffect, useState } from "react";
import { useLocale } from "next-intl";

type Workspace = { tenant_id: string; name: string; plan?: string };

export function WorkspaceSwitcher(): JSX.Element | null {
  const locale = useLocale();
  const isAr = locale === "ar";
  const [workspaces, setWorkspaces] = useState<Workspace[]>([]);
  const [current, setCurrent] = useState<string | null>(null);
  const [open, setOpen] = useState(false);

  useEffect(() => {
    try {
      const raw = localStorage.getItem("dealix_workspaces");
      if (raw) setWorkspaces(JSON.parse(raw));
      const user = localStorage.getItem("dealix_user");
      if (user) setCurrent(JSON.parse(user).tenant_id);
    } catch {
      /* ignore */
    }
  }, []);

  function pick(ws: Workspace) {
    try {
      const raw = localStorage.getItem("dealix_user");
      const user = raw ? JSON.parse(raw) : {};
      user.tenant_id = ws.tenant_id;
      user.tenant_name = ws.name;
      localStorage.setItem("dealix_user", JSON.stringify(user));
      window.location.reload();
    } catch {
      /* ignore */
    }
  }

  if (workspaces.length < 2) return null;

  const active = workspaces.find((w) => w.tenant_id === current);
  return (
    <div className="relative">
      <button
        onClick={() => setOpen((v) => !v)}
        className="text-sm px-3 py-1.5 rounded-lg border border-border hover:bg-muted flex items-center gap-2"
      >
        <span className="font-medium">{active?.name ?? "Workspace"}</span>
        <span className="text-muted-foreground">▾</span>
      </button>
      {open && (
        <div className="absolute mt-2 right-0 w-64 bg-card border border-border rounded-lg shadow-lg p-2 z-50">
          <div className="text-xs text-muted-foreground px-2 py-1">
            {isAr ? "غيّر مساحة العمل" : "Switch workspace"}
          </div>
          {workspaces.map((w) => (
            <button
              key={w.tenant_id}
              onClick={() => pick(w)}
              className={`block w-full text-left px-2 py-1.5 rounded text-sm hover:bg-muted ${
                w.tenant_id === current ? "bg-emerald-500/10" : ""
              }`}
            >
              <div className="font-medium">{w.name}</div>
              <div className="text-xs text-muted-foreground">
                {w.plan ?? "—"} · <code>{w.tenant_id}</code>
              </div>
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
