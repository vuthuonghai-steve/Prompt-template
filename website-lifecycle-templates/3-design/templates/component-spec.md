# Component Specification Template

## Component Overview

**Name**: [ComponentName]  
**Purpose**: [Brief description of component's role]  
**Category**: [UI Element / Layout / Form / Navigation / Data Display]

---

## Visual Specifications

### Layout
- **Container**: [flex / grid / block]
- **Spacing**: [gap-4, p-6, etc.]
- **Alignment**: [items-center, justify-between, etc.]

### Colors
- **Background**: [bg-background / bg-primary]
- **Text**: [text-foreground / text-muted-foreground]
- **Border**: [border-border]
- **Hover/Focus**: [hover:bg-accent, focus:ring-ring]

### Typography
- **Font**: [font-sans / font-serif]
- **Size**: [text-base / text-lg]
- **Weight**: [font-normal / font-semibold]
- **Line Height**: [leading-relaxed]

### Dimensions
- **Width**: [w-full / max-w-md]
- **Height**: [h-auto / min-h-[44px]]
- **Padding**: [p-4 / px-6 py-3]
- **Border Radius**: [rounded-md / rounded-lg]

---

## Responsive Behavior

### Mobile (< 640px)
- [Mobile-specific styles]
- [Touch target: minimum 44px]

### Tablet (640px - 1024px)
- [Tablet-specific styles]

### Desktop (> 1024px)
- [Desktop-specific styles]

---

## States

### Default
```tsx
<Component className="[default classes]" />
```

### Hover
```tsx
hover:bg-accent hover:text-accent-foreground
```

### Focus
```tsx
focus:outline-none focus:ring-2 focus:ring-ring
```

### Disabled
```tsx
disabled:opacity-50 disabled:cursor-not-allowed
```

### Active/Selected
```tsx
data-[state=active]:bg-primary data-[state=active]:text-primary-foreground
```

---

## Variants

### Size Variants
- **sm**: [Small size classes]
- **md**: [Medium size classes - default]
- **lg**: [Large size classes]

### Style Variants
- **default**: [Default appearance]
- **outline**: [Outlined style]
- **ghost**: [Minimal style]
- **destructive**: [Error/warning style]

---

## Accessibility

### Semantic HTML
- Use appropriate HTML element: `<button>`, `<nav>`, `<main>`, etc.

### ARIA Attributes
- `aria-label`: [Descriptive label]
- `aria-describedby`: [ID of description element]
- `role`: [ARIA role if needed]

### Keyboard Navigation
- **Tab**: Focus navigation
- **Enter/Space**: Activation
- **Escape**: Close/cancel
- **Arrow keys**: [If applicable]

### Screen Reader
- Meaningful text content
- `sr-only` class for hidden labels
- Alt text for images

---

## Component Structure

```tsx
interface ComponentProps {
  // Props definition
  variant?: 'default' | 'outline' | 'ghost'
  size?: 'sm' | 'md' | 'lg'
  className?: string
  children?: React.ReactNode
}

export function Component({ 
  variant = 'default',
  size = 'md',
  className,
  children 
}: ComponentProps) {
  return (
    <div className={cn(
      // Base styles
      "flex items-center justify-center",
      "rounded-md border border-border",
      "bg-background text-foreground",
      
      // Variants
      variant === 'outline' && "bg-transparent",
      variant === 'ghost' && "border-transparent",
      
      // Sizes
      size === 'sm' && "text-sm p-2",
      size === 'md' && "text-base p-4",
      size === 'lg' && "text-lg p-6",
      
      // Custom classes
      className
    )}>
      {children}
    </div>
  )
}
```

---

## Usage Examples

### Basic Usage
```tsx
<Component>Content</Component>
```

### With Variants
```tsx
<Component variant="outline" size="lg">
  Large Outlined Component
</Component>
```

### With Custom Styling
```tsx
<Component className="max-w-md mx-auto">
  Centered Component
</Component>
```

---

## Design Checklist

- [ ] Uses semantic design tokens (no direct colors)
- [ ] Mobile-first responsive design
- [ ] Minimum 44px touch targets
- [ ] Proper contrast ratios (WCAG AA)
- [ ] Keyboard accessible
- [ ] Screen reader friendly
- [ ] Consistent with design system
- [ ] All states defined (hover, focus, disabled)

---

**Sources**: v0, Lovable component patterns
