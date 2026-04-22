# Cursor Agent - Testing Prompts

> **Source**: Cursor Agent 2.0 System Prompt
> **Focus**: Test generation, linting, diagnostics

---

## 🧪 Test Generation

### Unit Test Generation
```
Generate unit tests for [function/class name] in [file path].

Requirements:
- Use [Jest/Vitest/Mocha] framework
- Cover happy path and edge cases
- Mock external dependencies
- Target 80%+ code coverage
```

**Example**:
```
Generate unit tests for the `calculateOrderTotal` function in src/services/order/service.order-code.ts.

Requirements:
- Use Vitest framework
- Cover: valid orders, empty cart, discount vouchers, shipping fees
- Mock: database, payment service
- Target 90% code coverage
```

---

### Integration Test Generation
```
Generate integration tests for [API endpoint/feature].

Requirements:
- Use [Supertest/Playwright] framework
- Test full request/response cycle
- Include authentication
- Test error scenarios
```

**Example**:
```
Generate integration tests for POST /api/v1/orders endpoint.

Requirements:
- Use Supertest + Vitest
- Test: successful order creation, invalid input, out of stock, payment failure
- Include JWT authentication
- Verify database state after each test
```

---

### E2E Test Generation
```
Generate E2E tests for [user flow].

Requirements:
- Use [Playwright/Cypress] framework
- Test critical user journey
- Include assertions for UI elements
- Handle async operations
```

**Example**:
```
Generate E2E tests for checkout flow: Browse → Add to Cart → Checkout → Payment.

Requirements:
- Use Playwright
- Test: product selection, cart updates, form validation, payment success
- Assert: order confirmation page, order in database
- Handle: loading states, API delays
```

---

## 🔍 Linting & Diagnostics

### Read Linter Errors
```
Check linter errors in [file/directory path].

Action:
- Use read_lints tool with specific paths
- Fix errors found
- Re-run linter to verify
```

**Example**:
```
Check linter errors in src/services/order/.

Action:
- Read lints for src/services/order/
- Fix: unused imports, type errors, formatting issues
- Run: npm run lint to verify all errors fixed
```

---

### Fix Type Errors
```
Fix TypeScript errors in [file path].

Steps:
1. Read file to understand context
2. Check linter diagnostics
3. Fix type mismatches
4. Verify with tsc --noEmit
```

**Example**:
```
Fix TypeScript errors in src/screens/Admin/OrderManagement.tsx.

Steps:
1. Read file and check imports
2. Read lints to see specific errors
3. Fix: missing type annotations, incorrect prop types
4. Run: npm run typecheck
```

---

## 🐛 Debugging

### Systematic Debugging
```
Debug [issue description] in [file/feature].

Approach:
1. Reproduce the issue
2. Use codebase_search to understand flow
3. Add logging/breakpoints
4. Identify root cause
5. Fix and verify
```

**Example**:
```
Debug "Order total calculation incorrect when voucher applied" in checkout flow.

Approach:
1. Reproduce: Add product, apply voucher, check total
2. Search: "How is order total calculated with vouchers?"
3. Add console.log in calculateOrderTotal function
4. Root cause: Voucher discount applied before tax instead of after
5. Fix: Apply discount after tax calculation
6. Verify: Run E2E test for checkout with voucher
```

---

### Test Failure Investigation
```
Investigate test failure: [test name] in [test file].

Steps:
1. Read test file
2. Check error message
3. Search for related code
4. Identify mismatch between test and implementation
5. Fix code or update test
```

**Example**:
```
Investigate test failure: "should calculate shipping fee correctly" in tests/order.test.ts.

Steps:
1. Read tests/order.test.ts
2. Error: Expected 30000, received 25000
3. Search: "How is shipping fee calculated?"
4. Found: Shipping fee logic changed but test not updated
5. Update test to match new shipping fee structure
6. Run: npm run test:unit
```

---

## ✅ Verification Workflow

### Pre-Commit Verification
```
Verify changes before committing.

Checklist:
- [ ] Run linter: npm run lint
- [ ] Run type check: npm run typecheck
- [ ] Run unit tests: npm run test:unit
- [ ] Run integration tests: npm run test:integration
- [ ] Check git diff for unintended changes
```

---

### Post-Implementation Verification
```
After implementing [feature], verify:

1. Functionality works as expected
2. All tests pass
3. No linter errors
4. No type errors
5. No breaking changes to existing features
```

**Example**:
```
After implementing "Apply voucher to order", verify:

1. Manual test: Apply voucher in checkout, verify discount applied
2. Run: npm run test (all tests pass)
3. Run: npm run lint (no errors)
4. Run: npm run typecheck (no errors)
5. Test: Existing checkout flow still works without voucher
```

---

## 🔄 Test-Driven Development (TDD)

### TDD Workflow
```
Implement [feature] using TDD.

Steps:
1. Write failing test for [feature]
2. Run test to confirm it fails
3. Implement minimal code to pass test
4. Run test to confirm it passes
5. Refactor code
6. Repeat for next test case
```

**Example**:
```
Implement "Calculate order total with multiple vouchers" using TDD.

Steps:
1. Write test: "should apply multiple vouchers correctly"
2. Run: npm run test (test fails - function not implemented)
3. Implement: calculateOrderTotal with multi-voucher logic
4. Run: npm run test (test passes)
5. Refactor: Extract voucher validation logic
6. Next test: "should reject invalid voucher combinations"
```

---

## 📊 Coverage Analysis

### Check Test Coverage
```
Analyze test coverage for [module/feature].

Steps:
1. Run: npm run test:coverage
2. Review coverage report
3. Identify uncovered lines
4. Write tests for uncovered code
5. Re-run coverage to verify improvement
```

**Example**:
```
Analyze test coverage for src/services/order/.

Steps:
1. Run: npm run test:coverage
2. Coverage: 65% (target: 80%)
3. Uncovered: Error handling in createOrder, edge cases in calculateTotal
4. Write tests for error scenarios and edge cases
5. Re-run: Coverage now 85%
```

---

## 🎯 Best Practices

### Test Naming Convention
```
Test names should be descriptive and follow pattern:
"should [expected behavior] when [condition]"

Examples:
- "should return 200 when order created successfully"
- "should throw error when product out of stock"
- "should apply discount when valid voucher provided"
```

---

### Test Organization
```
Organize tests by feature/module:

tests/
├── unit/
│   ├── services/
│   │   └── order.test.ts
│   └── utils/
│       └── format.test.ts
├── integration/
│   └── api/
│       └── orders.test.ts
└── e2e/
    └── checkout-flow.spec.ts
```

---

### Mock Best Practices
```
When mocking:
1. Mock external dependencies (API, database)
2. Don't mock code under test
3. Use realistic mock data
4. Reset mocks between tests
```

**Example**:
```typescript
// Mock database
vi.mock('@/lib/db', () => ({
  db: {
    order: {
      create: vi.fn(),
      findUnique: vi.fn(),
    },
  },
}))

// Reset mocks
afterEach(() => {
  vi.clearAllMocks()
})
```

---

## 🔗 Related Tools

- `read_lints`: Check linter errors
- `codebase_search`: Find code by meaning
- `grep`: Search for exact text
- `run_terminal_cmd`: Run test commands
- `edit_file`: Fix code issues
