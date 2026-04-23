# Pattern: Spec-Driven Development

## Nguồn
- Claude Code
- Cursor
- Windsurf

## Mô tả
Write detailed specification first, then implement against that spec. Spec acts as contract between planning and implementation phases.

## Khi nào dùng
- Complex features requiring coordination
- Multi-file changes
- API design
- Architecture decisions
- Team collaboration scenarios

## Cách áp dụng

### 1. Spec Structure

```markdown
# Feature Specification: [Feature Name]

## Overview
[Brief description of what this feature does]

## Requirements
### Functional
- [ ] Requirement 1
- [ ] Requirement 2

### Non-Functional
- [ ] Performance target
- [ ] Security requirement

## Architecture
[Component diagram, data flow]

## API Contract
```typescript
interface FeatureAPI {
  method(params: Params): Promise<Result>
}
```

## Implementation Checklist
- [ ] Step 1
- [ ] Step 2

## Test Scenarios
- [ ] Happy path
- [ ] Error cases
```

### 2. Spec-First Workflow

```
1. Write Spec
   ├── Define requirements
   ├── Design API contract
   ├── Plan architecture
   └── List test scenarios

2. Review Spec
   ├── Stakeholder approval
   └── Technical review

3. Implement Against Spec
   ├── Follow API contract exactly
   ├── Check off implementation steps
   └── Verify test scenarios

4. Validate Compliance
   ├── Does code match spec?
   └── Are all requirements met?
```

### 3. API Contract Example

```typescript
// spec.md
/**
 * Product Search API
 * 
 * Requirements:
 * - Support text search
 * - Support category filter
 * - Support price range
 * - Return paginated results
 * - Response time < 300ms p95
 */

interface ProductSearchParams {
  query?: string
  category?: string
  minPrice?: number
  maxPrice?: number
  page?: number
  limit?: number
}

interface ProductSearchResponse {
  products: Product[]
  total: number
  page: number
  hasMore: boolean
}

// Implementation must match this contract exactly
export async function searchProducts(
  params: ProductSearchParams
): Promise<ProductSearchResponse>
```

## Ví dụ thực tế

### E-commerce: Checkout Flow Spec

```markdown
# Checkout Flow Specification

## Requirements
- [ ] Collect shipping information
- [ ] Validate phone number format (Vietnam)
- [ ] Support multiple payment methods (VNPay, COD)
- [ ] Calculate shipping fee based on district
- [ ] Create order in database
- [ ] Send confirmation email
- [ ] Redirect to success page

## API Contract
```typescript
interface CheckoutRequest {
  cartId: string
  shipping: {
    name: string
    phone: string // Format: 0XXXXXXXXX
    address: string
    district: string
  }
  paymentMethod: 'vnpay' | 'cod'
}

interface CheckoutResponse {
  orderId: string
  totalAmount: number
  paymentUrl?: string // Only for VNPay
}
```

## Error Handling
- Invalid phone → 400 "Invalid phone format"
- Out of stock → 400 "Product unavailable"
- Payment failed → 400 "Payment processing failed"

## Test Scenarios
- [ ] Valid checkout with VNPay
- [ ] Valid checkout with COD
- [ ] Invalid phone number
- [ ] Out of stock product
- [ ] Payment gateway timeout
```

### Implementation Validation

```typescript
// ✅ Matches spec exactly
export async function checkout(
  request: CheckoutRequest
): Promise<CheckoutResponse> {
  // Validate phone format
  if (!isValidVietnamesePhone(request.shipping.phone)) {
    throw new ValidationError('Invalid phone format')
  }

  // Check stock
  const cart = await getCart(request.cartId)
  await validateStock(cart.items)

  // Calculate shipping
  const shippingFee = calculateShipping(request.shipping.district)

  // Create order
  const order = await createOrder({
    ...request,
    shippingFee,
    totalAmount: cart.total + shippingFee,
  })

  // Process payment
  let paymentUrl: string | undefined
  if (request.paymentMethod === 'vnpay') {
    paymentUrl = await createVNPayPayment(order)
  }

  // Send email
  await sendOrderConfirmation(order)

  return {
    orderId: order.id,
    totalAmount: order.totalAmount,
    paymentUrl,
  }
}
```

## Best Practices

### Do's
✅ Write spec before code
✅ Define API contract explicitly
✅ List all requirements
✅ Include test scenarios
✅ Review spec with stakeholders
✅ Validate implementation against spec

### Don'ts
❌ Start coding without spec
❌ Change API contract mid-implementation
❌ Skip requirement checklist
❌ Ignore non-functional requirements
❌ Implement features not in spec

## Trade-offs

| Ưu điểm | Nhược điểm |
|---------|------------|
| Clear requirements | Upfront time investment |
| Easier review | Spec can become outdated |
| Better testing | Requires discipline |
| Team alignment | May feel bureaucratic |

## Related Patterns
- [Test-Driven Development](../../6-testing/patterns/pattern-test-driven-validation.md)
- [API Integration Strategy](../../2-planning/templates/api-integration-strategy.md)
