# Pattern: Linter-Driven Recovery

## Nguồn
- Claude Code
- Cursor
- Windsurf

## Mô tả
Use linter/compiler errors as feedback loop to guide code fixes. Let type checker and linter tell you what's wrong, then fix systematically.

## Khi nào dùng
- After large refactors
- When fixing type errors
- After dependency updates
- When integrating new code
- During migration tasks

## Cách áp dụng

### 1. Error-Driven Workflow

```
1. Make Change
   └── Edit code

2. Run Linter
   └── Get error list

3. Analyze Errors
   ├── Group by type
   ├── Identify root causes
   └── Prioritize fixes

4. Fix Systematically
   ├── Fix root causes first
   ├── Re-run linter after each fix
   └── Verify error count decreases

5. Verify
   └── All errors resolved
```

### 2. TypeScript Error Recovery

```typescript
// Step 1: Run type checker
$ pnpm typecheck

// Output:
// src/services/order/service.order.ts:45:12 - error TS2339: 
//   Property 'totalAmount' does not exist on type 'Order'.
// src/services/order/service.order.ts:67:8 - error TS2345: 
//   Argument of type 'string' is not assignable to parameter of type 'number'.
// src/hooks/use-cart/hook.use-cart.ts:23:5 - error TS2322: 
//   Type 'CartItem[]' is not assignable to type 'readonly CartItem[]'.

// Step 2: Analyze errors
// - Missing property: totalAmount
// - Type mismatch: string vs number
// - Readonly violation: CartItem[]

// Step 3: Fix root cause first (missing property)
// Edit type definition
interface Order {
  id: string
  items: OrderItem[]
  totalAmount: number  // ✅ Add missing property
  status: OrderStatus
}

// Step 4: Re-run to see remaining errors
$ pnpm typecheck
// Now only 2 errors remain

// Step 5: Fix type mismatch
const price = parseFloat(priceString)  // Convert string to number

// Step 6: Fix readonly violation
const items: readonly CartItem[] = cart.items  // Add readonly

// Step 7: Verify all fixed
$ pnpm typecheck
// ✅ No errors
```

### 3. ESLint Error Recovery

```typescript
// Step 1: Run linter
$ pnpm lint

// Output:
// src/components/ProductCard.tsx
//   12:7   error  'product' is assigned a value but never used  @typescript-eslint/no-unused-vars
//   23:15  error  Missing return type on function              @typescript-eslint/explicit-function-return-type
//   45:3   error  Unexpected console statement                 no-console

// Step 2: Group by rule
// - no-unused-vars: 1 error
// - explicit-function-return-type: 1 error
// - no-console: 1 error

// Step 3: Fix each systematically

// Fix 1: Remove unused variable
- const product = getProduct(id)
+ // Removed unused variable

// Fix 2: Add return type
- function calculateTotal(items) {
+ function calculateTotal(items: CartItem[]): number {
    return items.reduce((sum, item) => sum + item.price, 0)
  }

// Fix 3: Remove console.log
- console.log('Product loaded:', product)
+ // Use proper logging in production

// Step 4: Verify
$ pnpm lint
// ✅ No errors
```

## Ví dụ thực tế

### E-commerce: Refactor Order Service

```typescript
// Initial refactor: Change Order type
interface Order {
  id: string
  items: OrderItem[]
  // Changed: totalAmount → total
  total: number
  // Changed: status → orderStatus
  orderStatus: OrderStatus
}

// Step 1: Run type checker
$ pnpm typecheck

// Errors found:
// src/services/order/service.order.ts:45:12 - error TS2339: 
//   Property 'totalAmount' does not exist on type 'Order'.
// src/services/order/service.order.ts:67:8 - error TS2339: 
//   Property 'status' does not exist on type 'Order'.
// src/screens/OrderDetail/OrderDetailScreen.tsx:89:23 - error TS2339: 
//   Property 'totalAmount' does not exist on type 'Order'.
// src/screens/OrderList/OrderListScreen.tsx:34:15 - error TS2339: 
//   Property 'status' does not exist on type 'Order'.

// Step 2: Analyze - 4 files need updates

// Step 3: Fix service layer first
Edit('src/services/order/service.order.ts', `
- return order.totalAmount
+ return order.total

- if (order.status === 'pending') {
+ if (order.orderStatus === 'pending') {
`)

// Step 4: Re-run
$ pnpm typecheck
// 2 errors remain (in screens)

// Step 5: Fix screens
Edit('src/screens/OrderDetail/OrderDetailScreen.tsx', `
- <Text>{order.totalAmount}</Text>
+ <Text>{order.total}</Text>
`)

Edit('src/screens/OrderList/OrderListScreen.tsx', `
- <Badge>{order.status}</Badge>
+ <Badge>{order.orderStatus}</Badge>
`)

// Step 6: Verify
$ pnpm typecheck
// ✅ No errors
```

### E-commerce: Fix Import Errors After Restructure

```typescript
// Restructured: Moved files to new locations
// src/utils/format.ts → src/utils/format/util.format-currency.ts

// Step 1: Run type checker
$ pnpm typecheck

// Errors:
// src/components/ProductCard.tsx:3:24 - error TS2307: 
//   Cannot find module '@/utils/format' or its corresponding type declarations.
// src/screens/Cart/CartScreen.tsx:5:24 - error TS2307: 
//   Cannot find module '@/utils/format' or its corresponding type declarations.
// src/screens/Checkout/CheckoutScreen.tsx:7:24 - error TS2307: 
//   Cannot find module '@/utils/format' or its corresponding type declarations.

// Step 2: Search for all imports
$ grep -r "from '@/utils/format'" src/

// Found 3 files

// Step 3: Fix all imports
Edit('src/components/ProductCard.tsx', `
- import { formatCurrency } from '@/utils/format'
+ import { formatCurrency } from '@/utils/format/util.format-currency'
`)

Edit('src/screens/Cart/CartScreen.tsx', `
- import { formatCurrency } from '@/utils/format'
+ import { formatCurrency } from '@/utils/format/util.format-currency'
`)

Edit('src/screens/Checkout/CheckoutScreen.tsx', `
- import { formatCurrency } from '@/utils/format'
+ import { formatCurrency } from '@/utils/format/util.format-currency'
`)

// Step 4: Verify
$ pnpm typecheck
// ✅ No errors
```

### E-commerce: Fix After Dependency Update

```typescript
// Updated: react-hook-form v7 → v8 (breaking changes)

// Step 1: Run type checker
$ pnpm typecheck

// Errors:
// src/screens/Checkout/CheckoutForm.tsx:15:5 - error TS2322: 
//   Type '{ mode: string; }' is not assignable to type 'UseFormProps'.
// src/screens/Checkout/CheckoutForm.tsx:23:12 - error TS2339: 
//   Property 'errors' does not exist on type 'UseFormReturn'.

// Step 2: Check migration guide
// v8 changes:
// - mode: 'onSubmit' → mode: 'onSubmit' as const
// - errors → formState.errors

// Step 3: Fix based on migration guide
Edit('src/screens/Checkout/CheckoutForm.tsx', `
  const {
    register,
    handleSubmit,
-   errors,
+   formState: { errors },
  } = useForm({
-   mode: 'onSubmit',
+   mode: 'onSubmit' as const,
  })
`)

// Step 4: Verify
$ pnpm typecheck
// ✅ No errors
```

## Recovery Strategies

### Strategy 1: Root Cause First

```typescript
// ❌ WRONG: Fix symptoms
Edit('file1.ts', ...) // Fix error 1
Edit('file2.ts', ...) // Fix error 2
Edit('file3.ts', ...) // Fix error 3
// 10 more files...

// ✅ CORRECT: Fix root cause
Edit('types/order.ts', ...) // Fix type definition
// All 13 errors resolved automatically
```

### Strategy 2: Incremental Verification

```typescript
// ❌ WRONG: Fix all, then verify
Edit('file1.ts', ...)
Edit('file2.ts', ...)
Edit('file3.ts', ...)
Bash('pnpm typecheck') // Many errors!

// ✅ CORRECT: Verify after each fix
Edit('file1.ts', ...)
Bash('pnpm typecheck') // Check progress
Edit('file2.ts', ...)
Bash('pnpm typecheck') // Check progress
```

### Strategy 3: Automated Fixes First

```typescript
// Step 1: Try auto-fix
$ pnpm lint --fix

// Step 2: Check what remains
$ pnpm lint

// Step 3: Fix remaining manually
Edit('file.ts', ...)
```

## Linter Configuration

### TypeScript Strict Mode

```json
// tsconfig.json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true
  }
}
```

### ESLint Rules

```javascript
// .eslintrc.js
module.exports = {
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:react/recommended',
    'plugin:react-hooks/recommended'
  ],
  rules: {
    '@typescript-eslint/explicit-function-return-type': 'error',
    '@typescript-eslint/no-unused-vars': 'error',
    'no-console': 'warn',
    'react-hooks/exhaustive-deps': 'error'
  }
}
```

## Best Practices

### Do's
✅ Run linter after each change
✅ Fix root causes first
✅ Group similar errors
✅ Use auto-fix when available
✅ Verify incrementally
✅ Read error messages carefully

### Don'ts
❌ Ignore linter errors
❌ Fix symptoms instead of root cause
❌ Make multiple changes before verifying
❌ Disable rules without understanding
❌ Skip type checking
❌ Commit with linter errors

## Trade-offs

| Ưu điểm | Nhược điểm |
|---------|------------|
| Systematic error resolution | Requires linter setup |
| Catches issues early | Can be noisy initially |
| Guides fixes | May slow down initially |
| Prevents regressions | Requires discipline |

## Related Patterns
- [Tool Use Sequencing](./pattern-tool-use-sequencing.md)
- [Test-Driven Development](../../6-testing/patterns/pattern-test-driven-validation.md)
