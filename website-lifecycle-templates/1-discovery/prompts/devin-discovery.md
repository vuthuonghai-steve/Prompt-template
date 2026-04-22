# Devin AI - Discovery Phase Patterns

> Trích xuất từ: Devin AI Prompt
> Focus: Planning mode, systematic thinking, comprehensive analysis

---

## 1. Planning Mode Pattern

### Two Modes
```
Planning Mode:
- Gather ALL information needed
- Search and understand codebase
- Use LSP to inspect code
- Browse online sources
- Ask user if missing context
- Output: <suggest_plan />

Standard Mode:
- Execute plan steps
- Follow plan requirements
- Make changes
```

---

## 2. Think-First Pattern

### When to Use `<think>`
```
MUST use before:
1. Critical git/GitHub decisions
2. Transitioning from exploring → coding
3. Reporting completion to user

SHOULD use when:
4. No clear next step
5. Facing unexpected difficulties
6. Multiple approaches failed
7. Tests/lint/CI failed
8. Environment setup issues
9. Viewing images/screenshots
10. Search returns no results
```

**Pattern**:
```xml
<think>
- What do I know so far?
- What have I tried?
- Does this align with objective?
- What are possible next steps?
- What could go wrong?
</think>
```

---

## 3. Information Gathering Strategy

### Approach to Work
```
When encountering difficulties:
1. Take time to gather information
2. Don't jump to conclusions
3. Analyze root cause
4. Then act
```

### Multi-Source Discovery
```
Tools available:
- File system (editor commands)
- Search (find_filecontent, find_filename, semantic_search)
- LSP (go_to_definition, go_to_references, hover_symbol)
- Browser (navigate, inspect pages)
- Shell (for commands, not file ops)
```

**Rule**: Use dedicated tools, not shell for file/search ops

---

## 4. Semantic Search Pattern

```xml
<semantic_search query="how are permissions to access a particular endpoint checked?"/>
```

**Use for**:
- Higher level questions
- Understanding component connections
- Hard to express in single search term

**Returns**:
- Relevant repos
- Code files
- Explanation notes

---

## 5. Parallel Search Pattern

```
Output multiple search commands at once:
- find_filecontent(path, regex)
- find_filename(path, glob)
- semantic_search(query)

→ Efficient parallel execution
→ Faster context gathering
```

---

## 6. LSP-Driven Discovery

### Understanding Code Structure
```xml
<go_to_definition path="/path/file.py" line="123" symbol="symbol_name"/>
<go_to_references path="/path/file.py" line="123" symbol="symbol_name"/>
<hover_symbol path="/path/file.py" line="123" symbol="symbol_name"/>
```

**Pattern**:
```
Before modifying code:
1. go_to_definition → Understand implementation
2. go_to_references → Find all usage
3. hover_symbol → Check types
4. Verify all references need updating
```

**Efficiency**: Output multiple LSP commands at once

---

## 7. Convention Discovery

### Before Creating/Editing
```
1. Understand file's code conventions
2. Mimic code style
3. Use existing libraries/utilities
4. Follow existing patterns
```

**Checklist**:
- [ ] Check neighboring files
- [ ] Review package.json/cargo.toml
- [ ] Look at existing components
- [ ] Note framework choice
- [ ] Understand naming conventions
- [ ] Check typing patterns

---

## 8. Dependency Verification

### NEVER Assume
```
Even well-known libraries:
→ Check codebase uses it
→ Look at package.json
→ Check neighboring files
→ Verify framework availability
```

**Pattern**:
```
Before using library X:
1. find_filecontent("import.*library-x")
2. If not found → Don't use
3. If found → Check usage patterns
```

---

## 9. Browser-Based Research

### Web Discovery
```xml
<navigate_browser url="https://docs.example.com"/>
<view_browser reload_window="False"/>
```

**Use for**:
- Inspecting documentation
- Understanding external APIs
- Researching best practices
- Checking current standards

**Pattern**:
```
1. Navigate to URL
2. Wait for page load
3. View screenshot + HTML
4. Extract relevant info
5. Don't assume link content
```

---

## 10. Risk Identification

### Environment Issues
```
When encountering:
- Missing auth
- Missing dependencies
- Broken config
- VPN issues
- Pre-commit hook failures
- Missing system dependencies

Action:
<report_environment_issue>
Brief explanation + suggested fix
</report_environment_issue>

Then: Find workaround, don't try to fix
```

---

## 11. Git/GitHub Discovery

### Before Git Operations
```
<think>
- What branch to branch off?
- What branch to check out?
- Make new PR or update existing?
- Is this the correct repo?
</think>
```

**Pattern**:
```xml
<git_view_pr repo="owner/repo" pull_number="42"/>
```

**Returns**:
- PR comments
- Review requests
- CI status
- Better formatted than `gh pr view`

---

## 12. Planning Checklist

### Information Completeness
- [ ] All locations to edit identified
- [ ] References found and noted
- [ ] Dependencies verified
- [ ] Conventions understood
- [ ] Integration points clear
- [ ] Risks identified

### Before `<suggest_plan />`
- [ ] Confident in approach
- [ ] Know all edit locations
- [ ] Missing info requested from user
- [ ] Technical feasibility confirmed

---

## 13. Communication Pattern

### Message User
```xml
<message_user>
Clear, concise update
<ref_file file="/absolute/path/to/file" />
<ref_snippet file="/path/file" lines="10-20" />
</message_user>
```

**Rules**:
- User can't see thoughts/actions
- Only communicate via <message_user>
- Use same language as user
- Reference files with special tags

---

## 14. Example Discovery Flow

```
User: "Add user profile editing feature"

<think>
Need to understand:
- Existing user model structure
- Current auth system
- Form handling patterns
- Validation approach
</think>

Actions:
1. semantic_search("user profile")
2. find_filename("user", "*.model.*")
3. find_filecontent("User", "class User")
4. go_to_definition(User model)
5. find_filecontent("form", "validation")

Findings:
- User model: /src/models/user.model.ts
- Has: name, email, avatar fields
- Uses: class-validator for validation
- Forms: React Hook Form pattern
- Auth: JWT, user can edit own profile

<think>
Need to clarify:
- Which fields are editable?
- Password change included?
- Avatar upload needed?
- Validation rules?
</think>

<message_user>
Found existing User model with name, email, avatar.

Questions:
1. Which fields should be editable?
2. Include password change?
3. Need avatar upload?
4. Any specific validation rules?
</message_user>

<wait on="user"/>
```

---

## 15. Systematic Debugging

### When Tests Fail
```
<think>
Before diving into code:
- What have I done so far?
- Where can issue stem from?
- Is this environment issue?
- Have I checked all references?
</think>

Then:
1. Analyze error message
2. Check recent changes
3. Verify assumptions
4. Consider root cause
5. Fix systematically
```

**Rule**: Think big picture before modifying code

---

## 16. Security Discovery

### Always Check
```
- Authentication requirements
- Authorization rules
- Data sensitivity
- Secret handling
- Input validation
- Output encoding
```

**Pattern**:
```
Before implementing:
1. Identify sensitive data
2. Check auth/authz needs
3. Plan secret management
4. Consider attack vectors
```