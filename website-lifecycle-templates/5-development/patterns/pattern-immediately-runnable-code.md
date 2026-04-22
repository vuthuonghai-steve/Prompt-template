# Pattern: Immediately Runnable Code

## Nguồn
- Claude Code
- Cursor Agent
- Windsurf Cascade

## Mô tả
Code phải chạy được ngay lập tức sau khi viết, không cần manual fixes. Syntax correct, imports resolved, types valid.

## Khi nào dùng
- Development: mọi lúc viết code
- Code review: verify code chạy được
- CI/CD: automated testing
- Pair programming: maintain flow

## Cách áp dụng

### 1. Pre-flight Checks
```typescript
// Checklist trước khi commit code
interface CodeQuality {
  syntaxValid: boolean
  importsResolved: boolean
  typesValid: boolean
  testsPass: boolean
  lintPass: boolean
}

async function validateCode(file: string): Promise<CodeQuality> {
  return {
    syntaxValid: await checkSyntax(file),
    importsResolved: await checkImports(file),
    typesValid: await checkTypes(file),
    testsPass: await runTests(file),
    lintPass: await runLint(file),
  }
}
```

### 2. Import Resolution
```typescript
// ❌ Broken imports
import { Button } from './Button'  // File không tồn tại
import { formatPrice } from '@/utils'  // Path alias chưa config

// ✅ Valid imports
import { Button } from '@/components/ui/button'
import { formatPrice } from '@/lib/utils/format-price'
```

### 3. Type Safety
```typescript
// ❌ Type errors
function addToCart(productId: number) {
  const product = getProduct(productId)  // getProduct expects string
  cart.add(product)  // cart.add expects Product, got Product | undefined
}

// ✅ Type safe
function addToCart(productId: string) {
  const product = getProduct(productId)
  
  if (!product) {
    throw new Error(`Product ${productId} not found`)
  }
  
  cart.add(product)
}
```

## Ví dụ thực tế

### E-commerce Product Component

```tsx
// ❌ Không chạy được
import { Button } from './Button'  // Wrong path
import { formatPrice } from 'utils'  // Missing @/

function ProductCard({ product }) {  // Missing types
  const price = formatPrice(product.price)  // formatPrice undefined
  
  return (
    <div>
      <h3>{product.name}</h3>
      <p>{price}</p>
      <Button onClick={handleAddToCart}>Add to Cart</Button>
    </div>
  )
}

// ✅ Immediately runnable
import { Button } from '@/components/ui/button'
import { formatPrice } from '@/lib/utils/format-price'
import type { Product } from '@/types/product'

interface ProductCardProps {
  product: Product
  onAddToCart: (productId: string) => void
}

export function ProductCard({ product, onAddToCart }: ProductCardProps) {
  const price = formatPrice(product.price)
  
  const handleAddToCart = () => {
    onAddToCart(product.id)
  }
  
  return (
    <div className="product-card">
      <h3>{product.name}</h3>
      <p className="price">{price}</p>
      <Button onClick={handleAddToCart}>Add to Cart</Button>
    </div>
  )
}
```

### API Service

```typescript
// ❌ Không chạy được
import axios from 'axios'  // Not installed
import { API_URL } from './config'  // File không tồn tại

class ProductService {
  async getProducts() {
    const response = await axios.get(`${API_URL}/products`)
    return response.data
  }
}

// ✅ Immediately runnable
import { apiClient } from '@/lib/api-client'
import { API_ENDPOINTS } from '@/config/endpoints'
import type { Product } from '@/types/product'

export class ProductService {
  async getProducts(): Promise<Product[]> {
    const response = await apiClient.get<Product[]>(
      API_ENDPOINTS.PRODUCTS.LIST
    )
    return response.data
  }
  
  async getProduct(id: string): Promise<Product> {
    const response = await apiClient.get<Product>(
      `${API_ENDPOINTS.PRODUCTS.DETAIL}/${id}`
    )
    return response.data
  }
}

export const productService = new ProductService()
```

### Validation Before Commit

```typescript
// pre-commit hook
import { execSync } from 'child_process'

interface ValidationResult {
  passed: boolean
  errors: string[]
}

function validateBeforeCommit(): ValidationResult {
  const errors: string[] = []
  
  // 1. Check syntax
  try {
    execSync('tsc --noEmit', { stdio: 'pipe' })
  } catch (error) {
    errors.push('TypeScript compilation failed')
  }
  
  // 2. Check imports
  try {
    execSync('eslint --rule "import/no-unresolved: error"', { 
      stdio: 'pipe' 
    })
  } catch (error) {
    errors.push('Unresolved imports detected')
  }
  
  // 3. Run tests
  try {
    execSync('npm test', { stdio: 'pipe' })
  } catch (error) {
    errors.push('Tests failed')
  }
  
  // 4. Lint
  try {
    execSync('npm run lint', { stdio: 'pipe' })
  } catch (error) {
    errors.push('Linting failed')
  }
  
  return {
    passed: errors.length === 0,
    errors,
  }
}

// Run validation
const result = validateBeforeCommit()

if (!result.passed) {
  console.error('❌ Commit blocked:')
  result.errors.forEach((error) => console.error(`  - ${error}`))
  process.exit(1)
}

console.log('✅ All checks passed')
```

### IDE Integration

```json
// .vscode/settings.json
{
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true,
    "source.organizeImports": true
  },
  "typescript.tsdk": "node_modules/typescript/lib",
  "typescript.enablePromptUseWorkspaceTsdk": true,
  
  // Auto-fix imports
  "javascript.preferences.importModuleSpecifier": "non-relative",
  "typescript.preferences.importModuleSpecifier": "non-relative",
  
  // Show errors immediately
  "typescript.validate.enable": true,
  "javascript.validate.enable": true
}
```

## Immediately Runnable Checklist

### Before Writing
- [ ] Understand existing patterns
- [ ] Check import paths
- [ ] Verify dependencies installed
- [ ] Know type definitions

### While Writing
- [ ] IDE shows no errors
- [ ] Imports auto-complete
- [ ] Types inferred correctly
- [ ] Format on save enabled

### Before Committing
- [ ] `tsc --noEmit` passes
- [ ] `npm run lint` passes
- [ ] `npm test` passes
- [ ] Manual test in browser

## Trade-offs

| Ưu điểm | Nhược điểm |
|---------|------------|
| Faster development | Upfront tooling setup |
| Fewer bugs | Stricter discipline |
| Better DX | Learning curve |

## Best Practices
1. **Use TypeScript**: Catch errors at compile time
2. **Configure path aliases**: Clean imports
3. **Enable auto-imports**: IDE does the work
4. **Run pre-commit hooks**: Catch issues early
5. **Test immediately**: Don't wait for CI
6. **Use linter**: Enforce consistency

## Anti-patterns
- ❌ Commit code với TypeScript errors
- ❌ Hardcode paths thay vì path aliases
- ❌ Skip testing locally
- ❌ Ignore linter warnings
- ❌ Commit broken imports

## Related Patterns
- [Non-Blocking Execution](./pattern-non-blocking-execution.md)
- [File Edit Validation](./pattern-file-edit-validation.md)
