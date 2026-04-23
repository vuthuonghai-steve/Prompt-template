# Development Phase - README

> Practical templates and prompts for coding, testing, and implementation
> Last Updated: 2026-04-22

---

## 📁 Structure

```
5-development/
├── templates/
│   ├── coding-standards.md      # Code quality guidelines
│   ├── project-structure.md     # Folder organization patterns
│   ├── api-design.md            # RESTful API conventions
│   ├── database-schema.md       # Database design patterns
│   └── git-workflow.md          # Version control best practices
└── prompts/
    ├── cursor-coding-prompt.md  # Cursor Agent implementation
    └── windsurf-refactor-prompt.md  # Windsurf refactoring
```

---

## 🎯 Phase Overview

Development phase covers:
- **Code Implementation**: Writing production-ready code
- **Testing**: Unit, integration, E2E tests
- **Version Control**: Git workflow and collaboration
- **Code Review**: Quality assurance processes
- **Documentation**: Code comments and API docs

---

## 📋 Templates

### 1. Coding Standards
**Purpose**: Ensure consistent, maintainable code quality

**Key Topics**:
- Naming conventions
- Code organization
- TypeScript best practices
- Security practices
- Testing standards
- Comments & documentation

**When to Use**: Before starting any coding task

---

### 2. Project Structure
**Purpose**: Organize codebase for scalability

**Key Topics**:
- Folder hierarchy patterns
- File naming conventions
- Module organization
- Configuration management

**When to Use**: Setting up new projects or refactoring structure

---

### 3. API Design
**Purpose**: Build consistent, RESTful APIs

**Key Topics**:
- URL structure patterns
- HTTP methods & status codes
- Request/response formats
- Error handling
- Authentication/authorization
- API versioning

**When to Use**: Designing new endpoints or refactoring APIs

---

### 4. Database Schema
**Purpose**: Design efficient, scalable databases

**Key Topics**:
- Table naming conventions
- Relationship patterns
- Indexing strategies
- Migration patterns
- Query optimization
- ORM integration

**When to Use**: Designing data models or optimizing queries

---

### 5. Git Workflow
**Purpose**: Manage code changes effectively

**Key Topics**:
- Branch strategies
- Commit message conventions
- Pull request process
- Code review guidelines
- Pre-commit hooks

**When to Use**: Throughout development lifecycle

---

## 🤖 AI Prompts

### 1. Cursor Coding Prompt
**Tool**: Cursor Agent
**Use Case**: Intelligent code implementation

**Strengths**:
- Semantic codebase search
- Context-aware suggestions
- Multi-file edits
- Pattern recognition

**Best For**:
- Implementing new features
- Following existing patterns
- Refactoring with consistency

---

### 2. Windsurf Refactor Prompt
**Tool**: Windsurf Cascade
**Use Case**: Autonomous refactoring

**Strengths**:
- Agentic execution
- Memory system
- Multi-step planning
- Performance optimization

**Best For**:
- Large-scale refactoring
- Architecture changes
- Performance improvements
- Technical debt reduction

---

## 🔍 Pattern Sources

Templates extracted from:
- **Cursor Agent**: Semantic understanding, code patterns
- **VSCode Agent**: Testing, documentation standards
- **Windsurf**: Refactoring, architecture patterns
- **Claude Code**: TypeScript, error handling
- **Replit**: API conventions, response formats

---

## 📊 Usage Guide

### For New Projects
1. Start with **Project Structure** template
2. Setup **Git Workflow** (branches, hooks)
3. Define **Coding Standards**
4. Design **API** and **Database Schema**
5. Use AI prompts for implementation

### For Existing Projects
1. Review **Coding Standards** for consistency
2. Audit **Project Structure** for improvements
3. Refactor **API** for consistency
4. Optimize **Database Schema**
5. Use **Windsurf Refactor Prompt** for large changes

### For Code Reviews
1. Check against **Coding Standards**
2. Verify **Git Workflow** compliance
3. Review **API Design** consistency
4. Validate **Database Schema** changes

---

## 🎨 Quick Reference

| Task | Template | AI Prompt |
|------|----------|-----------|
| New feature | Coding Standards + Project Structure | Cursor Coding |
| API endpoint | API Design | Cursor Coding |
| Database model | Database Schema | Cursor Coding |
| Refactoring | Coding Standards | Windsurf Refactor |
| Performance | Database Schema + API Design | Windsurf Refactor |
| Code review | All templates | - |

---

## 📝 Implementation Workflow

```
1. PLAN
   ├─ Review relevant templates
   ├─ Understand existing patterns
   └─ Define requirements

2. IMPLEMENT
   ├─ Use AI prompts for coding
   ├─ Follow coding standards
   └─ Write tests

3. REVIEW
   ├─ Self-review against templates
   ├─ Run linters/tests
   └─ Create PR

4. ITERATE
   ├─ Address review feedback
   ├─ Refactor if needed
   └─ Merge when approved
```

---

## 🔗 Related Phases

- **Previous**: [4-design](../4-design/) - UI/UX design
- **Next**: [6-testing](../6-testing/) - QA and testing
- **See Also**: [3-planning](../3-planning/) - Technical planning

---

## 📚 Additional Resources

### Tools
- **Linters**: ESLint, Prettier
- **Testing**: Vitest, Jest, Playwright
- **Git**: Husky, lint-staged, commitlint
- **Documentation**: JSDoc, Swagger/OpenAPI

### Best Practices
- Clean Code (Robert C. Martin)
- Refactoring (Martin Fowler)
- Design Patterns (Gang of Four)
- Test-Driven Development

---

**Navigation**:
- [← Back to Main](../README.md)
- [Templates →](./templates/)
- [Prompts →](./prompts/)
