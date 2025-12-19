# Prowler AWS Compliance Dashboard Generator V2

A Python CLI tool that transforms Prowler security scan CSV outputs into beautiful, interactive HTML dashboards. Supports both **CIS AWS Foundations Benchmark v5.0** and **AWS Foundational Security Best Practices (FSBP)** frameworks with full severity prioritization.

## Table of Contents

- [Features](#features)
- [Quick Start](#quick-start)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [CSV Input Formats](#csv-input-formats)
- [Dashboard Features](#dashboard-features)
- [Project Structure](#project-structure)
- [Technical Architecture](#technical-architecture)
- [Customization](#customization)
- [Generating Prowler Reports](#generating-prowler-reports)
- [Changelog](#changelog)

---

## Features

### Core Capabilities
- **Auto-detection**: Automatically identifies CIS vs FSBP framework from CSV content or filename
- **Multi-account support**: Combines findings from multiple AWS accounts into unified dashboards
- **Scan comparison**: Compares old vs new scans to track remediation progress
- **Self-contained HTML**: Generated dashboards work offline - no server required
- **Dark/Light themes**: Toggle between dark and light modes with persistence

### V2 Enhancements (December 2025)
- **Tabbed Multi-Account View**: Switch between "All Accounts" and individual account views
- **Per-Account Statistics**: Each tab shows its own stats, severity counts, and charts
- **Severity Prioritization**: Full support for Critical, High, Medium, Low severity levels
- **Clickable Executive Summary**: Click any summary card to instantly filter findings
- **Severity Breakdown Row**: Dedicated row showing failure counts by severity
- **Enhanced Filtering**: New severity filter in the filters bar
- **Risk & Remediation**: Display risk descriptions and remediation guidance from Prowler
- **Smart Account Naming**: Uses AWS account names for tabs, compact IDs for badges
- **Visual Improvements**: Hover effects, active states, and "Click to filter" hints

---

## Quick Start

```bash
# Navigate to project directory
cd "Claude Code Project"

# Generate dashboards from all main CSV files
python3 generate.py data/main/*.csv

# Open the landing page
open index.html
```

---

## Requirements

- **Python 3.8+**
- **No external dependencies** (standard library only)
- Modern web browser (Chrome, Firefox, Safari, Edge)

---

## Installation

No installation required. Clone or copy the project folder and run directly.

```bash
# Verify Python version
python3 --version  # Should be 3.8 or higher

# Test the generator
python3 generate.py --help
```

---

## Usage

### Basic Usage

```bash
# Generate dashboard from a single CSV file
python3 generate.py report.csv

# Generate with comparison (old vs new scan)
python3 generate.py old_scan.csv new_scan.csv

# Process all CSV files in a directory
python3 generate.py data/main/*.csv

# Mix both frameworks - they'll be separated automatically
python3 generate.py cis_report.csv fsbp_report.csv
```

### Multi-Account Comparison

When processing multiple CSV files, the generator:

1. Groups files by framework (CIS or FSBP)
2. Within each framework, groups files by scan date
3. Uses oldest date as "baseline" (old)
4. Uses newest date as "current" (new)
5. Combines all accounts from the same date
6. Calculates delta (fixed issues, new failures)

**Example with 2 accounts, 2 dates:**

```bash
python3 generate.py \
  report_indupro-acct1.csv \
  report_indupro-acct1_12_17_25.csv \
  report_indupro-acct2.csv \
  report_indupro-acct2_12_17_25.csv
```

**Output:**
```
Processing 4 file(s)...
  report_indupro-acct1.csv: CIS, main format, 397 rows, Dec 16, 2025
  report_indupro-acct1_12_17_25.csv: CIS, main format, 403 rows, Dec 17, 2025
  report_indupro-acct2.csv: CIS, main format, 292 rows, Dec 16, 2025
  report_indupro-acct2_12_17_25.csv: CIS, main format, 289 rows, Dec 17, 2025

Generating CIS dashboard...
  Old scan (Dec 16, 2025): 689 rows
  New scan (Dec 17, 2025): 692 rows
  Stats: 307 FAIL [2C/35H/211M/59L], 381 PASS, 7 fixed
  Output: output/cis_dashboard.html
```

---

## CSV Input Formats

The generator supports two Prowler CSV output formats:

### Main Format (Recommended)

The main Prowler output includes severity levels and is the recommended format for V2 features.

| Column | Description | Example |
|--------|-------------|---------|
| `ACCOUNT_UID` | AWS Account ID | `123456789012` |
| `ACCOUNT_NAME` | Account alias | `indupro-acct1` |
| `REGION` | AWS Region | `us-east-1` |
| `CHECK_ID` | Prowler check identifier | `iam_root_mfa_enabled` |
| `CHECK_TITLE` | Human-readable check name | `Ensure MFA is enabled for root` |
| `STATUS` | Result status | `PASS`, `FAIL`, `MANUAL` |
| `STATUS_EXTENDED` | Detailed status message | `Root account has MFA enabled` |
| `SEVERITY` | **Priority level** | `critical`, `high`, `medium`, `low` |
| `SERVICE_NAME` | AWS service | `iam`, `s3`, `ec2` |
| `RESOURCE_UID` | Resource ARN or ID | `arn:aws:iam::123456789012:root` |
| `RESOURCE_NAME` | Resource name | `root` |
| `RISK` | Risk description | `Without MFA, root account...` |
| `REMEDIATION_RECOMMENDATION_TEXT` | Fix instructions | `Enable MFA for root account...` |
| `REMEDIATION_RECOMMENDATION_URL` | Documentation link | `https://docs.aws.amazon.com/...` |
| `TIMESTAMP` | Scan timestamp | `2025-12-17T10:30:00Z` |
| `COMPLIANCE` | Framework identifier | `CIS-5.0`, `FSBP` |

### Compliance Format (Legacy)

Framework-specific output from Prowler's compliance mode. Does not include severity.

| Column | Description |
|--------|-------------|
| `ACCOUNTID` | AWS Account ID |
| `REGION` | AWS Region |
| `REQUIREMENTS_ID` | Control ID (e.g., `1.1`, `1.2`) |
| `REQUIREMENTS_DESCRIPTION` | Control description |
| `STATUS` | `PASS`, `FAIL`, `MANUAL` |
| `STATUSEXTENDED` | Detailed message |
| `RESOURCEID` | Resource identifier |
| `ASSESSMENTDATE` | Scan date |

**Note:** The main format is preferred as it includes severity data required for V2 features.

---

## Dashboard Features

### Landing Page (`index.html`)

A central hub linking to both dashboards with:
- Dark/light theme toggle (persisted in localStorage)
- Visual cards for CIS and FSBP frameworks
- Scan date information

### Tabbed Multi-Account Interface

When multiple AWS accounts are present, a tab bar appears below the header:

```
┌─────────────────────────────────────────────────────────────┐
│  [ All Accounts (692) ] [ indupro (403) ] [ Account ...7056 (289) ]  │
└─────────────────────────────────────────────────────────────┘
```

**Tab Behavior:**

| Tab | Shows |
|-----|-------|
| **All Accounts** | Combined view of all accounts (default) |
| **Individual Account** | Filtered view showing only that account's findings |

**What Changes Per Tab:**
- Executive summary cards show tab-specific counts
- Severity breakdown shows tab-specific severity distribution
- Charts recalculate for the selected account
- "By Account" chart becomes "Severity Distribution" on single-account tabs
- Findings table filters to selected account
- All filters work within the tab context

**Single Account Mode:**
If only one AWS account is in the data, the tab bar is automatically hidden.

### Executive Summary (Clickable)

Five interactive cards at the top of each dashboard:

| Card | Description | Click Action |
|------|-------------|--------------|
| **Total Failures** | Count of FAIL findings | Filter to show only failures |
| **Total Passes** | Count of PASS findings | Filter to show only passes |
| **Manual Reviews** | Findings requiring manual check | Filter to MANUAL status |
| **Issues Fixed** | Remediated since last scan | Filter to fixed items |
| **New Failures** | New issues since last scan | Filter to new failures |

Each card shows delta from previous scan when comparison data is available.

### Severity Breakdown Row

Four cards showing failure counts by severity (V2 feature):

| Severity | Color | Description |
|----------|-------|-------------|
| **Critical** | Red (#ef4444) | Immediate action required |
| **High** | Orange (#f97316) | Address within 24-48 hours |
| **Medium** | Yellow (#eab308) | Plan remediation this sprint |
| **Low** | Blue (#3b82f6) | Address when convenient |

Clicking a severity card filters to failures of that severity level.

### Analysis Charts

Three visualization panels:

1. **Status Distribution**: Donut chart showing FAIL/PASS/MANUAL percentages
2. **By Account**: Horizontal bar chart comparing failure rates across AWS accounts
3. **Top Failing Services**: Bar chart of services with most failures

### Filters Bar

| Filter | Options | Description |
|--------|---------|-------------|
| Account | All accounts in scan | Filter by specific AWS account |
| Status | All, FAIL, PASS, MANUAL | Filter by check result |
| Severity | All, Critical, High, Medium, Low | Filter by priority (V2) |
| Region | All regions in scan | Filter by AWS region |
| Service | All services in scan | Filter by AWS service |
| Change | All, Fixed, New Failures | Filter by remediation status |
| Search | Free text | Search check ID, title, resource |

### Findings Table

Sortable table with columns:

| Column | Description |
|--------|-------------|
| Check ID | Prowler check identifier |
| Title | Check description with status details |
| Status | PASS/FAIL/MANUAL badge + FIXED/NEW tag |
| Severity | Color-coded severity badge (V2) |
| Account | AWS account short name |
| Service | AWS service name |

### Detail Modal

Click any row to see full details:

- **Status**: Current status with delta indicator
- **Severity**: Priority level badge
- **Account & Region**: AWS account and region
- **Service**: AWS service
- **Resource**: Full resource ARN/ID and name
- **Status Details**: Extended status message
- **Risk**: Risk description (if available)
- **Remediation**: Step-by-step fix instructions with documentation link

---

## Project Structure

```
Claude Code Project/
├── generate.py                 # Main CLI tool (455 lines)
├── index.html                  # Landing page with theme toggle
├── README.md                   # This documentation
├── templates/
│   ├── cis_template.html       # CIS dashboard template (840 lines)
│   └── fsbp_template.html      # FSBP dashboard template (830 lines)
├── data/
│   └── main/                   # Main format CSV files
│       ├── report_indupro-acct1.csv
│       ├── report_indupro-acct1_12_17_25.csv
│       ├── report_indupro-acct2.csv
│       ├── report_indupro-acct2_12_17_25.csv
│       ├── fsbp_report_indupro-acct1.csv
│       ├── fsbp_report_indupro-acct1_12_17_25.csv
│       ├── fsbp_report_indupro-acct2.csv
│       └── fsbp_report_indupro-acct2_12_17_25.csv
└── output/                     # Generated dashboards
    ├── cis_dashboard.html      # ~800KB with embedded data
    └── fsbp_dashboard.html     # ~1.4MB with embedded data
```

---

## Technical Architecture

### Data Flow

```
Prowler CSV Files
       │
       ▼
┌─────────────────┐
│   generate.py   │
│                 │
│ 1. Parse CSV    │
│ 2. Detect format│
│ 3. Normalize    │
│ 4. Group by date│
│ 5. Calculate Δ  │
│ 6. Compute stats│
│ 7. Inject JSON  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  HTML Template  │
│                 │
│ + Embedded JSON │
│ + CSS Styles    │
│ + JavaScript    │
└────────┬────────┘
         │
         ▼
   Self-Contained
   HTML Dashboard
```

### Key Functions in generate.py

| Function | Purpose |
|----------|---------|
| `parse_csv()` | Read semicolon-delimited Prowler CSV |
| `detect_format()` | Identify main vs compliance format |
| `detect_framework()` | Determine CIS or FSBP from content |
| `normalize_row()` | Convert to common internal format |
| `calculate_delta()` | Compare scans, mark fixed/new-fail |
| `compute_stats()` | Aggregate counts including severity |
| `compute_by_account()` | Group stats by AWS account |
| `compute_by_service()` | Group stats by AWS service |
| `extract_finding()` | Extract display fields for table |
| `sort_findings()` | Sort by severity, then status, then ID |
| `generate_html()` | Inject JSON data into template |

### Template Structure

Both CIS and FSBP templates follow the same architecture:

```html
<!DOCTYPE html>
<html>
<head>
    <style>
        /* CSS Variables for theming */
        :root, [data-theme="dark"] { ... }
        [data-theme="light"] { ... }

        /* Component styles */
        .summary-card { ... }
        .severity-badge { ... }
        /* ... */
    </style>
</head>
<body>
    <!-- Header with theme toggle -->
    <!-- Executive Summary Grid -->
    <!-- Severity Grid -->
    <!-- Charts Row -->
    <!-- Filters Bar -->
    <!-- Findings Table -->
    <!-- Detail Modal -->

    <script>
        /*__DATA__*/  <!-- Replaced with: const DATA = {...}; -->

        // State management
        let filtered = [];
        let activeCardFilter = null;

        // Core functions
        function init() { ... }
        function renderSummary() { ... }
        function renderSeverity() { ... }
        function renderCharts() { ... }
        function applyFilters() { ... }
        function renderTable() { ... }
        function showDetail() { ... }

        // Card filter system
        function setCardFilter(type, value) { ... }
        function clearCardFilter() { ... }

        // Theme management
        function initTheme() { ... }
        function toggleTheme() { ... }
        function setTheme(theme) { ... }

        init();
    </script>
</body>
</html>
```

### Data Structure (Embedded JSON)

```javascript
const DATA = {
    scanInfo: "Comparing Dec 16, 2025 vs Dec 17, 2025",
    framework: "cis",
    stats: {
        total: 692,
        fail: 307,
        pass: 381,
        manual: 4,
        fixed: 7,
        newFail: 0,
        critical: 2,
        high: 35,
        medium: 211,
        low: 59,
        failDelta: -7,
        passDelta: 7,
        hasComparison: true
    },
    byAccount: {
        "acct1": { fail: 180, pass: 220, total: 400 },
        "acct2": { fail: 127, pass: 161, total: 288 }
    },
    byService: [
        { name: "iam", fail: 45 },
        { name: "s3", fail: 32 },
        // ...top 6 services
    ],
    regions: ["us-east-1", "us-west-2", "global"],
    services: ["iam", "s3", "ec2", "cloudtrail", ...],
    accounts: {
        "123456789012": { id: "123456789012", short: "acct1", name: "indupro-acct1" }
    },
    findings: [
        {
            id: "iam_root_mfa_enabled",
            title: "Ensure MFA is enabled for the root account",
            status: "FAIL",
            severity: "critical",
            delta: "unchanged",
            oldStatus: null,
            acctId: "123456789012",
            region: "us-east-1",
            service: "iam",
            resource: "arn:aws:iam::123456789012:root",
            resourceName: "root",
            statusExt: "Root account does not have MFA enabled",
            risk: "Without MFA, the root account is vulnerable...",
            remediation: "1. Sign in to AWS Console\n2. Navigate to IAM...",
            remediationUrl: "https://docs.aws.amazon.com/..."
        },
        // ... all findings
    ]
};
```

---

## Customization

### Theme Colors

Edit CSS variables in templates to customize colors:

```css
:root, [data-theme="dark"] {
    --bg-primary: #0a0a0f;
    --bg-secondary: #12121a;
    --accent-blue: #4a9eff;
    --accent-green: #3dd68c;
    --accent-red: #ff6b6b;
    --severity-critical: #ef4444;
    --severity-high: #f97316;
    --severity-medium: #eab308;
    --severity-low: #3b82f6;
}

[data-theme="light"] {
    --bg-primary: #f5f7fa;
    --bg-secondary: #ffffff;
    /* ... light theme overrides */
}
```

### Adding New Filters

1. Add HTML select element in filters bar
2. Add filter ID to the listener array in `init()`
3. Add filter logic in `applyFilters()`
4. Add reset logic in `resetFilters()`

### Modifying Table Columns

1. Update `<thead>` in HTML
2. Update `renderTable()` function to include new column
3. Update `colspan` in empty state message

---

## Generating Prowler Reports

### Prerequisites

```bash
# Install Prowler
pip install prowler

# Configure AWS credentials
aws configure
```

### Generate Main Format (Recommended)

```bash
# CIS 5.0 Benchmark - Main output with severity
prowler aws -M csv -f us-east-1

# FSBP - Main output with severity
prowler aws --compliance aws_foundational_security_best_practices_aws -M csv
```

### Generate Compliance Format

```bash
# CIS 5.0 Compliance format
prowler aws --compliance cis_5.0_aws -M csv

# FSBP Compliance format
prowler aws --compliance aws_foundational_security_best_practices_aws -M csv
```

### Output Location

Prowler outputs to `output/` by default. Copy files to the dashboard generator's `data/main/` folder.

---

## Changelog

### V2.1 (December 19, 2025)

**New Features:**
- **Tabbed Multi-Account Interface**: Switch between "All Accounts" and per-account views
- Per-account statistics with dedicated stats for each AWS account
- Dynamic charts that recalculate per tab
- Smart account naming (full names for tabs, compact IDs for badges)
- Automatic single-account mode (hides tabs when only one account)

**Technical:**
- Added `compute_account_stats()` function in generate.py
- New `renderTabs()`, `setTab()`, `getActiveStats()`, `getActiveFindings()` functions
- Added `isMultiAccount` and `accountStats` to embedded data
- Tab bar CSS with active states

### V2.0 (December 19, 2025)

**New Features:**
- Severity prioritization (Critical, High, Medium, Low)
- Clickable executive summary cards for instant filtering
- Severity breakdown row with color-coded cards
- "Show All" button when card filter is active
- "Click cards to filter" hint for discoverability
- Risk and remediation display in detail modal
- Severity column in findings table
- Severity dropdown filter

**Improvements:**
- Rewrote `generate.py` for main CSV format support
- Added severity stats to output summary
- Enhanced detail modal with more fields
- Better hover and active states on cards
- Findings sorted by severity, then status

**Technical:**
- Added `activeCardFilter` state management
- New `setCardFilter()` / `clearCardFilter()` functions
- New `renderSeverity()` function
- Updated `applyFilters()` for card filter integration
- CSS variables for severity colors

### V1.0 (December 17, 2025)

- Initial release
- CIS and FSBP dashboard support
- Multi-account comparison
- Dark/light theme toggle
- Interactive filtering
- Detail modals

---

## Support

For issues or feature requests, contact the development team.

---

*Generated with Claude Code - December 2025*
