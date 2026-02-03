---
name: release-skills
description: Universal release workflow. Auto-detects version files and changelogs. Supports Node.js, Python, Rust, Claude Plugin, and generic projects. Use when user says "release", "发布", "new version", "bump version", "push", "推送".
---

# Release Skills

Universal release workflow supporting any project type with multi-language changelog.

## Quick Start

Just run `/release-skills` - auto-detects your project configuration.

## Supported Projects

| Project Type | Version File | Auto-Detected |
|--------------|--------------|---------------|
| Node.js | package.json | ✓ |
| Python | pyproject.toml | ✓ |
| Rust | Cargo.toml | ✓ |
| Claude Plugin | marketplace.json | ✓ |
| Generic | VERSION / version.txt | ✓ |

## Options

| Flag | Description |
|------|-------------|
| `--dry-run` | Preview changes without executing |
| `--major` | Force major version bump |
| `--minor` | Force minor version bump |
| `--patch` | Force patch version bump |

## Workflow

### Step 1: Detect Project Configuration

1. Check for `.releaserc.yml` (optional config override)
2. Auto-detect version file by scanning (priority order):
   - `package.json` (Node.js)
   - `pyproject.toml` (Python)
   - `Cargo.toml` (Rust)
   - `marketplace.json` or `.claude-plugin/marketplace.json` (Claude Plugin)
   - `VERSION` or `version.txt` (Generic)
3. Scan for changelog files using glob patterns:
   - `CHANGELOG*.md`
   - `HISTORY*.md`
   - `CHANGES*.md`
4. Identify language of each changelog by filename suffix
5. Display detected configuration

**Language Detection Rules**:

| Filename Pattern | Language |
|------------------|----------|
| `CHANGELOG.md` (no suffix) | en (default) |
| `CHANGELOG.zh.md` / `CHANGELOG_CN.md` / `CHANGELOG.zh-CN.md` | zh |
| `CHANGELOG.ja.md` / `CHANGELOG_JP.md` | ja |
| `CHANGELOG.ko.md` / `CHANGELOG_KR.md` | ko |
| `CHANGELOG.de.md` / `CHANGELOG_DE.md` | de |
| `CHANGELOG.fr.md` / `CHANGELOG_FR.md` | fr |
| `CHANGELOG.es.md` / `CHANGELOG_ES.md` | es |
| `CHANGELOG.{lang}.md` | Corresponding language code |

**Output Example**:
```
Project detected:
  Version file: package.json (1.2.3)
  Changelogs:
    - CHANGELOG.md (en)
    - CHANGELOG.zh.md (zh)
    - CHANGELOG.ja.md (ja)
```

### Step 2: Analyze Changes Since Last Tag

```bash
LAST_TAG=$(git tag --sort=-v:refname | head -1)
git log ${LAST_TAG}..HEAD --oneline
git diff ${LAST_TAG}..HEAD --stat
```

Categorize by conventional commit types:

| Type | Description |
|------|-------------|
| feat | New features |
| fix | Bug fixes |
| docs | Documentation |
| refactor | Code refactoring |
| perf | Performance improvements |
| test | Test changes |
| style | Formatting, styling |
| chore | Maintenance (skip in changelog) |

**Breaking Change Detection**:
- Commit message starts with `BREAKING CHANGE`
- Commit body/footer contains `BREAKING CHANGE:`
- Removed public APIs, renamed exports, changed interfaces

If breaking changes detected, warn user: "Breaking changes detected. Consider major version bump (--major flag)."

### Step 3: Determine Version Bump

Rules (in priority order):
1. User flag `--major/--minor/--patch` → Use specified
2. BREAKING CHANGE detected → Major bump (1.x.x → 2.0.0)
3. `feat:` commits present → Minor bump (1.2.x → 1.3.0)
4. Otherwise → Patch bump (1.2.3 → 1.2.4)

Display version change: `1.2.3 → 1.3.0`

### Step 4: Generate Multi-language Changelogs

For each detected changelog file:

1. **Identify language** from filename suffix
2. **Generate content in that language**:
   - Section titles in target language
   - Change descriptions written naturally in target language (not translated)
   - Date format: YYYY-MM-DD (universal)
3. **Insert at file head** (preserve existing content)

**Section Title Translations** (built-in):

| Type | en | zh | ja | ko | de | fr | es |
|------|----|----|----|----|----|----|-----|
| feat | Features | 新功能 | 新機能 | 새로운 기능 | Funktionen | Fonctionnalités | Características |
| fix | Fixes | 修复 | 修正 | 수정 | Fehlerbehebungen | Corrections | Correcciones |
| docs | Documentation | 文档 | ドキュメント | 문서 | Dokumentation | Documentation | Documentación |
| refactor | Refactor | 重构 | リファクタリング | 리팩토링 | Refactoring | Refactorisation | Refactorización |
| perf | Performance | 性能优化 | パフォーマンス | 성능 | Leistung | Performance | Rendimiento |
| breaking | Breaking Changes | 破坏性变更 | 破壊的変更 | 주요 변경사항 | Breaking Changes | Changements majeurs | Cambios importantes |

**Changelog Format**:

```markdown
## {VERSION} - {YYYY-MM-DD}

### Features
- Description of new feature

### Fixes
- Description of fix

### Documentation
- Description of docs changes
```

Only include sections that have changes. Omit empty sections.

**Multi-language Example**:

English (CHANGELOG.md):
```markdown
## 1.3.0 - 2026-01-22

### Features
- Add user authentication module
- Support OAuth2 login

### Fixes
- Fix memory leak in connection pool
```

Chinese (CHANGELOG.zh.md):
```markdown
## 1.3.0 - 2026-01-22

### 新功能
- 新增用户认证模块
- 支持 OAuth2 登录

### 修复
- 修复连接池内存泄漏问题
```

Japanese (CHANGELOG.ja.md):
```markdown
## 1.3.0 - 2026-01-22

### 新機能
- ユーザー認証モジュールを追加
- OAuth2 ログインをサポート

### 修正
- コネクションプールのメモリリークを修正
```

### Step 5: Check README Updates

**IMPORTANT**: Before updating version file, check if README needs updates.

1. **Scan for README files**: `README*.md` in project root
2. **For each skill/feature changed**, check if README documentation matches:
   - Options/flags documented correctly
   - Usage examples reflect current syntax
   - Feature descriptions are accurate
3. **If README is outdated**:
   - Update README.md (and README.zh.md if exists) to reflect changes
   - Include in release commit

**Common README Updates Needed**:
| Change Type | README Section to Check |
|-------------|------------------------|
| New options/flags | Options table, usage examples |
| Renamed options | Options table, usage examples |
| New features | Feature description, examples |
| Breaking changes | Migration notes, deprecation warnings |
| Restructured internals | Architecture section (if exposed to users) |

### Step 6: Update Version File

1. Read version file (JSON/TOML/text)
2. Update version number
3. Write back (preserve formatting)

**Version Paths by File Type**:

| File | Path |
|------|------|
| package.json | `$.version` |
| pyproject.toml | `project.version` |
| Cargo.toml | `package.version` |
| marketplace.json | `$.metadata.version` |
| VERSION / version.txt | Direct content |

### Step 7: Commit and Tag

```bash
git add <all modified files>
git commit -m "chore: release v{VERSION}"
git tag v{VERSION}
```

**Note**: Do NOT add Co-Authored-By line. This is a release commit, not a code contribution.

**Important**: Do NOT push to remote. User will push manually when ready.

**Post-Release Output**:
```
Release v1.3.0 created locally.

To publish:
  git push origin main
  git push origin v1.3.0
```

## Configuration (.releaserc.yml)

Optional config file in project root to override defaults:

```yaml
# .releaserc.yml - Optional configuration

# Version file (auto-detected if not specified)
version:
  file: package.json
  path: $.version  # JSONPath for JSON, dotted path for TOML

# Changelog files (auto-detected if not specified)
changelog:
  files:
    - path: CHANGELOG.md
      lang: en
    - path: CHANGELOG.zh.md
      lang: zh
    - path: CHANGELOG.ja.md
      lang: ja

  # Section mapping (conventional commit type → changelog section)
  # Use null to skip a type in changelog
  sections:
    feat: Features
    fix: Fixes
    docs: Documentation
    refactor: Refactor
    perf: Performance
    test: Tests
    chore: null

# Commit message format
commit:
  message: "chore: release v{version}"

# Tag format
tag:
  prefix: v  # Results in v1.0.0
  sign: false

# Additional files to include in release commit
include:
  - README.md
  - package.json
```

## Dry-Run Mode

When `--dry-run` is specified:

```
=== DRY RUN MODE ===

Project detected:
  Version file: package.json (1.2.3)
  Changelogs: CHANGELOG.md (en), CHANGELOG.zh.md (zh)

Last tag: v1.2.3
Proposed version: v1.3.0

Changes detected:
  feat: add user authentication
  feat: support oauth2 login
  fix: memory leak in pool

Changelog preview (en):
  ## 1.3.0 - 2026-01-22
  ### Features
  - Add user authentication module
  - Support OAuth2 login
  ### Fixes
  - Fix memory leak in connection pool

Changelog preview (zh):
  ## 1.3.0 - 2026-01-22
  ### 新功能
  - 新增用户认证模块
  - 支持 OAuth2 登录
  ### 修复
  - 修复连接池内存泄漏问题

Files to modify:
  - package.json
  - CHANGELOG.md
  - CHANGELOG.zh.md

No changes made. Run without --dry-run to execute.
```

## Example Usage

```
/release-skills              # Auto-detect version bump
/release-skills --dry-run    # Preview only
/release-skills --minor      # Force minor bump
/release-skills --patch      # Force patch bump
/release-skills --major      # Force major bump (with confirmation)
```

## When to Use

Trigger this skill when user requests:
- "release", "发布", "create release", "new version", "新版本"
- "bump version", "update version", "更新版本"
- "prepare release"
- "push to remote" (with uncommitted changes)

**Important**: If user says "just push" or "直接 push" with uncommitted changes, STILL follow all steps above first.
