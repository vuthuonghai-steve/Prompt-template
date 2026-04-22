# Pattern: Code Quality Standards

## Nguồn
- Claude Code
- Cursor Agent
- Windsurf Cascade

## Mô tả
Maintain high code quality standards: readability, maintainability, consistency. Automated checks, code reviews, refactoring.

## Khi nào dùng
- Maintenance: continuous code quality
- Development: enforce standards
- Code review: quality gates
- Refactoring: improve existing code

## Cách áp dụng

### 1. Code Quality Metrics
```typescript
interface CodeQualityMetrics {
  // Complexity
  cyclomaticComplexity: number  // < 10 per function
  cognitiveComplexity: number   // < 15 per function
  
  // Size
  linesOfCode: number           // < 300 per file
  functionsPerFile: number      // < 10 per file
  
  // Maintainability
  maintainabilityIndex: number  // > 65
  technicalDebt: number         // hours to fix
  
  // Coverage
  testCoverage: number          // > 80%
  
  // Duplication
  duplicatedLines: number       // < 3%
}
```

### 2. Linting Rules
```typescript
// .eslintrc.js
module.exports = {
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:react/recommended',
    'plugin:react-hooks/recommended',
  ],
  rules: {
    // Code quality
    'complexity': ['error', 10],
    'max-lines': ['error', 300],
    'max-lines-per-function': ['error', 50],
    'max-params': ['error', 4],
    'max-depth': ['error', 3],
    
    // Best practices
    'no-console': ['warn', { allow: ['warn', 'error'] }],
    'no-debugger': 'error',
    'no-var': 'error',
    'prefer-const': 'error',
    'eqeqeq': ['error', 'always'],
    
    // TypeScript
    '@typescript-eslint/no-explicit-any': 'error',
    '@typescript-eslint/explicit-function-return-type': 'warn',
    '@typescript-eslint/no-unused-vars': 'error',
    
    // React
    'react/prop-types': 'off', // Using TypeScript
    'react-hooks/rules-of-hooks': 'error',
    'react-hooks/exhaustive-deps': 'warn',
  },
}
```

### 3. Code Review Checklist
```typescript
interface CodeReviewChecklist {
  // Functionality
  meetsRequirements: boolean
  edgeCasesHandled: boolean
  errorHandlingAdequate: boolean
  
  // Code quality
  readable: boolean
  maintainable: boolean
  testable: boolean
  
  // Best practices
  followsConventions: boolean
  noCodeSmells: boolean
  properlyDocumented: boolean
  
  // Performance
  noPerformanceIssues: boolean
  efficientAlgorithms: boolean
  
  // Security
  noSecurityVulnerabilities: boolean
  inputValidated: boolean
  sensitiveDataProtected: boolean
}
```

## Ví dụ thực tế

### Refactoring: Extract Function

```typescript
// ❌ Before: Long function, hard to understand
function processOrder(order: Order) {
  // Validate order
  if (!order.items || order.items.length === 0) {
    throw new Error('Order must have items')
  }
  if (!order.shippingAddress) {
    throw new Error('Shipping address required')
  }
  if (!order.paymentMethod) {
    throw new Error('Payment method required')
  }
  
  // Calculate totals
  let subtotal = 0
  for (const item of order.items) {
    subtotal += item.price * item.quantity
  }
  
  let shipping = 0
  if (subtotal < 500000) {
    shipping = 30000
  }
  
  let discount = 0
  if (order.voucher) {
    if (order.voucher.type === 'percentage') {
      discount = subtotal * (order.voucher.value / 100)
    } else {
      discount = order.voucher.value
    }
  }
  
  const total = subtotal + shipping - discount
  
  // Process payment
  const payment = await processPayment({
    amount: total,
    method: order.paymentMethod,
  })
  
  // Create order record
  const createdOrder = await db.orders.create({
    ...order,
    subtotal,
    shipping,
    discount,
    total,
    paymentId: payment.id,
  })
  
  return createdOrder
}

// ✅ After: Extracted functions, clear responsibilities
function processOrder(order: Order) {
  validateOrder(order)
  
  const pricing = calculatePricing(order)
  const payment = await processPayment(pricing.total, order.paymentMethod)
  const createdOrder = await createOrderRecord(order, pricing, payment)
  
  return createdOrder
}

function validateOrder(order: Order): void {
  if (!order.items?.length) {
    throw new Error('Order must have items')
  }
  if (!order.shippingAddress) {
    throw new Error('Shipping address required')
  }
  if (!order.paymentMethod) {
    throw new Error('Payment method required')
  }
}

function calculatePricing(order: Order): OrderPricing {
  const subtotal = calculateSubtotal(order.items)
  const shipping = calculateShipping(subtotal)
  const discount = calculateDiscount(subtotal, order.voucher)
  const total = subtotal + shipping - discount
  
  return { subtotal, shipping, discount, total }
}

function calculateSubtotal(items: OrderItem[]): number {
  return items.reduce(
    (sum, item) => sum + item.price * item.quantity,
    0
  )
}

function calculateShipping(subtotal: number): number {
  return subtotal < 500000 ? 30000 : 0
}

function calculateDiscount(
  subtotal: number,
  voucher?: Voucher
): number {
  if (!voucher) return 0
  
  return voucher.type === 'percentage'
    ? subtotal * (voucher.value / 100)
    : voucher.value
}
```

### Refactoring: Replace Magic Numbers

```typescript
// ❌ Before: Magic numbers
function calculateShipping(subtotal: number): number {
  if (subtotal < 500000) {
    return 30000
  }
  return 0
}

function applyVoucher(subtotal: number, voucher: Voucher): number {
  if (subtotal < 100000) {
    throw new Error('Minimum order not met')
  }
  
  if (voucher.value > subtotal * 0.5) {
    throw new Error('Discount too large')
  }
  
  return voucher.value
}

// ✅ After: Named constants
const SHIPPING = {
  FREE_SHIPPING_THRESHOLD: 500000,
  STANDARD_FEE: 30000,
} as const

const VOUCHER = {
  MIN_ORDER: 100000,
  MAX_DISCOUNT_PERCENTAGE: 0.5,
} as const

function calculateShipping(subtotal: number): number {
  return subtotal < SHIPPING.FREE_SHIPPING_THRESHOLD
    ? SHIPPING.STANDARD_FEE
    : 0
}

function applyVoucher(subtotal: number, voucher: Voucher): number {
  if (subtotal < VOUCHER.MIN_ORDER) {
    throw new Error('Minimum order not met')
  }
  
  const maxDiscount = subtotal * VOUCHER.MAX_DISCOUNT_PERCENTAGE
  if (voucher.value > maxDiscount) {
    throw new Error('Discount too large')
  }
  
  return voucher.value
}
```

### Refactoring: Simplify Conditionals

```typescript
// ❌ Before: Complex nested conditionals
function getProductStatus(product: Product): string {
  if (product.inStock) {
    if (product.quantity > 10) {
      return 'In Stock'
    } else {
      if (product.quantity > 0) {
        return 'Low Stock'
      } else {
        return 'Out of Stock'
      }
    }
  } else {
    return 'Out of Stock'
  }
}

// ✅ After: Early returns, clear logic
function getProductStatus(product: Product): string {
  if (!product.inStock || product.quantity === 0) {
    return 'Out of Stock'
  }
  
  if (product.quantity <= 10) {
    return 'Low Stock'
  }
  
  return 'In Stock'
}
```

### Code Quality Automation

```typescript
// package.json scripts
{
  "scripts": {
    "lint": "eslint . --ext .ts,.tsx",
    "lint:fix": "eslint . --ext .ts,.tsx --fix",
    "format": "prettier --write \"**/*.{ts,tsx,json,md}\"",
    "type-check": "tsc --noEmit",
    "test": "vitest",
    "test:coverage": "vitest --coverage",
    "quality": "npm run lint && npm run type-check && npm run test",
    "pre-commit": "lint-staged"
  }
}

// .husky/pre-commit
#!/bin/sh
. "$(dirname "$0")/_/husky.sh"

npm run quality
```

### SonarQube Integration

```yaml
# sonar-project.properties
sonar.projectKey=flower-shop
sonar.projectName=Flower Shop
sonar.sources=src
sonar.tests=src
sonar.test.inclusions=**/*.test.ts,**/*.test.tsx
sonar.typescript.lcov.reportPaths=coverage/lcov.info

# Quality gates
sonar.qualitygate.wait=true
sonar.coverage.exclusions=**/*.test.ts,**/*.test.tsx

# Thresholds
sonar.coverage.minimum=80
sonar.duplicated_lines_density.maximum=3
sonar.complexity.maximum=10
```

## Code Quality Checklist

### Readability
- [ ] Clear variable/function names
- [ ] Consistent formatting
- [ ] Appropriate comments
- [ ] Logical code organization

### Maintainability
- [ ] Functions < 50 lines
- [ ] Files < 300 lines
- [ ] Complexity < 10
- [ ] No code duplication

### Testability
- [ ] Pure functions where possible
- [ ] Dependencies injected
- [ ] Side effects isolated
- [ ] Test coverage > 80%

### Performance
- [ ] No premature optimization
- [ ] Efficient algorithms
- [ ] No memory leaks
- [ ] Lazy loading where appropriate

## Trade-offs

| Ưu điểm | Nhược điểm |
|---------|------------|
| Easier maintenance | Upfront time investment |
| Fewer bugs | Can slow development |
| Better collaboration | Requires discipline |

## Best Practices
1. **Automate quality checks**: Linting, formatting, tests
2. **Code review**: Peer review before merge
3. **Refactor continuously**: Don't accumulate tech debt
4. **Measure quality**: Track metrics over time
5. **Document standards**: Team alignment
6. **Learn from mistakes**: Post-mortems, retrospectives

## Anti-patterns
- ❌ Ignore linter warnings
- ❌ Skip code reviews
- ❌ Accumulate tech debt
- ❌ No quality metrics
- ❌ Inconsistent standards

## Related Patterns
- [Refactoring Maintainability](./pattern-refactoring-maintainability.md)
