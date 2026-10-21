"""Review boundaries and reproducibility for the public handoff workflow."""
import copy,json,sys,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/'src'))
from engine import run
from review import PROJECT

class ReviewTests(unittest.TestCase):
 def sample(self):return json.loads((R/'examples/studio.json').read_text())
 def test_serializable_priorities_and_exports(self):
  out=run(self.sample());json.dumps(out,allow_nan=False)
  self.assertEqual(out['review']['project'],PROJECT)
  self.assertEqual(sum(out['review']['summary'].values()),len(out['review']['items']))
  self.assertEqual(len({x['id'] for x in out['review']['items']}),len(out['review']['items']))
  self.assertIn('review-handoff.md',[x['name'] for x in out['artifacts']])
 def test_input_is_not_changed(self):
  p=self.sample();before=copy.deepcopy(p);run(p);self.assertEqual(p,before)
 def test_project_specific_policy_boundary(self):
  p=self.sample()
  if PROJECT=='datalens':
   p['rules']='[]';o=run(p);self.assertIn('coverage',[x['id'] for x in o['review']['items']])
  elif PROJECT=='recon-lab':
   p.update(source='id,amount\n1,10\n2,20',target='id,amount\n1,10',keys='id',compare='amount',tolerance='10000',relative='0')
   self.assertIn('missing',[x['id'] for x in run(p)['review']['items']])
  elif PROJECT=='runbook-radar':
   p.update(query='xylophone quantum zephyr',evaluation='[]');items=run(p)['review']['items']
   self.assertIn('no-match',[x['id'] for x in items]);self.assertIn('label-coverage',[x['id'] for x in items])
  elif PROJECT=='privacy-forge':
   p.update(csv='email,city\nsecret@example.com,Pune',policy='{"email":"keep"}',quasi='')
   o=run(p);self.assertIn('exposure-email',[x['id'] for x in o['review']['items']])
   self.assertNotIn('secret@example.com',json.dumps(o['review']))
  elif PROJECT=='pipeline-pulse':
   o=run(p);self.assertIn('blocked',[x['id'] for x in o['review']['items']])
   self.assertTrue(any(x['id'].startswith('failure-') for x in o['review']['items']))
 def test_legacy_contract_still_available(self):
  p=json.loads((R/'examples/sample.json').read_text());o=run(p)
  self.assertNotIn('review',o);self.assertIn('metrics',o)

if __name__=='__main__':unittest.main()
