# Naming Conventions

> **Kết hợp: Nested (Level 1-2) + Flat (Level 3+)**
> **Last Updated**: 2026-03-11

---

## Folder Structure

### Level 1-2: Nested Folders

```
src/
├── services/           # Level 1 - folder
│   ├── order/         # Level 2 - folder
│   └── user/
├── hooks/             # Level 1 - folder
│   ├── use-user/     # Level 2 - folder
│   └── use-cart/
├── utils/             # Level 1 - folder
│   ├── format/       # Level 2 - folder
│   └── validation/
└── types/             # Level 1 - folder
    ├── dto/          # Level 2 - folder
    └── entity/
```

### Level 3+: Flat (No Subfolders)

```
src/
├── services/
│   ├── order/
│   │   ├── service.order-code.ts    # ✅ Flat
│   │   └── service.payment.ts       # ✅ Flat
│   └── user/
│       └── service.user.ts          # ✅ Flat
├── hooks/
│   ├── use-user/
│   │   └── hook.use-user.ts         # ✅ Flat
│   └── use-cart/
│       └── hook.use-cart.ts         # ✅ Flat
└── types/
    └── dto/
        └── type.user-dto.ts         # ✅ Flat
```

---

## File Naming

### Format: `<type>.<name>.ts`

| Type | Example |
|------|---------|
| Service | `service.order-code.ts` |
| Hook | `hook.use-user-data.ts` |
| Util | `util.format-currency.ts` |
| Type | `type.user-dto.ts` |

---

## Import Examples

```typescript
// ✅ CORRECT - Import từ folder chứa file flat
import { OrderCodeService } from '@/services/order/service.order-code'
import { useUserData } from '@/hooks/use-user/hook.use-user-data'

// ❌ WRONG - Import folder không có file flat
import { OrderCodeService } from '@/services/order/another-folder'
```

---

## Rules

1. **Level 1-2**: Tạo folders để nhóm related files
2. **Level 3+**: KHÔNG tạo subfolders, chỉ flat files
3. **Prefix**: Luôn có `<type>.` ở đầu tên file

---

## Anti-Patterns

```
❌ services/order/code/service.order.ts     # ❌ Quá sâu
❌ hooks/useUserData.ts                     # ❌ Thiếu prefix
❌ services/order/another-folder/           # ❌ Folder không có flat files
```

---

## Migration

```bash
# Từ: services/order-code.service.ts
# Sang: services/order/service.order-code.ts
```

---

**Related**:
- [core.coding-checklist.md](./core.coding-checklist.md)
