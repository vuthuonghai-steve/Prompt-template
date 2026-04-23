# Performance Baseline Template

**Project**: [Project Name]  
**Date**: [YYYY-MM-DD]  
**Environment**: Development | Staging | Production  
**Baseline Version**: [e.g., v1.0.0]

---

## Executive Summary

**Purpose**: Establish performance baseline for [project name] to track improvements and detect regressions.

**Key Metrics**:
- Page Load Time: [e.g., 2.5s]
- Time to Interactive: [e.g., 3.2s]
- API Response Time: [e.g., 250ms]
- Database Query Time: [e.g., 50ms]

**Next Review**: [Date]

---

## Test Environment

### Infrastructure

| Component | Specification |
|-----------|---------------|
| **Server** | [e.g., AWS EC2 t3.medium] |
| **CPU** | [e.g., 2 vCPUs] |
| **Memory** | [e.g., 4GB RAM] |
| **Database** | [e.g., MongoDB 7.0, 2GB RAM] |
| **Network** | [e.g., 100 Mbps] |
| **CDN** | [e.g., Cloudflare] |

### Software Stack

| Component | Version |
|-----------|---------|
| **Node.js** | 20.x |
| **Next.js** | 15.4.4 |
| **React** | 19.1.0 |
| **MongoDB** | 7.0 |
| **Redis** | 7.2 |

### Test Conditions

- **Date/Time**: [YYYY-MM-DD HH:MM UTC]
- **Load**: [e.g., 10 concurrent users]
- **Network**: [e.g., Fast 3G, 4G, WiFi]
- **Device**: [e.g., Desktop Chrome, Mobile Safari]
- **Cache**: [e.g., Cold start, Warm cache]

---

## Frontend Performance

### Page Load Metrics (Lighthouse)

| Page | FCP | LCP | TTI | TBT | CLS | Score |
|------|-----|-----|-----|-----|-----|-------|
| **Homepage** | 1.2s | 2.1s | 2.8s | 150ms | 0.05 | 92 |
| **Product List** | 1.5s | 2.5s | 3.2s | 200ms | 0.08 | 88 |
| **Product Detail** | 1.3s | 2.3s | 3.0s | 180ms | 0.06 | 90 |
| **Cart** | 1.1s | 1.8s | 2.5s | 120ms | 0.03 | 94 |
| **Checkout** | 1.4s | 2.2s | 2.9s | 160ms | 0.07 | 89 |

**Metric Definitions**:
- **FCP** (First Contentful Paint): Time to first visible content
- **LCP** (Largest Contentful Paint): Time to largest content element
- **TTI** (Time to Interactive): Time until page is fully interactive
- **TBT** (Total Blocking Time): Time main thread is blocked
- **CLS** (Cumulative Layout Shift): Visual stability score

### Core Web Vitals

| Metric | Target | Current | Status |
|--------|--------|---------|--------|
| **LCP** | <2.5s | 2.3s | ✅ Good |
| **FID** | <100ms | 85ms | ✅ Good |
| **CLS** | <0.1 | 0.06 | ✅ Good |

### Bundle Size

| Bundle | Size (Gzipped) | Target | Status |
|--------|----------------|--------|--------|
| **Main JS** | 245 KB | <300 KB | ✅ |
| **Vendor JS** | 180 KB | <200 KB | ✅ |
| **CSS** | 45 KB | <50 KB | ✅ |
| **Total** | 470 KB | <550 KB | ✅ |

### Asset Optimization

| Asset Type | Count | Total Size | Avg Size | Optimized |
|------------|-------|------------|----------|-----------|
| **Images** | 25 | 1.2 MB | 48 KB | ✅ WebP |
| **Fonts** | 3 | 120 KB | 40 KB | ✅ WOFF2 |
| **Icons** | 1 | 15 KB | - | ✅ SVG Sprite |

---

## Backend Performance

### API Response Times

| Endpoint | Method | p50 | p95 | p99 | Target | Status |
|----------|--------|-----|-----|-----|--------|--------|
| `/api/products` | GET | 120ms | 250ms | 380ms | <300ms | ✅ |
| `/api/products/:id` | GET | 80ms | 150ms | 220ms | <200ms | ✅ |
| `/api/cart` | POST | 95ms | 180ms | 280ms | <250ms | ✅ |
| `/api/orders` | POST | 200ms | 450ms | 650ms | <500ms | ⚠️ |
| `/api/payment` | POST | 1200ms | 2500ms | 3800ms | <3000ms | ⚠️ |

**Legend**:
- ✅ Good: Within target
- ⚠️ Warning: Near target limit
- ❌ Critical: Exceeds target

### Database Query Performance

| Query | Collection | Avg Time | p95 | p99 | Index Used |
|-------|------------|----------|-----|-----|------------|
| Find products | products | 25ms | 45ms | 80ms | ✅ category_1 |
| Find by ID | products | 5ms | 10ms | 15ms | ✅ _id |
| User lookup | users | 8ms | 15ms | 25ms | ✅ email_1 |
| Order creation | orders | 35ms | 70ms | 120ms | ✅ userId_1 |
| Aggregation | orders | 150ms | 300ms | 500ms | ⚠️ Partial |

### Cache Hit Rates

| Cache Layer | Hit Rate | Miss Rate | Avg Latency |
|-------------|----------|-----------|-------------|
| **Redis (Products)** | 85% | 15% | 5ms |
| **Redis (Sessions)** | 92% | 8% | 3ms |
| **CDN (Static)** | 95% | 5% | 20ms |
| **Browser Cache** | 88% | 12% | 0ms |

---

## Load Testing Results

### Test Scenario: Normal Load

**Configuration**:
- Virtual Users: 50
- Duration: 10 minutes
- Ramp-up: 30 seconds

**Results**:

| Metric | Value |
|--------|-------|
| **Total Requests** | 15,000 |
| **Success Rate** | 99.8% |
| **Avg Response Time** | 180ms |
| **p95 Response Time** | 350ms |
| **p99 Response Time** | 520ms |
| **Requests/sec** | 25 |
| **Errors** | 30 (0.2%) |

### Test Scenario: Peak Load

**Configuration**:
- Virtual Users: 200
- Duration: 5 minutes
- Ramp-up: 1 minute

**Results**:

| Metric | Value |
|--------|-------|
| **Total Requests** | 24,000 |
| **Success Rate** | 98.5% |
| **Avg Response Time** | 450ms |
| **p95 Response Time** | 850ms |
| **p99 Response Time** | 1200ms |
| **Requests/sec** | 80 |
| **Errors** | 360 (1.5%) |

### Stress Test: Breaking Point

**Configuration**:
- Virtual Users: Ramp to 500
- Duration: 10 minutes

**Breaking Point**: 350 concurrent users

**Symptoms**:
- Response time >2s
- Error rate >5%
- CPU usage >90%
- Database connection pool exhausted

---

## Resource Utilization

### Server Metrics (Normal Load)

| Metric | Average | Peak | Threshold | Status |
|--------|---------|------|-----------|--------|
| **CPU Usage** | 35% | 55% | <70% | ✅ |
| **Memory Usage** | 2.1 GB | 2.8 GB | <3.5 GB | ✅ |
| **Disk I/O** | 15 MB/s | 30 MB/s | <50 MB/s | ✅ |
| **Network I/O** | 8 MB/s | 15 MB/s | <50 MB/s | ✅ |

### Database Metrics

| Metric | Average | Peak | Threshold | Status |
|--------|---------|------|-----------|--------|
| **Connections** | 25 | 45 | <80 | ✅ |
| **Query Time** | 35ms | 120ms | <200ms | ✅ |
| **CPU Usage** | 40% | 65% | <80% | ✅ |
| **Memory Usage** | 1.5 GB | 1.8 GB | <2 GB | ✅ |
| **Disk Usage** | 5 GB | - | <50 GB | ✅ |

### Redis Metrics

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| **Memory Usage** | 250 MB | <500 MB | ✅ |
| **Hit Rate** | 88% | >80% | ✅ |
| **Avg Latency** | 4ms | <10ms | ✅ |
| **Connections** | 15 | <50 | ✅ |

---

## Network Performance

### DNS Lookup

| Domain | Time | Status |
|--------|------|--------|
| www.example.com | 25ms | ✅ |
| api.example.com | 28ms | ✅ |
| cdn.example.com | 15ms | ✅ |

### SSL/TLS Handshake

| Domain | Time | Status |
|--------|------|--------|
| www.example.com | 120ms | ✅ |
| api.example.com | 115ms | ✅ |

### CDN Performance

| Region | Latency | Status |
|--------|---------|--------|
| **North America** | 45ms | ✅ |
| **Europe** | 80ms | ✅ |
| **Asia** | 120ms | ⚠️ |
| **Australia** | 180ms | ⚠️ |

---

## Mobile Performance

### Mobile Metrics (4G Network)

| Page | FCP | LCP | TTI | Score |
|------|-----|-----|-----|-------|
| **Homepage** | 2.1s | 3.5s | 4.2s | 78 |
| **Product List** | 2.5s | 4.0s | 5.0s | 72 |
| **Product Detail** | 2.3s | 3.8s | 4.5s | 75 |
| **Checkout** | 2.4s | 3.9s | 4.8s | 73 |

### Mobile Metrics (3G Network)

| Page | FCP | LCP | TTI | Score |
|------|-----|-----|-----|-------|
| **Homepage** | 4.2s | 6.5s | 8.0s | 52 |
| **Product List** | 5.0s | 7.5s | 9.5s | 45 |
| **Product Detail** | 4.5s | 7.0s | 8.5s | 48 |
| **Checkout** | 4.8s | 7.2s | 9.0s | 46 |

---

## E-Commerce Specific Metrics

### Checkout Flow Performance

| Step | Load Time | Completion Rate |
|------|-----------|-----------------|
| **Cart Review** | 1.8s | 95% |
| **Shipping Info** | 2.1s | 88% |
| **Payment** | 2.5s | 82% |
| **Confirmation** | 1.5s | 100% |

### Search Performance

| Query Type | Avg Time | p95 | Results Count |
|------------|----------|-----|---------------|
| **Simple** | 80ms | 150ms | 10-50 |
| **Filtered** | 120ms | 250ms | 5-30 |
| **Autocomplete** | 50ms | 100ms | 5-10 |

### Image Loading

| Image Type | Size | Load Time | Format |
|------------|------|-----------|--------|
| **Product Thumbnail** | 15 KB | 200ms | WebP |
| **Product Detail** | 80 KB | 500ms | WebP |
| **Hero Banner** | 120 KB | 800ms | WebP |

---

## Performance Bottlenecks

### Identified Issues

| Issue | Impact | Severity | Action |
|-------|--------|----------|--------|
| Order creation slow | p95 >450ms | Medium | Optimize DB query |
| Payment API timeout | p99 >3s | High | Add retry logic |
| Mobile 3G slow | Score <50 | Medium | Reduce bundle size |
| Asia CDN latency | >120ms | Low | Add Asia edge nodes |

### Optimization Opportunities

1. **Database Indexing**
   - Add compound index on `orders.userId_createdAt`
   - Expected improvement: 30% faster order queries

2. **API Caching**
   - Cache product list for 5 minutes
   - Expected improvement: 50% reduction in DB load

3. **Image Optimization**
   - Implement lazy loading
   - Expected improvement: 20% faster LCP

4. **Code Splitting**
   - Split checkout bundle
   - Expected improvement: 15% smaller initial bundle

---

## Monitoring & Alerting

### Alert Thresholds

| Metric | Warning | Critical |
|--------|---------|----------|
| **API Response Time** | >500ms | >1s |
| **Error Rate** | >1% | >5% |
| **CPU Usage** | >70% | >90% |
| **Memory Usage** | >80% | >95% |
| **Database Connections** | >60 | >75 |

### Monitoring Tools

- **Application**: New Relic / Datadog
- **Infrastructure**: CloudWatch / Grafana
- **Real User Monitoring**: Google Analytics
- **Synthetic Monitoring**: Pingdom / UptimeRobot

---

## Comparison with Targets

### Performance Targets

| Metric | Target | Current | Gap | Status |
|--------|--------|---------|-----|--------|
| **Homepage LCP** | <2.5s | 2.1s | -0.4s | ✅ |
| **API p95** | <300ms | 250ms | -50ms | ✅ |
| **Error Rate** | <1% | 0.2% | -0.8% | ✅ |
| **Lighthouse Score** | >90 | 92 | +2 | ✅ |
| **Mobile Score** | >70 | 78 | +8 | ✅ |

### Industry Benchmarks

| Metric | Industry Avg | Our Performance | Comparison |
|--------|--------------|-----------------|------------|
| **LCP** | 3.2s | 2.3s | 28% faster ✅ |
| **TTI** | 4.5s | 3.0s | 33% faster ✅ |
| **Bounce Rate** | 45% | 38% | 16% better ✅ |
| **Conversion Rate** | 2.5% | 3.2% | 28% better ✅ |

---

## Recommendations

### Immediate Actions (This Sprint)

1. **Optimize Order Creation**
   - Add database index
   - Expected: 30% improvement
   - Effort: 2 hours

2. **Implement API Caching**
   - Cache product list
   - Expected: 50% load reduction
   - Effort: 4 hours

### Short-term (Next Month)

1. **Image Lazy Loading**
   - Implement for product images
   - Expected: 20% faster LCP
   - Effort: 1 day

2. **Code Splitting**
   - Split checkout bundle
   - Expected: 15% smaller bundle
   - Effort: 2 days

### Long-term (Next Quarter)

1. **CDN Expansion**
   - Add Asia edge nodes
   - Expected: 40% faster Asia latency
   - Effort: 1 week

2. **Database Sharding**
   - Prepare for scale
   - Expected: 3x capacity
   - Effort: 2 weeks

---

## Next Steps

### Performance Review Schedule

- **Weekly**: Monitor key metrics
- **Monthly**: Full performance audit
- **Quarterly**: Baseline update

### Success Criteria

- [ ] All metrics within target thresholds
- [ ] No performance regressions
- [ ] Lighthouse score >90
- [ ] Core Web Vitals "Good" rating

---

## Appendix

### Test Scripts

```bash
# Lighthouse test
npx lighthouse https://example.com --output=json --output-path=./report.json

# Load test (k6)
k6 run --vus 50 --duration 10m load-test.js

# Database query profiling
db.products.find({category: "roses"}).explain("executionStats")
```

### Raw Data

- Lighthouse Reports: `/reports/lighthouse/`
- Load Test Results: `/reports/k6/`
- Database Profiling: `/reports/db-profiling/`
- APM Dashboards: [URL]

---

**Baseline Version**: 1.0  
**Next Review**: [Date + 1 month]  
**Owner**: [Name]  
**Last Updated**: 2026-04-23
