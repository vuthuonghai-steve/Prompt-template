# Pattern: SEARCH/REPLACE Block Editing

## Nguồn
- Aider
- Cursor
- Claude Code

## Mô tả
Structured code editing using SEARCH/REPLACE blocks for precise, reviewable changes. Clear separation between what to find and what to replace it with.

## Khi nào dùng
- Precise code modifications
- Refactoring with clear intent
- Multi-location changes
- Reviewable edits
- Avoiding ambiguous edits

## Cách áp dụng

### 1. SEARCH/REPLACE Format

```
<<<<<<< SEARCH
[exact code to find]
=======
[exact code to replace with]
>>>>>>> REPLACE
```

### 2. Basic Example

```typescript
<<<<<<< SEARCH
function calculateTotal(items) {
  return items.reduce((sum, item) => sum + item.price, 0)
}
=======
function calculateTotal(items: CartItem[]): number {
  return items.reduce((sum, item) => sum + item.price * item.quantity, 0)
}
>>>>>>> REPLACE
```

### 3. Multiple Changes in One File

```typescript
// File: src/services/order/service.order.ts

<<<<<<< SEARCH
import { Order } from '@/types/order'
=======
import { Order, OrderStatus } from '@/types/order'
import { logger } from '@/utils/logger'
>>>>>>> REPLACE

<<<<<<< SEARCH
async createOrder(data: CreateOrderData) {
  const order = await db.orders.create(data)
  return order
}
=======
async createOrder(data: CreateOrderData): Promise<Order> {
  logger.info('Creating order', { data })
  
  const order = await db.orders.create({
    ...data,
    status: OrderStatus.PENDING,
    createdAt: new Date()
  })
  
  logger.info('Order created', { orderId: order.id })
  return order
}
>>>>>>> REPLACE
```

## Ví dụ thực tế

### E-commerce: Add Type Safety

```typescript
// File: src/hooks/use-cart/hook.use-cart.ts

<<<<<<< SEARCH
export function useCart() {
  const [cart, setCart] = useState([])
  
  const addItem = (product) => {
    setCart([...cart, product])
  }
  
  return { cart, addItem }
}
=======
export function useCart() {
  const [cart, setCart] = useState<CartItem[]>([])
  
  const addItem = (product: Product) => {
    const cartItem: CartItem = {
      id: product.id,
      name: product.name,
      price: product.price,
      quantity: 1
    }
    setCart([...cart, cartItem])
  }
  
  return { cart, addItem }
}
>>>>>>> REPLACE
```

### E-commerce: Refactor API Endpoint

```typescript
// File: src/services/product/service.product.ts

<<<<<<< SEARCH
async getProducts(filters) {
  const response = await fetch('/api/v1/products?' + new URLSearchParams(filters))
  return response.json()
}
=======
async getProducts(filters?: ProductFilters): Promise<ProductListResponse> {
  const params = this.buildQueryParams(filters)
  const response = await apiClient.get<ProductListResponse>(
    ENDPOINTS.PRODUCTS.LIST,
    { params }
  )
  return response.data
}
>>>>>>> REPLACE

<<<<<<< SEARCH
async getProductById(id) {
  const response = await fetch(`/api/v1/products/${id}`)
  return response.json()
}
=======
async getProductById(id: string): Promise<Product> {
  const response = await apiClient.get<Product>(
    ENDPOINTS.PRODUCTS.DETAIL(id)
  )
  return response.data
}
>>>>>>> REPLACE
```

### E-commerce: Add Error Handling

```typescript
// File: src/screens/Checkout/CheckoutScreen.tsx

<<<<<<< SEARCH
const handleSubmit = async (data) => {
  const order = await OrderService.createOrder(data)
  navigate(`/order/success/${order.id}`)
}
=======
const handleSubmit = async (data: CheckoutFormData) => {
  try {
    setIsLoading(true)
    setError(null)
    
    const order = await OrderService.createOrder(data)
    
    toast.success('Order placed successfully!')
    navigate(`/order/success/${order.id}`)
  } catch (err) {
    const error = err as ApiError
    setError(error.message)
    toast.error('Failed to place order')
  } finally {
    setIsLoading(false)
  }
}
>>>>>>> REPLACE
```

### E-commerce: Update Component Props

```typescript
// File: src/components/ProductCard/ProductCard.tsx

<<<<<<< SEARCH
interface ProductCardProps {
  product: any
  onAddToCart: (product: any) => void
}

export function ProductCard({ product, onAddToCart }: ProductCardProps) {
  return (
    <div className="product-card">
      <img src={product.image} alt={product.name} />
      <h3>{product.name}</h3>
      <p>{product.price}</p>
      <button onClick={() => onAddToCart(product)}>
        Add to Cart
      </button>
    </div>
  )
}
=======
interface ProductCardProps {
  product: Product
  onAddToCart: (product: Product) => void
  variant?: 'default' | 'compact'
}

export function ProductCard({ 
  product, 
  onAddToCart,
  variant = 'default' 
}: ProductCardProps) {
  return (
    <div className={cn('product-card', `product-card--${variant}`)}>
      <img 
        src={product.image} 
        alt={product.name}
        loading="lazy"
      />
      <h3 className="product-card__name">{product.name}</h3>
      <p className="product-card__price">
        {formatCurrency(product.price)}
      </p>
      <Button 
        onClick={() => onAddToCart(product)}
        disabled={product.stock === 0}
      >
        {product.stock > 0 ? 'Add to Cart' : 'Out of Stock'}
      </Button>
    </div>
  )
}
>>>>>>> REPLACE
```

## Best Practices

### Rule 1: Exact Match Required

```typescript
// ❌ WRONG: Partial match
<<<<<<< SEARCH
function calculateTotal
=======
function calculateTotal(items: CartItem[]): number
>>>>>>> REPLACE

// ✅ CORRECT: Complete function
<<<<<<< SEARCH
function calculateTotal(items) {
  return items.reduce((sum, item) => sum + item.price, 0)
}
=======
function calculateTotal(items: CartItem[]): number {
  return items.reduce((sum, item) => sum + item.price * item.quantity, 0)
}
>>>>>>> REPLACE
```

### Rule 2: Include Context

```typescript
// ❌ WRONG: Ambiguous
<<<<<<< SEARCH
const total = 0
=======
const total = calculateTotal(items)
>>>>>>> REPLACE

// ✅ CORRECT: With context
<<<<<<< SEARCH
export function CartSummary({ items }: CartSummaryProps) {
  const total = 0
  
  return <div>Total: {total}</div>
}
=======
export function CartSummary({ items }: CartSummaryProps) {
  const total = calculateTotal(items)
  
  return <div>Total: {formatCurrency(total)}</div>
}
>>>>>>> REPLACE
```

### Rule 3: Preserve Indentation

```typescript
// ✅ CORRECT: Match exact indentation
<<<<<<< SEARCH
  async createOrder(data: CreateOrderData) {
    const order = await db.orders.create(data)
    return order
  }
=======
  async createOrder(data: CreateOrderData): Promise<Order> {
    logger.info('Creating order', { data })
    const order = await db.orders.create(data)
    logger.info('Order created', { orderId: order.id })
    return order
  }
>>>>>>> REPLACE
```

### Rule 4: One Logical Change Per Block

```typescript
// ❌ WRONG: Multiple unrelated changes
<<<<<<< SEARCH
function processOrder(order) {
  validateOrder(order)
  const total = calculateTotal(order.items)
  return { ...order, total }
}
=======
async function processOrder(order: Order): Promise<ProcessedOrder> {
  await validateOrder(order)
  const total = calculateTotal(order.items)
  const shipping = calculateShipping(order.address)
  await sendNotification(order.userId)
  return { ...order, total, shipping }
}
>>>>>>> REPLACE

// ✅ CORRECT: Separate logical changes
<<<<<<< SEARCH
function processOrder(order) {
  validateOrder(order)
  const total = calculateTotal(order.items)
  return { ...order, total }
}
=======
async function processOrder(order: Order): Promise<ProcessedOrder> {
  await validateOrder(order)
  const total = calculateTotal(order.items)
  return { ...order, total }
}
>>>>>>> REPLACE

<<<<<<< SEARCH
async function processOrder(order: Order): Promise<ProcessedOrder> {
  await validateOrder(order)
  const total = calculateTotal(order.items)
  return { ...order, total }
}
=======
async function processOrder(order: Order): Promise<ProcessedOrder> {
  await validateOrder(order)
  const total = calculateTotal(order.items)
  const shipping = calculateShipping(order.address)
  return { ...order, total, shipping }
}
>>>>>>> REPLACE
```

## Advantages Over Direct Edit

### Reviewability

```typescript
// SEARCH/REPLACE: Clear intent
<<<<<<< SEARCH
const price = product.price
=======
const price = product.salePrice || product.price
>>>>>>> REPLACE

// vs Direct Edit: Less clear what changed
Edit('file.ts', 'const price = product.salePrice || product.price')
```

### Safety

```typescript
// SEARCH/REPLACE: Fails if code changed
<<<<<<< SEARCH
function oldImplementation() {
  // exact code
}
=======
function newImplementation() {
  // new code
}
>>>>>>> REPLACE

// vs Direct Edit: May apply to wrong location
```

### Documentation

```typescript
// SEARCH/REPLACE: Shows before/after
// Easy to understand what changed and why

// vs Direct Edit: Only shows final state
// Harder to review intent
```

## Common Patterns

### Pattern 1: Add Import

```typescript
<<<<<<< SEARCH
import { useState } from 'react'
=======
import { useState, useEffect } from 'react'
>>>>>>> REPLACE
```

### Pattern 2: Add Type Annotation

```typescript
<<<<<<< SEARCH
const [cart, setCart] = useState([])
=======
const [cart, setCart] = useState<CartItem[]>([])
>>>>>>> REPLACE
```

### Pattern 3: Wrap with Try-Catch

```typescript
<<<<<<< SEARCH
const result = await apiCall()
return result
=======
try {
  const result = await apiCall()
  return result
} catch (error) {
  logger.error('API call failed', error)
  throw error
}
>>>>>>> REPLACE
```

### Pattern 4: Extract Constant

```typescript
<<<<<<< SEARCH
if (order.total > 1000000) {
  applyDiscount(order)
}
=======
const FREE_SHIPPING_THRESHOLD = 1000000

if (order.total > FREE_SHIPPING_THRESHOLD) {
  applyDiscount(order)
}
>>>>>>> REPLACE
```

## Integration with Tools

### Aider Format

```bash
# Aider uses this format natively
aider --message "Add type safety to cart hook"

# Aider generates SEARCH/REPLACE blocks
# User reviews and approves
```

### Claude Code Pattern

```typescript
// Claude Code: Use Edit tool with clear before/after
Edit('file.ts', {
  old_string: `function calculate(x) { return x * 2 }`,
  new_string: `function calculate(x: number): number { return x * 2 }`
})
```

## Best Practices

### Do's
✅ Include enough context for unique match
✅ Preserve exact indentation
✅ One logical change per block
✅ Show complete before/after
✅ Use for reviewable changes
✅ Fail fast if code changed

### Don'ts
❌ Use partial matches
❌ Mix multiple unrelated changes
❌ Ignore whitespace
❌ Make ambiguous edits
❌ Skip context lines
❌ Assume code hasn't changed

## Trade-offs

| Ưu điểm | Nhược điểm |
|---------|------------|
| Clear intent | More verbose |
| Reviewable | Requires exact match |
| Safe (fails if changed) | Can't handle fuzzy matches |
| Self-documenting | More typing |

## Related Patterns
- [Tool Use Sequencing](./pattern-tool-use-sequencing.md)
- [Linter-Driven Recovery](./pattern-linter-driven-recovery.md)
