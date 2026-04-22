# Design System Template

## Color System

### Primary Colors
- **Brand Primary**: [Main brand color]
- **Brand Secondary**: [Supporting color]

### Neutrals (2-3 colors)
- **Background**: [Base background]
- **Foreground**: [Text/content]
- **Muted**: [Subtle elements]

### Accents (1-2 colors)
- **Accent**: [Call-to-action]
- **Destructive**: [Errors/warnings]

### Rules
- **Total colors**: 3-5 maximum
- **NO gradients** unless explicitly requested
- **Semantic tokens**: Use design tokens (bg-background, text-foreground)
- **Contrast**: Always ensure proper text/background contrast

---

## Typography

### Font Families (Maximum 2)
- **Heading Font**: [Font name] - weights: [400, 600, 700]
- **Body Font**: [Font name] - weights: [400, 500]

### Scale
- **Heading 1**: text-4xl (36px) - font-bold
- **Heading 2**: text-3xl (30px) - font-semibold
- **Heading 3**: text-2xl (24px) - font-semibold
- **Body**: text-base (16px) - font-normal
- **Small**: text-sm (14px) - font-normal

### Rules
- **Line height**: 1.4-1.6 for body (leading-relaxed)
- **NO decorative fonts** for body text
- **Minimum size**: 14px for readability

---

## Spacing System

### Tailwind Scale (Prefer over arbitrary values)
- **xs**: gap-2 (8px)
- **sm**: gap-4 (16px)
- **md**: gap-6 (24px)
- **lg**: gap-8 (32px)
- **xl**: gap-12 (48px)

### Rules
- **Use gap classes** for spacing (gap-4, gap-x-2)
- **NO space-* classes**
- **NO mixing** margin/padding with gap on same element

---

## Component Patterns

### Layout Priority
1. **Flexbox** for most layouts: `flex items-center justify-between`
2. **CSS Grid** for complex 2D: `grid grid-cols-3 gap-4`
3. **NO floats** or absolute positioning

### Responsive Design
- **Mobile-first**: Design for mobile, enhance for desktop
- **Breakpoints**: sm (640px), md (768px), lg (1024px), xl (1280px)
- **Touch targets**: Minimum 44px for interactive elements

### Accessibility
- **Semantic HTML**: Use `<main>`, `<header>`, `<nav>`, `<section>`
- **ARIA roles**: Add when semantic HTML insufficient
- **Alt text**: All images (unless decorative)
- **Screen reader**: Use `sr-only` class for hidden text

---

## Design Tokens (globals.css)

```css
:root {
  /* Colors */
  --background: [hsl value];
  --foreground: [hsl value];
  --primary: [hsl value];
  --primary-foreground: [hsl value];
  --secondary: [hsl value];
  --secondary-foreground: [hsl value];
  --muted: [hsl value];
  --muted-foreground: [hsl value];
  --accent: [hsl value];
  --accent-foreground: [hsl value];
  --destructive: [hsl value];
  --destructive-foreground: [hsl value];
  --border: [hsl value];
  --input: [hsl value];
  --ring: [hsl value];
  
  /* Radius */
  --radius: 0.5rem;
}
```

---

## Implementation Checklist

- [ ] Define 3-5 colors total (1 primary, 2-3 neutrals, 1-2 accents)
- [ ] Choose maximum 2 font families
- [ ] Set up design tokens in globals.css
- [ ] Configure Tailwind with semantic tokens
- [ ] Use mobile-first responsive design
- [ ] Ensure accessibility (semantic HTML, ARIA, alt text)
- [ ] Test contrast ratios (WCAG AA minimum)
- [ ] Verify touch targets (44px minimum)

---

**Sources**: Lovable, v0, Bolt design guidelines
