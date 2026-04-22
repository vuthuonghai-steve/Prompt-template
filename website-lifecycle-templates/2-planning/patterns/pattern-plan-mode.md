# Pattern: Plan Mode

## Nguồn
- Claude Code
- Windsurf Cascade
- Cursor Agent

## Mô tả
Tạo implementation plan chi tiết trước khi code. Chia nhỏ task phức tạp thành steps có thể execute, identify dependencies, estimate effort.

## Khi nào dùng
- Planning phase: architecture design, tech stack selection
- Development: trước khi implement feature lớn
- Refactoring: plan migration strategy
- Bug fixing: plan systematic debugging approach

## Cách áp dụng

### 1. Plan Structure
```markdown
## Goal
[Mô tả rõ ràng mục tiêu cuối cùng]

## Context
[Background information, constraints, assumptions]

## Approach
[High-level strategy]

## Steps
1. [Step 1 - actionable, measurable]
   - Subtask 1.1
   - Subtask 1.2
2. [Step 2]
   ...

## Dependencies
- [External dependencies]
- [Blocking issues]

## Risks
- [Potential risks và mitigation]

## Success Criteria
- [Measurable outcomes]
```

### 2. Break Down Complex Tasks
```typescript
// Large task: "Build e-commerce checkout"
interface Plan {
  goal: string
  steps: Step[]
  dependencies: string[]
  estimatedHours: number
}

const checkoutPlan: Plan = {
  goal: 'Implement complete checkout flow',
  steps: [
    {
      id: '1',
      title: 'Design checkout UI',
      subtasks: [
        'Cart summary component',
        'Shipping form',
        'Payment form',
        'Order confirmation',
      ],
      estimatedHours: 16,
      dependencies: [],
    },
    {
      id: '2',
      title: 'Implement cart logic',
      subtasks: [
        'Add/remove items',
        'Update quantities',
        'Calculate totals',
        'Apply vouchers',
      ],
      estimatedHours: 12,
      dependencies: ['1'],
    },
    {
      id: '3',
      title: 'Integrate payment gateway',
      subtasks: [
        'VNPay integration',
        'Momo integration',
        'Payment verification',
        'Error handling',
      ],
      estimatedHours: 20,
      dependencies: ['2'],
    },
  ],
  dependencies: [
    'Product catalog API',
    'User authentication',
    'Payment gateway credentials',
  ],
  estimatedHours: 48,
}
```

### 3. Validate Plan Before Execution
```typescript
interface PlanValidation {
  isComplete: boolean
  missingInfo: string[]
  blockers: string[]
  risks: string[]
}

function validatePlan(plan: Plan): PlanValidation {
  const validation: PlanValidation = {
    isComplete: true,
    missingInfo: [],
    blockers: [],
    risks: [],
  }
  
  // Check dependencies
  plan.dependencies.forEach((dep) => {
    if (!isDependencyReady(dep)) {
      validation.blockers.push(`Dependency not ready: ${dep}`)
      validation.isComplete = false
    }
  })
  
  // Check step completeness
  plan.steps.forEach((step) => {
    if (!step.estimatedHours) {
      validation.missingInfo.push(`No estimate for: ${step.title}`)
    }
    if (step.subtasks.length === 0) {
      validation.missingInfo.push(`No subtasks for: ${step.title}`)
    }
  })
  
  return validation
}
```

## Ví dụ thực tế

### Planning Phase: E-commerce Architecture

```markdown
# Plan: E-commerce Flower Shop Architecture

## Goal
Thiết kế scalable, maintainable architecture cho e-commerce platform
với 10K+ products, 1K+ concurrent users.

## Context
- Startup với limited budget
- Team: 2 FE, 2 BE, 1 DevOps
- Timeline: 3 months MVP
- Must integrate: VNPay, Momo, GHN

## Approach
Monorepo với Next.js + PayloadCMS, deploy trên Vercel + MongoDB Atlas.

## Steps

### 1. Tech Stack Selection (Week 1)
- [ ] Evaluate Next.js vs Remix
- [ ] Choose CMS: PayloadCMS vs Strapi
- [ ] Database: MongoDB vs PostgreSQL
- [ ] Hosting: Vercel vs Railway
- [ ] Document decision rationale

**Estimated**: 20 hours

### 2. Architecture Design (Week 1-2)
- [ ] Design database schema
- [ ] Define API contracts
- [ ] Plan authentication flow
- [ ] Design payment integration
- [ ] Create architecture diagram

**Estimated**: 30 hours

### 3. Project Setup (Week 2)
- [ ] Initialize monorepo
- [ ] Setup Next.js + TypeScript
- [ ] Configure PayloadCMS
- [ ] Setup MongoDB
- [ ] Configure CI/CD

**Estimated**: 16 hours

### 4. Core Collections (Week 3-4)
- [ ] Product collection
- [ ] Category collection
- [ ] Order collection
- [ ] User collection
- [ ] Payment session collection

**Estimated**: 40 hours

## Dependencies
- ✅ MongoDB Atlas account
- ✅ Vercel account
- ⏳ VNPay merchant account (pending)
- ⏳ Momo merchant account (pending)
- ✅ GHN API credentials

## Risks
| Risk | Impact | Mitigation |
|------|--------|------------|
| Payment gateway approval delay | High | Start with test credentials, parallel process |
| Team learning curve (PayloadCMS) | Medium | Allocate 1 week learning time |
| MongoDB Atlas cost | Medium | Monitor usage, optimize queries |

## Success Criteria
- [ ] Architecture document approved by CTO
- [ ] All team members understand architecture
- [ ] Project setup complete và runnable
- [ ] Core collections defined và tested
- [ ] CI/CD pipeline working
```

## Plan Review Checklist

### Before Execution
- [ ] Goal rõ ràng và measurable?
- [ ] Steps actionable và có estimate?
- [ ] Dependencies identified?
- [ ] Risks assessed?
- [ ] Success criteria defined?
- [ ] Team alignment achieved?

### During Execution
- [ ] Track progress against plan
- [ ] Update estimates based on actuals
- [ ] Document deviations
- [ ] Adjust plan khi cần

### After Execution
- [ ] Review actual vs estimated
- [ ] Document lessons learned
- [ ] Update planning process

## Trade-offs

| Ưu điểm | Nhược điểm |
|---------|------------|
| Clear roadmap | Upfront time investment |
| Better estimates | Plan có thể outdated |
| Risk mitigation | Có thể over-plan |
| Team alignment | Cần discipline follow |

## Best Practices
1. **Start with why**: Rõ ràng về goal trước khi plan
2. **Break down ruthlessly**: Mỗi step < 1 day work
3. **Estimate conservatively**: Add buffer cho unknowns
4. **Validate dependencies**: Confirm blockers trước khi start
5. **Review regularly**: Plan là living document
6. **Learn from actuals**: Improve estimation over time

## Anti-patterns
- ❌ Plan quá chi tiết (analysis paralysis)
- ❌ Plan rồi không follow
- ❌ Không update plan khi có changes
- ❌ Plan một mình không involve team
- ❌ Ignore risks và dependencies

## Related Patterns
- [Todo Management](./pattern-todo-management.md)
- [Memory System](./pattern-memory-system.md)
