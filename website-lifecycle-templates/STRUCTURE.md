# Website Lifecycle Templates - Structure Guide

> **Standardized 4-Directory Architecture**
> **Last Updated**: 2026-04-23

---

## 📁 Standard Structure

Mỗi phase tuân theo cấu trúc 4-directory chuẩn:

```
{phase}/
├── patterns/     # Design patterns, best practices, workflows
├── prompts/      # AI tool prompts (Claude, ChatGPT, v1, etc.)
├── templates/    # Document templates, checklists, forms
└── examples/     # Real-world examples, case studies
```

---

## 🎯 Directory Purposes

### `patterns/`
**Chứa**: Architecture patterns, best practices, workflows, decision frameworks

**Ví dụ**:
- `pattern.research-methodology.md` - Cách research hiệu quả
- `pattern.stakeholder-interview.md` - Framework phỏng vấn stakeholder
- `pattern.design-system-setup.md` - Thiết lập design system

**Naming**: `pattern.{name}.md`

---

### `prompts/`
**Chứa**: AI tool prompts cho automation tasks

**Ví dụ**:
- `prompt.claude.competitor-analysis.md` - Claude prompt phân tích đối thủ
- `prompt.v1.wireframe-generation.md` - v1 prompt tạo wireframe
- `prompt.chatgpt.content-outline.md` - ChatGPT prompt outline content

**Naming**: `prompt.{tool}.{task}.md`

**Supported tools**: `claude`, `chatgpt`, `v1`, `cursor`, `windsurf`, `copilot`

---

### `templates/`
**Chứa**: Document templates, checklists, forms

**Ví dụ**:
- `template.discovery-report.md` - Template báo cáo discovery
- `template.design-brief.md` - Template design brief
- `template.test-plan.md` - Template test plan

**Naming**: `template.{name}.md`

---

### `examples/`
**Chứa**: Real-world examples, case studies, sample outputs

**Ví dụ**:
- `example.ecommerce-discovery.md` - Discovery cho e-commerce project
- `example.saas-design-system.md` - Design system cho SaaS
- `example.api-test-suite.md` - Test suite cho API

**Naming**: `example.{name}.md`

---

## 📋 Naming Conventions

### File Naming Pattern
```
{type}.{tool?}.{name}.md
```

| Type | Tool (optional) | Name | Example |
|------|----------------|------|---------|
| `pattern` | - | `research-methodology` | `pattern.research-methodology.md` |
| `prompt` | `claude` | `competitor-analysis` | `prompt.claude.competitor-analysis.md` |
| `template` | - | `discovery-report` | `template.discovery-report.md` |
| `example` | - | `ecommerce-discovery` | `example.ecommerce-discovery.md` |

### Rules
- ✅ Lowercase, kebab-case
- ✅ Descriptive names (< 50 chars)
- ✅ Tool prefix for prompts only
- ❌ No spaces, underscores, or special chars

---

## ➕ Adding New Content

### Step 1: Identify Type
```
Is it a...
├── Workflow/Pattern? → patterns/
├── AI Prompt? → prompts/
├── Document Template? → templates/
└── Real Example? → examples/
```

### Step 2: Choose Phase
```
1-discovery     → Research, requirements, stakeholder analysis
2-planning      → Project planning, roadmap, resource allocation
3-design        → UI/UX design, wireframes, prototypes
4-content       → Content strategy, copywriting, SEO
5-development   → Coding, implementation, integration
6-testing       → QA, testing, bug tracking
7-maintenance   → Monitoring, updates, optimization
```

### Step 3: Create File
```bash
# Pattern
touch {phase}/patterns/pattern.{name}.md

# Prompt
touch {phase}/prompts/prompt.{tool}.{task}.md

# Template
touch {phase}/templates/template.{name}.md

# Example
touch {phase}/examples/example.{name}.md
```

### Step 4: Update INDEX.md
Add entry to phase's INDEX.md:
```markdown
## Patterns
- [Pattern Name](patterns/pattern.{name}.md) - Brief description

## Prompts
- [Prompt Name](prompts/prompt.{tool}.{task}.md) - Brief description
```

---

## 🔗 Integration Guidelines

### Cross-Phase References
```markdown
**Related**:
- [2-Planning: Project Brief Template](../2-planning/templates/template.project-brief.md)
- [3-Design: Design System Pattern](../3-design/patterns/pattern.design-system.md)
```

### Internal References
```markdown
**See also**:
- [Research Pattern](patterns/pattern.research-methodology.md)
- [Discovery Template](templates/template.discovery-report.md)
```

### External References
```markdown
**Resources**:
- [Nielsen Norman Group](https://www.nngroup.com/)
- [Smashing Magazine](https://www.smashingmagazine.com/)
```

---

## ✅ Consistency Checklist

### Before Adding Content
- [ ] Correct directory (patterns/prompts/templates/examples)?
- [ ] Naming convention followed?
- [ ] Phase appropriate?
- [ ] INDEX.md updated?

### After Adding Content
- [ ] Cross-references working?
- [ ] No duplicate content?
- [ ] Frontmatter complete (if applicable)?
- [ ] Examples clear and actionable?

---

## 📊 Current Structure

```
website-lifecycle-templates/
├── 1-discovery/
│   ├── patterns/
│   ├── prompts/
│   ├── templates/
│   └── examples/
├── 2-planning/
│   ├── patterns/
│   ├── prompts/
│   ├── templates/
│   └── examples/
├── 3-design/
│   ├── patterns/
│   ├── prompts/
│   ├── templates/
│   └── examples/
├── 4-content/
│   ├── patterns/
│   ├── prompts/
│   ├── templates/
│   └── examples/
├── 5-development/
│   ├── patterns/
│   ├── prompts/
│   ├── templates/
│   └── examples/
├── 6-testing/
│   ├── patterns/
│   ├── prompts/
│   ├── templates/
│   └── examples/
└── 7-maintenance/
    ├── patterns/
    ├── prompts/
    ├── templates/
    └── examples/
```

---

## 🎯 Quick Reference

| Task | Command |
|------|---------|
| Add pattern | `touch {phase}/patterns/pattern.{name}.md` |
| Add prompt | `touch {phase}/prompts/prompt.{tool}.{task}.md` |
| Add template | `touch {phase}/templates/template.{name}.md` |
| Add example | `touch {phase}/examples/example.{name}.md` |
| Update index | Edit `{phase}/INDEX.md` |
| Verify structure | `find . -type d -maxdepth 2` |

---

**Maintained by**: attach_by_security team
**Version**: 1.0.0
