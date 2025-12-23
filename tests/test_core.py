
import unittest
import json
import sys
import os
from pathlib import Path
from unittest.mock import patch, mock_open, MagicMock

# Add project root to path so we can import prowldash
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from prowldash import safe_json_dumps, detect_framework, get_framework_info, parse_csv

class TestCore(unittest.TestCase):
    def test_safe_json_dumps_escapes_xss(self):
        """Test that HTML-sensitive characters are escaped in JSON."""
        data = {
            "key": "<script>alert('xss')</script>",
            "nested": {"val": "foo/"},
            "array": ["<div>"]
        }
        
        json_str = safe_json_dumps(data)
        
        # Verify characters are escaped
        self.assertNotIn("<", json_str)
        self.assertNotIn(">", json_str)
        
        # We explicitly replaced / with \/
        # But json.dumps might not escape it by default, so we look for \/
        self.assertIn("\\/", json_str)
        self.assertIn("\\u003c", json_str)  # <
        self.assertIn("\\u003e", json_str)  # >
        
        # Verify it's still valid JSON when loaded back
        loaded = json.loads(json_str)
        self.assertEqual(loaded["key"], "<script>alert('xss')</script>")
        self.assertEqual(loaded["nested"]["val"], "foo/")
        self.assertEqual(loaded["array"][0], "<div>")

    def test_detect_framework_filename(self):
        """Test framework detection from filenames."""
        cases = [
            ("pci_report.csv", "pci-dss"),
            ("cis_scan.csv", "cis"),
            ("hipaa-results.csv", "hipaa"),
            ("nist-800-53-scan.csv", "nist-800-53"),
            ("random-file.csv", "cis"),  # Default fallback
        ]
        
        for filename, expected in cases:
            with self.subTest(filename=filename):
                # We can pass empty rows because we're testing filename precedence (mostly)
                # But detect_primary_framework checks filename if filepath is provided
                result = detect_framework([], filepath=f"/tmp/{filename}")
                self.assertEqual(result, expected)

    def test_get_framework_info(self):
        """Test registry overrides."""
        # Known framework
        info = get_framework_info("cis")
        self.assertEqual(info["id"], "cis")
        
        # Alias/Pattern match
        info = get_framework_info("CIS")
        self.assertEqual(info["id"], "cis")
        
        # Unknown framework fallback
        info = get_framework_info("unknown-fw")
        self.assertEqual(info["id"], "unknown-fw")
        self.assertEqual(info["name"], "unknown-fw")

class TestCsvParsing(unittest.TestCase):
    @patch("prowldash.os.path.getsize")
    @patch("prowldash.USE_PANDAS", False)
    def test_parse_csv_stdlib_small_file(self, mock_getsize):
        """Test parsing small file uses stdlib csv."""
        mock_getsize.return_value = 1024  # 1KB
        
        csv_content = "ACCOUNT_UID;CHECK_ID\n123;check-1"
        with patch("builtins.open", mock_open(read_data=csv_content)):
            rows = parse_csv("dummy.csv")
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["ACCOUNT_UID"], "123")
            
    @patch("prowldash.os.path.getsize")
    @patch("prowldash.USE_PANDAS", True)
    @patch("prowldash.pd")
    def test_parse_csv_pandas_large_file(self, mock_pd, mock_getsize):
        """Test parsing large file >10MB uses Pandas if available."""
        mock_getsize.return_value = 15 * 1024 * 1024  # 15MB
        
        # Mock dataframe representing a chunk
        mock_df = MagicMock()
        mock_df.to_dict.return_value = [{"ACCOUNT_UID": "123"}]
        
        # Mock the reader object returned by read_csv
        # It needs to be a context manager AND iterable
        mock_reader = MagicMock()
        mock_reader.__enter__.return_value = mock_reader
        mock_reader.__iter__.return_value = iter([mock_df])
        
        mock_pd.read_csv.return_value = mock_reader
        
        rows = parse_csv("huge.csv")
        
        mock_pd.read_csv.assert_called_once()
        self.assertEqual(len(rows), 1)

if __name__ == "__main__":
    unittest.main()
