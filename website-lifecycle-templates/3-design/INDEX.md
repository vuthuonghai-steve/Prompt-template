# Phase 3: Design UI/UX

> **Mục tiêu**: Visual design, components, responsive, accessibility
> **Đầu ra**: High-fidelity designs, prototype, design system
> **Last Updated**: 2026-04-23

---

## 🔗 Quick Navigation

| Section | Description |
|---------|-------------|
| [Patterns](#-patterns) | Design patterns, workflows |
| [Prompts](#-prompts) | AI tool prompts for design |
| [Templates](#-templates) | Document templates |
| [Examples](#-examples) | Real-world examples |

---

## 📋 Design Checklist

- [ ] Chuyển wireframe thành visual design
- [ ] Định nghĩa color palette & typography
- [ ] Thiết kế component library
- [ ] Design states (hover, active, disabled, error)
- [ ] Responsive design (mobile, tablet, desktop)
- [ ] Accessibility compliance (WCAG)
- [ ] Tạo interactive prototype
- [ ] Design review & approval

---

## 🎨 Patterns

Patterns và best practices hiện có cho phase này.

| Pattern | Purpose | Link |
|---|---|---|
| `pattern-color-system.md` | Use a constrained, semantic color system | [View](./patterns/pattern-color-system.md) |
| `pattern-design-system-first.md` | Define tokens/components before screens | [View](./patterns/pattern-design-system-first.md) |
| `pattern-mobile-first.md` | Design from small screens upward | [View](./patterns/pattern-mobile-first.md) |
| `pattern-typography-system.md` | Keep typography consistent and minimal | [View](./patterns/pattern-typography-system.md) |

---

## 🤖 Prompts

AI tool prompts for automation.

| Tool | Purpose | Link |
|------|---------|------|
| **Lovable** | Design system, semantic tokens for React + Vite + Tailwind | [View](./prompts/lovable-design-patterns.md) |
| **v0** | Color limits, mobile-first for Next.js + shadcn/ui | [View](./prompts/v0-design-patterns.md) |

---

## 📁 Templates

Document templates và checklists.

| Template | Purpose | Link |
|----------|---------|------|
| `design-system.md` | Color, typography, spacing system | [View](./templates/design-system.md) |
| `component-spec.md` | Component documentation | [View](./templates/component-spec.md) |
| `accessibility.md` | WCAG AA compliance guide | [View](./templates/accessibility.md) |
| `responsive-design.md` | Mobile-first patterns | [View](./templates/responsive-design.md) |

---

## 💡 Examples

Real-world examples và sample outputs.

| Example | Description | Link |
|---|---|---|
| `example-button-component.md` | Button component spec sample | [View](./examples/example-button-component.md) |
| `example-color-palette-application.md` | Color palette application sample | [View](./examples/example-color-palette-application.md) |
| `example-design-system-tokens.md` | Design token sample | [View](./examples/example-design-system-tokens.md) |
| `example-responsive-product-card.md` | Responsive product card sample | [View](./examples/example-responsive-product-card.md) |

---

## 🎯 Quick Reference

### Design System Rules
- **Colors**: 3-5 maximum (1 primary, 2-3 neutrals, 1-2 accents)
- **Fonts**: 2 maximum (heading + body)
- **Tokens**: Use semantic (bg-background, text-foreground)
- **NO**: Direct colors (text-white, bg-blue-500)

### Accessibility Checklist
- [ ] Semantic HTML elements
- [ ] ARIA attributes where needed
- [ ] Alt text for images
- [ ] Keyboard navigation
- [ ] 44px minimum touch targets
- [ ] WCAG AA contrast ratios

### Responsive Approach
1. Design mobile-first (base styles)
2. Enhance for tablet (md: prefix)
3. Enhance for desktop (lg: prefix)
4. Test across breakpoints

---

## 📖 Resources

- [STRUCTURE.md](../STRUCTURE.md) - Structure guidelines

---

## 🔗 Navigation

[← Previous: Planning](../2-planning/INDEX.md) | [Next: Content →](../4-content/INDEX.md)
