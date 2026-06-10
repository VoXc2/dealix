"use client";

import { useState, useEffect, useCallback, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Search, Command, ArrowRight, ArrowLeft } from "lucide-react";
import { useLocale } from "next-intl";
import { useRouter } from "next/navigation";
import type { Route } from "next";
import { cn } from "@/lib/utils";
import { COMMANDS, registerCommandActions, searchCommands, type Command } from "@/lib/commands/registry";

interface CommandPaletteProps {
  open?: boolean;
  onOpenChange?: (open: boolean) => void;
}

const categoryLabels: Record<string, { en: string; ar: string }> = {
  navigation: { en: "Navigation", ar: "التنقل" },
  action: { en: "Actions", ar: "الإجراءات" },
  search: { en: "Search", ar: "البحث" },
};

export function CommandPalette({ open: controlledOpen, onOpenChange }: CommandPaletteProps) {
  const [internalOpen, setInternalOpen] = useState(false);
  const [query, setQuery] = useState("");
  const [selectedIndex, setSelectedIndex] = useState(0);
  const [results, setResults] = useState<Command[]>([]);
  const inputRef = useRef<HTMLInputElement>(null);
  const locale = useLocale();
  const router = useRouter();
  const isRTL = locale === "ar";

  const isOpen = controlledOpen !== undefined ? controlledOpen : internalOpen;
  const setOpen = onOpenChange || setInternalOpen;

  useEffect(() => {
    registerCommandActions(
      (href: Route<string>) => {
        router.push(href);
        setOpen(false);
      },
      () => {
        setOpen(false);
      },
    );
  }, [router, setOpen]);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === "k") {
        e.preventDefault();
        setOpen(!isOpen);
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [isOpen, setOpen]);

  useEffect(() => {
    if (!query.trim()) {
      setResults(COMMANDS.slice(0, 10));
      return;
    }
    setResults(searchCommands(query, locale));
    setSelectedIndex(0);
  }, [query, locale]);

  useEffect(() => {
    if (isOpen) {
      setTimeout(() => inputRef.current?.focus(), 50);
    } else {
      setQuery("");
    }
  }, [isOpen]);

  const executeCommand = useCallback(
    (cmd: Command) => {
      setOpen(false);
      cmd.action();
    },
    [setOpen],
  );

  const handleKeyDown = useCallback(
    (e: React.KeyboardEvent) => {
      if (e.key === "ArrowDown") {
        e.preventDefault();
        setSelectedIndex((prev) => (prev + 1) % results.length);
      } else if (e.key === "ArrowUp") {
        e.preventDefault();
        setSelectedIndex((prev) => (prev - 1 + results.length) % results.length);
      } else if (e.key === "Enter" && results[selectedIndex]) {
        e.preventDefault();
        executeCommand(results[selectedIndex]);
      } else if (e.key === "Escape") {
        setOpen(false);
      }
    },
    [results, selectedIndex, executeCommand, setOpen],
  );

  const grouped = results.reduce<Record<string, Command[]>>((acc, cmd) => {
    if (!acc[cmd.category]) acc[cmd.category] = [];
    acc[cmd.category].push(cmd);
    return acc;
  }, {});

  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 z-[100] flex items-start justify-center pt-[15vh] bg-black/60 backdrop-blur-sm"
          onClick={() => setOpen(false)}
        >
          <motion.div
            initial={{ opacity: 0, scale: 0.95, y: -20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: -20 }}
            transition={{ duration: 0.15, ease: "easeOut" }}
            onClick={(e) => e.stopPropagation()}
            className={cn(
              "w-full max-w-xl rounded-2xl border border-border bg-card shadow-2xl overflow-hidden",
              "dark:bg-card/95 dark:backdrop-blur-xl",
            )}
          >
            {/* Search input */}
            <div className="flex items-center gap-3 border-b border-border px-5 py-4">
              <Search className="w-5 h-5 text-muted-foreground shrink-0" />
              <input
                ref={inputRef}
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder={isRTL ? "ابحث عن أمر..." : "Search commands..."}
                className="flex-1 bg-transparent text-base text-foreground placeholder:text-muted-foreground outline-none"
                dir={isRTL ? "rtl" : "ltr"}
              />
              <kbd className="hidden sm:inline-flex items-center gap-1 rounded-md border border-border bg-muted/50 px-2 py-0.5 text-xs text-muted-foreground">
                <Command className="w-3 h-3" />
                <span>K</span>
              </kbd>
            </div>

            {/* Results */}
            <div className="max-h-[360px] overflow-y-auto p-2">
              {results.length === 0 && (
                <div className="py-12 text-center text-sm text-muted-foreground">
                  {isRTL ? "لا توجد نتائج" : "No results found"}
                </div>
              )}

              {Object.entries(grouped).map(([category, cmds]) => (
                <div key={category} className="mb-2 last:mb-0">
                  <div className="px-3 py-1.5 text-[11px] font-semibold uppercase tracking-wider text-muted-foreground">
                    {isRTL
                      ? categoryLabels[category]?.ar ?? category
                      : categoryLabels[category]?.en ?? category}
                  </div>
                  {cmds.map((cmd, idx) => {
                    const globalIndex = results.indexOf(cmd);
                    const isSelected = selectedIndex === globalIndex;
                    return (
                      <button
                        key={cmd.id}
                        onClick={() => executeCommand(cmd)}
                        onMouseEnter={() => setSelectedIndex(globalIndex)}
                        className={cn(
                          "flex w-full items-center gap-3 rounded-lg px-3 py-2.5 text-sm transition-colors",
                          isSelected
                            ? "bg-accent text-accent-foreground"
                            : "text-foreground hover:bg-accent/50",
                        )}
                        dir={isRTL ? "rtl" : "ltr"}
                      >
                        <span className="flex-1 text-left">
                          {isRTL ? cmd.labelAr : cmd.label}
                        </span>
                        {cmd.shortcut && (
                          <kbd className="hidden sm:inline-flex items-center gap-1 rounded border border-border bg-muted/50 px-1.5 py-0.5 text-[10px] text-muted-foreground">
                            {cmd.shortcut}
                          </kbd>
                        )}
                        <ArrowRight
                          className={cn(
                            "w-4 h-4 text-muted-foreground/50",
                            isRTL && "rotate-180",
                          )}
                        />
                      </button>
                    );
                  })}
                </div>
              ))}
            </div>

            {/* Footer */}
            <div className="border-t border-border px-5 py-2.5 flex items-center gap-4 text-[11px] text-muted-foreground">
              <span className="flex items-center gap-1">
                <ArrowRight className="w-3 h-3" />
                {isRTL ? "اختيار" : "Select"}
              </span>
              <span className="flex items-center gap-1">
                <kbd className="rounded border border-border px-1 text-[10px]">esc</kbd>
                {isRTL ? "إلغاء" : "Cancel"}
              </span>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
