---
name: evmbench
description: Smart contract security audit using EVMbench (OpenAI + Paradigm). Use when user wants to audit Solidity contracts, detect vulnerabilities, patch issues, or run the EVMbench benchmark. Triggers on keywords like "audit contract", "smart contract vulnerability", "evmbench", "solidity security".
allowed-tools: Bash, Read, Glob, WebFetch
---

# EVMbench Smart Contract Security Skill

EVMbench is an open benchmark by OpenAI + Paradigm that evaluates AI agents on detecting, patching, and exploiting smart contract vulnerabilities.

## Quick Start

Ask the user which mode they need:

1. **Web Audit** - Upload contracts to web UI, get instant vulnerability report
2. **Local Benchmark** - Run full detect/patch/exploit evaluation locally
3. **Interpret Results** - Help understand existing EVMbench output

---

## Mode 1: Web Audit (Fastest)

**URL**: https://paradigm.xyz/evmbench

Steps:
1. Zip the contract folder or prepare individual `.sol` files
2. Open https://paradigm.xyz/evmbench
3. Drag & drop the folder/zip
4. Select model (default: `codex-gpt-5.2`)
5. Agree to Terms and click **Start analysis**
6. Review high-severity findings

**Output**: List of high-severity vulnerabilities with descriptions.

---

## Mode 2: Local Setup

### Prerequisites
```bash
# Check requirements
node --version   # Node.js 18+
git --version
cargo --version  # Rust (for the harness)
```

### Install
```bash
git clone https://github.com/paradigmxyz/evmbench
cd evmbench
```

Read the repo README for exact setup:
```bash
cat README.md
```

### Run Detect Mode
```bash
# Detect vulnerabilities in a contract
# (follow repo instructions for exact CLI)
```

### Run Exploit Mode (Sandboxed)
- Runs on local Anvil instance (NOT mainnet)
- Requires Foundry/Anvil installed:
```bash
curl -L https://foundry.paradigm.xyz | bash
foundryup
```

---

## Mode 3: Interpret Results

When user shares EVMbench output, help them understand:

### Detect Results
- **Recall score**: % of ground-truth vulnerabilities found
- **False positives**: Issues flagged that aren't real vulnerabilities
- **Missed vulnerabilities**: What the agent failed to catch

### Patch Results
- **Success**: Vulnerability removed AND all tests still pass
- **Failure modes**:
  - Broke existing functionality
  - Vulnerability still exploitable after patch
  - Compilation error introduced

### Exploit Results
- **Score**: % of fund-draining attacks successfully executed
- Each task = deploy contract → execute exploit → verify funds moved

---

## Common Vulnerability Types in EVMbench

| Type | Description | Example |
|------|-------------|---------|
| Reentrancy | External call before state update | Classic DAO hack pattern |
| Access Control | Missing `onlyOwner` or role checks | Anyone can call admin functions |
| Integer Overflow | Unchecked arithmetic | Pre-Solidity 0.8 math bugs |
| Flash Loan Attack | Price manipulation via flash loans | Oracle manipulation |
| Logic Error | Business logic flaw | Wrong calculation in reward distribution |

---

## Analyzing a Contract Locally (Without EVMbench)

If user has a `.sol` file and wants a quick review:

```bash
# Read the contract
cat contracts/MyContract.sol
```

Then analyze for:
1. External calls before state changes (reentrancy)
2. Missing access modifiers
3. Unchecked return values
4. Arithmetic without SafeMath (pre-0.8) or unchecked blocks
5. tx.origin usage
6. Timestamp dependence
7. Delegatecall to untrusted contracts

---

## Resources

- Web UI: https://paradigm.xyz/evmbench
- GitHub: https://github.com/paradigmxyz/evmbench
- Paper: https://cdn.openai.com/evmbench/evmbench.pdf
- OpenAI blog: https://openai.com/index/introducing-evmbench/
- Paradigm blog: https://www.paradigm.xyz/2026/02/evmbench
