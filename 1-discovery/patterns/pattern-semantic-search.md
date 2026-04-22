# Pattern: Semantic Search

## Problem
Cần tìm code theo ý nghĩa (meaning), không phải exact text. Ví dụ: "Tìm nơi xử lý authentication" thay vì grep "auth".

## Solution
Sử dụng semantic search để tìm code dựa trên natural language query.

**Core principles:**
- Query phải là câu hỏi hoàn chỉnh: "How does X work?", "Where is Y handled?"
- Bắt đầu broad, sau đó narrow down
- Break large questions thành smaller queries

## Example

### ❌ Bad Query
```
Query: "AuthService"
Reason: Too vague, should use grep for exact text
```

### ✅ Good Query
```
Query: "Where do we encrypt user passwords before saving?"
Reason: Complete question with context about when it happens
```

### Search Strategy
```
Step 1: Broad search
Query: "How does user authentication work?"
Target: [] (search everywhere)

Step 2: Narrow down (if results point to backend/auth/)
Query: "Where are user roles checked?"
Target: ["backend/auth/"]
```

## When to Use
- Exploring unfamiliar codebases
- Ask "how/where/what" questions
- Find code by meaning, not exact text

## When NOT to Use
- Exact text matches → use grep
- Reading known files → use read_file
- Simple symbol lookups → use grep
- Find file by name → use file_search

## Anti-patterns
- ❌ Single word searches: "MyInterface"
- ❌ Multiple queries in one: "What is AuthService? How does AuthService work?"
- ❌ Using globs in target: ["src/**/utils/**"]

## Source
- Cursor Agent Prompt 2.0
- Windsurf Cascade
- VSCode Agent (GitHub Copilot)
