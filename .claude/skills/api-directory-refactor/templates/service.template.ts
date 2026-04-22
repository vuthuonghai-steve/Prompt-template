// Service Template
// Template cho service file sau khi refactor

import { <Entity>Repository } from '@/services/<entity>-repository'
import type { <Action><Entity>DTO } from '../types/<action>-<entity>.dto'

export class <Action><Entity>Service {
  static async execute(data: <Action><Entity>DTO & { userId: string }) {
    // 1. Validate business rules
    // const isValid = await this.validate(data)
    // if (!isValid) throw new Error('Validation failed')

    // 2. Call repository
    const result = await <Entity>Repository.<action>({
      ...data,
      createdBy: data.userId,
    })

    // 3. Return result
    return result
  }

  // Private validation methods
  // private static async validate(data: <Action><Entity>DTO) { ... }
}
