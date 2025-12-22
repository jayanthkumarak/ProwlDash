# ProwlDash

**ProwlDash** is a command-line utility for generating interactive HTML compliance dashboards from Prowler security scan outputs.

It parses CSV exports from [Prowler](https://github.com/prowler-cloud/prowler), auto-detects the compliance framework, and produces self-contained HTML dashboards suitable for offline viewing and executive reporting.

## Installation

No installation required. ProwlDash is a single Python script with no external dependencies.

```bash
git clone https://github.com/jayanthkumarak/ProwlDash.git
cd ProwlDash
python3 prowldash.py --help
```

## Usage

```bash
prowldash.py [OPTIONS] FILE [FILE ...]
```

### Examples

```bash
# Basic usage
python3 prowldash.py scan_results.csv

# Multiple files (multi-account support)
python3 prowldash.py account1.csv account2.csv account3.csv

# Specify output directory
python3 prowldash.py --output ./reports data/*.csv

# Force a specific framework
python3 prowldash.py --framework hipaa scan_results.csv

# List supported frameworks
python3 prowldash.py --list-frameworks
```

### Options

| Option | Description |
|--------|-------------|
| `-o`, `--output DIR` | Output directory (default: `./output`) |
| `-f`, `--framework ID` | Force specific compliance framework |
| `--no-timestamp` | Skip timestamped subfolder creation |
| `--list-frameworks` | Display all supported framework IDs |
| `-h`, `--help` | Show help message |
| `-v`, `--version` | Show version |

## Supported Frameworks

ProwlDash supports all AWS compliance frameworks available in Prowler:

- **CIS** — CIS Amazon Web Services Foundations Benchmark
- **FSBP** — AWS Foundational Security Best Practices
- **PCI-DSS** — Payment Card Industry Data Security Standard
- **HIPAA** — Health Insurance Portability and Accountability Act
- **NIST 800-53** — Security and Privacy Controls
- **NIST 800-171** — Protecting Controlled Unclassified Information
- **NIST CSF** — Cybersecurity Framework
- **SOC2** — Service Organization Control 2
- **ISO27001** — Information Security Management
- **GDPR** — General Data Protection Regulation
- **FedRAMP** — Federal Risk and Authorization Management
- **MITRE ATT&CK** — Adversarial Tactics and Techniques
- **Well-Architected** — AWS Well-Architected Framework Security Pillar
- **ENS** — Esquema Nacional de Seguridad (Spain)
- **KISA ISMS-P** — Korean Information Security Management System

Run `prowldash.py --list-frameworks` for the complete list.

## Output

ProwlDash generates:

1. **Framework-specific dashboards** — One HTML file per detected framework (e.g., `cis_dashboard.html`)
2. **Landing page** — An `index.html` linking all generated dashboards
3. **Timestamped folders** — Output organized by date/time (disable with `--no-timestamp`)

All HTML files are self-contained and require no server or internet connection.

## Scan Comparison

To compare scans and track remediation progress, provide an older scan alongside the current one:

```bash
python3 prowldash.py old_scan.csv new_scan.csv
```

The dashboard will highlight:
- **Fixed** — Issues that were failing but now pass
- **New Failures** — Issues that appeared since the previous scan

## Documentation

Interactive HTML documentation is available at `docs/index.html`.

## Requirements

- Python 3.7+
- No external dependencies

## License

MIT

## See Also

- [Prowler](https://github.com/prowler-cloud/prowler) — The security scanner that produces the CSV input
- [Prowler Documentation](https://docs.prowler.com/) — Official Prowler docs
