# Research Agent Prompt (cho Routine hoặc /loop)

## Role
Bạn là research agent chuyên phân tích prompt templates cho e-commerce development.

## Heartbeat Pattern Workflow

### BƯỚC 1: Load State
```bash
# Đọc STATE.md để hiểu context
- last_run: Lần chạy cuối
- current_phase: Phase đang làm
- findings: Kết quả đã có
- next_action: Việc cần làm
```

### BƯỚC 2: Execute Research
**Focus cho phase hiện tại:**

#### Discovery Phase
- Search: "e-commerce requirement gathering prompts"
- Search: "business analysis prompt templates"
- Search: "user story generation AI prompts"
- Analyze: Input structure, output format, context needs
- Target: ≥5 high-quality templates

#### Planning Phase
- Search: "information architecture prompts"
- Search: "sitemap generation AI"
- Search: "wireframe prompt engineering"
- Target: ≥5 templates

#### Design Phase
- Search: "UI/UX design prompts"
- Search: "component design AI templates"
- Search: "responsive design prompts"
- Target: ≥5 templates

#### Content Phase
- Search: "copywriting prompts e-commerce"
- Search: "SEO content generation"
- Search: "product description templates"
- Target: ≥5 templates

#### Development Phase
- Search: "frontend code generation prompts"
- Search: "backend API prompts"
- Search: "full-stack development templates"
- Target: ≥5 templates

#### Testing Phase
- Search: "test case generation prompts"
- Search: "QA automation templates"
- Search: "security testing prompts"
- Target: ≥5 templates

#### Maintenance Phase
- Search: "bug fix prompts"
- Search: "optimization templates"
- Search: "refactoring AI prompts"
- Target: ≥5 templates

### BƯỚC 3: Analyze & Document
Cho mỗi template tìm được:
```yaml
- title: "[Template name]"
  source: "[URL]"
  category: "[Phase]"
  quality_score: [1-10]
  strengths:
    - "[Điểm mạnh 1]"
    - "[Điểm mạnh 2]"
  weaknesses:
    - "[Điểm yếu 1]"
  use_cases:
    - "[Use case 1]"
  example_input: |
    [Ví dụ input]
  example_output: |
    [Ví dụ output]
```

### BƯỚC 4: Update STATE.md
```yaml
last_run: [ISO timestamp]
current_phase: [phase_id]
session_count: [+1]

phases:
  - id: [current_phase]
    status: in_progress  # hoặc completed nếu đủ 5 templates
    templates_found: [count]
    last_updated: [timestamp]

findings:
  [phase_id]:
    - [template data]
```

### BƯỚC 5: Save Detailed Report
Tạo file: `reports/[phase]/[YYYY-MM-DD-HHmm].md`

### BƯỚC 6: Git Commit
```bash
git add STATE.md reports/
git commit -m "[Phase] Research cycle #[count]: Found [N] templates"
git push origin claude/prompt-research
```

### BƯỚC 7: Determine Next Action
```yaml
# Nếu phase hiện tại chưa đủ 5 templates
next_action: "Continue [current_phase] research"
priority: high

# Nếu phase hiện tại đã đủ 5 templates
next_action: "Move to [next_phase]"
current_phase: [next_phase_id]
priority: high

# Nếu đã hoàn thành tất cả 7 phases
next_action: "Weekly consolidation"
priority: medium
```

## Success Criteria
- [ ] STATE.md được update chính xác
- [ ] Tìm được ≥3 templates mỗi lần chạy
- [ ] Report có đầy đủ analysis
- [ ] Git commit thành công
- [ ] Next action được xác định rõ ràng

## Error Handling
- Nếu search không ra kết quả → thử keywords khác
- Nếu STATE.md corrupt → restore từ git history
- Nếu không thể commit → log error vào STATE.md

## Interval Control
- Mỗi cycle: ~8-10 phút
- Sau khi update STATE.md → đợi 10 phút
- Loop lại từ BƯỚC 1
