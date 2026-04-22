# Bug Fix Example: Cart Total Calculation Error

> **Real-world example**: Discount logic causing incorrect cart totals

---

## 🐛 Bug Report

**Issue ID**: BUG-2026-04-18-042  
**Reported**: 2026-04-18 09:15 UTC  
**Severity**: 🟠 High  
**Status**: 🟢 Fixed  

### Description

Users reported incorrect cart totals when applying multiple discounts (voucher + loyalty points). Cart shows lower total than actual charge at checkout.

### User Impact

- **Affected users**: 234 users (last 7 days)
- **Complaints**: 18 support tickets
- **Revenue impact**: $3,200 overcharged (refunds issued)

---

## 🔍 Root Cause Analysis

### Investigation Steps

```bash
# 1. Reproduce issue
# Applied 20% voucher + 500 loyalty points (=$5)
# Expected: $100 → $80 (voucher) → $75 (points) = $75
# Actual: $100 → $80 (voucher) → $76 (points applied to original)

# 2. Check cart calculation logic
grep -r "calculateTotal" src/services/cart/

# 3. Found bug in service.cart-calculation.ts
```

### The Bug

```typescript
// ❌ BEFORE (WRONG)
export const calculateCartTotal = (cart: Cart): number => {
  const subtotal = cart.items.reduce((sum, item) => sum + item.price * item.quantity, 0)
  
  // Bug: Both discounts applied to original subtotal
  const voucherDiscount = cart.voucher 
    ? subtotal * (cart.voucher.percentage / 100) 
    : 0
  
  const pointsDiscount = cart.loyaltyPoints 
    ? cart.loyaltyPoints * 0.01  // 100 points = $1
    : 0
  
  // Wrong: Both discounts from original subtotal
  return subtotal - voucherDiscount - pointsDiscount
}
```

### Why It Happened

1. **Immediate cause**: Discounts calculated independently from original subtotal
2. **Contributing factors**: 
   - No test case for multiple discount combinations
   - Code review missed the logic error
   - Staging tests only used single discount
3. **Root cause**: Insufficient test coverage for discount edge cases

---

## 🛠️ The Fix

### Code Changes

```typescript
// ✅ AFTER (CORRECT)
export const calculateCartTotal = (cart: Cart): number => {
  const subtotal = cart.items.reduce((sum, item) => sum + item.price * item.quantity, 0)
  
  // Fix: Apply discounts sequentially
  let total = subtotal
  
  // Step 1: Apply voucher discount
  if (cart.voucher) {
    const voucherDiscount = total * (cart.voucher.percentage / 100)
    total = total - voucherDiscount
  }
  
  // Step 2: Apply loyalty points to discounted total
  if (cart.loyaltyPoints) {
    const pointsDiscount = Math.min(
      cart.loyaltyPoints * 0.01,  // 100 points = $1
      total  // Cannot discount more than remaining total
    )
    total = total - pointsDiscount
  }
  
  return Math.max(total, 0)  // Ensure non-negative
}
```

### Test Cases Added

```typescript
// test.cart-calculation.test.ts
describe('calculateCartTotal - Multiple Discounts', () => {
  it('should apply voucher then loyalty points sequentially', () => {
    const cart: Cart = {
      items: [{ price: 100, quantity: 1 }],
      voucher: { percentage: 20 },  // 20% off
      loyaltyPoints: 500,  // $5 off
    }
    
    // Expected: $100 → $80 (voucher) → $75 (points)
    expect(calculateCartTotal(cart)).toBe(75)
  })
  
  it('should not allow negative total', () => {
    const cart: Cart = {
      items: [{ price: 10, quantity: 1 }],
      voucher: { percentage: 50 },  // $5 after voucher
      loyaltyPoints: 1000,  // $10 off (more than remaining)
    }
    
    // Expected: $10 → $5 (voucher) → $0 (capped at 0)
    expect(calculateCartTotal(cart)).toBe(0)
  })
  
  it('should handle voucher only', () => {
    const cart: Cart = {
      items: [{ price: 100, quantity: 1 }],
      voucher: { percentage: 20 },
      loyaltyPoints: 0,
    }
    
    expect(calculateCartTotal(cart)).toBe(80)
  })
  
  it('should handle loyalty points only', () => {
    const cart: Cart = {
      items: [{ price: 100, quantity: 1 }],
      voucher: null,
      loyaltyPoints: 500,
    }
    
    expect(calculateCartTotal(cart)).toBe(95)
  })
})
```

---

## 📊 Verification

### Before Fix

```bash
# Test case: $100 cart + 20% voucher + 500 points
Input: subtotal=$100, voucher=20%, points=500
Expected: $75
Actual: $76 ❌
Error: $1 overcharge
```

### After Fix

```bash
# Same test case
Input: subtotal=$100, voucher=20%, points=500
Expected: $75
Actual: $75 ✅
Error: $0
```

### Test Results

```bash
npm test -- cart-calculation.test.ts

PASS  src/services/cart/test.cart-calculation.test.ts
  calculateCartTotal - Multiple Discounts
    ✓ should apply voucher then loyalty points sequentially (3ms)
    ✓ should not allow negative total (2ms)
    ✓ should handle voucher only (1ms)
    ✓ should handle loyalty points only (2ms)

Test Suites: 1 passed, 1 total
Tests:       4 passed, 4 total
```

---

## 📝 Files Changed

| File | Changes | Lines |
|------|---------|-------|
| `src/services/cart/service.cart-calculation.ts` | Fixed discount logic | +15 -8 |
| `src/services/cart/test.cart-calculation.test.ts` | Added test cases | +45 -0 |
| `docs/business-logic/discounts.md` | Documented discount order | +12 -0 |

---

## 🔄 Deployment

### Steps

```bash
# 1. Run tests
npm test

# 2. Build
npm run build

# 3. Deploy to staging
npm run deploy:staging

# 4. Verify in staging
npm run test:e2e -- cart-checkout.spec.ts

# 5. Deploy to production
npm run deploy:production

# 6. Monitor
npm run monitor:production
```

### Rollout

- **Deployed to staging**: 2026-04-18 14:30 UTC
- **Staging verification**: 2026-04-18 15:00 UTC (passed)
- **Deployed to production**: 2026-04-18 16:00 UTC
- **Production verification**: 2026-04-18 16:15 UTC (passed)

---

## 💰 Customer Impact Resolution

### Affected Users

```sql
-- Query to find affected orders
SELECT 
  order_id,
  user_id,
  cart_total_displayed,
  amount_charged,
  (amount_charged - cart_total_displayed) as overcharge
FROM orders
WHERE 
  created_at >= '2026-04-11'
  AND voucher_id IS NOT NULL
  AND loyalty_points_used > 0
  AND amount_charged > cart_total_displayed;

-- Result: 234 orders, total overcharge $3,247
```

### Refund Process

- **Affected orders**: 234
- **Total refunds**: $3,247
- **Refund method**: Automatic credit to user wallet
- **Notification**: Email sent to all affected users
- **Completion**: 2026-04-19 12:00 UTC

---

## 📚 Lessons Learned

### What Went Well

1. **Fast detection**: User reports flagged issue within 24 hours
2. **Clear reproduction**: Easy to reproduce with test data
3. **Quick fix**: Root cause identified and fixed in 4 hours

### What Could Be Improved

1. **Test coverage**: Should have tested multiple discount combinations
2. **Code review**: Logic error not caught in review
3. **Staging tests**: E2E tests only used single discount scenarios

### Prevention Measures

1. **Testing**: 
   - Added comprehensive discount combination tests
   - Updated E2E tests to cover edge cases
   - Added property-based testing for discount logic

2. **Documentation**: 
   - Documented discount application order
   - Added business logic diagrams
   - Updated code review checklist

3. **Monitoring**: 
   - Added alert for cart total vs charge mismatch
   - Dashboard for discount usage patterns

---

## 🔗 References

- **Issue**: #BUG-2026-04-18-042
- **PR**: #1247 (Fix cart discount calculation)
- **Commit**: `a3f9d2e` - Fix sequential discount application
- **Related**: #BUG-2026-03-15-028 (Similar voucher issue)

---

## 👥 Team

- **Developer**: John Doe
- **Reviewer**: Jane Smith
- **QA**: Bob Wilson
- **Product**: Carol Lee (approved refund process)

---

**Bug Type**: Logic Error  
**Component**: Cart Service  
**Fix Time**: 4 hours (detection to production)  
**Test Coverage**: 85% → 95%
