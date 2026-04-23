# Pattern: WebContainer Constraints

## Nguồn
- StackBlitz WebContainers
- CodeSandbox
- Replit

## Mô tả
Understanding and working within WebContainer limitations - browser-based Node.js runtime with specific constraints on native modules, filesystem, and system calls.

## Khi nào dùng
- Building browser-based dev environments
- Creating interactive coding tutorials
- Developing online IDEs
- Running Node.js in browser
- Prototyping without local setup

## Cách áp dụng

### 1. WebContainer Architecture

```
┌─────────────────────────────────┐
│         Browser Tab             │
│  ┌───────────────────────────┐  │
│  │    WebContainer VM        │  │
│  │  ┌─────────────────────┐  │  │
│  │  │   Node.js Runtime   │  │  │
│  │  │   (WASM-based)      │  │  │
│  │  └─────────────────────┘  │  │
│  │  ┌─────────────────────┐  │  │
│  │  │  Virtual Filesystem │  │  │
│  │  │  (In-memory)        │  │  │
│  │  └─────────────────────┘  │  │
│  └───────────────────────────┘  │
└─────────────────────────────────┘
```

### 2. Supported vs Unsupported

```typescript
// ✅ SUPPORTED
import express from 'express'
import react from 'react'
import { readFile } from 'fs/promises'

// ❌ NOT SUPPORTED
import sharp from 'sharp'           // Native image processing
import sqlite3 from 'sqlite3'       // Native database
import { spawn } from 'child_process'  // System processes
```

### 3. Constraint Categories

```typescript
interface WebContainerConstraints {
  // Native modules - NOT supported
  nativeModules: {
    imageProcessing: ['sharp', 'jimp-native'],
    databases: ['sqlite3', 'better-sqlite3'],
    crypto: ['bcrypt', 'argon2'],
    compression: ['node-zlib']
  }
  
  // System calls - LIMITED
  systemCalls: {
    childProcess: false,      // No spawn/exec
    networkRaw: false,        // No raw sockets
    filesystem: 'virtual'     // In-memory only
  }
  
  // Performance - CONSTRAINED
  performance: {
    memory: '~100MB',         // Browser memory limits
    cpu: 'single-thread',     // No worker threads
    storage: 'temporary'      // Lost on refresh
  }
}
```

## Ví dụ thực tế

### E-commerce: Image Upload Workaround

```typescript
// ❌ WRONG: Native image processing
import sharp from 'sharp'

async function processImage(file: File) {
  const buffer = await file.arrayBuffer()
  const processed = await sharp(buffer)
    .resize(800, 600)
    .webp()
    .toBuffer()
  return processed
}

// ✅ CORRECT: Browser-native Canvas API
async function processImage(file: File): Promise<Blob> {
  return new Promise((resolve, reject) => {
    const img = new Image()
    const canvas = document.createElement('canvas')
    const ctx = canvas.getContext('2d')
    
    img.onload = () => {
      // Resize
      const maxWidth = 800
      const maxHeight = 600
      let width = img.width
      let height = img.height
      
      if (width > maxWidth) {
        height = (height * maxWidth) / width
        width = maxWidth
      }
      if (height > maxHeight) {
        width = (width * maxHeight) / height
        height = maxHeight
      }
      
      canvas.width = width
      canvas.height = height
      ctx?.drawImage(img, 0, 0, width, height)
      
      // Convert to WebP
      canvas.toBlob(
        (blob) => {
          if (blob) resolve(blob)
          else reject(new Error('Failed to convert'))
        },
        'image/webp',
        0.9
      )
    }
    
    img.onerror = reject
    img.src = URL.createObjectURL(file)
  })
}
```

### E-commerce: Database Alternative

```typescript
// ❌ WRONG: Native SQLite
import sqlite3 from 'sqlite3'

const db = new sqlite3.Database(':memory:')
db.run('CREATE TABLE products (id INTEGER, name TEXT)')

// ✅ CORRECT: SQL.js (WASM-based)
import initSqlJs from 'sql.js'

async function initDatabase() {
  const SQL = await initSqlJs({
    locateFile: (file) => `https://sql.js.org/dist/${file}`
  })
  
  const db = new SQL.Database()
  
  db.run(`
    CREATE TABLE products (
      id INTEGER PRIMARY KEY,
      name TEXT NOT NULL,
      price REAL NOT NULL,
      stock INTEGER DEFAULT 0
    )
  `)
  
  return db
}

// Usage
const db = await initDatabase()

db.run(
  'INSERT INTO products (name, price, stock) VALUES (?, ?, ?)',
  ['Rose Bouquet', 50.00, 10]
)

const results = db.exec('SELECT * FROM products')
console.log(results)
```

### E-commerce: Password Hashing Alternative

```typescript
// ❌ WRONG: Native bcrypt
import bcrypt from 'bcrypt'

const hash = await bcrypt.hash(password, 10)

// ✅ CORRECT: Pure JS bcryptjs
import bcryptjs from 'bcryptjs'

const hash = await bcryptjs.hash(password, 10)
const isValid = await bcryptjs.compare(password, hash)
```

### E-commerce: File Storage Alternative

```typescript
// ❌ WRONG: Filesystem persistence
import { writeFile } from 'fs/promises'

await writeFile('/data/products.json', JSON.stringify(products))

// ✅ CORRECT: IndexedDB for persistence
async function saveProducts(products: Product[]) {
  const db = await openDB('siinstore', 1, {
    upgrade(db) {
      db.createObjectStore('products', { keyPath: 'id' })
    }
  })
  
  const tx = db.transaction('products', 'readwrite')
  
  for (const product of products) {
    await tx.store.put(product)
  }
  
  await tx.done
}

async function loadProducts(): Promise<Product[]> {
  const db = await openDB('siinstore', 1)
  return db.getAll('products')
}
```

## Package Alternatives

### Image Processing

```typescript
// Native: sharp
// Alternative: browser-image-compression
import imageCompression from 'browser-image-compression'

const options = {
  maxSizeMB: 1,
  maxWidthOrHeight: 1920,
  useWebWorker: true
}

const compressedFile = await imageCompression(file, options)
```

### Database

```typescript
// Native: sqlite3, better-sqlite3
// Alternative: sql.js (WASM)
import initSqlJs from 'sql.js'

// Alternative: Dexie.js (IndexedDB wrapper)
import Dexie from 'dexie'

class ProductDatabase extends Dexie {
  products!: Dexie.Table<Product, number>
  
  constructor() {
    super('ProductDatabase')
    this.version(1).stores({
      products: '++id, name, category, price'
    })
  }
}

const db = new ProductDatabase()
await db.products.add({ name: 'Rose', price: 50 })
```

### Crypto

```typescript
// Native: bcrypt, argon2
// Alternative: bcryptjs (pure JS)
import bcryptjs from 'bcryptjs'

// Alternative: Web Crypto API
async function hashPassword(password: string): Promise<string> {
  const encoder = new TextEncoder()
  const data = encoder.encode(password)
  const hashBuffer = await crypto.subtle.digest('SHA-256', data)
  const hashArray = Array.from(new Uint8Array(hashBuffer))
  return hashArray.map(b => b.toString(16).padStart(2, '0')).join('')
}
```

### PDF Generation

```typescript
// Native: puppeteer, playwright
// Alternative: jsPDF (pure JS)
import jsPDF from 'jspdf'

const doc = new jsPDF()
doc.text('Order Invoice', 10, 10)
doc.text(`Order ID: ${orderId}`, 10, 20)
doc.save('invoice.pdf')

// Alternative: pdfmake
import pdfMake from 'pdfmake/build/pdfmake'

const docDefinition = {
  content: [
    { text: 'Order Invoice', style: 'header' },
    { text: `Order ID: ${orderId}` }
  ]
}

pdfMake.createPdf(docDefinition).download('invoice.pdf')
```

## Detection and Fallback

```typescript
// Detect WebContainer environment
function isWebContainer(): boolean {
  return (
    typeof window !== 'undefined' &&
    'WebContainer' in window
  )
}

// Conditional imports
async function getImageProcessor() {
  if (isWebContainer()) {
    // Use browser-native solution
    return await import('./image-processor-canvas')
  } else {
    // Use native sharp
    return await import('./image-processor-sharp')
  }
}

// Usage
const processor = await getImageProcessor()
const processed = await processor.processImage(file)
```

## Performance Optimization

```typescript
// ✅ Use Web Workers for heavy computation
const worker = new Worker(new URL('./worker.ts', import.meta.url))

worker.postMessage({ type: 'process', data: largeDataset })

worker.onmessage = (e) => {
  console.log('Processed:', e.data)
}

// ✅ Lazy load heavy dependencies
const loadPdfGenerator = async () => {
  const { default: jsPDF } = await import('jspdf')
  return new jsPDF()
}

// ✅ Use streaming for large files
async function processLargeFile(file: File) {
  const stream = file.stream()
  const reader = stream.getReader()
  
  while (true) {
    const { done, value } = await reader.read()
    if (done) break
    
    // Process chunk
    await processChunk(value)
  }
}
```

## Compatibility Matrix

| Feature | Native Node.js | WebContainer | Alternative |
|---------|---------------|--------------|-------------|
| **Image Processing** | sharp | ❌ | Canvas API, browser-image-compression |
| **Database** | sqlite3 | ❌ | sql.js, IndexedDB, Dexie |
| **Crypto** | bcrypt | ❌ | bcryptjs, Web Crypto API |
| **PDF** | puppeteer | ❌ | jsPDF, pdfmake |
| **Child Process** | spawn/exec | ❌ | Web Workers |
| **Filesystem** | fs | ⚠️ Virtual | IndexedDB, localStorage |
| **HTTP Server** | http/express | ✅ | Fully supported |
| **WebSocket** | ws | ✅ | Fully supported |
| **Pure JS libs** | Any | ✅ | Fully supported |

## Best Practices

### Do's
✅ Use pure JavaScript libraries
✅ Leverage browser APIs (Canvas, Web Crypto)
✅ Use WASM alternatives (sql.js)
✅ Implement feature detection
✅ Provide fallbacks
✅ Test in WebContainer environment

### Don'ts
❌ Rely on native modules
❌ Use child_process
❌ Assume filesystem persistence
❌ Use raw network sockets
❌ Expect full Node.js compatibility
❌ Ignore memory constraints

## Trade-offs

| Ưu điểm | Nhược điểm |
|---------|------------|
| No local setup needed | Limited native module support |
| Instant startup | Performance constraints |
| Sandboxed security | No persistent filesystem |
| Cross-platform | Memory limitations |

## Related Patterns
- [Tool Use Sequencing](./pattern-tool-use-sequencing.md)
- [Performance Baseline](../../7-maintenance/templates/performance-baseline.md)
