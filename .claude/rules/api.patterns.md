---
trigger: always_on
paths:
  - "src/api/**/*.ts"
  - "src/services/**/*.ts"
---

# API Patterns

> **Last Updated**: 2026-03-05

---

## Service Layer Pattern

```typescript
// ✅ CORRECT
import { ApiService } from '@/services/ApiService'
import type { Product, PaginatedResponse } from '@/types'

export async function fetchProducts(
  page: number = 1,
  limit: number = 10,
  filters?: ProductFilters
): Promise<PaginatedResponse<Product>> {
  try {
    const response = await ApiService.get('/products', {
      params: { page, limit, ...filters },
    })
    return response.data
  } catch (error) {
    throw new Error(`Failed to fetch products: ${error}`)
  }
}
```

---

## PayloadCMS Response Format

```typescript
interface PaginatedResponse<T> {
  docs: T[]
  totalDocs: number
  limit: number
  page: number
  totalPages: number
  hasNextPage: boolean
  hasPrevPage: boolean
}

// Usage
const response = await fetchProducts(1, 10)
const products = response.docs
```

---

## Error Handling

```typescript
// ✅ CORRECT - with toast
const handleDelete = async (id: string) => {
  try {
    await deleteProductService(id)
    toast.success('Product deleted')
    refetch()
  } catch (error) {
    const message = error instanceof Error ? error.message : 'Unknown error'
    toast.error(`Failed: ${message}`)
  }
}

// ❌ WRONG - silent failure
const handleDelete = async (id: string) => {
  await deleteProductService(id)
  refetch()
}
```

---

## Query Parameters

```typescript
const filters = {
  'where[status][equals]': 'active',
  'where[category][like]': 'flowers',
  'sort': '-createdAt',
  'depth': 1,
  'page': 1,
  'limit': 20,
}
```

---

## Common Pitfalls

| ❌ Wrong | ✅ Correct |
|----------|-----------|
| Direct fetch | Use service layer |
| No error handling | Try-catch + toast |
| Missing types | Explicit types |

---

**Related**:
- [api.endpoints.md](./api.endpoints.md)
- [api.filtering.md](./api.filtering.md)
- [component.patterns.md](./component.patterns.md)
