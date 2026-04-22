# Pattern: File Edit Validation

## Nguồn
- Claude Code
- Cursor Agent
- Windsurf Cascade

## Mô tả
Validate file edits trước khi apply: syntax check, type check, import resolution. Đảm bảo edits không break code.

## Khi nào dùng
- Development: mọi file edit
- Code generation: AI-generated code
- Refactoring: large-scale changes
- Code review: automated validation

## Cách áp dụng

### 1. Pre-Edit Validation
```typescript
interface EditValidation {
  syntaxValid: boolean
  importsResolved: boolean
  typesValid: boolean
  noBreakingChanges: boolean
  errors: string[]
}

async function validateEdit(
  filePath: string,
  newContent: string
): Promise<EditValidation> {
  const errors: string[] = []
  
  // 1. Syntax check
  const syntaxValid = await checkSyntax(newContent)
  if (!syntaxValid) {
    errors.push('Syntax error detected')
  }
  
  // 2. Import resolution
  const importsResolved = await checkImports(filePath, newContent)
  if (!importsResolved) {
    errors.push('Unresolved imports')
  }
  
  // 3. Type check
  const typesValid = await checkTypes(filePath, newContent)
  if (!typesValid) {
    errors.push('Type errors detected')
  }
  
  // 4. Breaking changes
  const noBreakingChanges = await checkBreakingChanges(filePath, newContent)
  if (!noBreakingChanges) {
    errors.push('Breaking changes detected')
  }
  
  return {
    syntaxValid,
    importsResolved,
    typesValid,
    noBreakingChanges,
    errors,
  }
}
```

### 2. Safe Edit Pattern
```typescript
async function safeEdit(filePath: string, newContent: string) {
  // 1. Backup original
  const originalContent = await readFile(filePath)
  
  try {
    // 2. Validate edit
    const validation = await validateEdit(filePath, newContent)
    
    if (validation.errors.length > 0) {
      throw new Error(
        `Validation failed:\n${validation.errors.join('\n')}`
      )
    }
    
    // 3. Apply edit
    await writeFile(filePath, newContent)
    
    // 4. Run tests
    const testsPass = await runTests(filePath)
    
    if (!testsPass) {
      throw new Error('Tests failed after edit')
    }
    
    console.log('✅ Edit applied successfully')
    
  } catch (error) {
    // 5. Rollback on error
    await writeFile(filePath, originalContent)
    console.error('❌ Edit failed, rolled back:', error)
    throw error
  }
}
```

### 3. Incremental Validation
```typescript
// Validate as you type
function useIncrementalValidation(filePath: string) {
  const [content, setContent] = useState('')
  const [errors, setErrors] = useState<string[]>([])
  
  const debouncedValidate = useMemo(
    () =>
      debounce(async (newContent: string) => {
        const validation = await validateEdit(filePath, newContent)
        setErrors(validation.errors)
      }, 500),
    [filePath]
  )
  
  const handleChange = (newContent: string) => {
    setContent(newContent)
    debouncedValidate(newContent)
  }
  
  return { content, errors, handleChange }
}
```

## Ví dụ thực tế

### TypeScript File Edit

```typescript
// Validate TypeScript edits
import * as ts from 'typescript'

async function validateTypeScriptEdit(
  filePath: string,
  newContent: string
): Promise<EditValidation> {
  const errors: string[] = []
  
  // 1. Parse syntax
  const sourceFile = ts.createSourceFile(
    filePath,
    newContent,
    ts.ScriptTarget.Latest,
    true
  )
  
  const syntaxErrors = sourceFile.parseDiagnostics
  if (syntaxErrors.length > 0) {
    errors.push(
      ...syntaxErrors.map((d) => 
        ts.flattenDiagnosticMessageText(d.messageText, '\n')
      )
    )
  }
  
  // 2. Type check
  const program = ts.createProgram([filePath], {
    noEmit: true,
    skipLibCheck: true,
  })
  
  const typeErrors = ts.getPreEmitDiagnostics(program)
  if (typeErrors.length > 0) {
    errors.push(
      ...typeErrors.map((d) =>
        ts.flattenDiagnosticMessageText(d.messageText, '\n')
      )
    )
  }
  
  // 3. Check imports
  const imports = extractImports(sourceFile)
  const unresolvedImports = await checkImportResolution(imports)
  
  if (unresolvedImports.length > 0) {
    errors.push(
      ...unresolvedImports.map((imp) => `Unresolved import: ${imp}`)
    )
  }
  
  return {
    syntaxValid: syntaxErrors.length === 0,
    importsResolved: unresolvedImports.length === 0,
    typesValid: typeErrors.length === 0,
    noBreakingChanges: true, // TODO: implement
    errors,
  }
}
```

### React Component Edit

```typescript
// Validate React component edits
async function validateComponentEdit(
  filePath: string,
  newContent: string
): Promise<EditValidation> {
  const errors: string[] = []
  
  // 1. TypeScript validation
  const tsValidation = await validateTypeScriptEdit(filePath, newContent)
  errors.push(...tsValidation.errors)
  
  // 2. React-specific checks
  const hasDefaultExport = /export default/.test(newContent)
  if (!hasDefaultExport) {
    errors.push('Component must have default export')
  }
  
  // 3. Props interface check
  const hasPropsInterface = /interface \w+Props/.test(newContent)
  if (!hasPropsInterface) {
    errors.push('Component should define Props interface')
  }
  
  // 4. Hook rules
  const hookViolations = checkHookRules(newContent)
  if (hookViolations.length > 0) {
    errors.push(...hookViolations)
  }
  
  return {
    syntaxValid: tsValidation.syntaxValid,
    importsResolved: tsValidation.importsResolved,
    typesValid: tsValidation.typesValid && errors.length === 0,
    noBreakingChanges: true,
    errors,
  }
}

function checkHookRules(content: string): string[] {
  const errors: string[] = []
  
  // Check: Hooks must be called at top level
  const conditionalHooks = content.match(/if.*use[A-Z]\w+/g)
  if (conditionalHooks) {
    errors.push('Hooks cannot be called conditionally')
  }
  
  // Check: Hooks must start with "use"
  const invalidHookNames = content.match(/const \w+Hook = /g)
  if (invalidHookNames) {
    errors.push('Hook names must start with "use"')
  }
  
  return errors
}
```

### Automated Fix Suggestions

```typescript
// Suggest fixes for common errors
interface FixSuggestion {
  error: string
  fix: string
  autoFixable: boolean
}

function suggestFixes(
  validation: EditValidation
): FixSuggestion[] {
  const suggestions: FixSuggestion[] = []
  
  validation.errors.forEach((error) => {
    // Missing import
    if (error.includes('Cannot find name')) {
      const match = error.match(/Cannot find name '(\w+)'/)
      if (match) {
        suggestions.push({
          error,
          fix: `Add import: import { ${match[1]} } from '...'`,
          autoFixable: false,
        })
      }
    }
    
    // Missing semicolon
    if (error.includes('expected ;')) {
      suggestions.push({
        error,
        fix: 'Add semicolon at end of statement',
        autoFixable: true,
      })
    }
    
    // Unused variable
    if (error.includes('is declared but never used')) {
      const match = error.match(/'(\w+)' is declared/)
      if (match) {
        suggestions.push({
          error,
          fix: `Remove unused variable: ${match[1]}`,
          autoFixable: true,
        })
      }
    }
  })
  
  return suggestions
}
```

### Pre-commit Hook

```typescript
// .husky/pre-commit
import { execSync } from 'child_process'
import { readFileSync } from 'fs'

// Get staged files
const stagedFiles = execSync('git diff --cached --name-only --diff-filter=ACM')
  .toString()
  .trim()
  .split('\n')
  .filter((file) => file.endsWith('.ts') || file.endsWith('.tsx'))

let hasErrors = false

for (const file of stagedFiles) {
  const content = readFileSync(file, 'utf-8')
  
  const validation = await validateEdit(file, content)
  
  if (validation.errors.length > 0) {
    console.error(`\n❌ ${file}:`)
    validation.errors.forEach((error) => {
      console.error(`  - ${error}`)
    })
    
    hasErrors = true
  }
}

if (hasErrors) {
  console.error('\n❌ Commit blocked due to validation errors')
  process.exit(1)
}

console.log('✅ All files validated successfully')
```

## Validation Checklist

### Syntax
- [ ] No syntax errors
- [ ] Proper indentation
- [ ] Matching brackets/parens
- [ ] Valid JSX syntax

### Imports
- [ ] All imports resolved
- [ ] No circular dependencies
- [ ] Path aliases work
- [ ] No unused imports

### Types
- [ ] No type errors
- [ ] Props interfaces defined
- [ ] Return types specified
- [ ] No `any` types

### React-specific
- [ ] Hook rules followed
- [ ] Component has default export
- [ ] Props destructured
- [ ] Keys on list items

## Trade-offs

| Ưu điểm | Nhược điểm |
|---------|------------|
| Catch errors early | Slower edits |
| Prevent broken code | Setup overhead |
| Better code quality | False positives possible |

## Best Practices
1. **Validate incrementally**: As you type, not just on save
2. **Auto-fix when possible**: Semicolons, imports, formatting
3. **Show clear errors**: Line numbers, suggestions
4. **Rollback on failure**: Don't leave broken code
5. **Run tests**: Validation + tests = confidence
6. **Cache results**: Don't re-validate unchanged code

## Anti-patterns
- ❌ Skip validation "just this once"
- ❌ Ignore validation errors
- ❌ No rollback mechanism
- ❌ Validate only on commit (too late)
- ❌ No auto-fix suggestions

## Related Patterns
- [Immediately Runnable Code](./pattern-immediately-runnable-code.md)
- [Non-Blocking Execution](./pattern-non-blocking-execution.md)
