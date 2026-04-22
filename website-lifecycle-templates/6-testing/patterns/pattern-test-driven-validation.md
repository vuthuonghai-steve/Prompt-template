# Pattern: Test-Driven Validation

## Nguồn
- Claude Code
- Cursor Agent
- Windsurf Cascade

## Mô tả
Write tests trước khi implement features. Tests define expected behavior, guide implementation, catch regressions.

## Khi nào dùng
- Testing: mọi feature mới
- Development: TDD workflow
- Refactoring: ensure no regressions
- Bug fixing: reproduce bug first

## Cách áp dụng

### 1. TDD Cycle (Red-Green-Refactor)
```typescript
// 1. RED: Write failing test
describe('Cart', () => {
  it('should add product to cart', () => {
    const cart = new Cart()
    const product = { id: '1', name: 'Rose', price: 50000 }
    
    cart.add(product)
    
    expect(cart.items).toHaveLength(1)
    expect(cart.items[0]).toEqual(product)
  })
})

// 2. GREEN: Implement minimal code to pass
class Cart {
  items: Product[] = []
  
  add(product: Product) {
    this.items.push(product)
  }
}

// 3. REFACTOR: Improve code quality
class Cart {
  private items: Product[] = []
  
  add(product: Product): void {
    this.items.push(product)
  }
  
  getItems(): Product[] {
    return [...this.items]
  }
}
```

### 2. Test Structure (AAA Pattern)
```typescript
describe('ProductService', () => {
  it('should fetch product by id', async () => {
    // ARRANGE: Setup
    const productId = '123'
    const mockProduct = {
      id: productId,
      name: 'Rose Bouquet',
      price: 500000,
    }
    
    jest.spyOn(api, 'get').mockResolvedValue(mockProduct)
    
    // ACT: Execute
    const result = await productService.getProduct(productId)
    
    // ASSERT: Verify
    expect(result).toEqual(mockProduct)
    expect(api.get).toHaveBeenCalledWith(`/products/${productId}`)
  })
})
```

### 3. Test Coverage
```typescript
// Aim for high coverage, but focus on critical paths
interface CoverageMetrics {
  statements: number  // % of statements executed
  branches: number    // % of branches taken
  functions: number   // % of functions called
  lines: number       // % of lines executed
}

// Target coverage
const targetCoverage: CoverageMetrics = {
  statements: 80,
  branches: 75,
  functions: 80,
  lines: 80,
}
```

## Ví dụ thực tế

### E-commerce Cart Tests

```typescript
// cart.test.ts
describe('Cart', () => {
  let cart: Cart
  
  beforeEach(() => {
    cart = new Cart()
  })
  
  describe('add', () => {
    it('should add product to empty cart', () => {
      const product = createMockProduct()
      
      cart.add(product)
      
      expect(cart.getItems()).toHaveLength(1)
      expect(cart.getTotal()).toBe(product.price)
    })
    
    it('should increment quantity if product already exists', () => {
      const product = createMockProduct()
      
      cart.add(product)
      cart.add(product)
      
      expect(cart.getItems()).toHaveLength(1)
      expect(cart.getItems()[0].quantity).toBe(2)
    })
    
    it('should throw error if product is out of stock', () => {
      const product = createMockProduct({ inStock: false })
      
      expect(() => cart.add(product)).toThrow('Product out of stock')
    })
  })
  
  describe('remove', () => {
    it('should remove product from cart', () => {
      const product = createMockProduct()
      cart.add(product)
      
      cart.remove(product.id)
      
      expect(cart.getItems()).toHaveLength(0)
    })
    
    it('should throw error if product not in cart', () => {
      expect(() => cart.remove('invalid-id')).toThrow('Product not found')
    })
  })
  
  describe('applyVoucher', () => {
    it('should apply percentage discount', () => {
      const product = createMockProduct({ price: 100000 })
      cart.add(product)
      
      const voucher = { type: 'percentage', value: 10 }
      cart.applyVoucher(voucher)
      
      expect(cart.getTotal()).toBe(90000)
    })
    
    it('should apply fixed discount', () => {
      const product = createMockProduct({ price: 100000 })
      cart.add(product)
      
      const voucher = { type: 'fixed', value: 20000 }
      cart.applyVoucher(voucher)
      
      expect(cart.getTotal()).toBe(80000)
    })
    
    it('should not apply discount below minimum order', () => {
      const product = createMockProduct({ price: 50000 })
      cart.add(product)
      
      const voucher = { 
        type: 'percentage', 
        value: 10,
        minOrder: 100000,
      }
      
      expect(() => cart.applyVoucher(voucher)).toThrow(
        'Minimum order not met'
      )
    })
  })
})
```

### API Integration Tests

```typescript
// product-api.test.ts
describe('ProductAPI', () => {
  let api: ProductAPI
  
  beforeEach(() => {
    api = new ProductAPI()
  })
  
  describe('getProducts', () => {
    it('should fetch products with filters', async () => {
      const filters = {
        category: 'roses',
        minPrice: 50000,
        maxPrice: 100000,
      }
      
      const products = await api.getProducts(filters)
      
      expect(products).toBeInstanceOf(Array)
      products.forEach((product) => {
        expect(product.category).toBe('roses')
        expect(product.price).toBeGreaterThanOrEqual(50000)
        expect(product.price).toBeLessThanOrEqual(100000)
      })
    })
    
    it('should handle empty results', async () => {
      const filters = { category: 'nonexistent' }
      
      const products = await api.getProducts(filters)
      
      expect(products).toEqual([])
    })
    
    it('should handle API errors', async () => {
      jest.spyOn(global, 'fetch').mockRejectedValue(
        new Error('Network error')
      )
      
      await expect(api.getProducts({})).rejects.toThrow('Network error')
    })
  })
  
  describe('createProduct', () => {
    it('should create product with valid data', async () => {
      const productData = {
        name: 'Red Rose',
        price: 50000,
        category: 'roses',
      }
      
      const product = await api.createProduct(productData)
      
      expect(product).toMatchObject(productData)
      expect(product.id).toBeDefined()
      expect(product.createdAt).toBeDefined()
    })
    
    it('should validate required fields', async () => {
      const invalidData = { name: 'Rose' } // Missing price
      
      await expect(api.createProduct(invalidData)).rejects.toThrow(
        'Price is required'
      )
    })
  })
})
```

### Component Tests (React)

```typescript
// ProductCard.test.tsx
import { render, screen, fireEvent } from '@testing-library/react'

describe('ProductCard', () => {
  const mockProduct = {
    id: '1',
    name: 'Rose Bouquet',
    price: 500000,
    image: '/roses.jpg',
  }
  
  it('should render product information', () => {
    render(<ProductCard product={mockProduct} />)
    
    expect(screen.getByText('Rose Bouquet')).toBeInTheDocument()
    expect(screen.getByText('500,000đ')).toBeInTheDocument()
    expect(screen.getByAltText('Rose Bouquet')).toHaveAttribute(
      'src',
      '/roses.jpg'
    )
  })
  
  it('should call onAddToCart when button clicked', () => {
    const onAddToCart = jest.fn()
    
    render(
      <ProductCard product={mockProduct} onAddToCart={onAddToCart} />
    )
    
    const button = screen.getByText('Add to Cart')
    fireEvent.click(button)
    
    expect(onAddToCart).toHaveBeenCalledWith(mockProduct.id)
  })
  
  it('should show out of stock message', () => {
    const outOfStockProduct = { ...mockProduct, inStock: false }
    
    render(<ProductCard product={outOfStockProduct} />)
    
    expect(screen.getByText('Out of Stock')).toBeInTheDocument()
    expect(screen.getByText('Add to Cart')).toBeDisabled()
  })
})
```

### E2E Tests (Playwright)

```typescript
// checkout.spec.ts
import { test, expect } from '@playwright/test'

test.describe('Checkout Flow', () => {
  test('should complete checkout successfully', async ({ page }) => {
    // 1. Add product to cart
    await page.goto('/products/rose-bouquet')
    await page.click('button:has-text("Add to Cart")')
    
    // 2. Go to cart
    await page.click('a:has-text("Cart")')
    await expect(page.locator('.cart-item')).toHaveCount(1)
    
    // 3. Proceed to checkout
    await page.click('button:has-text("Checkout")')
    
    // 4. Fill shipping info
    await page.fill('input[name="name"]', 'John Doe')
    await page.fill('input[name="phone"]', '0901234567')
    await page.fill('textarea[name="address"]', '123 Main St')
    
    // 5. Select payment method
    await page.click('input[value="vnpay"]')
    
    // 6. Place order
    await page.click('button:has-text("Place Order")')
    
    // 7. Verify success
    await expect(page.locator('.order-success')).toBeVisible()
    await expect(page.locator('.order-id')).toContainText(/ORD-\d+/)
  })
  
  test('should validate required fields', async ({ page }) => {
    await page.goto('/checkout')
    
    // Try to submit without filling
    await page.click('button:has-text("Place Order")')
    
    // Verify error messages
    await expect(page.locator('.error-name')).toContainText(
      'Name is required'
    )
    await expect(page.locator('.error-phone')).toContainText(
      'Phone is required'
    )
  })
})
```

## Test-Driven Validation Checklist

### Unit Tests
- [ ] Test happy path
- [ ] Test edge cases
- [ ] Test error handling
- [ ] Test boundary conditions
- [ ] Mock external dependencies

### Integration Tests
- [ ] Test API endpoints
- [ ] Test database operations
- [ ] Test third-party integrations
- [ ] Test authentication/authorization

### E2E Tests
- [ ] Test critical user flows
- [ ] Test cross-browser compatibility
- [ ] Test mobile responsiveness
- [ ] Test performance

## Trade-offs

| Ưu điểm | Nhược điểm |
|---------|------------|
| Catch bugs early | Upfront time investment |
| Better design | Maintenance overhead |
| Confidence to refactor | Can be over-tested |

## Best Practices
1. **Write tests first**: Define behavior before implementation
2. **Test behavior, not implementation**: Focus on what, not how
3. **Keep tests simple**: One assertion per test
4. **Use descriptive names**: Test name = documentation
5. **Arrange-Act-Assert**: Clear test structure
6. **Mock external dependencies**: Isolate unit under test

## Anti-patterns
- ❌ Test implementation details
- ❌ Flaky tests (random failures)
- ❌ Slow tests (> 1s per test)
- ❌ No test coverage
- ❌ Tests that don't fail when code breaks

## Related Patterns
- [Debug Logging](./pattern-debug-logging.md)
