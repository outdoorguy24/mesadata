import csv, re, json

rows = list(csv.DictReader(open('/workspace/outreach/partners.csv')))
byname = {r['name']: r for r in rows}

# ---- Step 1: email results -------------------------------------------------
# idx -> (email, source, status, note)
E = {
 'Ramone Param': ('ramone@kennedymanda.com','Gojiberry enrich_contact_email (contact 26146848)','tool-verified','tool returned no deliverability status'),
 'Jeff Reynolds': ('','Gojiberry returned jeff.reynolds@agital.com, his former company (left Agital Oct 2024); stale','unverified-skip','do not use agital.com address'),
 'Ryan B. Sanford': ('ryan.sanford@midcapadvisors.com','Gojiberry enrich_contact_email (contact 26146855)','tool-verified','tool returned no deliverability status; domain matches firm'),
 'Don Bravaldo III, CPA': ('dbravaldo@bc-advisors.com','Gojiberry enrich_contact_email (contact 26146865)','tool-verified','tool returned no deliverability status'),
 'Robert Jansen': ('rj@bridgewoodadvisors.com','Gojiberry enrich_contact_email (contact 26146866)','tool-verified','tool returned no deliverability status; domain matches firm'),
 'Jim Miller': ('','no LinkedIn profile to look up; no email found','unverified-skip','not looked up'),
 'Kevin Berson': ('kevin@kinected.com','Published on kinected.com/contact.html (Kevin directly)','published',''),
 'David Halvorson': ('dave@horizonmaa.com','Gojiberry enrich_contact_email (contact 26146875)','tool-verified','tool returned no deliverability status'),
 'Tom Lenfestey': ('tom@thelawpracticeexchange.com','Gojiberry enrich_contact_email (contact 26146879); firm site also publishes general info@thelawpracticeexchange.com','tool-verified','tool returned no deliverability status; info@ is the published fallback'),
 'Nelis Parts': ('nelis@kyrostrategies.com','Gojiberry enrich_contact_email (contact 26146883); kyrostrategies.com is his own firm (Kyro CFO is its practice)','tool-verified','tool returned no deliverability status'),
 'Scott Magnano': ('scott@magnanoadvisory.com','Gojiberry enrich_contact_email (contact 26146892)','tool-verified','tool returned no deliverability status; domain matches firm'),
 'David J. Richards, CPA': ('david.richards@crradvisors.com','Gojiberry enrich_contact_email (contact 26146893)','tool-verified','tool returned no deliverability status'),
 'Wade Kozich': ('wkozich@gbq.com','Gojiberry enrich_contact_email (contact 26146895)','tool-verified','tool returned no deliverability status'),
 'Ray Fernandez Jr., CPA, CM&AA': ('rfernandez@abipadvisors.com','Gojiberry enrich_contact_email (contact 26146896)','tool-verified','tool returned no deliverability status'),
 'Justin G. Vaughn': ('jvaughn@vaughn-law.com','Gojiberry enrich_contact_email (contact 26146897)','tool-verified','tool returned no deliverability status'),
 'Robbie Crosier': ('robbie@pkclegal.com','Gojiberry enrich_contact_email (contact 26146898)','tool-verified','tool returned no deliverability status'),
 'Sheila Seck': ('sseck@seckassociates.com','Gojiberry enrich_contact_email (contact 26146901)','tool-verified','tool returned no deliverability status'),
 'Richard E. Weltman': ('','Gojiberry enrichment (contact 26146902) still running, no result','unverified-skip','pending at time of run'),
 'Brett Rosen': ('brett@rosenadvisory.com','Published on rosenadvisory.com (principal)','published',''),
}
import os
extra = '/workspace/outreach/_extra_emails.json'
if os.path.exists(extra):
    for k,v in json.load(open(extra)).items(): E[k]=tuple(v)

out = []
for r in rows:
    e = E.get(r['name'], ('','not looked up (Medium/Low, credits kept modest)','unverified-skip',''))
    d = dict(r); d['email']=e[0]; d['email_source']=e[1]; d['email_status']=e[2]; d['email_note']=e[3]
    out.append(d)
fn = list(rows[0].keys())+['email','email_source','email_status','email_note']
with open('/workspace/outreach/partners_verified.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fn); w.writeheader(); w.writerows(out)

# ---- Step 2: copy ------------------------------------------------------------
OPT = 'If this isn\'t relevant, reply "no" and I won\'t follow up.'
SIG = 'Alex Starr\nMesa Data Labs\n[postal address]'

def wrap(body):
    return body.strip()+'\n\n'+OPT+'\n\n'+SIG

TYPES = {
 'M&A advisor': {
  'label':'M&A advisors and sell-side bankers',
  'subject':'sell-side records',
  'base':"""Hi {first},

{hook} After closing, those records tend to get archived or deleted, and some have value to technology and research buyers.

We run a free two-minute estimate that shows an owner what their business records could be worth. Nothing goes to a buyer without the owner's OK, and we can discuss a referral arrangement.

Would a one-paragraph summary you can forward be useful?""",
  'fu':[
   ('records at closing',"""Hi {first},

One more detail on how this works. The owner answers a few questions about the company and gets an estimate of what its records could be worth to technology and research buyers. We share nothing with a buyer unless the owner says yes, and we don't quote a figure we can't support.

Your clients can do it during prep without touching the sale timeline. Should I send the short version you can pass along?"""),
   ('sale timing',"""Hi {first},

Records are easiest to review before a process starts. After closing, systems get merged or shut off and the history is hard to find. Raising it at the engagement stage costs an owner about two minutes.

If a current client comes to mind, we can walk them through it on your terms and keep you in the loop. Worth a look?"""),
   ('closing the loop',"""Hi {first},

I'll assume the timing is off and stop here. If a seller ever asks what their records might be worth, the free estimate is there and I'm glad to send the summary then.

Good luck with the deals in your pipeline."""),
  ]},
 'Business broker': {
  'label':'Business brokers',
  'subject':'listing records',
  'base':"""Hi {first},

{hook} Sellers rarely think about their records until a buyer asks, and some of that history has value to technology and research buyers on top of the sale price.

We run a free two-minute estimate that shows an owner what their business records could be worth. Nothing goes to a buyer without the owner's OK, and we can discuss a referral arrangement.

Would a short note you can forward to a seller be useful?""",
  'fu':[
   ('seller conversations',"""Hi {first},

A quick picture of how it works. The owner answers a few questions and gets an estimate of what the company's records could be worth to technology and research buyers. The estimate is free, and we don't promise a number.

It fits at listing or valuation time, when the owner is already gathering documents. Want the short version to share with a client?"""),
   ('after the sale',"""Hi {first},

After a sale closes, the seller's records usually end up archived, merged into the buyer's systems or deleted. A licensing conversation has to happen before that, which makes listing the natural moment.

If you have a seller with 100+ employees, we can walk them through it and keep you informed. Worth a look?"""),
   ('closing the loop',"""Hi {first},

I haven't heard back, so I'll assume this isn't a fit right now and stop here. If a seller asks what their records could be worth, the free estimate is available and I'm glad to send the summary.

Good luck with your current listings."""),
  ]},
 'Fractional CFO': {
  'label':'Fractional CFOs',
  'subject':'exit prep records',
  'base':"""Hi {first},

{hook} Some technology and research buyers pay to license the same records you assemble for diligence.

We run a free two-minute estimate that shows an owner what their business records could be worth. Nothing goes to a buyer without the owner's OK, and we can discuss a referral arrangement.

Is there a client where this could be relevant?""",
  'fu':[
   ('records inventory',"""Hi {first},

More on how it works. The owner answers a few questions about the company and gets an estimate of what its records could be worth to technology and research buyers. We share nothing without the owner's OK, and we don't promise figures.

You could run it alongside an exit readiness review. Want the short version to pass to a client?"""),
   ('diligence timing',"""Hi {first},

Records are cleanest in the months before a sale, when the books and operating history are already being organized. A few months later the same material is in a data room and out of the owner's hands.

If a client is 12 to 24 months from an exit, this is a low-effort item to add. Should I send a summary?"""),
   ('closing the loop',"""Hi {first},

I'll assume the timing isn't right and stop here. If a client ever asks what their business records might be worth, the free estimate is there and I'm happy to send details.

Best of luck with the engagements ahead."""),
  ]},
 'CPA / accounting': {
  'label':'CPA and accounting firms',
  'subject':'exit planning records',
  'base':"""Hi {first},

{hook} Some of the records those clients already keep have value to technology and research buyers.

We run a free two-minute estimate that shows an owner what their business records could be worth. Nothing goes to a buyer without the owner's OK, and we can discuss a referral arrangement where your firm's rules allow.

Would a one-paragraph summary you can share with a client be useful?""",
  'fu':[
   ('what the estimate covers',"""Hi {first},

A few more specifics. The owner answers a few questions about the company and gets an estimate of what its business records could be worth to technology and research buyers. Nothing is shared with a buyer without the owner's OK, and we don't promise figures.

You can simply mention it during exit planning, and a referral arrangement is optional. Want the short version to share?"""),
   ('before the engagement ends',"""Hi {first},

When a client sells or merges, the old system data tends to be archived or retired along with the engagement. A licensing conversation has to happen before that.

If one of your mid-size clients is planning a sale or wind-down, we can walk them through the estimate and keep your firm informed. Worth a look?"""),
   ('closing the loop',"""Hi {first},

I'll assume this isn't a priority and stop here. If a client asks what their business records could be worth, the free estimate is there and I'm glad to send the summary.

Thanks for reading, and good luck through the season."""),
  ]},
 'Law firm': {
  'label':'Law firms',
  'subject':'records at exit',
  'base':"""Hi {first},

{hook} Their business records can have value to technology and research buyers.

We run a free two-minute estimate that shows an owner what their business records could be worth. Nothing goes to a buyer without the owner's OK, and any license would go through the client's counsel. We can discuss a referral arrangement where your rules allow.

Would a one-page summary for clients be useful?""",
  'fu':[
   ('license review',"""Hi {first},

More on how it works. The owner answers a few questions about the company and gets an estimate of what its business records could be worth to technology and research buyers. Client files stay out of scope, and a license would be reviewed by the client's counsel. We don't promise figures.

Should I send the one-page version?"""),
   ('wind-down records',"""Hi {first},

In a sale, restructuring or dissolution, records are often archived or deleted under a retention schedule. The licensing question has to be raised before that point, and the client's lawyer is usually the first to hear about the event.

If a matter comes to mind, we can walk the owner through the estimate and keep you in the loop. Worth a look?"""),
   ('closing the loop',"""Hi {first},

I'll assume this isn't relevant right now and stop here. If a client asks what their records could be worth, the free estimate is there and I'm glad to share the summary.

Thanks for your time."""),
  ]},
}

# personalised hooks and subjects (email 1)
H = {
 'Ramone Param': ("The consulting and technology-services firms you sell keep project, ticket and delivery history.", 'sell-side records'),
 'Ryan B. Sanford': ("TPAs, agencies and MGAs on your sell-side list hold years of claims and administration records.", 'insurance records'),
 'Don Bravaldo III, CPA': ("Your clients in IT, healthcare and industrials carry years of operating records into a sale.", 'sell-side records'),
 'Robert Jansen': ("The mid-size manufacturers and distributors you represent keep years of order, quality and supply records.", 'distributor records'),
 'David Halvorson': ("The manufacturing, IT services and distribution owners you advise hold years of operating history.", 'client records'),
 'Kevin Berson': ("The companies Kinected takes to market carry years of operating history.", 'sell-side records'),
 'Tom Lenfestey': ("The larger law firms you sell have operating history beyond client files.", 'firm records'),
 'Nelis Parts': ("Exit prep 12 to 18 months out is when clients organize their finance and operating history.", 'exit prep records'),
 'Scott Magnano': ("The healthcare operators you take through exit readiness keep years of business records, and patient data would stay out of scope.", 'exit readiness'),
 'David J. Richards, CPA': ("You sit in both the CPA and the sell-side seat for mid-size owners.", 'sell-side records'),
 'Wade Kozich': ("Your transaction team sees mid-market owners at valuation and diligence, when records are already organized.", 'diligence records'),
 'Ray Fernandez Jr., CPA, CM&AA': ("Your exit planning and diligence work reaches owners just as their records are being gathered.", 'exit planning records'),
 'Justin G. Vaughn': ("You advise closely held owners on exits, so you often hear about a sale first.", 'records at exit'),
 'Robbie Crosier': ("Founder-led exits are core to your practice, and those founders hold years of operating records.", 'founder exit records'),
 'Sheila Seck': ("Your practice covers both M&A and technology licensing, so you know what a data license involves.", 'licensing records'),
 'Richard E. Weltman': ("In a dissolution or wind-down, a company's records are about to be archived or deleted.", 'wind-down records'),
 'Brett Rosen': ("The larger insurance agencies and benefits firms you advise keep years of operating records.", 'agency records'),
}
DOMS = ['starrwealthgroup.com','claritywithai.co','sageridge.co','mesadatalabs.com']

def first(name):
    n = name.split(',')[0].split()[0]
    return n

# ---- sequences md ------------------------------------------------------------
md = ['# Mesa Data Labs: cold email sequences for referral partners','',
      'DRAFTS ONLY. Nothing has been sent. Plain text, no links, no tracking. Replace [postal address] before sending.',
      'Built with the marketingskills cold-email skill (peer voice, 2-4 word lowercase subjects, one interest-based ask, new angle per follow-up, breakup last) and its copywriting AI-tells list.','',
      'Cadence: email 1 on day 0, follow-up 1 day 3, follow-up 2 day 8, breakup day 14. Send Tue-Thu, 9-11 AM or 1-3 PM recipient time. Stop the sequence on any reply.',
      '',
      'Compliance notes: referral fees can be restricted for lawyers, CPAs and licensed bankers or brokers. The CPA and law versions say "where your rules allow". Confirm any arrangement with counsel before offering terms. Law-firm and healthcare lines say client files and patient data are out of scope; confirm that matches how Mesa actually works before sending.',
      '']
for k,t in TYPES.items():
    md += ['---','',f'## {t["label"]}','','**Email 1 (base). Subject: '+t['subject']+'**','','```',wrap(t['base']),'```','']
    for i,(s,b) in enumerate(t['fu'],1):
        day = {1:3,2:8,3:14}[i]
        tag = 'Breakup' if i==3 else f'Follow-up {i}'
        md += [f'**{tag} (day {day}). Subject: {s}**','','```',wrap(b),'```','']
open('/workspace/outreach/cold-email-sequences.md','w').write('\n'.join(md))

# ---- email1 drafts csv --------------------------------------------------------
prio = {'High':0,'Medium':1,'Low':2}
cands = [d for d in out if d['email_status'] in ('published','tool-verified') and d['name'] in H]
cands.sort(key=lambda d:(prio[d['priority']], rows.index(byname[d['name']])))
drafts=[]
count = {x:0 for x in DOMS}
for i,d in enumerate(cands):
    dom = DOMS[i%4]
    count[dom]+=1
    hook,subj = H[d['name']]
    t = TYPES[d['partner type']]
    body = wrap(t['base'].format(first=first(d['name']), hook=hook))
    drafts.append(dict(name=d['name'],firm=d['firm'],email=d['email'],subject=subj,body=body,sending_domain=dom,partner_type=d['partner type'],priority=d['priority'],email_status=d['email_status']))
with open('/workspace/outreach/email1-drafts.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['name','firm','email','subject','body','sending_domain','partner_type','priority','email_status']); w.writeheader(); w.writerows(drafts)
print(count, len(drafts))

# ---- lint --------------------------------------------------------------------
issues=[]
texts=[(f'seq:{k}:base',t['base']) for k,t in TYPES.items()]+[(f'seq:{k}:fu{j}',b) for k,t in TYPES.items() for j,(s,b) in enumerate(t['fu'],1)]+[(f'd:{d["name"]}',d['body']) for d in drafts]
for n,tx in texts:
    for pat in ['—','–',r'\bAI\b',r'\bnot\b',r'\bno\b',':','!','quick question','Quick question','just checking','hope this','leverage','http','www','\\$\\d']:
        for m in re.finditer(pat,tx):
            issues.append((n,pat,tx[max(0,m.start()-25):m.end()+25].replace('\n',' ')))
for n,p,c in issues: print(n,'|',p,'|',c)
for d in drafts:
    core=d['body'].split("\n\nIf this isn't")[0]
    print(d['name'],'words(body before opt-out):',len(core.split()),'| subj words',len(d['subject'].split()))
