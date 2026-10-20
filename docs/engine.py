"""Heuristic sensitive-data discovery. Does not certify anonymization."""
import csv,io,re,hashlib,secrets
from collections import Counter
from common import *
PATTERNS=[('Email',re.compile(r'\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b',re.I)),('IPv4',re.compile(r'(?<!\d)(?:\d{1,3}\.){3}\d{1,3}(?!\d)')),('Phone-like',re.compile(r'(?<!\w)(?:\+\d{1,3}[ -]?)?\(?\d{3}\)?[ -]?\d{3}[ -]?\d{4}(?!\w)'))]
SENSITIVE={'name','full_name','first_name','last_name','address','email','phone','mobile','ssn','aadhaar','pan','dob','date_of_birth','customer_name'}

def legacy_run(p):
    h,rows=read_csv(p.get('csv',''));manual=columns(p.get('columns'),h);mode=p.get('mode','redact')
    if mode not in {'redact','tokenize'}:raise ValueError('Choose redact or tokenize.')
    salt=secrets.token_bytes(16);counts=Counter();output=[];masked=[]
    for i,row in enumerate(rows,2):
        new=dict(row)
        for c in h:
            value=row[c];types=[]
            if value.strip() and (c.lower().replace(' ','_')in SENSITIVE or c in manual):types.append('Selected / sensitive header')
            for kind,pattern in PATTERNS:
                matches=pattern.findall(value)
                if kind=='IPv4':matches=[s for s in matches if all(int(n)<=255 for n in s.split('.'))]
                if matches:types.append(kind)
            if types:
                counts[c]+=1;new[c]='[REDACTED]'if mode=='redact'else 'tok_'+hashlib.sha256(salt+value.encode()).hexdigest()[:16]
                output.append([str(i),c,', '.join(types),new[c]])
        masked.append(new)
    buf=io.StringIO();writer=csv.DictWriter(buf,fieldnames=h);writer.writeheader();writer.writerows(masked)
    findings=[finding('warning','Heuristic scan, not an anonymization guarantee','Rules can miss identifiers and produce false positives. Human review is required before sharing any dataset.')]
    findings.append(finding('info','Whole-cell masking','If any rule matches a cell, the entire cell is replaced; original values are omitted from the findings.'))
    if mode=='tokenize':findings.append(finding('info','Run-scoped tokens','Repeated values within this run receive the same token. A random per-run salt changes tokens on the next run and is not exported.'))
    if not output:findings.append(finding('info','No rules matched','This does not establish that the data is free of sensitive information.'))
    return result('Privacy review complete',[metric('Rows scanned',len(rows)),metric('Flagged cells',len(output)),metric('Flagged columns',len(counts)),metric('Masking mode',mode)],['CSV record','Column','Detection rule','Replacement'],output,findings,[{'label':c,'value':n}for c,n in counts.items()],[{'name':'masked-data.csv','content':buf.getvalue()}])


def run(p):
    if not isinstance(p,dict):raise ValueError("Send a JSON object.")
    if p.get("workspace")=="studio":
        from lab import run as studio_run
        return studio_run(p)
    return legacy_run(p)
