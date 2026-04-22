# Coding Checklist

> **MUST READ BEFORE WRITING ANY CODE**
> **Last Updated**: 2026-03-11

---

## Pre-Coding

### Step 1: Understand Requirements
- [ ] Doc yeu cau cua Steve
- [ ] Xac dinh files can thay doi
- [ ] Xac dinh pattern hien tai

### Step 2: Check Conventions

#### Folder Structure: Nested (Level 1-2) + Flat (Level 3+)

```
services/           # Level 1 - folder
├── order/         # Level 2 - folder
│   └── service.order-code.ts    # ✅ Level 3 - FLAT
└── user/
    └── service.user.ts          # ✅ Level 3 - FLAT
```

#### Types Location
```bash
# ✅ CORRECT - Flat từ Level 3
# File: src/types/dto/type.user-dto.ts
export interface UserDTO { ... }

# Import
import type { UserDTO } from '@/types/dto/type.user-dto'
```

#### Endpoints
```bash
# ❌ WRONG
ApiService.get('/api/v1/users')

# ✅ CORRECT
import { ENDPOINTS } from '@/api/config/endpoint'
ApiService.get(ENDPOINTS.USERS.LIST)
```

#### Import Order
```typescript
// 1. React & Next.js
// 2. Third-party
// 3. Internal components
// 4. Services, Hooks, Utils, Types
// 5. Constants
```

---

## Design System Check

### Primary Color (BẮT BUỘC)
```typescript
// ✅ CORRECT
<Button variant="default">Submit</Button>
<a className="text-primary">Link</a>

// ❌ WRONG
<Button className="bg-blue-500">Submit</Button>
```

### Forbidden Libraries
```typescript
// ❌ NEVER
import { Button } from 'antd'
import { Modal } from '@mui/material'

// ✅ ALWAYS
import { Button } from '@/components/ui/button'
```

---

## Validation Workflow

### Before Writing
1. Doc INDEX.md
2. Review relevant rules
3. Check existing patterns
4. Confirm with Steve if unsure

### After Writing
- [ ] Đúng level: folders (1-2), flat (3+)?
- [ ] File naming: `service.*.ts`, `hook.*.ts`, `util.*.ts`, `type.*.ts`?
- [ ] Import đúng cấu trúc folder?
- [ ] Endpoints from config?
- [ ] Primary color used?
- [ ] No forbidden libraries?
- [ ] Import order correct?

---

## Quick Reference

| Question | Action |
|----------|--------|
| Tạo folder mới? | Chỉ Level 1-2 |
| File ở đâu? | Level 3+ (flat, không subfolder) |
| Đặt tên file? | `service.<name>.ts`, `hook.<name>.ts`, etc. |
| Hardcode URL? | Add to ENDPOINTS config |
| Dung blue/indigo cho CTA? | Change to primary |
| Import antd/mui? | Use design system |

---

**Related**:
- [core.naming-conventions.md](./core.naming-conventions.md)
- [core.project-overview.md](./core.project-overview.md)
