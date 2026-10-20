"""Column-level policy laboratory with risk/utility views and safe audit receipts."""
import json,csv,io,hashlib,secrets,re
from collections import Counter
from common import *

def run(p):
    from engine import PATTERNS,SENSITIVE
    h,rows=read_csv(p.get('csv',''))
    try:policy=json.loads(p.get('policy','{}'))
    except (TypeError,ValueError):raise ValueError('Policy must be a JSON object mapping columns to actions.')
    actions={'auto','keep','redact','tokenize','generalize','drop'}
    if not isinstance(policy,dict) or any(c not in h or a not in actions for c,a in policy.items()):raise ValueError('Policy columns must exist. Actions: auto, keep, redact, tokenize, generalize, drop.')
    salt=secrets.token_bytes(24);signals={};audits=[];output=[];summary=[];details={};counts=Counter()
    def detect(c,value):
        labels=[]
        if value.strip() and c.lower().replace(' ','_') in SENSITIVE:labels.append('sensitive header')
        for label,pattern in PATTERNS:
            matches=pattern.findall(value)
            if label=='IPv4':matches=[v for v in matches if all(int(n)<=255 for n in v.split('.'))]
            if matches:labels.append(label)
        return labels
    for c in h:
        colsignals=[detect(c,r[c]) for r in rows];signals[c]=colsignals;count=sum(bool(x) for x in colsignals);action=policy.get(c,'auto');details[c]={'action':action,'detected':count,'rules':list(dict.fromkeys(s for ss in colsignals for s in ss))}
    kept=[c for c in h if policy.get(c)!='drop']
    if not kept:raise ValueError('Keep at least one output column.')
    changed=0;remaining=0
    for i,row in enumerate(rows):
        new={}
        for c in h:
            v=row[c];sig=signals[c][i];action=policy.get(c,'auto');effective='redact' if action=='auto' and sig else 'keep' if action=='auto' else action
            if effective=='drop':nv=None
            elif effective=='redact':nv='[REDACTED]' if v else ''
            elif effective=='tokenize':nv='tok_'+hashlib.sha256(salt+v.encode()).hexdigest()[:16] if v else ''
            elif effective=='generalize':
                n=number(v)
                if n is not None and abs(n)<10**50:
                    decade=(n//10)*10
                    if n<0 and n%10:decade-=10
                    nv=f'{decade}–{decade+9}'
                elif '@' in v:nv='[USER]@'+v.rsplit('@',1)[1]
                elif re.fullmatch(r'\d{4}-\d{2}-\d{2}',v):nv=v[:4]+'-**-**'
                else:nv=v[:1]+'…' if v else ''
            else:nv=v
            if nv is not None:new[c]=nv
            altered=nv!=v
            if altered:changed+=1;counts[c]+=1
            # This is a signal exposure ledger, not a re-identification risk metric.
            exposed=bool(sig) and effective in {'keep','generalize'}
            remaining+=int(exposed)
            if sig or altered:audits.append({'record':i+2,'column':c,'signals':sig,'action':effective,'changed':altered,'residual_signal':exposed})
        output.append(new)
    quasi=columns(p.get('quasi',''),kept)
    groups=Counter(tuple(r[c] for c in quasi) for r in output) if quasi else Counter()
    sizes=Counter(groups.values());singletons=sum(v for k,v in groups.items() if v==1)
    buf=io.StringIO();w=csv.DictWriter(buf,fieldnames=kept);w.writeheader();w.writerows(output)
    receipt={'version':2,'policy':policy,'rows':len(rows),'changed_cells':changed,'detected_cells':sum(d['detected'] for d in details.values()),'residual_signal_cells':remaining,'quasi_identifiers':quasi,'minimum_group_size':min(groups.values()) if groups else None,'input_sha256':hashlib.sha256(p['csv'].encode()).hexdigest(),'output_sha256':hashlib.sha256(buf.getvalue().encode()).hexdigest(),'limitations':'Heuristic signals only. Generalization and group size do not certify anonymity. No original cell values or token salt are included in this receipt.'}
    out=result('Privacy policy experiment complete',[metric('Detected cells',receipt['detected_cells']),metric('Changed cells',changed),metric('Residual signals',remaining),metric('Minimum group',receipt['minimum_group_size'] if quasi else 'Select QIs')],['Record','Column','Action','Detection'],[[a['record'],a['column'],a['action'],', '.join(a['signals']) or 'policy'] for a in audits],[finding('warning','Generalization can retain sensitive information','Residual signals count detected cells retained or generalized. Group size is evaluated only on selected quasi-identifiers; it is not an anonymization guarantee.')],artifacts=[{'name':'policy-output.csv','content':buf.getvalue()},{'name':'audit-receipt.json','content':json.dumps(receipt,indent=2)},{'name':'privacy-policy.json','content':json.dumps(policy,indent=2)}])
    out['lab']={'columns':[{'column':c,**details[c],'changed':counts[c]} for c in h],'output_headers':kept,'preview':output[:80],'audit':audits[:300],'receipt':receipt,'groups':[{'size':s,'groups':n} for s,n in sorted(sizes.items())],'singleton_groups':singletons,'retained_cell_percent':round(100*(len(rows)*len(h)-changed)/(len(rows)*len(h)),1)};return out
