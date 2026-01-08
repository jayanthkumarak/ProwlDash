# ProwlDash

[![Version](https://img.shields.io/badge/version-v4.8.0-blue.svg)](CHANGELOG.md)
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
*   **Framework Agnostic**: Supports 21+ frameworks including PCI-DSS, HIPAA, NIST 800-53, SOC2, and FSBP.

### Reporting
*   **Customization**: Supports Dark Mode and custom corporate branding via CSS.

![Light Theme Dashboard](docs/images/dashboard-light.png)

### Performance & Security
*   **Hybrid Parsing**: Automatically switches between standard library and Pandas parsing based on dataset size (>10MB) for optimal performance.
*   **Parallel Processing**: Utilizes multiple CPU cores for multi-account aggregation.
*   **Enterprise Security**: Comprehensive security hardening with 0 known vulnerabilities:
    - Content Security Policy (CSP) prevents XSS attacks
    - X-Frame-Options prevents clickjacking
    - Subresource Integrity (SRI) for CDN resources
    - Strict output encoding prevents injection attacks
    - Security penetration testing integrated into CI/CD

## Visual Gallery

<div align="center">
  <img src="docs/images/dashboard-dark.png" alt="Executive Summary" width="800">
  <p><em>Executive Summary with clear pass/fail indicators</em></p>
  
  <img src="docs/images/dashboard-charts.png" alt="Analysis Charts" width="800">
  <p><em>Interactive charts for severity and service distribution</em></p>

  <img src="docs/images/dashboard-table.png" alt="Findings Table" width="800">
  <p><em>Searchable and sortable findings table</em></p>
</div>

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

ProwlDash provides comprehensive command-line options for fine-grained control:

| Flag | Short | Description | Example |
| :--- | :--- | :--- | :--- |
| `--help` | `-h` | Show help message and exit | `prowldash --help` |
| `--version` | `-v` | Show version information and exit | `prowldash --version` |
| `--framework <ID>` | `-f` | Force a specific framework ID (overrides auto-detection) | `prowldash -f pci-dss report.csv` |
| `--output <DIR>` | `-o` | Specify a custom output directory | `prowldash -o ./reports data/*.csv` |
| `--no-timestamp` | | Disable timestamped subdirectories | `prowldash --no-timestamp report.csv` |
| `--max-workers <N>` | | Limit parallel worker processes (default: auto) | `prowldash --max-workers 4 data/*.csv` |
| `--verbose` | | Show detailed execution statistics | `prowldash --verbose report.csv` |
| `--list-frameworks` | | List all supported frameworks and exit | `prowldash --list-frameworks` |

### Examples

**View all available frameworks:**
```bash
prowldash --list-frameworks
```

**Force a specific framework:**
```bash
prowldash --framework hipaa hipaa_scan.csv
```

**Generate with detailed statistics:**
```bash
prowldash --verbose --output ./monthly-report data/*.csv
```

**Process with limited parallelism:**
```bash
prowldash --max-workers 2 --no-timestamp large_scan.csv
```

## Supported Frameworks

ProwlDash supports **21 compliance frameworks** with auto-detection capabilities. Use the `--framework` flag with the framework ID to override auto-detection.

### Framework Reference

| Framework ID | Full Name | Description |
| :--- | :--- | :--- |
| `cis` | CIS AWS Benchmark | CIS Amazon Web Services Foundations Benchmark compliance checks |
| `fsbp` | AWS FSBP | AWS Foundational Security Best Practices standard compliance checks |
| `aws-well-architected` | Well-Architected | AWS Well-Architected Framework security pillar checks |
| `pci-dss` | PCI DSS | Payment Card Industry Data Security Standard compliance checks |
| `hipaa` | HIPAA | Health Insurance Portability and Accountability Act compliance checks |
| `gdpr` | GDPR | General Data Protection Regulation compliance checks for EU data protection |
| `soc2` | SOC 2 | Service Organization Control 2 Trust Services Criteria compliance checks |
| `nist-800-53` | NIST 800-53 | NIST Special Publication 800-53 security and privacy controls |
| `nist-csf` | NIST CSF | NIST Cybersecurity Framework compliance checks |
| `nist-800-171` | NIST 800-171 | NIST Special Publication 800-171 CUI protection controls |
| `iso27001` | ISO 27001 | ISO/IEC 27001 Information Security management checks |
| `fedramp` | FedRAMP | Federal Risk and Authorization Management Program compliance for US federal cloud services |
| `cisa` | CISA | Cybersecurity and Infrastructure Security Agency cybersecurity best practices |
| `mitre-attack` | MITRE ATT&CK | MITRE ATT&CK Framework adversarial tactics and techniques |
| `ens` | ENS | Esquema Nacional de Seguridad (Spain) National Security Scheme compliance |
| `kisa` | KISA ISMS-P | Korea Internet & Security Agency ISMS-P information security certification |
| `ffiec` | FFIEC | Federal Financial Institutions Examination Council cybersecurity assessment for financial institutions |
| `rbi` | RBI CSF | Reserve Bank of India Cyber Security Framework for Indian banks |
| `nis2` | NIS2 | Network and Information Security Directive 2 EU cybersecurity requirements |
| `c5` | BSI C5 | Cloud Computing Compliance Criteria Catalogue German BSI C5 cloud security attestation |
| `gxp` | GxP | Good Practice Guidelines compliance for life sciences |

### Framework Auto-Detection

ProwlDash automatically detects frameworks from:
1. **COMPLIANCE column** in CSV (e.g., `"CIS-5.0: 1.1 | HIPAA: 164_308"`)
2. **Filename patterns** (e.g., `pci_report.csv` → PCI-DSS)
3. **`--framework` flag** (overrides auto-detection)

**Usage:**
```bash
# Auto-detect (recommended)
prowldash scan_results.csv

# Force specific framework
prowldash --framework pci-dss scan_results.csv

# List all available frameworks
prowldash --list-frameworks
```

## Security

ProwlDash takes security seriously. Version 4.8.0 includes comprehensive security hardening:

### Security Features
- **0 Known Vulnerabilities**: Extensive penetration testing confirms no security issues
- **Content Security Policy (CSP)**: Prevents cross-site scripting (XSS) attacks
- **Clickjacking Protection**: X-Frame-Options header prevents iframe embedding attacks
- **Resource Integrity**: Subresource Integrity (SRI) for all CDN resources
- **Secure Encoding**: All user data properly escaped to prevent injection attacks
- **HTTPS Enforcement**: All external resources use secure HTTPS connections

### Security Testing
- Automated security penetration testing integrated into CI/CD pipeline
- Static analysis for XSS, injection, and other web vulnerabilities
- Regular security audits and updates

### Reporting Security Issues
If you discover a security vulnerability, please report it responsibly:
- **DO NOT** create public GitHub issues for security vulnerabilities
- Email security concerns to the maintainers
- Include detailed reproduction steps and impact assessment

## License
Apache-2.0
