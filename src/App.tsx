import { Routes, Route } from 'react-router'
import LandingPage from './pages/LandingPage'
import Dashboard from './pages/Dashboard'
import Prospects from './pages/Prospects'
import Governance from './pages/Governance'
import Finance from './pages/Finance'
import Login from './pages/Login'
import NotFound from './pages/NotFound'
import Systems from './pages/marketing/Systems'
import SystemDetail from './pages/marketing/SystemDetail'
import Pricing from './pages/marketing/Pricing'
import Diagnostic from './pages/marketing/Diagnostic'
import Start from './pages/marketing/Start'
import Contact from './pages/marketing/Contact'
import Resources from './pages/marketing/Resources'
import Partners from './pages/marketing/Partners'

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />
      {/* Marketing / acquisition site */}
      <Route path="/systems" element={<Systems />} />
      <Route path="/systems/:slug" element={<SystemDetail />} />
      <Route path="/pricing" element={<Pricing />} />
      <Route path="/diagnostic" element={<Diagnostic />} />
      <Route path="/start" element={<Start />} />
      <Route path="/contact" element={<Contact />} />
      <Route path="/resources" element={<Resources />} />
      <Route path="/partners" element={<Partners />} />
      {/* Internal app */}
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/prospects" element={<Prospects />} />
      <Route path="/governance" element={<Governance />} />
      <Route path="/finance" element={<Finance />} />
      <Route path="/login" element={<Login />} />
      <Route path="*" element={<NotFound />} />
    </Routes>
  )
}
