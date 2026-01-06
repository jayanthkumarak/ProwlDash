
import unittest
import os
import shutil
import tempfile
from prowldash import generate_html, parse_csv

class TestDashboardGeneration(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.fixtures_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")
        self.cis_path = os.path.join(self.fixtures_dir, "cis_2.0_aws_compliance.csv")

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_html_generation_integrity(self):
        """
        Verify that the generated HTML:
        1. Contains injected JSON data (not placeholders).
        2. Does NOT contain regression artifacts (e.g. filterDelta).
        3. Contains critical JS initialization logic.
        """
        # Parse real data
        if not os.path.exists(self.cis_path):
            self.skipTest("CIS fixture not found")
            
        data = parse_csv(self.cis_path)
        
        # Generate HTML content (in memory)
        html_output = generate_html(data, "cis")
        
        # 1. Critical Data Injection Check
        self.assertIn("const DATA = [", html_output, "JSON Data block missing from output")
        self.assertNotIn("/*__DATA__*/", html_output, "Template placeholder was not replaced")
        
        # 2. Regression Check: V5.1.1 Crash Fix
        # The script crashed because it looked for 'filterDelta' which was removed from HTML.
        # We ensure no code tries to access getElementById('filterDelta')
        self.assertNotIn("document.getElementById('filterDelta')", html_output, 
                        "Regression: JS is trying to access removed element 'filterDelta'")
        
        # 3. Regression Check: HTML Layout
        # Ensure we have exactly ONE theme label (no duplicates from V5.1 regression)
        self.assertIn('<span id="themeLabel">Light</span>', html_output, "Theme label missing (broke functionality)")
        self.assertEqual(html_output.count('<span id="themeLabel">Light</span>'), 1, 
                        "Regression: Duplicate 'Light' theme label found in HTML")

        # 4. Critical Functionality Check
        self.assertIn("function init()", html_output, "init() function missing")
        self.assertIn("renderTable()", html_output, "renderTable call missing")
        
    def test_no_export_buttons(self):
        """Ensure Export buttons are really gone (V5.1 Simplification)."""
        if not os.path.exists(self.cis_path):
            self.skipTest("CIS fixture not found")
            
        data = parse_csv(self.cis_path)
        html_output = generate_html(data, "cis")
        
        self.assertNotIn("exportCSV", html_output, "exportCSV() function still present")
        self.assertNotIn("exportPDF", html_output, "exportPDF() function still present")
        self.assertNotIn("html2canvas", html_output, "html2canvas library still present")

if __name__ == "__main__":
    unittest.main()
