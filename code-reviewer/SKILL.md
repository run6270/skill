---
name: Code Reviewer
description: Performs thorough code review focusing on code quality, potential bugs, security issues, and best practices. Use this when the user asks to review code, check for issues, or perform code analysis.
allowed-tools: Read, Grep, Glob
---

# Code Reviewer Skill

This skill helps you perform comprehensive code reviews.

## What to Check

1. **Code Quality**
   - Code readability and maintainability
   - Proper naming conventions
   - Code organization and structure
   - DRY (Don't Repeat Yourself) principle

2. **Potential Bugs**
   - Logic errors
   - Edge cases handling
   - Null/undefined checks
   - Off-by-one errors

3. **Security Issues**
   - Input validation
   - SQL injection vulnerabilities
   - XSS vulnerabilities
   - Authentication/authorization issues
   - Sensitive data exposure

4. **Best Practices**
   - Error handling
   - Resource management
   - Performance considerations
   - Documentation and comments

## Review Process

1. Read the code files specified by the user
2. Analyze the code systematically
3. Provide specific feedback with line numbers
4. Suggest improvements with code examples
5. Prioritize issues by severity (Critical, High, Medium, Low)

## Output Format

Provide feedback in this structure:
- **Summary**: Brief overview of the code
- **Issues Found**: List issues by severity
- **Recommendations**: Specific actionable suggestions
- **Good Practices**: Highlight what's done well
