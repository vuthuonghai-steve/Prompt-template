/**
 * API Integration Test: Products Endpoint
 * Framework: Vitest + Supertest
 * Context: E-commerce flower shop API
 */

import { describe, it, expect, beforeAll, afterAll } from 'vitest'
import request from 'supertest'
import { app } from '../src/app'
import { db } from '../src/lib/db'

describe('Products API - Integration Tests', () => {
  let authToken: string
  let testProductId: string

  beforeAll(async () => {
    // Setup: Login as admin to get auth token
    const loginRes = await request(app)
      .post('/api/v1/auth/login')
      .send({
        email: 'admin@siinstore.com',
        password: 'Test123!@#',
      })

    authToken = loginRes.body.data.accessToken
  })

  afterAll(async () => {
    // Cleanup: Delete test products
    if (testProductId) {
      await db.product.delete({ where: { id: testProductId } })
    }
  })

  describe('GET /api/v1/products', () => {
    it('should return paginated products list', async () => {
      const res = await request(app)
        .get('/api/v1/products')
        .query({ page: 1, limit: 10 })

      expect(res.status).toBe(200)
      expect(res.body).toMatchObject({
        success: true,
        data: {
          items: expect.any(Array),
          pagination: {
            page: 1,
            limit: 10,
            total: expect.any(Number),
            totalPages: expect.any(Number),
          },
        },
      })

      // Verify product structure
      const product = res.body.data.items[0]
      expect(product).toMatchObject({
        id: expect.any(String),
        name: expect.any(String),
        slug: expect.any(String),
        price: expect.any(Number),
        images: expect.any(Array),
        category: expect.objectContaining({
          id: expect.any(String),
          name: expect.any(String),
        }),
      })
    })

    it('should filter products by category', async () => {
      const res = await request(app)
        .get('/api/v1/products')
        .query({ categoryId: 'cat-roses' })

      expect(res.status).toBe(200)
      expect(res.body.success).toBe(true)

      // Verify all products belong to category
      res.body.data.items.forEach((product: any) => {
        expect(product.category.id).toBe('cat-roses')
      })
    })

    it('should filter products by occasion tag', async () => {
      const res = await request(app)
        .get('/api/v1/products')
        .query({ occasion: 'birthday' })

      expect(res.status).toBe(200)
      expect(res.body.success).toBe(true)

      // Verify all products have birthday tag
      res.body.data.items.forEach((product: any) => {
        const hasBirthdayTag = product.tags.some(
          (tag: any) => tag.slug === 'birthday'
        )
        expect(hasBirthdayTag).toBe(true)
      })
    })

    it('should filter products by price range', async () => {
      const minPrice = 200000
      const maxPrice = 500000

      const res = await request(app)
        .get('/api/v1/products')
        .query({ minPrice, maxPrice })

      expect(res.status).toBe(200)
      expect(res.body.success).toBe(true)

      // Verify all products within price range
      res.body.data.items.forEach((product: any) => {
        expect(product.price).toBeGreaterThanOrEqual(minPrice)
        expect(product.price).toBeLessThanOrEqual(maxPrice)
      })
    })

    it('should search products by name', async () => {
      const res = await request(app)
        .get('/api/v1/products')
        .query({ search: 'rose' })

      expect(res.status).toBe(200)
      expect(res.body.success).toBe(true)

      // Verify all products contain "rose" in name
      res.body.data.items.forEach((product: any) => {
        expect(product.name.toLowerCase()).toContain('rose')
      })
    })

    it('should sort products by price ascending', async () => {
      const res = await request(app)
        .get('/api/v1/products')
        .query({ sortBy: 'price', order: 'asc' })

      expect(res.status).toBe(200)
      expect(res.body.success).toBe(true)

      // Verify products sorted by price
      const prices = res.body.data.items.map((p: any) => p.price)
      const sortedPrices = [...prices].sort((a, b) => a - b)
      expect(prices).toEqual(sortedPrices)
    })

    it('should return 400 for invalid pagination params', async () => {
      const res = await request(app)
        .get('/api/v1/products')
        .query({ page: -1, limit: 0 })

      expect(res.status).toBe(400)
      expect(res.body.success).toBe(false)
      expect(res.body.error).toContain('Invalid pagination')
    })
  })

  describe('GET /api/v1/products/:id', () => {
    it('should return product details by ID', async () => {
      const res = await request(app)
        .get('/api/v1/products/prod-rose-bouquet')

      expect(res.status).toBe(200)
      expect(res.body).toMatchObject({
        success: true,
        data: {
          id: 'prod-rose-bouquet',
          name: expect.any(String),
          description: expect.any(String),
          price: expect.any(Number),
          stock: expect.any(Number),
          images: expect.any(Array),
          category: expect.any(Object),
          tags: expect.any(Array),
          occasions: expect.any(Array),
          ageRanges: expect.any(Array),
        },
      })
    })

    it('should return 404 for non-existent product', async () => {
      const res = await request(app)
        .get('/api/v1/products/non-existent-id')

      expect(res.status).toBe(404)
      expect(res.body.success).toBe(false)
      expect(res.body.error).toContain('Product not found')
    })
  })

  describe('POST /api/v1/products', () => {
    it('should create new product (admin only)', async () => {
      const newProduct = {
        name: 'Test Lily Bouquet',
        slug: 'test-lily-bouquet',
        description: 'Beautiful white lilies',
        price: 350000,
        stock: 50,
        categoryId: 'cat-lilies',
        images: [
          { url: 'https://cdn.siinstore.com/lily-1.jpg', alt: 'Lily bouquet' },
        ],
        tags: ['tag-elegant', 'tag-white'],
        occasions: ['occ-wedding'],
        ageRanges: ['age-adult'],
      }

      const res = await request(app)
        .post('/api/v1/products')
        .set('Authorization', `Bearer ${authToken}`)
        .send(newProduct)

      expect(res.status).toBe(201)
      expect(res.body).toMatchObject({
        success: true,
        data: {
          id: expect.any(String),
          name: 'Test Lily Bouquet',
          slug: 'test-lily-bouquet',
          price: 350000,
        },
      })

      testProductId = res.body.data.id
    })

    it('should return 401 without auth token', async () => {
      const res = await request(app)
        .post('/api/v1/products')
        .send({ name: 'Test Product' })

      expect(res.status).toBe(401)
      expect(res.body.success).toBe(false)
    })

    it('should return 400 for invalid product data', async () => {
      const invalidProduct = {
        name: '', // Empty name
        price: -100, // Negative price
      }

      const res = await request(app)
        .post('/api/v1/products')
        .set('Authorization', `Bearer ${authToken}`)
        .send(invalidProduct)

      expect(res.status).toBe(400)
      expect(res.body.success).toBe(false)
      expect(res.body.errors).toBeDefined()
    })

    it('should return 409 for duplicate slug', async () => {
      const duplicateProduct = {
        name: 'Another Rose Bouquet',
        slug: 'rose-bouquet', // Existing slug
        price: 300000,
      }

      const res = await request(app)
        .post('/api/v1/products')
        .set('Authorization', `Bearer ${authToken}`)
        .send(duplicateProduct)

      expect(res.status).toBe(409)
      expect(res.body.success).toBe(false)
      expect(res.body.error).toContain('already exists')
    })
  })

  describe('PUT /api/v1/products/:id', () => {
    it('should update product (admin only)', async () => {
      const updates = {
        name: 'Updated Rose Bouquet',
        price: 400000,
      }

      const res = await request(app)
        .put('/api/v1/products/prod-rose-bouquet')
        .set('Authorization', `Bearer ${authToken}`)
        .send(updates)

      expect(res.status).toBe(200)
      expect(res.body).toMatchObject({
        success: true,
        data: {
          id: 'prod-rose-bouquet',
          name: 'Updated Rose Bouquet',
          price: 400000,
        },
      })
    })

    it('should return 404 for non-existent product', async () => {
      const res = await request(app)
        .put('/api/v1/products/non-existent-id')
        .set('Authorization', `Bearer ${authToken}`)
        .send({ name: 'Updated Name' })

      expect(res.status).toBe(404)
      expect(res.body.success).toBe(false)
    })
  })

  describe('DELETE /api/v1/products/:id', () => {
    it('should soft delete product (admin only)', async () => {
      // Create product to delete
      const createRes = await request(app)
        .post('/api/v1/products')
        .set('Authorization', `Bearer ${authToken}`)
        .send({
          name: 'Product to Delete',
          slug: 'product-to-delete',
          price: 100000,
        })

      const productId = createRes.body.data.id

      // Delete product
      const deleteRes = await request(app)
        .delete(`/api/v1/products/${productId}`)
        .set('Authorization', `Bearer ${authToken}`)

      expect(deleteRes.status).toBe(200)
      expect(deleteRes.body.success).toBe(true)

      // Verify product not in list
      const listRes = await request(app).get('/api/v1/products')
      const deletedProduct = listRes.body.data.items.find(
        (p: any) => p.id === productId
      )
      expect(deletedProduct).toBeUndefined()
    })

    it('should return 404 for non-existent product', async () => {
      const res = await request(app)
        .delete('/api/v1/products/non-existent-id')
        .set('Authorization', `Bearer ${authToken}`)

      expect(res.status).toBe(404)
      expect(res.body.success).toBe(false)
    })
  })

  describe('GET /api/v1/products/:id/stock', () => {
    it('should return product stock availability', async () => {
      const res = await request(app)
        .get('/api/v1/products/prod-rose-bouquet/stock')

      expect(res.status).toBe(200)
      expect(res.body).toMatchObject({
        success: true,
        data: {
          productId: 'prod-rose-bouquet',
          stock: expect.any(Number),
          available: expect.any(Boolean),
          lowStock: expect.any(Boolean),
        },
      })
    })
  })

  describe('POST /api/v1/products/:id/stock', () => {
    it('should update product stock (admin only)', async () => {
      const res = await request(app)
        .post('/api/v1/products/prod-rose-bouquet/stock')
        .set('Authorization', `Bearer ${authToken}`)
        .send({ quantity: 100, operation: 'set' })

      expect(res.status).toBe(200)
      expect(res.body).toMatchObject({
        success: true,
        data: {
          stock: 100,
        },
      })
    })

    it('should increment stock', async () => {
      const res = await request(app)
        .post('/api/v1/products/prod-rose-bouquet/stock')
        .set('Authorization', `Bearer ${authToken}`)
        .send({ quantity: 10, operation: 'increment' })

      expect(res.status).toBe(200)
      expect(res.body.success).toBe(true)
    })

    it('should decrement stock', async () => {
      const res = await request(app)
        .post('/api/v1/products/prod-rose-bouquet/stock')
        .set('Authorization', `Bearer ${authToken}`)
        .send({ quantity: 5, operation: 'decrement' })

      expect(res.status).toBe(200)
      expect(res.body.success).toBe(true)
    })

    it('should return 400 for negative stock', async () => {
      const res = await request(app)
        .post('/api/v1/products/prod-rose-bouquet/stock')
        .set('Authorization', `Bearer ${authToken}`)
        .send({ quantity: -10, operation: 'set' })

      expect(res.status).toBe(400)
      expect(res.body.success).toBe(false)
    })
  })

  describe('GET /api/v1/products/featured', () => {
    it('should return featured products', async () => {
      const res = await request(app)
        .get('/api/v1/products/featured')

      expect(res.status).toBe(200)
      expect(res.body).toMatchObject({
        success: true,
        data: expect.any(Array),
      })

      // Verify all products are featured
      res.body.data.forEach((product: any) => {
        expect(product.featured).toBe(true)
      })
    })
  })

  describe('GET /api/v1/products/best-sellers', () => {
    it('should return best-selling products', async () => {
      const res = await request(app)
        .get('/api/v1/products/best-sellers')
        .query({ limit: 5 })

      expect(res.status).toBe(200)
      expect(res.body).toMatchObject({
        success: true,
        data: expect.any(Array),
      })

      expect(res.body.data.length).toBeLessThanOrEqual(5)

      // Verify sorted by sales count
      const salesCounts = res.body.data.map((p: any) => p.salesCount)
      const sortedSales = [...salesCounts].sort((a, b) => b - a)
      expect(salesCounts).toEqual(sortedSales)
    })
  })
})
