import { Link } from "react-router";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Zap, Shield, TrendingUp, Lock, FileText, MessageSquare, Target, CheckCircle, ArrowRight, Sparkles, Eye, BrainCircuit } from "lucide-react";

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-white" dir="rtl">
      <nav className="border-b bg-white/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2"><div className="w-8 h-8 bg-gradient-to-br from-emerald-500 to-teal-600 rounded-lg flex items-center justify-center"><Zap className="w-5 h-5 text-white" /></div><span className="text-xl font-bold text-gray-900">Dealix</span></div>
          <div className="hidden md:flex items-center gap-6"><Link to="/systems" className="text-sm text-gray-600 hover:text-gray-900">الأنظمة</Link><Link to="/pricing" className="text-sm text-gray-600 hover:text-gray-900">الأسعار</Link><a href="#governance" className="text-sm text-gray-600 hover:text-gray-900">الحوكمة</a></div>
          <div className="flex gap-3"><Link to="/login"><Button variant="outline" size="sm">تسجيل الدخول</Button></Link><Link to="/dashboard"><Button size="sm" className="gap-2">ابدأ<ArrowRight className="w-4 h-4" /></Button></Link></div>
        </div>
      </nav>

      <section className="relative pt-20 pb-32 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-emerald-50 via-white to-teal-50" />
        <div className="relative max-w-7xl mx-auto px-4 text-center">
          <Badge className="mb-6 px-4 py-2 bg-emerald-100 text-emerald-800 hover:bg-emerald-100"><Sparkles className="w-4 h-4 ml-2" />نظام تشغيل الإيرادات المدعوم بالذكاء الاصطناعي</Badge>
          <h1 className="text-5xl md:text-7xl font-bold text-gray-900 mb-6 leading-tight">كُشف أين تضيع<br /><span className="bg-gradient-to-r from-emerald-600 to-teal-600 bg-clip-text text-transparent">إيرادات شركتك</span></h1>
          <p className="text-xl text-gray-600 mb-10 max-w-3xl mx-auto leading-relaxed">Dealix يساعد الشركات في السعودية والخليج على كشف ضياع الإيرادات، تنظيم المتابعات، تحسين المبيعات، وتشغيل War Room تنفيذي مدعوم بالذكاء الاصطناعي مع حوكمة وإثبات واضح.</p>
          <div className="flex gap-4 justify-center"><Link to="/dashboard"><Button size="lg" className="text-lg px-8 gap-2">ابدأ Sprint مجاني<ArrowRight className="w-5 h-5" /></Button></Link></div>
        </div>
      </section>

      <section id="features" className="py-24">
        <div className="max-w-7xl mx-auto px-4">
          <div className="text-center mb-16"><h2 className="text-4xl font-bold text-gray-900 mb-4">لماذا Dealix مختلف؟</h2><p className="text-lg text-gray-600 max-w-2xl mx-auto">لا نبيع أدوات. نبيع نظام تشغيل إيرادات كامل مع حوكمة وإثبات.</p></div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[{icon: Eye, title: "كشف تسرب الإيرادات", desc: "خريطة دقيقة توضح أين تضيع الفرص"}, {icon: MessageSquare, title: "تدقيق المتابعات", desc: "تحليل كامل لسرعة الرد والفرص المفقودة"}, {icon: FileText, title: "Proof Pack شهري", desc: "تقرير تنفيذي يثبت القيمة"}, {icon: Shield, title: "حوكمة كاملة", desc: "AI drafts, Human approves, System logs"}, {icon: Target, title: "Executive War Room", desc: "لوحة تحكم يومية"}, {icon: TrendingUp, title: "تحسين مستمر", desc: "تحليل الاعتراضات ورفع معدلات التحويل"}].map((f, i) => <Card key={i} className="hover:shadow-lg border-0 shadow-md"><CardHeader><div className="w-12 h-12 bg-emerald-100 rounded-xl flex items-center justify-center mb-4"><f.icon className="w-6 h-6 text-emerald-600" /></div><CardTitle className="text-xl">{f.title}</CardTitle></CardHeader><CardContent><p className="text-gray-600">{f.desc}</p></CardContent></Card>)}
          </div>
        </div>
      </section>

      <section id="pricing" className="py-24 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4">
          <div className="text-center mb-16"><h2 className="text-4xl font-bold text-gray-900 mb-4">الأسعار</h2></div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto">
            <Card className="border-0 shadow-lg"><CardHeader className="text-center pb-2"><CardTitle className="text-lg text-gray-600">Sprint Basic</CardTitle><div className="text-4xl font-bold text-gray-900 mt-2">2,500 <span className="text-lg font-normal">ر.س</span></div></CardHeader><CardContent><ul className="space-y-3">{["تحليل 10 عملاء", "تقرير تسرب الإيرادات", "تدقيق المتابعة", "خطة 30 يوم"].map((item, i) => <li key={i} className="flex items-center gap-2"><CheckCircle className="w-4 h-4 text-emerald-500" /><span className="text-sm">{item}</span></li>)}</ul><Button className="w-full mt-6" variant="outline">اختر</Button></CardContent></Card>
            <Card className="border-2 border-emerald-500 shadow-xl relative"><Badge className="absolute -top-3 left-1/2 -translate-x-1/2 bg-emerald-500">الأكثر شيوعاً</Badge><CardHeader className="text-center pb-2"><CardTitle className="text-lg text-gray-600">Sprint Standard</CardTitle><div className="text-4xl font-bold text-emerald-600 mt-2">5,000 <span className="text-lg font-normal">ر.س</span></div></CardHeader><CardContent><ul className="space-y-3">{["تحليل 25 عميل", "Proof Pack كامل", "CEO Brief", "خطة مفصلة"].map((item, i) => <li key={i} className="flex items-center gap-2"><CheckCircle className="w-4 h-4 text-emerald-500" /><span className="text-sm">{item}</span></li>)}</ul><Button className="w-full mt-6">اختر</Button></CardContent></Card>
            <Card className="border-0 shadow-lg bg-gradient-to-b from-gray-900 to-gray-800 text-white"><CardHeader className="text-center pb-2"><CardTitle className="text-lg text-gray-300">AI Retainer</CardTitle><div className="text-4xl font-bold text-white mt-2">3,000+ <span className="text-lg font-normal">ر.س/شهر</span></div></CardHeader><CardContent><ul className="space-y-3">{["War Room أسبوعي", "مراجعة Pipeline", "Proof Pack شهري", "تحسين الرسائل"].map((item, i) => <li key={i} className="flex items-center gap-2"><CheckCircle className="w-4 h-4 text-emerald-400" /><span className="text-sm">{item}</span></li>)}</ul><Button className="w-full mt-6 bg-emerald-500 hover:bg-emerald-600">تواصل</Button></CardContent></Card>
          </div>
        </div>
      </section>

      <section id="governance" className="py-24">
        <div className="max-w-7xl mx-auto px-4">
          <div className="text-center mb-16"><h2 className="text-4xl font-bold text-gray-900 mb-4">حوكمة الذكاء الاصطناعي</h2></div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <Card><CardContent className="p-8"><div className="flex items-center gap-4 mb-6"><div className="w-14 h-14 bg-emerald-100 rounded-xl flex items-center justify-center"><Shield className="w-7 h-7 text-emerald-600" /></div><div><h3 className="text-xl font-bold">AI drafts. Human approves.</h3></div></div><div className="space-y-3">{["كل إجراء مسجل", "قائمة موافقات", "امتثال SDAIA", "حماية البيانات PDPL"].map((item, i) => <div key={i} className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg"><Lock className="w-5 h-5 text-emerald-500" /><span>{item}</span></div>)}</div></CardContent></Card>
            <Card><CardContent className="p-8"><div className="flex items-center gap-4 mb-6"><div className="w-14 h-14 bg-blue-100 rounded-xl flex items-center justify-center"><BrainCircuit className="w-7 h-7 text-blue-600" /></div><div><h3 className="text-xl font-bold">نموذج الصلاحيات</h3></div></div><div className="space-y-2">{[{l: "Level 1: Observe", a: true}, {l: "Level 2: Advise", a: true}, {l: "Level 3: Draft", a: true}, {l: "Level 4: Act with Approval", a: false}, {l: "Level 5: Autonomous", a: false}].map((level, i) => <div key={i} className={`flex justify-between p-3 rounded-lg ${level.a ? 'bg-emerald-50' : 'bg-gray-50'}`}><span className={level.a ? 'font-medium' : 'text-gray-500'}>{level.l}</span><Badge variant={level.a ? "default" : "outline"} className={level.a ? "bg-emerald-500" : ""}>{level.a ? "نشط" : "قريباً"}</Badge></div>)}</div></CardContent></Card>
          </div>
        </div>
      </section>

      <section className="py-24 bg-gradient-to-br from-emerald-600 to-teal-700">
        <div className="max-w-4xl mx-auto px-4 text-center">
          <h2 className="text-4xl font-bold text-white mb-6">Dealix لا يحتاج مزيد أفكار الآن</h2>
          <p className="text-xl text-emerald-100 mb-10">يحتاج أول عميل مدفوع، أول Proof Pack، وأول Retainer.<br />هذا هو التحول الحقيقي من مشروع إلى شركة.</p>
          <Link to="/dashboard"><Button size="lg" className="bg-white text-emerald-700 hover:bg-emerald-50 text-lg px-10">ابدأ الآن<ArrowRight className="w-5 h-5 mr-2" /></Button></Link>
        </div>
      </section>

      <footer className="bg-gray-900 text-gray-400 py-16">
        <div className="max-w-7xl mx-auto px-4">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div><div className="flex items-center gap-2 mb-4"><div className="w-8 h-8 bg-gradient-to-br from-emerald-500 to-teal-600 rounded-lg flex items-center justify-center"><Zap className="w-5 h-5 text-white" /></div><span className="text-xl font-bold text-white">Dealix</span></div><p className="text-sm">نظام تشغيل إيرادات مدعوم بالذكاء الاصطناعي للسعودية والخليج.</p></div>
            <div><h4 className="text-white font-medium mb-4">الأنظمة الخمسة</h4><ul className="space-y-2 text-sm"><li><Link to="/systems/revenue-operating-system" className="hover:text-white">Revenue Operating System</Link></li><li><Link to="/systems/executive-command-os" className="hover:text-white">Executive Command OS</Link></li><li><Link to="/systems/follow-up-recovery-os" className="hover:text-white">Follow-up Recovery OS</Link></li><li><Link to="/systems/whatsapp-client-os" className="hover:text-white">WhatsApp Client OS</Link></li><li><Link to="/systems/proposal-proof-os" className="hover:text-white">Proposal & Proof OS</Link></li></ul></div>
            <div><h4 className="text-white font-medium mb-4">النظام</h4><ul className="space-y-2 text-sm"><li><Link to="/dashboard" className="hover:text-white">لوحة التحكم</Link></li><li><Link to="/prospects" className="hover:text-white">العملاء</Link></li><li><Link to="/governance" className="hover:text-white">الحوكمة</Link></li><li><Link to="/finance" className="hover:text-white">المالية</Link></li></ul></div>
            <div><h4 className="text-white font-medium mb-4">القطاعات</h4><ul className="space-y-2 text-sm"><li>وكالات التسويق</li><li>شركات التدريب</li><li>B2B Services</li></ul></div>
          </div>
          <div className="border-t border-gray-800 mt-12 pt-8 text-center text-sm"><p>&copy; 2026 Dealix. جميع الحقوق محفوظة.</p></div>
        </div>
      </footer>
    </div>
  );
}
