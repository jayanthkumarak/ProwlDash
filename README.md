# ProwlDash 📊

**Professional HTML Dashboard Generator for Prowler Security Scans**

> Turn your raw CSV scan data into compliant, executive-ready visualizations.

![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)
![Version](https://img.shields.io/badge/version-4.7.1-green.svg)
![Python](https://img.shields.io/badge/python-3.7+-blue.svg)

ProwlDash takes the CSV output from [Prowler](https://github.com/prowler-cloud/prowler) and generates a beautiful, interactive, single-file HTML dashboard. It supports multi-account scanning, historical comparisons, and multiple compliance frameworks.

---

## 🚀 Key Features (v4.7.1)

-   **Framework Agnostic**: Auto-detects and supports 40+ frameworks (CIS, FSBP, PCI-DSS, HIPAA, NIST, etc.).
-   **Smart Remediation Detection**: 
    -   Uses a **4-Layer Matching Algorithm** (Strict, Name, Singleton, Fuzzy) to accurately track "Fixed" issues even if AWS Resource IDs change (e.g., rebuilt GuardDuty detectors).
-   **Remediation Metrics**: 
    -   Quantitative "Expert" display of remediation percentages broken down by severity (e.g. "Critical: 40% Fixed").
-   **Multi-Account Support**: Consolidates scans from multiple accounts into a unified tabbed interface.
-   **Historical Comparison**: Automatically compares against previous scans to highlight **Fixed Issues** and **New Failures**.
-   **Zero Dependencies**: Generates a standalone HTML file that works offline. No server required.

## 📦 Installation

```bash
pip install prowldash
```

Or clone and run directly:

```bash
git clone https://github.com/jayanthkumarak/ProwlDash.git
cd ProwlDash
pip install .
```

## 🛠️ Usage

### Basic Usage
Generate a dashboard from a single scan file:

```bash
prowldash fsbp-report.csv
```

### Multi-Account & Wildcards
Combine multiple reports into one dashboard:

```bash
prowldash output/prod-*.csv output/dev-*.csv
```

### Specify Output Directory
```bash
prowldash --output my-reports/ scan.csv
```
*Note: ProwlDash automatically creates nested, timestamped folders (e.g., `output/2026-01-05/18-30-00/`) to prevent data loss.*

## 📊 Sample Output

The generated dashboard includes:
1.  **Executive Summary**: High-level stats, pass/fail ratios, and remediation counts.
2.  **Severity Breakdown**: Visual "Sparkline" progress bars showing remediation % per severity.
3.  **Trend Analysis**: Comparison with previous runs (Delta analysis).
4.  **Detailed Findings**: Searchable, filterable table of all findings with remediation steps.

## 🧪 Testing

ProwlDash comes with a comprehensive test suite covering its core matching logic and stats generation.

```bash
python3 -m unittest tests/test_prowldash.py
```

## 📝 License

Apache 2.0. See [LICENSE](LICENSE) for details.

---
