# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
