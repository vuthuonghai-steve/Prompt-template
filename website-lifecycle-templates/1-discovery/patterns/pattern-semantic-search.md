# Pattern: Semantic Search

## Nguồn
- Claude Code
- Cursor Agent
- Perplexity

## Mô tả
Tìm kiếm dựa trên ngữ nghĩa thay vì keyword matching đơn thuần. Hiểu ý định người dùng và context để trả về kết quả relevant.

## Khi nào dùng
- Discovery phase: tìm hiểu requirements từ stakeholders
- Research competitors, market trends
- Phân tích user feedback, reviews
- Tìm kiếm tài liệu, best practices

## Cách áp dụng

### 1. Context Gathering
```
Thay vì: "tìm hoa hồng"
Dùng: "tìm sản phẩm hoa phù hợp cho đám cưới mùa hè, 
       ngân sách 5-10 triệu, phong cách romantic"
```

### 2. Multi-dimensional Search
- Kết hợp nhiều tiêu chí: occasion, budget, style, season
- Rank theo relevance score
- Filter theo constraints

### 3. Learning from Feedback
- Track click-through rate
- Adjust ranking algorithm
- Refine semantic understanding

## Ví dụ thực tế

### E-commerce Flower Shop
```typescript
// Semantic search query
interface SearchQuery {
  intent: 'gift' | 'decoration' | 'event'
  occasion?: string
  budget?: { min: number; max: number }
  style?: string[]
  season?: string
  recipient?: string
}

// Semantic matching
function semanticMatch(product: Product, query: SearchQuery): number {
  let score = 0
  
  // Intent matching
  if (product.tags.includes(query.intent)) score += 10
  
  // Occasion matching
  if (query.occasion && product.occasions.includes(query.occasion)) {
    score += 8
  }
  
  // Budget matching
  if (query.budget) {
    const inBudget = product.price >= query.budget.min && 
                     product.price <= query.budget.max
    if (inBudget) score += 5
  }
  
  // Style matching
  if (query.style) {
    const styleMatch = query.style.filter(s => 
      product.styles.includes(s)
    ).length
    score += styleMatch * 3
  }
  
  return score
}
```

## Trade-offs

| Ưu điểm | Nhược điểm |
|---------|------------|
| Kết quả relevant hơn | Phức tạp hơn keyword search |
| Hiểu intent người dùng | Cần training data |
| Flexible với natural language | Performance overhead |

## Best Practices
1. Combine với keyword search làm fallback
2. Cache frequent queries
3. A/B test ranking algorithms
4. Monitor search analytics
5. Continuously refine semantic model

## Related Patterns
- [Context Gathering](./pattern-context-gathering.md)
- [Parallel Tool Calls](./pattern-parallel-tool-calls.md)
