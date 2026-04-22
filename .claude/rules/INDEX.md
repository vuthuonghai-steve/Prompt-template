---
trigger: always_on
priority: 100
description: Master index for all rules - START HERE
---

# SiinStore Rules Index

> **Priority**: START WITH THIS FILE
> **Last Updated**: 2026-03-05

---

## Quick Access

| Nhu cau | Rule File |
|---------|-----------|
| Bat dau task moi | [workflow.development.md](./workflow.development.md) |
| Truoc khi viet code | [core.coding-checklist.md](./core.coding-checklist.md) |
| Tim hieu project | [core.project-overview.md](./core.project-overview.md) |
| Quy uoc dat ten | [core.naming-conventions.md](./core.naming-conventions.md) |
| API service | [api.patterns.md](./api.patterns.md) |
| Component React | [component.patterns.md](./component.patterns.md) |
| State management | [component.state.md](./component.state.md) |
| Design system | [design-system.colors.md](./design-system.colors.md) |
| PayloadCMS | [payload.collections.md](./payload.collections.md) |

---

## Nhom Rules

### core
Project fundamentals - doc duoc load khi khoi dau.

| File | Mo ta |
|------|-------|
| [core.project-overview.md](./core.project-overview.md) | Project structure, tech stack |
| [core.naming-conventions.md](./core.naming-conventions.md) | Dat ten file, bien, ham |
| [core.coding-checklist.md](./core.coding-checklist.md) | Checklist truoc khi viet code |

### api
API service layer va data fetching.

| File | Mo ta |
|------|-------|
| [api.patterns.md](./api.patterns.md) | Service layer, response format, error handling |
| [api.endpoints.md](./api.endpoints.md) | Centralized endpoints config |
| [api.filtering.md](./api.filtering.md) | Debounced search pattern |

### component
React component development.

| File | Mo ta |
|------|-------|
| [component.patterns.md](./component.patterns.md) | Component structure, composition |
| [component.state.md](./component.state.md) | Redux, Context, local state |

### design-system
Design system va styling.

| File | Mo ta |
|------|-------|
| [design-system.colors.md](./design-system.colors.md) | Color palette, Primary rule |
| [design-system.components.md](./design-system.components.md) | Component usage, forbidden libraries |

### payload
PayloadCMS specific rules.

| File | Mo ta |
|------|-------|
| [payload.collections.md](./payload.collections.md) | Collection definitions |
| [payload.local-api.md](./payload.local-api.md) | Local API usage |
| [payload.hooks.md](./payload.hooks.md) | Lifecycle hooks |
| [payload.tag-pattern.md](./payload.tag-pattern.md) | **Tag = Single Source cho Metadata** |

### workflow
Development process va AI behavior.

| File | Mo ta |
|------|-------|
| [workflow.development.md](./workflow.development.md) | 3-Step development process |
| [workflow.ai-checklist.md](./workflow.ai-checklist.md) | Pre-action checklist |
| [workflow.reflection.md](./workflow.reflection.md) | Self-review protocol |

---

## Su dung

1. **Doc INDEX.md nay truoc** - No se huong dan toi file can thiet
2. **Su dung frontmatter** - Cac file co `trigger: always_on` se tu dong load
3. **Path-specific rules** - Chi ap dung khi lam viec voi file khớp pattern

```yaml
---
paths:
  - "src/screens/Admin/**/*.tsx"
---
# Chi ap dung khi lam viec voi Admin screens
```

---

**Ghi chu**: Cac file cu trong `.claude/rules/` da duoc refactor vao cau truc nay.
