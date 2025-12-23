<div align="center">

# ProwlDash

[![Version](https://img.shields.io/badge/version-4.6.0-brightgreen.svg)](CHANGELOG.md)
[![CI](https://github.com/jayanthkumarak/ProwlDash/actions/workflows/ci.yml/badge.svg)](https://github.com/jayanthkumarak/ProwlDash/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/)

**Enterprise-grade compliance dashboards for AWS security.**  
Turn raw [Prowler](https://github.com/prowler-cloud/prowler) CSV data into interactive, executive-ready HTML reports.

[Quick Start](#-quick-start) • [Features](#-key-features) • [Installation](#-installation) • [Documentation](docs/index.html)

</div>

---

## 🚀 Why ProwlDash?

Security teams struggle to share compliance data with stakeholders who lack AWS console access. Raw CSVs are unreadable; PDF reports are static and huge. 

**ProwlDash** bridges this gap by generating **self-contained, interactive HTML dashboards** that run offline. No server required.

- **📊 Executive Ready:** Beautiful, themed dashboards with high-level summaries.
- **⚡ Blazing Fast:** Process 100,000+ findings in seconds using all CPU cores.
- **🔒 Secure & Offline:** Zero external dependencies. Your data never leaves your machine.
- **♿ Accessible:** Full WCAG support with dark/light modes and colorblind-safe palettes.

## ✨ Key Features

| Feature | Description |
| :--- | :--- |
| **Universal Support** | Auto-detects 40+ frameworks (CIS, HIPAA, PCI-DSS, NIST, etc.) |
| **Smart Parsing** | Adaptive hybrid engine uses Pandas for huge files (>10MB) and stdlib for speed on small ones. |
| **Diff Engine** | Compare two scans to visualize remediation progress (Fixed vs. New Failures). |
| **Multi-Account** | Merge scans from 50+ AWS accounts into a single unified dashboard. |
| **Zero-Config** | No database, no API keys, no intricate setup. Just Python. |

## 📦 Installation

ProwlDash is a standalone Python tool. 

### Recommended (pip)
Install directly from source to get the `prowldash` command system-wide:

```bash
pip install git+https://github.com/jayanthkumarak/ProwlDash.git
```

### From Source
```bash
git clone https://github.com/jayanthkumarak/ProwlDash.git
cd ProwlDash
# No install needed, just run the script
python3 prowldash.py --help
```

> **Note:** Python 3.7+ required. `pip install pandas` is optional but recommended for large datasets.

## ⚡ Quick Start

1.  **Generate a Prowler CSV report**:
    ```bash
    prowler aws --compliance cis_5.0_aws -M csv
    ```

2.  **Create your dashboard**:
    ```bash
    prowldash output.csv
    ```

3.  **View results**:
    Open `output/YYYY-MM-DD_HHMMSS/index.html` in your browser.

## 📖 Usage Guide

### Processing Multiple Accounts
Pass multiple files or use wildcards to merge results into one view:
```bash
prowldash data/*.csv
```

### Tracking Remediation
Compare a new scan against an old baseline to see what changed:
```bash
prowldash old_scan.csv new_scan.csv
```

### Power User Options
```bash
# Force a specific framework ID (override detection)
prowldash --framework pci-dss scan.csv

# Limit parallel workers (useful for shared CI runners)
prowldash --max-workers 2 scan.csv

# Output to a specific static directory
prowldash --no-timestamp --output ./public scan.csv
```

See the [Full Documentation](docs/index.html) for all CLI options.

## 🏆 Performance

V4.6 is engineered for scale.

*   **Concurrency:** Automatically parallelizes across `min(cpu_count, file_count)` workers.
*   **Throughput:** Benchmarked at **~28,000 rows/second** on standard hardware.
*   **Memory Safety:** Uses chunked streaming for files >10MB to prevent OOM errors.

## 🧩 Supported Frameworks

<details>
<summary><strong>Click to expand full list (40+)</strong></summary>

| ID | Framework |
| :--- | :--- |
| `cis` | CIS AWS Foundations Benchmark |
| `fsbp` | AWS Foundational Security Best Practices |
| `pci-dss` | PCI DSS 3.2.1 / 4.0 |
| `hipaa` | HIPAA Security Rule |
| `nist-800-53` | NIST SP 800-53 |
| `soc2` | ACIPA SOC 2 |
| `gdpr` | EU GDPR |
| `iso27001` | ISO/IEC 27001 |
| ...and many more | (Auto-detected from CSV) |

</details>

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to set up your development environment and run tests.

## 📄 License

Apache-2.0 © [Jayanth Kumar](https://github.com/jayanthkumarak)
