# Design Phase Templates

**Phase 3/7**: UI/UX Design, Component Specifications, Design Systems

---

## 📁 Structure

```
3-design/
├── templates/           # Ready-to-use design templates
│   ├── design-system.md
│   ├── component-spec.md
│   ├── accessibility.md
│   └── responsive-design.md
├── prompts/            # AI tool design patterns
│   ├── lovable-design-patterns.md
│   └── v0-design-patterns.md
└── README.md
```

---

## 🎨 Templates

### 1. Design System Template
**File**: `templates/design-system.md`

**Purpose**: Define cohesive visual language

**Includes**:
- Color system (3-5 colors max)
- Typography (2 font families max)
- Spacing scale
- Component patterns
- Design tokens

**When to use**: Start of design phase, before creating components

---

### 2. Component Specification Template
**File**: `templates/component-spec.md`

**Purpose**: Document component design details

**Includes**:
- Visual specifications
- Responsive behavior
- States (hover, focus, disabled)
- Variants (size, style)
- Accessibility requirements
- Usage examples

**When to use**: For each major UI component

---

### 3. Accessibility Template
**File**: `templates/accessibility.md`

**Purpose**: Ensure WCAG 2.1 AA compliance

**Includes**:
- Semantic HTML patterns
- ARIA attributes
- Color contrast requirements
- Keyboard navigation
- Screen reader support
- Touch target sizing

**When to use**: Throughout design and development

---

### 4. Responsive Design Template
**File**: `templates/responsive-design.md`

**Purpose**: Mobile-first responsive patterns

**Includes**:
- Breakpoint system
- Layout patterns
- Typography scaling
- Mobile optimizations
- Navigation patterns
- Testing checklist

**When to use**: For all layouts and components

---

## 🤖 AI Tool Patterns

### Lovable Design Patterns
**File**: `prompts/lovable-design-patterns.md`

**Key Principles**:
- Design system is everything
- Semantic tokens only (NO direct colors)
- Component variants for shadcn
- Beautiful by default

**Best for**: React + Vite + Tailwind projects

---

### v0 Design Patterns
**File**: `prompts/v0-design-patterns.md`

**Key Principles**:
- 3-5 colors maximum
- 2 font families maximum
- Mobile-first always
- Tailwind scale preferred

**Best for**: Next.js + shadcn/ui projects

---

## 🎯 Quick Start

### Step 1: Define Design System
```bash
# Copy template
cp templates/design-system.md your-project/design-system.md

# Fill in:
# - Brand colors (1 primary, 2-3 neutrals, 1-2 accents)
# - Font families (heading + body)
# - Spacing scale
# - Design tokens
```

### Step 2: Create Component Specs
```bash
# For each major component
cp templates/component-spec.md your-project/components/button-spec.md

# Document:
# - Visual appearance
# - Responsive behavior
# - States and variants
# - Accessibility
```

### Step 3: Ensure Accessibility
```bash
# Reference throughout development
cat templates/accessibility.md

# Check:
# - Semantic HTML
# - ARIA attributes
# - Color contrast
# - Keyboard navigation
```

### Step 4: Implement Responsive Design
```bash
# Apply mobile-first patterns
cat templates/responsive-design.md

# Implement:
# - Mobile base styles
# - Tablet enhancements (md:)
# - Desktop enhancements (lg:)
```

---

## 📋 Design Checklist

### Color System
- [ ] 3-5 colors total (1 primary, 2-3 neutrals, 1-2 accents)
- [ ] NO direct colors (text-white, bg-blue-500)
- [ ] Use semantic tokens (bg-background, text-foreground)
- [ ] Proper contrast ratios (WCAG AA minimum)
- [ ] NO gradients unless requested

### Typography
- [ ] Maximum 2 font families
- [ ] Line-height 1.4-1.6 for body text
- [ ] Minimum 14px font size
- [ ] Responsive scaling (mobile → tablet → desktop)

### Layout
- [ ] Mobile-first approach
- [ ] Flexbox for most layouts
- [ ] CSS Grid for complex 2D layouts
- [ ] Proper spacing (gap classes, NO space-*)
- [ ] Responsive breakpoints (sm, md, lg, xl)

### Accessibility
- [ ] Semantic HTML elements
- [ ] ARIA attributes where needed
- [ ] Alt text for all images
- [ ] Keyboard navigation support
- [ ] Minimum 44px touch targets
- [ ] Screen reader friendly

### Components
- [ ] Small, focused components
- [ ] Variants for different use cases
- [ ] All states defined (hover, focus, disabled)
- [ ] Consistent with design system
- [ ] Reusable across project

---

## 🔗 Related Phases

- **Previous**: [2-planning](../2-planning/) - Architecture and technical planning
- **Next**: [4-development](../4-development/) - Implementation

---

## 📚 Key Concepts

### Design System
Cohesive set of design decisions (colors, typography, spacing) applied consistently across entire project.

### Semantic Tokens
Named CSS variables representing design intent (--primary, --background) rather than specific values (--blue-500).

### Mobile-First
Design for smallest screen first, then enhance for larger screens using responsive breakpoints.

### Component Variants
Different visual styles of same component (button: default, outline, ghost, destructive).

### WCAG AA
Web Content Accessibility Guidelines Level AA - minimum standard for accessible websites.

---

## 💡 Best Practices

### DO
✅ Define design system before creating components  
✅ Use semantic design tokens consistently  
✅ Design mobile-first, enhance for desktop  
✅ Ensure accessibility from the start  
✅ Create small, reusable components  
✅ Document component specifications  
✅ Test across devices and screen sizes  

### DON'T
❌ Use direct colors (text-white, bg-blue-500)  
❌ Exceed 5 total colors without permission  
❌ Use more than 2 font families  
❌ Add gradients unless requested  
❌ Create large monolithic components  
❌ Skip accessibility considerations  
❌ Design desktop-first  

---

## 🛠️ Tools & Resources

### Design Tools
- **Figma**: UI design and prototyping
- **Tailwind CSS**: Utility-first CSS framework
- **shadcn/ui**: Re-usable component library

### Accessibility Testing
- **Lighthouse**: Chrome DevTools audit
- **axe DevTools**: Browser extension
- **WAVE**: Web accessibility evaluation tool
- **WebAIM Contrast Checker**: Color contrast testing

### Color Tools
- **Coolors**: Color palette generator
- **Contrast Ratio**: WCAG contrast checker
- **HSL Color Picker**: HSL color selection

### Typography
- **Google Fonts**: Free font library
- **Font Pair**: Font pairing suggestions
- **Type Scale**: Typography scale calculator

---

## 📖 Examples

### Example 1: E-commerce Design System
```
Colors:
- Primary: hsl(210, 100%, 50%) - Blue (brand)
- Neutral 1: hsl(0, 0%, 100%) - White
- Neutral 2: hsl(0, 0%, 95%) - Light gray
- Neutral 3: hsl(0, 0%, 20%) - Dark gray
- Accent: hsl(150, 60%, 45%) - Green (success)

Typography:
- Heading: Inter (weights: 600, 700)
- Body: Inter (weights: 400, 500)

Spacing: Tailwind default scale (4, 8, 16, 24, 32, 48px)
```

### Example 2: SaaS Landing Page Components
```
Components:
1. Hero Section
   - Variants: default, with-image, centered
   - Responsive: stack mobile, side-by-side desktop
   
2. Feature Card
   - Variants: default, highlighted, compact
   - States: default, hover
   
3. CTA Button
   - Variants: primary, secondary, outline
   - States: default, hover, focus, disabled
   - Size: sm, md, lg
```

---

**Last Updated**: 2026-04-23  
**Phase**: 3/7 - Design  
**Status**: ✅ Complete
