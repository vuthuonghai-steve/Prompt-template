# Phase 7: Maintenance - AI Prompts

> **Extracted from**: Cursor, Claude Code, Windsurf
> **Focus**: Refactoring, debugging, optimization, feature additions

---

## 🔧 Refactoring Prompts

### From Cursor Agent

```
Refactor [component/function] to improve [performance/readability/maintainability].

Context:
- Current implementation: [describe current code]
- Issues: [performance bottleneck/code duplication/complexity]
- Constraints: [backward compatibility/API stability]

Requirements:
- Maintain existing functionality
- Add unit tests for refactored code
- Update documentation
- Measure performance impact
```

**Example**:
```
Refactor the cart calculation service to improve performance.

Context:
- Current: Recalculates total on every state change
- Issue: 200ms delay on cart updates with 10+ items
- Constraint: Must maintain discount application order

Requirements:
- Use memoization for expensive calculations
- Add performance benchmarks
- Ensure discount logic unchanged
```

---

### From Claude Code

```
Review [file/module] for code quality issues and suggest improvements.

Focus areas:
- Code duplication
- Complex functions (>50 lines)
- Missing error handling
- Type safety issues
- Performance bottlenecks

Provide:
1. List of issues found
2. Refactoring suggestions with code examples
3. Estimated impact (low/medium/high)
```

**Example**:
```
Review src/services/order/ for code quality issues.

Focus:
- Duplicate validation logic across files
- Complex order processing function (150 lines)
- Inconsistent error handling

Provide refactoring plan with priority order.
```

---

## 🐛 Debugging Prompts

### From Claude Code (Systematic Debugging)

```
Debug [issue description] using systematic approach.

Symptoms:
- What: [error message/unexpected behavior]
- When: [conditions that trigger it]
- Where: [affected components/pages]
- Impact: [user/business impact]

Investigation steps:
1. Reproduce the issue
2. Check error logs
3. Analyze relevant code
4. Identify root cause
5. Propose fix with test cases

Provide:
- Root cause analysis
- Fix implementation
- Prevention measures
```

**Example**:
```
Debug payment timeout errors occurring during checkout.

Symptoms:
- What: "Payment processing timeout" after 30s
- When: Peak hours (2-4 PM UTC), 15% of transactions
- Where: Checkout page, payment-proxy service
- Impact: $2K/day revenue loss, user complaints

Investigate systematically and provide fix.
```

---

### From Windsurf

```
Analyze error logs and identify patterns.

Logs: [paste error logs]

Tasks:
1. Group errors by type/frequency
2. Identify common patterns
3. Trace error origins
4. Suggest fixes for top 3 errors
5. Recommend monitoring improvements
```

**Example**:
```
Analyze production error logs from last 24 hours.

Logs: [500 lines of error logs]

Focus on:
- Most frequent errors
- Critical path failures
- User-facing errors

Provide actionable fixes.
```

---

## ⚡ Performance Optimization Prompts

### From Cursor

```
Optimize [component/page] for better performance.

Current metrics:
- Load time: [X]s
- LCP: [X]s
- FCP: [X]s
- Bundle size: [X]KB

Target:
- Load time: < [Y]s
- LCP: < [Y]s
- Lighthouse score: > [Z]

Analyze and provide optimization plan with:
1. Quick wins (< 1 day)
2. Medium effort (1-3 days)
3. Long-term improvements (> 3 days)
```

**Example**:
```
Optimize product listing page for mobile.

Current:
- Load time: 7.2s
- LCP: 6.8s
- Lighthouse: 42

Target:
- Load time: < 3s
- LCP: < 2.5s
- Lighthouse: > 85

Focus on image loading and JavaScript bundle size.
```

---

### From Claude Code

```
Profile [feature/page] and identify performance bottlenecks.

Steps:
1. Run Chrome DevTools Performance profiler
2. Analyze main thread activity
3. Identify expensive operations
4. Check network waterfall
5. Review bundle analysis

Provide:
- Top 5 bottlenecks with impact assessment
- Optimization recommendations
- Implementation priority
```

---

## ✨ Feature Addition Prompts

### From Cursor

```
Implement [feature name] following existing architecture.

Requirements:
- [Functional requirement 1]
- [Functional requirement 2]
- [Non-functional requirement]

Architecture:
- Database: [schema changes needed]
- API: [new endpoints]
- Frontend: [UI components]
- Testing: [test coverage requirements]

Provide:
1. Implementation plan
2. File structure
3. Code with tests
4. Documentation updates
```

**Example**:
```
Implement wishlist feature.

Requirements:
- Users can save products
- View saved items page
- Move to cart functionality
- Price drop notifications

Follow existing patterns:
- PayloadCMS collections
- Service layer architecture
- React Query for state
- Radix UI components
```

---

### From Windsurf

```
Add [feature] with minimal code changes.

Context:
- Existing codebase: [brief description]
- Similar features: [reference implementations]

Constraints:
- No breaking changes
- Reuse existing components
- Follow current patterns

Provide lean implementation focusing on:
1. Core functionality only
2. Reusing existing code
3. Minimal new dependencies
```

---

## 🔒 Security & Bug Fixes

### From Claude Code

```
Security review of [component/feature].

Check for:
- Input validation
- SQL injection risks
- XSS vulnerabilities
- Authentication/authorization issues
- Sensitive data exposure
- Rate limiting

Provide:
- Vulnerability assessment
- Risk level (critical/high/medium/low)
- Fix recommendations
- Security test cases
```

---

### From Cursor

```
Fix [bug description] with root cause analysis.

Bug:
- ID: [BUG-XXX]
- Description: [what's wrong]
- Steps to reproduce: [1, 2, 3]
- Expected: [correct behavior]
- Actual: [current behavior]

Provide:
1. Root cause analysis
2. Fix implementation
3. Test cases to prevent regression
4. Related bugs to check
```

---

## 📊 Code Quality Prompts

### From Windsurf

```
Improve code quality of [module/file].

Analyze:
- Cyclomatic complexity
- Code duplication
- Test coverage
- Type safety
- Documentation

Provide:
- Quality metrics before/after
- Refactoring suggestions
- Priority order
```

---

### From Claude Code

```
Add comprehensive tests for [feature/module].

Current coverage: [X]%
Target coverage: [Y]%

Test types needed:
- Unit tests: [components/functions]
- Integration tests: [API flows]
- E2E tests: [user journeys]

Provide:
- Test plan
- Test implementations
- Coverage report
```

---

## 🔄 Maintenance Workflows

### Weekly Code Health Check

```
Perform weekly code health check.

Tasks:
1. Run linter and fix issues
2. Update dependencies (patch versions)
3. Check test coverage
4. Review TODO/FIXME comments
5. Analyze bundle size
6. Check for security vulnerabilities

Provide summary report with action items.
```

---

### Monthly Dependency Update

```
Update project dependencies safely.

Steps:
1. List outdated packages
2. Check breaking changes
3. Update dev dependencies first
4. Update production dependencies
5. Run full test suite
6. Test in staging

Provide:
- Update plan
- Breaking changes summary
- Rollback strategy
```

---

### Quarterly Performance Audit

```
Conduct quarterly performance audit.

Audit areas:
1. Page load times (all routes)
2. API response times
3. Database query performance
4. Bundle size analysis
5. Lighthouse scores
6. Core Web Vitals

Provide:
- Performance report
- Regression analysis
- Optimization roadmap
```

---

## 🎯 Prompt Templates by Task Type

### Bug Fix Template

```
Fix: [Brief description]

**Symptoms**:
- Error: [error message]
- Frequency: [how often]
- Impact: [user/business impact]

**Investigation**:
1. Reproduce: [steps]
2. Logs: [relevant logs]
3. Root cause: [analysis]

**Fix**:
- Changes: [code changes]
- Tests: [test cases]
- Verification: [how to verify]

**Prevention**:
- Monitoring: [alerts to add]
- Tests: [coverage to add]
```

---

### Optimization Template

```
Optimize: [Component/Feature]

**Current State**:
- Metric 1: [value]
- Metric 2: [value]
- Issue: [bottleneck]

**Target**:
- Metric 1: < [target]
- Metric 2: < [target]

**Approach**:
1. [Quick win 1]
2. [Quick win 2]
3. [Long-term improvement]

**Measurement**:
- Before/after metrics
- A/B test results
```

---

### Feature Addition Template

```
Feature: [Name]

**Requirements**:
- Must have: [core features]
- Nice to have: [optional features]

**Architecture**:
- Backend: [API/database changes]
- Frontend: [UI components]
- Testing: [test strategy]

**Rollout**:
- Phase 1: [beta users]
- Phase 2: [gradual rollout]
- Phase 3: [full launch]

**Success Metrics**:
- Adoption: [target %]
- Engagement: [target metric]
```

---

## 📚 Best Practices

### When Refactoring

1. **Start small**: Refactor one function/component at a time
2. **Test first**: Ensure existing tests pass
3. **Measure impact**: Before/after metrics
4. **Document changes**: Update comments and docs

### When Debugging

1. **Reproduce first**: Consistent reproduction steps
2. **Isolate issue**: Narrow down to specific component
3. **Check logs**: Error logs, monitoring dashboards
4. **Fix root cause**: Not just symptoms

### When Optimizing

1. **Measure first**: Baseline metrics before optimization
2. **Profile**: Use profiling tools to find bottlenecks
3. **Prioritize**: Focus on high-impact optimizations
4. **Verify**: Measure improvement after changes

### When Adding Features

1. **Design first**: Architecture and API design
2. **Incremental**: Build in small, testable pieces
3. **Test coverage**: Write tests alongside code
4. **Documentation**: Update docs as you build

---

**Last Updated**: 2026-04-23  
**Sources**: Cursor Agent 2.0, Claude Code 2.0, Windsurf Wave 11
