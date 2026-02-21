---
name: skills-audit
description: Audits all installed Claude Code skills (project-level and global) for quality issues. Use when user asks to audit skills, review skill quality, or check for redundancy.
allowed-tools: Bash, Read, Glob
---

# Skills Audit

List and audit all installed skills for quality issues.

## Step 1: Discover All Skills

```bash
# Global skills
ls ~/.claude/skills/

# Project skills (if in a project)
ls .claude/skills/ 2>/dev/null || echo "(no project skills)"
```

## Step 2: Present Skill List to User

Show the user all discovered skills and ask which to audit:
- All skills
- Specific skill(s) by name
- Skills matching a pattern

## Step 3: Audit Each Selected Skill

For each skill, read its SKILL.md and evaluate:

### Conciseness (0-10)
- Is the skill free of unnecessary verbosity?
- Are instructions direct and actionable?
- No redundant explanations?

### Clarity (0-10)
- Is the trigger condition unambiguous?
- Are steps clearly ordered?
- Would a new user understand when to use it?

### Scope (0-10)
- Is the scope well-defined (not too broad, not too narrow)?
- Does it overlap significantly with other skills?
- Single responsibility principle?

### Token Efficiency (0-10)
- Could the same instructions be expressed in fewer tokens?
- Are there repetitive sections that could be condensed?
- Is the `allowed-tools` list minimal and accurate?

## Step 4: Output Report

For each audited skill:

```
## [skill-name]
- Conciseness: X/10
- Clarity: X/10
- Scope: X/10
- Token Efficiency: X/10
- Overlaps with: [other skills if any]
- Issues: [specific problems]
- Suggestions: [concrete improvements]
```

## Step 5: Summary

- Total skills audited
- Average scores
- Top 3 skills needing improvement
- Skills with significant overlap (candidates for merging)
