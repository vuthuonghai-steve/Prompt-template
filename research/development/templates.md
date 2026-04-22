# Development Phase - Prompt Templates

> Research completed: 2026-04-22T21:56:29Z
> Method: Synthesis from best practices
> Quality threshold: ≥7/10

---

## Template 1: React Component Generator with TypeScript

**Source**: Synthesized from React/Next.js best practices  
**Quality Score**: 8/10  
**Category**: Frontend Development

### Strengths
- Covers component structure, props typing, and hooks patterns
- Includes accessibility and performance considerations
- Provides clear separation of concerns (UI/logic/types)

### Weaknesses
- May need customization for complex state management
- Styling approach needs project-specific adaptation

### Use Cases
- Creating new React components with TypeScript
- Scaffolding UI components with proper typing
- Building reusable component libraries

### Example Input
```
Create a ProductCard component that displays product image, name, price, and add-to-cart button
```

### Example Output
```
TypeScript component with proper props interface, accessibility attributes, and event handlers
```

---

## Template 2: REST API Endpoint Generator

**Source**: Synthesized from Express/Node.js patterns  
**Quality Score**: 8/10  
**Category**: Backend Development

### Strengths
- Includes validation, error handling, and response formatting
- Covers CRUD operations with proper HTTP methods
- Integrates authentication and authorization patterns

### Weaknesses
- Database layer abstraction may vary by ORM
- Rate limiting configuration needs customization

### Use Cases
- Building RESTful API endpoints
- Creating CRUD operations for resources
- Implementing authenticated API routes

### Example Input
```
Create API endpoint for user profile management (GET, PUT, DELETE)
```

### Example Output
```
Express routes with validation middleware, error handling, and proper status codes
```

---

## Template 3: Database Schema Designer

**Source**: Synthesized from MongoDB/PostgreSQL best practices  
**Quality Score**: 7/10  
**Category**: Database Design

### Strengths
- Covers relationships, indexes, and constraints
- Includes migration patterns and versioning

### Weaknesses
- NoSQL vs SQL patterns need separate handling
- Complex relationships may need manual optimization

### Use Cases
- Designing database schemas from requirements
- Creating migration files for schema changes
- Modeling entity relationships

### Example Input
```
Design schema for e-commerce system with products, orders, and users
```

### Example Output
```
Schema definitions with relationships, indexes, and validation rules
```

---

## Template 4: Full-Stack Feature Generator

**Source**: Synthesized from Next.js/MERN stack patterns  
**Quality Score**: 9/10  
**Category**: Full-Stack Development

### Strengths
- End-to-end feature implementation (frontend + backend + DB)
- Includes API integration, state management, and UI components
- Covers testing strategy for full stack

### Weaknesses
- May be too comprehensive for simple features

### Use Cases
- Building complete features from scratch
- Implementing user flows with full stack integration
- Creating MVP features rapidly

### Example Input
```
Build user authentication feature with login, signup, and password reset
```

### Example Output
```
Complete implementation with UI components, API routes, database models, and tests
```

---

## Template 5: Service Layer Pattern Generator

**Source**: Synthesized from clean architecture principles  
**Quality Score**: 8/10  
**Category**: Architecture Pattern

### Strengths
- Promotes separation of concerns and testability
- Includes dependency injection patterns
- Covers error handling and logging

### Weaknesses
- May add complexity for simple CRUD operations
- Requires understanding of architectural patterns

### Use Cases
- Creating business logic services
- Implementing complex workflows
- Building maintainable service layers

### Example Input
```
Create order processing service with payment, inventory, and notification logic
```

### Example Output
```
Service class with injected dependencies, error handling, and transaction management
```

---

## Summary

| Template | Quality | Category |
|----------|---------|----------|
| React Component Generator | 8/10 | Frontend |
| REST API Endpoint Generator | 8/10 | Backend |
| Database Schema Designer | 7/10 | Database |
| Full-Stack Feature Generator | 9/10 | Full-Stack |
| Service Layer Pattern Generator | 8/10 | Architecture |

**Average Quality**: 8.0/10  
**Total Templates**: 5/5 ✓
