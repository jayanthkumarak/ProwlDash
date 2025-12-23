# ProwlDash V5.0

[![Version](https://img.shields.io/badge/version-5.0.0-brightgreen.svg)](CHANGELOG.md)
[![CI](https://github.com/jayanthkumarak/ProwlDash/actions/workflows/ci.yml/badge.svg)](https://github.com/jayanthkumarak/ProwlDash/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/)

**ProwlDash** is the enterprise-grade dashboard generator for [Prowler](https://github.com/prowler-cloud/prowler) security assessments. It transforms raw CSV data into interactive, auditor-ready HTML reports that can be viewed offline, shared securely, and presented to executive stakeholders.

The tool runs entirely offline, requires no infrastructure, and scales to handle data from hundreds of AWS accounts.

## Key Features (V5.0)

### 📊 Interactive Intelligence
*   **Offline Availability**: Generates a single, self-contained HTML file. No server required.
*   **Search & Filter**: Real-time filtering by Status, Severity, Region, Service, and *new* Multi-Keyword Search.
*   **Deep Linking**: Direct links to AWS Console resources for rapid remediation.

### 🛡️ Best-in-Class Compliance
*   **CIS Benchmarks**: Visualizes **Level 1** and **Level 2** profiles with distinct badges.
*   **MITRE ATT&CK**: Maps findings to MITRE Tactics and Techniques with clickable links to the Knowledge Base.
*   **Framework Agnostic**: Universal support for 40+ frameworks including **PCI-DSS**, **HIPAA**, **NIST 800-53**, **SOC2**, and **FSBP**.

### 💼 Executive Reporting
*   **PDF Export**: Generate a one-page "Executive Summary" PDF directly from the dashboard.
*   **CSV Export**: Download filtered datasets for custom analysis.
*   **Custom Branding**: Native support for **Dark Mode** and Corporate Color schemes via CSS variables.

### 🚀 Enterprise Performance
*   **Hybrid Parsing Engine**: Automatically switches between standard library (speed) and Pandas (throughput) based on dataset size (>10MB).
*   **Parallel Processing**: Utilizes all available CPU cores for massive multi-account aggregation.
*   **Robust & Secure**: Strict output encoding prevents injection attacks; handles malformed and legacy Prowler CSVs gracefully.

## Installation

ProwlDash is a standalone Python utility. It has zero heavy dependencies by default.

### Requirements
*   Python 3.7+
*   (Optional) `pandas` for accelerated processing of large datasets.

### Install via pip
```bash
pip install git+https://github.com/jayanthkumarak/ProwlDash.git
```

### Run from Source
```bash
git clone https://github.com/jayanthkumarak/ProwlDash.git
cd ProwlDash
python3 prowldash.py --help
```

## Usage

### 1. Basic Dashboard
Generate a dashboard from a single Prowler CSV report.
```bash
prowldash prowler-output.csv
```
*Output*: `output/<timestamp>/cis_dashboard.html`

### 2. Multi-Account Aggregation
Merge reports from multiple accounts into a single "Single Pane of Glass" view.
```bash
prowldash data/*.csv --output ./monthly-report
```

### 3. Compliance Frameworks
Force a specific framework view (if not auto-detected).
```bash
prowldash prowler-output.csv --framework pci-dss
```

## Advanced Options

| Flag | Description |
| :--- | :--- |
| `--framework <ID>` | Force a specific framework ID (e.g., `pci-dss`, `hipaa`). |
| `--output <DIR>` | Specify a custom output directory. |
| `--no-timestamp` | Disable timestamped subdirectories (useful for CI/CD). |
| `--max-workers <N>` | Limit parallel worker processes. |

## Supported Frameworks
ProwlDash automatically adapts to:
*   **CIS AWS Foundations Benchmark** (v1.x, v2.0, v3.0)
*   **AWS Foundational Security Best Practices** (FSBP)
*   **PCI DSS** (v3.2.1, v4.0)
*   **HIPAA**
*   **NIST 800-53** (Rev4, Rev5)
*   **SOC 2**
*   **ISO 27001**
*   ...and [many more](https://github.com/prowler-cloud/prowler).

## License
Apache-2.0
