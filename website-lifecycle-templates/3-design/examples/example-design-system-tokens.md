# Design System Tokens Example

> **Context**: E-commerce flower shop design system
> **Format**: JSON tokens for export to code
> **Last Updated**: 2026-04-23

---

## Overview

Design tokens là single source of truth cho design decisions, có thể export sang code (CSS variables, Tailwind config, styled-components).

---

## Token Structure

### 1. Color Tokens

```json
{
  "color": {
    "brand": {
      "primary": {
        "50": { "value": "#fdf2f8", "type": "color" },
        "100": { "value": "#fce7f3", "type": "color" },
        "200": { "value": "#fbcfe8", "type": "color" },
        "300": { "value": "#f9a8d4", "type": "color" },
        "400": { "value": "#f472b6", "type": "color" },
        "500": { "value": "#ec4899", "type": "color" },
        "600": { "value": "#db2777", "type": "color" },
        "700": { "value": "#be185d", "type": "color" },
        "800": { "value": "#9f1239", "type": "color" },
        "900": { "value": "#831843", "type": "color" }
      },
      "secondary": {
        "50": { "value": "#f0fdf4", "type": "color" },
        "100": { "value": "#dcfce7", "type": "color" },
        "500": { "value": "#22c55e", "type": "color" },
        "600": { "value": "#16a34a", "type": "color" }
      }
    },
    "neutral": {
      "white": { "value": "#ffffff", "type": "color" },
      "black": { "value": "#000000", "type": "color" },
      "gray": {
        "50": { "value": "#f9fafb", "type": "color" },
        "100": { "value": "#f3f4f6", "type": "color" },
        "200": { "value": "#e5e7eb", "type": "color" },
        "300": { "value": "#d1d5db", "type": "color" },
        "400": { "value": "#9ca3af", "type": "color" },
        "500": { "value": "#6b7280", "type": "color" },
        "600": { "value": "#4b5563", "type": "color" },
        "700": { "value": "#374151", "type": "color" },
        "800": { "value": "#1f2937", "type": "color" },
        "900": { "value": "#111827", "type": "color" }
      }
    },
    "semantic": {
      "success": { "value": "#22c55e", "type": "color" },
      "warning": { "value": "#f59e0b", "type": "color" },
      "error": { "value": "#ef4444", "type": "color" },
      "info": { "value": "#3b82f6", "type": "color" }
    }
  }
}
```

### 2. Typography Tokens

```json
{
  "typography": {
    "fontFamily": {
      "sans": {
        "value": "Inter, system-ui, -apple-system, sans-serif",
        "type": "fontFamily"
      },
      "serif": {
        "value": "Playfair Display, Georgia, serif",
        "type": "fontFamily"
      },
      "mono": {
        "value": "JetBrains Mono, monospace",
        "type": "fontFamily"
      }
    },
    "fontSize": {
      "xs": { "value": "0.75rem", "type": "fontSize" },
      "sm": { "value": "0.875rem", "type": "fontSize" },
      "base": { "value": "1rem", "type": "fontSize" },
      "lg": { "value": "1.125rem", "type": "fontSize" },
      "xl": { "value": "1.25rem", "type": "fontSize" },
      "2xl": { "value": "1.5rem", "type": "fontSize" },
      "3xl": { "value": "1.875rem", "type": "fontSize" },
      "4xl": { "value": "2.25rem", "type": "fontSize" },
      "5xl": { "value": "3rem", "type": "fontSize" }
    },
    "fontWeight": {
      "light": { "value": "300", "type": "fontWeight" },
      "normal": { "value": "400", "type": "fontWeight" },
      "medium": { "value": "500", "type": "fontWeight" },
      "semibold": { "value": "600", "type": "fontWeight" },
      "bold": { "value": "700", "type": "fontWeight" }
    },
    "lineHeight": {
      "tight": { "value": "1.25", "type": "lineHeight" },
      "normal": { "value": "1.5", "type": "lineHeight" },
      "relaxed": { "value": "1.75", "type": "lineHeight" }
    }
  }
}
```

### 3. Spacing Tokens

```json
{
  "spacing": {
    "0": { "value": "0", "type": "spacing" },
    "1": { "value": "0.25rem", "type": "spacing" },
    "2": { "value": "0.5rem", "type": "spacing" },
    "3": { "value": "0.75rem", "type": "spacing" },
    "4": { "value": "1rem", "type": "spacing" },
    "5": { "value": "1.25rem", "type": "spacing" },
    "6": { "value": "1.5rem", "type": "spacing" },
    "8": { "value": "2rem", "type": "spacing" },
    "10": { "value": "2.5rem", "type": "spacing" },
    "12": { "value": "3rem", "type": "spacing" },
    "16": { "value": "4rem", "type": "spacing" },
    "20": { "value": "5rem", "type": "spacing" },
    "24": { "value": "6rem", "type": "spacing" }
  }
}
```

### 4. Border Radius Tokens

```json
{
  "borderRadius": {
    "none": { "value": "0", "type": "borderRadius" },
    "sm": { "value": "0.125rem", "type": "borderRadius" },
    "base": { "value": "0.25rem", "type": "borderRadius" },
    "md": { "value": "0.375rem", "type": "borderRadius" },
    "lg": { "value": "0.5rem", "type": "borderRadius" },
    "xl": { "value": "0.75rem", "type": "borderRadius" },
    "2xl": { "value": "1rem", "type": "borderRadius" },
    "full": { "value": "9999px", "type": "borderRadius" }
  }
}
```

### 5. Shadow Tokens

```json
{
  "shadow": {
    "sm": {
      "value": "0 1px 2px 0 rgba(0, 0, 0, 0.05)",
      "type": "boxShadow"
    },
    "base": {
      "value": "0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)",
      "type": "boxShadow"
    },
    "md": {
      "value": "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
      "type": "boxShadow"
    },
    "lg": {
      "value": "0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)",
      "type": "boxShadow"
    },
    "xl": {
      "value": "0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)",
      "type": "boxShadow"
    }
  }
}
```

---

## Export to Code

### Tailwind Config

```typescript
// tailwind.config.ts
import type { Config } from 'tailwindcss'
import tokens from './design-tokens.json'

const config: Config = {
  theme: {
    extend: {
      colors: {
        primary: {
          50: tokens.color.brand.primary['50'].value,
          100: tokens.color.brand.primary['100'].value,
          200: tokens.color.brand.primary['200'].value,
          300: tokens.color.brand.primary['300'].value,
          400: tokens.color.brand.primary['400'].value,
          500: tokens.color.brand.primary['500'].value,
          600: tokens.color.brand.primary['600'].value,
          700: tokens.color.brand.primary['700'].value,
          800: tokens.color.brand.primary['800'].value,
          900: tokens.color.brand.primary['900'].value,
        },
        secondary: {
          50: tokens.color.brand.secondary['50'].value,
          100: tokens.color.brand.secondary['100'].value,
          500: tokens.color.brand.secondary['500'].value,
          600: tokens.color.brand.secondary['600'].value,
        },
      },
      fontFamily: {
        sans: [tokens.typography.fontFamily.sans.value],
        serif: [tokens.typography.fontFamily.serif.value],
        mono: [tokens.typography.fontFamily.mono.value],
      },
      fontSize: {
        xs: tokens.typography.fontSize.xs.value,
        sm: tokens.typography.fontSize.sm.value,
        base: tokens.typography.fontSize.base.value,
        lg: tokens.typography.fontSize.lg.value,
        xl: tokens.typography.fontSize.xl.value,
        '2xl': tokens.typography.fontSize['2xl'].value,
        '3xl': tokens.typography.fontSize['3xl'].value,
        '4xl': tokens.typography.fontSize['4xl'].value,
        '5xl': tokens.typography.fontSize['5xl'].value,
      },
      spacing: {
        0: tokens.spacing['0'].value,
        1: tokens.spacing['1'].value,
        2: tokens.spacing['2'].value,
        3: tokens.spacing['3'].value,
        4: tokens.spacing['4'].value,
        5: tokens.spacing['5'].value,
        6: tokens.spacing['6'].value,
        8: tokens.spacing['8'].value,
        10: tokens.spacing['10'].value,
        12: tokens.spacing['12'].value,
        16: tokens.spacing['16'].value,
        20: tokens.spacing['20'].value,
        24: tokens.spacing['24'].value,
      },
      borderRadius: {
        none: tokens.borderRadius.none.value,
        sm: tokens.borderRadius.sm.value,
        base: tokens.borderRadius.base.value,
        md: tokens.borderRadius.md.value,
        lg: tokens.borderRadius.lg.value,
        xl: tokens.borderRadius.xl.value,
        '2xl': tokens.borderRadius['2xl'].value,
        full: tokens.borderRadius.full.value,
      },
      boxShadow: {
        sm: tokens.shadow.sm.value,
        base: tokens.shadow.base.value,
        md: tokens.shadow.md.value,
        lg: tokens.shadow.lg.value,
        xl: tokens.shadow.xl.value,
      },
    },
  },
}

export default config
```

### CSS Variables

```css
/* styles/tokens.css */
:root {
  /* Colors */
  --color-primary-50: #fdf2f8;
  --color-primary-100: #fce7f3;
  --color-primary-500: #ec4899;
  --color-primary-600: #db2777;
  
  /* Typography */
  --font-sans: Inter, system-ui, -apple-system, sans-serif;
  --font-serif: Playfair Display, Georgia, serif;
  --font-size-base: 1rem;
  --font-size-lg: 1.125rem;
  --font-weight-normal: 400;
  --font-weight-semibold: 600;
  
  /* Spacing */
  --spacing-4: 1rem;
  --spacing-6: 1.5rem;
  --spacing-8: 2rem;
  
  /* Border Radius */
  --radius-base: 0.25rem;
  --radius-lg: 0.5rem;
  --radius-full: 9999px;
  
  /* Shadows */
  --shadow-base: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}
```

### TypeScript Types

```typescript
// types/design-tokens.ts
export interface ColorToken {
  value: string
  type: 'color'
}

export interface TypographyToken {
  value: string
  type: 'fontFamily' | 'fontSize' | 'fontWeight' | 'lineHeight'
}

export interface SpacingToken {
  value: string
  type: 'spacing'
}

export interface DesignTokens {
  color: {
    brand: {
      primary: Record<string, ColorToken>
      secondary: Record<string, ColorToken>
    }
    neutral: {
      white: ColorToken
      black: ColorToken
      gray: Record<string, ColorToken>
    }
    semantic: {
      success: ColorToken
      warning: ColorToken
      error: ColorToken
      info: ColorToken
    }
  }
  typography: {
    fontFamily: Record<string, TypographyToken>
    fontSize: Record<string, TypographyToken>
    fontWeight: Record<string, TypographyToken>
    lineHeight: Record<string, TypographyToken>
  }
  spacing: Record<string, SpacingToken>
  borderRadius: Record<string, { value: string; type: 'borderRadius' }>
  shadow: Record<string, { value: string; type: 'boxShadow' }>
}
```

---

## Usage in Components

```tsx
// components/ProductCard.tsx
import React from 'react'

interface ProductCardProps {
  name: string
  price: number
  image: string
}

export function ProductCard({ name, price, image }: ProductCardProps) {
  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow">
      <img 
        src={image} 
        alt={name}
        className="w-full h-48 object-cover"
      />
      <div className="p-4">
        <h3 className="font-serif text-xl font-semibold text-gray-900 mb-2">
          {name}
        </h3>
        <p className="text-primary-600 font-semibold text-lg">
          ${price.toFixed(2)}
        </p>
        <button className="mt-4 w-full bg-primary-500 hover:bg-primary-600 text-white font-medium py-2 px-4 rounded-lg transition-colors">
          Add to Cart
        </button>
      </div>
    </div>
  )
}
```

---

## Benefits

| Benefit | Description |
|---------|-------------|
| **Consistency** | Single source of truth cho design decisions |
| **Maintainability** | Thay đổi 1 chỗ, update toàn bộ app |
| **Scalability** | Dễ thêm themes (dark mode, seasonal) |
| **Collaboration** | Designers & developers dùng chung tokens |
| **Type Safety** | TypeScript types từ tokens |

---

## Tools

- **Figma Tokens Plugin**: Export tokens từ Figma
- **Style Dictionary**: Transform tokens sang nhiều formats
- **Theo**: Token transformer
- **Design Tokens Community Group**: Standard format

---

## Related

- [template-design-system-foundation.md](../templates/template-design-system-foundation.md)
- [example-component-library.md](./example-component-library.md)
