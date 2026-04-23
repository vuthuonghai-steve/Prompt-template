# Pattern: Tool Use Sequencing

## Nguồn
- Claude Code
- Cursor
- Windsurf

## Mô tả
Strategic ordering of tool calls to maximize efficiency and minimize context pollution. Read → Analyze → Plan → Execute pattern.

## Khi nào dùng
- Multi-step tasks
- Codebase exploration
- Refactoring workflows
- Debugging sessions
- Feature implementation

## Cách áp dụng

### 1. Tool Sequencing Hierarchy

```
1. DISCOVER (Read-only)
   ├── Glob - Find files by pattern
   ├── Grep - Search content
   └── Read - Read specific files

2. ANALYZE (No side effects)
   ├── Parse structure
   ├── Identify patterns
   └── Plan changes

3. PLAN (Document intent)
   ├── Write plan document
   ├── List affected files
   └── Define test scenarios

4. EXECUTE (Make changes)
   ├── Edit - Modify existing
   ├── Write - Create new
   └── Bash - Run commands

5. VERIFY (Validate)
   ├── Run tests
   ├── Check syntax
   └── Verify functionality
```

### 2. Anti-Pattern: Premature Execution

```typescript
// ❌ WRONG: Edit before understanding
Edit('src/components/Button.tsx', ...)  // Don't know context!

// ✅ CORRECT: Discover → Analyze → Execute
Glob('**/*Button*')                     // Find related files
Read('src/components/Button.tsx')       // Understand current code
Read('src/components/ui/button.tsx')    // Check design system
Grep('import.*Button', 'src/')          // Find usage
// Now we understand context
Edit('src/components/Button.tsx', ...)  // Safe to edit
```

### 3. Efficient Discovery Pattern

```typescript
// Pattern: Broad → Narrow

// Step 1: Broad search (find candidates)
Glob('src/**/*.tsx')  // Get all React files

// Step 2: Narrow search (find specific)
Grep('useCart', 'src/', { output_mode: 'files_with_matches' })

// Step 3: Read specific files
Read('src/hooks/use-cart/hook.use-cart.ts')
Read('src/contexts/CartContext.tsx')

// Step 4: Understand relationships
Grep('CartProvider', 'src/', { output_mode: 'content' })
```

### 4. Parallel vs Sequential

```typescript
// ✅ PARALLEL: Independent reads
Promise.all([
  Read('src/services/order/service.order.ts'),
  Read('src/services/payment/service.payment.ts'),
  Read('src/types/dto/type.order-dto.ts')
])

// ✅ SEQUENTIAL: Dependent operations
Read('src/config/endpoints.ts')          // Need to see structure
// Analyze endpoints structure
Edit('src/config/endpoints.ts', ...)     // Add new endpoint
Read('src/services/product/service.product.ts')  // Check usage
Edit('src/services/product/service.product.ts', ...)  // Update service
```

## Ví dụ thực tế

### E-commerce: Add Wishlist Feature

```typescript
// PHASE 1: DISCOVER
// Goal: Understand current architecture

// Step 1: Find related files
Glob('src/**/*cart*')  // See how cart is implemented
Glob('src/**/*user*')  // See user data structure

// Step 2: Read key files
Read('src/contexts/CartContext.tsx')     // Cart pattern
Read('src/hooks/use-cart/hook.use-cart.ts')  // Cart hook
Read('src/types/dto/type.user-dto.ts')   // User type

// Step 3: Search for patterns
Grep('localStorage', 'src/', { output_mode: 'files_with_matches' })
Grep('useReducer', 'src/', { output_mode: 'files_with_matches' })

// PHASE 2: ANALYZE
// Now we know:
// - Cart uses Context + useReducer
// - Cart persists to localStorage
// - User type is in types/dto/
// - Pattern: Context → Hook → Component

// PHASE 3: PLAN
Write('docs/plans/wishlist-implementation.md', `
# Wishlist Implementation Plan

## Architecture
- Follow cart pattern: Context + useReducer + localStorage
- Add wishlist field to User type
- Create WishlistContext
- Create useWishlist hook

## Files to create
- src/contexts/WishlistContext.tsx
- src/hooks/use-wishlist/hook.use-wishlist.ts
- src/types/dto/type.wishlist-dto.ts

## Files to modify
- src/types/dto/type.user-dto.ts (add wishlist field)
- src/app/layout.tsx (add WishlistProvider)
`)

// PHASE 4: EXECUTE
Write('src/types/dto/type.wishlist-dto.ts', ...)
Write('src/contexts/WishlistContext.tsx', ...)
Write('src/hooks/use-wishlist/hook.use-wishlist.ts', ...)
Edit('src/types/dto/type.user-dto.ts', ...)
Edit('src/app/layout.tsx', ...)

// PHASE 5: VERIFY
Bash('pnpm typecheck')
Bash('pnpm test src/hooks/use-wishlist')
```

### E-commerce: Refactor API Service

```typescript
// PHASE 1: DISCOVER
// Goal: Find all API service files

Glob('src/services/**/*.ts')  // List all services

// Read a few to understand pattern
Read('src/services/order/service.order.ts')
Read('src/services/product/service.product.ts')
Read('src/services/user/service.user.ts')

// Find endpoint usage
Grep('fetch\\(', 'src/services/', { output_mode: 'content' })
Grep('axios\\.', 'src/services/', { output_mode: 'content' })

// PHASE 2: ANALYZE
// Findings:
// - Some services use fetch, some use axios
// - Endpoints are hardcoded
// - No consistent error handling
// - No retry logic

// PHASE 3: PLAN
Write('docs/plans/api-service-refactor.md', `
# API Service Refactor

## Problems
- Inconsistent HTTP client (fetch vs axios)
- Hardcoded endpoints
- No error handling
- No retry logic

## Solution
- Create ApiClient wrapper
- Centralize endpoints in config
- Add error handling middleware
- Add retry logic

## Migration Strategy
1. Create ApiClient
2. Create endpoints config
3. Migrate one service at a time
4. Test each migration
`)

// PHASE 4: EXECUTE (Incremental)

// Step 1: Create infrastructure
Write('src/api/client/api-client.ts', ...)
Write('src/api/config/endpoints.ts', ...)

// Step 2: Migrate one service
Read('src/services/product/service.product.ts')  // Current code
Edit('src/services/product/service.product.ts', ...)  // Migrate

// Step 3: Test
Bash('pnpm test src/services/product')

// Step 4: Repeat for other services
Read('src/services/order/service.order.ts')
Edit('src/services/order/service.order.ts', ...)
Bash('pnpm test src/services/order')

// PHASE 5: VERIFY
Bash('pnpm typecheck')
Bash('pnpm test src/services/')
Bash('pnpm build')
```

### E-commerce: Debug Checkout Issue

```typescript
// PHASE 1: DISCOVER
// Goal: Understand checkout flow

// Step 1: Find checkout files
Glob('src/**/*checkout*')

// Step 2: Read main files
Read('src/screens/Checkout/CheckoutScreen.tsx')
Read('src/services/order/service.order.ts')
Read('src/api/routes/checkout/route.ts')

// Step 3: Search for error handling
Grep('try.*catch', 'src/screens/Checkout/', { output_mode: 'content' })
Grep('throw new Error', 'src/services/order/', { output_mode: 'content' })

// PHASE 2: ANALYZE
// Flow: CheckoutScreen → useCheckout hook → OrderService → API
// Error occurs in OrderService.createOrder()

// PHASE 3: PLAN
// Add logging at each step
// Add validation before API call
// Add better error messages

// PHASE 4: EXECUTE
Edit('src/services/order/service.order.ts', `
// Add validation
if (!order.shipping.phone) {
  throw new ValidationError('Phone is required')
}

// Add logging
console.log('Creating order:', order)

try {
  const response = await apiClient.post(ENDPOINTS.ORDERS.CREATE, order)
  console.log('Order created:', response.data)
  return response.data
} catch (error) {
  console.error('Order creation failed:', error)
  throw error
}
`)

// PHASE 5: VERIFY
Bash('pnpm dev')  // Start dev server
// Test checkout flow manually
// Check console logs
```

## Sequencing Rules

### Rule 1: Read Before Write
```typescript
// ❌ WRONG
Edit('file.ts', ...)  // Don't know current content

// ✅ CORRECT
Read('file.ts')       // Understand current state
Edit('file.ts', ...)  // Make informed changes
```

### Rule 2: Search Before Read
```typescript
// ❌ WRONG
Read('src/components/Button.tsx')  // Guessing location

// ✅ CORRECT
Glob('**/*Button*')                // Find all Button files
Read('src/components/Button.tsx')  // Read correct file
```

### Rule 3: Plan Before Execute
```typescript
// ❌ WRONG
Write('new-feature.ts', ...)  // No plan

// ✅ CORRECT
Write('docs/plans/new-feature.md', ...)  // Document plan
Write('new-feature.ts', ...)             // Implement plan
```

### Rule 4: Verify After Execute
```typescript
// ❌ WRONG
Edit('file.ts', ...)  // Done!

// ✅ CORRECT
Edit('file.ts', ...)
Bash('pnpm typecheck')  // Verify syntax
Bash('pnpm test')       // Verify functionality
```

## Best Practices

### Do's
✅ Discover before executing
✅ Read files before editing
✅ Search broadly, then narrow
✅ Plan multi-step changes
✅ Verify after changes
✅ Use parallel reads when possible

### Don'ts
❌ Edit without reading
❌ Skip discovery phase
❌ Make changes without plan
❌ Forget to verify
❌ Read files sequentially when parallel works
❌ Execute before understanding

## Trade-offs

| Ưu điểm | Nhược điểm |
|---------|------------|
| Fewer mistakes | More upfront time |
| Better context | More tool calls |
| Safer changes | Feels slower initially |
| Easier debugging | Requires discipline |

## Related Patterns
- [Semantic Code Search](./pattern-semantic-code-search.md)
- [Spec-Driven Development](./pattern-spec-driven-development.md)
