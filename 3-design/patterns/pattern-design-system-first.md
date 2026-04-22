# Pattern: Design System First

## Problem
Inconsistent styling, hardcoded colors, duplicate CSS. Mỗi component tự định nghĩa styles riêng.

## Solution
Tạo design system trước, sau đó components sử dụng design tokens.

**Core principles:**
- Define styles in ONE place (index.css, tailwind.config.ts)
- Use semantic tokens, NOT direct colors
- Create component variants using design system
- Never write custom styles in components

## Example

### ❌ Bad: Hardcoded Styles
```tsx
// DON'T do this
<Button className="bg-blue-500 text-white hover:bg-blue-600">
  Submit
</Button>

<div className="text-white bg-black">
  Content
</div>
```

### ✅ Good: Design System Tokens
```css
/* index.css - Define once */
:root {
  --primary: 220 90% 56%;
  --primary-foreground: 0 0% 100%;
  --background: 0 0% 100%;
  --foreground: 222 47% 11%;
}
```

```tsx
// Use semantic tokens
<Button variant="default">Submit</Button>
<div className="bg-background text-foreground">Content</div>
```

### ✅ Good: Component Variants
```typescript
// button.tsx - Create variants using design system
const buttonVariants = cva("...", {
  variants: {
    variant: {
      default: "bg-primary text-primary-foreground",
      secondary: "bg-secondary text-secondary-foreground",
      hero: "bg-gradient-primary text-white",
    }
  }
})
```

## Design System Structure

### 1. Color Tokens (index.css)
```css
:root {
  /* Semantic colors */
  --primary: [hsl values];
  --secondary: [hsl values];
  --accent: [hsl values];
  --background: [hsl values];
  --foreground: [hsl values];
  
  /* Gradients */
  --gradient-primary: linear-gradient(...);
  
  /* Shadows */
  --shadow-elegant: 0 10px 30px -10px hsl(var(--primary) / 0.3);
}
```

### 2. Tailwind Config
```typescript
// tailwind.config.ts
export default {
  theme: {
    extend: {
      colors: {
        primary: "hsl(var(--primary))",
        secondary: "hsl(var(--secondary))",
      },
      fontFamily: {
        sans: ["var(--font-inter)"],
      }
    }
  }
}
```

### 3. Component Variants
```typescript
// Create variants for all states
const buttonVariants = cva("base-styles", {
  variants: {
    variant: { default: "...", outline: "..." },
    size: { sm: "...", md: "...", lg: "..." }
  }
})
```

## When to Use
- ALWAYS for new projects
- Before creating any components
- When seeing hardcoded colors/styles
- When customizing shadcn components

## Workflow

```
Step 1: Define Design System
├── index.css (color tokens, gradients, shadows)
├── tailwind.config.ts (extend with tokens)
└── Component variants (button, card, etc.)

Step 2: Create Components
└── Use semantic tokens only

Step 3: Customize
└── Update design system, NOT individual components
```

## Anti-patterns
- ❌ `text-white`, `bg-white`, `text-black`, `bg-black`
- ❌ `bg-blue-500`, `text-red-600`
- ❌ Inline styles in components
- ❌ Custom CSS in component files
- ❌ Overriding with `className`

## Checklist
- [ ] All colors defined in index.css?
- [ ] Using semantic tokens (primary, secondary)?
- [ ] Component variants created?
- [ ] No hardcoded colors in components?
- [ ] Dark/light mode support?

## Source
- Lovable - "CRITICAL: The design system is everything"
- v0 (Vercel) - Semantic Design Token Generation
