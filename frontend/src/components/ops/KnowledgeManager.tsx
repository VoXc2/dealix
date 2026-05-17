"use client";

import { useCallback, useEffect, useState } from "react";
import { useLocale } from "next-intl";
import { RefreshCw, Plus } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";
import { toast } from "sonner";
import { api } from "@/lib/api";

interface Article {
  article_id: string;
  slug: string;
  title_en: string;
  title_ar: string;
  status: string;
}

interface Gap {
  gap_id: string;
  query_text: string;
  hit_count: number;
  status: string;
}

export function KnowledgeManager() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const T = (ar: string, en: string) => (isAr ? ar : en);

  const [articles, setArticles] = useState<Article[]>([]);
  const [gaps, setGaps] = useState<Gap[]>([]);
  const [loading, setLoading] = useState(true);
  const [draft, setDraft] = useState({ slug: "", title_en: "", body_en: "" });

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const [aRes, gRes] = await Promise.all([
        api.getKnowledgeArticles(),
        api.getKnowledgeGaps(),
      ]);
      setArticles((aRes.data as { articles?: Article[] }).articles || []);
      setGaps((gRes.data as { gaps?: Gap[] }).gaps || []);
    } catch {
      toast.error(T("تعذّر التحميل", "Could not load"));
    } finally {
      setLoading(false);
    }
  }, [isAr]);

  useEffect(() => {
    void load();
  }, [load]);

  async function create() {
    if (!draft.slug || !draft.title_en) {
      toast.error(T("الرجاء تعبئة الحقول", "Fill the fields"));
      return;
    }
    try {
      await api.createKnowledgeArticle(draft);
      setDraft({ slug: "", title_en: "", body_en: "" });
      toast.success(T("أُنشئ كمسودة", "Created as draft"));
      await load();
    } catch {
      toast.error(T("فشل الإنشاء", "Create failed"));
    }
  }

  async function publish(id: string) {
    try {
      const res = await api.publishKnowledgeArticle(id);
      const data = res.data as { published: boolean; approval_status?: string };
      toast.success(
        data.published
          ? T("نُشر", "Published")
          : T("بانتظار موافقة المؤسس", "Awaiting founder approval"),
      );
      await load();
    } catch {
      toast.error(T("فشل النشر", "Publish failed"));
    }
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-4">
        <p className="text-sm text-muted-foreground">
          {T("نشر مقال يحتاج موافقة المؤسس.", "Publishing an article needs founder approval.")}
        </p>
        <Button variant="outline" size="sm" onClick={() => void load()} disabled={loading}>
          <RefreshCw className={cn("w-4 h-4 me-1", loading && "animate-spin")} />
          {T("تحديث", "Refresh")}
        </Button>
      </div>

      <div className="rounded-2xl border border-border bg-card p-4 mb-6 space-y-2">
        <h3 className="text-sm font-semibold">{T("مقال جديد", "New article")}</h3>
        <Input
          placeholder="slug"
          value={draft.slug}
          onChange={(e) => setDraft({ ...draft, slug: e.target.value })}
        />
        <Input
          placeholder={T("العنوان", "Title")}
          value={draft.title_en}
          onChange={(e) => setDraft({ ...draft, title_en: e.target.value })}
        />
        <Input
          placeholder={T("المحتوى", "Body")}
          value={draft.body_en}
          onChange={(e) => setDraft({ ...draft, body_en: e.target.value })}
        />
        <Button variant="emerald" size="sm" onClick={() => void create()}>
          <Plus className="w-4 h-4 me-1" />
          {T("إنشاء مسودة", "Create draft")}
        </Button>
      </div>

      <h3 className="text-sm font-semibold mb-2">{T("المقالات", "Articles")}</h3>
      <div className="space-y-2 mb-6">
        {articles.length === 0 ? (
          <p className="text-xs text-muted-foreground">{T("لا مقالات", "No articles")}</p>
        ) : (
          articles.map((a) => (
            <div
              key={a.article_id}
              className="rounded-xl border border-border bg-card p-3 flex items-center justify-between gap-3"
            >
              <div className="min-w-0">
                <p className="text-sm font-medium truncate">{a.title_en || a.slug}</p>
                <Badge
                  variant="outline"
                  className={cn(
                    "text-[10px]",
                    a.status === "approved" ? "text-emerald-400" : "text-amber-400",
                  )}
                >
                  {a.status}
                </Badge>
              </div>
              {a.status !== "approved" && (
                <Button variant="outline" size="sm" onClick={() => void publish(a.article_id)}>
                  {T("نشر", "Publish")}
                </Button>
              )}
            </div>
          ))
        )}
      </div>

      <h3 className="text-sm font-semibold mb-2">
        {T("فجوات المعرفة", "Knowledge gaps")}
      </h3>
      <div className="space-y-2">
        {gaps.length === 0 ? (
          <p className="text-xs text-muted-foreground">{T("لا فجوات", "No gaps")}</p>
        ) : (
          gaps.map((g) => (
            <div
              key={g.gap_id}
              className="rounded-xl border border-border bg-card p-3 flex items-center justify-between gap-3"
            >
              <p className="text-sm truncate">{g.query_text}</p>
              <Badge variant="outline" className="text-[10px]">
                ×{g.hit_count}
              </Badge>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
