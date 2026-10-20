"""Local-only Python API plus static UI. Run: python server.py"""
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'src'))
from engine import run
class Handler(SimpleHTTPRequestHandler):
 def __init__(self,*a,**k):super().__init__(*a,directory=str(ROOT/'docs'),**k)
 def do_POST(self):
  if self.path!='/api/analyze':self.send_error(404);return
  try:
   length=int(self.headers.get('Content-Length','0'))
   if length<1 or length>4000000:raise ValueError('Request body must be 1 byte to 4 MB.')
   payload=json.loads(self.rfile.read(length))
   if not isinstance(payload,dict):raise ValueError('Send a JSON object.')
   body=json.dumps(run(payload),ensure_ascii=False,allow_nan=False).encode();code=200
  except (ValueError,TypeError,KeyError)as e:body=json.dumps({'error':str(e)}).encode();code=400
  self.send_response(code);self.send_header('Content-Type','application/json');self.send_header('X-Content-Type-Options','nosniff');self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)
if __name__=='__main__':
 print('Open http://127.0.0.1:8000 · POST /api/analyze for the native Python API')
 ThreadingHTTPServer(('127.0.0.1',8000),Handler).serve_forever()
