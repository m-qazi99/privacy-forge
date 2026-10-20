import unittest, sys, json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/'src'))
from engine import run

class StudioTests(unittest.TestCase):
 def sample(self):return json.loads((R/'examples/studio.json').read_text())
 def execute(self,**changes):
  p=self.sample();p.update(changes);return run(p)['lab']
 def test_json_serializable(self):json.dumps(run(self.sample()),allow_nan=False)
 def test_dropped_column_absent(self):
  l=self.execute();self.assertNotIn('name',l['output_headers']);self.assertTrue(all('name' not in r for r in l['preview']))
 def test_audit_excludes_original_values(self):
  l=self.execute();text=json.dumps(l['audit'])+json.dumps(l['receipt']);self.assertNotIn('example.test',text);self.assertNotIn('Asha',text)
 def test_token_consistency_in_run(self):
  l=self.execute(csv='id,email\n1,a@example.test\n2,a@example.test',policy='{"email":"tokenize"}',quasi='');self.assertEqual(l['preview'][0]['email'],l['preview'][1]['email'])
 def test_token_salt_changes_each_run(self):
  a=self.execute();b=self.execute();self.assertNotEqual(a['preview'][0]['customer_id'],b['preview'][0]['customer_id'])
 def test_keep_signals_count_as_residual(self):
  l=self.execute(csv='id,email\n1,a@example.test',policy='{"email":"keep"}',quasi='');self.assertEqual(l['receipt']['residual_signal_cells'],1)
 def test_auto_redacts_whole_cell(self):
  l=self.execute(csv='id,note\n1,Contact a@example.test now',policy='{}',quasi='');self.assertEqual(l['preview'][0]['note'],'[REDACTED]')
 def test_group_size_exact(self):
  l=self.execute(csv='id,age\n1,21\n2,25\n3,31',policy='{"age":"generalize"}',quasi='age');self.assertEqual(l['receipt']['minimum_group_size'],1);self.assertEqual(l['groups'],[{'size':1,'groups':1},{'size':2,'groups':1}])
 def test_drop_every_column_rejected(self):
  with self.assertRaises(ValueError):self.execute(csv='id\n1',policy='{"id":"drop"}',quasi='')
 def test_unknown_action_rejected(self):
  with self.assertRaises(ValueError):self.execute(policy='{"email":"encrypt"}')
 def test_negative_generalization_bucket(self):
  l=self.execute(csv='n\n-1',policy='{"n":"generalize"}',quasi='');self.assertEqual(l['preview'][0]['n'],'-10–-1')
 def test_receipt_has_hashes_not_salt(self):
  r=self.execute()['receipt'];self.assertEqual(len(r['input_sha256']),64);self.assertNotIn('salt',r)
