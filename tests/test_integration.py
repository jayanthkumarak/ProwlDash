
import unittest
import os
import shutil
import tempfile
import sys
from pathlib import Path

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import main function (we'll run it via subprocess or direct call if possible, 
# but direct call mimics usage better if we patch sys.argv)
from prowldash import main

class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.csv_path = os.path.join(self.test_dir, "test_scan.csv")
        
        # Create a dummy CSV
        with open(self.csv_path, "w") as f:
            f.write("ACCOUNT_UID;CHECK_ID;STATUS;SEVERITY;TIMESTAMP;COMPLIANCE\n")
            f.write("123456789012;check-1;FAIL;high;2025-01-01T12:00:00Z;CIS-1.0: 1.1\n")
            f.write("123456789012;check-2;PASS;low;2025-01-01T12:00:00Z;CIS-1.0: 1.2\n")

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_end_to_end_generation(self):
        """Test full dashboard generation from CSV."""
        output_dir = os.path.join(self.test_dir, "output")
        
        # Mock sys.argv
        sys.argv = [
            "prowldash.py", 
            "--output", output_dir, 
            "--no-timestamp", 
            self.csv_path
        ]
        
        try:
            # Run main logic
            main()
        except SystemExit as e:
            self.assertEqual(e.code, 0)
            
        # Verify output files exist
        self.assertTrue(os.path.exists(os.path.join(output_dir, "index.html")))
        # CIS should be detected from "CIS-1.0" in compliance column
        self.assertTrue(os.path.exists(os.path.join(output_dir, "cis_dashboard.html")))

if __name__ == "__main__":
    unittest.main()
