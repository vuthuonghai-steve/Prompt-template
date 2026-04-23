# Pattern: Database Migration Safety

## Nguồn
- Claude Code
- Cursor
- Windsurf

## Mô tả
Safe database schema changes with rollback capability, zero-downtime migrations, and data integrity verification.

## Khi nào dùng
- Schema changes in production
- Adding/removing columns
- Index creation
- Data type changes
- Large table migrations
- Multi-step migrations

## Cách áp dụng

### 1. Migration Structure

```typescript
interface Migration {
  version: string
  description: string
  up: (db: Database) => Promise<void>
  down: (db: Database) => Promise<void>
  validate?: (db: Database) => Promise<boolean>
}

// Example migration file
export const migration_20260423_add_wishlist: Migration = {
  version: '20260423_001',
  description: 'Add wishlist field to users collection',
  
  async up(db) {
    await db.collection('users').updateMany(
      {},
      { $set: { wishlist: [] } }
    )
  },
  
  async down(db) {
    await db.collection('users').updateMany(
      {},
      { $unset: { wishlist: '' } }
    )
  },
  
  async validate(db) {
    const usersWithoutWishlist = await db.collection('users').countDocuments({
      wishlist: { $exists: false }
    })
    return usersWithoutWishlist === 0
  }
}
```

### 2. Zero-Downtime Migration Pattern

```typescript
// Step 1: Add new column (nullable)
async function step1_add_column(db: Database) {
  await db.collection('products').updateMany(
    {},
    { $set: { newPrice: null } }
  )
}

// Step 2: Backfill data (batched)
async function step2_backfill(db: Database) {
  const batchSize = 1000
  let processed = 0
  
  while (true) {
    const products = await db.collection('products')
      .find({ newPrice: null })
      .limit(batchSize)
      .toArray()
    
    if (products.length === 0) break
    
    const bulkOps = products.map(p => ({
      updateOne: {
        filter: { _id: p._id },
        update: { $set: { newPrice: p.price * 1.1 } }
      }
    }))
    
    await db.collection('products').bulkWrite(bulkOps)
    processed += products.length
    
    console.log(`Backfilled ${processed} products`)
    await sleep(100) // Throttle to avoid overload
  }
}

// Step 3: Make column non-nullable (after verification)
async function step3_add_constraint(db: Database) {
  // Verify all rows have data
  const nullCount = await db.collection('products').countDocuments({
    newPrice: null
  })
  
  if (nullCount > 0) {
    throw new Error(`${nullCount} products still have null newPrice`)
  }
  
  // Add validation rule
  await db.command({
    collMod: 'products',
    validator: {
      $jsonSchema: {
        required: ['newPrice'],
        properties: {
          newPrice: { bsonType: 'double', minimum: 0 }
        }
      }
    }
  })
}

// Step 4: Remove old column (after monitoring)
async function step4_remove_old_column(db: Database) {
  await db.collection('products').updateMany(
    {},
    { $unset: { price: '' } }
  )
}
```

### 3. Migration Workflow

```
Pre-Migration
├── Backup database
├── Test migration on staging
├── Verify rollback works
└── Document rollback steps

During Migration
├── Run migration in transaction (if supported)
├── Monitor error logs
├── Verify data integrity
└── Check application health

Post-Migration
├── Verify application functionality
├── Monitor performance metrics
├── Keep backup for 7 days
└── Document lessons learned
```

## Ví dụ thực tế

### E-commerce: Add Product Tags

```typescript
// migrations/20260423_add_product_tags.ts

export const migration = {
  version: '20260423_002',
  description: 'Add tags array to products for better categorization',
  
  async up(db: Database) {
    console.log('Starting migration: Add product tags')
    
    // Step 1: Add tags field (empty array)
    await db.collection('products').updateMany(
      { tags: { $exists: false } },
      { $set: { tags: [] } }
    )
    
    // Step 2: Migrate category to tags
    const products = await db.collection('products')
      .find({ category: { $exists: true } })
      .toArray()
    
    for (const product of products) {
      const tags = [product.category]
      
      // Add seasonal tags
      if (product.seasonal) {
        tags.push(`season:${product.season}`)
      }
      
      // Add occasion tags
      if (product.occasion) {
        tags.push(`occasion:${product.occasion}`)
      }
      
      await db.collection('products').updateOne(
        { _id: product._id },
        { $set: { tags } }
      )
    }
    
    console.log(`Migrated ${products.length} products`)
  },
  
  async down(db: Database) {
    console.log('Rolling back: Remove product tags')
    
    await db.collection('products').updateMany(
      {},
      { $unset: { tags: '' } }
    )
  },
  
  async validate(db: Database) {
    // Verify all products have tags field
    const withoutTags = await db.collection('products').countDocuments({
      tags: { $exists: false }
    })
    
    if (withoutTags > 0) {
      console.error(`${withoutTags} products missing tags field`)
      return false
    }
    
    // Verify tags is array
    const invalidTags = await db.collection('products').countDocuments({
      tags: { $not: { $type: 'array' } }
    })
    
    if (invalidTags > 0) {
      console.error(`${invalidTags} products have invalid tags type`)
      return false
    }
    
    return true
  }
}
```

### E-commerce: Index Creation (Non-Blocking)

```typescript
// migrations/20260423_add_search_index.ts

export const migration = {
  version: '20260423_003',
  description: 'Add text search index on product name and description',
  
  async up(db: Database) {
    console.log('Creating search index (background)')
    
    // Create index in background to avoid blocking writes
    await db.collection('products').createIndex(
      {
        name: 'text',
        description: 'text',
        tags: 'text'
      },
      {
        name: 'product_search_idx',
        background: true, // Non-blocking
        weights: {
          name: 10,
          tags: 5,
          description: 1
        }
      }
    )
    
    console.log('Index creation started (will complete in background)')
  },
  
  async down(db: Database) {
    console.log('Dropping search index')
    
    await db.collection('products').dropIndex('product_search_idx')
  },
  
  async validate(db: Database) {
    const indexes = await db.collection('products').indexes()
    const searchIndex = indexes.find(idx => idx.name === 'product_search_idx')
    
    if (!searchIndex) {
      console.error('Search index not found')
      return false
    }
    
    console.log('Search index validated:', searchIndex)
    return true
  }
}
```

### E-commerce: Data Type Change

```typescript
// migrations/20260423_change_price_type.ts

export const migration = {
  version: '20260423_004',
  description: 'Change price from string to number for calculations',
  
  async up(db: Database) {
    console.log('Converting price from string to number')
    
    const batchSize = 500
    let processed = 0
    
    while (true) {
      const products = await db.collection('products')
        .find({ price: { $type: 'string' } })
        .limit(batchSize)
        .toArray()
      
      if (products.length === 0) break
      
      const bulkOps = products.map(p => {
        const numericPrice = parseFloat(p.price.replace(/[^0-9.]/g, ''))
        
        if (isNaN(numericPrice)) {
          console.warn(`Invalid price for product ${p._id}: ${p.price}`)
          return null
        }
        
        return {
          updateOne: {
            filter: { _id: p._id },
            update: { $set: { price: numericPrice } }
          }
        }
      }).filter(Boolean)
      
      if (bulkOps.length > 0) {
        await db.collection('products').bulkWrite(bulkOps)
      }
      
      processed += products.length
      console.log(`Converted ${processed} products`)
      
      // Throttle to avoid overload
      await new Promise(resolve => setTimeout(resolve, 100))
    }
    
    console.log(`Migration complete: ${processed} products converted`)
  },
  
  async down(db: Database) {
    console.log('Converting price from number to string')
    
    await db.collection('products').updateMany(
      { price: { $type: 'number' } },
      [{ $set: { price: { $toString: '$price' } } }]
    )
  },
  
  async validate(db: Database) {
    const stringPrices = await db.collection('products').countDocuments({
      price: { $type: 'string' }
    })
    
    if (stringPrices > 0) {
      console.error(`${stringPrices} products still have string prices`)
      return false
    }
    
    const invalidPrices = await db.collection('products').countDocuments({
      price: { $lt: 0 }
    })
    
    if (invalidPrices > 0) {
      console.error(`${invalidPrices} products have negative prices`)
      return false
    }
    
    return true
  }
}
```

## Migration Checklist

### Pre-Migration
- [ ] Backup production database
- [ ] Test migration on staging with production data copy
- [ ] Verify rollback procedure works
- [ ] Estimate migration duration
- [ ] Plan maintenance window (if needed)
- [ ] Document rollback steps
- [ ] Notify team of migration schedule

### During Migration
- [ ] Enable maintenance mode (if needed)
- [ ] Run migration
- [ ] Monitor error logs
- [ ] Verify data integrity
- [ ] Check application health endpoints
- [ ] Disable maintenance mode

### Post-Migration
- [ ] Verify application functionality
- [ ] Monitor performance metrics
- [ ] Check error rates
- [ ] Validate data with spot checks
- [ ] Keep backup for 7 days
- [ ] Document any issues encountered

## Best Practices

### Do's
✅ Always write down() rollback function
✅ Test on staging with production data
✅ Use batched updates for large tables
✅ Add validation checks
✅ Create indexes in background
✅ Monitor during migration
✅ Keep backups

### Don'ts
❌ Run migrations without backup
❌ Skip staging testing
❌ Update all rows in single query (large tables)
❌ Drop columns immediately
❌ Change data types without validation
❌ Ignore migration errors
❌ Delete backups immediately

## Trade-offs

| Ưu điểm | Nhược điểm |
|---------|------------|
| Safe schema evolution | Requires planning |
| Rollback capability | Multi-step complexity |
| Zero downtime possible | Longer migration time |
| Data integrity verified | Storage overhead (backups) |

## Related Patterns
- [Deployment Strategy](../templates/deployment-strategy.md)
- [Performance Baseline](../../7-maintenance/templates/performance-baseline.md)
