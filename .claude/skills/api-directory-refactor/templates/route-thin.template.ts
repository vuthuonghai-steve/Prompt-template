// Route Thin Template
// Template cho route.ts sau khi refactor (chi chua HTTP transport)

import { NextRequest, NextResponse } from 'next/server'
import { <action><Entity>Schema } from '../schemas/<action>-<entity>.schema'
import { <Action><Entity>Service } from '../services/<action>-<entity>.service'
import { getAuthUser } from '@/lib/auth'

export async function <METHOD>(request: NextRequest) {
  try {
    // 1. Parse & Validate
    const body = await request.<parseMethod>()
    const validated = <action><Entity>Schema.parse(body)

    // 2. Auth
    const user = await getAuthUser(request)
    if (!user) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    // 3. Execute Service
    const result = await <Action><Entity>Service.execute({
      ...validated,
      userId: user.id,
    })

    // 4. Response
    return NextResponse.json(result, { status: <STATUS> })
  } catch (error) {
    if (error.name === 'ZodError') {
      return NextResponse.json(
        { error: 'Validation failed', details: error.errors },
        { status: 400 }
      )
    }
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    )
  }
}

// Notes:
// - METHOD: GET, POST, PUT, DELETE, PATCH
// - parseMethod: json() for POST/PUT/PATCH, none for GET
// - STATUS: 200, 201, 204
