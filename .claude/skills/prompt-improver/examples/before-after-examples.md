# Before & After Examples

Cac vi du thuc te ve cai thien prompt tu "te" thanh "tot".

---

## Example 1: Mo Ho -> Cu The

### BEFORE (Score: 8/25)
```
Fix the login issue
```

**Van de:**
- Khong biet "issue" la gi
- Khong biet file nao
- Khong biet expected behavior

### AFTER (Score: 23/25)
```markdown
## Context
- Project: SiinStore API (Next.js + PayloadCMS)
- File: src/app/api/v1/auth/login/route.ts
- Environment: Development (localhost:3010)

## Problem
Login fails silently when user enters correct credentials but account is inactive.

**Expected:** Return 403 with message "Tai khoan chua duoc kich hoat"
**Actual:** Returns 200 success but user cannot access protected routes

## Task
Fix the login endpoint to properly check account status before returning success.

## Constraints
- Use existing `errorResponse` helper
- Check `user.status === 'active'` before success
- Do NOT modify the successful login flow

## Verification
- [ ] Inactive account returns 403
- [ ] Active account can login normally
- [ ] Error message is in Vietnamese
```

---

## Example 2: Overload -> Focused

### BEFORE (Score: 10/25)
```
Create a product page with images, reviews, cart button, related products,
SEO tags, loading states, error handling, responsive design, animations,
and make it fast and accessible
```

**Van de:**
- Qua nhieu yeu cau
- Khong co priority
- Khong co chi tiet

### AFTER (Score: 22/25)
```markdown
## Context
- Project: SiinStore Frontend (Next.js 15)
- Location: src/screens/product/ProductDetailScreen.tsx
- Design System: src/components/ui/

## Task
Create Product Detail page - Phase 1 (Core functionality only)

## Requirements (This Phase)
1. **Product Gallery**
   - Display product images in carousel
   - Support zoom on click
   - Responsive: 1 column mobile, 2 columns desktop

2. **Product Info Section**
   - Name, price, description
   - Stock status indicator
   - Variant selector (size, color)

3. **Add to Cart**
   - Quantity selector
   - Add to cart button
   - Success feedback

## Out of Scope (Next Phase)
- Reviews section
- Related products
- SEO optimization
- Advanced animations

## Technical Requirements
- Use existing UI components
- Follow screen pattern (logic in Screen, wrapper in app/)
- Mobile-first responsive

## Output
- Single file: ProductDetailScreen.tsx
- Export from src/screens/product/index.ts
```

---

## Example 3: Thieu Context -> Day Du

### BEFORE (Score: 12/25)
```
Add validation to the form
```

**Van de:**
- Form nao?
- Validation rules gi?
- Validation o dau (client/server)?

### AFTER (Score: 24/25)
```markdown
## Context
- Project: SiinStore Web
- File: src/screens/auth/RegisterScreen.tsx
- Form Library: React Hook Form + Zod

## Current State
Registration form has no client-side validation.
Users can submit empty or invalid data.

## Task
Add client-side validation to registration form.

## Form Fields & Rules

| Field | Type | Validation |
|-------|------|------------|
| `name` | text | Required, 2-50 chars |
| `email` | email | Required, valid email format |
| `phone` | tel | Required, VN phone format (10 digits, start with 0) |
| `password` | password | Required, min 8 chars, 1 uppercase, 1 number |
| `confirmPassword` | password | Must match password |

## Implementation Approach
1. Create Zod schema in `src/lib/validations/auth.ts`
2. Use `useForm` with `zodResolver`
3. Display errors below each field
4. Disable submit button when form invalid

## Error Messages (Vietnamese)
- Required: "Truong nay bat buoc"
- Email invalid: "Email khong hop le"
- Phone invalid: "So dien thoai khong hop le"
- Password weak: "Mat khau phai co it nhat 8 ky tu, 1 chu hoa, 1 so"
- Password mismatch: "Mat khau khong khop"

## Expected Output
- Updated RegisterScreen.tsx
- New file: src/lib/validations/auth.ts
```

---

## Example 4: Khong Co Vi Du -> Co Vi Du

### BEFORE (Score: 14/25)
```
Create a function to format Vietnamese currency
```

**Van de:**
- Khong biet input/output format
- Khong biet edge cases
- Khong biet style mong doi

### AFTER (Score: 25/25)
```markdown
## Context
- Project: SiinStore Web
- Location: src/utils/format.ts
- Usage: Display prices throughout the app

## Task
Create `formatCurrency` function for Vietnamese Dong (VND).

## Specification

**Function Signature:**
```typescript
function formatCurrency(amount: number, options?: FormatOptions): string
```

**Options:**
```typescript
interface FormatOptions {
  showSymbol?: boolean  // default: true
  compact?: boolean     // default: false (for large numbers)
}
```

## Examples

| Input | Options | Output |
|-------|---------|--------|
| `1000000` | default | `"1.000.000 d"` |
| `1000000` | `{showSymbol: false}` | `"1.000.000"` |
| `1500000` | `{compact: true}` | `"1,5tr d"` |
| `0` | default | `"0 d"` |
| `-50000` | default | `"-50.000 d"` |
| `1234567890` | `{compact: true}` | `"1,23ty d"` |

## Edge Cases
- Negative numbers: Show minus sign
- Zero: Show "0 d"
- Decimals: Round to nearest integer
- Very large numbers: Use compact format if enabled

## Constraints
- Use "d" symbol (not "VND" or "dong")
- Use dot (.) as thousand separator
- No decimals for VND
- Compact format: tr = trieu (million), ty = ty (billion)
```

---

## Example 5: Conflicting -> Clear

### BEFORE (Score: 9/25)
```
Make it fast but also add detailed logging and comprehensive error handling
with full stack traces and also keep it simple and minimal
```

**Van de:**
- "fast" vs "detailed logging" conflict
- "comprehensive" vs "simple minimal" conflict
- Khong co priority

### AFTER (Score: 22/25)
```markdown
## Context
- Project: SiinStore API
- Environment: Production optimization needed
- Current Issue: API responses slow, hard to debug in production

## Task
Optimize API performance while maintaining debuggability.

## Approach: Balanced Performance + Debugging

### Performance (Priority 1)
- [ ] Add response caching (Redis, 5 min TTL)
- [ ] Optimize database queries (add indexes)
- [ ] Implement pagination (max 50 items/page)

### Logging (Priority 2)
- [ ] Log only: request method, path, status, duration
- [ ] Full stack trace ONLY for 5xx errors
- [ ] Use log levels: error (5xx), warn (4xx), info (2xx)

### Error Handling (Priority 3)
- [ ] Catch and wrap errors with user-friendly messages
- [ ] Return minimal error info to client
- [ ] Store full error details in server logs only

## Trade-off Decisions
| Aspect | Decision | Reason |
|--------|----------|--------|
| Logging detail | Minimal in prod | Performance |
| Stack traces | Only 5xx | Security + performance |
| Error messages | Generic to client | Security |
| Debug mode | ENV-based toggle | Flexibility |

## Expected Outcome
- Response time < 200ms for cached requests
- Easy to debug with log aggregation
- No sensitive info leaked to clients
```

---

## Example 6: No Structure -> Well Organized

### BEFORE (Score: 11/25)
```
I need to build an e-commerce checkout flow that handles multiple payment
methods like credit card and bank transfer and also COD and it needs to
validate the shipping address and calculate shipping costs based on the
destination and apply vouchers if the user has any and then create the
order and send confirmation email and also update inventory
```

**Van de:**
- Single paragraph, hard to parse
- No clear steps
- No priority

### AFTER (Score: 24/25)
```markdown
## Feature: E-commerce Checkout Flow

### Context
- Project: SiinStore API + Web
- Payment Gateway: VNPay (credit card), Bank Transfer (manual)
- Shipping: GHN API for cost calculation

---

## Phase 1: Core Checkout (This Task)

### Step 1: Validate Cart
- [ ] Check all items in stock
- [ ] Verify prices haven't changed
- [ ] Calculate subtotal

### Step 2: Shipping
- [ ] Validate shipping address (required fields)
- [ ] Calculate shipping cost via GHN API
- [ ] Show estimated delivery date

### Step 3: Payment Selection
- [ ] COD (Cash on Delivery)
- [ ] Bank Transfer (show bank details)
- [ ] Credit Card (VNPay redirect)

### Step 4: Voucher Application
- [ ] Validate voucher code
- [ ] Check eligibility (min order, expiry)
- [ ] Apply discount

### Step 5: Order Creation
- [ ] Create order record
- [ ] Reserve inventory
- [ ] Generate order number

---

## Phase 2: Post-Order (Next Task)
- Send confirmation email
- Process payment callback
- Update final inventory

---

## Technical Requirements
- Use transactions for order creation
- Implement idempotency for payment
- Log all steps for debugging

## Output for Phase 1
- API: POST /api/v1/checkout
- Files: src/app/api/v1/checkout/route.ts
- Service: src/services/checkout/checkout-service.ts
```

---

## PATTERNS SUMMARY

| Problem | Solution Pattern |
|---------|-----------------|
| Mo ho | Add specific details: files, line numbers, exact behavior |
| Overload | Split into phases, prioritize, focus on one thing |
| Thieu context | Add project, environment, related files |
| Khong co vi du | Add input/output examples with edge cases |
| Mau thuan | Make explicit trade-offs, state priorities |
| Khong co cau truc | Use headers, bullet points, tables, numbered steps |

---

## QUICK FIX REFERENCE

| Phrase in prompt | Replace with |
|-----------------|--------------|
| "Fix it" | "Fix [specific issue] in [file] so that [expected behavior]" |
| "Make it better" | "Improve [metric] by [approach] to achieve [target]" |
| "Add feature" | "Add [feature] with [requirements] at [location]" |
| "Something is wrong" | "[Expected] but [actual] when [steps to reproduce]" |
| "Like the other one" | Reference specific file/function/pattern |
