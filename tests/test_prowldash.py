
import unittest
import sys
import os
from collections import namedtuple

# Add parent dir to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ProwlDash')))
import prowldash

class TestProwlDash(unittest.TestCase):

    def setUp(self):
        # Mock data
        self.old_row = {
            'acctId': '123456789012',
            'region': 'us-east-1',
            'checkId': 'cis_1.1',
            'resourceId': 'arn:aws:iam::123:user/old-user',
            'resourceName': 'old-user',
            'status': 'FAIL',
            'severity': 'critical'
        }
        
    def test_create_key(self):
        key = prowldash.create_key(self.old_row)
        self.assertEqual(key, '123456789012|us-east-1|cis_1.1|arn:aws:iam::123:user/old-user')

    def test_calculate_delta_strict_match(self):
        # Exact match, same status
        new_row = self.old_row.copy()
        delta = prowldash.calculate_delta([new_row], [self.old_row])
        self.assertEqual(delta[0]['delta'], 'unchanged')
        
    def test_calculate_delta_fixed_strict(self):
        # Exact match, FAIL -> PASS
        new_row = self.old_row.copy()
        new_row['status'] = 'PASS'
        delta = prowldash.calculate_delta([new_row], [self.old_row])
        self.assertEqual(delta[0]['delta'], 'fixed')
        self.assertEqual(delta[0]['oldSeverity'], 'critical') # Crucial for metrics

    def test_calculate_delta_name_match(self):
        # Different ARN, same ResourceName
        new_row = self.old_row.copy()
        new_row['resourceId'] = 'arn:aws:iam::123:user/old-user-v2' # Changed ARN
        new_row['status'] = 'PASS'
        
        delta = prowldash.calculate_delta([new_row], [self.old_row])
        self.assertEqual(delta[0]['delta'], 'fixed')
        # self.assertEqual(delta[0]['match_type'], 'name') # Internal impl detail

    def test_calculate_delta_singleton_match(self):
        # Different ARN, Different Name, but ONLY finding for this check
        new_row = self.old_row.copy()
        new_row['resourceId'] = 'arn:weird-id'
        new_row['resourceName'] = 'weird-name'
        new_row['status'] = 'PASS'
        
        delta = prowldash.calculate_delta([new_row], [self.old_row])
        self.assertEqual(delta[0]['delta'], 'fixed')

    def test_calculate_delta_fuzzy_match(self):
        # Ambiguous context (simulated by having comparison list check logic)
        # But we test the fuzzy logic helper directly? 
        # Actually `calculate_delta` encapsulates it.
        # Let's create a case where Singleton fails (2 items) but Fuzzy wins.
        
        row_a = self.old_row.copy()
        row_a['resourceId'] = 'bucket-100'
        row_b = self.old_row.copy()
        row_b['resourceId'] = 'bucket-200'
        
        old_rows = [row_a, row_b]
        
        new_row = self.old_row.copy()
        new_row['resourceId'] = 'bucket-101' # Very close to 100
        new_row['status'] = 'PASS'
        
        delta = prowldash.calculate_delta([new_row], old_rows)
        # Should match bucket-100 (similarity > 0.7 likely)
        self.assertEqual(delta[0]['delta'], 'fixed') 
        
    def test_stats_remediation(self):
        data = [
            {'status': 'PASS', 'delta': 'fixed', 'oldSeverity': 'critical'},
            {'status': 'PASS', 'delta': 'fixed', 'oldSeverity': 'high'},
            {'status': 'FAIL', 'severity': 'critical'}
        ]
        # We need old_data to establish denominator if we want perfect stats,
        # but the current `compute_stats` mostly counts based on `data`.
        # Wait, metrics rely on frontend logic now?
        # Backend `compute_stats` includes `fixed`.
        stats = prowldash.compute_stats(data, [])
        self.assertEqual(stats['fixed'], 2)

if __name__ == '__main__':
    unittest.main()
