import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Dealix - منصة إدارة الصفقات والتسويق بالعمولة',
  description: 'منصة متكاملة لإدارة الصفقات، تتبع العملاء المحتملين، وإدارة برامج التسويق بالعمولة في السوق السعودي',
  keywords: ['صفقات', 'تسويق بالعمولة', 'إدارة مبيعات', 'السعودية', 'Dealix'],
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ar" dir="rtl">
      <head>
        <link rel="icon" href="/favicon.ico" />
      </head>
      <body className="min-h-screen bg-gray-50">
        {children}
      </body>
    </html>
  );
}
