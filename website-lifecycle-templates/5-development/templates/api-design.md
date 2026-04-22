# API Design Template

> Extracted from: Cursor, VSCode Agent, Replit, Windsurf
> Phase: Development
> Last Updated: 2026-04-22

---

## 🎯 Core Principles

### 1. RESTful Design
- **Resource-based URLs**: `/users`, `/products`, `/orders`
- **HTTP methods**: GET, POST, PUT, PATCH, DELETE
- **Status codes**: 200, 201, 400, 401, 404, 500

### 2. Consistent Response Format
```typescript
// Success response
{
  "success": true,
  "data": { ... },
  "meta": {
    "page": 1,
    "limit": 20,
    "total": 100
  }
}

// Error response
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input",
    "details": [...]
  }
}
```

---

## 📋 URL Structure Patterns

### Resource Naming
```
✅ GOOD
GET    /api/v1/users
GET    /api/v1/users/:id
POST   /api/v1/users
PUT    /api/v1/users/:id
DELETE /api/v1/users/:id

❌ BAD
GET    /api/v1/getUsers
POST   /api/v1/createUser
GET    /api/v1/user-list
```

### Nested Resources
```
✅ GOOD
GET /api/v1/users/:userId/orders
GET /api/v1/users/:userId/orders/:orderId

❌ BAD (quá sâu)
GET /api/v1/users/:userId/orders/:orderId/items/:itemId/reviews
```

### Query Parameters
```typescript
// Filtering
GET /api/v1/products?category=electronics&status=active

// Sorting
GET /api/v1/products?sort=-createdAt,name

// Pagination
GET /api/v1/products?page=1&limit=20

// Search
GET /api/v1/products?q=laptop
```

---

## 🔧 Implementation Patterns

### Service Layer Pattern
```typescript
// services/user.service.ts
export class UserService {
  async getUsers(filters: UserFilters): Promise<User[]> {
    // Business logic here
  }
  
  async createUser(data: CreateUserDTO): Promise<User> {
    // Validation + creation
  }
}

// routes/user.routes.ts
router.get('/users', async (req, res) => {
  const users = await userService.getUsers(req.query)
  res.json({ success: true, data: users })
})
```

### Error Handling
```typescript
// middlewares/error.middleware.ts
export const errorHandler = (err, req, res, next) => {
  const statusCode = err.statusCode || 500
  
  res.status(statusCode).json({
    success: false,
    error: {
      code: err.code || 'INTERNAL_ERROR',
      message: err.message,
      ...(process.env.NODE_ENV === 'development' && {
        stack: err.stack
      })
    }
  })
}
```

### Validation Middleware
```typescript
// middlewares/validate.middleware.ts
import { z } from 'zod'

export const validate = (schema: z.ZodSchema) => {
  return async (req, res, next) => {
    try {
      req.body = await schema.parseAsync(req.body)
      next()
    } catch (error) {
      res.status(400).json({
        success: false,
        error: {
          code: 'VALIDATION_ERROR',
          message: 'Invalid input',
          details: error.errors
        }
      })
    }
  }
}
```

---

## 🔐 Security Best Practices

### Authentication
```typescript
// middlewares/auth.middleware.ts
export const authenticate = async (req, res, next) => {
  const token = req.headers.authorization?.split(' ')[1]
  
  if (!token) {
    return res.status(401).json({
      success: false,
      error: { code: 'UNAUTHORIZED', message: 'No token provided' }
    })
  }
  
  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET)
    req.user = decoded
    next()
  } catch (error) {
    res.status(401).json({
      success: false,
      error: { code: 'INVALID_TOKEN', message: 'Invalid token' }
    })
  }
}
```

### Rate Limiting
```typescript
import rateLimit from 'express-rate-limit'

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
  message: {
    success: false,
    error: {
      code: 'RATE_LIMIT_EXCEEDED',
      message: 'Too many requests'
    }
  }
})

app.use('/api/', limiter)
```

---

## 📊 Status Codes Guide

| Code | Meaning | Use Case |
|------|---------|----------|
| 200 | OK | Successful GET, PUT, PATCH |
| 201 | Created | Successful POST |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Validation error |
| 401 | Unauthorized | Missing/invalid auth |
| 403 | Forbidden | No permission |
| 404 | Not Found | Resource not found |
| 409 | Conflict | Duplicate resource |
| 500 | Internal Error | Server error |

---

## 🎨 Versioning Strategy

### URL Versioning (Recommended)
```
/api/v1/users
/api/v2/users
```

### Header Versioning
```
GET /api/users
Accept: application/vnd.api+json; version=1
```

---

## 📝 Documentation Pattern

### OpenAPI/Swagger
```yaml
openapi: 3.0.0
info:
  title: User API
  version: 1.0.0

paths:
  /users:
    get:
      summary: Get all users
      parameters:
        - name: page
          in: query
          schema:
            type: integer
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserListResponse'
```

---

## 🔍 Pattern Sources

**Cursor Agent**:
- Semantic search for API patterns
- Consistent error handling

**VSCode Agent**:
- Service layer separation
- Middleware patterns

**Replit**:
- RESTful conventions
- Response format standardization

**Windsurf**:
- Security best practices
- Rate limiting patterns

---

## 📋 Implementation Checklist

- [ ] Define API versioning strategy
- [ ] Setup standard response format
- [ ] Implement error handling middleware
- [ ] Add validation middleware
- [ ] Setup authentication/authorization
- [ ] Add rate limiting
- [ ] Document endpoints (Swagger/OpenAPI)
- [ ] Write API tests

---

**Related Templates**:
- [Project Structure](./project-structure.md)
- [Database Schema](./database-schema.md)
- [Coding Standards](./coding-standards.md)
