# Changelog

All notable changes to this project will be documented in this file.

## [4.6.1] - 2025-12-23

### Added
- **New Terminal UI**: Added a "Modern Slant" ASCII art banner and colorized output for a professional look.
- **Improved UX**: Clearer descriptive text relative to the tool's purpose and version.

## [4.6.0] - 2025-12-23

### Added
- **XSS Prevention**: Implemented `safe_json_dumps` to escape HTML characters in embedded JSON data.
- **Adaptive Parallelism**: Worker count now defaults to `min(cpu_count, file_count)` to reduce overhead.
- **Chunked Reading**: Large files (>10MB) are now read in chunks using Pandas to reduce memory footprint.
- **Accessibility**: Added ARIA roles, labels, and keyboard navigation support to the dashboard.
- **Benchmarking**: Added `tools/benchmark.py` and CI benchmarking job.
- **CLI**: Added `--max-workers` flag for manual control over parallelism.

### Changed
- Improved CSV parser selection logic.
- Updated documentation with performance journey and accessibility details.
- Fixed CI failure on environments without Pandas installed.

## [4.5.0] - 2025-12-22
- Multi-process parallel execution for bulk CSV processing.
- Smart CSV parsing (hybrid stdlib/Pandas approach).
