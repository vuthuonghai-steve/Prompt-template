# Pattern: Parallel Tool Calls

## Nguồn
- Claude Code
- Cursor Agent
- Windsurf Cascade

## Mô tả
Thực hiện nhiều operations độc lập song song thay vì tuần tự để tăng tốc độ execution.

## Khi nào dùng
- Discovery: research nhiều competitors cùng lúc
- Planning: analyze nhiều tech options song song
- Development: run multiple tests, linters, formatters
- Testing: parallel test execution

## Cách áp dụng

### 1. Identify Independent Operations
```typescript
// ❌ Sequential
const competitor1 = await analyzeCompetitor('shop1.com')
const competitor2 = await analyzeCompetitor('shop2.com')
const competitor3 = await analyzeCompetitor('shop3.com')

// ✅ Parallel
const [competitor1, competitor2, competitor3] = await Promise.all([
  analyzeCompetitor('shop1.com'),
  analyzeCompetitor('shop2.com'),
  analyzeCompetitor('shop3.com'),
])
```

### 2. Handle Errors Gracefully
```typescript
const results = await Promise.allSettled([
  operation1(),
  operation2(),
  operation3(),
])

results.forEach((result, index) => {
  if (result.status === 'fulfilled') {
    console.log(`Operation ${index} succeeded:`, result.value)
  } else {
    console.error(`Operation ${index} failed:`, result.reason)
  }
})
```

### 3. Limit Concurrency
```typescript
// Avoid overwhelming APIs/resources
async function parallelWithLimit<T>(
  items: T[],
  limit: number,
  fn: (item: T) => Promise<any>
) {
  const results = []
  for (let i = 0; i < items.length; i += limit) {
    const batch = items.slice(i, i + limit)
    const batchResults = await Promise.all(batch.map(fn))
    results.push(...batchResults)
  }
  return results
}
```

## Ví dụ thực tế

### Discovery: Competitor Analysis

```typescript
interface CompetitorData {
  name: string
  url: string
  pricing: { min: number; max: number }
  features: string[]
  strengths: string[]
  weaknesses: string[]
}

async function discoverCompetitors(
  urls: string[]
): Promise<CompetitorData[]> {
  // Parallel analysis
  const analyses = await Promise.allSettled(
    urls.map(async (url) => {
      const [pricing, features, reviews] = await Promise.all([
        scrapePricing(url),
        scrapeFeatures(url),
        scrapeReviews(url),
      ])
      
      return {
        name: extractName(url),
        url,
        pricing,
        features,
        strengths: analyzeStrengths(reviews),
        weaknesses: analyzeWeaknesses(reviews),
      }
    })
  )
  
  // Filter successful results
  return analyses
    .filter((r) => r.status === 'fulfilled')
    .map((r) => r.value)
}

// Usage
const competitors = await discoverCompetitors([
  'https://hoatuoi.com',
  'https://dalat-hasfarm.com',
  'https://flowercorner.vn',
])
```

### Discovery: Multi-source Research

```typescript
async function gatherRequirements(projectId: string) {
  // Parallel data gathering
  const [
    stakeholderInput,
    userFeedback,
    marketTrends,
    competitorFeatures,
    technicalConstraints,
  ] = await Promise.all([
    fetchStakeholderRequirements(projectId),
    fetchUserFeedback(projectId),
    researchMarketTrends('e-commerce flowers'),
    analyzeCompetitorFeatures(),
    assessTechnicalConstraints(projectId),
  ])
  
  return {
    stakeholderInput,
    userFeedback,
    marketTrends,
    competitorFeatures,
    technicalConstraints,
  }
}
```

## Performance Impact

| Approach | Time | Speedup |
|----------|------|---------|
| Sequential (3 operations × 2s) | 6s | 1x |
| Parallel (3 operations × 2s) | 2s | 3x |
| Parallel with limit (10 ops, limit 3) | ~7s | ~1.4x |

## Trade-offs

| Ưu điểm | Nhược điểm |
|---------|------------|
| Faster execution | Phức tạp hơn error handling |
| Better resource utilization | Có thể overwhelm APIs/servers |
| Improved UX (faster response) | Harder to debug |

## Best Practices
1. **Identify truly independent operations**: Đừng parallelize operations có dependencies
2. **Set concurrency limits**: Tránh overwhelm external services
3. **Handle partial failures**: Dùng `Promise.allSettled` thay vì `Promise.all` khi có thể
4. **Add timeouts**: Prevent hanging operations
5. **Monitor resource usage**: CPU, memory, network

## Anti-patterns
- ❌ Parallelize operations có dependencies
- ❌ Không limit concurrency
- ❌ Ignore errors trong parallel operations
- ❌ Parallelize quá nhiều làm overwhelm system

## Related Patterns
- [Context Gathering](./pattern-context-gathering.md)
- [Semantic Search](./pattern-semantic-search.md)
