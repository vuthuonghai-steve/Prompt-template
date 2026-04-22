# Pattern: Design System First

## Nguồn
- Lovable
- v0 (Vercel)
- Cursor Agent

## Mô tả
Xây dựng design system (colors, typography, components) trước khi design screens. Đảm bảo consistency, reusability, faster iteration.

## Khi nào dùng
- Design phase: trước khi design screens
- Development: setup component library trước features
- Maintenance: refactor UI thành design system
- Scaling: khi team/product lớn lên

## Cách áp dụng

### 1. Design Tokens
```typescript
// colors.ts
export const colors = {
  // Brand
  primary: {
    50: '#fef2f2',
    100: '#fee2e2',
    500: '#ef4444',  // Main brand color
    900: '#7f1d1d',
  },
  
  // Neutrals
  gray: {
    50: '#f9fafb',
    500: '#6b7280',
    900: '#111827',
  },
  
  // Semantic
  success: '#10b981',
  warning: '#f59e0b',
  error: '#ef4444',
  info: '#3b82f6',
}

// typography.ts
export const typography = {
  fontFamily: {
    sans: ['Inter', 'system-ui', 'sans-serif'],
    serif: ['Merriweather', 'Georgia', 'serif'],
  },
  
  fontSize: {
    xs: '0.75rem',    // 12px
    sm: '0.875rem',   // 14px
    base: '1rem',     // 16px
    lg: '1.125rem',   // 18px
    xl: '1.25rem',    // 20px
    '2xl': '1.5rem',  // 24px
    '3xl': '1.875rem', // 30px
  },
  
  fontWeight: {
    normal: 400,
    medium: 500,
    semibold: 600,
    bold: 700,
  },
}

// spacing.ts
export const spacing = {
  0: '0',
  1: '0.25rem',  // 4px
  2: '0.5rem',   // 8px
  3: '0.75rem',  // 12px
  4: '1rem',     // 16px
  6: '1.5rem',   // 24px
  8: '2rem',     // 32px
  12: '3rem',    // 48px
}
```

### 2. Component Library
```tsx
// Button.tsx
interface ButtonProps {
  variant: 'primary' | 'secondary' | 'outline' | 'ghost'
  size: 'sm' | 'md' | 'lg'
  children: React.ReactNode
  onClick?: () => void
}

export function Button({ 
  variant = 'primary', 
  size = 'md',
  children,
  onClick 
}: ButtonProps) {
  return (
    <button
      className={cn(
        'button',
        `button--${variant}`,
        `button--${size}`
      )}
      onClick={onClick}
    >
      {children}
    </button>
  )
}

// CSS
const styles = `
.button {
  font-family: var(--font-sans);
  font-weight: 600;
  border-radius: 0.5rem;
  transition: all 0.2s;
}

.button--primary {
  background: var(--color-primary-500);
  color: white;
}

.button--secondary {
  background: var(--color-gray-200);
  color: var(--color-gray-900);
}

.button--sm {
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
}

.button--md {
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
}

.button--lg {
  padding: 1rem 2rem;
  font-size: 1.125rem;
}
`
```

### 3. Component Composition
```tsx
// Build complex UIs from primitives
function ProductCard({ product }: Props) {
  return (
    <Card>
      <CardImage src={product.image} alt={product.name} />
      <CardContent>
        <Heading level={3}>{product.name}</Heading>
        <Text variant="muted">{product.category}</Text>
        <Price amount={product.price} />
        <Button variant="primary" size="md">
          Add to Cart
        </Button>
      </CardContent>
    </Card>
  )
}
```

## Ví dụ thực tế

### E-commerce Design System

```typescript
// design-system/tokens.ts
export const tokens = {
  colors: {
    // Brand: Pink Petals theme
    brand: {
      pink: {
        light: '#fce7f3',
        main: '#ec4899',
        dark: '#be185d',
      },
      green: {
        light: '#d1fae5',
        main: '#10b981',
        dark: '#047857',
      },
    },
    
    // Semantic
    semantic: {
      success: '#10b981',
      warning: '#f59e0b',
      error: '#ef4444',
      info: '#3b82f6',
    },
  },
  
  typography: {
    heading: {
      fontFamily: 'Playfair Display',
      fontWeight: 700,
    },
    body: {
      fontFamily: 'Inter',
      fontWeight: 400,
    },
  },
  
  spacing: {
    section: '4rem',
    card: '1.5rem',
    element: '1rem',
  },
  
  borderRadius: {
    sm: '0.25rem',
    md: '0.5rem',
    lg: '1rem',
    full: '9999px',
  },
}
```

### Component Library Structure

```
design-system/
├── tokens/
│   ├── colors.ts
│   ├── typography.ts
│   ├── spacing.ts
│   └── index.ts
├── primitives/
│   ├── Button.tsx
│   ├── Input.tsx
│   ├── Card.tsx
│   ├── Badge.tsx
│   └── index.ts
├── compositions/
│   ├── ProductCard.tsx
│   ├── Header.tsx
│   ├── Footer.tsx
│   └── index.ts
└── index.ts
```

### Usage in Screens

```tsx
// screens/ProductListing.tsx
import { 
  Button, 
  Card, 
  Heading, 
  ProductCard 
} from '@/design-system'

function ProductListing({ products }: Props) {
  return (
    <div className="container">
      <Heading level={1}>Fresh Flowers</Heading>
      
      <div className="filters">
        <Button variant="outline">All</Button>
        <Button variant="outline">Roses</Button>
        <Button variant="outline">Tulips</Button>
      </div>
      
      <div className="grid">
        {products.map((product) => (
          <ProductCard key={product.id} product={product} />
        ))}
      </div>
    </div>
  )
}
```

## Design System Checklist

### Foundation
- [ ] Color palette defined
- [ ] Typography scale established
- [ ] Spacing system created
- [ ] Border radius values set
- [ ] Shadow system defined

### Components
- [ ] Button variants
- [ ] Input fields
- [ ] Cards
- [ ] Badges/Tags
- [ ] Navigation
- [ ] Modals/Dialogs
- [ ] Forms

### Documentation
- [ ] Storybook setup
- [ ] Component usage examples
- [ ] Do's and Don'ts
- [ ] Accessibility guidelines

## Trade-offs

| Ưu điểm | Nhược điểm |
|---------|------------|
| Consistency across app | Upfront time investment |
| Faster development | Learning curve |
| Easy maintenance | Có thể over-engineer |
| Better collaboration | Cần discipline follow |

## Best Practices
1. **Start small**: Core components first (Button, Input, Card)
2. **Document everything**: Storybook, usage examples
3. **Version control**: Semantic versioning cho design system
4. **Accessibility first**: WCAG compliance built-in
5. **Test thoroughly**: Visual regression tests
6. **Iterate based on usage**: Add components as needed

## Anti-patterns
- ❌ Build entire design system upfront
- ❌ Không document components
- ❌ Ignore accessibility
- ❌ Không version control
- ❌ One-off components thay vì extend system

## Related Patterns
- [Mobile-First](./pattern-mobile-first.md)
- [Color System](./pattern-color-system.md)
- [Typography System](./pattern-typography-system.md)
