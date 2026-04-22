---
trigger: always_on
paths:
  - "src/app/api/**/*.ts"
  - "src/services/**/*.ts"
  - "src/crons/**/*.ts"
---

# PayloadCMS Local API

> **Last Updated**: 2026-03-05

---

## Init Payload

```typescript
import { getPayload } from 'payload'
import config from '@/payload.config'

const payload = await getPayload({ config })
```

---

## Basic Operations

### Find

```typescript
const products = await payload.find({
  collection: 'products',
  where: {
    status: { equals: 'published' },
    price: { greater_than: 100000 },
  },
  limit: 10,
  sort: '-createdAt',
  depth: 1,
})
```

### FindByID

```typescript
const order = await payload.findByID({
  collection: 'orders',
  id: 'order_id_123',
  depth: 2,
})
```

### Create

```typescript
const newOrder = await payload.create({
  collection: 'orders',
  data: {
    orderCode: 'HD20260123001',
    status: 'pending',
    totalAmount: 500000,
  },
  overrideAccess: true,
})
```

### Update

```typescript
await payload.update({
  collection: 'orders',
  id: 'order_id_123',
  data: { status: 'completed' },
})
```

### Delete

```typescript
await payload.delete({
  collection: 'orders',
  id: 'order_id_123',
})
```

---

## Query Operators

| Operator | Example |
|----------|---------|
| equals | `{ status: { equals: 'active' } }` |
| not_equals | `{ status: { not_equals: 'deleted' } }` |
| greater_than | `{ price: { greater_than: 100000 } }` |
| less_than | `{ quantity: { less_than: 10 } }` |
| in | `{ status: { in: ['pending', 'processing'] } }` |
| contains | `{ name: { contains: 'hoa' } }` |
| exists | `{ deletedAt: { exists: false } }` |

---

## Logical Operators

```typescript
// AND (default)
where: {
  status: { equals: 'active' },
  price: { greater_than: 100000 },
}

// OR
where: {
  or: [
    { status: { equals: 'pending' } },
    { status: { equals: 'processing' } },
  ],
}
```

---

## overrideAccess Usage

| Scenario | overrideAccess |
|----------|---------------|
| API route (user auth) | `false` |
| Background job / cron | `true` |
| Internal hook | `true` |
| Migrate / seed | `true` |

---

## Best Practices

| Rule | Reason |
|------|--------|
| Dung Local API | Nhanh hon, type-safe |
| Doc schema truoc | Hieu cau truc data |
| Dung depth 1-2 | Tranh query nang |
| KHONG sua payload-types.ts | De Payload tu generate |

---

**Related**:
- [payload.collections.md](./payload.collections.md)
- [payload.hooks.md](./payload.hooks.md)
