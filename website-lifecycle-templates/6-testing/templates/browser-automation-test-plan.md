# Browser Automation Test Plan

**Project**: [Project Name]  
**Date**: [YYYY-MM-DD]  
**Author**: [Name]  
**Tool**: Playwright | Puppeteer | Cypress

---

## Executive Summary

**Testing Goal**: [Brief description - e.g., "Automate E2E testing for critical e-commerce flows"]

**Coverage Target**: [e.g., "100% of critical user journeys, 80% of secondary flows"]

**Timeline**: [Test development schedule]

---

## Test Scope

### In Scope

**Critical Flows** (Must automate):
- [ ] User registration and login
- [ ] Product search and filtering
- [ ] Add to cart and checkout
- [ ] Payment processing
- [ ] Order confirmation

**Secondary Flows** (Should automate):
- [ ] Wishlist management
- [ ] Product reviews
- [ ] Account settings
- [ ] Password reset

### Out of Scope

- [ ] Admin panel testing (separate suite)
- [ ] Performance testing (use dedicated tools)
- [ ] Security testing (use OWASP ZAP)

---

## Test Environment Setup

### Browser Matrix

| Browser | Version | Platform | Priority |
|---------|---------|----------|----------|
| **Chrome** | Latest | Desktop | P0 |
| **Firefox** | Latest | Desktop | P1 |
| **Safari** | Latest | macOS | P1 |
| **Mobile Chrome** | Latest | Android | P0 |
| **Mobile Safari** | Latest | iOS | P0 |

### Test Data Strategy

**Approach**: [ ] Fixtures | [ ] Factory | [ ] Database Seeding | [ ] API Mocking

**Test Users**:
```typescript
const testUsers = {
  validUser: {
    email: 'test@example.com',
    password: 'Test123!@#',
  },
  adminUser: {
    email: 'admin@example.com',
    password: 'Admin123!@#',
  },
  newUser: {
    email: `test-${Date.now()}@example.com`,
    password: 'Test123!@#',
  },
}
```

**Test Products**:
```typescript
const testProducts = {
  inStock: { id: 'prod_001', name: 'Rose Bouquet', price: 50.00 },
  outOfStock: { id: 'prod_002', name: 'Tulip Arrangement', price: 45.00 },
  onSale: { id: 'prod_003', name: 'Lily Bundle', price: 35.00 },
}
```

---

## Test Architecture

### Project Structure

```
tests/
├── e2e/
│   ├── auth/
│   │   ├── login.spec.ts
│   │   └── register.spec.ts
│   ├── products/
│   │   ├── search.spec.ts
│   │   └── filters.spec.ts
│   ├── cart/
│   │   ├── add-to-cart.spec.ts
│   │   └── checkout.spec.ts
│   └── orders/
│       └── order-flow.spec.ts
├── fixtures/
│   ├── users.json
│   └── products.json
├── page-objects/
│   ├── LoginPage.ts
│   ├── ProductPage.ts
│   └── CheckoutPage.ts
└── utils/
    ├── test-helpers.ts
    └── api-helpers.ts
```

### Page Object Model

```typescript
// page-objects/CheckoutPage.ts
export class CheckoutPage {
  constructor(private page: Page) {}

  async fillShippingInfo(data: ShippingInfo) {
    await this.page.fill('[name="name"]', data.name)
    await this.page.fill('[name="email"]', data.email)
    await this.page.fill('[name="phone"]', data.phone)
    await this.page.fill('[name="address"]', data.address)
  }

  async selectPaymentMethod(method: 'vnpay' | 'cod') {
    await this.page.click(`[value="${method}"]`)
  }

  async placeOrder() {
    await this.page.click('button[type="submit"]')
    await this.page.waitForSelector('.order-success')
  }

  async getOrderId(): Promise<string> {
    const orderIdText = await this.page.textContent('.order-id')
    return orderIdText?.match(/ORD-\d+/)?.[0] || ''
  }
}
```

---

## Test Scenarios

### 1. User Authentication

#### Test: Successful Login

```typescript
test('User can login with valid credentials', async ({ page }) => {
  const loginPage = new LoginPage(page)
  
  await loginPage.goto()
  await loginPage.login('test@example.com', 'Test123!@#')
  
  await expect(page).toHaveURL('/dashboard')
  await expect(page.locator('.user-name')).toHaveText('Test User')
})
```

#### Test: Login Validation

```typescript
test('Show error for invalid credentials', async ({ page }) => {
  const loginPage = new LoginPage(page)
  
  await loginPage.goto()
  await loginPage.login('wrong@example.com', 'wrong')
  
  await expect(page.locator('.error-message')).toHaveText('Invalid credentials')
  await expect(page).toHaveURL('/login')
})
```

### 2. Product Search & Filtering

#### Test: Search Functionality

```typescript
test('Search returns relevant products', async ({ page }) => {
  await page.goto('/')
  
  await page.fill('[name="search"]', 'rose')
  await page.waitForSelector('.search-results')
  
  const results = await page.locator('.product-card').count()
  expect(results).toBeGreaterThan(0)
  
  const firstProduct = await page.locator('.product-card:first-child .product-name').textContent()
  expect(firstProduct?.toLowerCase()).toContain('rose')
})
```

#### Test: Filter by Category

```typescript
test('Filter products by category', async ({ page }) => {
  await page.goto('/products')
  
  await page.click('[data-filter="category-roses"]')
  await page.waitForSelector('.product-card')
  
  const products = await page.locator('.product-card').all()
  
  for (const product of products) {
    const category = await product.getAttribute('data-category')
    expect(category).toBe('roses')
  }
})
```

### 3. Shopping Cart

#### Test: Add to Cart

```typescript
test('Add product to cart', async ({ page }) => {
  await page.goto('/products/rose-bouquet')
  
  await page.click('button:has-text("Add to Cart")')
  
  await expect(page.locator('.cart-notification')).toBeVisible()
  await expect(page.locator('.cart-count')).toHaveText('1')
})
```

#### Test: Update Quantity

```typescript
test('Update cart item quantity', async ({ page }) => {
  // Setup: Add item to cart
  await addToCart(page, 'rose-bouquet')
  
  await page.goto('/cart')
  
  await page.click('.quantity-increase')
  await page.waitForTimeout(500) // Wait for update
  
  await expect(page.locator('.quantity-value')).toHaveText('2')
  await expect(page.locator('.cart-total')).toHaveText('$100.00')
})
```

### 4. Checkout Flow

#### Test: Complete Checkout

```typescript
test('Complete checkout successfully', async ({ page }) => {
  // Setup: Add item to cart
  await addToCart(page, 'rose-bouquet')
  
  await page.goto('/cart')
  await page.click('button:has-text("Checkout")')
  
  // Fill shipping info
  await page.fill('[name="name"]', 'John Doe')
  await page.fill('[name="email"]', 'john@example.com')
  await page.fill('[name="phone"]', '0901234567')
  await page.fill('[name="address"]', '123 Main St, District 1')
  
  // Select payment
  await page.click('[value="vnpay"]')
  
  // Place order
  await page.click('button[type="submit"]')
  
  // Verify success
  await expect(page).toHaveURL(/\/order\/success/)
  await expect(page.locator('.order-success__title')).toBeVisible()
  
  const orderId = await page.locator('.order-id').textContent()
  expect(orderId).toMatch(/ORD-\d{8}/)
})
```

#### Test: Checkout Validation

```typescript
test('Validate required fields', async ({ page }) => {
  await page.goto('/checkout')
  
  await page.click('button[type="submit"]')
  
  await expect(page.locator('.error-name')).toHaveText('Name is required')
  await expect(page.locator('.error-email')).toHaveText('Email is required')
  await expect(page.locator('.error-phone')).toHaveText('Phone is required')
})
```

### 5. Responsive Testing

#### Test: Mobile Navigation

```typescript
test('Mobile menu works correctly', async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 667 })
  await page.goto('/')
  
  await page.click('.hamburger-menu')
  await expect(page.locator('.mobile-nav')).toBeVisible()
  
  await page.click('.mobile-nav a:has-text("Products")')
  await expect(page).toHaveURL('/products')
})
```

#### Test: Mobile Checkout

```typescript
test('Mobile checkout flow', async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 667 })
  
  // Add to cart
  await page.goto('/products/rose-bouquet')
  await page.click('button:has-text("Add to Cart")')
  
  // Navigate to checkout
  await page.click('.cart-icon')
  await page.click('button:has-text("Checkout")')
  
  // Verify mobile layout
  await expect(page.locator('form[name="checkout"]')).toBeVisible()
  
  // Take screenshot
  await page.screenshot({ path: 'mobile-checkout.png' })
})
```

---

## Visual Regression Testing

### Setup

```typescript
// playwright.config.ts
import { defineConfig } from '@playwright/test'

export default defineConfig({
  expect: {
    toHaveScreenshot: {
      maxDiffPixels: 100,
      threshold: 0.2,
    },
  },
})
```

### Test Examples

```typescript
test('Product card visual regression', async ({ page }) => {
  await page.goto('/products')
  
  const productCard = page.locator('.product-card:first-child')
  await expect(productCard).toHaveScreenshot('product-card.png')
})

test('Checkout page visual regression', async ({ page }) => {
  await page.goto('/checkout')
  await expect(page).toHaveScreenshot('checkout-page.png', {
    fullPage: true,
  })
})
```

---

## Error Handling & Edge Cases

### Network Errors

```typescript
test('Handle API timeout gracefully', async ({ page }) => {
  // Simulate slow network
  await page.route('**/api/products', route => {
    setTimeout(() => route.fulfill({ status: 504 }), 5000)
  })
  
  await page.goto('/products')
  
  await expect(page.locator('.error-message')).toHaveText('Failed to load products')
  await expect(page.locator('.retry-button')).toBeVisible()
})
```

### Payment Failures

```typescript
test('Handle payment failure', async ({ page }) => {
  // Mock payment failure
  await page.route('**/api/payment', route => {
    route.fulfill({
      status: 400,
      body: JSON.stringify({ error: 'Payment declined' }),
    })
  })
  
  await completeCheckout(page)
  
  await expect(page.locator('.payment-error')).toHaveText('Payment declined')
  await expect(page).toHaveURL('/checkout')
})
```

### Out of Stock

```typescript
test('Handle out of stock product', async ({ page }) => {
  await page.goto('/products/out-of-stock-item')
  
  await expect(page.locator('.out-of-stock-badge')).toBeVisible()
  await expect(page.locator('button:has-text("Add to Cart")')).toBeDisabled()
})
```

---

## Performance Testing

### Metrics to Track

```typescript
test('Page load performance', async ({ page }) => {
  const startTime = Date.now()
  
  await page.goto('/')
  
  const loadTime = Date.now() - startTime
  expect(loadTime).toBeLessThan(3000) // 3 seconds
})

test('API response time', async ({ page }) => {
  const [response] = await Promise.all([
    page.waitForResponse('**/api/products'),
    page.goto('/products'),
  ])
  
  const timing = response.timing()
  expect(timing.responseEnd - timing.requestStart).toBeLessThan(500)
})
```

---

## Accessibility Testing

### ARIA Labels

```typescript
test('Form inputs have proper labels', async ({ page }) => {
  await page.goto('/checkout')
  
  await expect(page.locator('[name="name"]')).toHaveAttribute('aria-label', 'Full name')
  await expect(page.locator('[name="email"]')).toHaveAttribute('aria-label', 'Email address')
})
```

### Keyboard Navigation

```typescript
test('Checkout form keyboard navigation', async ({ page }) => {
  await page.goto('/checkout')
  
  await page.keyboard.press('Tab') // Focus name
  await page.keyboard.type('John Doe')
  
  await page.keyboard.press('Tab') // Focus email
  await page.keyboard.type('john@example.com')
  
  await page.keyboard.press('Tab') // Focus phone
  await page.keyboard.type('0901234567')
  
  await page.keyboard.press('Enter') // Submit
  
  // Verify submission
  await expect(page.locator('.order-success')).toBeVisible()
})
```

---

## Test Execution Strategy

### Test Prioritization

| Priority | Scenarios | Run Frequency |
|----------|-----------|---------------|
| **P0** | Critical flows (login, checkout) | Every commit |
| **P1** | Secondary flows (wishlist, reviews) | Daily |
| **P2** | Edge cases, visual regression | Weekly |

### Parallel Execution

```typescript
// playwright.config.ts
export default defineConfig({
  workers: process.env.CI ? 2 : 4,
  fullyParallel: true,
  retries: process.env.CI ? 2 : 0,
})
```

### Test Sharding (CI)

```yaml
# .github/workflows/test.yml
strategy:
  matrix:
    shard: [1, 2, 3, 4]
steps:
  - run: npx playwright test --shard=${{ matrix.shard }}/4
```

---

## Reporting & Monitoring

### Test Reports

```typescript
// playwright.config.ts
export default defineConfig({
  reporter: [
    ['html', { outputFolder: 'test-results/html' }],
    ['json', { outputFile: 'test-results/results.json' }],
    ['junit', { outputFile: 'test-results/junit.xml' }],
  ],
})
```

### Failure Screenshots

```typescript
test('Capture screenshot on failure', async ({ page }, testInfo) => {
  try {
    await page.goto('/checkout')
    await page.click('button[type="submit"]')
    // ... test logic
  } catch (error) {
    await page.screenshot({
      path: `test-results/failure-${testInfo.title}.png`,
      fullPage: true,
    })
    throw error
  }
})
```

### Metrics Dashboard

Track:
- [ ] Test pass rate (target: >95%)
- [ ] Test execution time (target: <10 min)
- [ ] Flaky test rate (target: <5%)
- [ ] Code coverage (target: >80%)

---

## Maintenance Strategy

### Test Stability

**Avoid**:
- Hard-coded waits (`page.waitForTimeout(5000)`)
- Brittle selectors (`nth-child`, absolute XPath)
- Test interdependencies

**Prefer**:
- Smart waits (`page.waitForSelector`, `page.waitForResponse`)
- Semantic selectors (`role`, `text`, `data-testid`)
- Independent, isolated tests

### Flaky Test Handling

```typescript
test('Retry flaky test', async ({ page }) => {
  test.setTimeout(30000) // Increase timeout
  
  await page.goto('/', { waitUntil: 'networkidle' })
  
  // Use retry logic
  await expect(async () => {
    const count = await page.locator('.product-card').count()
    expect(count).toBeGreaterThan(0)
  }).toPass({ timeout: 10000 })
})
```

---

## CI/CD Integration

### GitHub Actions Example

```yaml
name: E2E Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: pnpm install
      - run: npx playwright install --with-deps
      - run: pnpm test:e2e
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: test-results
          path: test-results/
```

---

## Success Criteria

**Test Coverage**:
- [ ] 100% of P0 scenarios automated
- [ ] 80% of P1 scenarios automated
- [ ] All critical user journeys covered

**Test Quality**:
- [ ] Pass rate >95%
- [ ] Execution time <10 minutes
- [ ] Flaky rate <5%
- [ ] Zero false positives

**Maintenance**:
- [ ] Tests updated with feature changes
- [ ] Flaky tests fixed within 24 hours
- [ ] Test documentation up to date

---

## Appendix

### Useful Commands

```bash
# Run all tests
npx playwright test

# Run specific test file
npx playwright test tests/e2e/checkout.spec.ts

# Run in headed mode
npx playwright test --headed

# Debug mode
npx playwright test --debug

# Generate report
npx playwright show-report

# Update snapshots
npx playwright test --update-snapshots
```

### Resources

- Playwright Docs: https://playwright.dev
- Best Practices: https://playwright.dev/docs/best-practices
- Selectors Guide: https://playwright.dev/docs/selectors

---

**Template Version**: 1.0  
**Last Updated**: 2026-04-23
