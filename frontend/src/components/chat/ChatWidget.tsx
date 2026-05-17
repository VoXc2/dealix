"use client";

import { useState } from "react";
import { useLocale } from "next-intl";
import { motion, AnimatePresence } from "framer-motion";
import { MessageCircle, X, Send, Loader2 } from "lucide-react";
import { api } from "@/lib/api";

interface ChatTurn {
  role: "user" | "bot";
  text: string;
  escalated?: boolean;
}

export function ChatWidget() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const T = (ar: string, en: string) => (isAr ? ar : en);

  const [open, setOpen] = useState(false);
  const [busy, setBusy] = useState(false);
  const [input, setInput] = useState("");
  const [turns, setTurns] = useState<ChatTurn[]>([]);

  async function send() {
    const message = input.trim();
    if (!message || busy) return;
    setInput("");
    setTurns((t) => [...t, { role: "user", text: message }]);
    setBusy(true);
    try {
      const res = await api.postChatMessage(message);
      const data = res.data as {
        answered: boolean;
        escalated?: boolean;
        answer_ar?: string;
        answer_en?: string;
        message_ar?: string;
        message_en?: string;
      };
      const text = data.answered
        ? (isAr ? data.answer_ar : data.answer_en) || ""
        : (isAr ? data.message_ar : data.message_en) || "";
      setTurns((t) => [...t, { role: "bot", text, escalated: data.escalated }]);
    } catch {
      setTurns((t) => [
        ...t,
        {
          role: "bot",
          text: T("تعذّر الاتصال — حاول لاحقاً.", "Connection failed — try again later."),
        },
      ]);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className={`fixed bottom-5 z-50 ${isAr ? "left-5" : "right-5"}`}>
      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ opacity: 0, y: 20, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 20, scale: 0.95 }}
            className="mb-3 w-80 h-96 rounded-2xl border border-border bg-card shadow-xl flex flex-col overflow-hidden"
          >
            <div className="flex items-center justify-between px-4 h-12 border-b border-border bg-muted/40">
              <span className="text-sm font-semibold">
                {T("مساعد ديليكس", "Dealix Assistant")}
              </span>
              <button onClick={() => setOpen(false)} aria-label="close">
                <X className="w-4 h-4 text-muted-foreground" />
              </button>
            </div>

            <div className="flex-1 overflow-y-auto p-3 space-y-2">
              {turns.length === 0 && (
                <p className="text-xs text-muted-foreground text-center mt-6">
                  {T(
                    "اسأل عن خدماتنا أو الأسعار أو طريقة البدء.",
                    "Ask about our services, pricing, or how to start.",
                  )}
                </p>
              )}
              {turns.map((turn, i) => (
                <div
                  key={i}
                  className={`flex ${turn.role === "user" ? "justify-end" : "justify-start"}`}
                >
                  <div
                    className={`max-w-[80%] rounded-xl px-3 py-2 text-xs ${
                      turn.role === "user"
                        ? "bg-gold-500 text-white"
                        : turn.escalated
                          ? "bg-amber-500/15 text-amber-300"
                          : "bg-muted text-foreground"
                    }`}
                  >
                    {turn.text}
                  </div>
                </div>
              ))}
              {busy && (
                <div className="flex justify-start">
                  <Loader2 className="w-4 h-4 animate-spin text-muted-foreground" />
                </div>
              )}
            </div>

            <div className="flex items-center gap-2 p-3 border-t border-border">
              <input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && send()}
                placeholder={T("اكتب رسالتك…", "Type your message…")}
                className="flex-1 bg-muted rounded-lg px-3 py-2 text-xs outline-none"
              />
              <button
                onClick={send}
                disabled={busy}
                aria-label="send"
                className="w-8 h-8 rounded-lg bg-gold-500 text-white flex items-center justify-center disabled:opacity-50"
              >
                <Send className="w-4 h-4" />
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      <button
        onClick={() => setOpen((o) => !o)}
        aria-label="chat"
        className="w-14 h-14 rounded-full bg-gold-500 text-white shadow-lg flex items-center justify-center hover:bg-gold-600 transition-colors"
      >
        {open ? <X className="w-6 h-6" /> : <MessageCircle className="w-6 h-6" />}
      </button>
    </div>
  );
}
