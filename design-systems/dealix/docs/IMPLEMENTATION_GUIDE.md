# DEALIX Design System - Implementation Guide

## 🚀 Quick Start

This guide covers how to integrate the complete Dealix design system into your Next.js / React project.

---

## 📁 File Structure

You've received the following files:

```
dealix-design/
├── DEALIX_BRAND_GUIDELINES.md    # Complete brand guidelines
├── DEALIX_DESIGN_SYSTEM.md       # Design system specifications
├── dealix-styles.css              # Production CSS stylesheet
├── dealix-style-guide.html        # Interactive style guide
├── DealixComponents.tsx           # React component library
└── IMPLEMENTATION_GUIDE.md        # This file
```

---

## 📦 Installation Steps

### 1. Copy CSS File

Copy `dealix-styles.css` to your project:

```bash
cp dealix-styles.css src/styles/
```

### 2. Import in Your Main Layout

In your Next.js app, import the CSS in your root layout:

```tsx
// app/layout.tsx or pages/_app.tsx
import '@/styles/dealix-styles.css'

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        {children}
      </body>
    </html>
  )
}
```

### 3. Copy React Components

Copy `DealixComponents.tsx` to your components directory:

```bash
cp DealixComponents.tsx src/components/dealix/
```

### 4. Use Components in Your Code

```tsx
import {
  Button,
  Card,
  Input,
  Navbar,
  Container,
} from '@/components/dealix/DealixComponents'

export default function Dashboard() {
  return (
    <Container>
      <Navbar
        brand="Dealix"
        logo="◆"
        items={[
          { label: 'Dashboard', href: '/dashboard', active: true },
          { label: 'Clients', href: '/clients' },
          { label: 'Reports', href: '/reports' },
        ]}
      />

      <Card>
        <h2>Welcome to Dealix</h2>
        <p>Your AI Revenue Operations System</p>
        <Button variant="primary">Get Started</Button>
      </Card>
    </Container>
  )
}
```

---

## 🎨 Color System

### Using Colors in Components

```tsx
// As CSS classes
<div className="bg-navy text-white">Navy Background</div>
<div className="text-gold">Gold Text</div>

// As inline styles
<div style={{ color: 'var(--color-navy)' }}>Navy Text</div>
<div style={{ backgroundColor: 'var(--color-gold)' }}>Gold Background</div>
```

### Available Color Variables

```css
--color-navy: #001F3F
--color-gold: #D4AF37
--color-black: #0A0A0A
--color-white: #FFFFFF
--color-slate: #364558
--color-ocean: #0066FF
--color-emerald: #10B981
--color-coral: #EF4444
--color-amber: #F59E0B
--color-light-gray: #F3F4F6
```

---

## 🔤 Typography

### Using Font Families

```tsx
// Display fonts (Headlines)
<h1 style={{ fontFamily: 'var(--font-display)' }}>
  Premium Headline
</h1>

// Body fonts
<p style={{ fontFamily: 'var(--font-body)' }}>
  Regular paragraph text
</p>

// Monospace fonts
<code style={{ fontFamily: 'var(--font-mono)' }}>
  const code = "example"
</code>
```

### Typography Classes

```tsx
<h1 className="text-h1">Heading 1</h1>
<h2 className="text-h2">Heading 2</h2>
<h3 className="text-h3">Heading 3</h3>
<p className="text-body">Body text</p>
<p className="text-caption">Caption text</p>
```

---

## 🎯 Component Usage Examples

### Button

```tsx
import { Button } from '@/components/dealix/DealixComponents'

// Primary button
<Button variant="primary">Submit</Button>

// Secondary button
<Button variant="secondary">Cancel</Button>

// Accent button
<Button variant="accent">Premium Action</Button>

// Disabled state
<Button variant="primary" disabled>Disabled</Button>

// Different sizes
<Button size="sm">Small</Button>
<Button size="md">Medium</Button>
<Button size="lg">Large</Button>
<Button size="xl">Extra Large</Button>

// Full width
<Button block>Full Width Button</Button>

// With icon
<Button icon="🚀">Launch</Button>
```

### Card

```tsx
import { Card } from '@/components/dealix/DealixComponents'

// Simple card
<Card>
  <h3>Card Title</h3>
  <p>Card content goes here</p>
</Card>

// Card with header
<Card
  header={<h3>Card Header</h3>}
  icon="📊"
>
  Card content
</Card>

// Card variants
<Card variant="elevated">Elevated Card</Card>
<Card variant="navy">Dark Card</Card>
<Card variant="bordered">Bordered Card</Card>

// Card with footer
<Card
  footer={
    <Button variant="primary" size="sm">
      Learn More
    </Button>
  }
>
  Card with action button
</Card>
```

### Input

```tsx
import { Input } from '@/components/dealix/DealixComponents'

// Basic input
<Input placeholder="Enter email" />

// With label
<Input
  label="Email Address"
  placeholder="you@example.com"
  type="email"
/>

// With error state
<Input
  label="Password"
  type="password"
  variant="error"
  error="Password must be at least 8 characters"
/>

// With success state
<Input
  label="Username"
  variant="success"
  value="johndoe"
/>

// With hint
<Input
  label="Website"
  hint="Include the full URL (https://...)"
  placeholder="https://example.com"
/>

// With icon
<Input
  label="Search"
  placeholder="Search..."
  icon="🔍"
  iconPosition="left"
/>
```

### Modal

```tsx
import { Modal, Button } from '@/components/dealix/DealixComponents'
import { useState } from 'react'

export default function MyComponent() {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <>
      <Button onClick={() => setIsOpen(true)}>Open Modal</Button>

      <Modal
        isOpen={isOpen}
        onClose={() => setIsOpen(false)}
        title="Confirm Action"
        footer={
          <>
            <Button
              variant="secondary"
              onClick={() => setIsOpen(false)}
            >
              Cancel
            </Button>
            <Button
              variant="primary"
              onClick={() => {
                // Handle action
                setIsOpen(false)
              }}
            >
              Confirm
            </Button>
          </>
        }
      >
        <p>Are you sure you want to proceed with this action?</p>
      </Modal>
    </>
  )
}
```

### Navbar

```tsx
import { Navbar, Button } from '@/components/dealix/DealixComponents'

<Navbar
  brand="Dealix"
  logo="◆"
  items={[
    { label: 'Dashboard', href: '/dashboard', active: true },
    { label: 'Clients', href: '/clients' },
    { label: 'Reports', href: '/reports' },
    { label: 'Settings', href: '/settings' },
  ]}
  actions={
    <>
      <Button variant="secondary" size="sm">
        Profile
      </Button>
      <Button variant="accent" size="sm">
        Upgrade
      </Button>
    </>
  }
/>
```

### Grid Layout

```tsx
import { Grid, Container } from '@/components/dealix/DealixComponents'
import { Card } from '@/components/dealix/DealixComponents'

<Container>
  <Grid columns={3} gap="lg">
    <Card>Card 1</Card>
    <Card>Card 2</Card>
    <Card>Card 3</Card>
    <Card>Card 4</Card>
    <Card>Card 5</Card>
    <Card>Card 6</Card>
  </Grid>
</Container>
```

### Form Example

```tsx
import { Form, Input, Button, Container } from '@/components/dealix/DealixComponents'
import { useState } from 'react'

export default function LoginForm() {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  })

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    console.log('Form submitted:', formData)
  }

  return (
    <Container>
      <Form onSubmit={handleSubmit}>
        <Input
          label="Email"
          type="email"
          placeholder="you@example.com"
          value={formData.email}
          onChange={(e) =>
            setFormData({ ...formData, email: e.target.value })
          }
        />

        <Input
          label="Password"
          type="password"
          placeholder="••••••••"
          value={formData.password}
          onChange={(e) =>
            setFormData({ ...formData, password: e.target.value })
          }
        />

        <Button type="submit" variant="primary" block>
          Sign In
        </Button>
      </Form>
    </Container>
  )
}
```

---

## 📐 Grid System & Spacing

### Container

```tsx
import { Container } from '@/components/dealix/DealixComponents'

<Container>
  {/* Max-width 1440px, responsive padding */}
  <h1>Page Title</h1>
</Container>
```

### Grid

```tsx
// CSS Grid classes
<div className="grid">
  <div className="col-6">Half width</div>
  <div className="col-6">Half width</div>
</div>

<div className="grid">
  <div className="col-4">One third</div>
  <div className="col-4">One third</div>
  <div className="col-4">One third</div>
</div>

// Responsive
<div className="grid">
  <div className="col-12 col-6-md col-4-lg">
    Responsive width
  </div>
</div>
```

### Spacing Classes

```tsx
// Margin utilities
<div className="m-4">Margin 16px on all sides</div>
<div className="mt-6">Margin-top 24px</div>
<div className="mb-2">Margin-bottom 8px</div>
<div className="mx-auto">Auto horizontal margin</div>

// Padding utilities
<div className="p-4">Padding 16px</div>
<div className="px-4">Horizontal padding</div>
<div className="py-6">Vertical padding</div>
```

### Gap Utilities

```tsx
<div className="flex gap-4">
  {/* 16px gap between flex items */}
</div>

<div className="grid grid--gap-8">
  {/* 32px gap between grid items */}
</div>
```

---

## 🎬 Animations

### Built-in Animations

```tsx
// Fade in
<div style={{ animation: 'fadeIn 300ms ease' }}>
  Content fades in
</div>

// Slide up
<div style={{ animation: 'slideUp 300ms ease' }}>
  Content slides up
</div>

// Pulse
<div style={{ animation: 'pulse 2s infinite' }}>
  Pulsing content
</div>

// Using animation classes
<div className="animate-fade-in">Fade in content</div>
<div className="animate-slide-up">Slide up content</div>
<div className="animate-pulse">Pulsing content</div>
```

---

## ♿ Accessibility

### Screen Reader Only Content

```tsx
<div className="sr-only">
  Screen reader only text
</div>
```

### Focus Management

All interactive elements have proper focus states:

```tsx
button:focus-visible {
  outline: 2px solid var(--color-gold);
  outline-offset: 2px;
}
```

### Reduced Motion

The design system respects `prefers-reduced-motion`:

```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
  }
}
```

---

## 🌍 RTL Support (Arabic)

For right-to-left languages, add `dir="rtl"` to your HTML:

```html
<html dir="rtl" lang="ar">
  <body>
    <!-- Arabic content -->
  </body>
</html>
```

Typography automatically adjusts:
- Line-height increases for Arabic
- Letter-spacing optimized for Arabic script

---

## 📱 Responsive Design

### Breakpoints

```css
--breakpoint-sm: 480px;
--breakpoint-md: 768px;
--breakpoint-lg: 1024px;
--breakpoint-xl: 1440px;
```

### Responsive Classes

```tsx
<div className="hide-mobile">Hidden on mobile</div>
<div className="show-mobile">Visible only on mobile</div>

// Grid responsive
<div className="grid">
  <div className="col-4">
    Full width mobile, 1/3 desktop
  </div>
</div>
```

---

## 🔧 Customization

### Override CSS Variables

```css
:root {
  /* Override primary color */
  --color-navy: #001a2e;
  
  /* Override fonts */
  --font-display: 'Your Font', sans-serif;
  
  /* Override spacing */
  --space-4: 18px;
}
```

### Add Custom Styles

```css
/* app.css */
@import 'dealix-styles.css';

/* Your custom styles */
.custom-section {
  background: linear-gradient(
    135deg,
    var(--color-navy),
    var(--color-gold)
  );
  color: white;
  padding: var(--space-8);
}
```

---

## 🚀 Next.js Specific Setup

### 1. app/layout.tsx

```tsx
import '@/styles/dealix-styles.css'

export const metadata = {
  title: 'Dealix - AI Revenue Operations',
  description: 'Premium B2B revenue platform',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <head>
        {/* Font imports */}
        <link
          href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap"
          rel="stylesheet"
        />
      </head>
      <body>{children}</body>
    </html>
  )
}
```

### 2. lib/components.ts (Export all components)

```tsx
export {
  Button,
  Card,
  Input,
  Modal,
  Navbar,
  Container,
  Grid,
  Flex,
  // ... other components
} from '@/components/dealix/DealixComponents'
```

### 3. Use throughout your app

```tsx
import { Button, Card, Container } from '@/lib/components'

export default function Page() {
  return (
    <Container>
      <Card>
        <h1>Welcome</h1>
        <Button>Get Started</Button>
      </Card>
    </Container>
  )
}
```

---

## 📚 Documentation Files

### DEALIX_BRAND_GUIDELINES.md
Complete brand identity, voice, tone, and usage guidelines. Use this when:
- Creating marketing materials
- Writing copy for the platform
- Designing new features
- Onboarding new team members

### DEALIX_DESIGN_SYSTEM.md
Technical specifications for all components. Reference this for:
- Component variations
- Color codes
- Typography specifications
- Spacing rules

---

## 🎓 Best Practices

1. **Use CSS Variables**: Always use `var(--color-navy)` instead of hardcoding colors
2. **Semantic HTML**: Use proper HTML tags (`<button>`, `<nav>`, etc.)
3. **Accessibility**: Always include alt text, labels, and ARIA attributes
4. **Mobile First**: Design for mobile first, enhance for larger screens
5. **Consistency**: Follow the component API in the library
6. **Performance**: Use CSS classes over inline styles when possible
7. **Type Safety**: Use TypeScript interfaces for React components

---

## 🐛 Troubleshooting

### CSS Not Loading

- Ensure `dealix-styles.css` is imported before other stylesheets
- Check file path is correct
- Clear browser cache

### Components Not Styling

- Verify CSS is imported in root layout
- Check class names match component names
- Ensure no conflicting CSS rules

### Font Not Loading

- Add font imports to your HTML head
- Use system fonts as fallback
- Check font weight values (300, 400, 500, 600, 700)

---

## 📞 Support

For questions or issues with the design system:

1. Check DEALIX_BRAND_GUIDELINES.md
2. Review DEALIX_DESIGN_SYSTEM.md
3. Examine component examples above
4. Check component TypeScript interfaces

---

## ✅ Next Steps

1. ✅ Copy files to your project
2. ✅ Import CSS in root layout
3. ✅ Copy React components
4. ✅ Import components where needed
5. ✅ Start building with Dealix design system!

**Your design system is ready. Build something amazing! 🚀**

