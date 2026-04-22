---
trigger: always_on
paths:
  - "src/api/**/*.ts"
---

# API Endpoints

> **Last Updated**: 2026-03-05

---

## Centralized Endpoints

Tat ca endpoints PHAI duoc dinh nghia tap trung!

**Vi tri**: `src/api/config/endpoint.ts`

```typescript
export const ENDPOINTS = {
  AUTH: {
    LOGIN: '/api/v1/auth/login',
    REGISTER: '/api/v1/auth/register',
  },
  STORES: {
    DASHBOARD: '/api/v1/stores/store-dashboard',
    ORDERS: '/api/v1/stores/orders',
  },
} as const
```

---

## Usage

```typescript
// ✅ CORRECT
import { ENDPOINTS } from '@/api/config/endpoint'

export const fetchDashboard = (params) => {
  return ApiService.get(ENDPOINTS.STORES.DASHBOARD, { params })
}

// ❌ WRONG
export const fetchDashboard = (params) => {
  return ApiService.get('/api/v1/stores/store-dashboard', { params })
}
```

---

## Rules

1. **KHONG** hardcode URL trong service files
2. **DUNG** ENDPOINTS object
3. **Neu** endpoint co tham so (vd: `/api/v1/users/:id`), dinh nghia nhu function

```typescript
// Function endpoint
export const getUserById = (id: string) => ENDPOINTS.USERS.DETAIL.replace(':id', id)
```

---

**Related**: [api.patterns.md](./api.patterns.md)
