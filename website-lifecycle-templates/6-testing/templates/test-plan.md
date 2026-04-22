# Test Plan Template

> **Mục đích**: Comprehensive testing strategy cho website

---

## 🎯 Test Scope

| Area | In Scope | Out of Scope |
|------|----------|--------------|
| **Functional** | All features | Third-party integrations |
| **UI/UX** | All pages | External links |
| **Performance** | Load time, Core Web Vitals | Server infrastructure |
| **Security** | OWASP Top 10 | Penetration testing |

---

## 🧪 Test Types

### 1. Unit Testing
- **Framework**: [Jest / Vitest / Mocha]
- **Coverage target**: 80%+
- **Focus**: Business logic, utilities, helpers

```bash
# Run unit tests
npm run test:unit
```

### 2. Integration Testing
- **Framework**: [Jest / Vitest]
- **Focus**: API endpoints, database operations, service layer

```bash
# Run integration tests
npm run test:integration
```

### 3. E2E Testing
- **Framework**: [Playwright / Cypress]
- **Focus**: Critical user flows

**Test scenarios**:
- [ ] User registration & login
- [ ] Product search & filtering
- [ ] Add to cart & checkout
- [ ] Form submissions
- [ ] Navigation flows

```bash
# Run E2E tests
npm run test:e2e
```

### 4. Cross-Browser Testing
- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Edge (latest)

### 5. Responsive Testing
- [ ] Mobile (320px - 480px)
- [ ] Tablet (768px - 1024px)
- [ ] Desktop (1280px+)

**Devices to test**:
- iPhone 12/13/14
- iPad Pro
- Samsung Galaxy S21
- Desktop 1920x1080

---

## ⚡ Performance Testing

### Lighthouse Audit
- [ ] **Performance**: > 90
- [ ] **Accessibility**: > 90
- [ ] **Best Practices**: > 90
- [ ] **SEO**: > 90

### Core Web Vitals
- [ ] **LCP** (Largest Contentful Paint): < 2.5s
- [ ] **FID** (First Input Delay): < 100ms
- [ ] **CLS** (Cumulative Layout Shift): < 0.1

### Load Testing
- **Tool**: [k6 / Artillery / JMeter]
- **Target**: 1000 concurrent users
- **Duration**: 5 minutes

---

## 🔒 Security Testing

### OWASP Top 10
- [ ] Injection (SQL, XSS)
- [ ] Broken Authentication
- [ ] Sensitive Data Exposure
- [ ] XML External Entities (XXE)
- [ ] Broken Access Control
- [ ] Security Misconfiguration
- [ ] Cross-Site Scripting (XSS)
- [ ] Insecure Deserialization
- [ ] Using Components with Known Vulnerabilities
- [ ] Insufficient Logging & Monitoring

### Security Checklist
- [ ] HTTPS enabled
- [ ] CSP headers configured
- [ ] CORS configured correctly
- [ ] Rate limiting on API endpoints
- [ ] Input validation & sanitization
- [ ] Authentication tokens secure (httpOnly, secure)

---

## ♿ Accessibility Testing

### WCAG 2.1 Level AA
- [ ] Keyboard navigation
- [ ] Screen reader compatibility
- [ ] Color contrast (4.5:1 for text)
- [ ] Alt text for images
- [ ] Form labels & error messages
- [ ] Focus indicators

**Tools**:
- axe DevTools
- WAVE
- Lighthouse Accessibility

---

## 🐛 Bug Tracking

| Severity | Definition | Response Time |
|----------|------------|---------------|
| 🔴 Critical | Blocks core functionality | < 4 hours |
| 🟡 High | Major feature broken | < 24 hours |
| 🟢 Medium | Minor feature issue | < 3 days |
| ⚪ Low | Cosmetic issue | < 1 week |

---

## 📊 Test Metrics

- **Test coverage**: [Current: __% | Target: 80%]
- **Pass rate**: [Current: __% | Target: 95%]
- **Bugs found**: [Total: __ | Critical: __ | High: __ | Medium: __ | Low: __]
- **Bugs fixed**: [Total: __ | Remaining: __]

---

## ✅ Sign-off Criteria

- [ ] All critical & high bugs fixed
- [ ] Test coverage > 80%
- [ ] Pass rate > 95%
- [ ] Performance score > 90
- [ ] Accessibility score > 90
- [ ] Security audit passed
- [ ] Stakeholder approval
