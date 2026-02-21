---
name: evmbench
description: Fully automated smart contract security audit. Give a file path or directory → automatically reads all Solidity contracts, runs EVMbench-style vulnerability detection, generates patch suggestions, and outputs a structured security report. No manual steps required. Triggers on "audit contract", "smart contract vulnerability", "evmbench", "solidity security", "check my contract".
allowed-tools: Bash, Read, Glob, Write, Edit
---

# EVMbench Automated Smart Contract Audit

**Zero manual steps.** User provides a path → full audit runs automatically.

---

## Step 1: Resolve Target

Extract the path from user input. If not provided, ask once:
> "Please provide the path to your contract file or directory."

Supported input types:
- **Directory path** - scans recursively
- **Single file** - any supported extension
- **GitHub URL** - clone first, then scan
- **Zip file** - extract first, then scan

Supported smart contract languages:
| Extension | Language | Notes |
|-----------|----------|-------|
| `.sol` | Solidity | Most common EVM language |
| `.vy` | Vyper | Python-like, common in DeFi |
| `.yul` | Yul | EVM intermediate language |
| `.huff` | Huff | Low-level EVM assembly |
| `.fe` | Fe | Rust-like EVM language |

```bash
# If directory: find all contract files (all supported languages)
find <path> \( -name "*.sol" -o -name "*.vy" -o -name "*.yul" -o -name "*.huff" -o -name "*.fe" \) \
  -not -path "*/node_modules/*" \
  -not -path "*/lib/*" \
  -not -path "*/test/*" \
  -not -path "*/.git/*"

# If GitHub URL:
git clone <url> /tmp/evmbench-target && find /tmp/evmbench-target ...

# If single file: use directly
```

---

## Step 2: Read All Contracts

Read every contract file found. For each file, note:
- Contract name(s)
- Solidity version pragma
- Imports and dependencies
- Key functions (especially payable, external, public)

---

## Step 3: Automated Vulnerability Detection (Detect Mode)

Detect language first, then apply language-specific + universal checks:
- **Solidity**: full checklist below
- **Vyper**: focus on reentrancy (no modifier support), integer issues, storage layout, `raw_call` misuse
- **Yul**: focus on memory safety, calldata handling, return value checks
- **Huff**: focus on stack underflow/overflow, missing revert paths

Analyze each contract systematically for ALL of the following vulnerability classes:

### Critical (Fund-draining risk)
| ID | Vulnerability | Detection Pattern |
|----|--------------|-------------------|
| C1 | **Reentrancy** | External call (`call`, `transfer`, `send`) before state update; missing reentrancy guard |
| C2 | **Access Control** | Missing `onlyOwner`/role check on privileged functions (`withdraw`, `mint`, `pause`, `upgrade`) |
| C3 | **Flash Loan / Price Oracle Manipulation** | Spot price used as oracle; no TWAP; single-block price dependency |
| C4 | **Unchecked Return Values** | `.call()` return value not checked; low-level calls without revert |
| C5 | **Integer Overflow/Underflow** | `unchecked` blocks with arithmetic; pre-0.8 without SafeMath |
| C6 | **Arbitrary External Call** | User-controlled `target` address in `.call()` |
| C7 | **Delegatecall to Untrusted Contract** | `delegatecall` with user-supplied address |
| C8 | **Selfdestruct** | Unprotected `selfdestruct` |

### High
| ID | Vulnerability | Detection Pattern |
|----|--------------|-------------------|
| H1 | **tx.origin Authentication** | `require(tx.origin == owner)` |
| H2 | **Timestamp Dependence** | `block.timestamp` used for randomness or critical logic |
| H3 | **Front-running** | Commit-reveal missing; predictable state transitions |
| H4 | **Signature Replay** | Missing nonce or chainId in signed messages |
| H5 | **Uninitialized Proxy** | Implementation contract not initialized; `initialize()` callable by anyone |
| H6 | **Storage Collision** | Proxy + implementation storage layout mismatch |
| H7 | **ERC20 Approval Race** | `approve()` without `increaseAllowance` pattern |

### Medium
| ID | Vulnerability | Detection Pattern |
|----|--------------|-------------------|
| M1 | **Denial of Service** | Unbounded loop; push-over-pull pattern missing |
| M2 | **Centralization Risk** | Single EOA controls critical functions |
| M3 | **Missing Event Emissions** | State-changing functions without events |
| M4 | **Incorrect ERC Standard** | Missing return values; wrong interface implementation |
| M5 | **Block Gas Limit** | Loop over dynamic array that can grow unbounded |

---

## Step 4: Generate Findings Report

For each vulnerability found, output:

```
## [SEVERITY] [ID] - [Vulnerability Name]

**File**: contracts/MyContract.sol
**Line**: 42-58
**Function**: `withdraw()`

**Description**:
[Explain what the vulnerability is and why it's dangerous]

**Vulnerable Code**:
```solidity
// paste the vulnerable snippet
```

**Impact**:
[What an attacker can do - e.g., "drain all ETH from the contract"]

**Proof of Concept**:
[Describe the attack steps in plain language]
```

---

## Step 5: Automated Patch Suggestions (Patch Mode)

For each Critical and High finding, generate a concrete fix:

```
## Patch for [ID] - [Vulnerability Name]

**Fix**:
```solidity
// Show the corrected code
```

**Explanation**:
[Why this fix works]

**Verification**:
[How to confirm the fix is correct - what test to write]
```

Apply patches only if user explicitly asks: "apply the patches" or "fix the vulnerabilities".

---

## Step 6: Final Security Report

Output a complete report:

```markdown
# Smart Contract Security Audit Report
**Date**: [today]
**Target**: [path]
**Files Analyzed**: [N] contracts

## Executive Summary
- Critical: [N]
- High: [N]
- Medium: [N]
- Total Issues: [N]

## Risk Score: [CRITICAL / HIGH / MEDIUM / LOW]

## Findings
[All findings from Step 4]

## Patches
[All patches from Step 5]

## Recommendations
1. [Top priority action]
2. [Second priority]
3. [Third priority]

## Files Audited
- [list of .sol files]
```

---

## Execution Rules

- **Never ask the user for anything** after receiving the path - run the full audit automatically
- Read ALL `.sol` files before starting analysis (don't analyze one at a time)
- If a file imports others, read those too for full context
- Flag false positives explicitly: "This pattern looks like X but is safe because Y"
- If no vulnerabilities found, say so clearly with confidence level
- Always complete Detect → Patch → Report in one pass
