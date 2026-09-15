"use client";

import Link from "next/link";

const links = [
  { href: "/company", label: "الشركة" },
  { href: "/services", label: "الخدمات" },
  { href: "/sectors", label: "القطاعات" },
  { href: "/products", label: "المنتجات" },
  { href: "/dealix-os", label: "Dealix OS" },
  { href: "/cases", label: "Proof" },
];

export default function Nav() {
  return (
    <nav className="navbar" aria-label="Primary navigation">
      <Link href="/" className="navbar-brand brand-logo-link" aria-label="Dealix Home">
        <img className="brand-logo" src="/dealix-logo-white.svg" alt="Dealix" width="178" height="43" />
      </Link>
      <ul className="navbar-links" role="list">
        {links.map((link) => <li key={link.href}><Link href={link.href}>{link.label}</Link></li>)}
      </ul>
      <div className="actions nav-actions">
        <details className="mobile-menu">
          <summary aria-label="فتح قائمة التنقل"><span aria-hidden="true">☰</span><span>القائمة</span></summary>
          <div className="mobile-menu-panel">
            {links.map((link) => <Link key={link.href} href={link.href}>{link.label}</Link>)}
            <Link href="/safety">الحوكمة</Link>
          </div>
        </details>
        <Link href="/safety" className="btn btn-ghost nav-secondary-action">الحوكمة</Link>
        <Link href="/book" className="nav-primary-action"><span className="nav-primary-full">التشخيص المجاني</span><span className="nav-primary-short">تشخيص</span></Link>
      </div>
    </nav>
  );
}
