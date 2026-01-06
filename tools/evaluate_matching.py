
import sys
import os
import csv
from collections import defaultdict
import difflib

# Add parent dir to path to import prowldash
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ProwlDash import prowldash

def load_csv(filepath):
    print(f"Loading {filepath}...")
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f, delimiter=';')
        rows = list(reader)
    # Normalize
    format_type = prowldash.detect_format(rows)
    return [prowldash.normalize_row(r, format_type) for r in rows]

def similarity(s1, s2):
    return difflib.SequenceMatcher(None, s1, s2).ratio()

def advanced_match(new_rows, old_rows):
    """
    Experimental comprehensive matching algorithm.
    """
    from ProwlDash.prowldash import create_key
    
    # 1. Strict Map
    old_map_strict = {create_key(r): r for r in old_rows}
    
    # 2. Name Map
    old_map_name = {}
    for r in old_rows:
        if r.get("resourceName"):
            k = f"{r['acctId']}|{r['region']}|{r['checkId']}|{r['resourceName']}"
            old_map_name[k] = r
            
    # 3. Context Map (Buckets for fuzzy matching)
    # Key: "acctId|region|checkId" -> List of rows
    context_map = defaultdict(list)
    for r in old_rows:
        short_key = f"{r['acctId']}|{r['region']}|{r['checkId']}"
        context_map[short_key].append(r)
        
    matched_old_ids = set() # To avoid double matching
    results = []
    
    matches = {
        "strict": 0,
        "name": 0,
        "fuzzy": 0,
        "singleton": 0,
        "new": 0
    }

    for row in new_rows:
        full_key = create_key(row)
        match_type = None
        old = None
        
        # A. Strict
        if full_key in old_map_strict:
            old = old_map_strict[full_key]
            match_type = "strict"
            
        # B. Name
        if not old and row.get("resourceName"):
            name_key = f"{row['acctId']}|{row['region']}|{row['checkId']}|{row['resourceName']}"
            if name_key in old_map_name:
                old = old_map_name[name_key]
                match_type = "name"
                
        # C. Fuzzy / Context
        if not old:
            short_key = f"{row['acctId']}|{row['region']}|{row['checkId']}"
            candidates = context_map.get(short_key, [])
            
            # Filter out already matched? (Maybe too expensive/complex for now, let's just find best match)
            # Actually, greedy matching is okay for this script.
            
            if len(candidates) == 1:
                old = candidates[0]
                match_type = "singleton"
            elif len(candidates) > 1:
                # Fuzzy Match on Resource ID
                # Find candidate with highest similarity
                best_ratio = 0
                best_cand = None
                for cand in candidates:
                    ratio = similarity(row['resourceId'], cand['resourceId'])
                    if ratio > best_ratio:
                        best_ratio = ratio
                        best_cand = cand
                
                # Threshold for fuzzy match
                if best_ratio > 0.7:  # Experimental threshold
                    old = best_cand
                    match_type = f"fuzzy ({best_ratio:.2f})"
        
        if old:
            matches[match_type.split(' ')[0]] += 1
            # Calculate Delta
            old_status = old.get("status")
            if old_status == "FAIL" and row.get("status") == "PASS":
                delta = "fixed"
            elif old_status == "PASS" and row.get("status") == "FAIL":
                delta = "new-fail"
            else:
                delta = "unchanged"
                
            results.append({
                "check": row['checkId'],
                "resource": row['resourceId'],
                "delta": delta,
                "match_type": match_type,
                "old_resource": old['resourceId'] if match_type.startswith('fuzzy') else None
            })
        else:
            matches["new"] += 1
            # "New" item (or failed match)
            results.append({
                "check": row['checkId'],
                "resource": row['resourceId'],
                "delta": "new-file" if row['status'] == 'FAIL' else 'new-pass',
                "match_type": None
            })

    return matches, results

def main():
    old_path = "ProwlDash/tests/data/old_scan.csv"
    new_path = "ProwlDash/tests/data/new_scan.csv"
    
    if not os.path.exists(old_path) or not os.path.exists(new_path):
        print("Error: Test data not found.")
        return

    old_rows = load_csv(old_path)
    new_rows = load_csv(new_path)
    
    print(f"\nOld Rows: {len(old_rows)}")
    print(f"New Rows: {len(new_rows)}")
    
    matches, results = advanced_match(new_rows, old_rows)
    
    print("\n--- Matching Statistics ---")
    for k, v in matches.items():
        print(f"{k.capitalize()}: {v}")
        
    print("\n--- Interesting 'Fixed' Examples (Fuzzy/Name/Singleton) ---")
    fixed = [r for r in results if r['delta'] == 'fixed' and r['match_type'] != 'strict']
    for r in fixed[:10]:
        print(f"[{r['match_type']}] {r['check']} - {r['resource']} (Old: {r['old_resource'] or 'Same'})")

    print("\n--- Unmatched 'New' Failures (Potential False Positives) ---")
    new_fails = [r for r in results if r['delta'] == 'new-file']
    for r in new_fails[:10]:
        print(f"[New] {r['check']} - {r['resource']}")

if __name__ == "__main__":
    main()
