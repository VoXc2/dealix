import { Routes, Route } from 'react-router'
import LandingPage from './pages/LandingPage'
import Dashboard from './pages/Dashboard'
import Prospects from './pages/Prospects'
import Governance from './pages/Governance'
import Finance from './pages/Finance'
import Login from './pages/Login'
import NotFound from './pages/NotFound'
import { siteRoutes } from './siteRoutes'

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/prospects" element={<Prospects />} />
      <Route path="/governance" element={<Governance />} />
      <Route path="/finance" element={<Finance />} />
      <Route path="/login" element={<Login />} />
      {siteRoutes
        .filter((r) => r.path !== '/')
        .map((r) => (
          <Route key={r.path} path={r.path} element={r.element} />
        ))}
      <Route path="*" element={<NotFound />} />
    </Routes>
  )
}
