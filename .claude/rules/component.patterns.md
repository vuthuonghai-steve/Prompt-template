---
trigger: always_on
paths:
  - "src/components/**/*.tsx"
  - "src/screens/**/*.tsx"
---

# Component Patterns

> **Last Updated**: 2026-03-05

---

## Functional Components

```typescript
// ✅ CORRECT
export const ProductList: React.FC<ProductListProps> = ({ products, onSelect }) => {
  const [selectedId, setSelectedId] = useState<string | null>(null)

  const handleSelect = useCallback((id: string) => {
    setSelectedId(id)
    onSelect?.(id)
  }, [onSelect])

  return (
    <div>
      {products.map(product => (
        <ProductCard
          key={product.id}
          product={product}
          isSelected={selectedId === product.id}
          onSelect={handleSelect}
        />
      ))}
    </div>
  )
}

// ❌ WRONG - Class component
class ProductList extends React.Component { ... }
```

---

## Props Interface

```typescript
// ✅ CORRECT
interface ProductCardProps {
  product: Product
  isSelected?: boolean
  onSelect?: (id: string) => void
  className?: string
}

export const ProductCard: React.FC<ProductCardProps> = ({ ... }) => { ... }

// ❌ WRONG - Inline props
export const ProductCard = ({ product, isSelected, onSelect }) => { ... }
```

---

## Custom Hooks

```typescript
// ✅ CORRECT - Logic trong hook
export function useProductList(productType: ProductType) {
  const [products, setProducts] = useState<Product[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const fetchProducts = useCallback(async () => {
    setLoading(true)
    try {
      const data = await fetchProductsService(productType)
      setProducts(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown')
    } finally {
      setLoading(false)
    }
  }, [productType])

  useEffect(() => { fetchProducts() }, [fetchProducts])

  return { products, loading, error, refetch: fetchProducts }
}
```

---

## Component Composition

```typescript
// ✅ CORRECT
export const ProductsScreen: React.FC = () => {
  const { products, loading, filters, updateFilter } = useProductListByType('bouquet')

  return (
    <div className="space-y-6">
      <ProductStats products={products} />
      <ProductFilters filters={filters} onFilterChange={updateFilter} />
      <ProductsTable products={products} loading={loading} />
    </div>
  )
}

// ❌ WRONG - Everything in one component
export const ProductsScreen = () => { /* 500+ lines */ }
```

---

## Common Pitfalls

| ❌ Wrong | ✅ Correct |
|----------|-----------|
| Logic trong component | Extract to hooks |
| Khong co loading/error state | Always handle states |
| Callback khong memoized | Use useCallback |
| Uncontrolled component | Consistent controlled |

---

**Related**:
- [component.state.md](./component.state.md)
- [api.patterns.md](./api.patterns.md)
