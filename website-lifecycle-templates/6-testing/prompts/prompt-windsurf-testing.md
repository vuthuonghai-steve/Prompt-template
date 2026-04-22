# Windsurf/Cline - Testing & Quality Prompts

> **Source**: Windsurf (Cline) System Prompt
> **Focus**: Code review, quality checks, test verification

---

## 🔍 Code Review for Testing

### Review Test Quality
```
Review tests for [feature/module].

Checklist:
- [ ] Tests cover happy path
- [ ] Tests cover edge cases
- [ ] Tests cover error scenarios
- [ ] Test names descriptive
- [ ] Assertions clear and specific
- [ ] No flaky tests (timing issues)
- [ ] Mocks used appropriately
- [ ] Test data realistic
```

**Example**:
```
Review tests for Order Service.

Findings:
✅ Happy path covered: Create order, calculate total
✅ Edge cases covered: Empty cart, out of stock
❌ Missing: Error scenarios (payment failure, invalid voucher)
✅ Test names descriptive: "should create order with valid data"
❌ Flaky test: "should process payment" (timing issue with mock)
✅ Mocks appropriate: Database, payment service mocked
❌ Test data unrealistic: Using price = 1 (should be realistic amounts)

Actions:
1. Add tests for error scenarios
2. Fix flaky test by using waitFor instead of setTimeout
3. Update test data to use realistic prices
```

---

## ✅ Quality Checks

### Pre-Commit Quality Gate
```
Before committing [changes], run quality checks:

1. Linting:
   npm run lint
   Fix all errors and warnings

2. Type checking:
   npm run typecheck
   Fix all type errors

3. Unit tests:
   npm run test:unit
   All tests must pass

4. Code formatting:
   npm run format
   Ensure consistent style

5. Git diff review:
   git diff
   Remove debug code, console.logs
```

---

### Code Quality Metrics
```
Measure code quality for [module]:

Metrics:
- Test coverage: > 80%
- Cyclomatic complexity: < 10
- Function length: < 50 lines
- File length: < 300 lines
- Code duplication: < 5%

Tools:
- Coverage: npm run test:coverage
- Complexity: npm run analyze
- Duplication: npm run check-duplicates
```

**Example**:
```
Code quality for src/services/order/:

Metrics:
✅ Test coverage: 85%
❌ Cyclomatic complexity: 15 (calculateOrderTotal function)
✅ Function length: avg 25 lines
✅ File length: avg 180 lines
⚠️ Code duplication: 8% (discount calculation repeated)

Actions:
1. Refactor calculateOrderTotal to reduce complexity
2. Extract discount calculation to separate function
3. Add tests to maintain coverage after refactor
```

---

## 🧪 Test Coverage Analysis

### Coverage Report Review
```
Analyze test coverage for [module]:

1. Generate report:
   npm run test:coverage

2. Review uncovered lines:
   - Identify critical paths not tested
   - Prioritize by risk/importance

3. Add missing tests:
   - Focus on business logic
   - Cover error handling
   - Test edge cases

4. Verify improvement:
   npm run test:coverage
   Compare before/after
```

**Example**:
```
Coverage analysis for Payment Service:

Current coverage: 65%

Uncovered lines:
- Line 45-52: Error handling for payment failure (CRITICAL)
- Line 78-85: Retry logic for network timeout (HIGH)
- Line 120-125: Logging for successful payment (LOW)

Added tests:
1. "should handle payment failure gracefully"
2. "should retry on network timeout"
3. "should log successful payment"

New coverage: 88% ✅
```

---

## 🔄 Regression Testing

### Prevent Regressions
```
After fixing [bug], add regression test:

1. Reproduce bug in test (test should fail)
2. Fix the bug
3. Verify test now passes
4. Add test to suite to prevent regression
```

**Example**:
```
Bug: "Discount applied twice when voucher + loyalty points used"

Regression test:
```typescript
it('should apply discount only once with voucher and loyalty points', async () => {
  // Arrange
  const order = {
    subtotal: 300000,
    voucherId: 'SAVE10', // 10% discount
    loyaltyPoints: 50000, // 50k points
  }

  // Act
  const total = await calculateOrderTotal(order)

  // Assert
  // Correct: 300000 - 30000 (voucher) - 50000 (points) = 220000
  // Bug was: 300000 - 30000 - 30000 (voucher applied twice) - 50000 = 190000
  expect(total).toBe(220000)
})
```

Fix applied, test passes ✅
```

---

## 🎯 Test Strategy

### Test Pyramid
```
Follow test pyramid for [project]:

Unit tests (70%):
- Fast, isolated
- Test business logic
- Mock dependencies

Integration tests (20%):
- Test API + database
- Test service interactions
- Use test database

E2E tests (10%):
- Test critical user flows
- Test in browser
- Slow but high confidence
```

---

### Test Prioritization
```
Prioritize tests by:

1. Critical path (must test):
   - User authentication
   - Payment processing
   - Order creation

2. High risk (should test):
   - Data validation
   - Error handling
   - Security checks

3. Nice to have (can test):
   - UI styling
   - Logging
   - Analytics
```

**Example**:
```
Test prioritization for E-commerce:

Critical (E2E tests):
✅ User can register and login
✅ User can browse products
✅ User can complete checkout
✅ Payment processing works

High risk (Integration tests):
✅ Product search returns correct results
✅ Cart updates correctly
✅ Voucher validation works
✅ Inventory decrements on order

Nice to have (Unit tests):
✅ Price formatting correct
✅ Date formatting correct
✅ Analytics events tracked
```

---

## 🐛 Bug Verification

### Verify Bug Fix
```
After fixing [bug], verify:

1. Bug no longer reproducible
2. Test added to prevent regression
3. Related functionality still works
4. No new bugs introduced
5. Performance not degraded
```

**Example**:
```
Bug fix: "Cart total incorrect when removing items"

Verification:
1. Manual test:
   - Add 3 items to cart
   - Remove 1 item
   - Verify total correct ✅

2. Regression test added:
   "should update total when item removed from cart" ✅

3. Related functionality:
   - Add item to cart ✅
   - Update quantity ✅
   - Clear cart ✅

4. No new bugs:
   - All existing tests pass ✅

5. Performance:
   - Cart update time: 50ms (was 45ms, acceptable) ✅
```

---

## 📊 Test Metrics

### Track Test Health
```
Monitor test suite health:

Metrics:
- Pass rate: > 95%
- Flaky tests: 0
- Test duration: < 10 minutes
- Coverage: > 80%
- New tests per feature: 3+ tests

Weekly review:
- Identify flaky tests
- Remove obsolete tests
- Update outdated tests
- Improve slow tests
```

---

## 🔧 Test Maintenance

### Keep Tests Maintainable
```
Maintain test suite:

1. Remove duplicate tests
2. Update tests when requirements change
3. Refactor tests to reduce duplication
4. Keep test data up to date
5. Document complex test scenarios
```

**Example**:
```
Test maintenance for Order tests:

Issues found:
- 3 duplicate tests for "create order"
- 5 tests failing due to outdated API response format
- Test data using old product IDs

Actions:
1. Remove duplicate tests, keep most comprehensive one
2. Update tests to match new API response:
   Old: { success: true, order: {...} }
   New: { data: {...}, meta: {...} }
3. Update test data to use current product IDs from seed
4. Extract common test setup to beforeEach

Result:
- Tests: 45 → 42 (removed duplicates)
- Pass rate: 100% (was 89%)
- Maintenance time: 2 hours
```

---

## 🎯 Best Practices

### Test Naming
```
Use descriptive test names:

Pattern: "should [expected behavior] when [condition]"

Good:
✅ "should return 200 when order created successfully"
✅ "should throw error when product out of stock"
✅ "should apply discount when valid voucher provided"

Bad:
❌ "test order creation"
❌ "it works"
❌ "test1"
```

---

### Test Organization
```
Organize tests logically:

By feature:
tests/
├── auth/
│   ├── login.test.ts
│   └── register.test.ts
├── orders/
│   ├── create-order.test.ts
│   └── calculate-total.test.ts
└── products/
    ├── search.test.ts
    └── filter.test.ts

By type:
tests/
├── unit/
├── integration/
└── e2e/
```

---

### Mock Strategy
```
Mock external dependencies:

Mock:
✅ External APIs (payment, shipping)
✅ Database (for unit tests)
✅ Email service
✅ File system

Don't mock:
❌ Code under test
❌ Simple utilities
❌ Type definitions
```

**Example**:
```typescript
// Mock external payment API
vi.mock('@/lib/stripe', () => ({
  stripe: {
    paymentIntents: {
      create: vi.fn().mockResolvedValue({
        id: 'pi_test123',
        status: 'succeeded',
      }),
    },
  },
}))

// Don't mock code under test
// ❌ vi.mock('@/services/order/service.order-code')
// ✅ Test the actual service
import { createOrder } from '@/services/order/service.order-code'
```

---

## 🔍 Test Debugging

### Debug Failing Tests
```
When test fails:

1. Read error message carefully
2. Check what changed recently
3. Run test in isolation
4. Add console.log to see state
5. Use debugger if needed
6. Fix root cause
7. Remove debug code
```

**Example**:
```
Test failing: "should create order with shipping"

1. Error: "Expected 330000, received 300000"
2. Recent change: Updated shipping fee calculation
3. Run in isolation: npm run test -- create-order.test.ts
4. Add logging:
   console.log('Subtotal:', subtotal)
   console.log('Shipping:', shippingFee)
   console.log('Total:', total)
5. Found: Shipping fee not added to total
6. Fix: Add shippingFee to total calculation
7. Remove console.log statements
8. Test passes ✅
```

---

## 🔗 Related Practices

### Continuous Testing
```
Integrate testing into workflow:

1. Local development:
   - Run tests on file save (watch mode)
   - Pre-commit hook runs tests

2. Pull requests:
   - CI runs full test suite
   - Require tests to pass before merge

3. Deployment:
   - Run tests before deploy
   - Smoke tests after deploy
```

---

### Test Documentation
```
Document test scenarios:

For complex features:
- Document test strategy
- List test cases
- Explain test data setup
- Note known limitations
```

**Example**:
```markdown
# Order Service Tests

## Test Strategy
- Unit tests: Business logic (calculateTotal, validateOrder)
- Integration tests: API endpoints + database
- E2E tests: Full checkout flow

## Test Cases
1. Happy path: Create order with valid data
2. Edge cases: Empty cart, out of stock, invalid voucher
3. Error cases: Payment failure, network timeout

## Test Data
- Users: admin@test.com, customer@test.com
- Products: Seeded from seed-test-data.ts
- Vouchers: TEST10 (10% off), SAVE20 (20% off)

## Known Limitations
- Payment tests use Stripe test mode
- Email tests use mock SMTP server
```

---

## 🔗 Related Tools

- Linter: Check code quality
- Type checker: Verify types
- Coverage tool: Measure test coverage
- CI/CD: Automate testing
- Code review: Manual quality check
