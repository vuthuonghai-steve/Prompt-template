---
trigger: always_on
paths:
  - "src/collections/**/*.ts"
  - "src/globals/**/*.ts"
---

# PayloadCMS Collections

> **Last Updated**: 2026-03-05

---

## Collection Structure

```typescript
import { CollectionConfig } from 'payload'

export const MyCollection: CollectionConfig = {
  slug: 'my-collection',
  labels: {
    singular: 'Ten don so',
    plural: 'Ten so nhieu',
  },
  admin: {
    useAsTitle: 'name',
    defaultColumns: ['name', 'status', 'createdAt'],
    group: 'Ten Nhom',
  },
  access: {
    create: () => true,
    read: () => true,
    update: () => true,
    delete: () => false,
  },
  fields: [/* ... */],
  hooks: {/* ... */},
  timestamps: true,
}
```

---

## Common Fields

```typescript
fields: [
  // Text
  { name: 'name', type: 'text', required: true },

  // Email
  { name: 'email', type: 'email', unique: true },

  // Number
  { name: 'price', type: 'number', min: 0 },

  // Select
  {
    name: 'status',
    type: 'select',
    options: [
      { label: 'Pending', value: 'pending' },
      { label: 'Active', value: 'active' },
    ],
  },

  // Relationship
  { name: 'customer', type: 'relationship', relationTo: 'customers' },
  { name: 'items', type: 'relationship', relationTo: 'products', hasMany: true },

  // Upload
  { name: 'image', type: 'upload', relationTo: 'media' },

  // Group
  {
    name: 'address',
    type: 'group',
    fields: [
      { name: 'street', type: 'text' },
      { name: 'city', type: 'text' },
    ],
  },

  // Array
  {
    name: 'items',
    type: 'array',
    fields: [
      { name: 'product', type: 'relationship', relationTo: 'products' },
      { name: 'quantity', type: 'number' },
    ],
  },
]
```

---

## Domain Organization

```
collections/
├── auth/        # Customer, Users
├── commerce/    # Product, Category
├── orders/      # Order, PaymentSession
├── stores/      # Store, StoreWallets
├── marketing/   # Voucher, Campaign
└── system/      # Media, Configs
```

---

**Related**:
- [payload.local-api.md](./payload.local-api.md)
- [payload.hooks.md](./payload.hooks.md)
- [payload.tag-pattern.md](./payload.tag-pattern.md) — **Tag vs Collection decision**

---

## ⚠️ CRITICAL: Tag Pattern cho Metadata

**TRƯỚC KHI tạo collection mới → Kiểm tra [payload.tag-pattern.md](./payload.tag-pattern.md)**

### Decision Matrix

| Metadata | ✅ Action | ❌ Không |
|----------|---------|---------|
| Style/Kiểu cách | Tag + `type: 'style'` | Tạo `style-types` |
| Color/Tone màu | Tag + `type: 'color'` | Tạo `color-tones` |
| Flower/Loại hoa | Tag + `type: 'flower'` | Tạo `flower-types` |
| Event/Dịp | Tag + `type: 'event'` | Tạo collection mới |
