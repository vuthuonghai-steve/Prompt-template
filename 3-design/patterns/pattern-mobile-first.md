# Pattern: Mobile-First Design

## Problem
Desktop-first design → mobile experience bị broken hoặc suboptimal.

## Solution
Design cho mobile TRƯỚC, sau đó enhance cho desktop.

**Core principles:**
- Mobile is PRIMARY experience
- Desktop is secondary
- Touch-first interactions
- Responsive breakpoints

## Example

### ✅ Good: Mobile-First Approach
```tsx
// Base styles = mobile
<div className="
  flex flex-col gap-4 p-4
  md:flex-row md:gap-6 md:p-6
  lg:gap-8 lg:p-8
">
  <Button className="w-full md:w-auto">
    Submit
  </Button>
</div>
```

### ❌ Bad: Desktop-First
```tsx
// DON'T do this
<div className="
  flex-row gap-8 p-8
  md:flex-col md:gap-4 md:p-4
">
  <Button className="w-auto md:w-full">
    Submit
  </Button>
</div>
```

## Technical Requirements

### 1. iOS Safari Optimization
```tsx
// layout.tsx
export const viewport = {
  width: "device-width",
  initialScale: 1,
  maximumScale: 1, // Disable auto-zoom
}

// Add background to html tag
<html className="bg-background">
```

### 2. Touch Targets
```css
/* Minimum 44px for interactive elements */
.button {
  min-height: 44px;
  min-width: 44px;
}
```

### 3. Font Sizes
```css
/* Minimum 16px for inputs (prevents zoom) */
input, textarea, select {
  font-size: 16px;
}
```

### 4. PWA Ready
```json
// manifest.json
{
  "name": "App Name",
  "short_name": "App",
  "display": "standalone",
  "theme_color": "#000000"
}
```

## Responsive Breakpoints

```typescript
// Tailwind default breakpoints
sm: 640px   // Small tablets
md: 768px   // Tablets
lg: 1024px  // Laptops
xl: 1280px  // Desktops
2xl: 1536px // Large desktops
```

## Layout Patterns

### Stack on Mobile, Row on Desktop
```tsx
<div className="flex flex-col md:flex-row gap-4">
  <div>Item 1</div>
  <div>Item 2</div>
</div>
```

### Full Width on Mobile, Fixed on Desktop
```tsx
<Button className="w-full md:w-auto">
  Submit
</Button>
```

### Hide on Mobile, Show on Desktop
```tsx
<div className="hidden md:block">
  Desktop only content
</div>
```

## Testing Checklist
- [ ] Touch targets ≥ 44px?
- [ ] Input font-size ≥ 16px?
- [ ] No horizontal scroll on mobile?
- [ ] Readable text without zoom?
- [ ] Works on iOS Safari?
- [ ] PWA manifest configured?

## Anti-patterns
- ❌ Desktop-first breakpoints
- ❌ Small touch targets (< 44px)
- ❌ Input font-size < 16px (causes zoom)
- ❌ Fixed widths without responsive variants
- ❌ Hover-only interactions

## Source
- v0 (Vercel) - "Mobile-First Priority"
- Lovable - "Always generate responsive designs"
