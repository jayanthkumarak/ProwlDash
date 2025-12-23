# ProwlDash

[![Version](https://img.shields.io/badge/version-4.5.0-brightgreen.svg)](CHANGELOG.md)
[![CI](https://github.com/jayanthkumarak/ProwlDash/actions/workflows/ci.yml/badge.svg)](https://github.com/jayanthkumarak/ProwlDash/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/)

ProwlDash generates interactive HTML compliance dashboards from Prowler security scan outputs.

## Overview

ProwlDash transforms the CSV exports from [Prowler](https://github.com/prowler-cloud/prowler) into self-contained HTML dashboards designed for offline viewing and executive reporting. The tool automatically detects which compliance framework your scan targets and produces a themed dashboard with filtering, sorting, and detailed remediation guidance.

Security teams use ProwlDash to share compliance status with stakeholders who may not have access to AWS console or Prowler's native outputs. The generated HTML files require no server, no internet connection, and no special software to view.

ProwlDash supports 21 compliance frameworks including CIS AWS Benchmark, AWS Foundational Security Best Practices, PCI-DSS, HIPAA, NIST 800-53, SOC 2, ISO 27001, GDPR, FedRAMP, and others.

## Installation

ProwlDash is a single Python file with zero required dependencies. Optional dependencies enhance performance for large-scale scans.

### Using pip

```bash
pip install -e git+https://github.com/jayanthkumarak/ProwlDash.git#egg=prowldash
```

### Using UV

```bash
uv pip install -e git+https://github.com/jayanthkumarak/ProwlDash.git#egg=prowldash
```

### From source

```bash
git clone https://github.com/jayanthkumarak/ProwlDash.git
cd ProwlDash
python3 prowldash.py --help
```

After installation via pip or UV, the `prowldash` command is available system-wide.

## Quick Start

Generate a dashboard from a Prowler CSV export:

```bash
prowldash your_scan.csv
```

ProwlDash creates a timestamped output folder containing an `index.html` landing page and framework-specific dashboards. Open `index.html` in any browser to view your results.

## Usage Guide

### Processing Multiple Files

When you have scans from multiple AWS accounts, pass them all at once:

```bash
prowldash account1.csv account2.csv account3.csv
```

ProwlDash combines the results into a unified dashboard with account-level filtering. You can also use glob patterns:

```bash
prowldash data/*.csv
```

### Specifying a Framework

ProwlDash detects the compliance framework from your CSV content and filename. To override detection, use the `--framework` flag with a framework ID:

```bash
prowldash --framework hipaa scan_results.csv
```

Run `prowldash --list-frameworks` to see all available framework IDs.

### Comparing Scans Over Time

Track remediation progress by providing an older scan alongside a newer one:

```bash
prowldash january_scan.csv february_scan.csv
```

The dashboard highlights which issues were fixed and which are newly failing, making it easy to demonstrate progress to auditors.

### Customizing Output

By default, ProwlDash writes to `./output/<timestamp>/`. To specify a different location:

```bash
prowldash --output /path/to/reports scan.csv
```

To skip the timestamped subfolder:

```bash
prowldash --no-timestamp --output ./latest scan.csv
```

## Command Reference

| Option | Description |
|--------|-------------|
| `-o`, `--output DIR` | Output directory (default: `./output`) |
| `-f`, `--framework ID` | Force specific compliance framework |
| `--no-timestamp` | Write directly to output directory without timestamp subfolder |
| `--list-frameworks` | Display all supported framework IDs |
| `-h`, `--help` | Show help message |
| `-v`, `--version` | Show version |

## Supported Frameworks

| ID | Framework |
|----|-----------|
| `cis` | CIS Amazon Web Services Foundations Benchmark |
| `fsbp` | AWS Foundational Security Best Practices |
| `aws-well-architected` | AWS Well-Architected Framework Security Pillar |
| `pci-dss` | Payment Card Industry Data Security Standard |
| `hipaa` | Health Insurance Portability and Accountability Act |
| `gdpr` | General Data Protection Regulation |
| `soc2` | Service Organization Control 2 |
| `nist-800-53` | NIST Special Publication 800-53 |
| `nist-csf` | NIST Cybersecurity Framework |
| `nist-800-171` | NIST Special Publication 800-171 |
| `iso27001` | ISO/IEC 27001 Information Security |
| `fedramp` | Federal Risk and Authorization Management Program |
| `mitre-attack` | MITRE ATT&CK Framework |
| `ffiec` | Federal Financial Institutions Examination Council |
| `cisa` | CISA Cybersecurity Best Practices |
| `ens` | Esquema Nacional de Seguridad (Spain) |
| `kisa` | Korea Internet & Security Agency ISMS-P |
| `rbi` | Reserve Bank of India Cyber Security Framework |
| `nis2` | EU Network and Information Security Directive 2 |
| `c5` | BSI Cloud Computing Compliance Criteria Catalogue |
| `gxp` | Good Practice Guidelines (Life Sciences) |

## Output Structure

ProwlDash generates the following structure:

```
output/
└── 2025-12-22_143052/
    ├── index.html           # Landing page linking all dashboards
    ├── cis_dashboard.html   # Framework-specific dashboard
    └── fsbp_dashboard.html  # Additional dashboards if multiple frameworks detected
```

All HTML files are self-contained. They embed all styles, scripts, and data, requiring no external resources.

## Prowler Integration

Generate Prowler reports in CSV format for use with ProwlDash:

```bash
# Install Prowler
pip install prowler

# Run a CIS benchmark scan
prowler aws --compliance cis_5.0_aws -M csv

# Run HIPAA compliance scan  
prowler aws --compliance hipaa_aws -M csv

# List all available compliance frameworks
prowler aws --list-compliance
```

ProwlDash works with Prowler's main CSV output format, which includes the `SEVERITY` column needed for dashboard statistics.

## Documentation

Interactive HTML documentation with framework reference cards is available at `docs/index.html` in this repository.

## Performance

V4.5 introduces significant performance improvements for processing multiple files and large scans.

### Parallel Processing

When processing multiple CSV files, ProwlDash automatically distributes work across all available CPU cores:

```bash
# Processes 8 files in parallel across all cores
prowldash data/*.csv
```

**Speedup:** Linear with CPU cores. Processing N files on an M-core machine completes in approximately 1/min(N,M) the sequential time. For example, 8 files on a 14-core Apple Silicon Mac processes ~8x faster.

### Smart CSV Parsing

ProwlDash selects the optimal CSV parser based on file size:

| File Size | Parser | Reason |
|-----------|--------|--------|
| < 10 MB | stdlib csv | Lower overhead, 2x faster for typical scans |
| ≥ 10 MB | Pandas | C-optimized for enterprise-scale scans |

To enable Pandas acceleration for large files:

```bash
pip install pandas
```

### PyPy Compatibility

For additional speed, run ProwlDash with PyPy:

```bash
pypy3 prowldash.py data/*.csv
```

PyPy's JIT compiler provides 2-5x speedup on pure Python code paths.

## Requirements

- Python 3.7 or later
- **Optional:** `pandas` for accelerated parsing of large files (>10MB)

## Contributing

Contributions are welcome. Please open an issue to discuss proposed changes before submitting a pull request.

## License

Apache-2.0. See [LICENSE](LICENSE) for details.

## See Also

- [Prowler](https://github.com/prowler-cloud/prowler) — The security scanner that produces CSV input for ProwlDash
- [Prowler Documentation](https://docs.prowler.com/) — Official Prowler documentation
