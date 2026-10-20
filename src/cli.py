"""Read a JSON request from stdin and emit a JSON report."""
import json,sys
from engine import run
if __name__=='__main__':
 try: print(json.dumps(run(json.load(sys.stdin)),indent=2,ensure_ascii=False,allow_nan=False))
 except (ValueError,TypeError,KeyError)as e: print(json.dumps({'error':str(e)}),file=sys.stderr);sys.exit(1)
