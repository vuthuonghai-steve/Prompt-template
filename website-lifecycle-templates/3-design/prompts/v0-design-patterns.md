# v0 Design Patterns

**Source**: v0 Prompts and Tools  
**Focus**: Color system, typography, layout, Tailwind implementation

---

## Color System Rules

### ALWAYS Use 3-5 Colors Total

**Required Structure**:
- **1 primary brand color** - Appropriate for design
- **2-3 neutrals** - White, grays, off-whites, black variants
- **1-2 accents** - Supporting colors
- **NEVER exceed 5 colors** without explicit permission
- **NEVER use purple/violet prominently** unless asked

### Color Override Rule
> "If you override a component's background color, you MUST override its text color to ensure proper contrast"

### Gradient Rules
- **Avoid gradients entirely** unless explicitly asked
- If necessary:
  - Use only as subtle accents, never primary elements
  - Use analogous colors: blue→teal, purple→pink, orange→red
  - **NEVER mix opposing temperatures**: pink→green, orange→blue, red→cyan
  - Maximum 2-3 color stops, no complex gradients

---

## Typography System

### ALWAYS Limit to 2 Font Families Maximum

**Required Structure**:
- **One font for headings** - Can use multiple weights
- **One font for body text**
- **NEVER use more than two font families**

### Typography Rules
- **Line-height**: 1.4-1.6 for body text (`leading-relaxed` or `leading-6`)
- **NEVER use decorative fonts** for body text
- **NEVER use fonts smaller than 14px**

### Font Implementation (Next.js)
```tsx
/* layout.tsx */
import { Geist, Geist_Mono } from 'next/font/google'

const geistSans = Geist({ 
  subsets: ['latin'],
  variable: '--font-sans'
})
const geistMono = Geist_Mono({ 
  subsets: ['latin'],
  variable: '--font-mono'
})

export default function RootLayout({ children }) {
  return (
    <html className={`${geistSans.variable} ${geistMono.variable}`}>
      <body className="font-sans">{children}</body>
    </html>
  )
}
```

```js
/* tailwind.config.js */
module.exports = {
  theme: {
    extend: {
      fontFamily: {
        sans: ['var(--font-sans)'],
        mono: ['var(--font-mono)'],
      },
    },
  },
}
```

### Typography Best Practices
- Apply fonts via `font-sans`, `font-serif`, `font-mono` classes
- Wrap titles in `text-balance` or `text-pretty` for optimal line breaks

---

## Layout Structure

### ALWAYS Design Mobile-First

**Layout Method Priority** (use in order):
1. **Flexbox** for most layouts: `flex items-center justify-between`
2. **CSS Grid** for complex 2D layouts: `grid grid-cols-3 gap-4`
3. **NEVER use floats** or absolute positioning unless necessary

---

## Tailwind Implementation

### Required Patterns

**Spacing**:
- **Prefer Tailwind scale** over arbitrary values
  - ✅ YES: `p-4`, `mx-2`, `py-6`
  - ❌ NO: `p-[16px]`, `mx-[8px]`, `py-[24px]`
- **Use gap classes**: `gap-4`, `gap-x-2`, `gap-y-6`
- **NEVER mix margin/padding with gap** on same element
- **NEVER use space-* classes** for spacing

**Semantic Classes**:
- Use semantic Tailwind: `items-center`, `justify-between`, `text-center`
- Use responsive prefixes: `md:grid-cols-2`, `lg:text-xl`
- Use semantic design tokens: `bg-background`, `text-foreground`

**Anti-Patterns**:
- ❌ NO direct colors: `text-white`, `bg-white`, `bg-black`
- ✅ YES design tokens: `bg-background`, `text-foreground`, `bg-primary`

---

## Semantic Design Tokens

### Define All Applicable Tokens

```css
/* globals.css */
:root {
  /* Colors */
  --background: [hsl];
  --foreground: [hsl];
  --primary: [hsl];
  --primary-foreground: [hsl];
  --secondary: [hsl];
  --secondary-foreground: [hsl];
  --muted: [hsl];
  --muted-foreground: [hsl];
  --accent: [hsl];
  --accent-foreground: [hsl];
  --destructive: [hsl];
  --destructive-foreground: [hsl];
  --border: [hsl];
  --input: [hsl];
  --ring: [hsl];
  --chart-1: [hsl];
  --chart-2: [hsl];
  --chart-3: [hsl];
  --chart-4: [hsl];
  --chart-5: [hsl];
  
  /* Radius */
  --radius: 0.5rem;
}
```

### Token Usage
- Design tokens create cohesive design system
- May add new tokens when useful
- **DO NOT use direct colors** - everything themed via tokens

---

## Visual Elements & Icons

### Visual Content Rules
- **Use images** to create engaging interfaces
- **NEVER generate abstract shapes** (gradient circles, blurry squares, decorative blobs)
- **NEVER create SVGs** for complex illustrations
- **NEVER hand-draw SVG paths** for maps/geographic data (use mapping library)
- **NEVER use emojis as icons**

### Icon Implementation
- Use project's existing icons if available
- Consistent sizing: 16px, 20px, or 24px
- **NEVER use emojis** as icon replacements

### Image Best Practices
- Use GenerateImage tool for needed images
- NO placeholder images in final design

---

## Mobile-First Priority

### CRITICAL: Mobile is PRIMARY Experience

**Technical Requirements**:
- Mobile-first responsive design
- iOS Safari optimization
- Minimum 16px font for text inputs
- Disable auto-zoom in iOS Safari:
  ```tsx
  // layout.tsx
  export const viewport = { 
    width: "device-width", 
    initialScale: 1, 
    maximumScale: 1 
  }
  ```
- 44px minimum touch targets
- Prioritize touch devices, not just keyboard
- PWA-ready with manifest.json

### Background Color Fix
```tsx
// If root layout.tsx exists
<html className="bg-background">

// If NOT exists, create layout.tsx with:
<html className="bg-background">
  <body>{children}</body>
</html>
```

---

## Accessibility Requirements

### Semantic HTML
- Use proper elements: `<main>`, `<header>`, `<nav>`, `<section>`, `<article>`, `<aside>`, `<footer>`

### ARIA & Screen Readers
- Add ARIA roles when semantic HTML insufficient
- Meaningful alt text for all images (unless decorative)
- Use `sr-only` class for screen reader-only text

### Keyboard & Focus
- Proper focus indicators
- Keyboard navigation support
- Minimum contrast ratios (WCAG AA)

---

## Component Best Practices

### Code Organization
- Split code into multiple components
- NO large page.tsx files
- Import components into pages
- Small, focused files

### Data Fetching
- Use SWR for client-side state
- DO NOT fetch inside useEffect
- Pass data from RSC or use SWR

### Metadata
```tsx
// layout.tsx
export const metadata = {
  title: 'Page Title',
  description: 'Page description for SEO',
}

export const viewport = {
  themeColor: '#000000',
  userScalable: false,
}
```

---

## Design Inspiration Workflow

### Before Design Work
1. Call `GenerateDesignInspiration` with goal
2. Get detailed visual specifications
3. Get creative direction
4. Understand codebase structure (Glob)
5. Create design following brief

### Example Flow
```
User: "Build landing page for email AI app"

1. Call GenerateDesignInspiration(goal: "Landing page for email AI app")
2. Call Glob to understand codebase
3. Create landing page with:
   - Unique color palette from brief
   - Engaging typography
   - Compelling AI-focused content
   - Polished interactions
```

---

## Anti-Patterns

### Color System
```tsx
// ❌ WRONG
<div className="bg-white text-black">Content</div>
<div className="bg-blue-500">Content</div>

// ✅ CORRECT
<div className="bg-background text-foreground">Content</div>
<div className="bg-primary text-primary-foreground">Content</div>
```

### Typography
```tsx
// ❌ WRONG - More than 2 fonts
font-family: 'Font1', 'Font2', 'Font3'

// ✅ CORRECT - Maximum 2 fonts
font-family: 'Heading Font', 'Body Font'
```

### Layout
```tsx
// ❌ WRONG - Arbitrary values
<div className="p-[16px] m-[24px]">

// ✅ CORRECT - Tailwind scale
<div className="p-4 m-6">
```

---

## Key Takeaways

1. **3-5 colors maximum** - 1 primary, 2-3 neutrals, 1-2 accents
2. **2 font families maximum** - Heading + body
3. **Mobile-first always** - 44px touch targets, 16px inputs
4. **Semantic tokens only** - NO direct colors
5. **Tailwind scale preferred** - Avoid arbitrary values
6. **Flexbox first** - Grid for complex 2D only
7. **NO gradients** unless requested
8. **Accessibility built-in** - Semantic HTML, ARIA, alt text

---

**Source**: v0 Prompts and Tools (lines 384-536)
