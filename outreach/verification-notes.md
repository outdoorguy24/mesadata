# Email verification notes (Oct 10, 2026)

## What was tried
| Method | Result | Reliability |
|---|---|---|
| Box SMTP (port 25) | Outbound 25 blocked from the box (443 works). Unusable. | n/a |
| Apify `cold_email_master/free-email-verifier` | 403 permission error. | n/a |
| Apify `s-r/free-email-verifier---verify-email-address` | Ran on 8 addresses. Returns only DNS/MX/blocklist ("status: safe", deliverable: null, catch_all: null). Mailbox NOT checked. | MX-only. Not a bounce check. |
| Apify `automation-lab/smtp-email-verifier` (SMTP RCPT) | Ran on 16 + 3 controls. Every result "unknown": Apify blocks outbound port 25. Cost about $0.05 (start fee + 16 x $0.001). | Useless here. |
| Apify paid verifier (cold_email_master/email-verifier-validator) | Requires paid Apify plan (account is FREE). Not run. | n/a |
| Apollo people_match (email_status) | Plan does not include People Enrichment. | n/a |
| Gojiberry contact record | No deliverability field, only email + bounced flag. | None. |
| Composio verifier toolkits (Hunter, Emailable, ZeroBounce-style, EmailListVerify, Listclean, Instantly, SendGrid) | Exist, but none is connected for this account. Not connected (needs the user). | n/a |
| **SMTP RCPT probe from the Composio remote sandbox** (`smtp_probe.py`) | Port 25 is open there. Does EHLO, MAIL FROM, RCPT TO real address, RSET, MAIL FROM again, RCPT TO a random fake address on the same domain, QUIT. No DATA, no message sent. | Good for Google Workspace and Proofpoint-fronted domains (real mailbox check + catch-all detection). |

## Limits of the SMTP probe
- Microsoft 365 / Exchange Online hosts reject the sandbox IP (34.168.15.191) at RCPT with "blocked using Spamhaus". So every Microsoft-hosted address is UNVERIFIABLE by SMTP from here, not invalid.
- Catch-all domains (Google Workspace catch-all, Proofpoint accept-all, arsmtp relay) accept any address, so a 250 proves nothing about the person's mailbox.
- Greylisting/anti-probe at some hosts yields unknown.
- A 250 on the real address plus a 5xx on a random fake = mailbox exists (strong evidence, still not a guarantee of inbox delivery).

## Grading rules used
- **verified**: (a) SMTP: real address 250 AND random fake 5xx; or (b) address published on the person's own firm site (or firm team/contact page) AND domain has MX and is not rejected.
- **risky**: catch-all domain without publication; Microsoft-hosted (probe blocked) without publication; unknown/greylisted.
- **invalid**: SMTP 5.1.1 user unknown for the real address, or no MX.

## Recommendation
For a 100% guarantee, connect a real verifier (Truelist, ZeroBounce, Hunter or Emailable) and run the risky list through it. Microsoft-hosted and catch-all addresses are exactly what these tools resolve best.

## Results (Oct 10, 2026)
Drafts are Gmail drafts only. Nothing sent. Placeholder [postal address] still in every body.

### HOLD (risky, starrwealthgroup.com) (1)
- Ramone Param <ramone@kennedymanda.com> | risky | sell-side records

### claritywithai.co (10)
- Ryan B. Sanford <ryan.sanford@midcapadvisors.com> | verified | insurance records
- David Halvorson <dave@horizonmaa.com> | verified | client records
- David J. Richards, CPA <david.richards@crrcpa.com> | verified | sell-side records
- Jack Simonian <jack@blackcastlepartners.com> | verified | project records
- Nick Fares <nick@sumcapadvisors.com> | verified | manufacturer records
- Robert Stasiak <rob.stasiak@ridgetrailcap.com> | verified | production records
- Robert J. Gonzales <robert@emerge.law> | verified | wind-down records
- Jessica Barclay <jbarclay@efcg.com> | verified | aec records
- Christopher Jahnle <cjahnle@haverfordcapital.com> | verified | physician group records
- Byron Burge <byron@burgeoningenterprises.com> | verified | practice sale records

### sageridge.co (10)
- Don Bravaldo III, CPA <dbravaldo@bc-advisors.com> | verified | sell-side records
- Wade Kozich <wkozich@gbq.com> | verified | diligence records
- Ray Fernandez Jr., CPA, CM&AA <rfernandez@abipadvisors.com> | verified | exit planning records
- Sheila Seck <sseck@seckassociates.com> | verified | licensing records
- Mike Moran <mmoran@mahealthcareadvisors.com> | verified | healthcare records
- Chris Nelms, CPA <cnelms@williamsmarston.com> | verified | diligence records
- Parth Kalaria <parth@kalarialaw.com> | verified | owner exit records
- Andrew Rice <anrice@troutcpa.com> | verified | transaction records
- Gary Moon <gary@nfluencepartners.com> | verified | healthtech records
- Dan Sokol <dan@sokolb2b.com> | verified | b2b owner records

### starrwealthgroup.com (10)
- Robert Jansen <rj@bridgewoodadvisors.com> | verified | distributor records
- Kevin Berson <kevin@kinected.com> | verified | sell-side records
- Scott Magnano <scott@magnanoadvisory.com> | verified | exit readiness
- Justin G. Vaughn <jvaughn@vaughn-law.com> | verified | records at exit
- Brett Rosen <brett@rosenadvisory.com> | verified | agency records
- Eric I. Mendelsohn <eric@archveoadvisors.com> | verified | distribution records
- Jerry Zhou, CPA <jzhou@hoodstrong.com> | verified | records in diligence
- Gregory Seigel <greg@seigeladvisoryservices.com> | verified | practice records
- Mike DeMaio <mike@crowncfo.com> | verified | exit planning records
- Ryan Soer <rsoer@intrepidib.com> | verified | owner records at sale

### HOLD (risky, sageridge.co) (1)
- Tom Lenfestey <tom@thelawpracticeexchange.com> | risky | firm records

### HOLD (risky, claritywithai.co) (2)
- Nelis Parts <nelis@kyrostrategies.com> | risky | exit prep records
- Robbie Crosier <robbie@pkclegal.com> | risky | founder exit records

### alexstarr.com (9)
- Michael Ifraimov <mifraimov@crownpeakadvisors.com> | verified | msp records
- Chuck Fenske <cgf@carletonmckenna.com> | verified | construction records
- Michael Carter <mcarter@cartermorse.com> | verified | family business records
- Tim Mueller <tmueller@itexchangenet.com> | verified | it services records
- Michael Polgur, CPA <mike@mpadvisoryllc.com> | verified | sell-side prep
- Michael B. Overstreet <moverstreet@grayreed.com> | verified | sale records
- Steve C. Swann <sswann@bmf.cpa> | verified | seller records
- Brian Kennedy <brian@racohenconsulting.com> | verified | staffing records
- John R. Allen III <john@allenbusinessadvisors.com> | verified | project history
