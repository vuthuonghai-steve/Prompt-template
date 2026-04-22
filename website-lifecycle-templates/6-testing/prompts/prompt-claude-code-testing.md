# Claude Code - Testing & Verification Prompts

> **Source**: Claude Code System Prompt
> **Focus**: Systematic debugging, verification, test execution

---

## 🔍 Systematic Debugging

### Debug Workflow
```
Debug [issue] in [component/feature].

Protocol:
1. Reproduce the issue consistently
2. Gather context (logs, error messages, stack traces)
3. Form hypothesis about root cause
4. Test hypothesis with minimal changes
5. Verify fix resolves issue
6. Add regression test
```

**Example**:
```
Debug "Payment fails silently in checkout" in payment flow.

Protocol:
1. Reproduce: Complete checkout, payment shows success but order not created
2. Context: Check browser console, API logs, database state
3. Hypothesis: Payment webhook not triggering order creation
4. Test: Add logging to webhook handler, trigger payment
5. Root cause: Webhook signature verification failing
6. Fix: Update webhook secret in environment
7. Verify: Complete checkout end-to-end
8. Add test: Mock webhook call in integration test
```

---

## ✅ Verification Before Completion

### Pre-Completion Checklist
```
Before marking task complete, verify:

Critical:
- [ ] Feature works as specified
- [ ] All tests pass (unit, integration, e2e)
- [ ] No linter errors
- [ ] No type errors
- [ ] No console errors in browser
- [ ] No breaking changes to existing features

Optional (if applicable):
- [ ] Performance acceptable
- [ ] Accessibility compliant
- [ ] Mobile responsive
- [ ] Cross-browser compatible
```

---

### Test Execution Workflow
```
Run tests systematically:

1. Unit tests first (fastest feedback)
   npm run test:unit

2. Integration tests (API/database)
   npm run test:integration

3. E2E tests (full user flows)
   npm run test:e2e

4. If any fail:
   - Read error message carefully
   - Identify root cause (code vs test issue)
   - Fix and re-run
   - Do NOT modify tests unless explicitly wrong
```

**Example**:
```
After implementing "Add product to cart":

1. npm run test:unit
   ✅ All 45 tests pass

2. npm run test:integration
   ❌ 1 test fails: "POST /api/v1/cart should add product"
   Error: Product not found
   Root cause: Test uses non-existent product ID
   Fix: Update test to use valid product ID from seed data

3. npm run test:e2e
   ✅ All 12 tests pass

4. Final verification: Manual test in browser
   ✅ Add to cart works correctly
```

---

## 🐛 Test Failure Investigation

### When Tests Fail
```
Test failed: [test name]

Investigation steps:
1. Read full error message and stack trace
2. Identify: Is this a code bug or test bug?
3. Check recent changes that might affect this test
4. Run test in isolation to rule out test interdependence
5. Add debugging output if needed
6. Fix root cause (prefer fixing code over changing test)
```

**Example**:
```
Test failed: "should calculate discount correctly"

Investigation:
1. Error: Expected 270000, received 300000
2. Analysis: Discount not being applied
3. Recent change: Refactored calculateOrderTotal function
4. Run in isolation: npm run test:unit -- discount.test.ts
5. Add console.log to see discount calculation steps
6. Root cause: Discount percentage divided by 100 twice
7. Fix: Remove duplicate division
8. Re-run: Test passes
```

---

## 🔄 Regression Testing

### After Bug Fix
```
After fixing [bug], ensure no regression:

1. Fix the specific bug
2. Add test that would have caught the bug
3. Run full test suite
4. Manually test related features
5. Check for similar bugs in codebase
```

**Example**:
```
After fixing "Voucher discount applied twice":

1. Fix: Remove duplicate discount application in calculateOrderTotal
2. Add test: "should apply voucher discount only once"
3. Run: npm run test (all tests pass)
4. Manual test: Apply voucher in checkout, verify total correct
5. Search codebase: Check if similar discount logic exists elsewhere
6. Found: Shipping discount has same issue
7. Fix: Apply same fix to shipping discount
8. Add test: "should apply shipping discount only once"
```

---

## 🧪 Test Writing Guidelines

### Write Effective Tests
```
When writing tests for [feature]:

Structure:
- Arrange: Set up test data and mocks
- Act: Execute the code under test
- Assert: Verify expected behavior

Best practices:
- One assertion per test (or closely related assertions)
- Test behavior, not implementation
- Use descriptive test names
- Clean up after each test
```

**Example**:
```typescript
describe('Order Service', () => {
  describe('createOrder', () => {
    it('should create order with correct total when voucher applied', async () => {
      // Arrange
      const orderData = {
        items: [{ productId: 'prod-1', quantity: 2, price: 100000 }],
        voucherId: 'voucher-10-percent',
      }
      const mockVoucher = { id: 'voucher-10-percent', discount: 0.1 }
      vi.mocked(db.voucher.findUnique).mockResolvedValue(mockVoucher)

      // Act
      const order = await createOrder(orderData)

      // Assert
      expect(order.subtotal).toBe(200000)
      expect(order.discount).toBe(20000)
      expect(order.total).toBe(180000)
    })
  })
})
```

---

## 🎯 Test Coverage Strategy

### Prioritize Test Coverage
```
Focus test coverage on:

High priority (must have 90%+ coverage):
- Business logic (order calculation, payment processing)
- Authentication & authorization
- Data validation
- Error handling

Medium priority (target 80%+ coverage):
- API endpoints
- Database operations
- Utility functions

Low priority (target 60%+ coverage):
- UI components (focus on critical paths)
- Configuration files
- Type definitions
```

---

## 🔧 Debugging Tools

### Use Available Tools
```
Debugging toolkit:

1. Read tool: Inspect code and logs
2. Grep tool: Search for error messages
3. Bash tool: Run tests, check logs
4. Edit tool: Add debugging output
5. Browser DevTools: Inspect network, console

Workflow:
- Start with logs and error messages
- Use Grep to find related code
- Read relevant files
- Add temporary logging if needed
- Remove debugging code after fix
```

**Example**:
```
Debug "API returns 500 error on checkout":

1. Read API logs: /var/log/api/error.log
   Error: "Cannot read property 'id' of undefined"

2. Grep for error location:
   grep -r "Cannot read property 'id'" src/
   Found in: src/services/order/service.order-code.ts:145

3. Read file: src/services/order/service.order-code.ts
   Line 145: const userId = req.user.id
   Issue: req.user is undefined (auth middleware not applied)

4. Fix: Add auth middleware to checkout route
   app.post('/api/v1/checkout', authenticate, checkoutHandler)

5. Verify: Test checkout flow, check logs
   ✅ No more 500 errors
```

---

## 📊 Performance Testing

### Verify Performance
```
After implementing [feature], check performance:

1. Measure baseline (before changes)
2. Implement feature
3. Measure new performance
4. Compare: Is degradation acceptable?
5. Optimize if needed
6. Add performance test to prevent regression
```

**Example**:
```
After implementing "Search products with filters":

1. Baseline: Product list loads in 200ms
2. Implement: Add filters (category, price, tags)
3. New performance: Product list loads in 1200ms
4. Analysis: Too slow (5x slower)
5. Optimize: Add database indexes on filter columns
6. After optimization: Product list loads in 280ms
7. Add test: Assert API response time < 500ms
```

---

## 🔒 Security Testing

### Security Verification
```
Before deploying [feature], verify security:

Checklist:
- [ ] Input validation on all user inputs
- [ ] SQL injection prevention (parameterized queries)
- [ ] XSS prevention (sanitize output)
- [ ] CSRF protection (tokens on state-changing requests)
- [ ] Authentication required on protected endpoints
- [ ] Authorization checks (user can only access own data)
- [ ] Rate limiting on sensitive endpoints
- [ ] Secrets not exposed in logs or errors
```

**Example**:
```
Security verification for "User profile update":

✅ Input validation: Email, phone, name validated with Zod
✅ SQL injection: Using Prisma ORM (parameterized)
✅ XSS: Output sanitized with DOMPurify
✅ CSRF: Token required on POST /api/v1/users/profile
✅ Authentication: JWT required
✅ Authorization: User can only update own profile
   Code: if (req.user.id !== userId) return 403
✅ Rate limiting: 10 requests per 15 minutes
✅ Secrets: Password not returned in API response
```

---

## 🎯 Best Practices

### Test Maintenance
```
Keep tests maintainable:

1. DRY: Extract common setup to beforeEach
2. Clear: Use descriptive variable names
3. Isolated: Each test independent
4. Fast: Mock slow operations (API, database)
5. Reliable: No flaky tests (avoid timing issues)
```

---

### Continuous Testing
```
Run tests continuously during development:

1. Watch mode for unit tests:
   npm run test:unit -- --watch

2. Run affected tests only:
   npm run test -- --changed

3. Pre-commit hook:
   Run linter + unit tests before commit

4. CI/CD:
   Run full test suite on every push
```

---

## 🔗 Related Commands

- `Read`: Inspect code, logs, test files
- `Grep`: Search for errors, test patterns
- `Bash`: Run test commands, check output
- `Edit`: Fix code, add tests
- `TaskUpdate`: Mark tests completed
