---
name: dlp-scanner
description: Data Loss Prevention scanner - detects plaintext credentials, private keys, and sensitive data in Claude Code workspace
---

# DLP Scanner - Data Loss Prevention

Automated scanner to detect and prevent leakage of sensitive credentials, private keys, and confidential data.

## 🎯 Purpose

Prevent accidental exposure of:
- Private keys (Ethereum, Bitcoin, SSH)
- Mnemonic phrases (12/24 words)
- API keys and tokens
- Passwords and secrets
- Personal Identifiable Information (PII)

## 🔍 Detection Patterns

### Cryptocurrency Private Keys

#### Ethereum Private Key
```regex
# 64 hex characters (with or without 0x prefix)
0x[a-fA-F0-9]{64}
[a-fA-F0-9]{64}
```

#### Bitcoin Private Key (WIF Format)
```regex
# Mainnet: starts with 5, K, or L
[5KL][1-9A-HJ-NP-Za-km-z]{50,51}

# Testnet: starts with 9 or c
[9c][1-9A-HJ-NP-Za-km-z]{50,51}
```

#### Solana Private Key
```regex
# Base58 encoded, typically 88 characters
[1-9A-HJ-NP-Za-km-z]{87,88}
```

### Mnemonic Phrases

#### 12-Word Mnemonic
```regex
\b([a-z]{3,8}\s+){11}[a-z]{3,8}\b
```

#### 24-Word Mnemonic
```regex
\b([a-z]{3,8}\s+){23}[a-z]{3,8}\b
```

### API Keys & Tokens

#### OpenAI API Key
```regex
sk-[a-zA-Z0-9]{48}
sk-proj-[a-zA-Z0-9]{48}
```

#### Anthropic API Key
```regex
sk-ant-[a-zA-Z0-9-]{95,}
```

#### AWS Access Key
```regex
AKIA[0-9A-Z]{16}
```

#### AWS Secret Key
```regex
[a-zA-Z0-9/+=]{40}
```

#### GitHub Token
```regex
ghp_[a-zA-Z0-9]{36}
gho_[a-zA-Z0-9]{36}
ghs_[a-zA-Z0-9]{36}
```

#### Google API Key
```regex
AIza[0-9A-Za-z_-]{35}
```

#### Stripe API Key
```regex
sk_live_[0-9a-zA-Z]{24,}
pk_live_[0-9a-zA-Z]{24,}
```

### SSH Keys

#### SSH Private Key
```regex
-----BEGIN.*PRIVATE KEY-----
-----BEGIN RSA PRIVATE KEY-----
-----BEGIN OPENSSH PRIVATE KEY-----
-----BEGIN EC PRIVATE KEY-----
```

### Generic Secrets

#### Generic API Key Pattern
```regex
[aA][pP][iI]_?[kK][eE][yY].*['\"]([0-9a-zA-Z]{32,})['\"]
```

#### Generic Secret Pattern
```regex
[sS][eE][cC][rR][eE][tT].*['\"]([0-9a-zA-Z]{32,})['\"]
```

#### Generic Token Pattern
```regex
[tT][oO][kK][eE][nN].*['\"]([0-9a-zA-Z]{32,})['\"]
```

#### Password in Code
```regex
[pP][aA][sS][sS][wW][oO][rR][dD].*['\"]([^'\"]{8,})['\"]
```

## 📂 Scan Locations

### High Priority (Always Scan)
- `~/.claude/projects/*/memory/` - Conversation memory
- `~/.claude/workspace/` - Working files
- `~/.claude/logs/` - Log files
- `~/.claude/agents/*/sessions/` - Agent session data

### Medium Priority (Scan if Suspicious)
- `~/.claude/skills/` - Installed skills
- `~/.claude/mcp/` - MCP server configurations
- `~/.claude/cron/` - Scheduled task definitions

### Low Priority (Scan on Demand)
- `~/.claude/completions/` - Shell completions
- `~/.claude/canvas/` - Canvas artifacts

## 🚨 Alert Levels

### CRITICAL - Immediate Action Required
- **Private keys found**: Ethereum, Bitcoin, SSH private keys
- **Mnemonic phrases found**: 12/24-word seed phrases
- **Live API keys found**: OpenAI, Anthropic, AWS keys

**Action**:
1. Immediately rotate compromised credentials
2. Clear from memory/logs
3. Review access logs for unauthorized usage
4. Notify security team if applicable

### HIGH - Review Within 1 Hour
- **Generic secrets found**: Tokens, passwords in plaintext
- **Suspicious patterns**: Base64 encoded credentials
- **Multiple credential types**: Indicates potential data dump

**Action**:
1. Verify if credentials are legitimate
2. Move to secure storage (environment variables, vault)
3. Remove from files
4. Update documentation

### MEDIUM - Review Within 24 Hours
- **Test/dummy credentials**: Fake keys for testing
- **Expired credentials**: Old API keys
- **Public tokens**: Non-sensitive tokens

**Action**:
1. Verify credentials are not real
2. Add comments indicating test data
3. Consider using placeholder patterns

### LOW - Informational
- **False positives**: Hex strings that look like keys
- **Documentation examples**: Example keys in docs
- **Hashed values**: Already encrypted/hashed data

**Action**:
1. Review and confirm false positive
2. Add to whitelist if appropriate
3. No immediate action required

## 🔧 Scanner Implementation

### Scan Command
```bash
#!/bin/bash

# DLP Scanner for Claude Code
CLAUDE_DIR="${HOME}/.claude"
REPORT_FILE="${HOME}/.claude/security-reports/dlp-scan-$(date +%Y-%m-%d-%H%M%S).txt"

echo "🔍 DLP Scan Started - $(date)" > "${REPORT_FILE}"
echo "======================================" >> "${REPORT_FILE}"

# Function to scan for pattern
scan_pattern() {
    local pattern="$1"
    local description="$2"
    local severity="$3"

    echo "" >> "${REPORT_FILE}"
    echo "Scanning for: ${description} [${severity}]" >> "${REPORT_FILE}"

    results=$(grep -r -E "${pattern}" "${CLAUDE_DIR}/projects" "${CLAUDE_DIR}/workspace" 2>/dev/null)

    if [ -n "$results" ]; then
        echo "⚠️ FOUND:" >> "${REPORT_FILE}"
        echo "$results" >> "${REPORT_FILE}"
        return 1
    else
        echo "✅ None found" >> "${REPORT_FILE}"
        return 0
    fi
}

# Scan for various patterns
scan_pattern "0x[a-fA-F0-9]{64}" "Ethereum Private Key" "CRITICAL"
scan_pattern "[5KL][1-9A-HJ-NP-Za-km-z]{50,51}" "Bitcoin Private Key" "CRITICAL"
scan_pattern "\b([a-z]{3,8}\s+){11}[a-z]{3,8}\b" "12-Word Mnemonic" "CRITICAL"
scan_pattern "\b([a-z]{3,8}\s+){23}[a-z]{3,8}\b" "24-Word Mnemonic" "CRITICAL"
scan_pattern "sk-[a-zA-Z0-9]{48}" "OpenAI API Key" "CRITICAL"
scan_pattern "sk-ant-[a-zA-Z0-9-]{95,}" "Anthropic API Key" "CRITICAL"
scan_pattern "AKIA[0-9A-Z]{16}" "AWS Access Key" "CRITICAL"
scan_pattern "ghp_[a-zA-Z0-9]{36}" "GitHub Token" "HIGH"
scan_pattern "-----BEGIN.*PRIVATE KEY-----" "SSH Private Key" "CRITICAL"

echo "" >> "${REPORT_FILE}"
echo "✅ DLP Scan Completed - $(date)" >> "${REPORT_FILE}"

# Output summary
cat "${REPORT_FILE}"
```

### Usage

#### Manual Scan
```bash
# Run full scan
bash ~/.claude/workspace/scripts/dlp-scan.sh

# Scan specific directory
grep -r -E "0x[a-fA-F0-9]{64}" ~/.claude/projects/*/memory/

# Scan specific file
grep -E "sk-[a-zA-Z0-9]{48}" ~/.claude/workspace/file.txt
```

#### Automated Scan (via nightly-audit)
The DLP scanner is automatically invoked as part of the nightly security audit.

## 🛡️ Prevention Strategies

### 1. Environment Variables
Store credentials in environment variables, not files:
```bash
# .bashrc or .zshrc
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
```

### 2. Secret Management Tools
Use dedicated secret management:
- **1Password CLI**: `op read "op://vault/item/field"`
- **AWS Secrets Manager**: `aws secretsmanager get-secret-value`
- **HashiCorp Vault**: `vault kv get secret/api-key`

### 3. Git Hooks
Prevent commits with secrets:
```bash
# .git/hooks/pre-commit
#!/bin/bash
if git diff --cached | grep -E "sk-[a-zA-Z0-9]{48}"; then
    echo "⚠️ Potential API key detected in commit!"
    exit 1
fi
```

### 4. .gitignore Patterns
```
# .gitignore
.env
.env.local
*.key
*.pem
secrets.json
credentials.json
```

### 5. Memory Hygiene
Regularly clear sensitive data from memory:
```bash
# Clear old memory files
find ~/.claude/projects/*/memory/ -name "*.md" -mtime +30 -delete

# Sanitize memory files
sed -i 's/sk-[a-zA-Z0-9]\{48\}/[REDACTED]/g' ~/.claude/projects/*/memory/*.md
```

## 🔄 Whitelist Management

### Create Whitelist
For known false positives:
```bash
# ~/.claude/dlp-whitelist.txt
# Format: pattern|file_path|reason

0x1234567890abcdef|example.md|Documentation example
test-api-key-12345|test.sh|Test fixture
```

### Use Whitelist in Scan
```bash
# Modified scan function
scan_with_whitelist() {
    local pattern="$1"
    local results=$(grep -r -E "${pattern}" "${CLAUDE_DIR}")

    # Filter out whitelisted items
    while IFS='|' read -r wl_pattern wl_path wl_reason; do
        results=$(echo "$results" | grep -v "$wl_path")
    done < ~/.claude/dlp-whitelist.txt

    echo "$results"
}
```

## 📊 Reporting

### Scan Report Format
```markdown
🔍 DLP Scan Report - YYYY-MM-DD HH:MM:SS

## Summary
- Total files scanned: 1,234
- Patterns checked: 15
- Findings: 3 CRITICAL, 1 HIGH, 0 MEDIUM, 2 LOW

## CRITICAL Findings

### 1. Ethereum Private Key
- **File**: ~/.claude/projects/project-x/memory/2026-03-04.md
- **Line**: 42
- **Pattern**: 0x1234...abcd
- **Action**: ROTATE IMMEDIATELY

### 2. OpenAI API Key
- **File**: ~/.claude/workspace/test.py
- **Line**: 15
- **Pattern**: sk-proj-...
- **Action**: ROTATE IMMEDIATELY

## HIGH Findings

### 1. GitHub Token
- **File**: ~/.claude/logs/session.log
- **Line**: 89
- **Pattern**: ghp_...
- **Action**: Review and rotate if active

## Recommendations
1. Rotate all CRITICAL credentials immediately
2. Move credentials to environment variables
3. Clear sensitive data from memory files
4. Enable pre-commit hooks to prevent future leaks
```

## 🧪 Testing

### Test Cases

#### Test 1: Detect Ethereum Private Key
```bash
echo "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef" > /tmp/test-eth.txt
grep -E "0x[a-fA-F0-9]{64}" /tmp/test-eth.txt
# Expected: Match found
```

#### Test 2: Detect Mnemonic Phrase
```bash
echo "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about" > /tmp/test-mnemonic.txt
grep -E "\b([a-z]{3,8}\s+){11}[a-z]{3,8}\b" /tmp/test-mnemonic.txt
# Expected: Match found
```

#### Test 3: Detect API Key
```bash
echo "OPENAI_API_KEY=sk-proj-1234567890abcdefghijklmnopqrstuvwxyz123456" > /tmp/test-api.txt
grep -E "sk-proj-[a-zA-Z0-9]{48}" /tmp/test-api.txt
# Expected: Match found
```

#### Test 4: False Positive (Hex String)
```bash
echo "SHA256: a1b2c3d4e5f6" > /tmp/test-hash.txt
grep -E "0x[a-fA-F0-9]{64}" /tmp/test-hash.txt
# Expected: No match (not 64 chars)
```

## 📚 Integration

This skill integrates with:
- `security-framework` for red line definitions
- `nightly-audit` for automated scanning
- `skill-audit` for skill content scanning
- Git hooks for pre-commit validation

## ⚠️ Limitations

1. **Regex limitations**: Cannot detect all obfuscation techniques
2. **False positives**: May flag legitimate hex strings
3. **Performance**: Full scan can be slow on large workspaces
4. **Encrypted data**: Cannot scan encrypted files
5. **Binary files**: Cannot scan compiled binaries

## 🔐 Best Practices

1. **Never commit credentials**: Use environment variables
2. **Rotate regularly**: Change API keys every 90 days
3. **Use least privilege**: Grant minimum necessary permissions
4. **Monitor usage**: Track API key usage for anomalies
5. **Audit regularly**: Run DLP scans weekly
6. **Educate team**: Train on credential hygiene
7. **Use secret managers**: Centralize credential storage
