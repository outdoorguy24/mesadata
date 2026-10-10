import csv,sys,json
# usage: python3 upd.py  (reads updates.json: list of dicts with name, email, grade, evidence, source)
rows=list(csv.DictReader(open('partners_verified.csv')))
fn=list(rows[0].keys())
U=json.load(open('updates.json'))
byname={r['name']:r for r in rows}
for u in U:
    if u['name'] in byname and not u.get('new'):
        r=byname[u['name']]
    else:
        r={k:'' for k in fn}; rows.append(r); r.update({k:v for k,v in u.get('row',{}).items()}); r['name']=u['name']
    r['email']=u['email']; r['email_source']=u['source']; r['email_grade']=u['grade']; r['grade_evidence']=u['evidence']
    r['email_status']='published' if u['grade']=='verified' and 'ublished' in u['evidence'] else ('smtp-confirmed' if u['grade']=='verified' else u['grade'])
with open('partners_verified.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fn); w.writeheader(); w.writerows(rows)
from collections import Counter; print(Counter(r['email_grade'] for r in rows), len(rows))
