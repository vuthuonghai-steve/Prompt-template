# Responsive Design Template

## Mobile-First Approach

**Priority**: Mobile is PRIMARY experience, desktop is secondary

---

## Breakpoint System

### Tailwind Breakpoints
- **sm**: 640px (Small tablets)
- **md**: 768px (Tablets)
- **lg**: 1024px (Laptops)
- **xl**: 1280px (Desktops)
- **2xl**: 1536px (Large desktops)

### Usage Pattern
```tsx
// Mobile-first: Base styles apply to mobile, then enhance
<div className="
  text-sm p-4           // Mobile (default)
  md:text-base md:p-6   // Tablet
  lg:text-lg lg:p-8     // Desktop
">
  Content
</div>
```

---

## Layout Patterns

### Stack → Side-by-Side
```tsx
// Mobile: Vertical stack
// Desktop: Horizontal layout
<div className="
  flex flex-col gap-4
  md:flex-row md:gap-6
">
  <div>Item 1</div>
  <div>Item 2</div>
</div>
```

### Single Column → Grid
```tsx
// Mobile: Single column
// Tablet: 2 columns
// Desktop: 3-4 columns
<div className="
  grid grid-cols-1 gap-4
  md:grid-cols-2 md:gap-6
  lg:grid-cols-3 lg:gap-8
">
  {items.map(item => <Card key={item.id} />)}
</div>
```

### Full Width → Constrained
```tsx
// Mobile: Full width
// Desktop: Constrained with max-width
<div className="
  w-full px-4
  md:max-w-2xl md:mx-auto
  lg:max-w-4xl
">
  Content
</div>
```

---

## Typography Scaling

### Heading Sizes
```tsx
<h1 className="
  text-2xl font-bold      // Mobile
  md:text-3xl             // Tablet
  lg:text-4xl             // Desktop
">
  Heading
</h1>
```

### Body Text
```tsx
<p className="
  text-sm leading-relaxed  // Mobile
  md:text-base             // Tablet
  lg:text-lg               // Desktop
">
  Body text
</p>
```

---

## Spacing Adjustments

### Padding/Margin
```tsx
<section className="
  py-8 px-4       // Mobile
  md:py-12 md:px-6  // Tablet
  lg:py-16 lg:px-8  // Desktop
">
  Content
</section>
```

### Gap Between Elements
```tsx
<div className="
  flex flex-col gap-4   // Mobile
  md:gap-6              // Tablet
  lg:gap-8              // Desktop
">
  Elements
</div>
```

---

## Mobile-Specific Optimizations

### iOS Safari
```tsx
// layout.tsx
export const viewport = {
  width: 'device-width',
  initialScale: 1,
  maximumScale: 1,  // Disable auto-zoom
  userScalable: false
}
```

### Touch Targets
```tsx
// Minimum 44px for interactive elements
<button className="
  min-h-[44px] min-w-[44px]
  px-4 py-2
">
  Button
</button>
```

### Input Fields
```tsx
// Minimum 16px font to prevent zoom on iOS
<input className="
  text-base  // 16px minimum
  px-4 py-3
" />
```

---

## Navigation Patterns

### Mobile Menu
```tsx
// Mobile: Hamburger menu
// Desktop: Horizontal nav
<nav className="
  fixed bottom-0 left-0 right-0  // Mobile: Bottom nav
  md:static md:flex md:items-center  // Desktop: Top nav
">
  <MobileMenu className="md:hidden" />
  <DesktopMenu className="hidden md:flex" />
</nav>
```

### Sidebar
```tsx
// Mobile: Drawer/overlay
// Desktop: Fixed sidebar
<aside className="
  fixed inset-y-0 left-0 z-50 w-64
  transform -translate-x-full transition-transform  // Mobile: Hidden
  md:translate-x-0 md:static  // Desktop: Visible
">
  Sidebar content
</aside>
```

---

## Content Visibility

### Show/Hide Elements
```tsx
// Show only on mobile
<div className="block md:hidden">
  Mobile-only content
</div>

// Show only on desktop
<div className="hidden md:block">
  Desktop-only content
</div>

// Show on tablet and up
<div className="hidden md:block">
  Tablet+ content
</div>
```

---

## Image Optimization

### Responsive Images
```tsx
<img 
  src="/image.jpg"
  srcSet="
    /image-mobile.jpg 640w,
    /image-tablet.jpg 1024w,
    /image-desktop.jpg 1920w
  "
  sizes="
    (max-width: 640px) 100vw,
    (max-width: 1024px) 50vw,
    33vw
  "
  alt="Description"
  className="w-full h-auto"
/>
```

### Next.js Image
```tsx
import Image from 'next/image'

<Image
  src="/image.jpg"
  alt="Description"
  width={800}
  height={600}
  className="
    w-full h-auto
    md:w-1/2
  "
  priority  // For above-the-fold images
/>
```

---

## Testing Checklist

### Mobile (< 640px)
- [ ] Touch targets minimum 44px
- [ ] Text minimum 16px for inputs
- [ ] No horizontal scroll
- [ ] Content readable without zoom
- [ ] Navigation accessible
- [ ] Forms easy to fill

### Tablet (640px - 1024px)
- [ ] Layout adapts appropriately
- [ ] Images scale correctly
- [ ] Navigation works well
- [ ] Content well-spaced

### Desktop (> 1024px)
- [ ] Max-width constraints applied
- [ ] Content not stretched
- [ ] Hover states work
- [ ] Keyboard navigation smooth

### Cross-Device
- [ ] Consistent branding
- [ ] Same functionality across devices
- [ ] Performance optimized
- [ ] Images load efficiently

---

## Common Patterns

### Hero Section
```tsx
<section className="
  py-12 px-4 text-center
  md:py-20 md:px-6
  lg:py-28 lg:px-8
">
  <h1 className="text-3xl md:text-4xl lg:text-5xl font-bold">
    Hero Title
  </h1>
  <p className="mt-4 text-base md:text-lg lg:text-xl">
    Hero description
  </p>
</section>
```

### Card Grid
```tsx
<div className="
  grid grid-cols-1 gap-4 p-4
  sm:grid-cols-2 sm:gap-6
  lg:grid-cols-3 lg:gap-8 lg:p-8
">
  {cards.map(card => <Card key={card.id} {...card} />)}
</div>
```

### Form Layout
```tsx
<form className="
  space-y-4 p-4
  md:space-y-6 md:p-6 md:max-w-md md:mx-auto
">
  <input className="w-full text-base px-4 py-3" />
  <button className="w-full md:w-auto px-6 py-3">
    Submit
  </button>
</form>
```

---

**Sources**: v0 mobile-first guidelines, Lovable responsive patterns
