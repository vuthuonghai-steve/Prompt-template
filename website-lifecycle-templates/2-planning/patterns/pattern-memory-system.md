# Pattern: Memory System

## Nguồn
- Claude Code
- Cursor Agent
- Windsurf Cascade

## Mô tả
Persistent memory system để lưu trữ context, decisions, lessons learned qua các sessions. Tránh repeat mistakes, maintain consistency.

## Khi nào dùng
- Planning: document architecture decisions
- Development: track coding patterns, conventions
- Testing: remember common bugs, edge cases
- Maintenance: log incidents, fixes, optimizations

## Cách áp dụng

### 1. Memory Types
```typescript
type MemoryType = 
  | 'user'        // User preferences, context
  | 'feedback'    // Corrections, guidance
  | 'project'     // Project state, decisions
  | 'reference'   // External resources, links

interface Memory {
  id: string
  type: MemoryType
  title: string
  content: string
  tags: string[]
  createdAt: Date
  updatedAt: Date
  relevance: number // 0-1
}
```

### 2. Memory Structure
```markdown
---
type: project
tags: [architecture, database, decision]
created: 2026-04-22
---

# Decision: Use MongoDB over PostgreSQL

## Context
E-commerce flower shop với flexible product attributes,
frequent schema changes expected.

## Decision
Chọn MongoDB Atlas

## Rationale
- Flexible schema cho product variations
- Easy horizontal scaling
- Team familiar với MongoDB
- Atlas managed service giảm DevOps overhead

## Trade-offs
- Lose ACID transactions (mitigated by careful design)
- No foreign key constraints (handle in application)
- Query complexity higher cho joins

## Outcome
- Setup time: 2 hours (vs 1 day for PostgreSQL + migrations)
- Development velocity: +30% (no migration overhead)
- Performance: Acceptable for MVP scale
```

### 3. Memory Retrieval
```typescript
interface MemoryQuery {
  type?: MemoryType
  tags?: string[]
  searchText?: string
  minRelevance?: number
}

function retrieveMemories(query: MemoryQuery): Memory[] {
  let results = allMemories
  
  if (query.type) {
    results = results.filter((m) => m.type === query.type)
  }
  
  if (query.tags) {
    results = results.filter((m) =>
      query.tags.some((tag) => m.tags.includes(tag))
    )
  }
  
  if (query.searchText) {
    results = results.filter((m) =>
      m.content.toLowerCase().includes(query.searchText.toLowerCase())
    )
  }
  
  if (query.minRelevance) {
    results = results.filter((m) => m.relevance >= query.minRelevance)
  }
  
  return results.sort((a, b) => b.relevance - a.relevance)
}
```

## Ví dụ thực tế

### Project Memory: Architecture Decisions

```markdown
# Memory: Architecture Decision Records (ADRs)

## ADR-001: Monorepo Structure
**Date**: 2026-04-15
**Status**: Accepted

**Context**: Cần quản lý frontend, backend, shared code.

**Decision**: Monorepo với pnpm workspaces

**Consequences**:
- ✅ Shared types, utils
- ✅ Atomic commits across packages
- ❌ Longer CI times (mitigated by caching)

---

## ADR-002: State Management
**Date**: 2026-04-16
**Status**: Accepted

**Context**: Complex cart, checkout state.

**Decision**: Redux Toolkit + RTK Query

**Consequences**:
- ✅ Predictable state updates
- ✅ Built-in caching, optimistic updates
- ❌ Boilerplate (acceptable for team size)

---

## ADR-003: Payment Integration
**Date**: 2026-04-18
**Status**: Accepted

**Context**: Support VNPay, Momo, future gateways.

**Decision**: Abstract payment gateway interface

**Consequences**:
- ✅ Easy add new gateways
- ✅ Testable without real API calls
- ❌ Initial abstraction overhead
```

### Feedback Memory: Lessons Learned

```markdown
# Memory: Lessons Learned

## Lesson: Always validate payment webhooks
**Date**: 2026-04-20
**Context**: Production incident - fake payment confirmations

**What happened**:
Attacker sent fake webhook requests, orders marked as paid.

**Root cause**:
Không verify webhook signature từ payment gateway.

**Fix**:
```typescript
function verifyWebhook(payload: any, signature: string): boolean {
  const expectedSignature = crypto
    .createHmac('sha256', WEBHOOK_SECRET)
    .update(JSON.stringify(payload))
    .digest('hex')
  
  return crypto.timingSafeEqual(
    Buffer.from(signature),
    Buffer.from(expectedSignature)
  )
}
```

**Prevention**:
- ✅ Add webhook signature verification
- ✅ Add security checklist to code review
- ✅ Add integration test for webhook security

---

## Lesson: Cache product data aggressively
**Date**: 2026-04-21
**Context**: Slow product listing page (2-3s load)

**What happened**:
Mỗi request fetch full product data từ DB.

**Root cause**:
Không có caching strategy.

**Fix**:
```typescript
// Redis cache với 5 min TTL
async function getProducts(filters: ProductFilters) {
  const cacheKey = `products:${JSON.stringify(filters)}`
  
  const cached = await redis.get(cacheKey)
  if (cached) return JSON.parse(cached)
  
  const products = await db.products.find(filters)
  await redis.setex(cacheKey, 300, JSON.stringify(products))
  
  return products
}
```

**Outcome**:
- Load time: 2-3s → 200-300ms
- DB load: -80%
```

## Memory Maintenance

### Regular Review
```typescript
// Monthly memory review
interface MemoryReview {
  outdated: Memory[]      // Cần update hoặc xóa
  relevant: Memory[]      // Vẫn còn giá trị
  needsUpdate: Memory[]   // Cần bổ sung thông tin
}

function reviewMemories(memories: Memory[]): MemoryReview {
  const now = new Date()
  const threeMonthsAgo = new Date(now.getTime() - 90 * 24 * 60 * 60 * 1000)
  
  return {
    outdated: memories.filter((m) => 
      m.updatedAt < threeMonthsAgo && m.relevance < 0.3
    ),
    relevant: memories.filter((m) => m.relevance >= 0.7),
    needsUpdate: memories.filter((m) =>
      m.updatedAt < threeMonthsAgo && m.relevance >= 0.5
    ),
  }
}
```

## Trade-offs

| Ưu điểm | Nhược điểm |
|---------|------------|
| Avoid repeat mistakes | Maintenance overhead |
| Faster onboarding | Can become outdated |
| Consistent decisions | Cần discipline update |

## Best Practices
1. **Write immediately**: Capture context while fresh
2. **Tag consistently**: Use standard taxonomy
3. **Review regularly**: Monthly cleanup
4. **Link related memories**: Create knowledge graph
5. **Update relevance**: Decay old memories
6. **Share with team**: Memory là team asset

## Anti-patterns
- ❌ Write vague memories ("something went wrong")
- ❌ Không tag hoặc categorize
- ❌ Never review/update
- ❌ Keep outdated memories
- ❌ Memory silos (không share)

## Related Patterns
- [Plan Mode](./pattern-plan-mode.md)
- [Todo Management](./pattern-todo-management.md)
