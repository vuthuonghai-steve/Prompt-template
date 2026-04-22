# Pattern: Refactoring Maintainability

## Nguồn
- Claude Code
- Cursor Agent
- Windsurf Cascade

## Mô tả
Systematic refactoring để improve code maintainability: reduce complexity, eliminate duplication, improve structure. Không thay đổi behavior.

## Khi nào dùng
- Maintenance: continuous improvement
- Before adding features: clean up first
- After bug fixes: prevent similar bugs
- Code smells detected: address immediately

## Cách áp dụng

### 1. Refactoring Catalog
```typescript
// Common refactoring patterns
enum RefactoringType {
  EXTRACT_FUNCTION = 'extract-function',
  EXTRACT_VARIABLE = 'extract-variable',
  INLINE_FUNCTION = 'inline-function',
  RENAME = 'rename',
  MOVE_FUNCTION = 'move-function',
  REPLACE_CONDITIONAL = 'replace-conditional',
  INTRODUCE_PARAMETER = 'introduce-parameter',
  REMOVE_DEAD_CODE = 'remove-dead-code',
}
```

### 2. Code Smells Detection
```typescript
interface CodeSmell {
  type: string
  severity: 'low' | 'medium' | 'high'
  location: string
  suggestion: string
}

const codeSmells = [
  {
    type: 'Long Function',
    severity: 'high',
    location: 'processOrder:1-150',
    suggestion: 'Extract smaller functions',
  },
  {
    type: 'Duplicate Code',
    severity: 'medium',
    location: 'calculateTotal, calculateSubtotal',
    suggestion: 'Extract common logic',
  },
  {
    type: 'Magic Numbers',
    severity: 'low',
    location: 'calculateShipping:5',
    suggestion: 'Replace with named constants',
  },
]
```

### 3. Refactoring Workflow
```typescript
// Safe refactoring process
async function refactor(
  filePath: string,
  refactoringType: RefactoringType
) {
  // 1. Ensure tests exist
  const hasTests = await checkTestCoverage(filePath)
  if (!hasTests) {
    throw new Error('Add tests before refactoring')
  }
  
  // 2. Run tests (baseline)
  const baselineTests = await runTests(filePath)
  if (!baselineTests.passed) {
    throw new Error('Fix failing tests first')
  }
  
  // 3. Apply refactoring
  await applyRefactoring(filePath, refactoringType)
  
  // 4. Run tests again
  const afterTests = await runTests(filePath)
  if (!afterTests.passed) {
    // Rollback
    await revertChanges(filePath)
    throw new Error('Refactoring broke tests')
  }
  
  // 5. Commit
  await commitChanges(filePath, `refactor: ${refactoringType}`)
}
```

## Ví dụ thực tế

### Extract Function

```typescript
// ❌ Before: Long function
async function handleCheckout(order: Order) {
  // Validate
  if (!order.items?.length) throw new Error('No items')
  if (!order.address) throw new Error('No address')
  
  // Calculate
  let total = 0
  for (const item of order.items) {
    total += item.price * item.quantity
  }
  
  // Apply discount
  if (order.voucher) {
    if (order.voucher.type === 'percentage') {
      total -= total * (order.voucher.value / 100)
    } else {
      total -= order.voucher.value
    }
  }
  
  // Process payment
  const payment = await stripe.charge({
    amount: total,
    currency: 'VND',
    source: order.paymentToken,
  })
  
  // Create order
  const createdOrder = await db.orders.create({
    ...order,
    total,
    paymentId: payment.id,
    status: 'paid',
  })
  
  // Send email
  await sendEmail({
    to: order.email,
    subject: 'Order Confirmation',
    body: `Your order ${createdOrder.id} is confirmed`,
  })
  
  return createdOrder
}

// ✅ After: Extracted functions
async function handleCheckout(order: Order) {
  validateOrder(order)
  
  const total = calculateTotal(order)
  const payment = await processPayment(total, order.paymentToken)
  const createdOrder = await createOrder(order, total, payment.id)
  
  await sendOrderConfirmation(createdOrder)
  
  return createdOrder
}

function validateOrder(order: Order): void {
  if (!order.items?.length) {
    throw new Error('Order must have items')
  }
  if (!order.address) {
    throw new Error('Shipping address required')
  }
}

function calculateTotal(order: Order): number {
  const subtotal = order.items.reduce(
    (sum, item) => sum + item.price * item.quantity,
    0
  )
  
  return applyDiscount(subtotal, order.voucher)
}

function applyDiscount(amount: number, voucher?: Voucher): number {
  if (!voucher) return amount
  
  return voucher.type === 'percentage'
    ? amount * (1 - voucher.value / 100)
    : amount - voucher.value
}

async function processPayment(
  amount: number,
  token: string
): Promise<Payment> {
  return stripe.charge({
    amount,
    currency: 'VND',
    source: token,
  })
}

async function createOrder(
  order: Order,
  total: number,
  paymentId: string
): Promise<Order> {
  return db.orders.create({
    ...order,
    total,
    paymentId,
    status: 'paid',
  })
}

async function sendOrderConfirmation(order: Order): Promise<void> {
  await sendEmail({
    to: order.email,
    subject: 'Order Confirmation',
    body: `Your order ${order.id} is confirmed`,
  })
}
```

### Replace Conditional with Polymorphism

```typescript
// ❌ Before: Type checking with conditionals
class PaymentProcessor {
  process(payment: Payment) {
    if (payment.method === 'vnpay') {
      return this.processVNPay(payment)
    } else if (payment.method === 'momo') {
      return this.processMomo(payment)
    } else if (payment.method === 'cod') {
      return this.processCOD(payment)
    } else {
      throw new Error('Unknown payment method')
    }
  }
  
  private processVNPay(payment: Payment) { /* ... */ }
  private processMomo(payment: Payment) { /* ... */ }
  private processCOD(payment: Payment) { /* ... */ }
}

// ✅ After: Polymorphism
interface PaymentMethod {
  process(payment: Payment): Promise<PaymentResult>
}

class VNPayMethod implements PaymentMethod {
  async process(payment: Payment): Promise<PaymentResult> {
    // VNPay-specific logic
    const response = await vnpayAPI.charge({
      amount: payment.amount,
      orderId: payment.orderId,
    })
    
    return {
      success: response.status === 'success',
      transactionId: response.transactionId,
    }
  }
}

class MomoMethod implements PaymentMethod {
  async process(payment: Payment): Promise<PaymentResult> {
    // Momo-specific logic
    const response = await momoAPI.createPayment({
      amount: payment.amount,
      orderInfo: payment.orderId,
    })
    
    return {
      success: response.resultCode === 0,
      transactionId: response.transId,
    }
  }
}

class CODMethod implements PaymentMethod {
  async process(payment: Payment): Promise<PaymentResult> {
    // COD logic (no actual payment)
    return {
      success: true,
      transactionId: `COD-${Date.now()}`,
    }
  }
}

// Factory
class PaymentMethodFactory {
  static create(method: string): PaymentMethod {
    switch (method) {
      case 'vnpay':
        return new VNPayMethod()
      case 'momo':
        return new MomoMethod()
      case 'cod':
        return new CODMethod()
      default:
        throw new Error(`Unknown payment method: ${method}`)
    }
  }
}

// Usage
class PaymentProcessor {
  async process(payment: Payment): Promise<PaymentResult> {
    const method = PaymentMethodFactory.create(payment.method)
    return method.process(payment)
  }
}
```

### Introduce Parameter Object

```typescript
// ❌ Before: Too many parameters
function createProduct(
  name: string,
  price: number,
  category: string,
  description: string,
  image: string,
  inStock: boolean,
  quantity: number,
  sku: string
) {
  return db.products.create({
    name,
    price,
    category,
    description,
    image,
    inStock,
    quantity,
    sku,
  })
}

// Usage
createProduct(
  'Rose Bouquet',
  500000,
  'roses',
  'Beautiful red roses',
  '/roses.jpg',
  true,
  10,
  'ROSE-001'
)

// ✅ After: Parameter object
interface CreateProductParams {
  name: string
  price: number
  category: string
  description: string
  image: string
  inStock: boolean
  quantity: number
  sku: string
}

function createProduct(params: CreateProductParams) {
  return db.products.create(params)
}

// Usage
createProduct({
  name: 'Rose Bouquet',
  price: 500000,
  category: 'roses',
  description: 'Beautiful red roses',
  image: '/roses.jpg',
  inStock: true,
  quantity: 10,
  sku: 'ROSE-001',
})
```

### Remove Dead Code

```typescript
// ❌ Before: Unused code
class ProductService {
  // Used
  async getProduct(id: string) {
    return db.products.findById(id)
  }
  
  // DEAD CODE - never called
  async getProductByName(name: string) {
    return db.products.findOne({ name })
  }
  
  // DEAD CODE - old implementation
  async getProductsOld() {
    return db.products.find()
  }
  
  // Used
  async getProducts(filters: ProductFilters) {
    return db.products.find(filters)
  }
}

// ✅ After: Dead code removed
class ProductService {
  async getProduct(id: string) {
    return db.products.findById(id)
  }
  
  async getProducts(filters: ProductFilters) {
    return db.products.find(filters)
  }
}
```

### Simplify Complex Conditionals

```typescript
// ❌ Before: Complex nested conditionals
function canApplyVoucher(
  order: Order,
  voucher: Voucher
): boolean {
  if (voucher.active) {
    if (voucher.expiresAt > new Date()) {
      if (order.total >= voucher.minOrder) {
        if (voucher.maxUses === null || voucher.usedCount < voucher.maxUses) {
          if (voucher.categories.length === 0 || 
              order.items.some(item => 
                voucher.categories.includes(item.category)
              )) {
            return true
          }
        }
      }
    }
  }
  return false
}

// ✅ After: Early returns, clear logic
function canApplyVoucher(
  order: Order,
  voucher: Voucher
): boolean {
  if (!voucher.active) return false
  if (voucher.expiresAt <= new Date()) return false
  if (order.total < voucher.minOrder) return false
  
  const hasReachedMaxUses = 
    voucher.maxUses !== null && 
    voucher.usedCount >= voucher.maxUses
  if (hasReachedMaxUses) return false
  
  const hasCategoryRestriction = voucher.categories.length > 0
  if (hasCategoryRestriction) {
    const hasMatchingCategory = order.items.some(item =>
      voucher.categories.includes(item.category)
    )
    if (!hasMatchingCategory) return false
  }
  
  return true
}
```

## Refactoring Checklist

### Before Refactoring
- [ ] Tests exist và pass
- [ ] Understand current behavior
- [ ] Identify code smell
- [ ] Plan refactoring approach

### During Refactoring
- [ ] Make small changes
- [ ] Run tests frequently
- [ ] Commit after each step
- [ ] Don't change behavior

### After Refactoring
- [ ] All tests still pass
- [ ] Code is cleaner
- [ ] No new bugs introduced
- [ ] Document if needed

## Trade-offs

| Ưu điểm | Nhược điểm |
|---------|------------|
| Easier to maintain | Takes time |
| Fewer bugs | Risk of breaking |
| Better design | Requires discipline |

## Best Practices
1. **Test first**: Ensure tests exist before refactoring
2. **Small steps**: One refactoring at a time
3. **Commit often**: Easy to rollback
4. **Don't change behavior**: Refactoring ≠ new features
5. **Use IDE tools**: Automated refactoring
6. **Review code smells**: Regular code reviews

## Anti-patterns
- ❌ Refactor without tests
- ❌ Mix refactoring với new features
- ❌ Large refactoring in one commit
- ❌ Ignore code smells
- ❌ Over-engineer

## Related Patterns
- [Code Quality Standards](./pattern-code-quality-standards.md)
