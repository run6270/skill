---
name: Git Commit Helper
description: Helps generate meaningful git commit messages following conventional commit format. Use when user asks to create a commit, write a commit message, or commit changes.
allowed-tools: Bash, Read
---

# Git Commit Helper Skill

This skill helps you create well-formatted git commit messages following the Conventional Commits specification.

## Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

## Types
- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, missing semi-colons, etc)
- **refactor**: Code refactoring
- **perf**: Performance improvements
- **test**: Adding or modifying tests
- **chore**: Build process or auxiliary tool changes

## Process

1. Run `git status` to see changed files
2. Run `git diff` to see the actual changes
3. Analyze the changes to understand what was modified
4. Generate a commit message with:
   - Appropriate type
   - Optional scope (file/module affected)
   - Clear, concise subject (50 chars max)
   - Detailed body if needed
   - References to issues if applicable

## Example

```
feat(user-auth): add password reset functionality

Implement email-based password reset flow with:
- Password reset token generation
- Email notification system
- Secure token validation
- New password update

Fixes #123
```

## Guidelines

- Use imperative mood ("add" not "added" or "adds")
- Don't capitalize first letter of subject
- No period at the end of subject
- Wrap body at 72 characters
- Explain what and why, not how
