import { useState } from "react";
import { trpc } from "@/providers/trpc";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import {
  Brain,
  AlertTriangle,
  Lightbulb,
  ShieldCheck,
  Activity,
  Target,
  Zap,
  BarChart3,
  CheckCircle,
  Clock,
} from "lucide-react";

export default function BrainOS() {
  const utils = trpc.useUtils();
  const stats = trpc.brain.dashboardStats.useQuery();
  const signals = trpc.brain.signalList.useQuery();
  const decisions = trpc.brain.decisionList.useQuery();
  const risks = trpc.brain.riskList.useQuery();
  const opportunities = trpc.brain.opportunityList.useQuery();

  const createSignal = trpc.brain.signalCreate.useMutation({ onSuccess: () => { utils.brain.signalList.invalidate(); utils.brain.dashboardStats.invalidate(); } });
  const createDecision = trpc.brain.decisionCreate.useMutation({ onSuccess: () => { utils.brain.decisionList.invalidate(); utils.brain.dashboardStats.invalidate(); } });
  const createRisk = trpc.brain.riskCreate.useMutation({ onSuccess: () => { utils.brain.riskList.invalidate(); utils.brain.dashboardStats.invalidate(); } });
  const createOpp = trpc.brain.opportunityCreate.useMutation({ onSuccess: () => { utils.brain.opportunityList.invalidate(); utils.brain.dashboardStats.invalidate(); } });

  const [newSignal, setNewSignal] = useState({ signalType: "revenue", source: "", description: "", strength: 5, confidence: 0.5 });
  const [newDecision, setNewDecision] = useState({ decision: "", owner: "", nextAction: "", metric: "", assumption: "", priority: 5 });
  const [newRisk, setNewRisk] = useState({ risk: "", probability: 3, impact: 3, mitigation: "", owner: "" });
  const [newOpp, setNewOpp] = useState({ opportunity: "", potentialValue: "0", confidence: 0.5, effort: "medium", owner: "" });

  // Helper for signal badge color
  const signalBadge = (type: string) => {
    const map: Record<string, string> = { revenue: "bg-emerald-100 text-emerald-700", pain: "bg-red-100 text-red-700", opportunity: "bg-amber-100 text-amber-700", risk: "bg-orange-100 text-orange-700", bottleneck: "bg-slate-100 text-slate-700", market: "bg-blue-100 text-blue-700", competitor: "bg-purple-100 text-purple-700" };
    return map[type] || "bg-gray-100 text-gray-700";
  };

  const priorityColor = (p: number) => {
    if (p >= 8) return "bg-red-100 text-red-700";
    if (p >= 6) return "bg-amber-100 text-amber-700";
    if (p >= 4) return "bg-blue-100 text-blue-700";
    return "bg-slate-100 text-slate-700";
  };

  return (
    <div className="min-h-screen bg-[#F0F9F8] p-6" dir="rtl">
      {/* Header */}
      <div className="max-w-7xl mx-auto">
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-[#15807A] rounded-lg flex items-center justify-center">
              <Brain className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-[#0A1F1E]">Company Brain OS</h1>
              <p className="text-sm text-[#4A6B69]">عقل استراتيجي واضح — بيانات، قرارات، مخاطر، فرص</p>
            </div>
          </div>
          <Badge variant="outline" className="text-[#15807A] border-[#15807A]">
            <ShieldCheck className="w-3 h-3 mr-1" />
            Draft-only mode
          </Badge>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4 mb-8">
          {[
            { icon: Activity, label: "Signals", value: stats.data?.signals ?? 0 },
            { icon: Target, label: "Decisions", value: stats.data?.decisions ?? 0 },
            { icon: AlertTriangle, label: "Active Risks", value: stats.data?.activeRisks ?? 0 },
            { icon: Lightbulb, label: "Opportunities", value: stats.data?.opportunities ?? 0 },
            { icon: Zap, label: "Experiments", value: stats.data?.experiments ?? 0 },
          ].map((s) => (
            <Card key={s.label} className="bg-white border-[#E8F4F3]">
              <CardContent className="p-4 flex items-center gap-3">
                <div className="w-10 h-10 bg-[#E8F4F3] rounded-lg flex items-center justify-center">
                  <s.icon className="w-5 h-5 text-[#15807A]" />
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
          {/* Signals Column */}
          <div className="space-y-6">
            <Card className="bg-white border-[#E8F4F3]">
              <CardHeader className="pb-0">
                <CardTitle className="text-sm text-[#0A1F1E] flex items-center gap-2">
                  <Activity className="w-4 h-4 text-[#15807A]" />
                  Company Signals
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3 mt-4">
                  {signals.data?.slice(0, 6).map((s: any) => (
                    <div key={s.id} className="flex items-center justify-between p-3 bg-[#F0F9F8] rounded-lg">
                      <div>
                        <Badge className={`${signalBadge(s.signalType)} text-[10px] px-2 py-0.5 border-0 mb-1 inline-block`}>{s.signalType}</Badge>
                        <p className="text-sm text-[#0A1F1E] line-clamp-2">{s.description}</p>
                        <p className="text-xs text-[#8CB3B0] mt-0.5">{s.source || "auto"} • {Math.round(s.strength)}/10</p>
                      </div>
                      <div className="text-xs text-[#4A6B69] tabular-nums">
                        {(Number(s.confidence ?? 0.5) * 100).toFixed(0)}%
                      </div>
                    </div>
                  ))}
                  {(!signals.data || signals.data.length === 0) && (
                    <div className="text-center text-sm text-[#8CB3B0] py-6">لا توجد signals بعد. أضف أول signal.</div>
                  )}
                </div>

                {/* Add Signal Form */}
                <div className="mt-4 pt-4 border-t border-[#E8F4F3] space-y-3">
                  <Select value={newSignal.signalType} onValueChange={(v) => setNewSignal({ ...newSignal, signalType: v })}>
                    <SelectTrigger className="border-[#E8F4F3]"><SelectValue placeholder="نوع الإشارة" /></SelectTrigger>
                    <SelectContent>
                      {["revenue", "pain", "opportunity", "risk", "bottleneck", "market", "competitor"].map(t => <SelectItem key={t} value={t}>{t}</SelectItem>)}
                    </SelectContent>
                  </Select>
                  <Textarea placeholder="الوصف..." className="border-[#E8F4F3]" value={newSignal.description} onChange={(e) => setNewSignal({ ...newSignal, description: e.target.value })} />
                  <Input placeholder="المصدر" className="border-[#E8F4F3]" value={newSignal.source} onChange={(e) => setNewSignal({ ...newSignal, source: e.target.value })} />
                  <div className="flex gap-2">
                    <Input type="number" placeholder="Strength 1-10" className="border-[#E8F4F3]" value={newSignal.strength} onChange={(e) => setNewSignal({ ...newSignal, strength: parseInt(e.target.value || "5") })} />
                    <Button size="sm" className="bg-[#15807A] hover:bg-[#0F5F5A]" onClick={() => createSignal.mutate(newSignal)}>أضف</Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Decisions Column */}
          <div className="space-y-6">
            <Card className="bg-white border-[#E8F4F3]">
              <CardHeader className="pb-0">
                <CardTitle className="text-sm text-[#0A1F1E] flex items-center gap-2">
                  <Target className="w-4 h-4 text-[#15807A]" />
                  Decisions Log
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3 mt-4">
                  {decisions.data?.slice(0, 6).map((d: any) => (
                    <div key={d.id} className="p-3 bg-[#F0F9F8] rounded-lg">
                      <div className="flex items-center justify-between mb-1">
                        <Badge className={`${priorityColor(d.priority)} text-[10px] px-2 py-0.5 border-0`}>P{d.priority}</Badge>
                        <span className="text-xs text-[#8CB3B0]">{d.owner}</span>
                      </div>
                      <p className="text-sm text-[#0A1F1E] line-clamp-2">{d.decision}</p>
                      <p className="text-xs text-[#4A6B69] mt-1">Next: {d.nextAction}</p>
                      {d.metric && <p className="text-xs text-[#8CB3B0]">Metric: {d.metric}</p>}
                    </div>
                  ))}
                  {(!decisions.data || decisions.data.length === 0) && (
                    <div className="text-center text-sm text-[#8CB3B0] py-6">لا توجد قرارات مسجلة. أضف أول قرار.</div>
                  )}
                </div>

                {/* Add Decision Form */}
                <div className="mt-4 pt-4 border-t border-[#E8F4F3] space-y-3">
                  <Textarea placeholder="القرار..." className="border-[#E8F4F3]" value={newDecision.decision} onChange={(e) => setNewDecision({ ...newDecision, decision: e.target.value })} />
                  <Input placeholder="المالك (Owner)" className="border-[#E8F4F3]" value={newDecision.owner} onChange={(e) => setNewDecision({ ...newDecision, owner: e.target.value })} />
                  <Input placeholder="الخطوة التالية (Next Action)" className="border-[#E8F4F3]" value={newDecision.nextAction} onChange={(e) => setNewDecision({ ...newDecision, nextAction: e.target.value })} />
                  <div className="flex gap-2">
                    <Input placeholder="Metric" className="border-[#E8F4F3]" value={newDecision.metric} onChange={(e) => setNewDecision({ ...newDecision, metric: e.target.value })} />
                    <Input type="number" placeholder="Priority 1-10" className="border-[#E8F4F3] w-28" value={newDecision.priority} onChange={(e) => setNewDecision({ ...newDecision, priority: parseInt(e.target.value || "5") })} />
                    <Button size="sm" className="bg-[#15807A] hover:bg-[#0F5F5A]" onClick={() => createDecision.mutate(newDecision)}>أضف</Button>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Risk Register */}
            <Card className="bg-white border-[#E8F4F3]">
              <CardHeader className="pb-0">
                <CardTitle className="text-sm text-[#0A1F1E] flex items-center gap-2">
                  <AlertTriangle className="w-4 h-4 text-[#c0392b]" />
                  Risk Register
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3 mt-4">
                  {risks.data?.slice(0, 5).map((r: any) => (
                    <div key={r.id} className="p-3 bg-[#F0F9F8] rounded-lg">
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-xs font-medium text-[#c0392b]">Severity: {r.severity}/9</span>
                        <span className="text-xs text-[#8CB3B0]">{r.owner || "Unassigned"}</span>
                      </div>
                      <p className="text-sm text-[#0A1F1E]">{r.risk}</p>
                      {r.mitigation && <p className="text-xs text-green-700 mt-1">Mitigation: {r.mitigation.substring(0, 60)}...</p>}
                    </div>
                  ))}
                  {(!risks.data || risks.data.length === 0) && (
                    <div className="text-center text-sm text-[#8CB3B0] py-6">لا توجد مخاطر مسجلة. أضف أول risk.</div>
                  )}
                </div>

                <div className="mt-4 pt-4 border-t border-[#E8F4F3] space-y-3">
                  <Textarea placeholder="المخاطرة..." className="border-[#E8F4F3]" value={newRisk.risk} onChange={(e) => setNewRisk({ ...newRisk, risk: e.target.value })} />
                  <div className="flex gap-2">
                    <Input type="number" placeholder="Probability 1-5" className="border-[#E8F4F3]" value={newRisk.probability} onChange={(e) => setNewRisk({ ...newRisk, probability: parseInt(e.target.value || "3") })} />
                    <Input type="number" placeholder="Impact 1-5" className="border-[#E8F4F3]" value={newRisk.impact} onChange={(e) => setNewRisk({ ...newRisk, impact: parseInt(e.target.value || "3") })} />
                    <Button size="sm" className="bg-[#c0392b] hover:bg-[#a93226]" onClick={() => createRisk.mutate(newRisk)}>أضف</Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Opportunities Column */}
          <div className="space-y-6">
            <Card className="bg-white border-[#E8F4F3]">
              <CardHeader className="pb-0">
                <CardTitle className="text-sm text-[#0A1F1E] flex items-center gap-2">
                  <Lightbulb className="w-4 h-4 text-[#15807A]" />
                  Opportunity Register
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3 mt-4">
                  {opportunities.data?.slice(0, 6).map((o: any) => (
                    <div key={o.id} className="p-3 bg-[#F0F9F8] rounded-lg">
                      <div className="flex items-center justify-between mb-1">
                        <Badge className={`${priorityColor(o.priority)} text-[10px] px-2 py-0.5 border-0`}>P{o.priority}</Badge>
                        <span className="text-xs text-[#8CB3B0]">{o.effort} effort</span>
                      </div>
                      <p className="text-sm text-[#0A1F1E]">{o.opportunity}</p>
                      <div className="flex items-center gap-3 mt-1">
                        <span className="text-xs text-[#4A6B69]">{o.potentialValue} SAR</span>
                        <span className="text-xs text-[#4A6B69]">{(Number(o.confidence ?? 0.5) * 100).toFixed(0)}% confidence</span>
                      </div>
                      {o.owner && <p className="text-xs text-[#8CB3B0] mt-0.5">Owner: {o.owner}</p>}
                    </div>
                  ))}
                  {(!opportunities.data || opportunities.data.length === 0) && (
                    <div className="text-center text-sm text-[#8CB3B0] py-6">لا توجد فرص مسجلة. أضف أول opportunity.</div>
                  )}
                </div>

                {/* Add Opportunity Form */}
                <div className="mt-4 pt-4 border-t border-[#E8F4F3] space-y-3">
                  <Textarea placeholder="الفرصة..." className="border-[#E8F4F3]" value={newOpp.opportunity} onChange={(e) => setNewOpp({ ...newOpp, opportunity: e.target.value })} />
                  <div className="flex gap-2">
                    <Input placeholder="القيمة (SAR)" className="border-[#E8F4F3]" value={newOpp.potentialValue} onChange={(e) => setNewOpp({ ...newOpp, potentialValue: e.target.value })} />
                    <Input placeholder="Confidence" className="border-[#E8F4F3] w-24" value={newOpp.confidence} onChange={(e) => setNewOpp({ ...newOpp, confidence: Number(e.target.value) })} />
                  </div>
                  <div className="flex gap-2">
                    <Select value={newOpp.effort} onValueChange={(v) => setNewOpp({ ...newOpp, effort: v })}>
                      <SelectTrigger className="border-[#E8F4F3]"><SelectValue placeholder="الجهد" /></SelectTrigger>
                      <SelectContent>
                        <SelectItem value="low">منخفض</SelectItem>
                        <SelectItem value="medium">متوسط</SelectItem>
                        <SelectItem value="high">عالي</SelectItem>
                      </SelectContent>
                    </Select>
                    <Button size="sm" className="bg-[#15807A] hover:bg-[#0F5F5A]" onClick={() => createOpp.mutate(newOpp)}>أضف</Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}
