from pathlib import Path
import ast,json
r=Path(__file__).resolve().parents[1]
for name in ['engine.py','common.py','lab.py']:
 assert (r/'src'/name).read_bytes()==(r/'docs'/name).read_bytes(), 'Browser/native engines diverged'
 ast.parse((r/'src'/name).read_text())
for name in ['index.html','studio.js','worker.js','studio-config.js','sample-result.js','studio.css','favicon.svg']:
 assert (r/'docs'/name).is_file(),name
json.loads((r/'examples/sample.json').read_text())
print('PASS: native/browser engines match and deployable assets exist')
