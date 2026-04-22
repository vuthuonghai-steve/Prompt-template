# Example: Color Palette Application

> **Context**: E-commerce flower shop - "Pink Petals" theme
> **Purpose**: Demonstrate how to apply color system across UI
> **Tools**: Figma, Tailwind CSS

---

## 🎨 Brand Color Palette

### Primary Colors

```
┌─────────────────────────────────────────────────────────────┐
│ PINK (Primary Brand Color)                                  │
├─────────────────────────────────────────────────────────────┤
│ Pink 50   #fdf2f8  ████  Backgrounds, subtle highlights    │
│ Pink 100  #fce7f3  ████  Hover states, light surfaces      │
│ Pink 200  #fbcfe8  ████  Borders, dividers                 │
│ Pink 300  #f9a8d4  ████  Disabled states                   │
│ Pink 400  #f472b6  ████  Secondary actions                 │
│ Pink 500  #ec4899  ████  PRIMARY - Main brand color        │
│ Pink 600  #db2777  ████  Hover states for primary          │
│ Pink 700  #be185d  ████  Active/pressed states             │
│ Pink 800  #9f1239  ████  Dark mode primary                 │
│ Pink 900  #831843  ████  Text on light backgrounds         │
└─────────────────────────────────────────────────────────────┘
```

### Secondary Colors

```
┌─────────────────────────────────────────────────────────────┐
│ GREEN (Secondary - Nature, Freshness)                       │
├─────────────────────────────────────────────────────────────┤
│ Green 50   #f0fdf4  ████  Success backgrounds              │
│ Green 100  #dcfce7  ████  Success light                    │
│ Green 500  #22c55e  ████  Success states, accents          │
│ Green 600  #16a34a  ████  Success hover                    │
│ Green 700  #15803d  ████  Success active                   │
└─────────────────────────────────────────────────────────────┘
```

### Neutral Colors

```
┌─────────────────────────────────────────────────────────────┐
│ GRAY (Neutrals)                                             │
├─────────────────────────────────────────────────────────────┤
│ Gray 50    #fafafa  ████  Page backgrounds                 │
│ Gray 100   #f5f5f5  ████  Card backgrounds                 │
│ Gray 200   #e5e5e5  ████  Borders, dividers                │
│ Gray 300   #d4d4d4  ████  Disabled borders                 │
│ Gray 400   #a3a3a3  ████  Placeholder text                 │
│ Gray 500   #737373  ████  Secondary text                   │
│ Gray 600   #525252  ████  Body text                        │
│ Gray 700   #404040  ████  Headings                         │
│ Gray 800   #262626  ████  Dark headings                    │
│ Gray 900   #171717  ████  Primary text                     │
└─────────────────────────────────────────────────────────────┘
```

### Semantic Colors

```
┌─────────────────────────────────────────────────────────────┐
│ SEMANTIC COLORS                                             │
├─────────────────────────────────────────────────────────────┤
│ Success    #22c55e  ████  Order confirmed, in stock        │
│ Warning    #f59e0b  ████  Low stock, pending               │
│ Error      #ef4444  ████  Out of stock, errors             │
│ Info       #3b82f6  ████  Notifications, tips              │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 Application Examples

### 1. Homepage Hero Section

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  Background: Pink 50 (#fdf2f8)                             │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐ │
│  │                                                         │ │
│  │  Fresh Flowers Delivered Daily                         │ │
│  │  Text: Gray 900 (#171717)                              │ │
│  │  Font: 48px, Bold                                      │ │
│  │                                                         │ │
│  │  Brighten someone's day with our premium collection    │ │
│  │  Text: Gray 600 (#525252)                              │ │
│  │  Font: 18px, Regular                                   │ │
│  │                                                         │ │
│  │  ┌─────────────────────────────────────────────────┐  │ │
│  │  │  Shop Now                                        │  │ │
│  │  │  Background: Pink 500 (#ec4899)                  │  │ │
│  │  │  Text: White (#ffffff)                           │  │ │
│  │  │  Hover: Pink 600 (#db2777)                       │  │ │
│  │  └─────────────────────────────────────────────────┘  │ │
│  │                                                         │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 2. Product Card

```
┌─────────────────────────────────────────┐
│  ┌───────────────────────────────────┐  │
│  │                                   │  │
│  │  [Product Image]                  │  │
│  │                                   │  │
│  └───────────────────────────────────┘  │
│                                         │
│  Background: White (#ffffff)            │
│  Border: Gray 200 (#e5e5e5)            │
│  Shadow: 0 2px 8px rgba(0,0,0,0.1)     │
│                                         │
│  Rose Bouquet                           │
│  Text: Gray 900 (#171717)              │
│  Font: 18px, Semibold                  │
│                                         │
│  ★★★★★ (127 reviews)                  │
│  Stars: Warning (#f59e0b)              │
│  Count: Gray 500 (#737373)             │
│                                         │
│  500,000đ                               │
│  Text: Pink 500 (#ec4899)              │
│  Font: 24px, Bold                      │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │  Add to Cart                      │ │
│  │  Background: Pink 500 (#ec4899)   │ │
│  │  Text: White (#ffffff)            │ │
│  │  Hover: Pink 600 (#db2777)        │ │
│  └───────────────────────────────────┘ │
│                                         │
└─────────────────────────────────────────┘
```

### 3. Navigation Bar

```
┌─────────────────────────────────────────────────────────────┐
│  Background: White (#ffffff)                                │
│  Border Bottom: Gray 200 (#e5e5e5)                         │
│  Shadow: 0 1px 3px rgba(0,0,0,0.1)                         │
│                                                             │
│  [Logo]  Home  Products  About  Contact    [Cart] [User]   │
│          ────                                               │
│  Links: Gray 600 (#525252)                                 │
│  Active: Pink 500 (#ec4899) + underline                    │
│  Hover: Pink 500 (#ec4899)                                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 4. Form Elements

```
┌─────────────────────────────────────────┐
│  Email Address                          │
│  Label: Gray 700 (#404040)             │
│  Font: 14px, Medium                    │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │ your@email.com                    │ │
│  │ Background: White (#ffffff)       │ │
│  │ Border: Gray 300 (#d4d4d4)       │ │
│  │ Focus: Pink 500 (#ec4899)        │ │
│  │ Text: Gray 900 (#171717)         │ │
│  └───────────────────────────────────┘ │
│                                         │
│  ✓ Email is valid                      │
│  Success: Green 500 (#22c55e)          │
│                                         │
│  ✗ Email is required                   │
│  Error: Error (#ef4444)                │
│                                         │
└─────────────────────────────────────────┘
```

### 5. Status Badges

```
┌─────────────────────────────────────────┐
│  Order Status Badges                    │
│                                         │
│  ┌──────────────┐                      │
│  │  In Stock    │                      │
│  │  Background: Green 100 (#dcfce7)   │ │
│  │  Text: Green 700 (#15803d)         │ │
│  │  Border: Green 500 (#22c55e)       │ │
│  └──────────────┘                      │
│                                         │
│  ┌──────────────┐                      │
│  │  Low Stock   │                      │
│  │  Background: Warning 100           │ │
│  │  Text: Warning 700                 │ │
│  │  Border: Warning 500               │ │
│  └──────────────┘                      │
│                                         │
│  ┌──────────────┐                      │
│  │  Out of Stock│                      │
│  │  Background: Error 100             │ │
│  │  Text: Error 700                   │ │
│  │  Border: Error 500                 │ │
│  └──────────────┘                      │
│                                         │
└─────────────────────────────────────────┘
```

---

## 💻 CSS Implementation

```css
:root {
  /* Primary - Pink */
  --color-primary-50: #fdf2f8;
  --color-primary-100: #fce7f3;
  --color-primary-200: #fbcfe8;
  --color-primary-300: #f9a8d4;
  --color-primary-400: #f472b6;
  --color-primary-500: #ec4899;
  --color-primary-600: #db2777;
  --color-primary-700: #be185d;
  --color-primary-800: #9f1239;
  --color-primary-900: #831843;
  
  /* Secondary - Green */
  --color-secondary-50: #f0fdf4;
  --color-secondary-100: #dcfce7;
  --color-secondary-500: #22c55e;
  --color-secondary-600: #16a34a;
  --color-secondary-700: #15803d;
  
  /* Neutrals - Gray */
  --color-gray-50: #fafafa;
  --color-gray-100: #f5f5f5;
  --color-gray-200: #e5e5e5;
  --color-gray-300: #d4d4d4;
  --color-gray-400: #a3a3a3;
  --color-gray-500: #737373;
  --color-gray-600: #525252;
  --color-gray-700: #404040;
  --color-gray-800: #262626;
  --color-gray-900: #171717;
  
  /* Semantic */
  --color-success: #22c55e;
  --color-warning: #f59e0b;
  --color-error: #ef4444;
  --color-info: #3b82f6;
  
  /* Aliases */
  --color-primary: var(--color-primary-500);
  --color-primary-hover: var(--color-primary-600);
  --color-primary-active: var(--color-primary-700);
  
  --color-text-primary: var(--color-gray-900);
  --color-text-secondary: var(--color-gray-600);
  --color-text-muted: var(--color-gray-500);
  
  --color-bg-primary: #ffffff;
  --color-bg-secondary: var(--color-gray-50);
  --color-bg-tertiary: var(--color-gray-100);
  
  --color-border: var(--color-gray-200);
  --color-border-hover: var(--color-gray-300);
}

/* Dark mode */
@media (prefers-color-scheme: dark) {
  :root {
    --color-text-primary: var(--color-gray-50);
    --color-text-secondary: var(--color-gray-400);
    --color-text-muted: var(--color-gray-500);
    
    --color-bg-primary: var(--color-gray-900);
    --color-bg-secondary: var(--color-gray-800);
    --color-bg-tertiary: var(--color-gray-700);
    
    --color-border: var(--color-gray-700);
    --color-border-hover: var(--color-gray-600);
  }
}
```

### Usage in Components

```css
/* Button */
.button-primary {
  background-color: var(--color-primary);
  color: white;
}

.button-primary:hover {
  background-color: var(--color-primary-hover);
}

.button-primary:active {
  background-color: var(--color-primary-active);
}

/* Card */
.card {
  background-color: var(--color-bg-primary);
  border: 1px solid var(--color-border);
}

/* Text */
.text-primary {
  color: var(--color-text-primary);
}

.text-secondary {
  color: var(--color-text-secondary);
}

/* Badge */
.badge-success {
  background-color: var(--color-secondary-100);
  color: var(--color-secondary-700);
  border: 1px solid var(--color-secondary-500);
}
```

---

## 🎨 Tailwind Configuration

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#fdf2f8',
          100: '#fce7f3',
          200: '#fbcfe8',
          300: '#f9a8d4',
          400: '#f472b6',
          500: '#ec4899',
          600: '#db2777',
          700: '#be185d',
          800: '#9f1239',
          900: '#831843',
        },
        secondary: {
          50: '#f0fdf4',
          100: '#dcfce7',
          500: '#22c55e',
          600: '#16a34a',
          700: '#15803d',
        },
      },
    },
  },
}
```

---

## ✅ Color Usage Guidelines

### Do's
✅ Use primary color for main CTAs
✅ Use secondary color for success states
✅ Use gray scale for text hierarchy
✅ Use semantic colors for status
✅ Maintain consistent color meaning
✅ Test color contrast (WCAG AA)

### Don'ts
❌ Use too many colors (stick to palette)
❌ Use color as only indicator
❌ Ignore accessibility
❌ Mix color systems
❌ Use primary for everything

---

## 📊 Color Contrast Ratios

```
Text on White Background:
- Gray 900: 16.1:1 ✅ AAA
- Gray 700: 10.4:1 ✅ AAA
- Gray 600: 7.5:1 ✅ AAA
- Gray 500: 4.7:1 ✅ AA
- Pink 500: 4.9:1 ✅ AA

White Text on Colored Background:
- Pink 500: 4.9:1 ✅ AA
- Pink 600: 6.3:1 ✅ AAA
- Green 500: 3.1:1 ⚠️ Large text only
- Green 600: 4.1:1 ✅ AA
```

---

## 🧪 Testing Checklist

- [ ] All colors defined in design system
- [ ] Color contrast meets WCAG AA
- [ ] Dark mode colors work
- [ ] Semantic colors consistent
- [ ] Color blind friendly
- [ ] Print styles considered
