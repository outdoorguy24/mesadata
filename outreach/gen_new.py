import csv,re,json
src=open('build_cold.py').read()
a=src.index("OPT = "); b=src.index("# personalised hooks")
ns={}
exec(src[a:b],ns)
TYPES=ns['TYPES']; wrap=ns['wrap']
print(list(TYPES))
H={
'Mike Moran':("The healthcare practices you take to market hold years of operating records, and patient data would stay out of scope.",'healthcare records','M&A advisor'),
'Nick Fares':("The manufacturing, industrial and distribution owners you sell keep decades of order, quality and supply records.",'manufacturer records','M&A advisor'),
'Tim Mueller':("The IT services and MSP firms you sell carry years of ticket, contract and client history.",'it services records','Business broker'),
'Eric I. Mendelsohn':("The distribution owners you represent hold years of order, shipment and customer history.",'distribution records','Business broker'),
'Robert Stasiak':("The founder-owned manufacturers you work with keep years of production and customer records.",'production records','Business broker'),
'Chris Nelms, CPA':("Your transaction group sees owners at sell-side diligence, when their records are already organized.",'diligence records','CPA / accounting'),
'Michael Polgur, CPA':("Your sell-side process reaches owners just as their records are being organized.",'sell-side prep','CPA / accounting'),
'Jerry Zhou, CPA':("Your diligence work puts you in front of owners right when their financial and operating records are gathered.",'records in diligence','CPA / accounting'),
'Robert J. Gonzales':("Your clients in a wind-down or restructuring have records that are about to be archived or deleted.",'wind-down records','Law firm'),
'Michael Carter':("The founder and family-owned companies you sell have decades of operating history behind them.",'family business records','M&A advisor'),
'Gregory Seigel':("The healthcare practices and facilities you sell keep years of operating records, and patient data would stay out of scope.",'practice records','M&A advisor'),
'Byron Burge':("The physician practices you sell have years of administrative and operating records, and patient data would stay out of scope.",'practice sale records','M&A advisor'),
'Mike DeMaio':("The owners you guide through exit planning keep years of finance and operating records.",'exit planning records','Fractional CFO'),
'Parth Kalaria':("You advise Texas owners on sales, tax and succession, so you often hear about an exit first.",'owner exit records','Law firm'),
'Michael Ifraimov':("The MSP and IT-services founders you sell hold years of ticket, monitoring and client records.",'msp records','M&A advisor'),
'Dan Sokol':("The Chicago B2B owners you advise keep years of customer and operating records.",'b2b owner records','M&A advisor'),
'Andrew Rice':("Your transaction advisory team sees owners at diligence, when records are already organized.",'transaction records','CPA / accounting'),
'Steve C. Swann':("Your transaction advisory work serves sellers of privately held companies, who keep years of operating records.",'seller records','CPA / accounting'),
'Michael B. Overstreet':("You represent family-owned Texas businesses in sales, so you hear about an exit early.",'sale records','Law firm'),
'Jack Simonian':("The engineering and environmental firms you sell hold years of project, survey and client records.",'project records','M&A advisor'),
'Jessica Barclay':("The architecture and engineering firms you advise keep decades of project and drawing records.",'aec records','M&A advisor'),
'Brian Kennedy':("The staffing firms you sell hold years of candidate, placement and client history.",'staffing records','Business broker'),
'Ryan Soer':("The middle-market owners you represent hold years of operating records by the time they reach a sale.",'owner records at sale','M&A advisor'),
'John R. Allen III':("The architecture, engineering and surveying firms you sell keep years of project records.",'project history','M&A advisor'),
'Chuck Fenske':("The engineering, construction and infrastructure firms you advise keep years of project and bid history.",'construction records','M&A advisor'),
'Christopher Jahnle':("The physician groups you take to market hold years of operating records, and patient data would stay out of scope.",'physician group records','M&A advisor'),
'Gary Moon':("The healthtech companies you sell carry years of product, usage and client records, and patient data would stay out of scope.",'healthtech records','M&A advisor'),
}
def first(n): return n.split(',')[0].split()[0]
rows={r['name']:r for r in csv.DictReader(open('partners_verified.csv'))}
order=['Michael Ifraimov','Chuck Fenske','Jack Simonian','Michael Carter','Nick Fares','Mike Moran','Tim Mueller','Eric I. Mendelsohn','Robert Stasiak','Chris Nelms, CPA','Michael Polgur, CPA','Jerry Zhou, CPA','Robert J. Gonzales','Parth Kalaria','Michael B. Overstreet','Gregory Seigel','Jessica Barclay','Andrew Rice','Steve C. Swann','Mike DeMaio','Christopher Jahnle','Gary Moon','Brian Kennedy','Ryan Soer','Byron Burge','Dan Sokol','John R. Allen III']
assert set(order)==set(H) and len(order)==27
quota={'starrwealthgroup.com':5,'claritywithai.co':7,'sageridge.co':6,'alexstarr.com':9}
names=list(quota)
new=[]
for n in order:
    m=max(names,key=lambda k:(quota[k],-names.index(k))); quota[m]-=1
    hook,subj,ptype=H[n]; r=rows[n]
    body=wrap(TYPES[ptype]['base'].format(first=first(n),hook=hook))
    new.append(dict(name=n,firm=r['firm'],email=r['email'],subject=subj,body=body,sending_domain=m,partner_type=ptype,priority=r['priority'],email_status='verified'))
# lint
bad=[]
for d in new:
    core=d['body'].split("\n\nIf this isn't")[0]
    for pat in ['—','–',r'\bAI\b',r'\bnot\b',r'\bno\b',':','!','\\$','http','www']:
        if re.search(pat,core): bad.append((d['name'],pat))
    print(d['name'],d['sending_domain'],len(core.split()),'words |',d['subject'])
print('LINT',bad)
json.dump(new,open('new_drafts.json','w'),indent=1)
