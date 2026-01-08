# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [4.8.0] - 2026-01-07

### Security
- **CRITICAL**: Complete security hardening of generated HTML reports
  - Fixed 23 security vulnerabilities (14 HIGH, 8 MEDIUM, 1 LOW) - now 0 vulnerabilities
  - Added Content Security Policy (CSP) to prevent XSS attacks
  - Added X-Frame-Options header to prevent clickjacking
  - Added X-Content-Type-Options header to prevent MIME type sniffing
  - Implemented comprehensive XSS protection with proper data escaping
  - Added Subresource Integrity (SRI) to CDN script resources
  - Fixed insecure HTTP resources (migrated to HTTPS)
  - Secured URL construction with encodeURIComponent for external links
- **Security Testing**: Enhanced penetration testing tool with improved false positive detection

### Changed
- **Version**: Updated to semantic versioning (4.8.0) for security-focused release

## [5.1.2] - 2025-12-23
### Added
- **Testing**: Added new integration test suite `tests/test_generation.py` to verify HTML/JS integrity and prevent regression.
### Fixed
- **UI**: Fixed sticky header to properly stack "Security Controls" and column headers for a "freeze pane" effect.
- **UI**: Removed truncation from "Title" column to display full check descriptions naturally.

## [5.1.1] - 2025-12-23
### Fixed
- **Critical**: Fixed Dashboard rendering crash caused by regression in V5.1.0 where removed HTML elements (`filterDelta`) were still referenced in JavaScript.
- **UI**: Fixed broken header layout showing visible "Light" theme text.

## [5.1.0] - 2025-12-23
### Removed
- **Export Functionality**: Removed Client-side PDF and CSV export buttons and dependencies (`html2canvas`, `jsPDF`) to simplify logic and reduce external requests.
- **CIS Level Filters**: Removed "Level 1" and "Level 2" filtering and badging due to inconsistent profile matching in Prowler data.

## [5.0.3] - 2025-12-23
### Changed
- **UX**: Added tooltips to L1/L2 compliance badges to verify "CIS Profile Maturity" context.
### Fixed
- **Filtering**: Made CIS Level filtering case-insensitive to ensure reliable results (`Level 1` vs `level 1`).

## [5.0.2] - 2025-12-23
### Fixed
- **Critical**: Corrected the template injection marker to `/*__DATA__*/`. The V5.0.1 patch used an incorrect placeholder `{{ DATA }}`, which failed to render.
- **Verification**: Added automated grep test to CI to prevent regression.

## [5.0.1] - 2025-12-23
### Fixed
- **Critical**: Restored missing `DATA` variable in dashboard template that caused empty reports in V5.0.0.
- **Documentation**: Reverted README to professional tone.

## [5.0.0] - 2025-12-23

### Added
- **Compliance Intelligence**:
    - Automatic detection of CIS Levels (L1/L2) with visual badges.
    - Interactive MITRE ATT&CK integration: click technique IDs to view official documentation.
    - Deep linking to V5.0 compliance frameworks.
- **Reporting Engine**:
    - **PDF Export**: Generate executive summary reports directly from the browser (no backend required).
    - **CSV Export**: Download filtered datasets for offline analysis.
    - **Interactive Filtering**: Real-time client-side filtering by Status, Severity, Service, Region, and CIS Level.
- **Enterprise Features**:
    - **Theming**: Persistent Dark/Light mode toggle and CSS variables for corporate branding.
    - **Search**: Advanced multi-keyword search with real-time highlighting.
- **Optimization**:
    - Lazy-loaded visualization libraries for faster initial render.
    - Minified embedded JavaScript for reduced file size.

### Changed
- **Core Parsing**:
    - Hybrid parsing engine now switches between `csv` (stdlib) and `pandas` based on file size for optimal performance.
    - Enhanced robustness for malformed CSVs (unclosed quotes, mixed encoding).
- **UI/UX**:
    - Completely redesigned dashboard layout with sticky headers and scrollable tables.
    - Refined color palette for better accessibility (Okabe-Ito friendly).

### Fixed
- Corrected MITRE URL generation (handling `.` vs `/` in technique IDs).
- Fixed issue with parsing multi-line cells in Prowler V3/V4 outputs.

## [4.0.0] - 2024-12-22
- Initial major release supporting Prowler V4 output format.
