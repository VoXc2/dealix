"use client";

import { useCallback, useEffect, useState } from "react";
import { useTranslations } from "next-intl";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import { api } from "@/lib/api";

interface Citation {
  chunk_id: string;
  source_id: string;
  title?: string;
  relevance?: number;
}

interface QueryResult {
  answer_mode: string;
  answer_ar: string;
  answer_en: string;
  citations: Citation[];
  confidence: number;
  governance_decision: string;
}

interface Stats {
  workspace_id: string;
  chunk_count: number;
  source_count: number;
  sources: string[];
  restricted_chunk_count: number;
}

const INPUT =
  "w-full rounded-md border border-border bg-background px-3 py-2 text-sm";

export function KnowledgeContent() {
  const t = useTranslations("knowledge");

  const [workspaceId, setWorkspaceId] = useState("demo");
  const [stats, setStats] = useState<Stats | null>(null);

  // Ingest form
  const [sourceId, setSourceId] = useState("");
  const [docTitle, setDocTitle] = useState("");
  const [text, setText] = useState("");
  const [allowedRoles, setAllowedRoles] = useState("");
  const [ingesting, setIngesting] = useState(false);
  const [ingestMsg, setIngestMsg] = useState("");

  // Query form
  const [viewerRole, setViewerRole] = useState("");
  const [question, setQuestion] = useState("");
  const [asking, setAsking] = useState(false);
  const [result, setResult] = useState<QueryResult | null>(null);

  const refreshStats = useCallback(async () => {
    try {
      const res = await api.getKnowledgeStats(workspaceId);
      setStats(res.data as Stats);
    } catch {
      setStats(null);
    }
  }, [workspaceId]);

  useEffect(() => {
    void refreshStats();
  }, [refreshStats]);

  const handleIngest = async () => {
    setIngesting(true);
    setIngestMsg("");
    try {
      await api.ingestKnowledge({
        workspace_id: workspaceId,
        text,
        source_id: sourceId,
        title: docTitle || undefined,
        allowed_roles: allowedRoles
          .split(",")
          .map((r) => r.trim())
          .filter(Boolean),
      });
      setIngestMsg("ok");
      setText("");
      setSourceId("");
      setDocTitle("");
      setAllowedRoles("");
      await refreshStats();
    } catch {
      setIngestMsg("error");
    } finally {
      setIngesting(false);
    }
  };

  const handleAsk = async () => {
    setAsking(true);
    setResult(null);
    try {
      const res = await api.queryKnowledge({
        workspace_id: workspaceId,
        question,
        viewer_role: viewerRole,
      });
      setResult(res.data as QueryResult);
    } catch {
      setResult(null);
    } finally {
      setAsking(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Workspace + stats */}
      <Card>
        <CardHeader>
          <CardTitle>{t("sources")}</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <div className="flex items-end gap-3">
            <div className="flex-1">
              <Label>{t("workspace")}</Label>
              <Input
                value={workspaceId}
                onChange={(e) => setWorkspaceId(e.target.value)}
              />
            </div>
            <Button variant="outline" onClick={() => void refreshStats()}>
              ↻
            </Button>
          </div>
          {stats && (
            <div className="flex flex-wrap gap-2">
              <Badge variant="secondary">
                {t("chunkCount")}: {stats.chunk_count}
              </Badge>
              <Badge variant="secondary">
                {t("sourceCount")}: {stats.source_count}
              </Badge>
              <Badge variant="secondary">
                {t("restricted")}: {stats.restricted_chunk_count}
              </Badge>
              {stats.sources.map((s) => (
                <Badge key={s}>{s}</Badge>
              ))}
            </div>
          )}
        </CardContent>
      </Card>

      <div className="grid gap-6 md:grid-cols-2">
        {/* Ingest */}
        <Card>
          <CardHeader>
            <CardTitle>{t("ingestTitle")}</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <div>
              <Label>{t("sourceId")}</Label>
              <Input
                value={sourceId}
                onChange={(e) => setSourceId(e.target.value)}
              />
            </div>
            <div>
              <Label>{t("docTitle")}</Label>
              <Input
                value={docTitle}
                onChange={(e) => setDocTitle(e.target.value)}
              />
            </div>
            <div>
              <Label>{t("text")}</Label>
              <textarea
                className={INPUT}
                rows={5}
                value={text}
                onChange={(e) => setText(e.target.value)}
              />
            </div>
            <div>
              <Label>{t("allowedRoles")}</Label>
              <Input
                value={allowedRoles}
                onChange={(e) => setAllowedRoles(e.target.value)}
              />
            </div>
            <Button
              onClick={() => void handleIngest()}
              disabled={ingesting || !sourceId || !text}
            >
              {t("ingest")}
            </Button>
            {ingestMsg === "ok" && (
              <p className="text-sm text-emerald-600">✓</p>
            )}
            {ingestMsg === "error" && (
              <p className="text-sm text-red-600">✗</p>
            )}
          </CardContent>
        </Card>

        {/* Ask */}
        <Card>
          <CardHeader>
            <CardTitle>{t("askTitle")}</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <div>
              <Label>{t("viewerRole")}</Label>
              <Input
                value={viewerRole}
                onChange={(e) => setViewerRole(e.target.value)}
                placeholder="staff / executive"
              />
            </div>
            <div>
              <Label>{t("question")}</Label>
              <textarea
                className={INPUT}
                rows={3}
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
              />
            </div>
            <Button
              onClick={() => void handleAsk()}
              disabled={asking || !question}
            >
              {t("ask")}
            </Button>

            {result && result.answer_mode === "evidence_backed" && (
              <div className="space-y-2 rounded-md border border-border p-3">
                <p className="text-sm font-medium">{t("answer")}</p>
                <p className="text-sm">{result.answer_en}</p>
                <p className="text-sm" dir="rtl">
                  {result.answer_ar}
                </p>
                <p className="text-xs font-medium">{t("citations")}</p>
                <div className="flex flex-wrap gap-2">
                  {result.citations.map((c) => (
                    <Badge key={c.chunk_id} variant="secondary">
                      {c.source_id}
                      {typeof c.relevance === "number"
                        ? ` (${c.relevance})`
                        : ""}
                    </Badge>
                  ))}
                </div>
              </div>
            )}
            {result && result.answer_mode !== "evidence_backed" && (
              <p className="text-sm text-muted-foreground">{t("noAnswer")}</p>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
