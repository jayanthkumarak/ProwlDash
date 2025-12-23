#!/usr/bin/env python3
"""
Prowler Dashboard Generator V3

Framework-agnostic dashboard generator for Prowler AWS security scan outputs.
Supports 40+ compliance frameworks including CIS, FSBP, PCI-DSS, HIPAA, NIST, etc.

Usage:
    python generate.py <csv_file> [csv_file2 ...]
    python generate.py data/main/*.csv
    python generate.py --framework PCI-DSS data/*.csv

Features:
    - Auto-detection of compliance framework from CSV content
    - Severity support (critical, high, medium, low)
    - Clickable executive summary cards
    - Comparison between old and new scans
    - Multi-account tabbed interface
    - Framework-specific theming
"""

import csv
import json
import sys
import os
from pathlib import Path
from datetime import datetime
from collections import defaultdict, Counter


# =============================================================================
# FRAMEWORK REGISTRY - Add new frameworks here
# =============================================================================
# Colorblind-friendly palette based on Okabe-Ito
# Reference: https://siegal.bio.nyu.edu/color-palette/
# Core colors: Orange #E69F00, Sky Blue #56B4E9, Bluish Green #009E73,
#              Yellow #F0E442, Blue #0072B2, Vermillion #D55E00, Purple #CC79A7

FRAMEWORK_REGISTRY = {
    # AWS Frameworks
    "cis": {
        "id": "cis",
        "name": "CIS AWS Benchmark",
        "full_name": "CIS Amazon Web Services Foundations Benchmark",
        "icon": "🔒",
        "color": "#0072B2",  # Blue (Okabe-Ito)
        "gradient": "linear-gradient(90deg, #0072B2, #56B4E9)",
        "description": "CIS Amazon Web Services Foundations Benchmark compliance checks.",
        "patterns": ["CIS-", "CIS_"],
    },
    "fsbp": {
        "id": "fsbp",
        "name": "AWS FSBP",
        "full_name": "AWS Foundational Security Best Practices",
        "icon": "🛡️",
        "color": "#E69F00",  # Orange (Okabe-Ito)
        "gradient": "linear-gradient(90deg, #E69F00, #F0E442)",
        "description": "AWS Foundational Security Best Practices standard compliance checks.",
        "patterns": ["AWS-Foundational-Security", "FSBP"],
    },
    "aws-well-architected": {
        "id": "aws-well-architected",
        "name": "Well-Architected",
        "full_name": "AWS Well-Architected Framework",
        "icon": "🏗️",
        "color": "#CC79A7",  # Reddish Purple (Okabe-Ito)
        "gradient": "linear-gradient(90deg, #CC79A7, #D4A5C9)",
        "description": "AWS Well-Architected Framework security pillar checks.",
        "patterns": ["AWS-Well-Architected"],
    },
    # Regulatory Frameworks
    "pci-dss": {
        "id": "pci-dss",
        "name": "PCI DSS",
        "full_name": "Payment Card Industry Data Security Standard",
        "icon": "💳",
        "color": "#009E73",  # Bluish Green (Okabe-Ito)
        "gradient": "linear-gradient(90deg, #009E73, #56B4E9)",
        "description": "PCI DSS compliance checks for payment card security.",
        "patterns": ["PCI-", "PCI_"],
    },
    "hipaa": {
        "id": "hipaa",
        "name": "HIPAA",
        "full_name": "Health Insurance Portability and Accountability Act",
        "icon": "🏥",
        "color": "#CC79A7",  # Reddish Purple (Okabe-Ito)
        "gradient": "linear-gradient(90deg, #CC79A7, #E69F00)",
        "description": "HIPAA compliance checks for healthcare data protection.",
        "patterns": ["HIPAA"],
    },
    "gdpr": {
        "id": "gdpr",
        "name": "GDPR",
        "full_name": "General Data Protection Regulation",
        "icon": "🇪🇺",
        "color": "#0072B2",  # Blue (Okabe-Ito)
        "gradient": "linear-gradient(90deg, #0072B2, #009E73)",
        "description": "GDPR compliance checks for EU data protection.",
        "patterns": ["GDPR"],
    },
    "soc2": {
        "id": "soc2",
        "name": "SOC 2",
        "full_name": "Service Organization Control 2",
        "icon": "📋",
        "color": "#56B4E9",  # Sky Blue (Okabe-Ito)
        "gradient": "linear-gradient(90deg, #56B4E9, #0072B2)",
        "description": "SOC 2 Trust Services Criteria compliance checks.",
        "patterns": ["SOC2", "SOC_2"],
    },
    # NIST Frameworks
    "nist-800-53": {
        "id": "nist-800-53",
        "name": "NIST 800-53",
        "full_name": "NIST Special Publication 800-53",
        "icon": "🏛️",
        "color": "#009E73",  # Bluish Green (Okabe-Ito)
        "gradient": "linear-gradient(90deg, #009E73, #0072B2)",
        "description": "NIST 800-53 security and privacy controls.",
        "patterns": ["NIST-800-53"],
    },
    "nist-csf": {
        "id": "nist-csf",
        "name": "NIST CSF",
        "full_name": "NIST Cybersecurity Framework",
        "icon": "🔐",
        "color": "#56B4E9",  # Sky Blue (Okabe-Ito)
        "gradient": "linear-gradient(90deg, #56B4E9, #009E73)",
        "description": "NIST Cybersecurity Framework compliance checks.",
        "patterns": ["NIST-CSF"],
    },
    "nist-800-171": {
        "id": "nist-800-171",
        "name": "NIST 800-171",
        "full_name": "NIST Special Publication 800-171",
        "icon": "🔏",
        "color": "#0072B2",  # Blue (Okabe-Ito)
        "gradient": "linear-gradient(90deg, #0072B2, #56B4E9)",
        "description": "NIST 800-171 CUI protection controls.",
        "patterns": ["NIST-800-171"],
    },
    # International Standards
    "iso27001": {
        "id": "iso27001",
        "name": "ISO 27001",
        "full_name": "ISO/IEC 27001 Information Security",
        "icon": "🌐",
        "color": "#CC79A7",  # Reddish Purple (Okabe-Ito)
        "gradient": "linear-gradient(90deg, #CC79A7, #56B4E9)",
        "description": "ISO 27001 information security management checks.",
        "patterns": ["ISO27001", "ISO-27001"],
    },
    # Government Frameworks
    "fedramp": {
        "id": "fedramp",
        "name": "FedRAMP",
        "full_name": "Federal Risk and Authorization Management Program",
        "icon": "🦅",
        "color": "#D55E00",  # Vermillion (Okabe-Ito)
        "gradient": "linear-gradient(90deg, #D55E00, #E69F00)",
        "description": "FedRAMP compliance for US federal cloud services.",
        "patterns": ["FedRAMP", "FedRamp"],
    },
    "cisa": {
        "id": "cisa",
        "name": "CISA",
        "full_name": "Cybersecurity and Infrastructure Security Agency",
        "icon": "🛡️",
        "color": "#0072B2",  # Blue (Okabe-Ito)
        "gradient": "linear-gradient(90deg, #0072B2, #56B4E9)",
        "description": "CISA cybersecurity best practices.",
        "patterns": ["CISA"],
    },
    # Other Frameworks
    "mitre-attack": {
        "id": "mitre-attack",
        "name": "MITRE ATT&CK",
        "full_name": "MITRE ATT&CK Framework",
        "icon": "⚔️",
        "color": "#D55E00",  # Vermillion (Okabe-Ito)
        "gradient": "linear-gradient(90deg, #D55E00, #CC79A7)",
        "description": "MITRE ATT&CK adversarial tactics and techniques.",
        "patterns": ["MITRE-ATTACK", "MITRE_ATTACK"],
    },
    "ens": {
        "id": "ens",
        "name": "ENS",
        "full_name": "Esquema Nacional de Seguridad (Spain)",
        "icon": "🇪🇸",
        "color": "#E69F00",  # Orange (Okabe-Ito)
        "gradient": "linear-gradient(90deg, #E69F00, #F0E442)",
        "description": "Spanish National Security Scheme compliance.",
        "patterns": ["ENS-"],
    },
    "kisa": {
        "id": "kisa",
        "name": "KISA ISMS-P",
        "full_name": "Korea Internet & Security Agency ISMS-P",
        "icon": "🇰🇷",
        "color": "#56B4E9",  # Sky Blue (Okabe-Ito)
        "gradient": "linear-gradient(90deg, #56B4E9, #0072B2)",
        "description": "Korean ISMS-P information security certification.",
        "patterns": ["KISA-ISMS"],
    },
    "ffiec": {
        "id": "ffiec",
        "name": "FFIEC",
        "full_name": "Federal Financial Institutions Examination Council",
        "icon": "🏦",
        "color": "#009E73",  # Bluish Green (Okabe-Ito)
        "gradient": "linear-gradient(90deg, #009E73, #56B4E9)",
        "description": "FFIEC cybersecurity assessment for financial institutions.",
        "patterns": ["FFIEC"],
    },
    "rbi": {
        "id": "rbi",
        "name": "RBI CSF",
        "full_name": "Reserve Bank of India Cyber Security Framework",
        "icon": "🇮🇳",
        "color": "#E69F00",  # Orange (Okabe-Ito)
        "gradient": "linear-gradient(90deg, #E69F00, #D55E00)",
        "description": "RBI Cyber Security Framework for Indian banks.",
        "patterns": ["RBI-"],
    },
    "nis2": {
        "id": "nis2",
        "name": "NIS2",
        "full_name": "Network and Information Security Directive 2",
        "icon": "🇪🇺",
        "color": "#0072B2",  # Blue (Okabe-Ito)
        "gradient": "linear-gradient(90deg, #0072B2, #009E73)",
        "description": "EU NIS2 Directive cybersecurity requirements.",
        "patterns": ["NIS2"],
    },
    "c5": {
        "id": "c5",
        "name": "BSI C5",
        "full_name": "Cloud Computing Compliance Criteria Catalogue",
        "icon": "🇩🇪",
        "color": "#999999",  # Grey (Okabe-Ito)
        "gradient": "linear-gradient(90deg, #999999, #56B4E9)",
        "description": "German BSI C5 cloud security attestation.",
        "patterns": ["C5-"],
    },
    "gxp": {
        "id": "gxp",
        "name": "GxP",
        "full_name": "Good Practice Guidelines",
        "icon": "💊",
        "color": "#009E73",  # Bluish Green (Okabe-Ito)
        "gradient": "linear-gradient(90deg, #009E73, #E69F00)",
        "description": "GxP compliance for life sciences.",
        "patterns": ["GxP-", "GXP"],
    },
}

# Default framework for unknown types
DEFAULT_FRAMEWORK = {
    "id": "generic",
    "name": "Security Scan",
    "full_name": "Prowler Security Scan Results",
    "icon": "🔍",
    "color": "#999999",  # Grey (Okabe-Ito)
    "gradient": "linear-gradient(90deg, #999999, #56B4E9)",
    "description": "Prowler security scan compliance checks.",
    "patterns": [],
}


def parse_csv(filepath: str) -> list[dict]:
    """Parse semicolon-delimited Prowler CSV."""
    rows = []
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            rows.append(row)
    return rows


def detect_format(rows: list[dict]) -> str:
    """Detect CSV format: 'main' (with SEVERITY) or 'compliance' (framework-specific)."""
    if not rows:
        return "unknown"
    if "SEVERITY" in rows[0] and "CHECK_ID" in rows[0]:
        return "main"
    if "REQUIREMENTS_ID" in rows[0]:
        return "compliance"
    return "main"


def get_framework_info(framework_id: str) -> dict:
    """Get framework metadata from registry, with fallback to default."""
    # Normalize the framework ID
    fw_lower = framework_id.lower().strip()

    # Direct match
    if fw_lower in FRAMEWORK_REGISTRY:
        return FRAMEWORK_REGISTRY[fw_lower]

    # Pattern matching for aliases
    for fw_id, fw_info in FRAMEWORK_REGISTRY.items():
        for pattern in fw_info.get("patterns", []):
            if pattern.lower() in fw_lower or fw_lower in pattern.lower():
                return fw_info

    # Return default with customized name
    default = DEFAULT_FRAMEWORK.copy()
    default["id"] = fw_lower
    default["name"] = framework_id
    default["full_name"] = framework_id
    return default


def extract_frameworks_from_compliance(compliance_str: str) -> list[str]:
    """Extract framework names from COMPLIANCE column.

    Format: "CIS-5.0: 1.1 | HIPAA: 164_308 | PCI-4.0: 8.3.10"
    Returns: ["CIS-5.0", "HIPAA", "PCI-4.0"]
    """
    if not compliance_str:
        return []

    frameworks = []
    # Split by pipe separator
    parts = compliance_str.split("|")
    for part in parts:
        part = part.strip()
        if ":" in part:
            # Format: "Framework: Control_ID"
            fw_name = part.split(":")[0].strip()
            if fw_name:
                frameworks.append(fw_name)
    return frameworks


def detect_primary_framework(rows: list[dict], filepath: str = "", user_framework: str = None) -> str:
    """Detect the primary framework from CSV content.

    Priority:
    1. User-specified framework (--framework flag)
    2. Framework from filename (most reliable indicator)
    3. Framework from COMPLIANCE column analysis
    4. Default to 'cis'
    """
    # User override takes precedence
    if user_framework:
        # Normalize user input
        user_fw = user_framework.lower().strip()
        # Check if it matches a known framework
        for fw_id in FRAMEWORK_REGISTRY:
            if user_fw == fw_id or user_fw in fw_id:
                return fw_id
            for pattern in FRAMEWORK_REGISTRY[fw_id].get("patterns", []):
                if user_fw in pattern.lower():
                    return fw_id
        return user_fw

    # Try filename detection FIRST - most reliable indicator
    # Filename typically contains the primary framework (e.g., fsbp_report.csv, cis_scan.csv)
    if filepath:
        name = os.path.basename(filepath).lower()
        # Check if filename explicitly mentions a framework
        for fw_id, fw_info in FRAMEWORK_REGISTRY.items():
            for pattern in fw_info.get("patterns", []):
                if pattern.lower().replace("-", "").replace("_", "") in name.replace("-", "").replace("_", ""):
                    return fw_id

    if not rows:
        return "cis"  # Default

    # Analyze COMPLIANCE column - look for frameworks across all entries
    framework_counts = Counter()

    for row in rows[:100]:  # Sample first 100 rows
        compliance = row.get("COMPLIANCE", "")
        frameworks = extract_frameworks_from_compliance(compliance)
        # Count ALL frameworks mentioned, not just the first
        for fw_name in frameworks:
            # Normalize to registry ID
            for fw_id, fw_info in FRAMEWORK_REGISTRY.items():
                for pattern in fw_info.get("patterns", []):
                    if pattern.upper() in fw_name.upper():
                        framework_counts[fw_id] += 1
                        break
                else:
                    continue
                break

    if framework_counts:
        # Return the most common framework
        return framework_counts.most_common(1)[0][0]

    return "cis"  # Default fallback


def detect_framework_from_filename(filepath: str) -> str:
    """Detect framework from filename."""
    name = os.path.basename(filepath).lower()

    # Check against all patterns in registry
    for fw_id, fw_info in FRAMEWORK_REGISTRY.items():
        for pattern in fw_info.get("patterns", []):
            if pattern.lower().replace("-", "").replace("_", "") in name.replace("-", "").replace("_", ""):
                return fw_id

    # Legacy detection
    if "fsbp" in name or "foundational" in name:
        return "fsbp"
    if "hipaa" in name:
        return "hipaa"
    if "pci" in name:
        return "pci-dss"
    if "nist" in name:
        return "nist-800-53"
    if "soc2" in name or "soc_2" in name:
        return "soc2"

    return "cis"  # Default


def detect_framework(rows: list[dict], filepath: str = "") -> str:
    """Detect framework from CSV content or filename (backward compatible)."""
    return detect_primary_framework(rows, filepath)


def get_scan_date(rows: list[dict]) -> str:
    """Extract scan date from first row."""
    if not rows:
        return "Unknown"

    # Try TIMESTAMP (main format)
    date_str = rows[0].get("TIMESTAMP", "") or rows[0].get("ASSESSMENTDATE", "")
    if date_str:
        try:
            # Handle various date formats
            dt = datetime.fromisoformat(date_str.split(".")[0].replace("Z", ""))
            return dt.strftime("%b %d, %Y")
        except ValueError:
            pass
    return "Unknown"


def normalize_row(row: dict, csv_format: str) -> dict:
    """Normalize row to common format regardless of CSV type."""
    if csv_format == "main":
        return {
            "acctId": row.get("ACCOUNT_UID", ""),
            "acctName": row.get("ACCOUNT_NAME", ""),
            "region": row.get("REGION", ""),
            "checkId": row.get("CHECK_ID", ""),
            "checkTitle": row.get("CHECK_TITLE", ""),
            "status": row.get("STATUS", ""),
            "statusExt": row.get("STATUS_EXTENDED", ""),
            "severity": row.get("SEVERITY", "").lower(),
            "service": row.get("SERVICE_NAME", ""),
            "resourceId": row.get("RESOURCE_UID", ""),
            "resourceName": row.get("RESOURCE_NAME", ""),
            "risk": row.get("RISK", ""),
            "remediation": row.get("REMEDIATION_RECOMMENDATION_TEXT", ""),
            "remediationUrl": row.get("REMEDIATION_RECOMMENDATION_URL", ""),
            "compliance": row.get("COMPLIANCE", ""),
            "_raw": row,
        }
    else:
        # Compliance format
        return {
            "acctId": row.get("ACCOUNTID", ""),
            "acctName": "",
            "region": row.get("REGION", ""),
            "checkId": row.get("REQUIREMENTS_ID", ""),
            "checkTitle": row.get("REQUIREMENTS_DESCRIPTION", ""),
            "status": row.get("STATUS", ""),
            "statusExt": row.get("STATUSEXTENDED", ""),
            "severity": "",  # Not available in compliance format
            "service": row.get("REQUIREMENTS_ATTRIBUTES_SERVICE", "") or row.get("REQUIREMENTS_ATTRIBUTES_SECTION", ""),
            "resourceId": row.get("RESOURCEID", ""),
            "resourceName": row.get("RESOURCENAME", ""),
            "risk": "",
            "remediation": row.get("REQUIREMENTS_ATTRIBUTES_REMEDIATIONPROCEDURE", ""),
            "remediationUrl": "",
            "compliance": row.get("FRAMEWORK", ""),
            "profile": row.get("REQUIREMENTS_ATTRIBUTES_PROFILE", ""),
            "section": row.get("REQUIREMENTS_ATTRIBUTES_SECTION", ""),
            "rationale": row.get("REQUIREMENTS_ATTRIBUTES_RATIONALESTATEMENT", ""),
            "_raw": row,
        }


def create_key(row: dict) -> str:
    """Create unique key for finding comparison."""
    return f"{row['acctId']}|{row['region']}|{row['checkId']}|{row['resourceId']}"


def calculate_delta(new_rows: list[dict], old_rows: list[dict]) -> list[dict]:
    """Compare scans and mark delta status."""
    if not old_rows:
        return [dict(r, delta="unchanged", oldStatus=None) for r in new_rows]

    old_map = {create_key(r): r for r in old_rows}
    results = []

    for row in new_rows:
        key = create_key(row)
        old = old_map.get(key)
        delta = "unchanged"
        old_status = None

        if old:
            old_status = old.get("status")
            if old_status == "FAIL" and row.get("status") == "PASS":
                delta = "fixed"
            elif old_status == "PASS" and row.get("status") == "FAIL":
                delta = "new-fail"
        elif row.get("status") == "FAIL":
            delta = "new-fail"

        results.append(dict(row, delta=delta, oldStatus=old_status))

    return results


def compute_stats(data: list[dict], old_data: list[dict]) -> dict:
    """Compute aggregate statistics including severity breakdown."""
    stats = {
        "total": len(data),
        "fail": sum(1 for r in data if r.get("status") == "FAIL"),
        "pass": sum(1 for r in data if r.get("status") == "PASS"),
        "manual": sum(1 for r in data if r.get("status") == "MANUAL"),
        "fixed": sum(1 for r in data if r.get("delta") == "fixed"),
        "newFail": sum(1 for r in data if r.get("delta") == "new-fail"),
        # Severity breakdown (for failures only)
        "critical": sum(1 for r in data if r.get("status") == "FAIL" and r.get("severity") == "critical"),
        "high": sum(1 for r in data if r.get("status") == "FAIL" and r.get("severity") == "high"),
        "medium": sum(1 for r in data if r.get("status") == "FAIL" and r.get("severity") == "medium"),
        "low": sum(1 for r in data if r.get("status") == "FAIL" and r.get("severity") == "low"),
    }

    if old_data:
        old_fail = sum(1 for r in old_data if r.get("status") == "FAIL")
        old_pass = sum(1 for r in old_data if r.get("status") == "PASS")
        stats["failDelta"] = stats["fail"] - old_fail
        stats["passDelta"] = stats["pass"] - old_pass
        stats["hasComparison"] = True
    else:
        stats["failDelta"] = 0
        stats["passDelta"] = 0
        stats["hasComparison"] = False

    return stats


def get_accounts(data: list[dict]) -> dict:
    """Extract unique accounts - uses account ID as primary identifier."""
    accounts = {}
    acct_counter = 0
    for r in data:
        acct_id = r.get("acctId", "")
        if acct_id and acct_id not in accounts:
            acct_counter += 1
            raw_name = r.get("acctName") or ""

            # Always use account ID for display (clearer, more consistent)
            display = acct_id

            # Short name for badges - last 4 digits
            short = f"...{acct_id[-4:]}" if len(acct_id) >= 4 else acct_id

            accounts[acct_id] = {
                "id": acct_id,
                "short": short,        # For badges/tags (compact)
                "display": display,    # For tabs/headers (account ID)
                "name": raw_name or acct_id  # Original name for reference
            }
    return accounts


def compute_by_account(data: list[dict], accounts: dict) -> dict:
    """Stats grouped by account for charts (uses display names)."""
    by_acct = defaultdict(lambda: {"fail": 0, "pass": 0, "total": 0})
    for r in data:
        acct_id = r.get("acctId", "unknown")
        # Use short name for chart labels
        key = accounts.get(acct_id, {}).get("short", acct_id)
        by_acct[key]["total"] += 1
        if r.get("status") == "FAIL":
            by_acct[key]["fail"] += 1
        elif r.get("status") == "PASS":
            by_acct[key]["pass"] += 1
    return dict(by_acct)


def compute_account_stats(data: list[dict], accounts: dict) -> dict:
    """Compute full stats for each account (for tabs)."""
    account_stats = {}

    for acct_id in accounts.keys():
        acct_data = [r for r in data if r.get("acctId") == acct_id]
        if not acct_data:
            continue

        account_stats[acct_id] = {
            "total": len(acct_data),
            "fail": sum(1 for r in acct_data if r.get("status") == "FAIL"),
            "pass": sum(1 for r in acct_data if r.get("status") == "PASS"),
            "manual": sum(1 for r in acct_data if r.get("status") == "MANUAL"),
            "fixed": sum(1 for r in acct_data if r.get("delta") == "fixed"),
            "newFail": sum(1 for r in acct_data if r.get("delta") == "new-fail"),
            "critical": sum(1 for r in acct_data if r.get("status") == "FAIL" and r.get("severity") == "critical"),
            "high": sum(1 for r in acct_data if r.get("status") == "FAIL" and r.get("severity") == "high"),
            "medium": sum(1 for r in acct_data if r.get("status") == "FAIL" and r.get("severity") == "medium"),
            "low": sum(1 for r in acct_data if r.get("status") == "FAIL" and r.get("severity") == "low"),
        }

    return account_stats


def compute_by_service(data: list[dict]) -> list[dict]:
    """Stats grouped by service, top 6."""
    by_svc = defaultdict(lambda: {"fail": 0, "pass": 0})
    for r in data:
        svc = r.get("service") or "Unknown"
        if r.get("status") == "FAIL":
            by_svc[svc]["fail"] += 1
        elif r.get("status") == "PASS":
            by_svc[svc]["pass"] += 1

    sorted_svcs = sorted(by_svc.items(), key=lambda x: x[1]["fail"], reverse=True)[:6]
    return [{"name": n, **v} for n, v in sorted_svcs]


def compute_by_severity(data: list[dict]) -> list[dict]:
    """Stats grouped by severity (failures only)."""
    severity_order = ["critical", "high", "medium", "low"]
    by_sev = {s: 0 for s in severity_order}

    for r in data:
        if r.get("status") == "FAIL":
            sev = r.get("severity", "").lower()
            if sev in by_sev:
                by_sev[sev] += 1

    return [{"name": s, "count": by_sev[s]} for s in severity_order]


def extract_finding(row: dict) -> dict:
    """Extract fields needed for display."""
    return {
        "id": row.get("checkId", ""),
        "title": row.get("checkTitle", ""),
        "status": row.get("status", ""),
        "severity": row.get("severity", ""),
        "delta": row.get("delta", "unchanged"),
        "oldStatus": row.get("oldStatus"),
        "acctId": row.get("acctId", ""),
        "region": row.get("region", ""),
        "service": row.get("service", ""),
        "resource": row.get("resourceId", ""),
        "resourceName": row.get("resourceName", ""),
        "statusExt": row.get("statusExt", ""),
        "risk": row.get("risk", ""),
        "remediation": row.get("remediation", ""),
        "remediationUrl": row.get("remediationUrl", ""),
        # CIS-specific (from compliance format)
        "profile": row.get("profile", ""),
        "section": row.get("section", ""),
        "rationale": row.get("rationale", ""),
    }


def sort_findings(findings: list[dict]) -> list[dict]:
    """Sort: By severity (critical first), then status (FAIL first), then by ID."""
    severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3, "": 4}
    status_order = {"FAIL": 0, "MANUAL": 1, "PASS": 2}
    return sorted(findings, key=lambda x: (
        severity_order.get(x["severity"], 4),
        status_order.get(x["status"], 9),
        x["id"]
    ))


def generate_html(data: dict, framework: str) -> str:
    """Generate complete HTML with embedded data."""
    template = get_template(framework)
    json_data = json.dumps(data, separators=(",", ":"))
    return template.replace("/*__DATA__*/", f"const DATA = {json_data};")


def get_template(framework: str) -> str:
    """Return the universal HTML dashboard template.

    Uses a single template that dynamically adapts to any framework
    via DATA.frameworkInfo passed at generation time.
    """
    script_dir = Path(__file__).parent
    
    # Universal template works for all frameworks
    template_file = script_dir / "templates" / "dashboard_template.html"
    if template_file.exists():
        return template_file.read_text(encoding="utf-8")

    raise FileNotFoundError(f"Dashboard template not found. Expected: {template_file}")



def show_help():
    """Display comprehensive help information."""
    help_text = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                    PROWLER DASHBOARD GENERATOR V3                            ║
╚══════════════════════════════════════════════════════════════════════════════╝

DESCRIPTION
  Framework-agnostic dashboard generator for Prowler AWS security scan outputs.
  Auto-detects and supports 20+ compliance frameworks including:
    CIS, FSBP, PCI-DSS, HIPAA, NIST, SOC2, ISO27001, GDPR, FedRAMP, and more.

USAGE
  python3 generate.py [OPTIONS] <csv_file> [csv_file2 ...]

OPTIONS
  --help, -h              Show this help message
  --version, -v           Show version information
  --output, -o <path>     Output directory (default: ./output)
  --framework, -f <name>  Force specific framework (auto-detected if omitted)
  --no-timestamp          Don't create timestamped subfolder
  --list-frameworks       List all supported frameworks

EXAMPLES
  # Auto-detect framework from CSV content
  python3 generate.py report.csv

  # Process multiple files (grouped by detected framework)
  python3 generate.py data/main/*.csv

  # Force specific framework
  python3 generate.py --framework hipaa hipaa_report.csv

  # Custom output directory
  python3 generate.py -o /path/to/reports data/main/*.csv

FRAMEWORK AUTO-DETECTION
  The generator detects frameworks from:
  1. COMPLIANCE column in CSV (e.g., "CIS-5.0: 1.1 | HIPAA: 164_308")
  2. Filename patterns (e.g., "pci_report.csv" → PCI-DSS)
  3. --framework flag (overrides auto-detection)

SUPPORTED FRAMEWORKS
  AWS:        CIS, FSBP, Well-Architected
  Regulatory: PCI-DSS, HIPAA, GDPR, SOC2, FFIEC
  NIST:       800-53, 800-171, CSF
  Government: FedRAMP, CISA, ENS (Spain), NIS2 (EU)
  Other:      ISO27001, MITRE ATT&CK, KISA, RBI, GxP, C5

OUTPUT STRUCTURE
  output/
  ├── 2025-12-19_143052/
  │   ├── index.html              <- Landing page
  │   ├── cis_dashboard.html      <- Auto-detected framework
  │   └── pci-dss_dashboard.html  <- Another framework
  └── ...

CSV FORMAT
  Use Prowler's main output format (includes SEVERITY column):
    prowler aws --output-formats csv

  Required columns: ACCOUNT_UID, CHECK_ID, STATUS, SEVERITY

DASHBOARD FEATURES
  • Executive Summary    - Clickable cards (failures, passes, fixed, new)
  • Severity Breakdown   - Critical/High/Medium/Low failure counts
  • Analysis Charts      - By severity, account, service
  • Findings Table       - Sortable, filterable, searchable
  • Detail Panel         - Risk info and remediation guidance
  • Dark/Light Theme     - Toggle with localStorage persistence
  • Multi-Account Tabs   - Switch between accounts or combined view

For detailed documentation, see README.md
"""
    print(help_text)


def list_frameworks():
    """List all supported frameworks."""
    print("\nSupported Compliance Frameworks:")
    print("=" * 60)
    for fw_id, fw_info in sorted(FRAMEWORK_REGISTRY.items()):
        print(f"  {fw_info['icon']}  {fw_id:<20} {fw_info['name']}")
    print("\nUse --framework <id> to force a specific framework.")
    print("Example: python3 generate.py --framework hipaa report.csv\n")


def show_version():
    """Display version information."""
    print("Prowler Dashboard Generator V3.0")
    print(f"Supports {len(FRAMEWORK_REGISTRY)}+ compliance frameworks")
    print("Python 3.8+ required (no external dependencies)")


def generate_landing_page(generated_files: list, scan_info: str, stats_by_fw: dict) -> str:
    """Generate a landing page HTML linking to the dashboards."""

    cards_html = ""
    card_styles = ""

    for fw, path, fw_info in generated_files:
        filename = os.path.basename(path)
        stats = stats_by_fw.get(fw, {})

        # Use framework info from registry
        icon = fw_info.get('icon', '🔍')
        title = fw_info.get('name', fw.upper())
        desc = fw_info.get('description', f'{fw.upper()} compliance checks.')
        color = fw_info.get('color', '#6b7280')
        gradient = fw_info.get('gradient', f'linear-gradient(90deg, {color}, {color})')

        fail_count = stats.get('fail', 0)
        pass_count = stats.get('pass', 0)

        # Add dynamic card style for this framework
        card_styles += f'''
        .card.{fw}::before {{ background: {gradient}; }}
        .card.{fw} h2 {{ color: {color}; }}
'''

        cards_html += f'''
        <a href="{filename}" class="card {fw}">
            <div class="card-icon">{icon}</div>
            <h2>{title}</h2>
            <p>{desc}</p>
            <div class="card-meta">
                <span class="fail">{fail_count} Failed</span>
                <span class="pass">{pass_count} Passed</span>
            </div>
        </a>
'''

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AWS Compliance Dashboards</title>
    <style>
        :root, [data-theme="dark"] {{
            --bg-primary: #0a0a0f;
            --bg-secondary: #12121a;
            --bg-hover: #22222e;
            --border: #2a2a38;
            --text-primary: #f0f0f5;
            --text-secondary: #9090a0;
            --text-muted: #606070;
        }}
        [data-theme="light"] {{
            --bg-primary: #f5f7fa;
            --bg-secondary: #ffffff;
            --bg-hover: #dfe4eb;
            --border: #d1d9e6;
            --text-primary: #1a1f36;
            --text-secondary: #4a5568;
            --text-muted: #718096;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 40px 20px;
        }}
        .top-bar {{ position: fixed; top: 20px; right: 20px; }}
        .theme-toggle {{
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 8px 14px;
            color: var(--text-secondary);
            font-size: 13px;
            cursor: pointer;
        }}
        .theme-toggle:hover {{ background: var(--bg-hover); color: var(--text-primary); }}
        .logo {{ font-size: 14px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 2px; margin-bottom: 12px; }}
        h1 {{ font-size: 36px; font-weight: 600; letter-spacing: -1px; margin-bottom: 8px; text-align: center; }}
        .subtitle {{ color: var(--text-secondary); font-size: 16px; margin-bottom: 50px; text-align: center; }}
        .cards {{ display: flex; gap: 24px; flex-wrap: wrap; justify-content: center; }}
        .card {{
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 32px 40px;
            width: 340px;
            text-decoration: none;
            color: inherit;
            transition: all 0.2s ease;
            position: relative;
            overflow: hidden;
        }}
        .card::before {{ content: ''; position: absolute; top: 0; left: 0; right: 0; height: 4px; }}
        .card:hover {{ transform: translateY(-4px); border-color: var(--text-muted); box-shadow: 0 20px 40px rgba(0,0,0,0.3); }}
        .card-icon {{ font-size: 48px; margin-bottom: 20px; }}
        .card h2 {{ font-size: 20px; font-weight: 600; margin-bottom: 8px; }}
        /* Dynamic framework styles */
{card_styles}
        .card p {{ color: var(--text-secondary); font-size: 14px; line-height: 1.5; margin-bottom: 20px; }}
        .card-meta {{ display: flex; gap: 16px; font-size: 12px; color: var(--text-muted); }}
        .card-meta .fail {{ color: #D55E00; }}  /* Vermillion (Okabe-Ito) */
        .card-meta .pass {{ color: #009E73; }}  /* Bluish Green (Okabe-Ito) */
        .footer {{ margin-top: 60px; text-align: center; color: var(--text-muted); font-size: 12px; }}
    </style>
</head>
<body>
    <div class="top-bar">
        <button class="theme-toggle" onclick="toggleTheme()">Toggle Theme</button>
    </div>
    <div class="logo">Indupro</div>
    <h1>AWS Compliance Dashboards</h1>
    <p class="subtitle">{scan_info}</p>
    <div class="cards">{cards_html}
    </div>
    <div class="footer">
        <p>Generated by Prowler Dashboard Generator</p>
    </div>
    <script>
        function toggleTheme() {{
            const current = document.documentElement.getAttribute('data-theme') || 'dark';
            const next = current === 'dark' ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', next);
            localStorage.setItem('theme', next);
        }}
        const saved = localStorage.getItem('theme');
        if (saved) document.documentElement.setAttribute('data-theme', saved);
    </script>
</body>
</html>'''
    return html


def parse_args(argv: list) -> dict:
    """Parse command line arguments."""
    args = {
        'files': [],
        'output': None,
        'framework': None,
        'no_timestamp': False,
        'list_frameworks': False,
    }

    i = 1
    while i < len(argv):
        arg = argv[i]
        if arg in ('--output', '-o'):
            if i + 1 < len(argv):
                args['output'] = argv[i + 1]
                i += 2
                continue
            else:
                print("Error: --output requires a path argument")
                sys.exit(1)
        elif arg in ('--framework', '-f'):
            if i + 1 < len(argv):
                args['framework'] = argv[i + 1]
                i += 2
                continue
            else:
                print("Error: --framework requires a framework name")
                sys.exit(1)
        elif arg == '--no-timestamp':
            args['no_timestamp'] = True
        elif arg == '--list-frameworks':
            args['list_frameworks'] = True
        elif not arg.startswith('-'):
            args['files'].append(arg)
        i += 1

    return args


def main():
    # Handle help and version flags
    if len(sys.argv) < 2 or any(arg in sys.argv for arg in ['--help', '-h']):
        show_help()
        sys.exit(0 if '--help' in sys.argv or '-h' in sys.argv else 1)

    if any(arg in sys.argv for arg in ['--version', '-v']):
        show_version()
        sys.exit(0)

    if '--list-frameworks' in sys.argv:
        list_frameworks()
        sys.exit(0)

    # Parse arguments
    args = parse_args(sys.argv)
    files = args['files']
    user_framework = args.get('framework')

    if args.get('list_frameworks'):
        list_frameworks()
        sys.exit(0)

    if not files:
        print("Error: No CSV files provided")
        show_help()
        sys.exit(1)

    print(f"Processing {len(files)} file(s)...")

    # Group files by framework (dynamic, not hardcoded)
    framework_files = defaultdict(list)  # {framework_id: [(filepath, rows, scan_date), ...]}

    for f in files:
        if not os.path.exists(f):
            print(f"  Warning: {f} not found, skipping")
            continue

        rows = parse_csv(f)
        if not rows:
            print(f"  Warning: {f} is empty, skipping")
            continue

        csv_format = detect_format(rows)

        # Detect framework - user override takes precedence
        if user_framework:
            fw = detect_primary_framework(rows, f, user_framework)
        else:
            fw = detect_primary_framework(rows, f)

        scan_date = get_scan_date(rows)

        # Normalize rows
        normalized = [normalize_row(r, csv_format) for r in rows]

        # Get framework display name
        fw_info = get_framework_info(fw)
        print(f"  {os.path.basename(f)}: {fw_info['name']}, {csv_format} format, {len(rows)} rows, {scan_date}")

        framework_files[fw].append((f, normalized, scan_date))

    # Determine output directory
    if args['output']:
        base_output = Path(args['output'])
    else:
        base_output = Path(__file__).parent / "output"

    # Create timestamped subfolder by default
    if args['no_timestamp']:
        output_dir = base_output
    else:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        output_dir = base_output / timestamp

    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"\nOutput directory: {output_dir}")

    generated = []  # List of (framework_id, path, fw_info) tuples
    stats_by_fw = {}  # Store stats for landing page
    scan_info_combined = ""

    # Process each detected framework
    for fw, file_list in framework_files.items():
        if not file_list:
            continue

        fw_info = get_framework_info(fw)
        print(f"\nGenerating {fw_info['name']} dashboard...")

        # Group files by scan date
        date_groups = {}
        for filepath, rows, scan_date in file_list:
            if scan_date not in date_groups:
                date_groups[scan_date] = []
            date_groups[scan_date].extend(rows)

        sorted_dates = sorted(
            date_groups.keys(),
            key=lambda d: datetime.strptime(d, "%b %d, %Y") if d != "Unknown" else datetime.min
        )

        if len(sorted_dates) >= 2:
            old_date = sorted_dates[0]
            new_date = sorted_dates[-1]
            old_rows = date_groups[old_date]
            new_rows = date_groups[new_date]
            scan_info = f"Comparing {old_date} vs {new_date}"
            print(f"  Old scan ({old_date}): {len(old_rows)} rows")
            print(f"  New scan ({new_date}): {len(new_rows)} rows")
        else:
            new_date = sorted_dates[0]
            new_rows = date_groups[new_date]
            old_rows = []
            scan_info = f"Scan: {new_date}"

        # Process
        data = calculate_delta(new_rows, old_rows)
        accounts = get_accounts(data)

        stats = compute_stats(data, old_rows)
        by_account = compute_by_account(data, accounts)
        by_service = compute_by_service(data)
        by_severity = compute_by_severity(data)
        account_stats = compute_account_stats(data, accounts)  # Per-account stats for tabs
        regions = sorted(set(r.get("region", "") for r in data if r.get("region")))
        services = sorted(set(r.get("service", "") for r in data if r.get("service")))

        findings = [extract_finding(r) for r in data]
        for f in findings:
            f["acct"] = accounts.get(f["acctId"], {}).get("short", "unknown")
        findings = sort_findings(findings)

        # Determine if multi-account mode
        is_multi_account = len(accounts) > 1

        dashboard_data = {
            "scanInfo": scan_info,
            "framework": fw,
            "frameworkInfo": fw_info,  # Include framework metadata
            "stats": stats,
            "accountStats": account_stats,  # Per-account stats for tabs
            "isMultiAccount": is_multi_account,
            "byAccount": by_account,
            "byService": by_service,
            "bySeverity": by_severity,
            "regions": regions,
            "services": services,
            "accounts": accounts,
            "findings": findings,
        }

        # Generate HTML (pass fw_info for theming)
        html = generate_html(dashboard_data, fw)

        output_path = output_dir / f"{fw}_dashboard.html"
        output_path.write_text(html, encoding="utf-8")

        sev_info = f"[{stats['critical']}C/{stats['high']}H/{stats['medium']}M/{stats['low']}L]"
        print(f"  Stats: {stats['fail']} FAIL {sev_info}, {stats['pass']} PASS, {stats['fixed']} fixed")
        print(f"  Output: {output_path}")

        generated.append((fw, output_path, fw_info))  # Include fw_info
        stats_by_fw[fw] = stats
        scan_info_combined = scan_info  # Use the last scan_info

    # Generate landing page if we have dashboards
    if generated:
        landing_html = generate_landing_page(generated, scan_info_combined, stats_by_fw)
        landing_path = output_dir / "index.html"
        landing_path.write_text(landing_html, encoding="utf-8")
        print(f"\nLanding page: {landing_path}")

    print("\n" + "=" * 50)
    print("Done! Generated files:")
    for fw, p, fw_info in generated:
        print(f"  {p}")
    if generated:
        print(f"  {output_dir / 'index.html'}")
    print(f"\nOpen {output_dir / 'index.html'} in any browser.")


if __name__ == "__main__":
    main()
