# Project Structure Template

> Extracted from: Cursor, VSCode Agent, Windsurf, Claude Code
> Phase: Development
> Last Updated: 2026-04-22

---

## 🎯 Core Principles

### 1. Codebase Organization
- **Modular structure**: Tách biệt concerns (components, services, utils)
- **Flat hierarchy**: Tránh nested quá sâu (max 3-4 levels)
- **Domain-driven**: Nhóm theo business domain, không theo technical layer

### 2. File Naming Conventions
```
components/
├── Button/
│   ├── Button.tsx
│   ├── Button.test.tsx
│   ├── Button.styles.ts
│   └── index.ts          # Barrel export

services/
├── api/
│   ├── auth.service.ts
│   ├── user.service.ts
│   └── index.ts

utils/
├── format.util.ts
├── validation.util.ts
└── index.ts
```

---

## 📁 Standard Structure Patterns

### Frontend (React/Next.js)
```
src/
├── app/                  # Next.js App Router
│   ├── (auth)/          # Route groups
│   ├── api/             # API routes
│   └── layout.tsx
├── components/
│   ├── ui/              # Design system
│   ├── features/        # Feature-specific
│   └── layouts/
├── lib/
│   ├── hooks/
│   ├── utils/
│   └── constants/
├── services/            # API calls
├── store/               # State management
└── types/               # TypeScript definitions
```

### Backend (Node.js/Express)
```
src/
├── api/
│   ├── routes/
│   ├── controllers/
│   └── middlewares/
├── services/            # Business logic
├── models/              # Data models
├── utils/
├── config/
└── types/
```

### Full-stack Monorepo
```
apps/
├── web/                 # Frontend
├── api/                 # Backend
└── admin/               # Admin panel

packages/
├── ui/                  # Shared components
├── config/              # Shared configs
└── types/               # Shared types
```

---

## 🔧 Configuration Files Location

| File | Location | Purpose |
|------|----------|---------|
| `package.json` | Root | Dependencies |
| `tsconfig.json` | Root | TypeScript config |
| `.env.example` | Root | Environment template |
| `.gitignore` | Root | Git ignore rules |
| `README.md` | Root | Project documentation |

---

## 📋 Best Practices

### DO ✅
- Nhóm files theo feature/domain
- Dùng barrel exports (`index.ts`)
- Tách config ra khỏi code
- Đặt tests gần source code

### DON'T ❌
- Nested folders quá 4 levels
- Mix business logic với UI
- Hardcode configs trong code
- Đặt tests riêng folder `__tests__`

---

## 🎨 Naming Patterns

| Type | Pattern | Example |
|------|---------|---------|
| Component | PascalCase | `UserProfile.tsx` |
| Service | camelCase + .service | `auth.service.ts` |
| Util | camelCase + .util | `format.util.ts` |
| Hook | use + PascalCase | `useUserData.ts` |
| Type | PascalCase + Type/Interface | `UserDTO.ts` |
| Constant | UPPER_SNAKE_CASE | `API_ENDPOINTS.ts` |

---

## 🔍 Pattern Sources

**Cursor Agent**:
- Semantic search for codebase exploration
- File organization by meaning, not just structure

**VSCode Agent**:
- Modular structure with clear separation
- Barrel pattern for clean imports

**Windsurf**:
- Domain-driven organization
- Flat hierarchy preference

**Claude Code**:
- Feature-first structure
- Co-location of related files

---

## 📝 Implementation Checklist

- [ ] Tạo folder structure theo domain
- [ ] Setup barrel exports
- [ ] Tách config files
- [ ] Đặt tên files theo convention
- [ ] Tạo README.md cho mỗi major folder
- [ ] Setup path aliases (`@/components`, `@/lib`)

---

**Related Templates**:
- [API Design](./api-design.md)
- [Coding Standards](./coding-standards.md)
