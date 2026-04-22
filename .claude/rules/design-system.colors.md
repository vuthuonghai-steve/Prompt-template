---
trigger: always_on
paths:
  - "src/components/**/*.tsx"
  - "src/screens/**/*.tsx"
---

# Design System Colors

> **Last Updated**: 2026-03-05

---

## Color Palette

### Primary (Pink)
CTAs, links, active states.

| Token | Hex |
|-------|-----|
| primary-50 | #FFF5F8 |
| primary-100 | #FFE8EF |
| primary-200 | #FFD1DF |
| primary-500 | #FF8CAF |
| primary-700 | #CC688B |

### Secondary (Orange)
Accents, secondary CTAs.

| Token | Hex |
|-------|-----|
| secondary-500 | #FF9D19 |

### Accents
| Name | Hex |
|------|-----|
| lavender | #9D7FE0 |
| peach | #FF7D32 |
| gold | #FFD232 |

### Semantic
| Name | Hex |
|------|-----|
| success | #10B981 |
| warning | #F59E0B |
| error | #EF4444 |
| info | #F06292 |

---

## Primary Color Rule

**Màu primary (Pink) PHẢI được tôn trọng!**

### BẮT BUỘC

```typescript
// ✅ CORRECT
<Button variant="default">Primary Action</Button>
<a className="text-primary hover:text-primary-700">Link</a>
<div className="border-primary-500 bg-primary-50">Selected</div>
<input className="focus:ring-primary-500" />

// ❌ WRONG
<Button className="bg-blue-500">Submit</Button>
<a className="text-blue-600">Link</a>
```

### Màu KHÔNG được thay thế primary

| ❌ Avoid | ✅ Use |
|---------|--------|
| blue-* | primary-* |
| indigo-* | primary-* |
| purple-* (CTA) | primary-* |
| rose-* | primary-* |

---

**Related**:
- [design-system.components.md](./design-system.components.md)
