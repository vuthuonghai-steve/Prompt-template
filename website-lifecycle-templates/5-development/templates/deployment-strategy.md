# Deployment Strategy Template

**Project**: [Project Name]  
**Date**: [YYYY-MM-DD]  
**Author**: [Name]  
**Environment**: Development | Staging | Production

---

## Executive Summary

**Deployment Goal**: [Brief description - e.g., "Deploy e-commerce flower shop to production with zero downtime"]

**Business Impact**: [Expected outcomes - e.g., "Enable 24/7 online ordering, support 1000+ concurrent users"]

**Timeline**: [Target go-live date]

---

## Deployment Architecture

### Infrastructure Overview

```
┌─────────────────────────────────────────────────┐
│                 Load Balancer                    │
│              (nginx / AWS ALB)                   │
└────────────┬────────────────────┬────────────────┘
             │                    │
    ┌────────▼────────┐  ┌────────▼────────┐
    │   App Server 1  │  │   App Server 2  │
    │   (Next.js)     │  │   (Next.js)     │
    └────────┬────────┘  └────────┬────────┘
             │                    │
             └────────┬───────────┘
                      │
             ┌────────▼────────┐
             │    Database     │
             │   (MongoDB)     │
             └─────────────────┘
```

### Technology Stack

| Component | Technology | Version |
|-----------|------------|---------|
| **Frontend** | Next.js | 15.4.4 |
| **Backend** | PayloadCMS | 3.49.1 |
| **Database** | MongoDB | 7.0 |
| **Cache** | Redis | 7.2 |
| **CDN** | Cloudflare | - |
| **Hosting** | Vercel / AWS | - |

---

## Environment Strategy

### Environment Tiers

| Environment | Purpose | URL | Database | Auto-Deploy |
|-------------|---------|-----|----------|-------------|
| **Development** | Local dev | localhost:3000 | Local MongoDB | No |
| **Staging** | Pre-prod testing | staging.example.com | Staging DB | Yes (main branch) |
| **Production** | Live traffic | www.example.com | Prod DB | Manual approval |

### Environment Variables

```bash
# Development
NODE_ENV=development
DATABASE_URL=mongodb://localhost:27017/flower-shop-dev
NEXT_PUBLIC_API_URL=http://localhost:3000/api

# Staging
NODE_ENV=staging
DATABASE_URL=mongodb+srv://staging.mongodb.net/flower-shop
NEXT_PUBLIC_API_URL=https://staging.example.com/api

# Production
NODE_ENV=production
DATABASE_URL=mongodb+srv://prod.mongodb.net/flower-shop
NEXT_PUBLIC_API_URL=https://www.example.com/api
```

---

## Deployment Pipeline

### CI/CD Workflow

```
┌──────────────┐
│  Git Push    │
│  to main     │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Run Tests   │
│  (Vitest)    │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Build       │
│  (next build)│
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Deploy to   │
│  Staging     │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Smoke Tests │
│  (Playwright)│
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Manual      │
│  Approval    │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Deploy to   │
│  Production  │
└──────────────┘
```

### GitHub Actions Example

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: pnpm install
      - run: pnpm test
      - run: pnpm build

  deploy-staging:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to Staging
        run: |
          vercel deploy --prod --token=${{ secrets.VERCEL_TOKEN }}

  deploy-production:
    needs: deploy-staging
    runs-on: ubuntu-latest
    environment: production
    steps:
      - name: Deploy to Production
        run: |
          vercel deploy --prod --token=${{ secrets.VERCEL_TOKEN }}
```

---

## Database Migration Strategy

### Migration Workflow

**Pre-Deployment**:
1. [ ] Backup production database
2. [ ] Test migration on staging
3. [ ] Verify data integrity
4. [ ] Document rollback steps

**During Deployment**:
1. [ ] Enable maintenance mode (optional)
2. [ ] Run migrations
3. [ ] Verify schema changes
4. [ ] Disable maintenance mode

**Post-Deployment**:
1. [ ] Verify application functionality
2. [ ] Monitor error logs
3. [ ] Check performance metrics

### Migration Example

```typescript
// migrations/2026-04-23-add-wishlist.ts
export async function up(db: Db) {
  await db.collection('users').updateMany(
    {},
    { $set: { wishlist: [] } }
  )
}

export async function down(db: Db) {
  await db.collection('users').updateMany(
    {},
    { $unset: { wishlist: '' } }
  )
}
```

---

## Zero-Downtime Deployment

### Blue-Green Deployment

```
┌─────────────────────────────────────────────────┐
│              Load Balancer                       │
└────────────┬────────────────────┬────────────────┘
             │                    │
    ┌────────▼────────┐  ┌────────▼────────┐
    │   Blue (v1.0)   │  │  Green (v1.1)   │
    │   Active        │  │  Standby        │
    └─────────────────┘  └─────────────────┘

Step 1: Deploy v1.1 to Green
Step 2: Run smoke tests on Green
Step 3: Switch traffic to Green
Step 4: Monitor for 10 minutes
Step 5: Decommission Blue (or keep as rollback)
```

### Rolling Deployment

```
Initial State:
[Server 1: v1.0] [Server 2: v1.0] [Server 3: v1.0]

Step 1: Deploy to Server 1
[Server 1: v1.1] [Server 2: v1.0] [Server 3: v1.0]

Step 2: Deploy to Server 2
[Server 1: v1.1] [Server 2: v1.1] [Server 3: v1.0]

Step 3: Deploy to Server 3
[Server 1: v1.1] [Server 2: v1.1] [Server 3: v1.1]
```

---

## Health Checks & Monitoring

### Health Check Endpoints

```typescript
// app/api/health/route.ts
export async function GET() {
  const checks = {
    database: await checkDatabase(),
    redis: await checkRedis(),
    externalAPI: await checkPaymentGateway(),
  }

  const healthy = Object.values(checks).every(c => c.status === 'ok')

  return Response.json(
    { status: healthy ? 'healthy' : 'degraded', checks },
    { status: healthy ? 200 : 503 }
  )
}
```

### Monitoring Checklist

- [ ] Application logs (errors, warnings)
- [ ] Performance metrics (response time, throughput)
- [ ] Database metrics (connections, query time)
- [ ] Server metrics (CPU, memory, disk)
- [ ] Business metrics (orders, revenue)

### Alert Thresholds

| Metric | Warning | Critical |
|--------|---------|----------|
| Error Rate | >1% | >5% |
| Response Time | >500ms | >1s |
| CPU Usage | >70% | >90% |
| Memory Usage | >80% | >95% |
| Database Connections | >80% | >95% |

---

## Rollback Strategy

### Rollback Triggers

- [ ] Error rate >5% for 5 minutes
- [ ] Critical bug discovered
- [ ] Database migration failed
- [ ] Performance degradation >50%
- [ ] Security vulnerability detected

### Rollback Steps

**Immediate Rollback** (< 5 minutes):
1. Switch load balancer to previous version
2. Verify application functionality
3. Notify team

**Database Rollback** (if needed):
1. Stop application
2. Restore database backup
3. Run down migration
4. Restart application
5. Verify data integrity

### Rollback Example

```bash
# Vercel rollback
vercel rollback [deployment-url]

# Docker rollback
docker service update --rollback my-app

# Kubernetes rollback
kubectl rollout undo deployment/my-app
```

---

## Security Checklist

### Pre-Deployment Security

- [ ] All secrets in environment variables (not hardcoded)
- [ ] HTTPS enabled with valid SSL certificate
- [ ] CORS configured correctly
- [ ] Rate limiting enabled
- [ ] SQL injection prevention (parameterized queries)
- [ ] XSS prevention (input sanitization)
- [ ] CSRF protection enabled
- [ ] Security headers configured

### Security Headers Example

```typescript
// next.config.js
module.exports = {
  async headers() {
    return [
      {
        source: '/:path*',
        headers: [
          { key: 'X-Frame-Options', value: 'DENY' },
          { key: 'X-Content-Type-Options', value: 'nosniff' },
          { key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' },
          { key: 'Permissions-Policy', value: 'camera=(), microphone=(), geolocation=()' },
        ],
      },
    ]
  },
}
```

---

## Performance Optimization

### Pre-Deployment Optimization

- [ ] Enable gzip/brotli compression
- [ ] Optimize images (WebP, lazy loading)
- [ ] Minify CSS/JS
- [ ] Enable CDN for static assets
- [ ] Configure caching headers
- [ ] Database indexes created
- [ ] API response caching

### Caching Strategy

```typescript
// Example: Cache product list for 5 minutes
export const revalidate = 300 // seconds

export async function getProducts() {
  const products = await fetch('/api/products', {
    next: { revalidate: 300 }
  })
  return products.json()
}
```

---

## E-Commerce Specific Considerations

### Inventory Management

- [ ] Real-time inventory sync enabled
- [ ] Low stock alerts configured
- [ ] Out-of-stock handling tested
- [ ] Inventory reservation during checkout

### Payment Gateway

- [ ] Payment gateway credentials verified
- [ ] Webhook endpoints configured
- [ ] Test transactions completed
- [ ] Refund process tested
- [ ] PCI DSS compliance verified

### Order Processing

- [ ] Order confirmation emails working
- [ ] Order status updates functional
- [ ] Shipping integration tested
- [ ] Invoice generation working

---

## Deployment Checklist

### Pre-Deployment (1 week before)

- [ ] Code freeze announced
- [ ] All features tested in staging
- [ ] Database backup verified
- [ ] Rollback plan documented
- [ ] Team notified of deployment window
- [ ] Customer support briefed

### Deployment Day (Go-Live)

- [ ] Backup production database
- [ ] Enable maintenance mode (if needed)
- [ ] Run database migrations
- [ ] Deploy application
- [ ] Run smoke tests
- [ ] Verify critical flows (checkout, payment)
- [ ] Disable maintenance mode
- [ ] Monitor for 2 hours

### Post-Deployment (24 hours)

- [ ] Monitor error logs
- [ ] Check performance metrics
- [ ] Verify business metrics (orders, revenue)
- [ ] Collect user feedback
- [ ] Document lessons learned

---

## Communication Plan

### Stakeholder Communication

| Stakeholder | Before | During | After |
|-------------|--------|--------|-------|
| **Engineering Team** | Deployment plan | Real-time updates | Post-mortem |
| **Product Team** | Feature list | Go/no-go decision | Success metrics |
| **Customer Support** | Known issues | Escalation path | FAQ updates |
| **Customers** | Maintenance notice | Status page | Feature announcement |

### Status Page Example

```markdown
## Scheduled Maintenance

**Date**: April 23, 2026  
**Time**: 02:00 - 04:00 UTC  
**Impact**: Website will be unavailable for 5 minutes  
**Reason**: Deploying new features and performance improvements

We apologize for any inconvenience.
```

---

## Disaster Recovery

### Backup Strategy

| Data | Frequency | Retention | Location |
|------|-----------|-----------|----------|
| **Database** | Daily | 30 days | AWS S3 |
| **Media Files** | Daily | 90 days | Cloudflare R2 |
| **Code** | On commit | Forever | GitHub |
| **Config** | On change | 90 days | Vault |

### Recovery Time Objectives

| Scenario | RTO | RPO |
|----------|-----|-----|
| **Application Crash** | 5 minutes | 0 (no data loss) |
| **Database Corruption** | 1 hour | 24 hours |
| **Complete Outage** | 4 hours | 24 hours |

---

## Success Criteria

**Deployment Success**:
- [ ] Zero critical errors in first 24 hours
- [ ] Response time <500ms p95
- [ ] Error rate <1%
- [ ] All critical flows functional
- [ ] No customer complaints

**Business Success** (7 days):
- [ ] Order volume maintained or increased
- [ ] Conversion rate maintained or increased
- [ ] Customer satisfaction score >4.5/5
- [ ] Zero payment failures

---

## Lessons Learned Template

**What Went Well**:
- [Success 1]
- [Success 2]

**What Could Be Improved**:
- [Issue 1] → [Action item]
- [Issue 2] → [Action item]

**Action Items**:
- [ ] [Action 1] - Owner: [Name] - Due: [Date]
- [ ] [Action 2] - Owner: [Name] - Due: [Date]

---

## Appendix

### Useful Commands

```bash
# Check deployment status
vercel ls

# View logs
vercel logs [deployment-url]

# Rollback
vercel rollback [deployment-url]

# Database backup
mongodump --uri="mongodb+srv://..." --out=/backup

# Database restore
mongorestore --uri="mongodb+srv://..." /backup
```

### Contact Information

- **DevOps Lead**: [Name] - [Email/Slack]
- **Database Admin**: [Name] - [Email/Slack]
- **On-Call Engineer**: [Name] - [Phone]
- **Escalation**: [Manager] - [Phone]

---

**Template Version**: 1.0  
**Last Updated**: 2026-04-23
