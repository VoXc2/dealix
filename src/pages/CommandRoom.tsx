import { useState } from "react";
import { trpc } from "@/providers/trpc";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "@/components/ui/card";
import {
  ClipboardCheck,
  Mail,
  Phone,
  MessageSquare,
  FileCheck,
  AlertTriangle,
  X,
  Send,
  Clock,
  CheckCircle2,
  BarChart3,
} from "lucide-react";

export default function CommandRoom() {
  const utils = trpc.useUtils();
  const drafts = trpc.commandRoom.draftList.useQuery();
  const stats = trpc.commandRoom.draftStats.useQuery();
  const pipeline = trpc.commandRoom.pipelineByStage.useQuery();
  const topOpps = trpc.commandRoom.topOpportunities.useQuery();

  const approve = trpc.commandRoom.approveDraft.useMutation({ onSuccess: () => utils.commandRoom.draftList.invalidate() });
  const reject = trpc.commandRoom.rejectDraft.useMutation({ onSuccess: () => utils.commandRoom.draftList.invalidate() });

  const typeIcon = (type: string) => {
    if (type === "email") return <Mail className="w-4 h-4" />;
    if (type === "whatsapp") return <MessageSquare className="w-4 h-4" />;
    if (type === "linkedin") return <FileCheck className="w-4 h-4" />;
    return <Send className="w-4 h-4" />;
  };

  const priorityColor = (p: number) => {
    if (p >= 8) return "bg-red-100 text-red-700";
    if (p >= 6) return "bg-amber-100 text-amber-700";
    if (p >= 4) return "bg-blue-100 text-blue-700";
    return "bg-slate-100 text-slate-700";
  };

  return (
    <div className="min-h-screen bg-[#F0F9F8] p-6" dir="rtl">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-[#15807A] rounded-lg flex items-center justify-center">
              <BarChart3 className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-[#0A1F1E]">Revenue Command Room</h1>
              <p className="text-sm text-[#4A6B69]">غرفة القيادة — Drafts، Pipeline، والقرارات اليومية</p>
            </div>
          </div>
          <Badge variant="outline" className="text-[#15807A] border-[#15807A]">
            <ClipboardCheck className="w-3 h-3 mr-1" />
            OUTBOUND_MODE: draft_only
          </Badge>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          {[
            { label: "Drafts", value: stats.data?.total ?? 0 },
            { label: "Pending Approval", value: stats.data?.pending ?? 0 },
            { label: "Approved", value: stats.data?.approved ?? 0 },
            { label: "Sent", value: stats.data?.sent ?? 0 },
          ].map((s) => (
            <Card key={s.label} className="bg-white border-[#E8F4F3]">
              <CardContent className="p-4 flex items-center gap-3">
                <div className="w-10 h-10 bg-[#E8F4F3] rounded-lg flex items-center justify-center">
                  <BarChart3 className="w-5 h-5 text-[#15807A]" />
                </div>
                <div>
                  <p className="text-xs text-[#4A6B69]">{s.label}</p>
                  <p className="text-xl font-bold text-[#0A1F1E]">{s.value}</p>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Main Grid */}
        <div className="grid lg:grid-cols-3 gap-8">
          {/* Drafts Queue */}
          <div className="lg:col-span-2 space-y-6">
            <Card className="bg-white border-[#E8F4F3]">
              <CardHeader className="pb-0">
                <CardTitle className="text-sm text-[#0A1F1E] flex items-center gap-2">
                  <Send className="w-4 h-4 text-[#15807A]" />
                  Outreach Drafts Queue
                </CardTitle>
                <CardDescription className="text-xs text-[#8CB3B0]">
                  كل drafts تتطلب موافقة يدوية قبل الإرسال
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3 mt-4">
                  {drafts.data?.slice(0, 10).map((d: any) => (
                    <div key={d.id} className={`p-4 rounded-lg border ${d.approved ? "border-green-200 bg-green-50" : "border-[#E8F4F3] bg-[#F0F9F8]"}`}>
                      <div className="flex items-start justify-between">
                        <div className="flex items-center gap-2 mb-2">
                          <div className="w-8 h-8 bg-white rounded-lg flex items-center justify-center shadow-sm">
                            {typeIcon(d.type)}
                          </div>
                          <div>
                            <span className="text-sm font-bold text-[#0A1F1E]">{d.prospectEmail || "—"}</span>
                            <span className="text-xs text-[#8CB3B0] mx-2">{d.prospectCompany || "—"}</span>
                          </div>
                          <Badge className={`${priorityColor(d.priority)} text-[10px] border-0`}>P{d.priority}</Badge>
                        </div>
                        <div className="flex gap-1">
                          {!d.approved && (
                            <Button size="sm" variant="outline" className="h-7 text-xs border-green-200 text-green-700 hover:bg-green-50" onClick={() => approve.mutate({ id: d.id })}>
                              <CheckCircle2 className="w-3 h-3 mr-1" />
                              موافقة
                            </Button>
                          )}
                          {!d.approved && (
                            <Button size="sm" variant="outline" className="h-7 text-xs border-red-200 text-red-700 hover:bg-red-50" onClick={() => reject.mutate({ id: d.id })}>
                              <X className="w-3 h-3 mr-1" />
                              رفض
                            </Button>
                          )}
                          {d.approved && !d.sent && (
                            <Badge className="bg-green-100 text-green-700 text-[10px] border-0">
                              <CheckCircle2 className="w-3 h-3 mr-1" />
                              تمت الموافقة
                            </Badge>
                          )}
                        </div>
                      </div>

                      {/* Arabic content */}
                      {d.contentAr && (
                        <div className="mt-2">
                          <pre className="text-xs text-[#0A1F1E] whitespace-pre-wrap bg-white p-2 rounded border border-[#E8F4F3] font-sans">{d.contentAr}</pre>
                        </div>
                      )}

                      {/* English content */}
                      {d.contentEn && (
                        <div className="mt-1">
                          <pre className="text-xs text-[#4A6B69] whitespace-pre-wrap bg-white p-2 rounded border border-[#E8F4F3] font-sans">{d.contentEn}</pre>
                        </div>
                      )}

                      <div className="flex items-center gap-3 mt-2 text-xs text-[#8CB3B0]">
                        <span className="bg-[#E8F4F3] px-2 py-0.5 rounded">[AI]</span>
                        <span>{d.outboundMode || "draft_only"}</span>
                        <span>{d.recommendedSendDate || "Today"}</span>
                      </div>
                    </div>
                  ))}
                  {(!drafts.data || drafts.data.length === 0) && (
                    <div className="text-center text-sm text-[#8CB3B0] py-8">
                      لا توجد drafts في الانتظار.
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Sidebar: Pipeline + Top Opportunities */}
          <div className="space-y-6">
            {/* Pipeline Stages */}
            <Card className="bg-white border-[#E8F4F3]">
              <CardHeader className="pb-0">
                <CardTitle className="text-sm text-[#0A1F1E] flex items-center gap-2">
                  <BarChart3 className="w-4 h-4 text-[#15807A]" />
                  Pipeline Overview
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2 mt-4">
                  {pipeline.data && Object.entries(pipeline.data).map(([stage, count]) => (
                    <div key={stage} className="flex items-center justify-between p-2 bg-[#F0F9F8] rounded">
                      <span className="text-xs text-[#0A1F1E]">{stage.replace("_", " ")}</span>
                      <Badge className="bg-[#15807A] text-white text-[10px] border-0">{count}</Badge>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Top Opportunities */}
            <Card className="bg-white border-[#E8F4F3]">
              <CardHeader className="pb-0">
                <CardTitle className="text-sm text-[#0A1F1E] flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-[#15807A]" />
                  Top Opportunities
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2 mt-4">
                  {topOpps.data?.slice(0, 5).map((o: any) => (
                    <div key={o.id} className="p-2 bg-[#F0F9F8] rounded">
                      <p className="text-xs font-bold text-[#0A1F1E]">{o.company}</p>
                      <p className="text-xs text-[#4A6B69]">{o.value} SAR</p>
                      <p className="text-xs text-[#8CB3B0]">{o.status}</p>
                    </div>
                  ))}
                  {(!topOpps.data || topOpps.data.length === 0) && (
                    <div className="text-center text-sm text-[#8CB3B0] py-4">لا توجد فرص قريبة</div>
                  )}
                </div>
              </CardContent>
            </Card>

            {/* Safety */}
            <Card className="bg-[#0A1F1E] text-white">
              <CardContent className="p-4 text-center">
                <AlertTriangle className="w-6 h-6 text-amber-400 mx-auto mb-2" />
                <p className="text-sm font-semibold">SAFETY SETTINGS</p>
                <p className="text-xs mt-1 text-[#8CB3B0]">No draft is sent without manual review. AI-generated content is tagged.</p>
                <p className="text-xs text-amber-300 mt-1">OUTBOUND_MODE = draft_only</p>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}
