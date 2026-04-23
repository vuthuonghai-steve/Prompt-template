# Pattern: MCP Integration

## Nguồn
- Claude Code
- Cursor

## Mô tả
Model Context Protocol (MCP) integration for extending AI capabilities with external tools, APIs, and data sources through standardized server connections.

## Khi nào dùng
- Need external data access (databases, APIs)
- Require specialized tools (design, testing)
- Want persistent context across sessions
- Need real-time data integration
- Building custom AI workflows

## Cách áp dụng

### 1. MCP Architecture

```
┌─────────────────┐
│   AI Assistant  │
│  (Claude Code)  │
└────────┬────────┘
         │
         │ MCP Protocol
         │
┌────────▼────────┐
│   MCP Server    │
│   (stdio/SSE)   │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
┌───▼───┐ ┌──▼────┐
│ Tools │ │Resources│
└───────┘ └────────┘
```

### 2. MCP Server Configuration

```json
// .claude/mcp.json
{
  "mcpServers": {
    "database": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "DATABASE_URL": "postgresql://localhost/siinstore"
      }
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem"],
      "env": {
        "ALLOWED_PATHS": "/home/user/projects"
      }
    },
    "pencil": {
      "command": "node",
      "args": ["./mcp-servers/pencil/index.js"]
    }
  }
}
```

### 3. Tool Definition

```typescript
// MCP Tool Interface
interface MCPTool {
  name: string
  description: string
  inputSchema: JSONSchema
  handler: (params: any) => Promise<any>
}

// Example: Database Query Tool
const queryTool: MCPTool = {
  name: 'query_products',
  description: 'Query products from database with filters',
  inputSchema: {
    type: 'object',
    properties: {
      category: { type: 'string' },
      minPrice: { type: 'number' },
      maxPrice: { type: 'number' },
      limit: { type: 'number', default: 10 }
    }
  },
  handler: async (params) => {
    const { category, minPrice, maxPrice, limit } = params
    
    const query = `
      SELECT * FROM products
      WHERE category = $1
        AND price BETWEEN $2 AND $3
      LIMIT $4
    `
    
    const result = await db.query(query, [category, minPrice, maxPrice, limit])
    return result.rows
  }
}
```

### 4. Resource Definition

```typescript
// MCP Resource Interface
interface MCPResource {
  uri: string
  name: string
  description: string
  mimeType: string
  handler: () => Promise<string>
}

// Example: Product Catalog Resource
const productCatalogResource: MCPResource = {
  uri: 'catalog://products',
  name: 'Product Catalog',
  description: 'Current product inventory with stock levels',
  mimeType: 'application/json',
  handler: async () => {
    const products = await db.query('SELECT * FROM products WHERE stock > 0')
    return JSON.stringify(products.rows, null, 2)
  }
}
```

## Ví dụ thực tế

### E-commerce: Database MCP Server

```typescript
// mcp-servers/database/index.ts
import { Server } from '@modelcontextprotocol/sdk/server/index.js'
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js'
import { Pool } from 'pg'

const pool = new Pool({
  connectionString: process.env.DATABASE_URL
})

const server = new Server(
  {
    name: 'siinstore-database',
    version: '1.0.0'
  },
  {
    capabilities: {
      tools: {},
      resources: {}
    }
  }
)

// Tool: Query Products
server.setRequestHandler('tools/call', async (request) => {
  if (request.params.name === 'query_products') {
    const { category, minPrice, maxPrice, limit = 10 } = request.params.arguments
    
    const result = await pool.query(
      `SELECT id, name, price, stock, category
       FROM products
       WHERE category = $1
         AND price BETWEEN $2 AND $3
         AND stock > 0
       ORDER BY created_at DESC
       LIMIT $4`,
      [category, minPrice, maxPrice, limit]
    )
    
    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify(result.rows, null, 2)
        }
      ]
    }
  }
  
  if (request.params.name === 'update_stock') {
    const { productId, quantity } = request.params.arguments
    
    await pool.query(
      'UPDATE products SET stock = stock + $1 WHERE id = $2',
      [quantity, productId]
    )
    
    return {
      content: [
        {
          type: 'text',
          text: `Stock updated for product ${productId}`
        }
      ]
    }
  }
})

// Resource: Low Stock Alert
server.setRequestHandler('resources/read', async (request) => {
  if (request.params.uri === 'catalog://low-stock') {
    const result = await pool.query(
      `SELECT id, name, stock, category
       FROM products
       WHERE stock < 10
       ORDER BY stock ASC`
    )
    
    return {
      contents: [
        {
          uri: request.params.uri,
          mimeType: 'application/json',
          text: JSON.stringify(result.rows, null, 2)
        }
      ]
    }
  }
})

// Start server
const transport = new StdioServerTransport()
await server.connect(transport)
```

### E-commerce: Analytics MCP Server

```typescript
// mcp-servers/analytics/index.ts
import { Server } from '@modelcontextprotocol/sdk/server/index.js'
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js'

const server = new Server(
  {
    name: 'siinstore-analytics',
    version: '1.0.0'
  },
  {
    capabilities: {
      tools: {},
      resources: {}
    }
  }
)

// Tool: Get Sales Report
server.setRequestHandler('tools/call', async (request) => {
  if (request.params.name === 'get_sales_report') {
    const { startDate, endDate, groupBy = 'day' } = request.params.arguments
    
    const result = await pool.query(
      `SELECT 
         DATE_TRUNC($1, created_at) as period,
         COUNT(*) as order_count,
         SUM(total_amount) as revenue,
         AVG(total_amount) as avg_order_value
       FROM orders
       WHERE created_at BETWEEN $2 AND $3
         AND status = 'completed'
       GROUP BY period
       ORDER BY period DESC`,
      [groupBy, startDate, endDate]
    )
    
    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify(result.rows, null, 2)
        }
      ]
    }
  }
  
  if (request.params.name === 'get_top_products') {
    const { limit = 10, period = '30 days' } = request.params.arguments
    
    const result = await pool.query(
      `SELECT 
         p.id,
         p.name,
         COUNT(oi.id) as times_ordered,
         SUM(oi.quantity) as total_quantity,
         SUM(oi.price * oi.quantity) as revenue
       FROM products p
       JOIN order_items oi ON p.id = oi.product_id
       JOIN orders o ON oi.order_id = o.id
       WHERE o.created_at > NOW() - INTERVAL $1
         AND o.status = 'completed'
       GROUP BY p.id, p.name
       ORDER BY revenue DESC
       LIMIT $2`,
      [period, limit]
    )
    
    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify(result.rows, null, 2)
        }
      ]
    }
  }
})

// Resource: Real-time Dashboard
server.setRequestHandler('resources/read', async (request) => {
  if (request.params.uri === 'analytics://dashboard') {
    const [todayOrders, todayRevenue, activeUsers] = await Promise.all([
      pool.query(
        `SELECT COUNT(*) as count FROM orders 
         WHERE DATE(created_at) = CURRENT_DATE`
      ),
      pool.query(
        `SELECT SUM(total_amount) as revenue FROM orders 
         WHERE DATE(created_at) = CURRENT_DATE AND status = 'completed'`
      ),
      pool.query(
        `SELECT COUNT(DISTINCT user_id) as count FROM sessions 
         WHERE last_activity > NOW() - INTERVAL '15 minutes'`
      )
    ])
    
    const dashboard = {
      today: {
        orders: todayOrders.rows[0].count,
        revenue: todayRevenue.rows[0].revenue || 0,
        activeUsers: activeUsers.rows[0].count
      },
      timestamp: new Date().toISOString()
    }
    
    return {
      contents: [
        {
          uri: request.params.uri,
          mimeType: 'application/json',
          text: JSON.stringify(dashboard, null, 2)
        }
      ]
    }
  }
})

const transport = new StdioServerTransport()
await server.connect(transport)
```

### E-commerce: Design System MCP (Pencil)

```typescript
// Using Pencil MCP for design validation

// Tool usage in AI workflow:
// 1. Read design file
const design = await mcp.call('pencil', 'batch_get', {
  filePath: 'designs/checkout-flow.pen',
  patterns: [{ type: 'frame' }],
  readDepth: 2
})

// 2. Validate design against requirements
const validation = await mcp.call('pencil', 'validate_design', {
  filePath: 'designs/checkout-flow.pen',
  rules: {
    minFontSize: 14,
    colorContrast: 4.5,
    touchTargetSize: 44
  }
})

// 3. Generate code from design
const code = await mcp.call('pencil', 'generate_code', {
  filePath: 'designs/checkout-flow.pen',
  nodeId: 'checkout-form',
  framework: 'react',
  typescript: true
})
```

## MCP Server Development

### Server Template

```typescript
// mcp-servers/template/index.ts
import { Server } from '@modelcontextprotocol/sdk/server/index.js'
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js'

const server = new Server(
  {
    name: 'my-mcp-server',
    version: '1.0.0'
  },
  {
    capabilities: {
      tools: {},
      resources: {},
      prompts: {}
    }
  }
)

// List available tools
server.setRequestHandler('tools/list', async () => {
  return {
    tools: [
      {
        name: 'my_tool',
        description: 'Description of what this tool does',
        inputSchema: {
          type: 'object',
          properties: {
            param1: { type: 'string', description: 'First parameter' },
            param2: { type: 'number', description: 'Second parameter' }
          },
          required: ['param1']
        }
      }
    ]
  }
})

// Handle tool calls
server.setRequestHandler('tools/call', async (request) => {
  const { name, arguments: args } = request.params
  
  if (name === 'my_tool') {
    // Implement tool logic
    const result = await doSomething(args)
    
    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify(result)
        }
      ]
    }
  }
  
  throw new Error(`Unknown tool: ${name}`)
})

// List available resources
server.setRequestHandler('resources/list', async () => {
  return {
    resources: [
      {
        uri: 'myscheme://resource',
        name: 'My Resource',
        description: 'Description of this resource',
        mimeType: 'application/json'
      }
    ]
  }
})

// Handle resource reads
server.setRequestHandler('resources/read', async (request) => {
  const { uri } = request.params
  
  if (uri === 'myscheme://resource') {
    const data = await fetchData()
    
    return {
      contents: [
        {
          uri,
          mimeType: 'application/json',
          text: JSON.stringify(data)
        }
      ]
    }
  }
  
  throw new Error(`Unknown resource: ${uri}`)
})

const transport = new StdioServerTransport()
await server.connect(transport)
```

## Best Practices

### Do's
✅ Define clear tool schemas
✅ Validate input parameters
✅ Handle errors gracefully
✅ Use appropriate MIME types
✅ Document tool capabilities
✅ Test with real data

### Don'ts
❌ Expose sensitive credentials
❌ Skip input validation
❌ Return unstructured data
❌ Ignore error handling
❌ Create overly complex tools
❌ Mix concerns in single server

## Trade-offs

| Ưu điểm | Nhược điểm |
|---------|------------|
| Extensible capabilities | Setup complexity |
| Standardized protocol | Requires server development |
| Real-time data access | Performance overhead |
| Reusable across tools | Debugging challenges |

## Related Patterns
- [Tool Use Sequencing](./pattern-tool-use-sequencing.md)
- [API Integration Strategy](../../2-planning/templates/api-integration-strategy.md)
