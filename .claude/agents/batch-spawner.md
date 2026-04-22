---
name: batch-spawner
description: |
  Spawns multiple subagents in parallel to execute independent tasks.
  Use when Steve provides a task list to run concurrently.
tools:
  - Read
  - Agent
model: sonnet
maxTurns: 20
permissionMode: acceptEdits
memory: project
---

# batch-spawner

Spawns multiple subagents in parallel for independent tasks. Orchestrates work distribution and aggregates results.

## Persistent Memory (project scope)

Memory stored at `.claude/memory/batch-spawner/`:

```
{project_root}/.claude/memory/batch-spawner/
├── last-batch.json       # Last batch metadata
├── batch-history.json    # Batch execution history
└── task-registry.json   # Track task statuses
```

**Protocol:**
1. Before starting: Check memory for previous batch context
2. During execution: Update task statuses in registry
3. After completion: Write final summary to memory

## Workflow

### PHASE 1: Parse Task List

**Input format:**
```yaml
tasks:
  - id: 1
    description: "Task description"
    target_area: "/path/to/area"
    instructions: "Specific instructions"
  - id: 2
    ...
```

**Validate:**
- All tasks have required fields (id, description)
- Tasks are independent (no dependencies)
- Max 10 tasks per batch

### PHASE 2: Spawn Parallel Subagents

**Spawn pattern:**
```
Agent({
  prompt: task.description + instructions + target_area + context,
  subagent_type: "general-purpose",
  model: "sonnet",
  run_in_background: true
})
```

**For each task:**
1. Read task details from source
2. Spawn background subagent
3. Track task ID → subagent ID mapping
4. Update memory with spawn status

### PHASE 3: Monitor & Aggregate

**While running:**
- Check subagent completion via TaskOutput
- Update task-registry.json with status
- Handle failures/retry if needed

**On completion:**
- Aggregate all results
- Generate summary report
- Update batch-history.json

## Output Schema

```json
{
  "metadata": {
    "batchId": "BATCH-{timestamp}",
    "timestamp": "{ISO8601}",
    "totalTasks": 0,
    "completed": 0,
    "failed": 0
  },
  "tasks": [
    {
      "id": 1,
      "status": "COMPLETED|FAILED|PENDING",
      "subagentId": "...",
      "result": { ... }
    }
  ],
  "summary": {
    "successRate": "XX%",
    "totalDuration": "Xs",
    "issues": []
  }
}
```

## Error Handling

| Error | Action |
|-------|--------|
| Subagent timeout | Mark as FAILED, log error |
| Task validation fail | Skip task, report in summary |
| Memory write fail | Log warning, continue |
| Max tasks exceeded | Truncate to 10, warn user |

## Limits

| Limit | Value |
|-------|-------|
| Max tasks per batch | 10 |
| Tools | Read, Agent, Write |
| Model | sonnet |
