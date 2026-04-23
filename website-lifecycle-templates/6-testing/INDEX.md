# Phase 6: Testing, Review & Launch

> **Mục tiêu**: QA, performance, security, deployment
> **Đầu ra**: Test reports, production deployment
> **Artifact inventory completion**: 100% (source validation pending for synthesized material)
> **Last Updated**: 2026-04-23

---

## 🔗 Quick Navigation

| Section | Description |
|---------|-------------|
| [Patterns](#-patterns) | Testing patterns, workflows |
| [Prompts](#-prompts) | AI tool prompts for testing |
| [Templates](#-templates) | Document templates |
| [Examples](#-examples) | Real-world examples |

---

## 📋 Testing Checklist

- [ ] Unit testing
- [ ] Integration testing
- [ ] E2E testing
- [ ] Cross-browser testing
- [ ] Responsive testing (devices)
- [ ] Performance testing (Lighthouse)
- [ ] Security testing (OWASP)
- [ ] SEO audit
- [ ] Accessibility audit (WCAG)
- [ ] Bug fixing
- [ ] Final review
- [ ] Production deployment
- [ ] Post-launch monitoring

---

## 🎨 Patterns

Testing patterns và best practices. Standalone Test Pyramid/Mock Strategy docs are not separate files yet; related guidance lives in `test-plan.md` and `pattern-test-driven-validation.md`.

| Pattern | Description | Link |
|---------|-------------|------|
| Test-Driven Validation | Red → Green → Refactor cycle, AAA structure, coverage targets | [View](./patterns/pattern-test-driven-validation.md) |
| Debug Logging | Structured logs, request IDs, performance/error traces | [View](./patterns/pattern-debug-logging.md) |
| Browser Automation Testing | Critical journey automation and browser coverage | [View](./patterns/pattern-browser-automation-testing.md) |

---

## 🤖 Prompts

AI tool prompts for testing automation.

| Tool | Focus | Link |
|------|-------|------|
| **Cursor Agent** | Test generation, linting, diagnostics | [View](./prompts/prompt-cursor-testing.md) |
| **Claude Code** | Systematic debugging, verification | [View](./prompts/prompt-claude-code-testing.md) |
| **Devin AI** | CI/CD integration, browser testing | [View](./prompts/prompt-devin-testing.md) |
| **Windsurf/Cline** | Code review, quality checks | [View](./prompts/prompt-windsurf-testing.md) |

---

## 📁 Templates

Document templates và checklists.

| Template | Purpose | Link |
|----------|---------|------|
| `test-plan.md` | Comprehensive test plan | [View](./templates/test-plan.md) |
| `bug-report.md` | Bug report template | [View](./templates/bug-report.md) |
| `performance-checklist.md` | Performance optimization | [View](./templates/performance-checklist.md) |
| `security-checklist.md` | Security audit checklist | [View](./templates/security-checklist.md) |

---

## 💡 Examples

Real-world examples cho e-commerce flower shop.

| Example | Description | Link |
|---------|-------------|------|
| `example-test-checkout-flow.spec.ts` | E2E test: Browse → Cart → Checkout → Payment | [View](./examples/example-test-checkout-flow.spec.ts) |
| `example-api-test-products.test.ts` | API integration test: Products CRUD | [View](./examples/example-api-test-products.test.ts) |
| `example-performance-report.md` | Lighthouse audit + Core Web Vitals analysis | [View](./examples/example-performance-report.md) |
| `example-security-audit-findings.md` | OWASP Top 10 + penetration test findings | [View](./examples/example-security-audit-findings.md) |

---

## 📖 Resources

- [STRUCTURE.md](../STRUCTURE.md) - Structure guidelines

---

## 🔗 Navigation

[← Previous: Development](../5-development/INDEX.md) | [Next: Maintenance →](../7-maintenance/INDEX.md)
