import { Routes, Route } from 'react-router'
import LandingPage from './pages/LandingPage'
import Systems from './pages/Systems'
import SystemDetail from './pages/SystemDetail'
import Pricing from './pages/Pricing'
import Diagnostic from './pages/Diagnostic'
import Start from './pages/Start'
import Dashboard from './pages/Dashboard'
import Prospects from './pages/Prospects'
import Governance from './pages/Governance'
import Finance from './pages/Finance'
import Login from './pages/Login'
import NotFound from './pages/NotFound'

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route path="/systems" element={<Systems />} />
      <Route path="/systems/:slug" element={<SystemDetail />} />
      <Route path="/pricing" element={<Pricing />} />
      <Route path="/diagnostic" element={<Diagnostic />} />
      <Route path="/start" element={<Start />} />
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/prospects" element={<Prospects />} />
      <Route path="/governance" element={<Governance />} />
      <Route path="/finance" element={<Finance />} />
      <Route path="/login" element={<Login />} />
      <Route path="*" element={<NotFound />} />
    </Routes>
  )
}
