# Pattern: Todo Management

## Nguồn
- Claude Code
- Cursor Agent
- Windsurf Cascade

## Mô tả
Quản lý tasks có cấu trúc, track progress, dependencies, và priorities để đảm bảo project delivery đúng hạn.

## Khi nào dùng
- Planning phase: break down project thành tasks
- Development: track implementation progress
- Testing: manage test cases, bug fixes
- Maintenance: prioritize feature requests, bugs

## Cách áp dụng

### 1. Task Structure
```typescript
interface Task {
  id: string
  title: string
  description: string
  status: 'todo' | 'in-progress' | 'blocked' | 'done'
  priority: 'low' | 'medium' | 'high' | 'critical'
  assignee?: string
  dependencies?: string[] // task IDs
  estimatedHours?: number
  actualHours?: number
  dueDate?: Date
  tags?: string[]
}
```

### 2. Task Breakdown (WBS)
```
Project: E-commerce Flower Shop
├── 1. Discovery (2 weeks)
│   ├── 1.1 Stakeholder interviews
│   ├── 1.2 User research
│   └── 1.3 Competitor analysis
├── 2. Planning (2 weeks)
│   ├── 2.1 Architecture design
│   ├── 2.2 Tech stack selection
│   └── 2.3 Milestone planning
├── 3. Design (3 weeks)
│   ├── 3.1 Design system
│   ├── 3.2 Wireframes
│   └── 3.3 High-fidelity mockups
└── 4. Development (8 weeks)
    ├── 4.1 Frontend setup
    ├── 4.2 Backend API
    └── 4.3 Integration
```

### 3. Dependency Management
```typescript
const tasks: Task[] = [
  {
    id: 'task-1',
    title: 'Design database schema',
    status: 'done',
    priority: 'high',
  },
  {
    id: 'task-2',
    title: 'Implement user authentication',
    status: 'in-progress',
    priority: 'high',
    dependencies: ['task-1'], // Blocked until task-1 done
  },
  {
    id: 'task-3',
    title: 'Build product catalog',
    status: 'todo',
    priority: 'medium',
    dependencies: ['task-1', 'task-2'],
  },
]

// Check if task can start
function canStartTask(task: Task, allTasks: Task[]): boolean {
  if (!task.dependencies) return true
  
  return task.dependencies.every((depId) => {
    const depTask = allTasks.find((t) => t.id === depId)
    return depTask?.status === 'done'
  })
}
```

## Ví dụ thực tế

### Planning Phase: Sprint Planning

```typescript
// Sprint 1: Foundation (2 weeks)
const sprint1: Task[] = [
  {
    id: 's1-t1',
    title: 'Setup Next.js project',
    status: 'done',
    priority: 'critical',
    estimatedHours: 4,
    actualHours: 3,
  },
  {
    id: 's1-t2',
    title: 'Design database schema',
    status: 'done',
    priority: 'critical',
    estimatedHours: 8,
    actualHours: 10,
  },
  {
    id: 's1-t3',
    title: 'Setup PayloadCMS',
    status: 'done',
    priority: 'high',
    estimatedHours: 6,
    actualHours: 8,
    dependencies: ['s1-t1', 's1-t2'],
  },
]

// Sprint 2: Core Features (2 weeks)
const sprint2: Task[] = [
  {
    id: 's2-t1',
    title: 'Implement product catalog',
    status: 'in-progress',
    priority: 'high',
    estimatedHours: 16,
    dependencies: ['s1-t3'],
  },
  {
    id: 's2-t2',
    title: 'Build shopping cart',
    status: 'todo',
    priority: 'high',
    estimatedHours: 12,
    dependencies: ['s2-t1'],
  },
]
```

### Task Board Visualization

```
┌─────────────┬──────────────┬──────────────┬──────────────┐
│   TODO      │ IN PROGRESS  │   BLOCKED    │     DONE     │
├─────────────┼──────────────┼──────────────┼──────────────┤
│ Build cart  │ Product      │ Payment      │ Setup Next   │
│ (High)      │ catalog      │ integration  │ (Critical)   │
│             │ (High)       │ (Medium)     │              │
│             │              │ [Waiting API]│ DB schema    │
│ Checkout    │ User auth    │              │ (Critical)   │
│ (High)      │ (High)       │              │              │
│             │              │              │ Setup CMS    │
│ Reviews     │              │              │ (High)       │
│ (Low)       │              │              │              │
└─────────────┴──────────────┴──────────────┴──────────────┘
```

## Metrics & Tracking

```typescript
interface SprintMetrics {
  totalTasks: number
  completedTasks: number
  inProgressTasks: number
  blockedTasks: number
  completionRate: number
  velocityPoints: number
  estimatedVsActual: {
    estimated: number
    actual: number
    variance: number
  }
}

function calculateMetrics(tasks: Task[]): SprintMetrics {
  const completed = tasks.filter((t) => t.status === 'done')
  const inProgress = tasks.filter((t) => t.status === 'in-progress')
  const blocked = tasks.filter((t) => t.status === 'blocked')
  
  const totalEstimated = tasks.reduce(
    (sum, t) => sum + (t.estimatedHours || 0),
    0
  )
  const totalActual = completed.reduce(
    (sum, t) => sum + (t.actualHours || 0),
    0
  )
  
  return {
    totalTasks: tasks.length,
    completedTasks: completed.length,
    inProgressTasks: inProgress.length,
    blockedTasks: blocked.length,
    completionRate: (completed.length / tasks.length) * 100,
    velocityPoints: completed.length,
    estimatedVsActual: {
      estimated: totalEstimated,
      actual: totalActual,
      variance: ((totalActual - totalEstimated) / totalEstimated) * 100,
    },
  }
}
```

## Trade-offs

| Ưu điểm | Nhược điểm |
|---------|------------|
| Clear visibility | Overhead maintain tasks |
| Better planning | Có thể quá rigid |
| Track progress | Cần discipline |

## Best Practices
1. **Break down large tasks**: Mỗi task nên < 1 day work
2. **Update status daily**: Keep board current
3. **Review dependencies**: Unblock tasks ASAP
4. **Track actual vs estimated**: Improve estimation
5. **Prioritize ruthlessly**: Focus on high-impact tasks

## Anti-patterns
- ❌ Tasks quá lớn (> 2 days)
- ❌ Không update status
- ❌ Ignore dependencies
- ❌ Không track actual hours
- ❌ Quá nhiều tasks "in progress"

## Related Patterns
- [Plan Mode](./pattern-plan-mode.md)
- [Memory System](./pattern-memory-system.md)
