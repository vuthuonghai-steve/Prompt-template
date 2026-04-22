# Pattern: Typography System (Max 2 Fonts)

## Problem
Too many fonts → visual chaos, slow loading, inconsistent hierarchy.

## Solution
Limit to MAXIMUM 2 font families: 1 for headings + 1 for body text.

**Core principles:**
- Maximum 2 font families total
- One for headings (multiple weights OK)
- One for body text
- Never decorative fonts for body text
- Never fonts < 14px for decorative fonts

## Example

### ✅ Good: 2 Font System
```typescript
// layout.tsx
import { Inter, Playfair_Display } from 'next/font/google'

const inter = Inter({ subsets: ['latin'] })
const playfair = Playfair_Display({ subsets: ['latin'] })

// tailwind.config.ts
fontFamily: {
  sans: ['var(--font-inter)'],    // Body text
  serif: ['var(--font-playfair)'], // Headings
}
```

```tsx
// Usage
<h1 className="font-serif text-4xl">Heading</h1>
<p className="font-sans text-base">Body text</p>
```

### ❌ Bad: Too Many Fonts
```typescript
// DON'T do this
import { Inter, Playfair, Roboto, Montserrat } from 'next/font/google'

// 4 fonts = chaos + slow loading
```

## Typography Implementation

### 1. Line Height
```css
/* Body text: 1.4-1.6 */
.body-text {
  line-height: 1.5; /* or leading-relaxed, leading-6 */
}

/* Headings: 1.1-1.3 */
.heading {
  line-height: 1.2; /* or leading-tight */
}
```

### 2. Font Sizes
```typescript
// Tailwind scale
text-xs:   12px
text-sm:   14px
text-base: 16px  // Default body
text-lg:   18px
text-xl:   20px
text-2xl:  24px
text-3xl:  30px
text-4xl:  36px
```

### 3. Font Weights
```typescript
// Use multiple weights of same family
font-light:    300
font-normal:   400
font-medium:   500
font-semibold: 600
font-bold:     700
```

## Font Selection Guide

### Heading Fonts
```
Serif: Playfair Display, Merriweather, Lora
Sans-serif: Inter, Poppins, Montserrat
Display: Space Grotesk, Outfit
```

### Body Fonts
```
Sans-serif: Inter, Open Sans, Roboto
Serif: Lora, Merriweather (for editorial)
Mono: JetBrains Mono, Fira Code (for code)
```

## Common Pairings

| Heading | Body | Use Case |
|---------|------|----------|
| Playfair Display | Inter | Elegant, editorial |
| Montserrat | Open Sans | Modern, clean |
| Space Grotesk | Inter | Tech, startup |
| Lora | Merriweather | Traditional, blog |

## Next.js Implementation

```typescript
// app/layout.tsx
import { Inter, Playfair_Display } from 'next/font/google'

const inter = Inter({ 
  subsets: ['latin'],
  variable: '--font-inter'
})

const playfair = Playfair_Display({ 
  subsets: ['latin'],
  variable: '--font-playfair'
})

export default function RootLayout({ children }) {
  return (
    <html className={`${inter.variable} ${playfair.variable}`}>
      <body className="font-sans">{children}</body>
    </html>
  )
}
```

```typescript
// tailwind.config.ts
module.exports = {
  theme: {
    extend: {
      fontFamily: {
        sans: ['var(--font-inter)'],
        serif: ['var(--font-playfair)'],
      },
    },
  },
}
```

## Typography Scale

```tsx
// Consistent hierarchy
<h1 className="font-serif text-4xl font-bold">
  Main Heading
</h1>
<h2 className="font-serif text-3xl font-semibold">
  Section Heading
</h2>
<h3 className="font-serif text-2xl font-medium">
  Subsection
</h3>
<p className="font-sans text-base leading-relaxed">
  Body text with comfortable line height.
</p>
```

## Anti-patterns
- ❌ More than 2 font families
- ❌ Decorative fonts for body text
- ❌ Fonts < 14px for decorative fonts
- ❌ Line-height < 1.4 for body text
- ❌ Mixing too many weights

## Checklist
- [ ] Maximum 2 font families?
- [ ] Heading font defined?
- [ ] Body font defined?
- [ ] Line-height 1.4-1.6 for body?
- [ ] No decorative fonts for body?
- [ ] Font sizes ≥ 14px?
- [ ] Consistent hierarchy?

## Source
- v0 (Vercel) - "Typography: ALWAYS limit to maximum 2 font families"
- Lovable - Typography guidelines
