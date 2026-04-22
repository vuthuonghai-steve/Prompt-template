# Cursor Chat - Discovery Phase Patterns

> Trích xuất từ: Cursor Chat Prompt
> Focus: Semantic search, context understanding, rapid exploration

---

## 1. Codebase Search Pattern

### Semantic Search
```
Tool: codebase_search
Purpose: Find relevant code semantically
When: Need to understand existing patterns
```

**Best Practices**:
- Reuse user's exact query wording
- Keep question format from user
- Specify target_directories if known
- Explain why searching

**Example**:
```json
{
  "query": "how are permissions checked for endpoints?",
  "target_directories": ["src/auth", "src/middleware"],
  "explanation": "Finding existing permission patterns"
}
```

---

## 2. File Reading Strategy

### Progressive Reading
```
1. Read file outline first
2. Assess if sufficient
3. Note lines not shown
4. Read more if needed (max 250 lines/call)
5. Read entire file only if edited/attached
```

**Pattern**:
```
read_file(target_file, start_line, end_line)
→ Assess completeness
→ Read more if insufficient
→ Avoid reading entire large files
```

---

## 3. Discovery Tools Priority

| Tool | Use Case | When |
|------|----------|------|
| `codebase_search` | Semantic understanding | High-level questions |
| `grep_search` | Exact pattern match | Know specific symbol/function |
| `file_search` | Find file by path | Know partial filename |
| `list_dir` | Explore structure | Initial discovery |

**Rule**: Semantic search for concepts, grep for exact strings

---

## 4. LSP-Driven Discovery

### Understanding Code
```
go_to_definition → Find implementation
go_to_references → Find usage
hover_symbol → Get type info
```

**Pattern**:
```
When analyzing code:
1. Use LSP to understand types
2. Find all references before changing
3. Check input/output types
4. Verify assumptions
```

**Parallel Execution**:
```
Output multiple LSP commands at once
→ Gather context faster
→ Reduce round trips
```

---

## 5. Context Gathering Workflow

### Step 1: Explore Structure
```bash
list_dir("src/")
→ Understand project layout
→ Identify relevant modules
```

### Step 2: Semantic Search
```
codebase_search("user authentication flow")
→ Find related code
→ Understand patterns
```

### Step 3: Deep Dive
```
read_file(relevant_files)
→ Read implementations
→ Check conventions
```

### Step 4: Verify Understanding
```
go_to_definition / go_to_references
→ Validate assumptions
→ Find all dependencies
```

---

## 6. Requirement Extraction Pattern

### From User Query
```
User: "Add user profile editing"

Extract:
1. Feature: Profile editing
2. Actor: User
3. Scope: What fields?
4. Constraints: Validation rules?
5. Integration: Existing user model?
```

### Questions to Ask
- What fields are editable?
- Who can edit? (Self only? Admin?)
- Validation requirements?
- Existing user model structure?

---

## 7. Convention Discovery

**From Cursor Prompt**:
```
Before creating/editing:
1. Look at existing components
2. Check framework choice
3. Note naming conventions
4. Understand typing patterns
5. Follow existing patterns
```

**Pattern**:
```
read_file("similar_component.tsx")
→ Extract conventions:
  - File structure
  - Import order
  - Naming style
  - Type definitions
→ Apply to new code
```

---

## 8. Dependency Analysis

### Check Before Using
```
NEVER assume library exists
→ Check package.json
→ Look at neighboring files
→ Verify framework usage
```

**Pattern**:
```
grep_search("import.*library-name")
→ If found: Use it
→ If not found: Ask or suggest alternative
```

---

## 9. Web Research Pattern

**From Cursor**:
```
web_search when:
- Need up-to-date information
- Verify current facts
- Check technology updates
- Research best practices
```

**Query Format**:
- Specific keywords
- Include version numbers
- Add dates if relevant

---

## 10. Discovery Checklist

### Before Proposing Solution
- [ ] Searched codebase for existing patterns
- [ ] Read relevant files completely
- [ ] Checked dependencies availability
- [ ] Understood code conventions
- [ ] Verified technical feasibility
- [ ] Identified integration points

### Information Gathered
- [ ] Existing code structure
- [ ] Framework/library choices
- [ ] Naming conventions
- [ ] Type patterns
- [ ] Security considerations

---

## 11. Parallel Discovery

**Efficiency Pattern**:
```
Single message with multiple tool calls:
- codebase_search("auth")
- codebase_search("user model")
- list_dir("src/auth")
- grep_search("JWT")

→ Gather all context in parallel
→ Reduce latency
```

---

## 12. Example Discovery Session

```
User: "Add password reset feature"

AI Actions:
1. codebase_search("password", "authentication", "email")
2. list_dir("src/auth")
3. read_file("src/auth/user.model.ts")
4. grep_search("email.*service")
5. go_to_definition(User, "email")

Findings:
- User model has email field
- EmailService exists
- No password reset yet
- Uses bcrypt for hashing
- JWT for tokens

Requirements Clarification:
- Reset via email link?
- Token expiration time?
- Rate limiting needed?
- Password strength rules?
```

---

## 13. Output Format

**Concise Responses**:
```
User: "What auth method is used?"
AI: "JWT with refresh tokens"

NOT: "Based on my analysis of the codebase, 
      I found that the authentication method 
      currently implemented is JWT..."
```

**Rule**: Answer directly, no preamble