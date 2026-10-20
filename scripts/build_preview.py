"""Generate the explicitly labeled synthetic first-visit preview from real Python."""
import json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/'src'))
from engine import run
p=json.loads((R/'examples/studio.json').read_text())
(R/'docs/sample-result.js').write_text('window.SAMPLE_RESULT='+json.dumps(run(p),ensure_ascii=False)+';')
print('Synthetic preview regenerated with native Python.')
