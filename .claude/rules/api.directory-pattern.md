---
trigger: always_on
paths:
  - "src/app/api/v1/**/*.ts"
  - "src/services/**/*.ts"
description: API Directory Pattern cho App Router - Module-first organization
priority: 60
---

# API Directory Pattern

> **App Router API Structure - Module-First Organization**
> **Last Updated**: 2026-03-18

---

## Overview

Pattern này tổ chức API theo module-first: gom support files (services, schemas, types, constants, utils) lên đầu module thay vì để chúng theo từng endpoint. Giúp AI agent dễ tìm kiếm và developer dễ maintain.

---

## Structure

```
src/app/api/v1/
├── products/                      # Module root (collection)
│   ├── route.ts                  # GET/POST /api/v1/products (optional)
│   ├── services/                 # Application logic
│   │   ├── list-products.service.ts
│   │   ├── create-product.service.ts
│   │   └── shared/               # Dùng chung trong module
│   │       └── product-helper.service.ts
│   ├── schemas/                  # Zod validation
│   │   ├── list-products.schema.ts
│   │   ├── create-product.schema.ts
│   │   └── product-id.schema.ts
│   ├── types/                    # DTO, response types
│   │   ├── list-products.dto.ts
│   │   └── create-product.dto.ts
│   ├── constants/                # Enum, defaults, error codes
│   │   └── product.constants.ts
│   ├── utils/                    # Pure helpers
│   │   ├── format-product.ts
│   │   └── shared/
│   │       └── price.utils.ts
│   ├── [slug]/                   # Dynamic route
│   │   └── route.ts              # GET/PUT/DELETE /api/v1/products/:slug
│   └── price-movement/            # Sub-module
│       ├── route.ts
│       └── bulk-update/
│           └── route.ts
├── orders/
│   ├── route.ts
│   ├── services/
│   │   ├── create-order.service.ts
│   │   └── cancel-order.service.ts
│   ├── schemas/
│   │   └── create-order.schema.ts
│   ├── types/
│   │   └── create-order.dto.ts
│   └── [id]/
│       ├── route.ts
│       └── cancel/
│           └── route.ts
└── auth/
    ├── route.ts
    ├── login/
    │   ├── route.ts
    │   ├── schemas/
    │   └── services/
    └── register/
        ├── route.ts
        ├── schemas/
        └── services/
```

---

## Mental Model

### Layer Responsibilities

| Layer | Responsibility | AI Search Pattern |
|-------|----------------|-------------------|
| `route.ts` | HTTP transport: parse, auth, call service, map response | `rg "export.*GET\|POST" src/app/api/v1/products` |
| `services/` | Application logic: orchestration, transaction, domain calls | `rg --files src/app/api/v1/products/services` |
| `schemas/` | Zod validation for body/query/params | `rg --files src/app/api/v1/products/schemas` |
| `types/` | DTO, response shape, context types | `rg --files src/app/api/v1/products/types` |
| `constants/` | Enum, default values, field maps, error codes | `rg --files src/app/api/v1/products/constants` |
| `utils/` | Pure helper functions, no DB calls | `rg --files src/app/api/v1/products/utils` |

### Quy tắc quan trọng

1. **Route = Mỏng**: Chỉ là HTTP transport, không chứa business logic
2. **Services = Use-case**: Application logic của endpoint
3. **Domain = Tách**: Logic dùng chung toàn hệ thống đặt ở `src/services/**`
4. **Support files = Module root**: Gom lên đầu module, không theo từng endpoint

---

## Naming Conventions

### File Naming

| Type | Pattern | Example |
|------|---------|---------|
| Service | `<action>-<entity>.service.ts` | `create-product.service.ts` |
| Schema | `<action>-<entity>.schema.ts` | `create-product.schema.ts` |
| Type | `<action>-<entity>.dto.ts` | `create-product.dto.ts` |
| Constant | `<entity>.constants.ts` | `product.constants.ts` |
| Utils | `<action>-<entity>.ts` | `format-product.ts` |

### Vocabulary (BẮT BUỘC)

```
✅ Dùng: services, schemas, types, constants, utils
❌ Không dùng: hooks, model, validation, validators, _lib, shared (trừ shared/ folder)
```

### Folder chia

Chỉ tạo folder con trong support khi đủ lớn (≥3 files):

```
# Khi module còn nhỏ
products/services/create-product.service.ts

# Khi module đủ lớn (≥3 files)
products/services/create/
  ├── create-product.service.ts
  ├── validate-product.service.ts
  └── notify-product-created.service.ts
```

---

## Route File Template

```typescript
// src/app/api/v1/products/create/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { createProductSchema } from '../schemas/create-product.schema'
import { CreateProductService } from '../services/create-product.service'
import { getAuthUser } from '@/lib/auth'

export async function POST(request: NextRequest) {
  try {
    // 1. Parse & Validate
    const body = await request.json()
    const validated = createProductSchema.parse(body)

    // 2. Auth
    const user = await getAuthUser(request)
    if (!user) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    // 3. Execute Service
    const result = await CreateProductService.execute({
      ...validated,
      userId: user.id,
    })

    // 4. Response
    return NextResponse.json(result, { status: 201 })
  } catch (error) {
    if (error.name === 'ZodError') {
      return NextResponse.json({ error: 'Validation failed', details: error.errors }, { status: 400 })
    }
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
  }
}
```

---

## Service File Template

```typescript
// src/app/api/v1/products/services/create-product.service.ts
import { ProductRepository } from '@/services/product-repository'
import { InventoryService } from '@/services/inventory-service'
import type { CreateProductDTO } from '../types/create-product.dto'

export class CreateProductService {
  static async execute(data: CreateProductDTO & { userId: string }) {
    // Validate inventory
    const inventoryAvailable = await InventoryService.check(data.productItems)
    if (!inventoryAvailable) {
      throw new Error('Inventory not available')
    }

    // Create product
    const product = await ProductRepository.create({
      ...data,
      createdBy: data.userId,
    })

    // Sync inventory
    await InventoryService.reserve(data.productItems, product.id)

    return product
  }
}
```

---

## Schema File Template

```typescript
// src/app/api/v1/products/schemas/create-product.schema.ts
import { z } from 'zod'

export const createProductSchema = z.object({
  name: z.string().min(1).max(200),
  slug: z.string().min(1).max(200),
  description: z.string().optional(),
  categoryId: z.string(),
  productItems: z.array(z.object({
    sku: z.string(),
    price: z.number().positive(),
    quantity: z.number().int().min(0),
  })),
  images: z.array(z.string().url()).optional(),
  isActive: z.boolean().default(true),
})

export type CreateProductInput = z.infer<typeof createProductSchema>
```

---

## AI Agent Search Patterns

### Tìm tất cả service của module
```bash
ls src/app/api/v1/products/services
```

### Tìm tất cả schema liên quan endpoint
```bash
rg --files src/app/api/v1/products/schemas
```

### Tìm route và service tương ứng
```bash
# Tìm route
rg "export.*function.*POST" src/app/api/v1/products/create/route.ts
# Tìm service được gọi
rg "CreateProductService" src/app/api/v1/products/create/route.ts
```

### Tìm tất cả endpoint của một module
```bash
rg --files src/app/api/v1/products | rg "route.ts"
```

### Tìm domain service (dùng chung toàn hệ thống)
```bash
ls src/services/ | rg "product"
```

---

## Boundary Rules

### Trong route.ts
- Parse request body/query
- Validate input (dùng schema)
- Auth check
- Gọi service
- Map response

### Trong services/ (module)
- Application logic cụ thể của endpoint
- Orchestration nhiều domain services
- Transaction flow

### Trong src/services/ (global)
- Domain logic dùng lại toàn hệ thống
- Không gắn với HTTP context
- Repository pattern, domain services

### Trong schemas/
- Chỉ Zod validation
- Không có business logic

### Trong types/
- DTO interfaces
- Response types
- Payload shapes

### Trong constants/
- Enum definitions
- Default values
- Error code maps (local to module)

### Trong utils/
- Pure functions
- Format helpers
- Không query DB, không side effects lớn

---

## Anti-Patterns

```
❌ Route chứa business logic
❌ Dồn tất cả vào một file route.ts
❌ Model, validation, validators, _lib lẫn lộn
❌ Tạo support folder cho endpoint nhỏ (chỉ 1-2 files)
❌ Cả types/ và interfaces/ cùng lúc
❌ Dùng hooks/ trong api vì trùng với PayloadCMS hooks
```

---

## Migration Path

Khi refactor endpoint hiện tại:

1. Tạo folder module root (nếu chưa có)
2. Di chuyển logic từ route.ts → services/
3. Di chuyển validation → schemas/
4. Di chuyển types → types/
5. Gom constants vào constants/
6. Route.ts chỉ giữ HTTP transport

---

**Related**:
- [api.patterns.md](./api.patterns.md) - Frontend service layer
- [api.endpoints.md](./api.endpoints.md) - Endpoint configuration
- [core.naming-conventions.md](./core.naming-conventions.md) - File naming
