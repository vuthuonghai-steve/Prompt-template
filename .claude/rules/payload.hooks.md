---
trigger: always_on
paths:
  - "src/collections/**/*.ts"
  - "src/payload-hooks/**/*.ts"
---

# PayloadCMS Hooks

> **Last Updated**: 2026-03-05

---

## Hook Types

| Hook | Time | Use case |
|------|------|-----------|
| beforeValidate | Pre-validation | Normalize data |
| beforeChange | Pre create/update | Enrich data |
| afterChange | Post create/update | Create related records |
| beforeDelete | Pre-delete | Check constraints |
| afterDelete | Post-delete | Cleanup |
| beforeRead | Pre-read | Filter sensitive data |
| afterRead | Post-read | Transform response |

---

## Hook Structure

```typescript
// collections/auth/config/hooks/createWallet.ts
import { CollectionAfterChangeHook } from 'payload'

export const createCustomerWalletHook: CollectionAfterChangeHook = async ({
  doc,
  operation,
  req,
}) => {
  // Only on CREATE
  if (operation !== 'create') return doc

  await req.payload.create({
    collection: 'customer-wallets',
    data: {
      customer: doc.id,
      balance: 0,
    },
    overrideAccess: true,
  })

  return doc
}
```

---

## Register Hook

```typescript
// collections/auth/Customer.ts
import { createCustomerWalletHook } from './config/hooks'

export const Customer: CollectionConfig = {
  slug: 'customers',
  hooks: {
    afterChange: [createCustomerWalletHook],
  },
}
```

---

## Best Practices

| Rule | Reason |
|------|--------|
| Tach hooks ra file riêng | De test, maintain |
| Dung depth 1-2 | Tranh over-fetch |
| Su dung overrideAccess trong system actions | AI/system can bypass |

---

**Related**:
- [payload.collections.md](./payload.collections.md)
- [payload.local-api.md](./payload.local-api.md)
