# Lovable Design Patterns

**Source**: Lovable Agent Prompt  
**Focus**: Design system, component patterns, visual guidelines

---

## Design System Philosophy

### CRITICAL Rule
> "The design system is everything. You should never write custom styles in components, you should always use the design system and customize it."

### Core Principles
1. **Semantic tokens only** - NO direct colors (text-white, bg-white)
2. **Design system first** - Define in `index.css` and `tailwind.config.ts`
3. **Component variants** - Customize shadcn components with variants
4. **Reusability** - Maximize component reuse

---

## Color System

### Semantic Token Approach
```css
/* index.css - Define design tokens */
:root {
  --primary: [hsl values for main brand color];
  --primary-glow: [lighter version of primary];
  --secondary: [appropriate hsl values];
  --accent: [complementary color];
  
  /* Gradients */
  --gradient-primary: linear-gradient(135deg, hsl(var(--primary)), hsl(var(--primary-glow)));
  --gradient-subtle: linear-gradient(180deg, [background-start], [background-end]);
  
  /* Shadows */
  --shadow-elegant: 0 10px 30px -10px hsl(var(--primary) / 0.3);
  --shadow-glow: 0 0 40px hsl(var(--primary-glow) / 0.4);
  
  /* Animations */
  --transition-smooth: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
```

### Usage in Components
```tsx
// ✅ CORRECT - Use semantic tokens
<Button variant="default">Submit</Button>
<a className="text-primary">Link</a>

// ❌ WRONG - Direct colors
<Button className="bg-blue-500">Submit</Button>
<a className="text-blue-600">Link</a>
```

### Color Function Matching
- **ALWAYS use HSL colors** in index.css and tailwind.config.ts
- **Check CSS variable format** before using in color functions
- If RGB colors exist, DON'T wrap in hsl() functions

---

## Component Variants

### Creating Variants
```tsx
// button.tsx - Add variants using design system
const buttonVariants = cva(
  "...",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground",
        premium: "bg-gradient-to-r from-primary to-primary-glow",
        hero: "bg-white/10 text-white border border-white/20 hover:bg-white/20",
        outline: "border border-input bg-background hover:bg-accent",
      }
    }
  }
)
```

### Shadcn Component Customization
- Review and customize shadcn components
- Create variants for different use cases
- Use design system tokens consistently
- **Note**: Outline variants not transparent by default

---

## Typography

### Font Setup
```tsx
// Never use explicit classes in components
// ❌ WRONG
<h1 className="text-white font-bold">Title</h1>

// ✅ CORRECT - Define in design system
// tailwind.config.ts
theme: {
  extend: {
    fontFamily: {
      heading: ['var(--font-heading)'],
      body: ['var(--font-body)'],
    }
  }
}

// Component usage
<h1 className="font-heading text-4xl">Title</h1>
```

---

## Layout & Spacing

### Design System Approach
```css
/* index.css - Define spacing tokens */
:root {
  --spacing-xs: 0.5rem;
  --spacing-sm: 1rem;
  --spacing-md: 1.5rem;
  --spacing-lg: 2rem;
  --spacing-xl: 3rem;
}
```

### Component Structure
- Create small, focused components
- Avoid large monolithic files
- Split functionality into separate modules

---

## Responsive Design

### Always Generate Responsive
- Mobile-first approach
- Use Tailwind responsive prefixes
- Test across breakpoints

```tsx
<div className="
  grid grid-cols-1 gap-4
  md:grid-cols-2 md:gap-6
  lg:grid-cols-3 lg:gap-8
">
  {items.map(item => <Card key={item.id} />)}
</div>
```

---

## Beautiful Design Requirements

### Visual Excellence
- Pay attention to contrast, color, typography
- Edit `index.css` and `tailwind.config.ts` frequently
- Avoid boring designs - leverage colors and animations
- Consider dark vs light mode styles

### Dark/Light Mode
```css
/* index.css */
:root {
  --background: 0 0% 100%;
  --foreground: 222.2 84% 4.9%;
}

.dark {
  --background: 222.2 84% 4.9%;
  --foreground: 210 40% 98%;
}
```

---

## SEO Best Practices

### Always Implement
- **Title tags**: Include main keyword, < 60 characters
- **Meta description**: Max 160 characters with keyword
- **Single H1**: Match page's primary intent
- **Semantic HTML**: Use proper elements
- **Image optimization**: Descriptive alt attributes
- **Structured data**: JSON-LD when applicable
- **Performance**: Lazy loading, defer scripts
- **Canonical tags**: Prevent duplicate content
- **Mobile optimization**: Responsive with viewport meta
- **Clean URLs**: Descriptive, crawlable links

---

## First Impression Guidelines

### Initial Project Setup
1. Think about what user wants to build
2. Draw inspiration from existing beautiful designs
3. List features for first version (don't do too much)
4. List colors, gradients, animations, fonts, styles
5. Start with design system (CRITICAL)
6. Edit `tailwind.config.ts` and `index.css` based on design
7. Create custom variants for shadcn components
8. Use semantic tokens for everything
9. Generate images with imagegen tool (no placeholders)
10. Create separate component files (not one large index)

### Design System First
```tsx
// ❌ NEVER Write
<button className="bg-blue-500 text-white px-4 py-2 rounded">
  Click me
</button>

// ✅ ALWAYS Write
// First enhance design system in index.css and tailwind.config.ts
<Button variant="hero">Click me</Button>  // Beautiful by design
```

---

## Anti-Patterns to Avoid

### Direct Color Usage
```tsx
// ❌ WRONG
<div className="bg-white text-black">Content</div>
<div className="bg-blue-500">Content</div>

// ✅ CORRECT
<div className="bg-background text-foreground">Content</div>
<div className="bg-primary text-primary-foreground">Content</div>
```

### Inline Style Overrides
```tsx
// ❌ WRONG - Hacky inline overrides
<div className="bg-blue-500 hover:bg-blue-600">Button</div>

// ✅ CORRECT - Define in design system
// Update index.css with design tokens, then:
<Button variant="primary">Button</Button>
```

### White Text on White Background
- Pay attention to dark vs light mode
- Ensure correct styles for each mode
- Test contrast in both themes

---

## Image & Media

### Image Generation
- Use imagegen tool for hero images, banners
- Generate images instead of using placeholder URLs
- Never leave placeholder images in design
- Can use web_search for real people/facts images

### Media Files
- Support for `glb`, `gltf`, `mp3` files
- Use native `<audio>` element for audio
- JavaScript for audio control

---

## Key Takeaways

1. **Design system is everything** - Define once, use everywhere
2. **Semantic tokens only** - No direct colors
3. **Component variants** - Customize shadcn components
4. **Beautiful by default** - Leverage colors, animations, gradients
5. **Responsive always** - Mobile-first approach
6. **SEO built-in** - Implement best practices automatically
7. **Small components** - Split functionality, avoid monoliths
8. **Dark/light mode** - Consider both themes

---

**Source**: Lovable Agent Prompt (lines 204-304)
