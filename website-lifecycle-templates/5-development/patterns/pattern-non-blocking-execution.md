# Pattern: Non-Blocking Execution

## Nguồn
- Claude Code
- Cursor Agent
- Windsurf Cascade

## Mô tả
Thực hiện operations mà không block main thread hoặc user workflow. Sử dụng async/await, background tasks, optimistic updates.

## Khi nào dùng
- Development: async operations (API calls, file I/O)
- UI: prevent blocking user interactions
- Background jobs: long-running tasks
- Real-time: concurrent operations

## Cách áp dụng

### 1. Async/Await Pattern
```typescript
// ❌ Blocking
function fetchProducts() {
  const response = fetch('/api/products') // Blocks
  return response.json()
}

// ✅ Non-blocking
async function fetchProducts() {
  const response = await fetch('/api/products')
  return response.json()
}
```

### 2. Optimistic Updates
```typescript
// Update UI immediately, sync in background
async function addToCart(productId: string) {
  // 1. Optimistic update
  const optimisticItem = {
    id: productId,
    quantity: 1,
    status: 'pending',
  }
  updateCartUI(optimisticItem)
  
  try {
    // 2. Background sync
    const result = await api.cart.add(productId)
    
    // 3. Confirm success
    updateCartUI({ ...result, status: 'confirmed' })
  } catch (error) {
    // 4. Rollback on error
    removeFromCartUI(productId)
    showError('Failed to add to cart')
  }
}
```

### 3. Background Tasks
```typescript
// Queue background tasks
interface BackgroundTask {
  id: string
  type: string
  payload: any
  status: 'pending' | 'running' | 'completed' | 'failed'
}

class TaskQueue {
  private queue: BackgroundTask[] = []
  private running = false
  
  async enqueue(task: BackgroundTask) {
    this.queue.push(task)
    if (!this.running) {
      this.process()
    }
  }
  
  private async process() {
    this.running = true
    
    while (this.queue.length > 0) {
      const task = this.queue.shift()!
      task.status = 'running'
      
      try {
        await this.executeTask(task)
        task.status = 'completed'
      } catch (error) {
        task.status = 'failed'
        console.error(`Task ${task.id} failed:`, error)
      }
    }
    
    this.running = false
  }
  
  private async executeTask(task: BackgroundTask) {
    // Execute based on task type
    switch (task.type) {
      case 'sync-cart':
        await syncCart(task.payload)
        break
      case 'send-analytics':
        await sendAnalytics(task.payload)
        break
      default:
        throw new Error(`Unknown task type: ${task.type}`)
    }
  }
}
```

## Ví dụ thực tế

### E-commerce Checkout Flow

```typescript
// Non-blocking checkout
async function processCheckout(order: Order) {
  // 1. Show loading state (non-blocking UI)
  showCheckoutLoading()
  
  try {
    // 2. Parallel operations
    const [
      validatedCart,
      shippingOptions,
      paymentMethods,
    ] = await Promise.all([
      validateCart(order.cart),
      fetchShippingOptions(order.address),
      fetchPaymentMethods(),
    ])
    
    // 3. Update UI immediately
    updateCheckoutUI({
      cart: validatedCart,
      shipping: shippingOptions,
      payment: paymentMethods,
    })
    
    // 4. Background: Pre-calculate totals
    calculateTotals(validatedCart, shippingOptions[0])
      .then(updateTotalsUI)
      .catch(console.error)
    
  } catch (error) {
    showCheckoutError(error)
  } finally {
    hideCheckoutLoading()
  }
}
```

### Search with Debouncing

```typescript
// Non-blocking search
function useProductSearch() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)
  
  // Debounce search
  const debouncedSearch = useMemo(
    () =>
      debounce(async (searchQuery: string) => {
        if (!searchQuery) {
          setResults([])
          return
        }
        
        setLoading(true)
        
        try {
          const data = await api.products.search(searchQuery)
          setResults(data)
        } catch (error) {
          console.error('Search failed:', error)
        } finally {
          setLoading(false)
        }
      }, 300),
    []
  )
  
  useEffect(() => {
    debouncedSearch(query)
  }, [query, debouncedSearch])
  
  return { query, setQuery, results, loading }
}
```

### Image Upload with Progress

```typescript
// Non-blocking upload
async function uploadProductImage(file: File) {
  // 1. Show preview immediately (optimistic)
  const preview = URL.createObjectURL(file)
  showImagePreview(preview)
  
  // 2. Upload in background with progress
  const formData = new FormData()
  formData.append('image', file)
  
  try {
    const response = await fetch('/api/upload', {
      method: 'POST',
      body: formData,
      // Track progress
      onUploadProgress: (progressEvent) => {
        const percentCompleted = Math.round(
          (progressEvent.loaded * 100) / progressEvent.total
        )
        updateUploadProgress(percentCompleted)
      },
    })
    
    const { url } = await response.json()
    
    // 3. Replace preview with uploaded URL
    updateImageUrl(url)
    
  } catch (error) {
    // 4. Rollback on error
    removeImagePreview()
    showError('Upload failed')
  }
}
```

### Background Sync

```typescript
// Sync data in background
class BackgroundSync {
  private syncInterval: NodeJS.Timeout | null = null
  
  start() {
    // Sync every 30 seconds
    this.syncInterval = setInterval(() => {
      this.sync()
    }, 30000)
    
    // Initial sync
    this.sync()
  }
  
  stop() {
    if (this.syncInterval) {
      clearInterval(this.syncInterval)
    }
  }
  
  private async sync() {
    try {
      // Get pending changes
      const pendingChanges = await db.getPendingChanges()
      
      if (pendingChanges.length === 0) return
      
      // Sync in background (don't block UI)
      await Promise.all(
        pendingChanges.map((change) =>
          api.sync(change).catch((error) => {
            console.error('Sync failed:', error)
            // Retry later
          })
        )
      )
      
      // Mark as synced
      await db.markAsSynced(pendingChanges.map((c) => c.id))
      
    } catch (error) {
      console.error('Background sync failed:', error)
    }
  }
}
```

## Non-Blocking Checklist

### UI
- [ ] Loading states for async operations
- [ ] Optimistic updates cho user actions
- [ ] Debounce/throttle frequent operations
- [ ] Cancel pending requests on unmount

### Performance
- [ ] Parallel operations với Promise.all
- [ ] Background tasks không block main thread
- [ ] Web Workers cho heavy computations
- [ ] Lazy load below-the-fold content

### Error Handling
- [ ] Graceful degradation
- [ ] Rollback optimistic updates on error
- [ ] Retry logic cho failed operations
- [ ] User feedback on errors

## Trade-offs

| Ưu điểm | Nhược điểm |
|---------|------------|
| Better UX (responsive) | More complex code |
| Higher perceived performance | Race conditions possible |
| Parallel execution | Error handling harder |

## Best Practices
1. **Show loading states**: User knows something is happening
2. **Optimistic updates**: Update UI immediately
3. **Parallel operations**: Use Promise.all for independent tasks
4. **Cancel on unmount**: Prevent memory leaks
5. **Error boundaries**: Catch async errors
6. **Retry logic**: Handle transient failures

## Anti-patterns
- ❌ Blocking UI với synchronous operations
- ❌ Không show loading states
- ❌ Không handle errors
- ❌ Không cancel pending requests
- ❌ Sequential operations có thể parallel

## Related Patterns
- [Immediately Runnable Code](./pattern-immediately-runnable-code.md)
- [File Edit Validation](./pattern-file-edit-validation.md)
