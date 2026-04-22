# Pattern: Semantic Code Search

## Nguồn
- VSCode Agent
- Cursor Agent
- Windsurf Cascade

## Mô tả
Tìm kiếm code bằng natural language thay vì exact text matching. Query strategy: broad → narrow với file/directory scoping.

## Khi nào dùng
- Development: Explore unfamiliar codebase
- Debugging: Tìm root cause của bug
- Refactoring: Identify all usages của function/component
- Code review: Understand implementation patterns

## Cách áp dụng

### 1. Query Strategy: Broad → Narrow

```typescript
// ❌ Exact text search (limited)
grep "calculateTotal" src/

// ✅ Semantic search (comprehensive)
// Query 1: "How is order total calculated?"
// → Finds: calculateTotal, computeOrderAmount, getTotalPrice

// Query 2: "Where do we handle payment processing?"
// → Finds: processPayment, handleStripeWebhook, validatePaymentMethod

// Query 3: "Show me all product filtering logic"
// → Finds: filterProducts, applyFilters, ProductFilters component
```

### 2. Scoped Search

```typescript
interface SearchQuery {
  query: string
  scope?: {
    directories?: string[]
    fileTypes?: string[]
    excludePatterns?: string[]
  }
}

// Example: Find authentication logic in backend only
const query: SearchQuery = {
  query: "user authentication and session management",
  scope: {
    directories: ["src/api", "src/services"],
    fileTypes: [".ts", ".js"],
    excludePatterns: ["*.test.ts", "*.spec.ts"],
  },
}
```

### 3. Progressive Refinement

```typescript
// Step 1: Broad search
"How do we handle product inventory?"
// Results: 50 files

// Step 2: Narrow by directory
"How do we handle product inventory?" + scope: src/services/
// Results: 12 files

// Step 3: Narrow by specific aspect
"How do we update inventory after order?"
// Results: 3 files (exactly what we need)
```

## Ví dụ thực tế

### E-commerce: Debug Cart Calculation Bug

```typescript
// Problem: Cart total sometimes incorrect

// Step 1: Semantic search
Query: "Where is cart total calculated?"
Results:
- src/services/cart/service.cart.ts (calculateTotal method)
- src/hooks/use-cart/hook.use-cart.ts (cart reducer)
- src/components/cart/CartSummary.tsx (display logic)

// Step 2: Narrow to calculation logic
Query: "How do we apply discounts to cart total?"
Results:
- src/services/cart/service.cart.ts (applyDiscount method)
- src/services/voucher/service.voucher.ts (validateVoucher)

// Step 3: Find the bug
Query: "Where do we calculate shipping cost?"
Results:
- src/services/cart/service.cart.ts (calculateShipping)
// Bug found: Shipping calculated before discount, should be after
```

### E-commerce: Understand Payment Flow

```typescript
// New developer needs to understand payment integration

// Query 1: High-level overview
"How does payment processing work?"
Results:
- src/services/payment/service.payment.ts (main service)
- src/api/webhooks/payment.ts (webhook handlers)
- docs/payment-integration.md (documentation)

// Query 2: Specific gateway
"How do we integrate with VNPay?"
Results:
- src/services/payment/vnpay.ts (VNPay implementation)
- src/types/payment.ts (VNPay types)
- tests/payment/vnpay.test.ts (test cases)

// Query 3: Error handling
"How do we handle payment failures?"
Results:
- src/services/payment/service.payment.ts (error handling)
- src/hooks/use-payment/hook.use-payment.ts (UI error states)
```

### E-commerce: Find All Product Filtering

```typescript
// Task: Refactor product filtering logic

// Query: "Show me all product filtering implementations"
Results:
1. src/services/product/service.product.ts
   - buildQueryParams method
   - Converts filters to API params

2. src/hooks/use-products/hook.use-products.ts
   - useProducts hook with filters
   - React Query integration

3. src/components/products/ProductFilters.tsx
   - UI for filter selection
   - State management

4. src/types/product.ts
   - ProductFilters interface
   - Type definitions

// Now we know exactly what to refactor
```

## Semantic Search vs Traditional Search

| Aspect | Traditional (grep/find) | Semantic Search |
|--------|------------------------|-----------------|
| Query | Exact text match | Natural language |
| Results | Literal matches only | Conceptually related |
| Scope | File/directory only | Semantic understanding |
| Refinement | Manual filtering | Progressive narrowing |
| Learning curve | Low | Medium |

## Implementation với AI Tools

### VSCode Agent / Cursor

```typescript
// Use semantic search command
// VSCode: Cmd+Shift+P → "Search: Semantic Search"
// Cursor: Cmd+K → Type natural language query

// Example queries:
"Where do we validate user input?"
"How is authentication implemented?"
"Show me all API error handling"
"Find product recommendation logic"
```

### Custom Implementation

```typescript
// Semantic search service
class SemanticSearchService {
  async search(query: string, options?: SearchOptions): Promise<SearchResult[]> {
    // 1. Parse natural language query
    const intent = await this.parseIntent(query)
    
    // 2. Generate search terms
    const terms = await this.generateSearchTerms(intent)
    
    // 3. Search codebase
    const results = await this.searchCode(terms, options?.scope)
    
    // 4. Rank by relevance
    return this.rankResults(results, intent)
  }
  
  private async parseIntent(query: string): Promise<SearchIntent> {
    // Use LLM to understand query intent
    // "How is payment processed?" → intent: "payment_processing"
  }
  
  private async generateSearchTerms(intent: SearchIntent): Promise<string[]> {
    // Generate related terms
    // "payment_processing" → ["processPayment", "handlePayment", "PaymentService"]
  }
}
```

## Best Practices

### Do's
✅ Start broad, narrow progressively
✅ Use natural language queries
✅ Scope to relevant directories
✅ Combine with traditional search
✅ Verify results manually

### Don'ts
❌ Rely solely on semantic search
❌ Skip manual code review
❌ Ignore false positives
❌ Over-narrow initial query
❌ Forget to scope large codebases

## Trade-offs

| Ưu điểm | Nhược điểm |
|---------|------------|
| Find conceptually related code | May return false positives |
| Natural language queries | Requires AI/LLM integration |
| Discover unknown patterns | Slower than grep |
| Better for exploration | Less precise than exact match |

## Related Patterns
- [Context Gathering](../../1-discovery/patterns/pattern-context-gathering.md)
- [Parallel Tool Calls](../../1-discovery/patterns/pattern-parallel-tool-calls.md)
