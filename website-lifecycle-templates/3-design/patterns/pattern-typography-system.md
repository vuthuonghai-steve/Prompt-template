# Pattern: Typography System

## Nguồn
- Lovable
- v0 (Vercel)
- Tailwind CSS

## Mô tả
Systematic typography scale với font families, sizes, weights, line heights. Đảm bảo readability, hierarchy, và brand consistency.

## Khi nào dùng
- Design phase: define typography scale
- Development: implement text styles
- Content: ensure readability
- Branding: maintain visual identity

## Cách áp dụng

### 1. Type Scale
```typescript
// Modular scale (1.25 ratio)
export const typeScale = {
  xs: '0.75rem',    // 12px
  sm: '0.875rem',   // 14px
  base: '1rem',     // 16px
  lg: '1.125rem',   // 18px
  xl: '1.25rem',    // 20px
  '2xl': '1.5rem',  // 24px
  '3xl': '1.875rem', // 30px
  '4xl': '2.25rem',  // 36px
  '5xl': '3rem',     // 48px
  '6xl': '3.75rem',  // 60px
}

// Line heights
export const lineHeight = {
  tight: 1.25,
  normal: 1.5,
  relaxed: 1.75,
  loose: 2,
}

// Font weights
export const fontWeight = {
  light: 300,
  normal: 400,
  medium: 500,
  semibold: 600,
  bold: 700,
  extrabold: 800,
}
```

### 2. Font Families
```typescript
export const fontFamily = {
  // Headings: Serif for elegance
  heading: ['Playfair Display', 'Georgia', 'serif'],
  
  // Body: Sans-serif for readability
  body: ['Inter', 'system-ui', 'sans-serif'],
  
  // Monospace: Code, numbers
  mono: ['Fira Code', 'Consolas', 'monospace'],
}
```

### 3. Text Styles
```typescript
interface TextStyle {
  fontFamily: string
  fontSize: string
  fontWeight: number
  lineHeight: number
  letterSpacing?: string
}

export const textStyles = {
  // Headings
  h1: {
    fontFamily: fontFamily.heading,
    fontSize: typeScale['5xl'],
    fontWeight: fontWeight.bold,
    lineHeight: lineHeight.tight,
  },
  h2: {
    fontFamily: fontFamily.heading,
    fontSize: typeScale['4xl'],
    fontWeight: fontWeight.bold,
    lineHeight: lineHeight.tight,
  },
  h3: {
    fontFamily: fontFamily.heading,
    fontSize: typeScale['3xl'],
    fontWeight: fontWeight.semibold,
    lineHeight: lineHeight.normal,
  },
  
  // Body
  body: {
    fontFamily: fontFamily.body,
    fontSize: typeScale.base,
    fontWeight: fontWeight.normal,
    lineHeight: lineHeight.relaxed,
  },
  bodyLarge: {
    fontFamily: fontFamily.body,
    fontSize: typeScale.lg,
    fontWeight: fontWeight.normal,
    lineHeight: lineHeight.relaxed,
  },
  bodySmall: {
    fontFamily: fontFamily.body,
    fontSize: typeScale.sm,
    fontWeight: fontWeight.normal,
    lineHeight: lineHeight.normal,
  },
  
  // Special
  caption: {
    fontFamily: fontFamily.body,
    fontSize: typeScale.xs,
    fontWeight: fontWeight.normal,
    lineHeight: lineHeight.normal,
    letterSpacing: '0.025em',
  },
  button: {
    fontFamily: fontFamily.body,
    fontSize: typeScale.base,
    fontWeight: fontWeight.semibold,
    lineHeight: lineHeight.tight,
    letterSpacing: '0.025em',
  },
}
```

## Ví dụ thực tế

### E-commerce Typography System

```typescript
// typography.config.ts
export const typography = {
  // Font families
  fonts: {
    heading: '"Playfair Display", Georgia, serif',
    body: '"Inter", system-ui, sans-serif',
  },
  
  // Type scale
  sizes: {
    // Display (hero sections)
    display: {
      fontSize: '3.75rem',    // 60px
      lineHeight: 1.1,
      fontWeight: 700,
      letterSpacing: '-0.02em',
    },
    
    // Headings
    h1: {
      fontSize: '3rem',       // 48px
      lineHeight: 1.2,
      fontWeight: 700,
    },
    h2: {
      fontSize: '2.25rem',    // 36px
      lineHeight: 1.3,
      fontWeight: 600,
    },
    h3: {
      fontSize: '1.875rem',   // 30px
      lineHeight: 1.4,
      fontWeight: 600,
    },
    h4: {
      fontSize: '1.5rem',     // 24px
      lineHeight: 1.5,
      fontWeight: 600,
    },
    
    // Body
    large: {
      fontSize: '1.125rem',   // 18px
      lineHeight: 1.75,
      fontWeight: 400,
    },
    base: {
      fontSize: '1rem',       // 16px
      lineHeight: 1.75,
      fontWeight: 400,
    },
    small: {
      fontSize: '0.875rem',   // 14px
      lineHeight: 1.5,
      fontWeight: 400,
    },
    
    // Special
    caption: {
      fontSize: '0.75rem',    // 12px
      lineHeight: 1.5,
      fontWeight: 400,
      letterSpacing: '0.025em',
    },
  },
}
```

### CSS Implementation

```css
/* Font imports */
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@400;500;600;700&display=swap');

/* CSS Variables */
:root {
  /* Fonts */
  --font-heading: 'Playfair Display', Georgia, serif;
  --font-body: 'Inter', system-ui, sans-serif;
  
  /* Sizes */
  --text-display: 3.75rem;
  --text-h1: 3rem;
  --text-h2: 2.25rem;
  --text-h3: 1.875rem;
  --text-h4: 1.5rem;
  --text-large: 1.125rem;
  --text-base: 1rem;
  --text-small: 0.875rem;
  --text-caption: 0.75rem;
  
  /* Line heights */
  --leading-tight: 1.25;
  --leading-normal: 1.5;
  --leading-relaxed: 1.75;
  
  /* Weights */
  --font-normal: 400;
  --font-medium: 500;
  --font-semibold: 600;
  --font-bold: 700;
}

/* Utility classes */
.text-display {
  font-family: var(--font-heading);
  font-size: var(--text-display);
  line-height: 1.1;
  font-weight: var(--font-bold);
  letter-spacing: -0.02em;
}

.text-h1 {
  font-family: var(--font-heading);
  font-size: var(--text-h1);
  line-height: 1.2;
  font-weight: var(--font-bold);
}

.text-body {
  font-family: var(--font-body);
  font-size: var(--text-base);
  line-height: var(--leading-relaxed);
  font-weight: var(--font-normal);
}

/* Responsive typography */
@media (max-width: 768px) {
  :root {
    --text-display: 2.5rem;
    --text-h1: 2rem;
    --text-h2: 1.75rem;
    --text-h3: 1.5rem;
  }
}
```

### React Components

```tsx
// Heading component
interface HeadingProps {
  level: 1 | 2 | 3 | 4 | 5 | 6
  children: React.ReactNode
  className?: string
}

export function Heading({ level, children, className }: HeadingProps) {
  const Tag = `h${level}` as keyof JSX.IntrinsicElements
  
  const styles = {
    1: 'text-h1',
    2: 'text-h2',
    3: 'text-h3',
    4: 'text-h4',
    5: 'text-base font-semibold',
    6: 'text-small font-semibold',
  }
  
  return (
    <Tag className={cn(styles[level], className)}>
      {children}
    </Tag>
  )
}

// Text component
interface TextProps {
  variant?: 'large' | 'base' | 'small' | 'caption'
  weight?: 'normal' | 'medium' | 'semibold' | 'bold'
  children: React.ReactNode
}

export function Text({ 
  variant = 'base', 
  weight = 'normal',
  children 
}: TextProps) {
  const sizeStyles = {
    large: 'text-large',
    base: 'text-base',
    small: 'text-small',
    caption: 'text-caption',
  }
  
  const weightStyles = {
    normal: 'font-normal',
    medium: 'font-medium',
    semibold: 'font-semibold',
    bold: 'font-bold',
  }
  
  return (
    <p className={cn(sizeStyles[variant], weightStyles[weight])}>
      {children}
    </p>
  )
}
```

### Usage Example

```tsx
function ProductPage({ product }: Props) {
  return (
    <div>
      {/* Hero */}
      <h1 className="text-display">
        Fresh Flowers Delivered Daily
      </h1>
      
      {/* Product name */}
      <Heading level={2}>{product.name}</Heading>
      
      {/* Description */}
      <Text variant="large">
        {product.description}
      </Text>
      
      {/* Price */}
      <Text variant="base" weight="bold">
        {formatPrice(product.price)}
      </Text>
      
      {/* Meta info */}
      <Text variant="small" weight="normal">
        In stock • Ships in 24 hours
      </Text>
      
      {/* Fine print */}
      <Text variant="caption">
        Free delivery on orders over 500,000đ
      </Text>
    </div>
  )
}
```

## Typography Checklist

### Foundation
- [ ] Font families selected (heading, body, mono)
- [ ] Type scale defined (xs to 6xl)
- [ ] Line heights set (tight, normal, relaxed)
- [ ] Font weights chosen (light to bold)
- [ ] Letter spacing adjusted for headings

### Readability
- [ ] Body text ≥ 16px
- [ ] Line length 45-75 characters
- [ ] Line height 1.5-1.75 for body
- [ ] Sufficient contrast (WCAG AA)
- [ ] Responsive scaling for mobile

### Implementation
- [ ] CSS variables defined
- [ ] Utility classes created
- [ ] React components built
- [ ] Storybook documentation

## Trade-offs

| Ưu điểm | Nhược điểm |
|---------|------------|
| Consistent hierarchy | Upfront design work |
| Better readability | Font loading overhead |
| Easier maintenance | Cần discipline follow |

## Best Practices
1. **Limit font families**: 2-3 max (heading, body, mono)
2. **Use system fonts as fallback**: Faster loading
3. **Optimize font loading**: `font-display: swap`
4. **Responsive typography**: Scale down on mobile
5. **Test readability**: Real content, real devices
6. **Maintain hierarchy**: Clear visual distinction

## Anti-patterns
- ❌ Quá nhiều font families (> 3)
- ❌ Body text < 16px
- ❌ Line height quá tight (< 1.4)
- ❌ Không responsive typography
- ❌ Hardcode font sizes thay vì dùng scale

## Related Patterns
- [Design System First](./pattern-design-system-first.md)
- [Color System](./pattern-color-system.md)
