# Devin AI - Testing & CI/CD Prompts

> **Source**: Devin AI System Prompt
> **Focus**: CI/CD integration, browser testing, deployment verification

---

## 🧪 Testing Strategy

### Comprehensive Testing Approach
```
Test [feature] across all layers:

1. Unit tests: Business logic in isolation
2. Integration tests: API + database interactions
3. E2E tests: Full user flows in browser
4. CI tests: Run in continuous integration
5. Manual verification: Test in staging environment
```

**Example**:
```
Test "Checkout flow with payment" across all layers:

1. Unit tests:
   - calculateOrderTotal function
   - validatePaymentMethod function
   - applyVoucherDiscount function

2. Integration tests:
   - POST /api/v1/orders endpoint
   - Payment webhook handler
   - Order creation in database

3. E2E tests (Playwright):
   - Browse products → Add to cart → Checkout → Payment → Confirmation
   - Test with different payment methods
   - Test with vouchers

4. CI tests:
   - Run all tests on GitHub Actions
   - Verify no environment-specific failures

5. Manual verification:
   - Deploy to staging
   - Complete real checkout flow
   - Verify order in admin panel
```

---

## 🌐 Browser Testing

### Playwright E2E Testing
```
Write E2E test for [user flow] using Playwright.

Structure:
1. Navigate to starting page
2. Interact with UI elements (click, type, select)
3. Wait for async operations
4. Assert expected state
5. Verify data persisted (database, API)
```

**Example**:
```typescript
// E2E test: Product search and filter
test('should search and filter products', async ({ page }) => {
  // Navigate
  await page.goto('https://siinstore.com/products')

  // Search
  await page.fill('[data-testid="search-input"]', 'rose')
  await page.click('[data-testid="search-btn"]')
  await page.waitForSelector('[data-testid="product-card"]')

  // Verify search results
  const products = await page.locator('[data-testid="product-card"]').all()
  expect(products.length).toBeGreaterThan(0)

  // Apply filter
  await page.click('[data-testid="filter-occasion"]')
  await page.click('text=Birthday')
  await page.waitForTimeout(1000) // Wait for filter to apply

  // Verify filtered results
  const filteredProducts = await page.locator('[data-testid="product-card"]').all()
  expect(filteredProducts.length).toBeLessThanOrEqual(products.length)

  // Verify filter badge
  await expect(page.locator('[data-testid="active-filter"]')).toContainText('Birthday')
})
```

---

### Browser Debugging
```
Debug browser test failure:

1. Run test with headed mode:
   npx playwright test --headed

2. Use browser DevTools:
   - Inspect elements
   - Check console errors
   - Monitor network requests

3. Add screenshots on failure:
   await page.screenshot({ path: 'failure.png' })

4. Use trace viewer:
   npx playwright test --trace on
   npx playwright show-trace trace.zip
```

**Example**:
```
Debug "Checkout button not clickable":

1. Run headed: npx playwright test checkout.spec.ts --headed
   Observation: Button appears but click has no effect

2. Open DevTools in test browser:
   Console error: "Cannot read property 'id' of undefined"

3. Add screenshot before click:
   await page.screenshot({ path: 'before-click.png' })
   await page.click('[data-testid="checkout-btn"]')

4. Root cause: Cart data not loaded before button click
   Fix: Add wait for cart data:
   await page.waitForSelector('[data-testid="cart-item"]')
   await page.click('[data-testid="checkout-btn"]')
```

---

## 🔄 CI/CD Integration

### GitHub Actions Testing
```
Set up CI/CD pipeline for testing:

.github/workflows/test.yml:
- Run on: push, pull_request
- Jobs:
  1. Lint & type check
  2. Unit tests
  3. Integration tests
  4. E2E tests
  5. Build verification
```

**Example**:
```yaml
name: Test Suite

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: 18
      - run: npm ci
      - run: npm run lint
      - run: npm run typecheck

  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: npm ci
      - run: npm run test:unit

  integration-tests:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: test
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: npm ci
      - run: npm run test:integration

  e2e-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: npm ci
      - run: npx playwright install --with-deps
      - run: npm run test:e2e
      - uses: actions/upload-artifact@v3
        if: failure()
        with:
          name: playwright-report
          path: playwright-report/
```

---

### CI Test Failures
```
When CI tests fail:

1. Check CI logs for error messages
2. Reproduce locally:
   - Use same Node version
   - Use same environment variables
   - Use same database state

3. Common CI-specific issues:
   - Timing issues (add waits)
   - Environment variables missing
   - Database not seeded
   - Port conflicts

4. Fix and push
5. Verify CI passes
```

**Example**:
```
CI failure: "E2E tests timeout"

1. Check logs:
   Error: Timeout waiting for selector '[data-testid="product-card"]'

2. Reproduce locally:
   npm run test:e2e
   ✅ Tests pass locally

3. Analysis: CI environment slower than local
   Issue: Default timeout (5s) too short for CI

4. Fix: Increase timeout in playwright.config.ts
   timeout: 30000 // 30 seconds

5. Push and verify:
   git add playwright.config.ts
   git commit -m "Increase E2E test timeout for CI"
   git push
   ✅ CI tests pass
```

---

## 🚀 Deployment Testing

### Pre-Deployment Verification
```
Before deploying to production:

1. All tests pass in CI
2. Manual testing in staging:
   - Critical user flows
   - Payment processing
   - Email notifications
   - Third-party integrations

3. Performance check:
   - Load time < 3s
   - API response < 500ms
   - No memory leaks

4. Security check:
   - No exposed secrets
   - HTTPS enabled
   - Security headers configured
```

---

### Post-Deployment Verification
```
After deploying to production:

1. Smoke tests:
   - Homepage loads
   - API health check passes
   - Database connection works

2. Critical path testing:
   - User can register/login
   - User can browse products
   - User can complete checkout

3. Monitoring:
   - Check error logs
   - Monitor API response times
   - Check user analytics

4. Rollback plan ready if issues found
```

**Example**:
```
Post-deployment verification for "New checkout flow":

1. Smoke tests:
   ✅ curl https://siinstore.com (200 OK)
   ✅ curl https://siinstore.com/api/health (200 OK)

2. Critical path:
   ✅ Register new user
   ✅ Browse products
   ✅ Add to cart
   ✅ Complete checkout with test payment
   ✅ Verify order in admin panel

3. Monitoring (first 30 minutes):
   ✅ No errors in logs
   ✅ API response time: 180ms avg (good)
   ✅ 5 successful orders from real users

4. Rollback: Not needed, deployment successful
```

---

## 🔧 Environment Testing

### Test Across Environments
```
Test [feature] in multiple environments:

1. Local development:
   - Fast iteration
   - Full debugging access

2. Staging:
   - Production-like environment
   - Test with real data (anonymized)
   - Test integrations (payment, email)

3. Production:
   - Smoke tests only
   - Monitor real user behavior
   - Quick rollback if issues
```

---

### Environment-Specific Issues
```
Handle environment differences:

Common issues:
- API URLs different per environment
- Database credentials different
- Third-party API keys different
- CORS settings different

Solution:
- Use environment variables
- Document required env vars
- Validate env vars on startup
```

**Example**:
```typescript
// Validate environment variables
const requiredEnvVars = [
  'DATABASE_URL',
  'JWT_SECRET',
  'STRIPE_SECRET_KEY',
  'STRIPE_WEBHOOK_SECRET',
]

for (const envVar of requiredEnvVars) {
  if (!process.env[envVar]) {
    throw new Error(`Missing required environment variable: ${envVar}`)
  }
}
```

---

## 🎯 Test Data Management

### Seed Test Data
```
Set up test data for consistent testing:

1. Create seed script:
   - Users (admin, customer)
   - Products (various categories)
   - Orders (different states)
   - Vouchers (active, expired)

2. Run before tests:
   npm run db:seed:test

3. Clean up after tests:
   npm run db:clean:test
```

**Example**:
```typescript
// seed-test-data.ts
export async function seedTestData() {
  // Create test users
  const admin = await db.user.create({
    data: {
      email: 'admin@test.com',
      password: await bcrypt.hash('Test123!', 12),
      role: 'admin',
    },
  })

  const customer = await db.user.create({
    data: {
      email: 'customer@test.com',
      password: await bcrypt.hash('Test123!', 12),
      role: 'customer',
    },
  })

  // Create test products
  const products = await db.product.createMany({
    data: [
      { name: 'Rose Bouquet', price: 300000, stock: 50 },
      { name: 'Lily Arrangement', price: 400000, stock: 30 },
    ],
  })

  // Create test vouchers
  await db.voucher.create({
    data: {
      code: 'TEST10',
      discount: 0.1,
      expiresAt: new Date('2026-12-31'),
    },
  })
}
```

---

## 📊 Test Reporting

### Generate Test Reports
```
Create comprehensive test reports:

1. Coverage report:
   npm run test:coverage
   Open: coverage/index.html

2. E2E test report:
   npx playwright test
   Open: playwright-report/index.html

3. CI test summary:
   - Tests passed/failed
   - Coverage percentage
   - Performance metrics
```

---

## 🔗 Best Practices

### Test Isolation
```
Ensure tests are isolated:

1. Each test independent (no shared state)
2. Clean up after each test
3. Use transactions for database tests
4. Mock external services
```

---

### Test Performance
```
Keep tests fast:

1. Unit tests: < 100ms each
2. Integration tests: < 1s each
3. E2E tests: < 30s each
4. Full suite: < 10 minutes

Optimize:
- Run tests in parallel
- Mock slow operations
- Use test database (in-memory if possible)
```

---

## 🔗 Related Tools

- `<shell>`: Run test commands
- `<open_file>`: Inspect test files
- `<str_replace>`: Fix test code
- `<navigate_browser>`: E2E testing
- `<view_browser>`: Verify UI state
