"use client";

import { useState, useCallback, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { MessageCircle, X, Send, Loader2, Bot, User, Minimize2, Maximize2 } from "lucide-react";
import { useLocale } from "next-intl";
import { cn } from "@/lib/utils";

interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: string;
}

const WELCOME_MESSAGE: ChatMessage = {
  id: "welcome",
  role: "assistant",
  content: "مرحباً! كيف يمكنني مساعدتك اليوم؟",
  timestamp: new Date().toISOString(),
};

interface LiveChatProps {
  apiEndpoint?: string;
  locale?: string;
}

export function LiveChat({ apiEndpoint = "/api/v1/chat", locale: propLocale }: LiveChatProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [isMinimized, setIsMinimized] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([WELCOME_MESSAGE]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const locale = propLocale || "ar";
  const isRTL = locale === "ar";

  const handleSend = useCallback(async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: ChatMessage = {
      id: `user-${Date.now()}`,
      role: "user",
      content: input.trim(),
      timestamp: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      const res = await fetch(apiEndpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMessage.content }),
      });
      const data = await res.json();
      const assistantMessage: ChatMessage = {
        id: `assistant-${Date.now()}`,
        role: "assistant",
        content: data.response || data.message || "I'm here to help!",
        timestamp: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch {
      const fallback: ChatMessage = {
        id: `assistant-${Date.now()}`,
        role: "assistant",
        content: isRTL ? "عذراً، حدث خطأ. حاول مرة أخرى." : "Sorry, something went wrong. Please try again.",
        timestamp: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, fallback]);
    } finally {
      setIsLoading(false);
    }
  }, [input, isLoading, apiEndpoint, isRTL]);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  useEffect(() => {
    if (isOpen && !isMinimized) {
      const container = document.getElementById("chat-messages");
      if (container) container.scrollTop = container.scrollHeight;
    }
  }, [messages, isOpen, isMinimized]);

  return (
    <>
      {/* Chat button */}
      {!isOpen && (
        <motion.button
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          whileHover={{ scale: 1.05 }}
          onClick={() => setIsOpen(true)}
          className={cn(
            "fixed bottom-6 right-6 z-50 flex h-14 w-14 items-center justify-center rounded-full shadow-xl",
            "bg-gold-500 hover:bg-gold-400 text-white transition-colors",
            "dark:shadow-gold-500/20",
          )}
          aria-label={isRTL ? "فتح الدردشة" : "Open chat"}
        >
          <MessageCircle className="w-6 h-6" />
        </motion.button>
      )}

      {/* Chat window */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: 20, scale: 0.95 }}
            animate={{
              opacity: 1,
              y: 0,
              scale: 1,
              height: isMinimized ? "auto" : "480px",
              width: isMinimized ? "auto" : "360px",
            }}
            exit={{ opacity: 0, y: 20, scale: 0.95 }}
            className={cn(
              "fixed bottom-6 right-6 z-50 flex flex-col rounded-2xl border border-border bg-card shadow-2xl overflow-hidden",
              "dark:shadow-2xl dark:shadow-black/40",
            )}
            style={{ width: isMinimized ? "auto" : "360px", height: isMinimized ? "auto" : "480px" }}
          >
            {/* Header */}
            <div className="flex items-center justify-between px-4 py-3 border-b border-border bg-accent/30">
              <div className="flex items-center gap-2">
                <Bot className="w-5 h-5 text-gold-500" />
                <span className="text-sm font-semibold text-foreground">
                  {isRTL ? "ديليكس مساعد" : "Dealix Assistant"}
                </span>
              </div>
              <div className="flex items-center gap-1">
                <button
                  onClick={() => setIsMinimized(!isMinimized)}
                  className="rounded-lg p-1 text-muted-foreground hover:text-foreground hover:bg-accent transition-colors"
                >
                  {isMinimized ? <Maximize2 className="w-4 h-4" /> : <Minimize2 className="w-4 h-4" />}
                </button>
                <button
                  onClick={() => setIsOpen(false)}
                  className="rounded-lg p-1 text-muted-foreground hover:text-foreground hover:bg-accent transition-colors"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>
            </div>

            {!isMinimized && (
              <>
                {/* Messages */}
                <div id="chat-messages" className="flex-1 overflow-y-auto p-4 space-y-3">
                  {messages.map((msg) => (
                    <div
                      key={msg.id}
                      className={cn(
                        "flex gap-2 max-w-[85%]",
                        msg.role === "user" ? "ml-auto" : "mr-auto",
                      )}
                      dir={isRTL ? "rtl" : "ltr"}
                    >
                      {msg.role === "assistant" && (
                        <div className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-gold-500/10 mt-1">
                          <Bot className="w-3.5 h-3.5 text-gold-500" />
                        </div>
                      )}
                      <div
                        className={cn(
                          "rounded-2xl px-3.5 py-2 text-sm",
                          msg.role === "user"
                            ? "bg-gold-500 text-white"
                            : "bg-accent text-foreground",
                        )}
                      >
                        <p className="text-sm leading-relaxed">{msg.content}</p>
                        <p className="text-[10px] opacity-60 mt-1">
                          {new Date(msg.timestamp).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
                        </p>
                      </div>
                      {msg.role === "user" && (
                        <div className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-accent mt-1">
                          <User className="w-3.5 h-3.5 text-muted-foreground" />
                        </div>
                      )}
                    </div>
                  ))}
                  {isLoading && (
                    <div className="flex items-center gap-2 text-sm text-muted-foreground">
                      <Loader2 className="w-4 h-4 animate-spin" />
                      <span>{isRTL ? "يكتب..." : "Typing..."}</span>
                    </div>
                  )}
                </div>

                {/* Input */}
                <div className="border-t border-border p-3">
                  <div className="flex items-center gap-2">
                    <input
                      type="text"
                      value={input}
                      onChange={(e) => setInput(e.target.value)}
                      onKeyDown={handleKeyDown}
                      placeholder={isRTL ? "اكتب رسالتك..." : "Type your message..."}
                      className="flex-1 rounded-xl border border-border bg-background px-4 py-2.5 text-sm outline-none focus:border-gold-500/50 transition-colors"
                      dir={isRTL ? "rtl" : "ltr"}
                    />
                    <button
                      onClick={handleSend}
                      disabled={!input.trim() || isLoading}
                      className="flex h-10 w-10 items-center justify-center rounded-xl bg-gold-500 text-white hover:bg-gold-400 disabled:opacity-50 transition-colors"
                    >
                      {isLoading ? (
                        <Loader2 className="w-4 h-4 animate-spin" />
                      ) : (
                        <Send className="w-4 h-4" />
                      )}
                    </button>
                  </div>
                </div>
              </>
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}
