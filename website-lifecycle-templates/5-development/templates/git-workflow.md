# Git Workflow Template

> Extracted from: Cursor, VSCode Agent, Windsurf, Claude Code
> Phase: Development
> Last Updated: 2026-04-22

---

## 🎯 Core Principles

### 1. Branch Strategy
- **main/master**: Production-ready code
- **develop**: Integration branch
- **feature/***: New features
- **bugfix/***: Bug fixes
- **hotfix/***: Emergency production fixes

### 2. Commit Guidelines
- **Atomic commits**: One logical change per commit
- **Descriptive messages**: Clear, concise commit messages
- **Conventional commits**: Follow standard format

---

## 📋 Branch Naming Conventions

```bash
# Feature branches
feature/user-authentication
feature/payment-integration
feature/admin-dashboard

# Bugfix branches
bugfix/login-error
bugfix/cart-calculation

# Hotfix branches
hotfix/security-patch
hotfix/critical-bug

# Release branches
release/v1.2.0
```

---

## 🔧 Git Workflow

### Feature Development Flow
```bash
# 1. Create feature branch from develop
git checkout develop
git pull origin develop
git checkout -b feature/user-authentication

# 2. Work on feature (multiple commits)
git add .
git commit -m "feat: add user registration form"
git commit -m "feat: implement email verification"

# 3. Keep branch updated
git fetch origin
git rebase origin/develop

# 4. Push to remote
git push origin feature/user-authentication

# 5. Create Pull Request
# (via GitHub/GitLab UI)

# 6. After PR approval, merge to develop
git checkout develop
git merge --no-ff feature/user-authentication
git push origin develop

# 7. Delete feature branch
git branch -d feature/user-authentication
git push origin --delete feature/user-authentication
```

### Hotfix Flow
```bash
# 1. Create hotfix from main
git checkout main
git pull origin main
git checkout -b hotfix/security-patch

# 2. Fix the issue
git add .
git commit -m "fix: patch security vulnerability"

# 3. Merge to main
git checkout main
git merge --no-ff hotfix/security-patch
git tag -a v1.2.1 -m "Security patch"
git push origin main --tags

# 4. Merge to develop
git checkout develop
git merge --no-ff hotfix/security-patch
git push origin develop

# 5. Delete hotfix branch
git branch -d hotfix/security-patch
```

---

## 📝 Commit Message Format

### Conventional Commits
```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
| Type | Description | Example |
|------|-------------|---------|
| `feat` | New feature | `feat: add user login` |
| `fix` | Bug fix | `fix: resolve cart calculation error` |
| `docs` | Documentation | `docs: update API documentation` |
| `style` | Code style (formatting) | `style: format code with prettier` |
| `refactor` | Code refactoring | `refactor: simplify auth logic` |
| `test` | Add/update tests | `test: add user service tests` |
| `chore` | Maintenance | `chore: update dependencies` |
| `perf` | Performance improvement | `perf: optimize database queries` |

### Examples
```bash
# Good commits
git commit -m "feat(auth): implement JWT authentication"
git commit -m "fix(cart): correct total price calculation"
git commit -m "docs: add API endpoint documentation"

# With body
git commit -m "feat(payment): integrate Stripe payment

- Add Stripe SDK
- Create payment service
- Add webhook handler

Closes #123"

# Bad commits
git commit -m "update"
git commit -m "fix bug"
git commit -m "changes"
```

---

## 🔐 Pre-commit Hooks

### Husky + lint-staged Setup
```json
// package.json
{
  "husky": {
    "hooks": {
      "pre-commit": "lint-staged",
      "commit-msg": "commitlint -E HUSKY_GIT_PARAMS"
    }
  },
  "lint-staged": {
    "*.{js,ts,tsx}": [
      "eslint --fix",
      "prettier --write"
    ],
    "*.{json,md}": [
      "prettier --write"
    ]
  }
}
```

### Commitlint Config
```js
// commitlint.config.js
module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [
      2,
      'always',
      ['feat', 'fix', 'docs', 'style', 'refactor', 'test', 'chore', 'perf']
    ],
    'subject-case': [2, 'never', ['upper-case']],
    'subject-max-length': [2, 'always', 72]
  }
}
```

---

## 🎨 Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Changes Made
- Change 1
- Change 2
- Change 3

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Screenshots (if applicable)
[Add screenshots here]

## Checklist
- [ ] Code follows project conventions
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] No console.logs or debug code
- [ ] Tests added/updated

## Related Issues
Closes #123
```

---

## 🔍 Code Review Guidelines

### Reviewer Checklist
- [ ] Code logic is correct
- [ ] Edge cases handled
- [ ] Tests are adequate
- [ ] No security vulnerabilities
- [ ] Performance considerations
- [ ] Code is readable
- [ ] Follows project conventions
- [ ] Documentation updated

### Review Comments Format
```markdown
# Blocking issues (must fix)
🚨 **BLOCKER**: SQL injection vulnerability in user query

# Suggestions (nice to have)
💡 **SUGGESTION**: Consider using a constant for this magic number

# Questions
❓ **QUESTION**: Why did you choose this approach over X?

# Praise
✅ **NICE**: Great test coverage!
```

---

## 🎯 Git Best Practices

### DO ✅
```bash
# Commit often, push regularly
git commit -m "feat: add user validation"

# Use meaningful branch names
git checkout -b feature/user-authentication

# Keep commits atomic
# One logical change per commit

# Write descriptive commit messages
git commit -m "fix(auth): resolve token expiration issue

The JWT tokens were expiring too quickly due to incorrect
timestamp calculation. Updated to use UTC time.

Fixes #456"

# Rebase to keep history clean
git rebase origin/develop

# Use tags for releases
git tag -a v1.0.0 -m "Release version 1.0.0"
```

### DON'T ❌
```bash
# Don't commit directly to main
git checkout main
git commit -m "quick fix"  # ❌

# Don't use vague commit messages
git commit -m "update"  # ❌
git commit -m "fix"  # ❌

# Don't commit large binary files
git add large-file.zip  # ❌

# Don't force push to shared branches
git push --force origin develop  # ❌

# Don't commit secrets
git add .env  # ❌
```

---

## 🔧 Useful Git Commands

### Undo Changes
```bash
# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1

# Undo changes in working directory
git checkout -- file.txt

# Unstage file
git reset HEAD file.txt
```

### Stash Changes
```bash
# Stash current changes
git stash

# List stashes
git stash list

# Apply latest stash
git stash pop

# Apply specific stash
git stash apply stash@{0}
```

### Clean History
```bash
# Interactive rebase (last 3 commits)
git rebase -i HEAD~3

# Squash commits
# In interactive rebase, change 'pick' to 'squash'

# Amend last commit
git commit --amend -m "Updated commit message"
```

---

## 🔍 Pattern Sources

**Cursor Agent**:
- Semantic understanding of code changes
- Intelligent commit suggestions

**VSCode Agent**:
- Git integration patterns
- Conflict resolution

**Windsurf**:
- Branch strategy
- Code review protocols

**Claude Code**:
- Commit message conventions
- Pre-commit hook setup

---

## 📋 Implementation Checklist

- [ ] Define branch naming conventions
- [ ] Setup Husky + lint-staged
- [ ] Configure commitlint
- [ ] Create PR template
- [ ] Document code review guidelines
- [ ] Setup branch protection rules
- [ ] Configure CI/CD for PR checks
- [ ] Train team on Git workflow

---

**Related Templates**:
- [Coding Standards](./coding-standards.md)
- [Project Structure](./project-structure.md)
