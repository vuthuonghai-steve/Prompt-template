# Phase 3: Design UI/UX

> **Mục tiêu**: Visual design, components, responsive, accessibility
> **Đầu ra**: High-fidelity designs, prototype, design system

---

## 📋 Checklist

- [ ] Chuyển wireframe thành visual design
- [ ] Định nghĩa color palette & typography
- [ ] Thiết kế component library
- [ ] Design states (hover, active, disabled, error)
- [ ] Responsive design (mobile, tablet, desktop)
- [ ] Accessibility compliance (WCAG)
- [ ] Tạo interactive prototype
- [ ] Design review & approval

---

## 📁 Templates

| Template | Purpose | When to Use |
|----------|---------|-------------|
| [design-system.md](templates/design-system.md) | Color, typography, spacing system | Start of design phase |
| [component-spec.md](templates/component-spec.md) | Component documentation | For each major component |
| [accessibility.md](templates/accessibility.md) | WCAG AA compliance guide | Throughout development |
| [responsive-design.md](templates/responsive-design.md) | Mobile-first patterns | For all layouts |

---

## 🤖 AI Tool Patterns

| Source | Focus | Best For |
|--------|-------|----------|
| [lovable-design-patterns.md](prompts/lovable-design-patterns.md) | Design system, semantic tokens | React + Vite + Tailwind |
| [v0-design-patterns.md](prompts/v0-design-patterns.md) | Color limits, mobile-first | Next.js + shadcn/ui |

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

## 📖 Full Documentation

See [README.md](README.md) for complete guide with examples and best practices.

---

## 🔗 Navigation

[← Previous: Planning](../2-planning/INDEX.md) | [Next: Development →](../4-development/INDEX.md)

---

**Last Updated**: 2026-04-23  
**Status**: ✅ Complete
