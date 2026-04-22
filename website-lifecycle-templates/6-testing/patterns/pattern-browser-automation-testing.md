# Pattern: Browser Automation Testing

## Nguồn
- Cline
- Puppeteer
- Playwright

## Mô tả
Automated UI testing với browser automation tools. Puppeteer-controlled validation với screenshots, coordinate-based interaction.

## Khi nào dùng
- Testing: E2E testing cho critical flows
- QA: Visual regression testing
- Debugging: Reproduce user-reported bugs
- Monitoring: Production smoke tests

## Cách áp dụng

### 1. Basic Browser Automation

```typescript
import puppeteer from 'puppeteer'

async function testCheckoutFlow() {
  const browser = await puppeteer.launch({ headless: false })
  const page = await browser.newPage()
  
  try {
    // 1. Navigate to product page
    await page.goto('http://localhost:3000/products/rose-bouquet')
    await page.screenshot({ path: 'step1-product-page.png' })
    
    // 2. Add to cart
    await page.click('button:has-text("Add to Cart")')
    await page.waitForSelector('.cart-notification')
    await page.screenshot({ path: 'step2-added-to-cart.png' })
    
    // 3. Go to cart
    await page.click('a[href="/cart"]')
    await page.waitForSelector('.cart-item')
    await page.screenshot({ path: 'step3-cart-page.png' })
    
    // 4. Proceed to checkout
    await page.click('button:has-text("Checkout")')
    await page.waitForSelector('form[name="checkout"]')
    
    // 5. Fill shipping info
    await page.type('input[name="name"]', 'John Doe')
    await page.type('input[name="phone"]', '0901234567')
    await page.type('textarea[name="address"]', '123 Main St, District 1')
    await page.screenshot({ path: 'step4-shipping-info.png' })
    
    // 6. Select payment method
    await page.click('input[value="vnpay"]')
    
    // 7. Place order
    await page.click('button[type="submit"]')
    await page.waitForSelector('.order-success')
    await page.screenshot({ path: 'step5-order-success.png' })
    
    // 8. Verify order ID
    const orderIdElement = await page.$('.order-id')
    const orderIdText = await orderIdElement?.textContent()
    
    console.log('✅ Checkout flow completed:', orderIdText)
    
  } catch (error) {
    await page.screenshot({ path: 'error-screenshot.png' })
    throw error
  } finally {
    await browser.close()
  }
}
```

### 2. Coordinate-Based Interaction

```typescript
// Click at specific coordinates
await page.mouse.click(x, y)

// Scroll to position
await page.evaluate(() => {
  window.scrollTo(0, 500)
})

// Drag and drop
await page.mouse.move(startX, startY)
await page.mouse.down()
await page.mouse.move(endX, endY)
await page.mouse.up()
```

### 3. Visual Regression Testing

```typescript
import { toMatchImageSnapshot } from 'jest-image-snapshot'

expect.extend({ toMatchImageSnapshot })

test('Product card visual regression', async () => {
  const page = await browser.newPage()
  await page.goto('http://localhost:3000/products')
  
  // Take screenshot
  const screenshot = await page.screenshot({
    clip: {
      x: 0,
      y: 0,
      width: 400,
      height: 600,
    },
  })
  
  // Compare with baseline
  expect(screenshot).toMatchImageSnapshot({
    failureThreshold: 0.01,
    failureThresholdType: 'percent',
  })
})
```

## Ví dụ thực tế

### E-commerce: Test Complete Checkout Flow

```typescript
// tests/e2e/checkout.spec.ts
import { test, expect } from '@playwright/test'

test.describe('Checkout Flow', () => {
  test('should complete checkout successfully', async ({ page }) => {
    // 1. Add product to cart
    await page.goto('/products/rose-bouquet')
    await page.click('button:has-text("Add to Cart")')
    
    // Verify cart notification
    await expect(page.locator('.cart-notification')).toBeVisible()
    await expect(page.locator('.cart-count')).toHaveText('1')
    
    // 2. Go to cart
    await page.click('a[href="/cart"]')
    await expect(page.locator('.cart-item')).toHaveCount(1)
    
    // Verify product details
    await expect(page.locator('.cart-item__name')).toHaveText('Rose Bouquet')
    await expect(page.locator('.cart-item__price')).toHaveText('500,000đ')
    
    // 3. Proceed to checkout
    await page.click('button:has-text("Checkout")')
    await expect(page).toHaveURL('/checkout')
    
    // 4. Fill shipping information
    await page.fill('input[name="name"]', 'John Doe')
    await page.fill('input[name="email"]', 'john@example.com')
    await page.fill('input[name="phone"]', '0901234567')
    await page.fill('textarea[name="address"]', '123 Main St, District 1, HCMC')
    
    // 5. Select payment method
    await page.click('input[value="vnpay"]')
    
    // 6. Review order summary
    await expect(page.locator('.order-summary__subtotal')).toHaveText('500,000đ')
    await expect(page.locator('.order-summary__shipping')).toHaveText('30,000đ')
    await expect(page.locator('.order-summary__total')).toHaveText('530,000đ')
    
    // 7. Place order
    await page.click('button[type="submit"]')
    
    // 8. Verify success page
    await expect(page).toHaveURL(/\/order\/success/)
    await expect(page.locator('.order-success__title')).toBeVisible()
    
    // 9. Verify order ID format
    const orderIdText = await page.locator('.order-id').textContent()
    expect(orderIdText).toMatch(/ORD-\d{8}/)
    
    // 10. Take screenshot for documentation
    await page.screenshot({ path: 'checkout-success.png', fullPage: true })
  })
  
  test('should validate required fields', async ({ page }) => {
    await page.goto('/checkout')
    
    // Try to submit without filling
    await page.click('button[type="submit"]')
    
    // Verify error messages
    await expect(page.locator('.error-name')).toHaveText('Name is required')
    await expect(page.locator('.error-phone')).toHaveText('Phone is required')
    await expect(page.locator('.error-address')).toHaveText('Address is required')
  })
  
  test('should handle payment failure gracefully', async ({ page }) => {
    // Mock payment failure
    await page.route('**/api/payment', (route) => {
      route.fulfill({
        status: 400,
        body: JSON.stringify({ error: 'Payment failed' }),
      })
    })
    
    await page.goto('/checkout')
    // ... fill form ...
    await page.click('button[type="submit"]')
    
    // Verify error message
    await expect(page.locator('.payment-error')).toBeVisible()
    await expect(page.locator('.payment-error')).toHaveText('Payment failed. Please try again.')
  })
})
```

### E-commerce: Test Product Search

```typescript
test('Product search functionality', async ({ page }) => {
  await page.goto('/')
  
  // 1. Type in search box
  await page.fill('input[name="search"]', 'rose')
  
  // 2. Wait for autocomplete
  await page.waitForSelector('.search-suggestions')
  
  // 3. Verify suggestions
  const suggestions = await page.locator('.search-suggestion').count()
  expect(suggestions).toBeGreaterThan(0)
  
  // 4. Click first suggestion
  await page.click('.search-suggestion:first-child')
  
  // 5. Verify results page
  await expect(page).toHaveURL(/\/search\?q=rose/)
  await expect(page.locator('.product-card')).toHaveCount(5)
})
```

### E-commerce: Mobile Responsive Testing

```typescript
test('Mobile checkout flow', async ({ page }) => {
  // Set mobile viewport
  await page.setViewportSize({ width: 375, height: 667 })
  
  await page.goto('/products/rose-bouquet')
  
  // Verify mobile layout
  await expect(page.locator('.product-image')).toBeVisible()
  await expect(page.locator('.product-details')).toBeVisible()
  
  // Test mobile navigation
  await page.click('.hamburger-menu')
  await expect(page.locator('.mobile-nav')).toBeVisible()
  
  // Complete checkout on mobile
  await page.click('button:has-text("Add to Cart")')
  await page.click('.cart-icon')
  await page.click('button:has-text("Checkout")')
  
  // Verify mobile form layout
  await expect(page.locator('form[name="checkout"]')).toBeVisible()
  
  // Take mobile screenshot
  await page.screenshot({ path: 'mobile-checkout.png' })
})
```

## Best Practices

### Do's
✅ Take screenshots at each step
✅ Wait for elements before interacting
✅ Use semantic selectors (text, role)
✅ Test critical user flows
✅ Run tests in CI/CD
✅ Test on multiple browsers

### Don'ts
❌ Use brittle selectors (nth-child)
❌ Hard-code wait times (use waitFor)
❌ Skip error scenarios
❌ Test everything (focus on critical)
❌ Ignore flaky tests

## Trade-offs

| Ưu điểm | Nhược điểm |
|---------|------------|
| Catch UI bugs early | Slower than unit tests |
| Test real user flows | Flaky if not written well |
| Visual regression detection | Requires maintenance |
| Cross-browser testing | Resource intensive |

## Related Patterns
- [Test-Driven Validation](../../6-testing/patterns/pattern-test-driven-validation.md)
- [Debug Logging](../../6-testing/patterns/pattern-debug-logging.md)
