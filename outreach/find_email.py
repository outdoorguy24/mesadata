import sys,re,json,urllib.request,urllib.parse,ssl,csv
from concurrent.futures import ThreadPoolExecutor
ctx=ssl.create_default_context()
UA={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36'}
SKIP=('linkedin','facebook','twitter','bizbuysell','bizquest','ibba.org','masource','businessbrokerregistry','zoominfo','rocketreach','crunchbase','yelp','mergr','prospeo','signalhire','contactout','apollo','wikipedia','instagram','youtube','pitchbook','dnb.com','cbinsights','lawyers.com','avvo','martindale','justia','bbb.org','mapquest','yellowpages','clutch','buzzfile','manta','allbiz','chamberofcommerce','zippia','leadiq','lusha','adapt.io','datanyze','owler','sec.gov','indeed','glassdoor','wix.com')
def get(u,t=12):
    try:
        return urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=t,context=ctx).read().decode('utf8','ignore')
    except Exception: return ''
def search(q):
    import base64,html
    h=get('https://www.bing.com/search?q='+urllib.parse.quote(q))
    out=[]
    for blk in h.split('class="b_algo"')[1:]:
        m=re.search(r'<a[^>]*href="([^"]+)"',blk)
        if not m: continue
        m=html.unescape(m.group(1))
        mm=re.search(r'[&?]u=a1([A-Za-z0-9_-]+)',m)
        if mm:
            b=mm.group(1); b+='='*(-len(b)%4)
            try: u=base64.urlsafe_b64decode(b).decode()
            except Exception: continue
        else: u=m
        if u not in out: out.append(u)
    return out
EM=re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[a-z]{2,}')
def emails(h):
    s=set()
    for m in EM.findall(h):
        m=m.lower()
        if m.endswith(('.png','.jpg','.svg','.webp','.gif','.js','.css')) or 'sentry' in m or 'example' in m or 'domain.com' in m or 'wixpress' in m: continue
        s.add(m)
    return s
def run(row):
    name,firm=row
    q=f'"{firm}" {name.split(",")[0]} email contact'
    toks=[re.sub(r'[^a-z]','',w.lower()) for w in re.split(r'[ /,&()-]+',firm) if len(w)>2 and w.lower() not in ('llc','llp','pllc','the','and','advisors','advisory','group','partners','law','firm','capital','cpa','cpas','inc','plc','consulting')]
    allres=[u for u in search(q) if not any(s in u for s in SKIP)]
    res=[u for u in allres if any(t and t in urllib.parse.urlparse(u).netloc.lower().replace('-','') for t in toks)][:4]
    doms=[]
    for u in res:
        p=urllib.parse.urlparse(u)
        b=f'{p.scheme}://{p.netloc}'
        if b not in doms: doms.append(b)
    found={}
    for b in doms[:2]:
        for path in ['','/contact','/contact-us','/team','/about','/about-us','/our-team','/people','/leadership']:
            h=get(b+path,10)
            for e in emails(h): found.setdefault(e,b+path)
        # also pages returned by search on that site
    for u in res:
        h=get(u,10)
        for e in emails(h): found.setdefault(e,u)
    ln=re.sub(r'[^a-z]','',name.split(',')[0].split()[-1].lower()); fn=name.split()[0].lower()
    hits={e:s for e,s in found.items() if ln in e.split('@')[0] or (fn in e.split('@')[0]) or e.split('@')[0] in (fn[0]+ln,fn+ln[0],fn[0]+'.'+ln)}
    return {'name':name,'firm':firm,'sites':doms[:3],'person_emails':hits,'other_emails':{e:s for e,s in found.items() if e not in hits}}
if __name__=='__main__':
    rows=[(r['name'],r['firm']) for r in csv.DictReader(open('partners_verified.csv')) if not r['email']]
    with ThreadPoolExecutor(8) as ex: out=list(ex.map(run,rows))
    json.dump(out,open('find_existing_noemail.json','w'),indent=1)
    for o in out: print(o['name'],'|',o['firm'],'|',o['sites'][:1],'|',o['person_emails'],'|',list(o['other_emails'])[:3])
