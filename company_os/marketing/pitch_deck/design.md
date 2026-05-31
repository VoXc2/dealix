# Dealix Pitch Deck — Visual Design Document

## 1. Profile Baseline Declaration

- **Profile selection**: `profiles/strategic.md`
- **Selection rationale**: Pitch deck for investors/funders — matches fundraising pitch scenario
- **Referenced dimensions**: Narrative framework (Problem → Solution → Product → Market → Advantage → Revenue → Roadmap → Governance → Financials → CTA), information density (medium-high), data persuasiveness, premium feel
- **Deviation notes**: Arabic content requires RTL layout consideration; Brand color is teal/emerald (#15807A) from Dealix identity

## 2. Style Baseline Declaration

- **Style anchor**: Sequoia Capital pitch deck style + McKinsey strategic report aesthetics
  - From Sequoia: Clean, confident, data-driven storytelling with big numbers
  - From McKinsey: Professional authority, strategic elevation, restrained elegance
- **Referenced dimensions**: Information hierarchy, data prominence, clean layouts, strategic narrative flow
- **Color temperature**: Cool-neutral with teal warmth — conveys both tech sophistication and trust

## 3. Style Details

### Color Design Principles
- **Overall tendency**: Conservative & steady with local highlights for key data
- **Temperature**: Cool-neutral
- **Primary**: #15807A (Dealix brand teal)
- **Background**: #0A1F1E (dark teal-black for emphasis pages), #FFFFFF (white for content pages)
- **Text dark**: #0A1F1E (headings), #1A2E2D (body)
- **Text light**: #FFFFFF (on dark), #8CB3B0 (secondary on dark)
- **Secondary**: #E8F4F3 (light teal tint for backgrounds/cards)
- **Accent**: #D4A843 (gold for key numbers, ROI, growth metrics — conveys premium)

### Font Usage
- **Title**: QuattrocentoSans Bold — powerful, authoritative
- **Body**: QuattrocentoSans — clear, readable
- **Big numbers**: QuattrocentoSans Bold at 48-60px
- **Arabic text**: System Arabic fonts (Noto Sans Arabic via system fallback)
- Font size hierarchy:
  - Cover title: 48px
  - Page title: 32px
  - Body: 20px (light content), 18px (moderate)
  - Big numbers: 56px
  - Annotations: 14px

### Text Box and Container Styles
- Content separation: Whitespace + font size differences primarily
- Cards: Sharp-cornered rectangles with subtle border (#E8F4F3)
- Dark pages: No cards, direct text on dark background
- Decorative: Thin lines (#15807A) as section dividers

### Image Style
- **Icons**: Outline style, teal color, used sparingly for key concepts
- **Tables**: Minimal style, teal header row, alternating subtle rows
- **Charts**: Teal color family, minimal gridlines, clean labels
- **Illustrations**: Abstract data visualization imagery, teal-toned

## 4. Layout System

### Global Layout
- Canvas: 1280x720px
- Page margins: 60px sides, 50px top/bottom
- RTL text direction for Arabic content
- Consistent: Logo top-right, page number bottom-left

### Special Pages
- **Cover**: Dark background (#0A1F1E), centered large title, gold accent, subtitle below
- **Final**: Dark background, centered CTA, contact info

### Content Pages
- **Title at top**: Full-width, 32px, bold
- **Layout patterns**:
  - Left-right split: Text left, visual/chart right
  - Three-column cards: For features/comparisons
  - Big numbers: Centered KPIs with supporting text
  - Timeline: Horizontal for roadmap

## 5. Style Usage Rules

- `title`: Page titles, cover title
- `subtitle`: Section headers, card titles
- `body`: Main content text
- `heading`: Big numbers, KPIs
- `caption`: Annotations, sources
- Primary color: Titles, icons, accents
- Accent (gold): Key numbers, growth metrics, CTAs
- Background: Page backgrounds
- Secondary: Card backgrounds, subtle fills

## 6. Risk Prohibitions

- [ ] No blue/cyan colors — stick to teal/gold palette
- [ ] No rounded rectangles — sharp corners for authority
- [ ] Body text never below 18px
- [ ] No generic stock photos
- [ ] No unsupported claims without data
- [ ] No flashy gradients or shadows
- [ ] Title font never below 28px
- [ ] Big numbers never below 44px
- [ ] Arabic text must be RTL-aligned

## 7. Theme Definition

```yaml
theme:
  colors:
    primary: "#15807A"
    secondary: "#E8F4F3"
    accent: "#D4A843"
    background: "#FFFFFF"
    text: "#0A1F1E"
  textStyles:
    title:
      fontSize: 32
      color: "$text"
      fontFamily: "QuattrocentoSans"
    subtitle:
      fontSize: 22
      color: "$primary"
      fontFamily: "QuattrocentoSans"
    body:
      fontSize: 20
      color: "$text"
      lineHeight: 1.6
      fontFamily: "QuattrocentoSans"
    heading:
      fontSize: 56
      color: "$accent"
      fontFamily: "QuattrocentoSans"
    caption:
      fontSize: 14
      color: "#8CB3B0"
      fontFamily: "QuattrocentoSans"
  tableStyles:
    default:
      headerFill: "$primary"
      headerColor: "#FFFFFF"
      headerBold: true
      bodyFill: ["#FFFFFF", "#F0F9F8"]
      bodyColor: "$text"
      border:
        style: solid
        width: 1
        color: "#E8F4F3"
```
