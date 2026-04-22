# Pattern: Debug Logging

## Nguồn
- Claude Code
- Cursor Agent
- Windsurf Cascade

## Mô tả
Systematic logging strategy để debug issues nhanh chóng. Structured logs, log levels, contextual information.

## Khi nào dùng
- Testing: debug test failures
- Development: trace execution flow
- Production: monitor errors
- Performance: identify bottlenecks

## Cách áp dụng

### 1. Log Levels
```typescript
enum LogLevel {
  DEBUG = 0,
  INFO = 1,
  WARN = 2,
  ERROR = 3,
}

class Logger {
  private level: LogLevel
  
  constructor(level: LogLevel = LogLevel.INFO) {
    this.level = level
  }
  
  debug(message: string, context?: any) {
    if (this.level <= LogLevel.DEBUG) {
      console.debug(`[DEBUG] ${message}`, context)
    }
  }
  
  info(message: string, context?: any) {
    if (this.level <= LogLevel.INFO) {
      console.info(`[INFO] ${message}`, context)
    }
  }
  
  warn(message: string, context?: any) {
    if (this.level <= LogLevel.WARN) {
      console.warn(`[WARN] ${message}`, context)
    }
  }
  
  error(message: string, error?: Error, context?: any) {
    if (this.level <= LogLevel.ERROR) {
      console.error(`[ERROR] ${message}`, { error, context })
    }
  }
}
```

### 2. Structured Logging
```typescript
interface LogEntry {
  timestamp: string
  level: string
  message: string
  context?: any
  error?: {
    name: string
    message: string
    stack?: string
  }
  metadata?: {
    userId?: string
    requestId?: string
    sessionId?: string
  }
}

function createLogEntry(
  level: string,
  message: string,
  options?: {
    context?: any
    error?: Error
    metadata?: any
  }
): LogEntry {
  return {
    timestamp: new Date().toISOString(),
    level,
    message,
    context: options?.context,
    error: options?.error && {
      name: options.error.name,
      message: options.error.message,
      stack: options.error.stack,
    },
    metadata: options?.metadata,
  }
}
```

### 3. Contextual Logging
```typescript
// Add context to all logs
class ContextualLogger {
  constructor(
    private logger: Logger,
    private context: Record<string, any>
  ) {}
  
  debug(message: string, additionalContext?: any) {
    this.logger.debug(message, {
      ...this.context,
      ...additionalContext,
    })
  }
  
  info(message: string, additionalContext?: any) {
    this.logger.info(message, {
      ...this.context,
      ...additionalContext,
    })
  }
  
  error(message: string, error?: Error, additionalContext?: any) {
    this.logger.error(message, error, {
      ...this.context,
      ...additionalContext,
    })
  }
}

// Usage
const logger = new ContextualLogger(baseLogger, {
  userId: '123',
  requestId: 'abc-def',
})

logger.info('User logged in')
// Output: [INFO] User logged in { userId: '123', requestId: 'abc-def' }
```

## Ví dụ thực tế

### E-commerce Checkout Logging

```typescript
// Checkout flow với debug logging
async function processCheckout(order: Order) {
  const logger = new ContextualLogger(baseLogger, {
    orderId: order.id,
    userId: order.userId,
    flow: 'checkout',
  })
  
  logger.info('Checkout started', {
    cartTotal: order.total,
    itemCount: order.items.length,
  })
  
  try {
    // Step 1: Validate cart
    logger.debug('Validating cart')
    const validatedCart = await validateCart(order.cart)
    logger.info('Cart validated', {
      validItems: validatedCart.length,
    })
    
    // Step 2: Calculate shipping
    logger.debug('Calculating shipping', {
      address: order.shippingAddress,
    })
    const shipping = await calculateShipping(order)
    logger.info('Shipping calculated', {
      method: shipping.method,
      cost: shipping.cost,
    })
    
    // Step 3: Process payment
    logger.debug('Processing payment', {
      method: order.paymentMethod,
      amount: order.total,
    })
    const payment = await processPayment(order)
    logger.info('Payment processed', {
      transactionId: payment.id,
      status: payment.status,
    })
    
    // Step 4: Create order
    logger.debug('Creating order')
    const createdOrder = await createOrder(order)
    logger.info('Order created', {
      orderId: createdOrder.id,
      status: createdOrder.status,
    })
    
    logger.info('Checkout completed successfully')
    return createdOrder
    
  } catch (error) {
    logger.error('Checkout failed', error as Error, {
      step: getCurrentStep(),
      orderData: order,
    })
    throw error
  }
}
```

### API Request Logging

```typescript
// Middleware để log API requests
function requestLogger(req: Request, res: Response, next: NextFunction) {
  const requestId = generateRequestId()
  const logger = new ContextualLogger(baseLogger, {
    requestId,
    method: req.method,
    path: req.path,
    userId: req.user?.id,
  })
  
  // Log request
  logger.info('Request received', {
    query: req.query,
    body: sanitizeBody(req.body),
    headers: sanitizeHeaders(req.headers),
  })
  
  const startTime = Date.now()
  
  // Log response
  res.on('finish', () => {
    const duration = Date.now() - startTime
    
    if (res.statusCode >= 500) {
      logger.error('Request failed', undefined, {
        statusCode: res.statusCode,
        duration,
      })
    } else if (res.statusCode >= 400) {
      logger.warn('Request error', {
        statusCode: res.statusCode,
        duration,
      })
    } else {
      logger.info('Request completed', {
        statusCode: res.statusCode,
        duration,
      })
    }
  })
  
  // Attach logger to request
  req.logger = logger
  next()
}
```

### Performance Logging

```typescript
// Log performance metrics
class PerformanceLogger {
  private timers: Map<string, number> = new Map()
  
  start(label: string) {
    this.timers.set(label, performance.now())
    logger.debug(`Performance: ${label} started`)
  }
  
  end(label: string) {
    const startTime = this.timers.get(label)
    
    if (!startTime) {
      logger.warn(`Performance: ${label} not started`)
      return
    }
    
    const duration = performance.now() - startTime
    this.timers.delete(label)
    
    logger.info(`Performance: ${label} completed`, {
      duration: `${duration.toFixed(2)}ms`,
    })
    
    // Warn if slow
    if (duration > 1000) {
      logger.warn(`Performance: ${label} is slow`, {
        duration: `${duration.toFixed(2)}ms`,
        threshold: '1000ms',
      })
    }
  }
}

// Usage
const perfLogger = new PerformanceLogger()

perfLogger.start('fetch-products')
const products = await fetchProducts()
perfLogger.end('fetch-products')
```

### Error Tracking

```typescript
// Comprehensive error logging
function logError(error: Error, context?: any) {
  const errorLog: LogEntry = {
    timestamp: new Date().toISOString(),
    level: 'ERROR',
    message: error.message,
    error: {
      name: error.name,
      message: error.message,
      stack: error.stack,
    },
    context: {
      ...context,
      userAgent: navigator.userAgent,
      url: window.location.href,
      timestamp: Date.now(),
    },
  }
  
  // Log to console
  console.error('[ERROR]', errorLog)
  
  // Send to error tracking service
  sendToErrorTracking(errorLog)
  
  // Store locally for debugging
  storeErrorLocally(errorLog)
}

// Global error handler
window.addEventListener('error', (event) => {
  logError(event.error, {
    type: 'uncaught',
    filename: event.filename,
    lineno: event.lineno,
    colno: event.colno,
  })
})

// Unhandled promise rejections
window.addEventListener('unhandledrejection', (event) => {
  logError(new Error(event.reason), {
    type: 'unhandled-rejection',
  })
})
```

## Debug Logging Checklist

### Development
- [ ] Log level set to DEBUG
- [ ] Contextual information included
- [ ] Performance metrics tracked
- [ ] Error stack traces captured

### Production
- [ ] Log level set to INFO or WARN
- [ ] Sensitive data sanitized
- [ ] Logs sent to monitoring service
- [ ] Error tracking enabled

### Best Practices
- [ ] Structured log format
- [ ] Request IDs for tracing
- [ ] Timestamps in ISO format
- [ ] Log rotation configured

## Trade-offs

| Ưu điểm | Nhược điểm |
|---------|------------|
| Faster debugging | Performance overhead |
| Better observability | Log storage costs |
| Easier troubleshooting | Sensitive data risk |

## Best Practices
1. **Use log levels**: DEBUG for dev, INFO for prod
2. **Add context**: User ID, request ID, session ID
3. **Sanitize data**: Remove passwords, tokens
4. **Structure logs**: JSON format for parsing
5. **Performance tracking**: Log slow operations
6. **Error details**: Stack traces, context

## Anti-patterns
- ❌ Log sensitive data (passwords, tokens)
- ❌ Too much logging (noise)
- ❌ No log levels (everything is INFO)
- ❌ Unstructured logs (hard to parse)
- ❌ No context (can't trace issues)

## Related Patterns
- [Test-Driven Validation](./pattern-test-driven-validation.md)
