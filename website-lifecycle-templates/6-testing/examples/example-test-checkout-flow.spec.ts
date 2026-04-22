/**
 * E2E Test: Checkout Flow
 * Framework: Playwright
 * Context: E-commerce flower shop
 */

import { test, expect } from '@playwright/test'

test.describe('Checkout Flow - Happy Path', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to homepage
    await page.goto('https://siinstore.com')

    // Accept cookies if banner appears
    const cookieBanner = page.locator('[data-testid="cookie-banner"]')
    if (await cookieBanner.isVisible()) {
      await page.click('[data-testid="accept-cookies"]')
    }
  })

  test('Complete checkout flow: Browse → Add to Cart → Checkout → Payment', async ({ page }) => {
    // Step 1: Browse products
    await test.step('Browse flower products', async () => {
      await page.click('text=Shop Flowers')
      await expect(page).toHaveURL(/.*\/products/)

      // Wait for products to load
      await page.waitForSelector('[data-testid="product-card"]')

      // Verify products are displayed
      const productCount = await page.locator('[data-testid="product-card"]').count()
      expect(productCount).toBeGreaterThan(0)
    })

    // Step 2: Filter by occasion
    await test.step('Filter by Birthday occasion', async () => {
      await page.click('[data-testid="filter-occasion"]')
      await page.click('text=Birthday')

      // Wait for filtered results
      await page.waitForTimeout(1000)

      // Verify filter applied
      const filterBadge = page.locator('[data-testid="active-filter"]')
      await expect(filterBadge).toContainText('Birthday')
    })

    // Step 3: Select product
    await test.step('Select "Rose Bouquet" product', async () => {
      await page.click('[data-testid="product-card"]:has-text("Rose Bouquet")').first()
      await expect(page).toHaveURL(/.*\/products\/rose-bouquet/)

      // Verify product details
      await expect(page.locator('h1')).toContainText('Rose Bouquet')
      await expect(page.locator('[data-testid="product-price"]')).toBeVisible()
    })

    // Step 4: Add to cart
    await test.step('Add product to cart', async () => {
      // Select quantity
      await page.selectOption('[data-testid="quantity-select"]', '2')

      // Add to cart
      await page.click('[data-testid="add-to-cart-btn"]')

      // Verify success notification
      await expect(page.locator('[data-testid="toast-success"]')).toContainText('Added to cart')

      // Verify cart badge updated
      const cartBadge = page.locator('[data-testid="cart-badge"]')
      await expect(cartBadge).toContainText('2')
    })

    // Step 5: View cart
    await test.step('View shopping cart', async () => {
      await page.click('[data-testid="cart-icon"]')
      await expect(page).toHaveURL(/.*\/cart/)

      // Verify cart items
      const cartItems = page.locator('[data-testid="cart-item"]')
      await expect(cartItems).toHaveCount(1)

      // Verify product details in cart
      await expect(cartItems.first()).toContainText('Rose Bouquet')
      await expect(cartItems.first()).toContainText('Quantity: 2')

      // Verify subtotal
      const subtotal = page.locator('[data-testid="cart-subtotal"]')
      await expect(subtotal).toBeVisible()
    })

    // Step 6: Proceed to checkout
    await test.step('Proceed to checkout', async () => {
      await page.click('[data-testid="checkout-btn"]')
      await expect(page).toHaveURL(/.*\/checkout/)
    })

    // Step 7: Fill shipping information
    await test.step('Fill shipping information', async () => {
      await page.fill('[name="fullName"]', 'Nguyen Van A')
      await page.fill('[name="phone"]', '0901234567')
      await page.fill('[name="email"]', 'nguyenvana@example.com')
      await page.fill('[name="address"]', '123 Nguyen Hue Street')
      await page.selectOption('[name="city"]', 'Ho Chi Minh City')
      await page.selectOption('[name="district"]', 'District 1')
      await page.fill('[name="notes"]', 'Please deliver before 5 PM')

      // Select delivery date
      await page.click('[data-testid="delivery-date-picker"]')
      await page.click('[data-testid="date-tomorrow"]')

      // Select delivery time slot
      await page.selectOption('[name="timeSlot"]', '14:00-17:00')
    })

    // Step 8: Apply voucher
    await test.step('Apply discount voucher', async () => {
      await page.fill('[data-testid="voucher-input"]', 'BIRTHDAY10')
      await page.click('[data-testid="apply-voucher-btn"]')

      // Verify voucher applied
      await expect(page.locator('[data-testid="toast-success"]')).toContainText('Voucher applied')

      // Verify discount shown
      const discount = page.locator('[data-testid="discount-amount"]')
      await expect(discount).toBeVisible()
      await expect(discount).toContainText('-')
    })

    // Step 9: Select payment method
    await test.step('Select payment method', async () => {
      await page.click('[data-testid="payment-method-cod"]')

      // Verify payment method selected
      const selectedPayment = page.locator('[data-testid="payment-method-cod"]')
      await expect(selectedPayment).toHaveClass(/selected/)
    })

    // Step 10: Review order summary
    await test.step('Review order summary', async () => {
      // Verify order summary
      await expect(page.locator('[data-testid="order-summary"]')).toBeVisible()

      // Verify line items
      await expect(page.locator('[data-testid="summary-subtotal"]')).toBeVisible()
      await expect(page.locator('[data-testid="summary-shipping"]')).toBeVisible()
      await expect(page.locator('[data-testid="summary-discount"]')).toBeVisible()
      await expect(page.locator('[data-testid="summary-total"]')).toBeVisible()
    })

    // Step 11: Place order
    let orderCode: string
    await test.step('Place order', async () => {
      await page.click('[data-testid="place-order-btn"]')

      // Wait for order confirmation page
      await page.waitForURL(/.*\/order-confirmation/)

      // Verify success message
      await expect(page.locator('h1')).toContainText('Order Placed Successfully')

      // Extract order code
      const orderCodeElement = page.locator('[data-testid="order-code"]')
      orderCode = await orderCodeElement.textContent() || ''
      expect(orderCode).toMatch(/^ORD-\d{8}$/)

      // Verify order details
      await expect(page.locator('[data-testid="order-total"]')).toBeVisible()
      await expect(page.locator('[data-testid="delivery-info"]')).toContainText('Nguyen Van A')
    })

    // Step 12: Verify order in account
    await test.step('Verify order in My Orders', async () => {
      await page.click('[data-testid="view-my-orders-btn"]')
      await expect(page).toHaveURL(/.*\/account\/orders/)

      // Find the order in list
      const orderRow = page.locator(`[data-testid="order-row"]:has-text("${orderCode}")`)
      await expect(orderRow).toBeVisible()

      // Verify order status
      await expect(orderRow).toContainText('Pending')
    })
  })

  test('Checkout validation: Empty cart', async ({ page }) => {
    await page.goto('https://siinstore.com/cart')

    // Verify empty cart message
    await expect(page.locator('[data-testid="empty-cart-message"]')).toBeVisible()

    // Verify checkout button disabled
    const checkoutBtn = page.locator('[data-testid="checkout-btn"]')
    await expect(checkoutBtn).toBeDisabled()
  })

  test('Checkout validation: Invalid shipping info', async ({ page }) => {
    // Add product to cart first
    await page.goto('https://siinstore.com/products/rose-bouquet')
    await page.click('[data-testid="add-to-cart-btn"]')
    await page.click('[data-testid="cart-icon"]')
    await page.click('[data-testid="checkout-btn"]')

    // Try to submit without filling required fields
    await page.click('[data-testid="place-order-btn"]')

    // Verify validation errors
    await expect(page.locator('[data-testid="error-fullName"]')).toContainText('Full name is required')
    await expect(page.locator('[data-testid="error-phone"]')).toContainText('Phone number is required')
    await expect(page.locator('[data-testid="error-address"]')).toContainText('Address is required')
  })

  test('Checkout validation: Invalid voucher code', async ({ page }) => {
    // Add product and go to checkout
    await page.goto('https://siinstore.com/products/rose-bouquet')
    await page.click('[data-testid="add-to-cart-btn"]')
    await page.click('[data-testid="cart-icon"]')
    await page.click('[data-testid="checkout-btn"]')

    // Try invalid voucher
    await page.fill('[data-testid="voucher-input"]', 'INVALID123')
    await page.click('[data-testid="apply-voucher-btn"]')

    // Verify error message
    await expect(page.locator('[data-testid="toast-error"]')).toContainText('Invalid voucher code')
  })

  test('Checkout: Out of stock product', async ({ page }) => {
    // Navigate to out-of-stock product
    await page.goto('https://siinstore.com/products/rare-orchid')

    // Verify out of stock badge
    await expect(page.locator('[data-testid="out-of-stock-badge"]')).toBeVisible()

    // Verify add to cart button disabled
    const addToCartBtn = page.locator('[data-testid="add-to-cart-btn"]')
    await expect(addToCartBtn).toBeDisabled()
  })
})

test.describe('Checkout Flow - Edge Cases', () => {
  test('Checkout with minimum order value not met', async ({ page }) => {
    // Add low-value product
    await page.goto('https://siinstore.com/products/greeting-card')
    await page.click('[data-testid="add-to-cart-btn"]')
    await page.click('[data-testid="cart-icon"]')

    // Try to checkout
    await page.click('[data-testid="checkout-btn"]')

    // Verify minimum order warning
    await expect(page.locator('[data-testid="min-order-warning"]')).toContainText('Minimum order value is 200,000 VND')
  })

  test('Checkout with expired delivery date', async ({ page }) => {
    // Add product and go to checkout
    await page.goto('https://siinstore.com/products/rose-bouquet')
    await page.click('[data-testid="add-to-cart-btn"]')
    await page.click('[data-testid="cart-icon"]')
    await page.click('[data-testid="checkout-btn"]')

    // Fill shipping info
    await page.fill('[name="fullName"]', 'Test User')
    await page.fill('[name="phone"]', '0901234567')
    await page.fill('[name="address"]', '123 Test Street')

    // Try to select past date (should be disabled)
    await page.click('[data-testid="delivery-date-picker"]')
    const pastDate = page.locator('[data-testid="date-yesterday"]')
    await expect(pastDate).toBeDisabled()
  })

  test('Checkout: Session timeout handling', async ({ page }) => {
    // Add product to cart
    await page.goto('https://siinstore.com/products/rose-bouquet')
    await page.click('[data-testid="add-to-cart-btn"]')

    // Simulate session timeout (clear cookies)
    await page.context().clearCookies()

    // Try to checkout
    await page.click('[data-testid="cart-icon"]')
    await page.click('[data-testid="checkout-btn"]')

    // Verify redirect to login or session expired message
    await expect(page).toHaveURL(/.*\/(login|session-expired)/)
  })
})
