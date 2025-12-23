# ProwlDash

[![Version](https://img.shields.io/badge/version-4.9.6-brightgreen.svg)](CHANGELOG.md)
[![CI](https://github.com/jayanthkumarak/ProwlDash/actions/workflows/ci.yml/badge.svg)](https://github.com/jayanthkumarak/ProwlDash/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/)

ProwlDash converts [Prowler](https://github.com/prowler-cloud/prowler) CSV reports into interactive, self-contained HTML dashboards. It enables security teams to distribute compliance findings to stakeholders who lack access to the AWS console or Prowler's raw output.

The tool runs entirely offline, requires no infrastructure, and scales to handle data from hundreds of AWS accounts.

## Features

*   **Offline Availability**: Generates a single HTML file with embedded data and logic. No server or external dependencies required.
*   **Universal Support**: Automatically detects and adapts to 40+ compliance frameworks (CIS, PCI-DSS, HIPAA, NIST, etc.).
*   **Compliance Metadata**: Visualizes CIS Levels (L1/L2) and links MITRE ATT&CK techniques directly to the knowledge base.
*   **Robust Parsing**: Enhanced CSV parser handles complex Prowler outputs, including compliance-specific metadata and malformed fields.
*   **Adaptive Performance**: Utilizes a hybrid parsing engine that switches between standard library CSV (low overhead) and Pandas (high throughput) based on file size, parallelizing work across available CPU cores.
*   **Security Focused**: Implements strict output encoding to prevent injection attacks from untrusted input data.
*   **Accessibility**: Built with semantic HTML and ARIA roles to ensure usability for all users.

## Installation

ProwlDash is a standalone Python utility. It can be installed directly from the repository.

### Requirements
*   Python 3.7+
*   (Optional) `pandas` for accelerated processing of large datasets (>10MB).

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

### Basic Generation
Generate a dashboard from a single Prowler CSV export. The output will be saved to a timestamped directory in `./output/`.

```bash
prowldash prowler-output.csv
```

### Multi-Account Aggregation
Pass multiple CSV files to merge them into a unified dashboard. This allows for a centralized view of compliance across an entire organization.

```bash
prowldash account-a.csv account-b.csv account-c.csv
# or using glob patterns
prowldash data/*.csv
```

### Remediation Tracking
Provide two scan files to compare changes over time. The dashboard will highlight issues that have been fixed and identify new failures.

```bash
prowldash baseline.csv latest.csv
```

### Configuration Options

| Flag | Description |
| :--- | :--- |
| `--framework <ID>` | Force a specific framework ID (e.g., `pci-dss`), overriding auto-detection. |
| `--output <DIR>` | Specify a custom output directory. |
| `--no-timestamp` | Disable the creation of timestamped subdirectories. |
| `--max-workers <N>` | Limit the number of parallel worker processes. |

## Supported Frameworks

ProwlDash supports all major Prowler compliance frameworks, including:
*   **CIS AWS Foundations Benchmark** (`cis`)
*   **AWS Foundational Security Best Practices** (`fsbp`)
*   **PCI DSS** (`pci-dss`)
*   **HIPAA** (`hipaa`)
*   **NIST SP 800-53** (`nist-800-53`)
*   **SOC 2** (`soc2`)
*   **ISO 27001** (`iso27001`)

For a complete list of supported IDs, run:
```bash
prowldash --list-frameworks
```

## License

Apache-2.0
