# Pattern: Chain-of-Thought Planning

## Nguồn
- Claude Code
- OpenAI o1
- Gemini

## Mô tả
Explicit reasoning process before action - break down complex problems into steps, consider alternatives, and document decision rationale.

## Khi nào dùng
- Complex problem solving
- Architecture decisions
- Debugging unclear issues
- Multi-step implementations
- Trade-off analysis

## Cách áp dụng

### 1. Chain-of-Thought Structure

```
1. UNDERSTAND
   ├── What is the problem?
   ├── What are the constraints?
   └── What is the desired outcome?

2. ANALYZE
   ├── What are possible approaches?
   ├── What are the trade-offs?
   └── What are the risks?

3. DECIDE
   ├── Which approach is best?
   ├── Why this approach?
   └── What are the next steps?

4. PLAN
   ├── Break into concrete steps
   ├── Identify dependencies
   └── Define success criteria

5. EXECUTE
   └── Implement the plan
```

### 2. Explicit Reasoning Format

```markdown
## Problem
[Clear statement of what needs to be solved]

## Analysis
**Option 1**: [Approach]
- Pros: [Benefits]
- Cons: [Drawbacks]
- Complexity: [Low/Medium/High]

**Option 2**: [Approach]
- Pros: [Benefits]
- Cons: [Drawbacks]
- Complexity: [Low/Medium/High]

## Decision
**Chosen**: Option 1
**Rationale**: [Why this is the best choice given constraints]

## Implementation Plan
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Success Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]
```

## Ví dụ thực tế

### E-commerce: Shopping Cart State Management

```markdown
## Problem
Need to implement shopping cart state management for flower shop e-commerce.
Requirements:
- Persist across page refreshes
- Support add/remove/update quantity
- Calculate totals automatically
- Sync across multiple tabs

## Analysis

**Option 1: Redux + Redux Persist**
- Pros: 
  - Centralized state
  - Time-travel debugging
  - Well-established patterns
- Cons:
  - Boilerplate code
  - Learning curve for team
  - Overkill for simple cart
- Complexity: High

**Option 2: Context API + localStorage**
- Pros:
  - Built into React
  - Simple implementation
  - No extra dependencies
- Cons:
  - No time-travel debugging
  - Manual localStorage sync
  - No cross-tab sync
- Complexity: Medium

**Option 3: Zustand + localStorage middleware**
- Pros:
  - Minimal boilerplate
  - Built-in persistence
  - Simple API
  - Good TypeScript support
- Cons:
  - Less ecosystem than Redux
  - Team unfamiliar with it
- Complexity: Low

## Decision
**Chosen**: Option 2 (Context API + localStorage)

**Rationale**:
- Team already familiar with Context API
- Cart state is simple (add/remove/update)
- No need for time-travel debugging
- Can add cross-tab sync later if needed
- Keeps bundle size small
- Matches existing patterns in codebase

## Implementation Plan

1. Create CartContext with useReducer
   - Define CartItem type
   - Define cart actions (ADD, REMOVE, UPDATE_QUANTITY, CLEAR)
   - Implement reducer logic

2. Add localStorage persistence
   - Load cart from localStorage on mount
   - Save cart to localStorage on every change
   - Handle JSON parse errors

3. Create useCart hook
   - Expose cart state
   - Expose action functions (addItem, removeItem, etc.)
   - Calculate totals (subtotal, tax, shipping, total)

4. Integrate with components
   - Wrap app with CartProvider
   - Use useCart in ProductCard, Cart, Checkout

5. Add tests
   - Test reducer logic
   - Test localStorage sync
   - Test total calculations

## Success Criteria
- [ ] Cart persists across page refresh
- [ ] Can add/remove/update items
- [ ] Totals calculate correctly
- [ ] No console errors
- [ ] Tests pass
- [ ] TypeScript types correct
```

### E-commerce: Payment Gateway Integration

```markdown
## Problem
Integrate VNPay payment gateway for checkout flow.
Requirements:
- Support credit card and bank transfer
- Handle payment callbacks
- Verify payment signatures
- Handle payment failures gracefully

## Analysis

**Option 1: Direct API Integration**
- Pros:
  - Full control over flow
  - No middleman
  - Lower fees
- Cons:
  - Complex signature verification
  - Need to handle all edge cases
  - Security responsibility
- Complexity: High
- Risk: High (security)

**Option 2: Use VNPay SDK**
- Pros:
  - Signature verification handled
  - Tested by many users
  - Documentation available
- Cons:
  - SDK may be outdated
  - Less flexibility
  - Dependency on SDK updates
- Complexity: Medium
- Risk: Medium

**Option 3: Backend Proxy Pattern**
- Pros:
  - Secrets stay on server
  - Can add retry logic
  - Can log all transactions
  - Frontend stays simple
- Cons:
  - Extra API endpoint
  - Slightly slower
- Complexity: Medium
- Risk: Low

## Decision
**Chosen**: Option 3 (Backend Proxy Pattern)

**Rationale**:
- Security: API keys never exposed to frontend
- Maintainability: Payment logic centralized
- Flexibility: Can switch gateways without frontend changes
- Observability: All payments logged server-side
- Testing: Easier to mock in tests

## Implementation Plan

1. Backend: Create payment API endpoint
   - POST /api/payment/create
   - POST /api/payment/verify
   - POST /api/webhooks/vnpay (callback)

2. Backend: Implement VNPay integration
   - Generate payment URL with signature
   - Verify callback signature
   - Update order status
   - Handle errors and retries

3. Frontend: Create payment service
   - createPayment(orderId, amount)
   - verifyPayment(transactionId)
   - Handle redirects

4. Frontend: Update checkout flow
   - Call payment service on submit
   - Redirect to VNPay
   - Handle return from VNPay
   - Show success/failure

5. Add monitoring
   - Log all payment attempts
   - Alert on high failure rate
   - Track payment duration

## Success Criteria
- [ ] Can create payment successfully
- [ ] Signature verification works
- [ ] Callback updates order status
- [ ] Failed payments handled gracefully
- [ ] All payments logged
- [ ] Tests cover happy path and errors
```

### E-commerce: Product Search Optimization

```markdown
## Problem
Product search is slow (>2s) with 10,000+ products.
Current: Full-text search on every keystroke.

## Analysis

**Current State**:
- Database: MongoDB full-text index
- Query: Runs on every keystroke
- No caching
- No debouncing
- Returns all fields

**Bottlenecks Identified**:
1. Too many queries (every keystroke)
2. No caching (same queries repeated)
3. Returning unnecessary data (images, descriptions)
4. No pagination (loading all results)

**Option 1: Add Debouncing**
- Pros: Simple, immediate improvement
- Cons: Still slow queries, no caching
- Expected improvement: 50% fewer queries
- Complexity: Low

**Option 2: Add Redis Cache**
- Pros: Fast repeated queries
- Cons: Cache invalidation complexity
- Expected improvement: 90% faster for cached
- Complexity: Medium

**Option 3: Elasticsearch**
- Pros: Purpose-built for search, very fast
- Cons: New infrastructure, learning curve
- Expected improvement: 95% faster
- Complexity: High

**Option 4: Hybrid (Debounce + Cache + Optimize Query)**
- Pros: Best of all worlds, incremental
- Cons: Multiple changes to coordinate
- Expected improvement: 80% faster
- Complexity: Medium

## Decision
**Chosen**: Option 4 (Hybrid Approach)

**Rationale**:
- Incremental: Can implement in phases
- Cost-effective: No new infrastructure
- Proven: All techniques well-established
- Reversible: Can add Elasticsearch later if needed

**Phase 1**: Quick wins (Week 1)
- Add debouncing (300ms)
- Optimize query (only return needed fields)
- Add pagination (20 results)
- Expected: 60% improvement

**Phase 2**: Caching (Week 2)
- Add Redis cache
- Cache popular searches
- 5-minute TTL
- Expected: Additional 20% improvement

**Phase 3**: Advanced (Week 3)
- Add autocomplete
- Add search suggestions
- Track search analytics

## Implementation Plan

### Phase 1: Quick Wins
1. Frontend: Add debouncing
   ```typescript
   const debouncedSearch = useDebouncedCallback(
     (query) => searchProducts(query),
     300
   )
   ```

2. Backend: Optimize query
   ```typescript
   // Only return needed fields
   db.products.find(
     { $text: { $search: query } },
     { projection: { name: 1, price: 1, image: 1 } }
   ).limit(20)
   ```

3. Frontend: Add pagination
   - Load 20 results initially
   - Infinite scroll for more

### Phase 2: Caching
1. Add Redis
2. Cache key: `search:${query}`
3. TTL: 5 minutes
4. Invalidate on product update

### Phase 3: Advanced
1. Autocomplete endpoint
2. Search suggestions
3. Analytics tracking

## Success Criteria
- [ ] Search response time <500ms p95
- [ ] Debouncing reduces queries by 50%
- [ ] Cache hit rate >70%
- [ ] User satisfaction score >4/5
- [ ] No increase in error rate
```

## Chain-of-Thought in Code Comments

```typescript
// Problem: Need to calculate shipping fee based on district
// Analysis:
// - Option 1: Hardcode district -> fee mapping (simple but not scalable)
// - Option 2: Database lookup (flexible but slower)
// - Option 3: Config file (good balance)
// Decision: Option 3 - Config file
// Rationale: Easy to update, fast lookup, version controlled

const SHIPPING_FEES: Record<string, number> = {
  'district-1': 30000,
  'district-2': 35000,
  'district-3': 40000,
  // ... more districts
}

export function calculateShipping(district: string): number {
  // Default to highest fee if district not found
  // Rationale: Better to overcharge and refund than undercharge
  return SHIPPING_FEES[district] || 50000
}
```

## Best Practices

### Do's
✅ Write down reasoning before coding
✅ Consider multiple approaches
✅ Document trade-offs explicitly
✅ State assumptions clearly
✅ Define success criteria upfront
✅ Break complex problems into steps

### Don'ts
❌ Jump to implementation
❌ Consider only one approach
❌ Hide reasoning in your head
❌ Skip trade-off analysis
❌ Ignore constraints
❌ Make implicit assumptions

## Trade-offs

| Ưu điểm | Nhược điểm |
|---------|------------|
| Better decisions | Takes more time upfront |
| Clearer communication | More documentation |
| Easier to review | Can feel bureaucratic |
| Reduces rework | May over-analyze simple problems |

## Related Patterns
- [Spec-Driven Development](./pattern-spec-driven-development.md)
- [Tool Use Sequencing](./pattern-tool-use-sequencing.md)
