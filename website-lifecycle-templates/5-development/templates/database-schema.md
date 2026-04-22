# Database Schema Template

> Extracted from: Cursor, VSCode Agent, Windsurf, Claude Code
> Phase: Development
> Last Updated: 2026-04-22

---

## 🎯 Core Principles

### 1. Schema Design
- **Normalization**: Tránh data duplication
- **Indexing**: Optimize query performance
- **Relationships**: Clear foreign key constraints
- **Naming**: Consistent, descriptive names

### 2. Data Integrity
- **Constraints**: NOT NULL, UNIQUE, CHECK
- **Cascading**: ON DELETE, ON UPDATE rules
- **Validation**: Database-level validation

---

## 📋 Naming Conventions

### Tables
```sql
-- ✅ GOOD - Plural, snake_case
users
products
order_items
user_profiles

-- ❌ BAD
User
tblProducts
OrderItem
```

### Columns
```sql
-- ✅ GOOD - Descriptive, snake_case
id
user_id
created_at
email_address
is_active

-- ❌ BAD
ID
userId
createdDate
email
active
```

### Indexes
```sql
-- ✅ GOOD - Descriptive prefix
idx_users_email
idx_products_category_id
idx_orders_user_id_created_at

-- ❌ BAD
index1
user_index
```

---

## 🔧 Schema Patterns

### User Management
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  full_name VARCHAR(255),
  is_active BOOLEAN DEFAULT true,
  email_verified_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_created_at ON users(created_at);

-- Trigger for updated_at
CREATE TRIGGER update_users_updated_at
  BEFORE UPDATE ON users
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();
```

### E-commerce Schema
```sql
-- Products
CREATE TABLE products (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL,
  slug VARCHAR(255) UNIQUE NOT NULL,
  description TEXT,
  price DECIMAL(10, 2) NOT NULL CHECK (price >= 0),
  stock_quantity INTEGER DEFAULT 0 CHECK (stock_quantity >= 0),
  category_id UUID REFERENCES categories(id) ON DELETE SET NULL,
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Orders
CREATE TABLE orders (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  status VARCHAR(50) NOT NULL DEFAULT 'pending',
  total_amount DECIMAL(10, 2) NOT NULL CHECK (total_amount >= 0),
  shipping_address JSONB,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Order Items
CREATE TABLE order_items (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  order_id UUID NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
  product_id UUID NOT NULL REFERENCES products(id) ON DELETE RESTRICT,
  quantity INTEGER NOT NULL CHECK (quantity > 0),
  unit_price DECIMAL(10, 2) NOT NULL CHECK (unit_price >= 0),
  subtotal DECIMAL(10, 2) GENERATED ALWAYS AS (quantity * unit_price) STORED
);

CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_order_items_order_id ON order_items(order_id);
```

---

## 🔐 Security Patterns

### Soft Delete
```sql
ALTER TABLE users ADD COLUMN deleted_at TIMESTAMP;

CREATE INDEX idx_users_deleted_at ON users(deleted_at);

-- Query active users
SELECT * FROM users WHERE deleted_at IS NULL;
```

### Audit Trail
```sql
CREATE TABLE audit_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  table_name VARCHAR(255) NOT NULL,
  record_id UUID NOT NULL,
  action VARCHAR(50) NOT NULL, -- INSERT, UPDATE, DELETE
  old_data JSONB,
  new_data JSONB,
  user_id UUID REFERENCES users(id),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_audit_logs_table_record ON audit_logs(table_name, record_id);
CREATE INDEX idx_audit_logs_user_id ON audit_logs(user_id);
```

---

## 📊 Relationship Patterns

### One-to-Many
```sql
-- User has many posts
CREATE TABLE posts (
  id UUID PRIMARY KEY,
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  title VARCHAR(255) NOT NULL,
  content TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Many-to-Many
```sql
-- Products and Tags (many-to-many)
CREATE TABLE tags (
  id UUID PRIMARY KEY,
  name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE product_tags (
  product_id UUID REFERENCES products(id) ON DELETE CASCADE,
  tag_id UUID REFERENCES tags(id) ON DELETE CASCADE,
  PRIMARY KEY (product_id, tag_id)
);

CREATE INDEX idx_product_tags_product_id ON product_tags(product_id);
CREATE INDEX idx_product_tags_tag_id ON product_tags(tag_id);
```

### Self-Referencing
```sql
-- Categories with parent-child relationship
CREATE TABLE categories (
  id UUID PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  parent_id UUID REFERENCES categories(id) ON DELETE SET NULL,
  level INTEGER DEFAULT 0,
  path VARCHAR(500) -- Materialized path: /1/2/3
);

CREATE INDEX idx_categories_parent_id ON categories(parent_id);
CREATE INDEX idx_categories_path ON categories(path);
```

---

## 🎨 Migration Pattern

### Migration File Structure
```
migrations/
├── 001_create_users_table.sql
├── 002_create_products_table.sql
├── 003_add_email_verification.sql
└── 004_create_orders_table.sql
```

### Migration Template
```sql
-- Migration: 001_create_users_table.sql
-- Up
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Down
DROP TABLE IF EXISTS users;
```

---

## 🔍 Query Optimization

### Indexing Strategy
```sql
-- Single column index
CREATE INDEX idx_users_email ON users(email);

-- Composite index (order matters!)
CREATE INDEX idx_orders_user_status ON orders(user_id, status);

-- Partial index
CREATE INDEX idx_active_users ON users(email) WHERE is_active = true;

-- Full-text search
CREATE INDEX idx_products_search ON products USING GIN(to_tsvector('english', name || ' ' || description));
```

### Query Examples
```sql
-- ✅ GOOD - Uses index
SELECT * FROM users WHERE email = 'user@example.com';

-- ✅ GOOD - Composite index usage
SELECT * FROM orders WHERE user_id = '...' AND status = 'pending';

-- ❌ BAD - Function on indexed column prevents index usage
SELECT * FROM users WHERE LOWER(email) = 'user@example.com';

-- ✅ GOOD - Use functional index instead
CREATE INDEX idx_users_email_lower ON users(LOWER(email));
SELECT * FROM users WHERE LOWER(email) = 'user@example.com';
```

---

## 📝 ORM Patterns (Prisma Example)

### Schema Definition
```prisma
// schema.prisma
model User {
  id            String    @id @default(uuid())
  email         String    @unique
  passwordHash  String    @map("password_hash")
  fullName      String?   @map("full_name")
  isActive      Boolean   @default(true) @map("is_active")
  createdAt     DateTime  @default(now()) @map("created_at")
  updatedAt     DateTime  @updatedAt @map("updated_at")
  
  orders        Order[]
  
  @@index([email])
  @@map("users")
}

model Order {
  id            String    @id @default(uuid())
  userId        String    @map("user_id")
  status        String    @default("pending")
  totalAmount   Decimal   @map("total_amount")
  createdAt     DateTime  @default(now()) @map("created_at")
  
  user          User      @relation(fields: [userId], references: [id], onDelete: Cascade)
  items         OrderItem[]
  
  @@index([userId])
  @@index([status])
  @@map("orders")
}
```

---

## 🔍 Pattern Sources

**Cursor Agent**:
- Schema exploration via semantic search
- Relationship pattern identification

**VSCode Agent**:
- Migration patterns
- Index optimization

**Windsurf**:
- Security patterns (audit logs, soft delete)
- Data integrity constraints

**Claude Code**:
- ORM integration patterns
- Query optimization

---

## 📋 Implementation Checklist

- [ ] Define naming conventions
- [ ] Design entity relationships
- [ ] Add appropriate indexes
- [ ] Setup constraints (FK, UNIQUE, CHECK)
- [ ] Implement soft delete if needed
- [ ] Add audit trail for sensitive tables
- [ ] Create migration files
- [ ] Write seed data scripts
- [ ] Document schema (ERD diagram)
- [ ] Test query performance

---

**Related Templates**:
- [API Design](./api-design.md)
- [Project Structure](./project-structure.md)
- [Coding Standards](./coding-standards.md)
