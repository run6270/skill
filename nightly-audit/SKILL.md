---
name: nightly-audit
description: Automated nightly security audit for Claude Code - 13 core metrics with explicit reporting and Git backup
---

# Nightly Security Audit

Comprehensive automated security audit that runs every night at 03:00, covering 13 core metrics with explicit reporting.

## 🎯 Purpose

Detect security anomalies, configuration tampering, and credential leaks through systematic nightly audits.

## 📊 13 Core Metrics

### 1. Claude Code Security Audit
- Configuration integrity
- Permission settings
- Trust model validation

### 2. Process & Network Audit
- Listening ports (TCP + UDP)
- Top 15 high-resource processes
- Anomalous outbound connections

### 3. Sensitive Directory Changes
Files modified in last 24h:
- `~/.claude/`
- `~/.ssh/`
- `~/.gnupg/`
- `/etc/` (if accessible)

### 4. System Scheduled Tasks
- User crontab
- System cron jobs (`/etc/cron.d/`)
- Systemd timers
- User-level systemd units

### 5. Logins & SSH
- Recent login records
- Failed SSH attempts
- Suspicious login patterns

### 6. Critical File Integrity
- Hash baseline comparison
- Permission checks
- Configuration file validation

### 7. Yellow Line Operation Cross-Validation
- Compare `sudo` records in system logs
- Cross-check against memory logs
- Flag unrecorded operations

### 8. Disk Usage
- Overall usage rate (>85% alert)
- Large files added in last 24h (>100MB)
- Rapid growth detection

### 9. Environment Variables
- List variables containing KEY/TOKEN/SECRET/PASSWORD
- Compare against expected whitelist
- Detect new sensitive variables

### 10. Plaintext Credential Leak Scan (DLP)
Regex scan for:
- Ethereum/Bitcoin private keys
- 12/24-word mnemonic phrases
- API keys and tokens
- SSH private keys
- High-risk plaintext passwords

### 11. Skill/MCP Integrity
- List installed skills/MCPs
- Generate hash manifest
- Diff against previous baseline
- Flag any changes

### 12. Memory Audit
- Scan conversation history for sensitive data
- Check for credential leaks
- Validate memory size and growth

### 13. Git Backup
- Incremental commit of `.claude/` directory
- Push to private repository
- Verify backup success

## 🔍 DLP Scan Patterns

### Private Key Patterns
```regex
# Ethereum private key (64 hex chars)
0x[a-fA-F0-9]{64}

# Bitcoin WIF private key
[5KL][1-9A-HJ-NP-Za-km-z]{50,51}

# SSH private key header
-----BEGIN.*PRIVATE KEY-----

# Generic hex private key
[a-fA-F0-9]{64,}
```

### Mnemonic Patterns
```regex
# 12-word mnemonic
\b([a-z]+\s+){11}[a-z]+\b

# 24-word mnemonic
\b([a-z]+\s+){23}[a-z]+\b
```

### API Key Patterns
```regex
# OpenAI API key
sk-[a-zA-Z0-9]{48}

# Anthropic API key
sk-ant-[a-zA-Z0-9-]{95}

# AWS access key
AKIA[0-9A-Z]{16}

# GitHub token
ghp_[a-zA-Z0-9]{36}
```

## 📝 Audit Report Format

```markdown
🛡️ Claude Code Daily Security Audit Report (YYYY-MM-DD)

1. Platform Audit: ✅ Configuration validated
2. Process & Network: ✅ No anomalous connections
3. Directory Changes: ✅ 3 files modified (normal activity)
4. System Cron: ✅ No suspicious tasks found
5. Logins & SSH: ✅ 0 failed attempts
6. Config Baseline: ✅ Hash check passed
7. Yellow Line Audit: ✅ 2 sudo operations (verified)
8. Disk Capacity: ✅ Usage 45%, 0 large files
9. Environment Vars: ✅ No anomalous variables
10. Credential Scan: ✅ No plaintext leaks found
11. Skill Baseline: ✅ No unauthorized changes
12. Memory Audit: ✅ No sensitive data leaks
13. Git Backup: ✅ Pushed to private repo

📝 Detailed report: ~/.claude/security-reports/report-YYYY-MM-DD.txt
```

## 🚨 Alert Levels

### CRITICAL (Immediate Action Required)
- Plaintext private keys/mnemonics found
- Unauthorized configuration changes
- Suspicious network connections
- Unknown system tasks

### HIGH (Review Within 24h)
- Failed SSH brute-force attempts
- Large unexpected file additions
- New sensitive environment variables
- Skill/MCP integrity violations

### MEDIUM (Monitor)
- Disk usage >85%
- Unrecorded yellow line operations
- Minor configuration drifts

### LOW (Informational)
- Normal file modifications
- Expected cron jobs
- Routine system activity

## 🔧 Audit Script

The audit is implemented as a shell script at:
```
~/.claude/workspace/scripts/nightly-security-audit.sh
```

### Script Structure
```bash
#!/bin/bash

# Configuration
CLAUDE_DIR="${HOME}/.claude"
REPORT_DIR="${HOME}/.claude/security-reports"
BACKUP_REPO="git@github.com:username/claude-backup.git"
DATE=$(date +%Y-%m-%d)
REPORT_FILE="${REPORT_DIR}/report-${DATE}.txt"

# Create report directory
mkdir -p "${REPORT_DIR}"

# Initialize report
echo "🛡️ Claude Code Security Audit - ${DATE}" > "${REPORT_FILE}"
echo "========================================" >> "${REPORT_FILE}"

# 1. Platform Audit
echo "1. Platform Audit..." >> "${REPORT_FILE}"
# Check configuration integrity
# ...

# 2. Process & Network Audit
echo "2. Process & Network Audit..." >> "${REPORT_FILE}"
# List listening ports
ss -tlnp >> "${REPORT_FILE}" 2>&1
# ...

# [Continue for all 13 metrics]

# 13. Git Backup
echo "13. Git Backup..." >> "${REPORT_FILE}"
cd "${CLAUDE_DIR}"
git add -A
git commit -m "Automated backup - ${DATE}" || echo "No changes to commit"
git push origin main || echo "⚠️ Backup push failed"

# Generate summary
echo "" >> "${REPORT_FILE}"
echo "✅ Audit completed successfully" >> "${REPORT_FILE}"

# Output summary to stdout (for notification)
cat "${REPORT_FILE}"
```

## 📅 Cron Configuration

### Setup Instructions

1. Create the audit script:
```bash
mkdir -p ~/.claude/workspace/scripts
# Copy script content to ~/.claude/workspace/scripts/nightly-security-audit.sh
chmod +x ~/.claude/workspace/scripts/nightly-security-audit.sh
```

2. Test the script manually:
```bash
bash ~/.claude/workspace/scripts/nightly-security-audit.sh
```

3. Add to crontab:
```bash
crontab -e

# Add this line (runs at 3:00 AM daily)
0 3 * * * bash ~/.claude/workspace/scripts/nightly-security-audit.sh
```

### Alternative: Using Claude Code Cron (if available)
```bash
claude-code cron add \
  --name "nightly-security-audit" \
  --description "Nightly Security Audit" \
  --cron "0 3 * * *" \
  --command "bash ~/.claude/workspace/scripts/nightly-security-audit.sh"
```

## 🔔 Notification Options

### Option 1: Email
```bash
# Add to end of audit script
mail -s "Claude Code Security Audit - ${DATE}" user@example.com < "${REPORT_FILE}"
```

### Option 2: Telegram
```bash
# Add to end of audit script
TELEGRAM_BOT_TOKEN="your_bot_token"
TELEGRAM_CHAT_ID="your_chat_id"
MESSAGE=$(cat "${REPORT_FILE}")

curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
  -d "chat_id=${TELEGRAM_CHAT_ID}" \
  -d "text=${MESSAGE}"
```

### Option 3: Slack
```bash
# Add to end of audit script
SLACK_WEBHOOK="your_webhook_url"
MESSAGE=$(cat "${REPORT_FILE}")

curl -X POST "${SLACK_WEBHOOK}" \
  -H 'Content-Type: application/json' \
  -d "{\"text\": \"${MESSAGE}\"}"
```

## 🔐 Git Backup Configuration

### Setup Private Repository

1. Create private GitHub repository:
```bash
# On GitHub: Create new private repo "claude-backup"
```

2. Initialize Git in `.claude/` directory:
```bash
cd ~/.claude
git init
git remote add origin git@github.com:username/claude-backup.git
```

3. Create `.gitignore`:
```bash
cat > ~/.claude/.gitignore << 'EOF'
# Exclude large/temporary files
devices/*.tmp
media/
logs/
completions/
canvas/
*.bak*
*.tmp
EOF
```

4. Initial commit:
```bash
git add -A
git commit -m "Initial Claude Code backup"
git push -u origin main
```

## 📊 Baseline Generation

### First-Time Setup

Generate initial baselines:
```bash
# Configuration hash baseline
sha256sum ~/.claude/settings.json > ~/.claude/.config-baseline.sha256

# Skill/MCP baseline
find ~/.claude/skills -type f -exec sha256sum {} \; > ~/.claude/.skill-baseline.sha256
find ~/.claude/mcp -type f -exec sha256sum {} \; >> ~/.claude/.skill-baseline.sha256
```

## 🧪 Validation

### Test Audit Script
```bash
# Run manually
bash ~/.claude/workspace/scripts/nightly-security-audit.sh

# Check report
cat ~/.claude/security-reports/report-$(date +%Y-%m-%d).txt

# Verify all 13 metrics are present
grep -c "✅\|⚠️\|❌" ~/.claude/security-reports/report-$(date +%Y-%m-%d).txt
# Should output: 13
```

### Test DLP Scanner
```bash
# Create test file with fake private key
echo "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef" > /tmp/test-key.txt

# Run DLP scan
grep -r "0x[a-fA-F0-9]\{64\}" ~/.claude/

# Should detect the test pattern
```

## ⚠️ Known Limitations

1. **24-hour detection latency**: Audits run once daily
2. **Notification dependency**: Relies on external services (email/Telegram/Slack)
3. **Git push failures**: Network issues may prevent backup
4. **False positives**: DLP scanner may flag legitimate hex strings
5. **Performance impact**: Full directory scan may be slow on large installations

## 🔄 Maintenance

### Update Audit Script
```bash
# Edit script
vim ~/.claude/workspace/scripts/nightly-security-audit.sh

# Test changes
bash ~/.claude/workspace/scripts/nightly-security-audit.sh

# Verify cron still works
crontab -l
```

### Review Historical Reports
```bash
# List all reports
ls -lh ~/.claude/security-reports/

# View specific report
cat ~/.claude/security-reports/report-2026-03-01.txt

# Search for alerts
grep -r "⚠️\|❌" ~/.claude/security-reports/
```

## 📚 Integration

This skill integrates with:
- `security-framework` for red/yellow line definitions
- `skill-audit` for skill integrity checks
- `dlp-scanner` for credential leak detection
- Git for disaster recovery backup
