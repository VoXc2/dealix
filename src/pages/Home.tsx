import Hero from '../sections/Hero'
import Features from '../sections/Features'
import HowItWorks from '../sections/HowItWorks'
import Deliverables from '../sections/Deliverables'
import Pricing from '../sections/Pricing'
import Sectors from '../sections/Sectors'
import Proof from '../sections/Proof'
import CTA from '../sections/CTA'
import Footer from '../sections/Footer'

export default function Home() {
  return (
    <div className="min-h-screen bg-white" dir="rtl">
      <nav className="fixed top-0 left-0 right-0 z-50 bg-white/80 backdrop-blur-md border-b border-[#E8F4F3]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 bg-[#15807A] rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-sm">D</span>
              </div>
              <span className="text-xl font-bold text-[#0A1F1E]">Dealix</span>
            </div>
            <div className="hidden md:flex items-center gap-8">
              <a href="#features" className="text-sm text-[#4A6B69] hover:text-[#15807A] transition-colors">المميزات</a>
              <a href="#how" className="text-sm text-[#4A6B69] hover:text-[#15807A] transition-colors">كيف يعمل</a>
              <a href="#pricing" className="text-sm text-[#4A6B69] hover:text-[#15807A] transition-colors">الأسعار</a>
              <a href="#sectors" className="text-sm text-[#4A6B69] hover:text-[#15807A] transition-colors">القطاعات</a>
            </div>
            <a href="#cta" className="bg-[#15807A] text-white px-5 py-2 rounded-lg text-sm font-medium hover:bg-[#0F5F5A] transition-colors">
              احجز استشارة
            </a>
          </div>
        </div>
      </nav>

      <main>
        <Hero />
        <Features />
        <HowItWorks />
        <Deliverables />
        <Pricing />
        <Sectors />
        <Proof />
        <CTA />
      </main>

      <Footer />
    </div>
  )
}
