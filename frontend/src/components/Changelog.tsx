"use client";

/**
 * In-app changelog popover. Pulls the latest entries from /CHANGELOG.md
 * (served by the FE host as a static asset) and surfaces a "new" badge
 * in the header until the user dismisses it. Dismissals are stored in
 * localStorage per user.
 */

import { useEffect, useState } from "react";
import { useLocale } from "next-intl";

const DISMISS_KEY = "dealix_changelog_seen_sha";

type Entry = { title: string; date: string; body: string };

function parseChangelog(md: string): Entry[] {
  // Naive markdown parser — splits on H2 (## v...) blocks.
  const out: Entry[] = [];
  const lines = md.split(/\r?\n/);
  let current: Entry | null = null;
  for (const line of lines) {
    const m = line.match(/^##\s+(.+)$/);
    if (m) {
      if (current) out.push(current);
      const dateMatch = m[1].match(/(\d{4}-\d{2}-\d{2})/);
      current = {
        title: m[1].replace(/\s*\(?\d{4}-\d{2}-\d{2}\)?\s*/, "").trim(),
        date: dateMatch?.[1] ?? "",
        body: "",
      };
    } else if (current) {
      current.body += line + "\n";
    }
  }
  if (current) out.push(current);
  return out.slice(0, 8);
}

async function sha256Hex(text: string): Promise<string> {
  if (typeof window === "undefined" || !window.crypto?.subtle) return text.slice(0, 32);
  const buf = await window.crypto.subtle.digest(
    "SHA-256",
    new TextEncoder().encode(text)
  );
  return Array.from(new Uint8Array(buf))
    .map((b) => b.toString(16).padStart(2, "0"))
    .join("");
}

export function Changelog(): JSX.Element | null {
  const locale = useLocale();
  const isAr = locale === "ar";
  const [entries, setEntries] = useState<Entry[]>([]);
  const [open, setOpen] = useState(false);
  const [unread, setUnread] = useState(false);

  useEffect(() => {
    fetch("/CHANGELOG.md")
      .then(async (r) => (r.ok ? r.text() : ""))
      .then(async (md) => {
        if (!md) return;
        const items = parseChangelog(md);
        setEntries(items);
        const top = items[0];
        if (!top) return;
        const sha = await sha256Hex(top.title + top.date);
        const seen = localStorage.getItem(DISMISS_KEY);
        setUnread(seen !== sha);
        if (seen !== sha && !open) {
          // do not auto-open; just badge.
        }
      })
      .catch(() => {});
  }, [open]);

  async function ack() {
    if (entries.length) {
      const sha = await sha256Hex(entries[0].title + entries[0].date);
      localStorage.setItem(DISMISS_KEY, sha);
    }
    setUnread(false);
    setOpen(false);
  }

  return (
    <div className="relative">
      <button
        onClick={() => setOpen((v) => !v)}
        className="text-sm px-2 py-1 rounded hover:bg-muted relative"
        aria-label={isAr ? "ما الجديد" : "What's new"}
      >
        {isAr ? "ما الجديد" : "What's new"}
        {unread && (
          <span className="absolute -top-1 -right-1 inline-block w-2 h-2 bg-emerald-500 rounded-full" />
        )}
      </button>
      {open && (
        <div className="absolute z-50 mt-2 right-0 w-96 max-h-[480px] overflow-auto bg-card border border-border rounded-xl shadow-lg p-4">
          <h3 className="font-semibold mb-2">
            {isAr ? "آخر التحديثات" : "Latest updates"}
          </h3>
          {entries.length === 0 ? (
            <p className="text-sm text-muted-foreground">
              {isAr ? "لا تحديثات بعد." : "Nothing yet."}
            </p>
          ) : (
            <ul className="space-y-3">
              {entries.map((e, i) => (
                <li key={i} className="text-sm">
                  <div className="font-medium">{e.title}</div>
                  <div className="text-xs text-muted-foreground">{e.date}</div>
                  <p className="mt-1 whitespace-pre-line">{e.body.trim().slice(0, 300)}</p>
                </li>
              ))}
            </ul>
          )}
          <div className="mt-3 text-right">
            <button onClick={ack} className="text-xs underline">
              {isAr ? "تم القراءة" : "Mark as read"}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
