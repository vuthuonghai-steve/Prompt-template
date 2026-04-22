# Quick Start Guide

> **Hướng dẫn nhanh sử dụng Website Lifecycle Templates**

---

## 🚀 Bắt đầu

### 1. Chọn Phase đang làm việc

```
1-discovery/     → Đang thu thập requirements?
2-planning/      → Đang thiết kế architecture?
3-design/        → Đang design UI/UX?
4-content/       → Đang viết content?
5-development/   → Đang code?
6-testing/       → Đang test?
7-maintenance/   → Đang maintain production?
```

### 2. Đọc INDEX.md trong phase

Mỗi phase có `INDEX.md` với:
- 📋 Checklist
- 📁 Danh sách templates
- 🎯 AI prompts tham khảo
- 🔗 Navigation links

### 3. Sử dụng Templates

Templates nằm trong thư mục `templates/` của mỗi phase.

**Ví dụ**:
```bash
# Discovery phase
1-discovery/templates/requirements.md
1-discovery/templates/user-stories.md

# Development phase
5-development/templates/api-design.md
5-development/templates/coding-standards.md
```

---

## 📚 Templates có sẵn

### Phase 1: Discovery
- `requirements.md` - Requirements document
- `user-stories.md` - User stories format
- `use-cases.md` - Use cases template
- `risk-analysis.md` - Risk assessment

### Phase 2: Planning
- `sitemap.md` - Sitemap structure
- `tech-stack-decision.md` - Tech comparison
- `architecture-decision.md` - ADR format
- `milestone-plan.md` - Timeline planning

### Phase 3: Design
- `design-system.md` - Design system structure
- `component-spec.md` - Component specs
- `color-palette.md` - Color guidelines
- `typography.md` - Typography scale

### Phase 4: Content
- `content-guidelines.md` - ✅ Tone of voice, style guide
- `seo-checklist.md` - ✅ SEO optimization
- `metadata-template.md` - Meta tags
- `copywriting-brief.md` - Copy brief

### Phase 5: Development
- `project-structure.md` - Folder structure
- `api-design.md` - API conventions
- `database-schema.md` - DB design
- `coding-standards.md` - Code style

### Phase 6: Testing
- `test-plan.md` - ✅ Comprehensive testing
- `bug-report.md` - ✅ Bug tracking
- `performance-checklist.md` - Performance audit
- `security-checklist.md` - Security audit

### Phase 7: Maintenance
- `feature-request.md` - ✅ New feature proposal
- `maintenance-log.md` - ✅ Change tracking
- `performance-report.md` - ✅ Performance optimization
- `incident-report.md` - Production incidents

**Legend**: ✅ = Template đã hoàn thành

---

## 🎯 Use Cases

### Scenario 1: Bắt đầu dự án mới
1. Đọc `1-discovery/INDEX.md`
2. Dùng `requirements.md` để gather requirements
3. Dùng `user-stories.md` để viết user stories
4. Chuyển sang `2-planning/` khi xong

### Scenario 2: Đang code feature mới
1. Đọc `5-development/INDEX.md`
2. Follow `coding-standards.md`
3. Tham khảo `api-design.md` cho API endpoints
4. Chuyển sang `6-testing/` khi code xong

### Scenario 3: Production có bug
1. Đọc `7-maintenance/INDEX.md`
2. Dùng `bug-report.md` để track bug
3. Dùng `maintenance-log.md` để log fix
4. Dùng `performance-report.md` nếu liên quan performance

---

## 🤖 AI Prompts

Mỗi phase có section **🎯 AI Prompts** trong INDEX.md, liệt kê:
- AI tools phù hợp (Cursor, Claude Code, Windsurf, etc.)
- Prompts tham khảo từ các tools
- Best practices từ industry

**Đang xây dựng**: Agents đang trích xuất prompts từ `system-prompts-and-models-of-ai-tools/`

---

## 📊 Progress Tracking

| Phase | Templates | Status |
|-------|-----------|--------|
| 1. Discovery | 4 templates | 🚧 In Progress |
| 2. Planning | 4 templates | 🚧 In Progress |
| 3. Design | 4 templates | 🚧 In Progress |
| 4. Content | 4 templates | ✅ 2/4 Done |
| 5. Development | 4 templates | 🚧 In Progress |
| 6. Testing | 4 templates | ✅ 2/4 Done |
| 7. Maintenance | 4 templates | ✅ 3/4 Done |

---

## 🔗 Quick Links

- [Main README](./README.md)
- [Phase 1: Discovery](./1-discovery/INDEX.md)
- [Phase 2: Planning](./2-planning/INDEX.md)
- [Phase 3: Design](./3-design/INDEX.md)
- [Phase 4: Content](./4-content/INDEX.md)
- [Phase 5: Development](./5-development/INDEX.md)
- [Phase 6: Testing](./6-testing/INDEX.md)
- [Phase 7: Maintenance](./7-maintenance/INDEX.md)

---

## 💡 Tips

1. **Không cần follow tuyến tính**: Có thể nhảy giữa các phases
2. **Customize templates**: Adapt cho project của bạn
3. **Combine với AI tools**: Dùng prompts từ Cursor, Claude Code để tăng tốc
4. **Iterate**: Templates sẽ được cải thiện dựa trên feedback

---

**Last Updated**: 2026-04-23
**Status**: 🚧 Multi-agent system đang xây dựng
