types={
"M&A advisors and sell-side bankers":(
"Hi {first}, we run a free estimate tool that shows owners of 100+ person companies what their business records could be worth to technology and research buyers. Some of your sell-side clients may hold records worth licensing. Happy to connect.",
"""Thanks for connecting, {first}.

We help established companies (100+ employees) see what their business records could be worth when licensed to technology and research buyers. The estimate is free and takes about two minutes. Nothing is shared with a buyer without the owner's OK.

For clients preparing to sell, the records are often an unused asset, and they tend to be lost or archived after closing. We can discuss a referral arrangement if it's useful to your clients.

Would you like a one-paragraph summary you can forward?"""),
"Business brokers":(
"Hi {first}, we offer owners of 100+ person companies a free estimate of what their business records could be worth to technology and research buyers. It may help your sellers. We can discuss a referral arrangement. Glad to connect.",
"""Thanks for connecting, {first}.

We give owners of established companies (100+ employees) a free, two-minute estimate of what their business records could be worth when licensed to technology and research buyers. Nothing is shared with a buyer without the owner's OK.

For your sellers, this is potential extra value beyond the sale price, and it is easy to raise at listing or valuation time. We can discuss a referral arrangement.

Want a short note to forward to a client or two?"""),
"Fractional CFOs":(
"Hi {first}, we offer a free estimate showing what a 100+ person company's business records could be worth to technology and research buyers. It may help your exit-prep clients. We can discuss a referral arrangement. Glad to connect.",
"""Thanks for connecting, {first}.

We help established companies (100+ employees) see what their business records could be worth when licensed to technology and research buyers. The estimate is free, takes about two minutes, and nothing is shared with a buyer without the owner's OK.

For clients preparing an exit, the records are already organized for diligence, so the same work may support a licensing conversation. We can discuss a referral arrangement.

Is there a client where this could be relevant? We can walk you through the estimate."""),
"CPAs and accounting firms":(
"Hi {first}, we offer a free estimate showing what a 100+ person company's business records could be worth to technology and research buyers. It may help your mid-size clients. We can discuss a referral arrangement, where your rules allow.",
"""Thanks for connecting, {first}.

We help established companies (100+ employees) see what their business records could be worth when licensed to technology and research buyers. The estimate is free and takes about two minutes. Nothing is shared with a buyer without the owner's OK.

Clients planning a sale, merger or wind-down may find this useful, and it is simple to mention during exit planning. We can discuss a referral arrangement that fits your firm's independence and fee rules.

May we send a short summary to share with a client?"""),
"Law firms":(
"Hi {first}, we offer a free estimate showing what a 100+ person company's business records could be worth to technology and research buyers. It may help clients selling or winding down. We can discuss a referral arrangement, where your rules allow.",
"""Thanks for connecting, {first}.

We help established companies (100+ employees) see what their business records could be worth when licensed to technology and research buyers. The estimate is free and takes about two minutes. Nothing is shared with a buyer without the owner's OK, and any license would be reviewed by the client's counsel.

It may be relevant for clients in a sale, restructuring or dissolution, where records are otherwise archived or deleted. We can discuss a referral arrangement that complies with your professional-conduct rules.

Would a one-page summary for clients be useful?"""),
}
out=["# Outreach drafts (DRAFT ONLY, nothing has been sent)\n",
"Working brand: Mesa (final name TBD). Replace {first} with the partner's first name. Written as \"we\". No phone number, no promised amounts.\n",
"**Compliance check before any send:** referral fees can be restricted for lawyers (fee-sharing rules), CPAs (commission and independence rules), and bankers or brokers licensed through a broker-dealer. The drafts say \"where your rules allow\" for that reason. Confirm the actual arrangement with counsel before you offer terms.\n"]
for t,(n,f) in types.items():
    out.append(f"\n## {t}\n")
    out.append(f"**LinkedIn connection note** ({len(n)} chars)\n\n{n}\n")
    out.append(f"**Follow-up message (after they accept)**\n\n{f}\n")
    assert len(n)<300,(t,len(n))
    print(t,len(n))
open("drafts.md","w").write("\n".join(out))
