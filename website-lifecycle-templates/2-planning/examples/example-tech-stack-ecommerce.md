# Tech Stack - E-commerce (SiinStore)

> **Project**: SiinStore Flower Shop
> **Architecture**: Monorepo với Next.js + PayloadCMS
> **Date**: 2026-04-22

---

## 1. Technology Stack Overview

```yaml
Frontend:
  Framework: Next.js 15.4.4 (App Router)
  UI Library: React 19.1.0
  Language: TypeScript 5.7.3
  Styling: TailwindCSS 4.1.12
  Components: Radix UI (headless)
  State: Redux Toolkit
  Forms: React Hook Form + Zod

Backend:
  CMS: PayloadCMS 3.49.1
  Runtime: Node.js 20+
  Database: MongoDB 7.0
  ORM: Mongoose (built-in Payload)
  API: REST + GraphQL (Payload auto-generated)

Infrastructure:
  Hosting: Vercel (Frontend + API routes)
  Database: MongoDB Atlas (M10 cluster)
  CDN: Cloudflare
  Storage: AWS S3 (images)
  Email: SendGrid
  SMS: Twilio

DevOps:
  Package Manager: pnpm 10.12.4
  Version Control: Git + GitHub
  CI/CD: GitHub Actions + Vercel
  Monitoring: Sentry + Vercel Analytics
  Testing: Vitest + Playwright
```

---

## 2. Architecture Decision Records (ADRs)

### ADR-001: Monorepo vs Separate Repos

**Decision**: Monorepo với Next.js + PayloadCMS trong cùng 1 project

**Rationale**:
- ✅ Shared types giữa frontend/backend
- ✅ Single deployment pipeline
- ✅ Easier local development
- ✅ Code reuse (utils, constants)

**Trade-offs**:
- ❌ Larger bundle size
- ❌ Longer build time
- ✅ Mitigate: Vercel incremental builds

**Alternatives Considered**:
- Separate repos: Phức tạp hơn, duplicate types
- Microservices: Overkill cho MVP

---

### ADR-002: PayloadCMS vs Strapi vs Custom Backend

**Decision**: PayloadCMS 3.x

**Rationale**:
- ✅ TypeScript-first (type-safe)
- ✅ Auto-generated Admin UI
- ✅ Built-in authentication
- ✅ Flexible hooks system
- ✅ GraphQL + REST APIs
- ✅ Local API (no HTTP overhead)

**Trade-offs**:
- ❌ Newer ecosystem (less plugins)
- ❌ Learning curve
- ✅ Mitigate: Good documentation

**Alternatives Considered**:
| CMS | Pros | Cons | Score |
|-----|------|------|-------|
| Strapi | Mature, many plugins | JavaScript, slower | 7/10 |
| Sanity | Great DX, real-time | Expensive, vendor lock-in | 6/10 |
| Custom | Full control | Time-consuming, maintenance | 5/10 |
| **Payload** | **Type-safe, flexible** | **Newer** | **9/10** |

---

### ADR-003: MongoDB vs PostgreSQL

**Decision**: MongoDB

**Rationale**:
- ✅ PayloadCMS native support
- ✅ Flexible schema (e-commerce products vary)
- ✅ Horizontal scaling (sharding)
- ✅ JSON-like documents (match frontend state)

**Trade-offs**:
- ❌ No ACID transactions (workaround: sessions)
- ❌ No foreign key constraints
- ✅ Mitigate: Application-level validation

**Alternatives Considered**:
- PostgreSQL: Better for relational data, but overkill
- MySQL: Legacy, less flexible

---

### ADR-004: Redux Toolkit vs Zustand vs Context API

**Decision**: Redux Toolkit

**Rationale**:
- ✅ Predictable state management
- ✅ DevTools (time-travel debugging)
- ✅ RTK Query (data fetching + caching)
- ✅ Team familiarity

**Trade-offs**:
- ❌ Boilerplate (mitigate: RTK slices)
- ❌ Learning curve

**Alternatives Considered**:
- Zustand: Simpler, but less tooling
- Context API: Built-in, but performance issues

---

### ADR-005: TailwindCSS vs CSS Modules vs Styled Components

**Decision**: TailwindCSS 4.x

**Rationale**:
- ✅ Utility-first (rapid prototyping)
- ✅ Design system consistency
- ✅ Purge unused CSS (small bundle)
- ✅ JIT compiler (fast builds)

**Trade-offs**:
- ❌ HTML verbosity
- ✅ Mitigate: Extract components

**Alternatives Considered**:
- CSS Modules: More verbose
- Styled Components: Runtime overhead

---

### ADR-006: Vercel vs AWS vs Self-Hosted

**Decision**: Vercel

**Rationale**:
- ✅ Zero-config Next.js deployment
- ✅ Edge functions (low latency)
- ✅ Automatic HTTPS + CDN
- ✅ Preview deployments (per PR)
- ✅ Built-in analytics

**Trade-offs**:
- ❌ Vendor lock-in
- ❌ Cost at scale
- ✅ Mitigate: Start with Hobby plan, scale later

**Alternatives Considered**:
- AWS: More control, but complex setup
- Self-hosted: Cheapest, but maintenance overhead

---

## 3. Detailed Stack Breakdown

### 3.1 Frontend Stack

```typescript
// package.json (frontend dependencies)
{
  "dependencies": {
    // Core
    "next": "15.4.4",
    "react": "19.1.0",
    "react-dom": "19.1.0",
    "typescript": "5.7.3",

    // UI Components
    "@radix-ui/react-dialog": "^1.0.5",
    "@radix-ui/react-dropdown-menu": "^2.0.6",
    "@radix-ui/react-select": "^2.0.0",
    "lucide-react": "^0.263.1",

    // Styling
    "tailwindcss": "4.1.12",
    "clsx": "^2.1.0",
    "tailwind-merge": "^2.2.0",

    // State Management
    "@reduxjs/toolkit": "^2.0.1",
    "react-redux": "^9.0.4",

    // Forms
    "react-hook-form": "^7.49.3",
    "zod": "^3.22.4",
    "@hookform/resolvers": "^3.3.4",

    // Data Fetching
    "axios": "^1.6.5",
    "swr": "^2.2.4",

    // Utilities
    "date-fns": "^3.0.6",
    "lodash": "^4.17.21",
    "nanoid": "^5.0.4"
  },
  "devDependencies": {
    // Testing
    "vitest": "^1.2.0",
    "@testing-library/react": "^14.1.2",
    "playwright": "^1.40.1",

    // Linting
    "eslint": "^8.56.0",
    "prettier": "^3.1.1",
    "typescript-eslint": "^6.19.0"
  }
}
```

---

### 3.2 Backend Stack

```typescript
// package.json (backend dependencies)
{
  "dependencies": {
    // CMS
    "payload": "3.49.1",
    "@payloadcms/db-mongodb": "^3.0.0",
    "@payloadcms/richtext-lexical": "^3.0.0",
    "@payloadcms/plugin-cloud-storage": "^3.0.0",

    // Database
    "mongodb": "^6.3.0",

    // Authentication
    "jsonwebtoken": "^9.0.2",
    "bcrypt": "^5.1.1",

    // File Upload
    "@aws-sdk/client-s3": "^3.490.0",
    "sharp": "^0.33.1",

    // Payment
    "vnpay": "^1.0.0",
    "momo-payment": "^1.0.0",

    // Notifications
    "@sendgrid/mail": "^7.7.0",
    "twilio": "^4.20.0",

    // Utilities
    "dotenv": "^16.3.1",
    "express": "^4.18.2"
  }
}
```

---

### 3.3 Infrastructure Stack

```yaml
Hosting:
  Frontend: Vercel (Edge Network)
  Backend: Vercel Serverless Functions
  Database: MongoDB Atlas (M10 - 2GB RAM, 10GB storage)

CDN:
  Provider: Cloudflare
  Features:
    - DDoS protection
    - Image optimization
    - Caching rules

Storage:
  Provider: AWS S3
  Bucket: siinstore-images
  Region: ap-southeast-1 (Singapore)
  Features:
    - Versioning enabled
    - Lifecycle policies (delete after 90 days)

Email:
  Provider: SendGrid
  Plan: Essentials (50K emails/month)
  Features:
    - Transactional emails
    - Email templates
    - Analytics

SMS:
  Provider: Twilio
  Features:
    - OTP verification
    - Order notifications
    - Delivery updates

Monitoring:
  Error Tracking: Sentry
  Analytics: Vercel Analytics + Google Analytics 4
  Uptime: UptimeRobot (5-min checks)
```

---

## 4. Development Environment

### 4.1 Local Setup

```bash
# Prerequisites
node -v    # v20.11.0
pnpm -v    # 10.12.4

# Clone repo
git clone https://github.com/siinstore/siinstore-api.git
cd siinstore-api

# Install dependencies
pnpm install

# Environment variables
cp .env.example .env.local
# Edit .env.local với local MongoDB URI

# Run development server
pnpm dev
# Frontend: http://localhost:3000
# Admin: http://localhost:3000/admin
# API: http://localhost:3000/api
```

### 4.2 Environment Variables

```bash
# .env.local
# Database
MONGODB_URI=mongodb://localhost:27017/siinstore
DATABASE_NAME=siinstore

# Payload
PAYLOAD_SECRET=your-secret-key-here
PAYLOAD_PUBLIC_SERVER_URL=http://localhost:3000

# AWS S3
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_REGION=ap-southeast-1
AWS_BUCKET=siinstore-images

# Payment
VNPAY_TMN_CODE=your-tmn-code
VNPAY_HASH_SECRET=your-hash-secret
MOMO_PARTNER_CODE=your-partner-code
MOMO_ACCESS_KEY=your-access-key

# Notifications
SENDGRID_API_KEY=your-sendgrid-key
TWILIO_ACCOUNT_SID=your-twilio-sid
TWILIO_AUTH_TOKEN=your-twilio-token

# Analytics
NEXT_PUBLIC_GA_ID=G-XXXXXXXXXX
SENTRY_DSN=https://xxx@sentry.io/xxx
```

---

## 5. CI/CD Pipeline

### 5.1 GitHub Actions Workflow

```yaml
# .github/workflows/ci.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v2
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'
      
      - name: Install dependencies
        run: pnpm install
      
      - name: Lint
        run: pnpm lint
      
      - name: Type check
        run: pnpm type-check
      
      - name: Unit tests
        run: pnpm test:unit
      
      - name: Build
        run: pnpm build

  e2e:
    runs-on: ubuntu-latest
    needs: test
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v2
      - uses: actions/setup-node@v4
      
      - name: Install dependencies
        run: pnpm install
      
      - name: Install Playwright
        run: pnpm exec playwright install --with-deps
      
      - name: E2E tests
        run: pnpm test:e2e

  deploy:
    runs-on: ubuntu-latest
    needs: [test, e2e]
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          vercel-args: '--prod'
```

---

## 6. Performance Targets

| Metric | Target | Tool |
|--------|--------|------|
| Lighthouse Score | > 90 | Lighthouse CI |
| First Contentful Paint | < 1.5s | Web Vitals |
| Largest Contentful Paint | < 2.5s | Web Vitals |
| Time to Interactive | < 3s | Web Vitals |
| Cumulative Layout Shift | < 0.1 | Web Vitals |
| API Response Time (p95) | < 500ms | Vercel Analytics |
| Database Query Time | < 100ms | MongoDB Atlas |

---

## 7. Security Measures

```yaml
Authentication:
  - JWT với refresh token
  - HttpOnly cookies
  - CSRF protection

Authorization:
  - Role-based access control (RBAC)
  - Admin, Store Manager, Customer roles

Data Protection:
  - Bcrypt password hashing (10 rounds)
  - Sensitive data encryption at rest
  - HTTPS only (TLS 1.3)

API Security:
  - Rate limiting (100 req/min per IP)
  - Input validation (Zod schemas)
  - SQL injection prevention (Mongoose)
  - XSS prevention (sanitize inputs)

Payment Security:
  - PCI DSS compliant (via VNPay/MoMo)
  - No credit card storage
  - Tokenized payments
```

---

## 8. Scalability Plan

### Phase 1: MVP (0-1K users/day)
- Vercel Hobby plan
- MongoDB Atlas M10
- Single region (Singapore)

### Phase 2: Growth (1K-10K users/day)
- Vercel Pro plan
- MongoDB Atlas M30 (8GB RAM)
- Enable sharding
- Add Redis cache (Upstash)

### Phase 3: Scale (10K+ users/day)
- Vercel Enterprise
- MongoDB Atlas M50+ (16GB RAM)
- Multi-region deployment
- Dedicated CDN (Cloudflare Enterprise)
- Microservices migration (if needed)

---

## 9. Cost Estimation

### Monthly Costs (MVP)

| Service | Plan | Cost |
|---------|------|------|
| Vercel | Hobby | $0 (free tier) |
| MongoDB Atlas | M10 | $57/month |
| AWS S3 | Standard | ~$10/month (100GB) |
| Cloudflare | Free | $0 |
| SendGrid | Essentials | $20/month |
| Twilio | Pay-as-you-go | ~$50/month |
| Sentry | Developer | $26/month |
| **Total** | | **~$163/month** |

### Monthly Costs (Growth)

| Service | Plan | Cost |
|---------|------|------|
| Vercel | Pro | $20/month |
| MongoDB Atlas | M30 | $285/month |
| AWS S3 | Standard | ~$50/month (500GB) |
| Cloudflare | Pro | $20/month |
| SendGrid | Pro | $90/month |
| Twilio | Pay-as-you-go | ~$200/month |
| Sentry | Team | $80/month |
| Upstash Redis | Pro | $40/month |
| **Total** | | **~$785/month** |

---

## 10. Related Documents

- **Architecture**: [example-architecture-microservices.md](./example-architecture-microservices.md)
- **Sitemap**: [example-sitemap-flower-shop.md](./example-sitemap-flower-shop.md)
- **Development**: `5-development/examples/`
- **Testing**: `6-testing/examples/`
