import { createElement } from 'react';
import Script from 'next/script';

export const metadata = {
  title: 'Dealix | Market to Delivery',
  description: 'Research hypotheses and a browser-local diagnostic intake draft. Not approved offers.',
  robots: { index: false, follow: false },
};

export default function ServiceCatalogPage() {
  return (
    <main>
      {createElement('dealix-catalog-workspace')}
      <noscript>This research catalog requires JavaScript. No request has been submitted.</noscript>
      <Script src="/market-to-delivery-workspace.js" strategy="afterInteractive" />
    </main>
  );
}
