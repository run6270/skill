---
name: Codex-audit
description: Audits all AGENTS.md files for redundancy, verbosity, and optimization opportunities. Use when user asks to audit AGENTS.md, clean up instructions, or optimize Codex configuration.
allowed-tools: Bash, Read, Glob
---

# Codex Audit

Read and audit all AGENTS.md files in the system.

## Step 1: Discover All AGENTS.md Files

```bash
# Global
cat ~/.Codex/AGENTS.md

# Global rules
ls ~/.Codex/rules/

# Project-level
find . -name "AGENTS.md" -not -path "*/node_modules/*" 2>/dev/null

# Memory
cat ~/.Codex/projects/*/memory/MEMORY.md 2>/dev/null
```

## Step 2: Read All Files

Read each discovered file completely.

## Step 3: Audit Each File

### Check for Redundant Instructions
- Instructions that duplicate default Codex behavior
- Instructions repeated across multiple files
- Instructions that contradict each other

### Check for Verbosity
- Long explanations that could be one line
- Examples that aren't necessary
- Sections that could be merged

### Check for Misplaced Content
- Content that belongs in a skill instead of AGENTS.md
- Content that belongs in MEMORY.md instead of AGENTS.md
- Project-specific content in global files

### Check for Stale Content
- References to deprecated tools or APIs
- Instructions for workflows no longer used
- Outdated model names or endpoints

## Step 4: Output Report

```
## [file-path]

### Redundant Instructions
- Line X: "[instruction]" → Already default behavior / duplicates [other file]

### Verbose Sections
- Section "[name]": Could be condensed from N lines to: "[suggested replacement]"

### Misplaced Content
- "[content]" → Should be in [skill/memory/other file]

### Stale Content
- "[content]" → Outdated because [reason]

### Suggested Rewrite
[condensed version of the file]
```

## Step 5: Summary

- Total files audited
- Estimated token savings if suggestions applied
- Priority order for cleanup
- Specific merge/move recommendations
