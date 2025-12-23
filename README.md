# ProwlDash

[![Version](https://img.shields.io/badge/version-5.1.0-brightgreen.svg)](CHANGELOG.md)
[![CI](https://github.com/jayanthkumarak/ProwlDash/actions/workflows/ci.yml/badge.svg)](https://github.com/jayanthkumarak/ProwlDash/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/)

ProwlDash is a standalone utility that converts [Prowler](https://github.com/prowler-cloud/prowler) CSV reports into interactive, self-contained HTML dashboards. It allows security teams to distribute compliance findings to stakeholders who do not have access to the AWS console or Prowler's raw output.

The tool runs entirely offline, requires no infrastructure, and is designed to scale to hundreds of AWS accounts.

## Key Features

### Interactive Dashboard
*   **Offline Availability**: Generates a single HTML file with embedded data and logic. No server requires.
*   **Search & Filter**: Real-time filtering by Status, Severity, Region, Service, and keyword search.
*   **Deep Linking**: Direct links to AWS Console resources.

### Compliance Intelligence
*   **MITRE ATT&CK**: Maps findings to MITRE Tactics and Techniques with links to the official Knowledge Base.
*   **Framework Agnostic**: Supports 40+ frameworks including PCI-DSS, HIPAA, NIST 800-53, SOC2, and FSBP.

### Reporting
*   **Customization**: Supports Dark Mode and custom corporate branding via CSS.

### Performance & Security
*   **Hybrid Parsing**: Automatically switches between standard library and Pandas parsing based on dataset size (>10MB) for optimal performance.
*   **Parallel Processing**: Utilizes multiple CPU cores for multi-account aggregation.
*   **Secure**: Strict output encoding prevents injection attacks.

## Installation

ProwlDash is a standalone Python utility.

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

### Basic Dashboard
Generate a dashboard from a single Prowler CSV report.
```bash
prowldash prowler-output.csv
```
The output will be saved to `output/<timestamp>/cis_dashboard.html`.

### Multi-Account Aggregation
Merge reports from multiple accounts.
```bash
prowldash data/*.csv --output ./monthly-report
```

### Compliance Frameworks
Force a specific framework view (e.g., PCI-DSS).
```bash
prowldash prowler-output.csv --framework pci-dss
```

## Advanced Options

| Flag | Description |
| :--- | :--- |
| `--framework <ID>` | Force a specific framework ID. |
| `--output <DIR>` | Specify a custom output directory. |
| `--no-timestamp` | Disable timestamped subdirectories. |
| `--max-workers <N>` | Limit parallel worker processes. |

## Supported Frameworks
ProwlDash supports all major Prowler compliance frameworks, including:
*   CIS AWS Foundations Benchmark
*   AWS Foundational Security Best Practices (FSBP)
*   PCI DSS
*   HIPAA
*   NIST 800-53
*   SOC 2
*   ISO 27001

## License
Apache-2.0
