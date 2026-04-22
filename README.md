# E-commerce Prompt Research Project

## Mục tiêu
Nghiên cứu và phân tích prompt templates cho 7 giai đoạn xây dựng website thương mại điện tử.

## 7 Phases

1. **Discovery** - Thu thập yêu cầu, phân tích business
2. **Planning** - IA, sitemap, wireframe, tech stack
3. **Design** - UI/UX, component, responsive
4. **Content** - Copywriting, SEO, metadata
5. **Development** - Frontend/Backend coding
6. **Testing** - QA, security, performance
7. **Maintenance** - Bug fix, optimization, updates

## Cấu trúc Project

```
attach_by_security/
├── STATE.md                    # Heartbeat state (QUAN TRỌNG)
├── RESEARCH_PROMPT.md          # Prompt template cho agent
├── README.md                   # File này
├── reports/                    # Research reports
│   ├── discovery/
│   ├── planning/
│   ├── design/
│   ├── content/
│   ├── development/
│   ├── testing/
│   └── maintenance/
└── templates/                  # Master templates (weekly consolidation)
    └── (sẽ tạo sau)
```

## Cách sử dụng

### Option 1: /loop Dynamic Mode (Chạy ngay)

```bash
# Trong Claude Code session
/loop Execute RESEARCH_PROMPT.md with 10-minute intervals
```

### Option 2: Routines (24/7, min 1h interval)

1. Vào claude.ai/code/routines
2. Tạo routine mới với prompt từ `RESEARCH_PROMPT.md`
3. Chọn repo này
4. Schedule: Hourly (hoặc custom cron)
5. Enable "Allow unrestricted branch pushes"

### Option 3: API Trigger (On-demand)

```bash
curl -X POST https://api.anthropic.com/v1/claude_code/routines/trig_xxx/fire \
  -H "Authorization: Bearer $CLAUDE_API_KEY" \
  -H "anthropic-beta: experimental-cc-routine-2026-04-01" \
  -H "Content-Type: application/json" \
  -d '{"text": "Run research cycle now"}'
```

## Heartbeat Pattern

Mỗi lần chạy:
1. Đọc `STATE.md` → load context
2. Research phase hiện tại → tìm templates
3. Update `STATE.md` → save progress
4. Commit → Git history
5. Đợi 10 phút → loop

**Lợi ích**: Vượt giới hạn 200k tokens, state không bao giờ mất.

## Progress Tracking

Check `STATE.md` để xem:
- Phase hiện tại
- Số templates đã tìm được
- Next action
- Last run timestamp

## Git Workflow

```bash
# Agent tự động commit vào branch
git checkout -b claude/prompt-research

# Mỗi cycle tạo commit
git log --oneline
# [Phase] Research cycle #1: Found 3 templates
# [Phase] Research cycle #2: Found 5 templates
```

## Kết quả mong đợi

Sau 7 cycles (1 cycle/phase):
- 35+ prompt templates (5/phase)
- Detailed analysis reports
- Master templates (weekly consolidation)
- Actionable insights cho mỗi phase

## Lưu ý

- **Min interval**: Schedule trigger = 1h, /loop = linh hoạt
- **Context limit**: 200k tokens/session → Heartbeat pattern giải quyết
- **Cost**: ~7 sessions/day (nếu hourly) → estimate theo plan
