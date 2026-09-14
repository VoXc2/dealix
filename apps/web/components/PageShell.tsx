import type { ReactNode } from "react";
import Nav from "./Nav";
import Footer from "./Footer";

// Note: TopInfoBar + skip link render once in app/layout.tsx for all pages.
export default function PageShell({ children }: { children: ReactNode }) {
  return (
    <>
      <Nav />
      <main id="main-content">{children}</main>
      <Footer />
    </>
  );
}
