---
name: API Documentation Generator
description: Generates comprehensive API documentation from code. Use when user asks to document APIs, create API docs, or generate OpenAPI/Swagger documentation.
---

# API Documentation Generator

This skill helps generate detailed API documentation from your codebase.

## What to Document

1. **Endpoints**
   - HTTP method (GET, POST, PUT, DELETE, etc.)
   - URL path and parameters
   - Query parameters
   - Request body schema
   - Response schema
   - Status codes

2. **Authentication**
   - Authentication methods
   - Required headers
   - Token format

3. **Examples**
   - Sample requests
   - Sample responses
   - Error responses

4. **Models/Schemas**
   - Data structures
   - Field types
   - Validation rules
   - Relationships

## Output Format

Generate documentation in one of these formats:
- **Markdown**: Human-readable documentation
- **OpenAPI 3.0**: Industry standard API specification
- **Postman Collection**: For API testing

## Process

1. Scan the codebase for API route definitions
2. Extract endpoint information
3. Identify request/response models
4. Generate examples from tests or code
5. Format documentation according to chosen format

## Example Output (Markdown)

```markdown
## POST /api/users

Create a new user account.

### Request Body
\`\`\`json
{
  "email": "user@example.com",
  "password": "secure_password",
  "name": "John Doe"
}
\`\`\`

### Response (201 Created)
\`\`\`json
{
  "id": "123",
  "email": "user@example.com",
  "name": "John Doe",
  "createdAt": "2025-01-15T10:30:00Z"
}
\`\`\`

### Errors
- `400 Bad Request`: Invalid input data
- `409 Conflict`: Email already exists
```
