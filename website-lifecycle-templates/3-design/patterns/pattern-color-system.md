# Pattern: Color System

## Nguồn
- Lovable
- v0 (Vercel)
- Tailwind CSS

## Mô tả
Systematic color palette với shades, semantic colors, và accessibility compliance. Đảm bảo visual consistency và brand identity.

## Khi nào dùng
- Design phase: define brand colors
- Development: implement color tokens
- Maintenance: ensure color consistency
- Accessibility: meet WCAG contrast ratios

## Cách áp dụng

### 1. Color Palette Structure
```typescript
// 50-900 scale (Tailwind-inspired)
interface ColorScale {
  50: string   // Lightest
  100: string
  200: string
  300: string
  400: string
  500: string  // Base color
  600: string
  700: string
  800: string
  900: string  // Darkest
}

const colorPalette = {
  // Brand colors
  primary: {
    50: '#fef2f2',
    100: '#fee2e2',
    200: '#fecaca',
    300: '#fca5a5',
    400: '#f87171',
    500: '#ef4444',  // Main brand
    600: '#dc2626',
    700: '#b91c1c',
    800: '#991b1b',
    900: '#7f1d1d',
  },
  
  // Neutrals
  gray: {
    50: '#f9fafb',
    100: '#f3f4f6',
    200: '#e5e7eb',
    300: '#d1d5db',
    400: '#9ca3af',
    500: '#6b7280',
    600: '#4b5563',
    700: '#374151',
    800: '#1f2937',
    900: '#111827',
  },
}
```

### 2. Semantic Colors
```typescript
// Map semantic meaning to palette
const semanticColors = {
  // Actions
  primary: colorPalette.primary[500],
  secondary: colorPalette.gray[600],
  
  // States
  success: '#10b981',
  warning: '#f59e0b',
  error: '#ef4444',
  info: '#3b82f6',
  
  // Surfaces
  background: '#ffffff',
  surface: colorPalette.gray[50],
  border: colorPalette.gray[200],
  
  // Text
  textPrimary: colorPalette.gray[900],
  textSecondary: colorPalette.gray[600],
  textMuted: colorPalette.gray[400],
}
```

### 3. Accessibility Compliance
```typescript
// WCAG AA: 4.5:1 for normal text, 3:1 for large text
// WCAG AAA: 7:1 for normal text, 4.5:1 for large text

function getContrastRatio(fg: string, bg: string): number {
  // Calculate relative luminance
  const getLuminance = (color: string) => {
    const rgb = hexToRgb(color)
    const [r, g, b] = rgb.map((val) => {
      val = val / 255
      return val <= 0.03928
        ? val / 12.92
        : Math.pow((val + 0.055) / 1.055, 2.4)
    })
    return 0.2126 * r + 0.7152 * g + 0.0722 * b
  }
  
  const l1 = getLuminance(fg)
  const l2 = getLuminance(bg)
  const lighter = Math.max(l1, l2)
  const darker = Math.min(l1, l2)
  
  return (lighter + 0.05) / (darker + 0.05)
}

// Validate color combinations
const colorCombinations = [
  { fg: semanticColors.textPrimary, bg: semanticColors.background },
  { fg: 'white', bg: semanticColors.primary },
  { fg: 'white', bg: semanticColors.error },
]

colorCombinations.forEach(({ fg, bg }) => {
  const ratio = getContrastRatio(fg, bg)
  const passAA = ratio >= 4.5
  const passAAA = ratio >= 7
  
  console.log(`${fg} on ${bg}: ${ratio.toFixed(2)}:1`)
  console.log(`  WCAG AA: ${passAA ? '✅' : '❌'}`)
  console.log(`  WCAG AAA: ${passAAA ? '✅' : '❌'}`)
})
```

## Ví dụ thực tế

### E-commerce Flower Shop: Pink Petals Theme

```typescript
// Brand colors
export const flowerShopColors = {
  // Primary: Pink (romantic, feminine)
  pink: {
    50: '#fdf2f8',
    100: '#fce7f3',
    200: '#fbcfe8',
    300: '#f9a8d4',
    400: '#f472b6',
    500: '#ec4899',  // Main brand
    600: '#db2777',
    700: '#be185d',
    800: '#9f1239',
    900: '#831843',
  },
  
  // Secondary: Green (nature, freshness)
  green: {
    50: '#f0fdf4',
    100: '#dcfce7',
    200: '#bbf7d0',
    300: '#86efac',
    400: '#4ade80',
    500: '#22c55e',  // Accent
    600: '#16a34a',
    700: '#15803d',
    800: '#166534',
    900: '#14532d',
  },
  
  // Neutrals
  gray: {
    50: '#fafafa',
    100: '#f5f5f5',
    200: '#e5e5e5',
    300: '#d4d4d4',
    400: '#a3a3a3',
    500: '#737373',
    600: '#525252',
    700: '#404040',
    800: '#262626',
    900: '#171717',
  },
}

// Semantic mapping
export const semanticColors = {
  // Brand
  primary: flowerShopColors.pink[500],
  primaryHover: flowerShopColors.pink[600],
  primaryActive: flowerShopColors.pink[700],
  
  secondary: flowerShopColors.green[500],
  secondaryHover: flowerShopColors.green[600],
  
  // States
  success: flowerShopColors.green[500],
  warning: '#f59e0b',
  error: '#ef4444',
  info: '#3b82f6',
  
  // Surfaces
  background: '#ffffff',
  surface: flowerShopColors.gray[50],
  surfaceHover: flowerShopColors.gray[100],
  border: flowerShopColors.gray[200],
  
  // Text
  textPrimary: flowerShopColors.gray[900],
  textSecondary: flowerShopColors.gray[600],
  textMuted: flowerShopColors.gray[400],
  textOnPrimary: '#ffffff',
}
```

### CSS Variables

```css
:root {
  /* Brand */
  --color-primary: #ec4899;
  --color-primary-hover: #db2777;
  --color-primary-active: #be185d;
  
  --color-secondary: #22c55e;
  --color-secondary-hover: #16a34a;
  
  /* States */
  --color-success: #22c55e;
  --color-warning: #f59e0b;
  --color-error: #ef4444;
  --color-info: #3b82f6;
  
  /* Surfaces */
  --color-background: #ffffff;
  --color-surface: #fafafa;
  --color-border: #e5e5e5;
  
  /* Text */
  --color-text-primary: #171717;
  --color-text-secondary: #525252;
  --color-text-muted: #a3a3a3;
}

/* Dark mode */
@media (prefers-color-scheme: dark) {
  :root {
    --color-background: #171717;
    --color-surface: #262626;
    --color-border: #404040;
    
    --color-text-primary: #fafafa;
    --color-text-secondary: #d4d4d4;
    --color-text-muted: #737373;
  }
}
```

### Usage in Components

```tsx
// Button with semantic colors
function Button({ variant = 'primary', children }: Props) {
  const styles = {
    primary: 'bg-primary hover:bg-primary-hover text-white',
    secondary: 'bg-secondary hover:bg-secondary-hover text-white',
    outline: 'border-2 border-primary text-primary hover:bg-primary hover:text-white',
    ghost: 'text-primary hover:bg-surface',
  }
  
  return (
    <button className={cn('button', styles[variant])}>
      {children}
    </button>
  )
}

// Badge with state colors
function Badge({ status }: Props) {
  const styles = {
    success: 'bg-success/10 text-success border-success',
    warning: 'bg-warning/10 text-warning border-warning',
    error: 'bg-error/10 text-error border-error',
    info: 'bg-info/10 text-info border-info',
  }
  
  return (
    <span className={cn('badge', styles[status])}>
      {status}
    </span>
  )
}
```

## Color System Checklist

### Foundation
- [ ] Brand colors defined (primary, secondary)
- [ ] Neutral scale (gray 50-900)
- [ ] Semantic colors (success, warning, error, info)
- [ ] Surface colors (background, surface, border)
- [ ] Text colors (primary, secondary, muted)

### Accessibility
- [ ] All text meets WCAG AA (4.5:1)
- [ ] Large text meets WCAG AA (3:1)
- [ ] Interactive elements have sufficient contrast
- [ ] Focus states visible
- [ ] Dark mode support

### Implementation
- [ ] CSS variables defined
- [ ] Tailwind config updated
- [ ] TypeScript types exported
- [ ] Storybook documentation

## Trade-offs

| Ưu điểm | Nhược điểm |
|---------|------------|
| Consistent brand | Upfront design work |
| Accessible by default | Cần validate combinations |
| Easy theming | Learning curve |

## Best Practices
1. **Use semantic names**: `primary` not `pink-500`
2. **Test contrast**: Use tools like WebAIM Contrast Checker
3. **Support dark mode**: Define both light/dark palettes
4. **Limit palette**: 2-3 brand colors + neutrals + semantic
5. **Document usage**: When to use each color

## Anti-patterns
- ❌ Hardcode hex values trong components
- ❌ Ignore contrast ratios
- ❌ Quá nhiều brand colors (> 3)
- ❌ Không consistent naming
- ❌ Forget dark mode

## Related Patterns
- [Design System First](./pattern-design-system-first.md)
- [Typography System](./pattern-typography-system.md)
