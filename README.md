# Prowler Dashboard Generator V3

A framework-agnostic Python CLI tool that transforms Prowler security scan CSV outputs into beautiful, interactive HTML dashboards. Auto-detects and supports **20+ compliance frameworks** including CIS, FSBP, PCI-DSS, HIPAA, NIST, SOC2, ISO27001, GDPR, FedRAMP, and more.

## Features

- **Framework Agnostic**: Auto-detects compliance framework from filename or CSV content
- **20+ Frameworks Supported**: CIS, FSBP, PCI-DSS, HIPAA, NIST 800-53/171/CSF, SOC2, ISO27001, GDPR, FedRAMP, and more
- **Multi-Account Support**: Tabbed interface combining findings from multiple AWS accounts
- **Scan Comparison**: Visual diff between old and new scans to track remediation progress
- **Severity Prioritization**: Full support for Critical, High, Medium, Low severity levels
- **Self-Contained HTML**: Generated dashboards work offline - no server required
- **Dark/Light Themes**: Toggle between themes with localStorage persistence
- **Timestamped Output**: Organized output folders with date/time stamps

---

## Quick Start

```bash
# Generate dashboards from CSV files
python3 generate.py *.csv

# Specify output directory
python3 generate.py --output ./reports data/*.csv

# Force a specific framework
python3 generate.py --framework hipaa scan_results.csv

# List all supported frameworks
python3 generate.py --list-frameworks

# Show help
python3 generate.py --help
```

---

## Supported Frameworks

| Framework | Description |
|-----------|-------------|
| **CIS** | CIS AWS Foundations Benchmark |
| **FSBP** | AWS Foundational Security Best Practices |
| **PCI-DSS** | Payment Card Industry Data Security Standard |
| **HIPAA** | Health Insurance Portability and Accountability Act |
| **NIST 800-53** | NIST Special Publication 800-53 |
| **NIST 800-171** | NIST Special Publication 800-171 |
| **NIST CSF** | NIST Cybersecurity Framework |
| **SOC2** | Service Organization Control 2 |
| **ISO 27001** | ISO/IEC 27001 Information Security |
| **GDPR** | General Data Protection Regulation |
| **FedRAMP** | Federal Risk and Authorization Management |
| **CISA** | Cybersecurity and Infrastructure Security Agency |
| **ENS** | Esquema Nacional de Seguridad (Spain) |
| **FFIEC** | Federal Financial Institutions Examination Council |
| **GxP** | Good Practice regulations (FDA 21 CFR Part 11) |
| **MITRE ATT&CK** | MITRE ATT&CK Framework |
| **RBI** | Reserve Bank of India Cyber Security Framework |
| **Well-Architected** | AWS Well-Architected Framework |
| **Trusted Advisor** | AWS Trusted Advisor checks |
| **Generic** | Fallback for unrecognized frameworks |

Run `python3 generate.py --list-frameworks` for the complete list with details.

---

## Installation

No external dependencies required - uses Python standard library only.

```bash
# Requirements
Python 3.8+

# Verify installation
python3 generate.py --version
```

---

## Usage

### Basic Usage

```bash
# Single file
python3 generate.py report.csv

# Multiple files (auto-grouped by framework and date)
python3 generate.py scan1.csv scan2.csv scan3.csv

# Directory glob
python3 generate.py data/*.csv
```

### Output Options

```bash
# Custom output directory
python3 generate.py --output ./my-reports data/*.csv

# Skip timestamped subfolder
python3 generate.py --no-timestamp --output ./latest data/*.csv
```

### Framework Override

```bash
# Force specific framework detection
python3 generate.py --framework pci-dss compliance_scan.csv

# Short form
python3 generate.py -f hipaa hipaa_results.csv
```

### Multi-Account Comparison

When processing multiple CSV files:

1. Files are grouped by detected framework
2. Within each framework, files are grouped by scan date
3. Oldest date becomes baseline, newest becomes current
4. Delta calculation shows fixed issues and new failures

```bash
# Example: 2 accounts, 2 dates, 2 frameworks
python3 generate.py \
  cis_acct1_dec16.csv \
  cis_acct1_dec17.csv \
  cis_acct2_dec16.csv \
  cis_acct2_dec17.csv \
  fsbp_acct1_dec16.csv \
  fsbp_acct1_dec17.csv

# Output:
# output/2025-12-19_143052/
#   ├── index.html          # Landing page
#   ├── cis_dashboard.html  # CIS findings
#   └── fsbp_dashboard.html # FSBP findings
```

---

## Output Structure

```
output/
└── 2025-12-19_143052/           # Timestamped folder
    ├── index.html               # Landing page with framework cards
    ├── cis_dashboard.html       # CIS framework dashboard
    ├── fsbp_dashboard.html      # FSBP framework dashboard
    └── hipaa_dashboard.html     # HIPAA framework dashboard (if applicable)
```

### Landing Page

The `index.html` landing page provides:
- Cards for each generated framework dashboard
- Framework-specific icons and color schemes
- Pass/Fail statistics per framework
- Dark/light theme toggle

### Dashboard Features

Each framework dashboard includes:

| Feature | Description |
|---------|-------------|
| **Executive Summary** | Clickable cards for Total Failures, Passes, Manual Reviews, Fixed, New |
| **Severity Breakdown** | Critical, High, Medium, Low counts with click-to-filter |
| **Multi-Account Tabs** | Switch between "All Accounts" and individual account views |
| **Analysis Charts** | Status distribution, by-account comparison, top failing services |
| **Filter Bar** | Filter by account, status, severity, region, service, change type |
| **Search** | Full-text search across check ID, title, and resource |
| **Detail Modal** | Click any row for full details including remediation guidance |

---

## CSV Input Formats

### Main Format (Recommended)

Standard Prowler output with severity levels:

| Column | Description |
|--------|-------------|
| `ACCOUNT_UID` | AWS Account ID |
| `ACCOUNT_NAME` | Account alias |
| `CHECK_ID` | Prowler check identifier |
| `CHECK_TITLE` | Human-readable check name |
| `STATUS` | PASS, FAIL, MANUAL |
| `SEVERITY` | critical, high, medium, low |
| `SERVICE_NAME` | AWS service |
| `COMPLIANCE` | Framework identifiers |
| `RISK` | Risk description |
| `REMEDIATION_RECOMMENDATION_TEXT` | Fix instructions |

### Compliance Format

Framework-specific output from Prowler's compliance mode:

| Column | Description |
|--------|-------------|
| `ACCOUNTID` | AWS Account ID |
| `REQUIREMENTS_ID` | Control ID |
| `REQUIREMENTS_DESCRIPTION` | Control description |
| `STATUS` | PASS, FAIL, MANUAL |

---

## Framework Detection

The tool detects frameworks in this priority order:

1. **User Override**: `--framework` flag takes precedence
2. **Filename Patterns**: e.g., `fsbp_report.csv` → FSBP, `cis_5.0_aws.csv` → CIS
3. **COMPLIANCE Column**: Analyzes framework mentions across rows
4. **Default**: Falls back to CIS if no framework detected

### Template Fallback

If a specific framework template doesn't exist, the tool falls back to the CIS template with a note in the console output.

---

## Generating Prowler Reports

```bash
# Install Prowler
pip install prowler

# CIS Benchmark scan
prowler aws --compliance cis_5.0_aws -M csv

# FSBP scan
prowler aws --compliance aws_foundational_security_best_practices_aws -M csv

# HIPAA scan
prowler aws --compliance hipaa_aws -M csv

# PCI-DSS scan
prowler aws --compliance pci_dss_4.0_aws -M csv
```

---

## Project Structure

```
CSV2Dashboard/
├── generate.py              # Main CLI tool (~1100 lines)
├── README.md                # This documentation
├── .gitignore               # Git ignore rules
└── templates/
    ├── cis_template.html    # CIS dashboard template
    └── fsbp_template.html   # FSBP dashboard template
```

---

## Changelog

### V3.0 (December 2025)

**Framework Agnostic Support:**
- Added framework registry with 20+ compliance frameworks
- Auto-detection from filename patterns and COMPLIANCE column
- `--framework` flag for manual override
- `--list-frameworks` to display all supported frameworks
- Dynamic landing page with framework-specific styling
- Template fallback system for unknown frameworks

**Output Organization:**
- Timestamped output subdirectories by default
- `--output` flag for custom output path
- `--no-timestamp` flag to skip subfolder creation
- Auto-generated landing page (index.html) per run

**CLI Improvements:**
- Added `--help` with comprehensive usage guide
- Added `--version` flag
- Improved error messages and progress output

### V2.0 (December 2025)

- Tabbed multi-account interface
- Severity prioritization (Critical/High/Medium/Low)
- Clickable executive summary cards
- Per-account statistics
- Resizable table columns

### V1.0 (December 2025)

- Initial release
- CIS and FSBP support
- Multi-account comparison
- Dark/light themes

---

## License

MIT License

---

*Built with Claude Code*
