#!/usr/bin/env python3
"""
Benchmark script for ProwlDash.
Generates synthetic CSV data and runs prowldash.py to measure performance.
"""
import os
import sys
import time
import subprocess
import argparse
import random
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.absolute()
PROWLDASH_SCRIPT = PROJECT_ROOT / "prowldash.py"

def generate_dummy_csv(filepath, rows=1000):
    """Generate a valid Prowler CSV with random data."""
    compliance_opts = ["CIS-1.0: 1.1", "HIPAA: 164.308", "PCI-3.2.1: 1.1.1"]
    statuses = ["PASS", "FAIL", "INFO"]
    severities = ["critical", "high", "medium", "low"]
    
    with open(filepath, "w") as f:
        # Header
        f.write("ACCOUNT_UID;ACCOUNT_NAME;REGION;CHECK_ID;CHECK_TITLE;STATUS;STATUS_EXTENDED;SEVERITY;SERVICE_NAME;RESOURCE_UID;RESOURCE_NAME;COMPLIANCE;TIMESTAMP\n")
        
        for i in range(rows):
            acct = f"1234567890{random.randint(0, 9)}"
            check_id = f"check-{random.randint(1, 100)}"
            status = random.choice(statuses)
            severity = random.choice(severities)
            compliance = random.choice(compliance_opts)
            
            line = (
                f"{acct};Account {acct};us-east-1;{check_id};Check Title {check_id};"
                f"{status};Status extended info;{severity};iam;arn:aws:iam::{acct}:user/user-{i};"
                f"user-{i};{compliance};2025-01-01T12:00:00Z"
            )
            f.write(line + "\n")

def run_benchmark(num_files, rows_per_file, max_workers=None):
    """Run benchmark and return stats."""
    temp_dir = PROJECT_ROOT / "bench_temp"
    temp_dir.mkdir(exist_ok=True)
    
    # Clean previous
    for f in temp_dir.glob("*.csv"):
        f.unlink()
        
    print(f"Generating {num_files} files with {rows_per_file} rows each...")
    files = []
    for i in range(num_files):
        p = temp_dir / f"bench_{i}.csv"
        generate_dummy_csv(p, rows_per_file)
        files.append(str(p))
        
    cmd = [sys.executable, str(PROWLDASH_SCRIPT), "--no-timestamp", "--output", str(temp_dir / "output")]
    if max_workers:
        cmd.extend(["--max-workers", str(max_workers)])
    cmd.extend(files)
    
    print(f"Running command: {' '.join(cmd)}")
    
    start_time = time.time()
    
    # Run with /usr/bin/time if available for memory, otherwise just time
    try:
        # Using subprocess to run
        proc = subprocess.run(cmd, capture_output=True, text=True)
        if proc.returncode != 0:
            print("Error running prowldash:")
            print(proc.stderr)
            return None
    except Exception as e:
        print(f"Exception: {e}")
        return None
        
    duration = time.time() - start_time
    
    # Cleanup
    # for f in temp_dir.glob("*.csv"):
    #     f.unlink()
        
    return duration

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--files", type=int, default=4)
    parser.add_argument("--rows", type=int, default=5000)
    parser.add_argument("--workers", type=int, default=None)
    args = parser.parse_args()
    
    print("=" * 40)
    print(f"Benchmark: {args.files} files, {args.rows} rows")
    if args.workers:
        print(f"Max workers: {args.workers}")
    print("=" * 40)
    
    duration = run_benchmark(args.files, args.rows, args.workers)
    
    if duration:
        print(f"\nSuccess! Duration: {duration:.3f}s")
        print(f"Throughput: {(args.files * args.rows) / duration:.0f} rows/sec")
    else:
        print("Benchmark failed.")
