import { useEffect, type ReactNode } from 'react'
import { useLocation } from 'react-router'
import SiteNav from './SiteNav'
import SiteFooter from './SiteFooter'

// Shared RTL marketing layout. Scrolls to top on route change so deep links and
// in-app navigation always start at the hero.
export default function SiteLayout({ children }: { children: ReactNode }) {
  const { pathname } = useLocation()
  useEffect(() => {
    window.scrollTo(0, 0)
  }, [pathname])

  return (
    <div className="min-h-screen bg-white flex flex-col" dir="rtl">
      <SiteNav />
      <main className="flex-1">{children}</main>
      <SiteFooter />
    </div>
  )
}
