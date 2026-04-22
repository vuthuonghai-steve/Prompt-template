# Example: API Service Implementation

> **Context**: E-commerce flower shop
> **Service**: Product API with error handling, caching, retry logic
> **Stack**: TypeScript, Axios, React Query

---

## 📁 File Structure

```
src/
├── services/
│   └── product/
│       ├── service.product.ts          # Main service
│       ├── service.product.types.ts    # TypeScript types
│       └── service.product.cache.ts    # Cache layer
├── lib/
│   ├── api-client.ts                   # Axios instance
│   └── query-client.ts                 # React Query config
└── hooks/
    └── use-product/
        └── hook.use-product.ts         # React hook
```

---

## 💻 Implementation

### 1. API Client Setup

```typescript
// lib/api-client.ts
import axios, { AxiosError, AxiosRequestConfig } from 'axios'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3000/api'

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = localStorage.getItem('auth_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    
    // Add request ID for tracing
    config.headers['X-Request-ID'] = generateRequestId()
    
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
apiClient.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as AxiosRequestConfig & { _retry?: boolean }
    
    // Retry logic for 5xx errors
    if (
      error.response?.status &&
      error.response.status >= 500 &&
      !originalRequest._retry
    ) {
      originalRequest._retry = true
      
      // Wait before retry
      await new Promise((resolve) => setTimeout(resolve, 1000))
      
      return apiClient(originalRequest)
    }
    
    // Handle 401 - Unauthorized
    if (error.response?.status === 401) {
      // Clear auth and redirect to login
      localStorage.removeItem('auth_token')
      window.location.href = '/login'
    }
    
    return Promise.reject(error)
  }
)

function generateRequestId(): string {
  return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`
}
```

### 2. TypeScript Types

```typescript
// services/product/service.product.types.ts

export interface Product {
  id: string
  name: string
  description: string
  price: number
  image: string
  category: string
  tags: string[]
  inStock: boolean
  quantity: number
  rating: {
    average: number
    count: number
  }
  createdAt: string
  updatedAt: string
}

export interface ProductFilters {
  category?: string
  tags?: string[]
  minPrice?: number
  maxPrice?: number
  inStock?: boolean
  search?: string
  sortBy?: 'price' | 'name' | 'rating' | 'createdAt'
  sortOrder?: 'asc' | 'desc'
  page?: number
  limit?: number
}

export interface ProductListResponse {
  products: Product[]
  pagination: {
    page: number
    limit: number
    total: number
    totalPages: number
  }
}

export interface CreateProductData {
  name: string
  description: string
  price: number
  image: string
  category: string
  tags?: string[]
  quantity: number
}

export interface UpdateProductData extends Partial<CreateProductData> {
  id: string
}

export class ProductServiceError extends Error {
  constructor(
    message: string,
    public code: string,
    public statusCode?: number
  ) {
    super(message)
    this.name = 'ProductServiceError'
  }
}
```

### 3. Product Service

```typescript
// services/product/service.product.ts
import { apiClient } from '@/lib/api-client'
import {
  Product,
  ProductFilters,
  ProductListResponse,
  CreateProductData,
  UpdateProductData,
  ProductServiceError,
} from './service.product.types'

const ENDPOINTS = {
  LIST: '/products',
  DETAIL: (id: string) => `/products/${id}`,
  CREATE: '/products',
  UPDATE: (id: string) => `/products/${id}`,
  DELETE: (id: string) => `/products/${id}`,
  SEARCH: '/products/search',
}

export class ProductService {
  /**
   * Get list of products with filters
   */
  async getProducts(filters?: ProductFilters): Promise<ProductListResponse> {
    try {
      const params = this.buildQueryParams(filters)
      
      const response = await apiClient.get<ProductListResponse>(
        ENDPOINTS.LIST,
        { params }
      )
      
      return response.data
    } catch (error) {
      throw this.handleError(error, 'Failed to fetch products')
    }
  }
  
  /**
   * Get single product by ID
   */
  async getProduct(id: string): Promise<Product> {
    try {
      const response = await apiClient.get<Product>(ENDPOINTS.DETAIL(id))
      return response.data
    } catch (error) {
      throw this.handleError(error, `Failed to fetch product ${id}`)
    }
  }
  
  /**
   * Search products
   */
  async searchProducts(query: string): Promise<Product[]> {
    try {
      const response = await apiClient.get<Product[]>(ENDPOINTS.SEARCH, {
        params: { q: query },
      })
      return response.data
    } catch (error) {
      throw this.handleError(error, 'Failed to search products')
    }
  }
  
  /**
   * Create new product
   */
  async createProduct(data: CreateProductData): Promise<Product> {
    try {
      // Validate data
      this.validateProductData(data)
      
      const response = await apiClient.post<Product>(ENDPOINTS.CREATE, data)
      return response.data
    } catch (error) {
      throw this.handleError(error, 'Failed to create product')
    }
  }
  
  /**
   * Update existing product
   */
  async updateProduct(data: UpdateProductData): Promise<Product> {
    try {
      const { id, ...updateData } = data
      
      const response = await apiClient.patch<Product>(
        ENDPOINTS.UPDATE(id),
        updateData
      )
      return response.data
    } catch (error) {
      throw this.handleError(error, `Failed to update product ${data.id}`)
    }
  }
  
  /**
   * Delete product
   */
  async deleteProduct(id: string): Promise<void> {
    try {
      await apiClient.delete(ENDPOINTS.DELETE(id))
    } catch (error) {
      throw this.handleError(error, `Failed to delete product ${id}`)
    }
  }
  
  /**
   * Build query params from filters
   */
  private buildQueryParams(filters?: ProductFilters): Record<string, any> {
    if (!filters) return {}
    
    const params: Record<string, any> = {}
    
    if (filters.category) params.category = filters.category
    if (filters.tags?.length) params.tags = filters.tags.join(',')
    if (filters.minPrice) params.minPrice = filters.minPrice
    if (filters.maxPrice) params.maxPrice = filters.maxPrice
    if (filters.inStock !== undefined) params.inStock = filters.inStock
    if (filters.search) params.search = filters.search
    if (filters.sortBy) params.sortBy = filters.sortBy
    if (filters.sortOrder) params.sortOrder = filters.sortOrder
    if (filters.page) params.page = filters.page
    if (filters.limit) params.limit = filters.limit
    
    return params
  }
  
  /**
   * Validate product data
   */
  private validateProductData(data: CreateProductData): void {
    if (!data.name || data.name.trim().length === 0) {
      throw new ProductServiceError(
        'Product name is required',
        'VALIDATION_ERROR'
      )
    }
    
    if (data.price <= 0) {
      throw new ProductServiceError(
        'Product price must be greater than 0',
        'VALIDATION_ERROR'
      )
    }
    
    if (data.quantity < 0) {
      throw new ProductServiceError(
        'Product quantity cannot be negative',
        'VALIDATION_ERROR'
      )
    }
  }
  
  /**
   * Handle API errors
   */
  private handleError(error: any, defaultMessage: string): ProductServiceError {
    if (error instanceof ProductServiceError) {
      return error
    }
    
    if (error.response) {
      // Server responded with error
      const statusCode = error.response.status
      const message = error.response.data?.message || defaultMessage
      
      return new ProductServiceError(
        message,
        `HTTP_${statusCode}`,
        statusCode
      )
    }
    
    if (error.request) {
      // Request made but no response
      return new ProductServiceError(
        'Network error - please check your connection',
        'NETWORK_ERROR'
      )
    }
    
    // Something else happened
    return new ProductServiceError(
      error.message || defaultMessage,
      'UNKNOWN_ERROR'
    )
  }
}

// Export singleton instance
export const productService = new ProductService()
```

### 4. React Hook with React Query

```typescript
// hooks/use-product/hook.use-product.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { productService } from '@/services/product/service.product'
import type {
  Product,
  ProductFilters,
  CreateProductData,
  UpdateProductData,
} from '@/services/product/service.product.types'

const QUERY_KEYS = {
  products: (filters?: ProductFilters) => ['products', filters],
  product: (id: string) => ['product', id],
  search: (query: string) => ['products', 'search', query],
}

/**
 * Hook to fetch products list
 */
export function useProducts(filters?: ProductFilters) {
  return useQuery({
    queryKey: QUERY_KEYS.products(filters),
    queryFn: () => productService.getProducts(filters),
    staleTime: 5 * 60 * 1000, // 5 minutes
    gcTime: 10 * 60 * 1000, // 10 minutes
  })
}

/**
 * Hook to fetch single product
 */
export function useProduct(id: string) {
  return useQuery({
    queryKey: QUERY_KEYS.product(id),
    queryFn: () => productService.getProduct(id),
    enabled: !!id,
    staleTime: 5 * 60 * 1000,
  })
}

/**
 * Hook to search products
 */
export function useProductSearch(query: string) {
  return useQuery({
    queryKey: QUERY_KEYS.search(query),
    queryFn: () => productService.searchProducts(query),
    enabled: query.length >= 2,
    staleTime: 2 * 60 * 1000, // 2 minutes
  })
}

/**
 * Hook to create product
 */
export function useCreateProduct() {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: (data: CreateProductData) =>
      productService.createProduct(data),
    onSuccess: () => {
      // Invalidate products list
      queryClient.invalidateQueries({ queryKey: ['products'] })
    },
  })
}

/**
 * Hook to update product
 */
export function useUpdateProduct() {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: (data: UpdateProductData) =>
      productService.updateProduct(data),
    onSuccess: (updatedProduct) => {
      // Update cache for this product
      queryClient.setQueryData(
        QUERY_KEYS.product(updatedProduct.id),
        updatedProduct
      )
      
      // Invalidate products list
      queryClient.invalidateQueries({ queryKey: ['products'] })
    },
  })
}

/**
 * Hook to delete product
 */
export function useDeleteProduct() {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: (id: string) => productService.deleteProduct(id),
    onSuccess: (_, deletedId) => {
      // Remove from cache
      queryClient.removeQueries({ queryKey: QUERY_KEYS.product(deletedId) })
      
      // Invalidate products list
      queryClient.invalidateQueries({ queryKey: ['products'] })
    },
  })
}
```

---

## 🎯 Usage Examples

### Component: Product List

```typescript
// components/ProductList.tsx
import { useProducts } from '@/hooks/use-product/hook.use-product'
import { ProductCard } from './ProductCard'

export function ProductList() {
  const { data, isLoading, error } = useProducts({
    category: 'roses',
    inStock: true,
    sortBy: 'price',
    sortOrder: 'asc',
  })
  
  if (isLoading) {
    return <div>Loading products...</div>
  }
  
  if (error) {
    return <div>Error: {error.message}</div>
  }
  
  return (
    <div className="product-grid">
      {data?.products.map((product) => (
        <ProductCard key={product.id} product={product} />
      ))}
    </div>
  )
}
```

### Component: Product Detail

```typescript
// components/ProductDetail.tsx
import { useProduct } from '@/hooks/use-product/hook.use-product'

export function ProductDetail({ productId }: { productId: string }) {
  const { data: product, isLoading, error } = useProduct(productId)
  
  if (isLoading) return <div>Loading...</div>
  if (error) return <div>Error: {error.message}</div>
  if (!product) return <div>Product not found</div>
  
  return (
    <div>
      <h1>{product.name}</h1>
      <img src={product.image} alt={product.name} />
      <p>{product.description}</p>
      <p className="price">{formatPrice(product.price)}</p>
      <button>Add to Cart</button>
    </div>
  )
}
```

### Component: Create Product Form

```typescript
// components/CreateProductForm.tsx
import { useCreateProduct } from '@/hooks/use-product/hook.use-product'
import { useState } from 'react'

export function CreateProductForm() {
  const createProduct = useCreateProduct()
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    price: 0,
    image: '',
    category: '',
    quantity: 0,
  })
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    try {
      await createProduct.mutateAsync(formData)
      alert('Product created successfully!')
      // Reset form
      setFormData({
        name: '',
        description: '',
        price: 0,
        image: '',
        category: '',
        quantity: 0,
      })
    } catch (error) {
      alert(`Error: ${error.message}`)
    }
  }
  
  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Product name"
        value={formData.name}
        onChange={(e) => setFormData({ ...formData, name: e.target.value })}
      />
      
      <textarea
        placeholder="Description"
        value={formData.description}
        onChange={(e) =>
          setFormData({ ...formData, description: e.target.value })
        }
      />
      
      <input
        type="number"
        placeholder="Price"
        value={formData.price}
        onChange={(e) =>
          setFormData({ ...formData, price: Number(e.target.value) })
        }
      />
      
      <button type="submit" disabled={createProduct.isPending}>
        {createProduct.isPending ? 'Creating...' : 'Create Product'}
      </button>
    </form>
  )
}
```

---

## ✅ Best Practices Demonstrated

### 1. Error Handling
- Custom error class
- Retry logic for 5xx errors
- User-friendly error messages
- Network error detection

### 2. Type Safety
- Full TypeScript coverage
- Interface definitions
- Type guards

### 3. Caching
- React Query for automatic caching
- Stale time configuration
- Cache invalidation

### 4. Performance
- Request deduplication
- Optimistic updates
- Lazy loading

### 5. Developer Experience
- Clear method names
- JSDoc comments
- Consistent patterns
- Easy to test
