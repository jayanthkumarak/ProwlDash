#!/bin/bash
# Check if a virtual environment is already active
if [[ -z "$VIRTUAL_ENV" ]]; then
    source "/Users/jayanthkumar/Documents/Indupro AWS Audit/induproenv/bin/activate"
else
    echo "Virtual environment already active: $VIRTUAL_ENV"
fi

# --- CONFIGURATION ---
# Define your accounts and the target path variables here
ACCOUNTS=("indupro-acct1" "indupro-acct2")
BASE_DIR="/Users/jayanthkumar/Documents/Indupro AWS Audit/Structured Scanning"

# NEW: Use nested structure YYYY-MM-DD/HH-MM-SS to correspond with ProwlDash
DATE_TAG=$(date +"%Y-%m-%d")
TIME_TAG=$(date +"%H-%M-%S")
OUTPUT_DIR="$BASE_DIR/$DATE_TAG/$TIME_TAG"

# Create the directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

echo "Starting Prowler Scans with FSBP, CIS and AWS Well architected Security scans for date: $DATE_TAG time: $TIME_TAG"
echo "Output Directory: $OUTPUT_DIR"

# --- MAIN LOOP ---
for ACCOUNT in "${ACCOUNTS[@]}"; do
    
    # --- 1. Run FSBP Scan ---
    echo "Running FSBP for $ACCOUNT..."
    prowler aws \
        --profile "$ACCOUNT" \
        --compliance aws_foundational_security_best_practices_aws \
        --output-filename "fsbp_report_${ACCOUNT}_${DATE_TAG}_${TIME_TAG}" \
        --output-directory "$OUTPUT_DIR"

    # --- 2. Run CIS Scan ---
    # Validate 'cis_5.0_aws' is correct for your version; otherwise change to 'cis_3.0_aws'
    echo "Running CIS 5.0 for $ACCOUNT..."
    prowler aws \
        --profile "$ACCOUNT" \
        --compliance cis_5.0_aws \
        --output-filename "cis_report_${ACCOUNT}_${DATE_TAG}_${TIME_TAG}" \
        --output-directory "$OUTPUT_DIR"

     # --- 3. Run AWS Well Architected - Security Scan ---
    # 
    echo "Running AWS Well Architected Framework - Security Scan for $ACCOUNT..."
    prowler aws \
        --profile "$ACCOUNT" \
        --compliance aws_well_architected_framework_security_pillar_aws \
        --output-filename "aws_well_arch_report_${ACCOUNT}_${DATE_TAG}_${TIME_TAG}" \
        --output-directory "$OUTPUT_DIR"

    # --- 4. Run Prowler ThreatScore Scan ---
    echo "Running Prowler ThreatScore for $ACCOUNT..."
    prowler aws \
        --profile "$ACCOUNT" \
        --compliance prowler_threatscore_aws \
        --output-filename "threatscore_report_${ACCOUNT}_${DATE_TAG}_${TIME_TAG}" \
        --output-directory "$OUTPUT_DIR"

done

echo "All scans completed. Files are ready for ProwlDash ingestion."
