# Engineering Memo: V4.5 Performance Architecture

**Date:** December 23, 2025
**Subject:** Optimization strategy for bulk CSV processing in ProwlDash V4.5

## Executive Summary

V4.5 changes the processing model from sequential single-threaded execution to multi-process parallel execution. This resulted in an approximately 8x throughput increase on 14-core Apple Silicon hardware for batched workloads.

We also evaluated replacing the standard library `csv` module with `pandas`. Benchmarking revealed `pandas` introduces significant overhead for files under 10MB. Consequently, V4.5 implements a hybrid parser that conditionally loads `pandas` only for large files.

## 1. Parallel Execution Model

### Problem
ProwlDash V4.3 processed files sequentially. On modern multi-core systems, this left CPU utilization low (<15%) while users waited for IO and parse operations to complete one-by-one.

### Implementation
We implemented the `concurrent.futures.ProcessPoolExecutor` to distribute file processing across independent processes.

*   **Worker Count**: Defaults to `os.cpu_count()` (e.g., 14 workers on M3 Max).
*   **Isolation**: Each process handles a full file lifecycle (Parse → Normalize → Analyze), eliminating shared state complexity.
*   **Scaling**: Throughput scales linearly with core count until disk IO becomes the bottleneck.

## 2. CSV Parser Benchmarking

We tested two parsing approaches against typical Prowler outputs (semicolon-delimited CSVs).

**Test Environment:**
*   Files: Prowler V3/V4 outputs (various sizes)
*   Hardware: Apple M3 Max

**Results:**

| Dataset Size | Stdlib `csv` (ms) | Pandas (ms) | Delta |
|:---|---:|---:|:---|
| **Small (<500KB)** | 15ms | 45ms | **Stdlib +30ms** |
| **Medium (2-5MB)** | 52ms | 104ms | **Stdlib +52ms** |
| **Large (>10MB)** | 450ms | 120ms | **Pandas -330ms** |

**Findings:**
`pandas` incurs initialization overhead (~30-50ms) that outweighs its parsing speed advantages for typical Prowler scan files (which are usually <5MB). 

### Decision
V4.5 uses a conditional logic:
1.  Check `os.path.getsize(filepath)`.
2.  If >10MB, invoke `pandas.read_csv` (requires `pip install pandas`).
3.  Otherwise, use standard `csv.DictReader`.

This hybrid approach optimizes for the 90th percentile case (small/medium files) while providing a fallback for enterprise-scale dumps.

## 3. Hardware Considerations

*   **Apple Silicon (ARM64)**: Shows efficient process forking and low overhead. Speedup is near-instant for batch sizes < Core Count.
*   **PyPy**: The codebase remains pure Python. Running with PyPy JIT yields an additional ~2x speedup on top of the architectural changes for the `stdlib` parsing path.
