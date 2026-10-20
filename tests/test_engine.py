import unittest,sys,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/'src'))
from engine import run
from common import read_csv
class EngineTests(unittest.TestCase):
 def sample(self):return json.loads((R/'examples/sample.json').read_text())
 def test_empty_csv_rejected(self):
  with self.assertRaises(ValueError):read_csv('')
 def test_duplicate_headers_rejected(self):
  with self.assertRaises(ValueError):read_csv('a,a\n1,2')
 def test_ragged_csv_rejected(self):
  with self.assertRaises(ValueError):read_csv('a,b\n1')
 def test_quoted_csv_and_bom(self):
  h,r=read_csv('\ufeffid,note\n1,"hello, world"');self.assertEqual(r[0]['note'],'hello, world')
 def test_sample_masks_names_and_contacts(self):
  r=run(self.sample());masked=r['artifacts'][0]['content'];self.assertNotIn('asha@example.com',masked);self.assertNotIn('Asha Rao',masked);self.assertIn('[REDACTED]',masked)
 def test_no_original_values_in_findings(self):
  r=run(self.sample());s=json.dumps(r['table']);self.assertNotIn('asha@example.com',s)
 def test_selected_column_masked(self):
  r=run({'csv':'id,secret\n1,hidden','columns':'secret'});self.assertNotIn('hidden',r['artifacts'][0]['content'])
 def test_token_stable_within_run_and_changes_between_runs(self):
  p={'csv':'email\na@example.com\na@example.com','mode':'tokenize'};a=run(p);b=run(p);self.assertEqual(a['table']['rows'][0][3],a['table']['rows'][1][3]);self.assertNotEqual(a['table']['rows'][0][3],b['table']['rows'][0][3])
 def test_invalid_ipv4_not_flagged(self):
  r=run({'csv':'note\n999.999.999.999'});self.assertEqual(r['metrics'][1]['value'],0)
 def test_invalid_mode(self):
  with self.assertRaises(ValueError):run({'csv':'id\n1','mode':'bad'})

if __name__=='__main__':unittest.main()
