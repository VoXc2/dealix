"use client";

import { useState } from "react";
import { useLocale } from "next-intl";
import { Button } from "@/components/ui/button";

export function HermesAgentWidget() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const [messages, setMessages] = useState<{ role: "user" | "hermes"; text: string }[]>([
    { role: "hermes", text: isAr ? "مرحباً — أنا هرميس، وكيل Dealix الذكي. أقدر أشخص قطاعك وأقنعك بالحل الأمثل مع كل الأدلة." : "Hello — I\'m Hermes, Dealix smart agent. I can diagnose your sector and convince you with full evidence." },
  ]);
  const [input, setInput] = useState("");
  const quick = isAr
    ? ["ما أفضل حل لقطاعي؟", "كيف يضمن Dealix عدم إرسال بارد؟", "كم وقت التشخيص؟", "أريد تسجيل حساب"]
    : ["Best solution for my sector?", "How does Dealix avoid cold outreach?", "How long is diagnostic?", "I want to register"];

  function send(text: string) {
    if (!text.trim()) return;
    setMessages((m) => [...m, { role: "user", text }, { role: "hermes", text: isAr ? `هرميس: فهمت — قطاعك يحتاج تشخيص D1 (3 عائلات) + عرض ${text.includes("ZATCA") ? "ZATCA" : "مجاني 7 أيام"} + إثبات L0-L5 — كلشي بأفضل شكل، 5 وكلاء يديرون، DeepWIP≤3. هل تريد تسجيل حساب الآن؟` : `Hermes: Got it — your sector needs D1 diagnostic (3 families) + ${text.includes("ZATCA") ? "ZATCA" : "free 7d"} offer + L0-L5 proof — all in best form, 5 agents manage, DeepWIP≤3. Want to register now?` }]);
    setInput("");
  }

  return (
    <div className="fixed bottom-4 right-4 w-80 rounded-2xl border border-gold-500/20 bg-navy-900/90 backdrop-blur-xl shadow-2xl z-50 overflow-hidden">
      <div className="bg-gradient-to-r from-gold-500 to-gold-400 text-navy-900 px-4 py-3 flex items-center gap-2">
        <div className="w-8 h-8 rounded-full bg-white flex items-center justify-center text-lg">🤖</div>
        <div>
          <div className="font-bold text-sm">Hermes</div>
          <div className="text-xs opacity-70">{isAr ? "وكيل Dealix الذكي — يقنع" : "Dealix Smart Agent — convinces"}</div>
        </div>
        <div className="ml-auto w-2 h-2 bg-emerald-500 rounded-full animate-pulse"></div>
      </div>
      <div className="h-64 overflow-y-auto p-3 space-y-2">
        {messages.map((m, i) => (
          <div key={i} className={m.role === "hermes" ? "bg-white/10 rounded-lg p-2 text-sm" : "bg-gold-500/20 rounded-lg p-2 text-sm ml-6"}>
            <div className="text-xs text-white/40 mb-1">{m.role === "hermes" ? "Hermes" : isAr ? "أنت" : "You"}</div>
            <div className="text-white/90">{m.text}</div>
          </div>
        ))}
      </div>
      <div className="p-2 border-t border-white/10">
        <div className="flex flex-wrap gap-1 mb-2">
          {quick.map((q) => (
            <button key={q} onClick={() => send(q)} className="text-xs bg-white/10 hover:bg-white/20 rounded-full px-2 py-1">
              {q}
            </button>
          ))}
        </div>
        <div className="flex gap-2">
          <input value={input} onChange={(e) => setInput(e.target.value)} onKeyDown={(e) => e.key === "Enter" && send(input)} placeholder={isAr ? "اكتب..." : "Type..."} className="flex-1 bg-white/10 border border-white/10 rounded-lg px-3 py-2 text-sm text-white placeholder-white/40" />
          <Button onClick={() => send(input)} size="sm" className="bg-gold-500 text-navy-900 hover:bg-gold-400">
            {isAr ? "إرسال" : "Send"}
          </Button>
        </div>
      </div>
    </div>
  );
}
