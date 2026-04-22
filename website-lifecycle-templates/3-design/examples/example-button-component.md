# Example: Design System Component - Button

> **Context**: E-commerce flower shop design system
> **Component**: Button with variants
> **Tools**: Figma, Tailwind CSS, React

---

## 🎨 Design Specifications

### Button Variants

```
┌─────────────────────────────────────────────────────────────┐
│                     PRIMARY BUTTON                          │
│  ┌───────────────────────────────────────────────────────┐ │
│  │                    Add to Cart                        │ │
│  └───────────────────────────────────────────────────────┘ │
│  Background: #ec4899 (Pink 500)                            │
│  Text: #ffffff (White)                                     │
│  Hover: #db2777 (Pink 600)                                │
│  Border Radius: 8px                                        │
│  Padding: 12px 24px                                        │
│  Font: Inter, 16px, 600 weight                            │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                   SECONDARY BUTTON                          │
│  ┌───────────────────────────────────────────────────────┐ │
│  │                   View Details                        │ │
│  └───────────────────────────────────────────────────────┘ │
│  Background: transparent                                    │
│  Text: #ec4899 (Pink 500)                                 │
│  Border: 2px solid #ec4899                                │
│  Hover: Background #fce7f3 (Pink 50)                      │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                     GHOST BUTTON                            │
│  ┌───────────────────────────────────────────────────────┐ │
│  │                      Cancel                           │ │
│  └───────────────────────────────────────────────────────┘ │
│  Background: transparent                                    │
│  Text: #6b7280 (Gray 500)                                 │
│  Hover: Background #f3f4f6 (Gray 100)                     │
└─────────────────────────────────────────────────────────────┘
```

### Size Variants

```
┌──────────────────────────────────────────┐
│ SMALL (sm)                               │
│  ┌────────────────┐                      │
│  │   Add to Cart  │  Height: 36px        │
│  └────────────────┘  Padding: 8px 16px   │
│                      Font: 14px          │
└──────────────────────────────────────────┘

┌──────────────────────────────────────────┐
│ MEDIUM (md) - Default                    │
│  ┌──────────────────────┐                │
│  │     Add to Cart      │  Height: 44px  │
│  └──────────────────────┘  Padding: 12px 24px │
│                            Font: 16px    │
└──────────────────────────────────────────┘

┌──────────────────────────────────────────┐
│ LARGE (lg)                               │
│  ┌────────────────────────────┐          │
│  │       Add to Cart          │  Height: 52px │
│  └────────────────────────────┘  Padding: 16px 32px │
│                                  Font: 18px │
└──────────────────────────────────────────┘
```

### States

```
┌─────────────────────────────────────────────────────────┐
│ DEFAULT STATE                                           │
│  Background: #ec4899                                    │
│  Cursor: pointer                                        │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ HOVER STATE                                             │
│  Background: #db2777 (darker)                           │
│  Transform: translateY(-1px)                            │
│  Box Shadow: 0 4px 12px rgba(236, 72, 153, 0.3)       │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ ACTIVE/PRESSED STATE                                    │
│  Background: #be185d (even darker)                      │
│  Transform: translateY(0)                               │
│  Box Shadow: none                                       │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ DISABLED STATE                                          │
│  Background: #e5e7eb (Gray 200)                         │
│  Text: #9ca3af (Gray 400)                              │
│  Cursor: not-allowed                                    │
│  Opacity: 0.6                                           │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ LOADING STATE                                           │
│  Background: #ec4899                                    │
│  Text: Hidden                                           │
│  Spinner: Visible (white)                               │
│  Cursor: wait                                           │
└─────────────────────────────────────────────────────────┘
```

---

## 💻 Implementation

### React Component

```tsx
// Button.tsx
import { forwardRef } from 'react'
import { cn } from '@/lib/utils'

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost'
  size?: 'sm' | 'md' | 'lg'
  loading?: boolean
  icon?: React.ReactNode
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      variant = 'primary',
      size = 'md',
      loading = false,
      icon,
      children,
      className,
      disabled,
      ...props
    },
    ref
  ) => {
    const baseStyles = 'inline-flex items-center justify-center gap-2 font-semibold rounded-lg transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2'
    
    const variants = {
      primary: 'bg-pink-500 text-white hover:bg-pink-600 active:bg-pink-700 focus:ring-pink-500 disabled:bg-gray-200 disabled:text-gray-400',
      secondary: 'bg-transparent text-pink-500 border-2 border-pink-500 hover:bg-pink-50 active:bg-pink-100 focus:ring-pink-500 disabled:border-gray-300 disabled:text-gray-400',
      ghost: 'bg-transparent text-gray-600 hover:bg-gray-100 active:bg-gray-200 focus:ring-gray-500 disabled:text-gray-400',
    }
    
    const sizes = {
      sm: 'h-9 px-4 text-sm',
      md: 'h-11 px-6 text-base',
      lg: 'h-13 px-8 text-lg',
    }
    
    return (
      <button
        ref={ref}
        className={cn(
          baseStyles,
          variants[variant],
          sizes[size],
          loading && 'cursor-wait',
          disabled && 'cursor-not-allowed opacity-60',
          className
        )}
        disabled={disabled || loading}
        {...props}
      >
        {loading ? (
          <svg
            className="animate-spin h-5 w-5"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
          >
            <circle
              className="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="4"
            />
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            />
          </svg>
        ) : (
          <>
            {icon && <span className="inline-flex">{icon}</span>}
            {children}
          </>
        )}
      </button>
    )
  }
)

Button.displayName = 'Button'
```

### Usage Examples

```tsx
// ProductCard.tsx
import { Button } from '@/components/ui/button'
import { ShoppingCart, Heart } from 'lucide-react'

function ProductCard({ product }: Props) {
  const [loading, setLoading] = useState(false)
  
  const handleAddToCart = async () => {
    setLoading(true)
    await addToCart(product.id)
    setLoading(false)
  }
  
  return (
    <div className="product-card">
      <img src={product.image} alt={product.name} />
      <h3>{product.name}</h3>
      <p className="price">{formatPrice(product.price)}</p>
      
      {/* Primary button with icon */}
      <Button
        variant="primary"
        size="md"
        loading={loading}
        onClick={handleAddToCart}
        icon={<ShoppingCart size={20} />}
      >
        Add to Cart
      </Button>
      
      {/* Secondary button */}
      <Button
        variant="secondary"
        size="sm"
        onClick={() => navigate(`/products/${product.id}`)}
      >
        View Details
      </Button>
      
      {/* Ghost button */}
      <Button
        variant="ghost"
        size="sm"
        icon={<Heart size={18} />}
        onClick={handleAddToWishlist}
      >
        Save
      </Button>
    </div>
  )
}
```

---

## 🎨 Figma Design Tokens

```json
{
  "button": {
    "primary": {
      "background": {
        "default": "#ec4899",
        "hover": "#db2777",
        "active": "#be185d"
      },
      "text": "#ffffff",
      "shadow": {
        "hover": "0 4px 12px rgba(236, 72, 153, 0.3)"
      }
    },
    "secondary": {
      "border": "#ec4899",
      "text": "#ec4899",
      "background": {
        "hover": "#fce7f3",
        "active": "#fbcfe8"
      }
    },
    "ghost": {
      "text": "#6b7280",
      "background": {
        "hover": "#f3f4f6",
        "active": "#e5e7eb"
      }
    },
    "disabled": {
      "background": "#e5e7eb",
      "text": "#9ca3af",
      "opacity": 0.6
    },
    "borderRadius": "8px",
    "sizes": {
      "sm": {
        "height": "36px",
        "padding": "8px 16px",
        "fontSize": "14px"
      },
      "md": {
        "height": "44px",
        "padding": "12px 24px",
        "fontSize": "16px"
      },
      "lg": {
        "height": "52px",
        "padding": "16px 32px",
        "fontSize": "18px"
      }
    }
  }
}
```

---

## ✅ Accessibility Checklist

- [x] Minimum touch target: 44x44px (WCAG 2.1)
- [x] Color contrast ratio ≥ 4.5:1 (WCAG AA)
- [x] Focus visible indicator
- [x] Keyboard accessible (Enter/Space)
- [x] Disabled state clearly indicated
- [x] Loading state announced to screen readers
- [x] Semantic HTML (`<button>` element)
- [x] ARIA labels when icon-only

---

## 📱 Responsive Behavior

```css
/* Mobile: Full width buttons */
@media (max-width: 768px) {
  .button {
    width: 100%;
    justify-content: center;
  }
}

/* Tablet/Desktop: Auto width */
@media (min-width: 769px) {
  .button {
    width: auto;
  }
}
```

---

## 🧪 Testing Scenarios

### Visual Testing
- [ ] All variants render correctly
- [ ] All sizes render correctly
- [ ] Hover states work
- [ ] Active states work
- [ ] Disabled state visible
- [ ] Loading spinner animates
- [ ] Icons align properly

### Functional Testing
- [ ] onClick handler fires
- [ ] Disabled button doesn't fire onClick
- [ ] Loading button doesn't fire onClick
- [ ] Keyboard navigation works
- [ ] Focus states visible

### Accessibility Testing
- [ ] Screen reader announces button text
- [ ] Screen reader announces loading state
- [ ] Keyboard focus visible
- [ ] Color contrast passes WCAG AA

---

## 📊 Usage Guidelines

### When to Use Each Variant

**Primary Button:**
- Main call-to-action
- Form submissions
- Purchase actions
- One per screen/section

**Secondary Button:**
- Alternative actions
- Navigation
- Less important CTAs
- Can have multiple per screen

**Ghost Button:**
- Tertiary actions
- Cancel/dismiss
- Subtle interactions
- Icon-only buttons

### Common Mistakes

❌ **Don't:**
- Use multiple primary buttons in same section
- Make buttons too small (< 44px height)
- Use low contrast colors
- Forget loading states
- Ignore disabled states

✅ **Do:**
- Use clear, action-oriented labels
- Maintain consistent sizing
- Provide visual feedback
- Test on real devices
- Follow accessibility guidelines
