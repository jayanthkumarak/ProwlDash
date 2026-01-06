# Contributing to ProwlDash

Thank you for your interest in contributing to ProwlDash! We welcome contributions from the community to help make this tool better for everyone.

## Getting Started

1.  **Fork the repository** on GitHub.
2.  **Clone your fork** locally:
    ```bash
    git clone https://github.com/your-username/ProwlDash.git
    cd ProwlDash
    ```
3.  **Install dependencies** (optional, for development):
    ```bash
    pip install pandas ruff pytest
    ```

## Development Workflow

### Code Style
We use `ruff` for linting and formatting. Please run the following before submitting a PR:

```bash
ruff check prowldash.py
```

### Running Tests
ProwlDash has a test suite to ensure stability. Run tests using:

```bash
# Run unit tests
python3 tests/test_core.py

# Run integration tests
python3 tests/test_integration.py
```

### Benchmarking
If you are making performance-critical changes, please run the benchmark script to ensure no regressions:

```bash
python3 tools/benchmark.py
```

## Pull Request Process

1.  Create a new branch for your feature or fix:
    ```bash
    git checkout -b feature/amazing-feature
    ```
2.  Commit your changes with clear, descriptive messages.
3.  Push your branch to GitHub.
4.  Open a Pull Request against the `main` branch.
5.  Ensure all CI checks pass.

## Adding New Frameworks

To add support for a new compliance framework:
1.  Open `prowldash.py`.
2.  Add the framework definition to `FRAMEWORK_REGISTRY` dict.
    - Include `id`, `name`, `icon`, `color`, and detection `patterns`.
3.  Test detection with a sample CSV if possible.

## Key Principles
- **Single File:** We aim to keep the core logic/distribution simple.
- **Offline First:** Generated HTML must be self-contained (no external CDN links).
- **Performance:** Handle large CSVs efficiently.

Thank you for your help!
