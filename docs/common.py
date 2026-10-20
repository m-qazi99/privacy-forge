"""Small CSV primitives shared by a project's Python engine."""
import csv, io, math
from decimal import Decimal, InvalidOperation
MAX_CHARS=2_000_000
MAX_ROWS=10_000

def read_csv(text):
    if not isinstance(text,str) or not text.strip(): raise ValueError('Paste CSV data or load a sample first.')
    if len(text)>MAX_CHARS: raise ValueError('CSV exceeds the 2 MB text limit.')
    stream=io.StringIO(text.lstrip('\ufeff'));reader=csv.reader(stream,strict=True)
    try:
        headers=next(reader)
        if not headers or any(not x.strip() for x in headers): raise ValueError('Every column needs a non-empty header.')
        headers=[x.strip() for x in headers]
        if len(set(headers))!=len(headers): raise ValueError('Column names must be unique.')
        rows=[]
        for line,row in enumerate(reader,2):
            if not row: continue
            if len(row)!=len(headers): raise ValueError(f'CSV record {line} has {len(row)} fields; expected {len(headers)}.')
            if len(rows)>=MAX_ROWS: raise ValueError('Use at most 10,000 data rows per analysis.')
            rows.append(dict(zip(headers,row)))
        if not rows: raise ValueError('The CSV has a header but no data rows.')
        return headers,rows
    except csv.Error as e: raise ValueError('Invalid CSV: '+str(e)) from e
    except StopIteration as e: raise ValueError('The CSV is empty.') from e

def number(value):
    try:
        n=Decimal(str(value).strip())
        return n if n.is_finite() else None
    except (InvalidOperation,ValueError): return None

def columns(value,headers):
    selected=[x.strip() for x in str(value or '').split(',') if x.strip()]
    missing=[x for x in selected if x not in headers]
    if missing: raise ValueError('Unknown columns: '+', '.join(missing))
    return list(dict.fromkeys(selected))

def result(title,metrics,headers,rows,findings,chart=None,artifacts=None):
    return {'title':title,'metrics':metrics,'table':{'columns':headers,'rows':rows},'findings':findings,'chart':chart or [],'artifacts':artifacts or [],'rows_shown':min(len(rows),200),'rows_total':len(rows)}

def metric(label,value,note=''): return {'label':label,'value':value,'note':note}
def finding(severity,title,detail): return {'severity':severity,'title':title,'detail':detail}
