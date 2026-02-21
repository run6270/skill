---
name: reflect
description: Reviews the current conversation to extract learnings, identify improvement opportunities, and create or improve skills. Use after completing a task, when errors occurred, or when user asks to reflect on the session.
allowed-tools: Bash, Read, Write, Edit
---

# Reflect

Analyze the current conversation and extract actionable improvements.

## Step 1: Review the Conversation

Mentally scan the full conversation for:
- Tasks attempted and their outcomes
- Errors encountered and how they were resolved
- User corrections or feedback
- Repeated patterns (good or bad)
- Workflow inefficiencies

## Step 2: Categorize Findings

### Errors & Fixes
List each error with:
- What went wrong
- Root cause
- How it was resolved
- Whether it's likely to recur

### User Feedback
List explicit and implicit feedback:
- Corrections made by user
- Preferences revealed
- Frustrations expressed
- Approaches that worked well

### Workflow Patterns
Identify:
- Multi-step sequences that were repeated
- Tool combinations that worked well
- Approaches that were inefficient

## Step 3: Generate Improvement Actions

For each finding, determine the best action:

| Finding | Action |
|---------|--------|
| Recurring error pattern | Create/update a skill with the fix |
| User preference revealed | Save to MEMORY.md |
| Reusable workflow discovered | Create a new skill |
| Existing skill was wrong | Update the skill |
| CLAUDE.md instruction was unclear | Clarify the instruction |

## Step 4: Execute Improvements

For each action:

**Save to memory** (user preferences, project facts):
```bash
# Append to MEMORY.md
```

**Create new skill** (reusable workflow):
- Create `~/.claude/skills/[skill-name]/SKILL.md`
- Include: trigger conditions, step-by-step instructions, examples

**Update existing skill** (fix or improve):
- Read current skill
- Apply targeted improvements

## Step 5: Summary

Output a brief reflection:
```
## Session Reflection

### What went well
- [item]

### What could improve
- [item] → [action taken]

### Saved to memory
- [item]

### Skills created/updated
- [skill-name]: [what changed]
```
