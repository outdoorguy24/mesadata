# Mesa Data Labs: project notes (as of 2026-10-10)

**What it is:** a free "what are your company's records worth?" estimate funnel for established companies (100+ employees) in law, accounting, software/IT services, consulting, financial services, insurance ops, healthcare operators, manufacturers, wholesale distributors. Modeled on briggsanalytics.com/estimate (@BriggsBuilds), but focused on larger companies, honest ranges, and no "AI" wording on the site.

**Decisions so far**
- Brand: Mesa Data Labs (domain candidate mesadatalabs.com, appeared unregistered in a quick RDAP check on 2026-10-10; not yet purchased; verify at a registrar).
- Style: southwestern desert, one font family (Zilla Slab), arch-framed line icons, cream/terracotta/brown/charcoal palette, less is more.
- Leads: form submissions go to a Google Sheet (not yet wired; submitEndpoint in site/config.js is a stub). Footer contact email is a placeholder.
- X: personal account, display name "Alexander Hartley", real photo, handle @alexhartley_ai (preferred; verify it is free), bio "Helping established companies find out what their data is worth to AI labs. Building Mesa Data." Human approves each post/reply; no auto-posting.
- Reach for 100+ person owners: LinkedIn, referral partners (M&A advisors, brokers, fractional CFOs, CPA and law firms), associations/events, peer groups (Vistage/EO), trade media. X is mainly for credibility and meeting advisors.
- Direct outreach to referral partners first (drafts only; nothing sent yet). Referral fees may be restricted for lawyers/CPAs/licensed bankers; check with counsel.

**Folders**
- `site/` static site (index.html, styles.css, app.js, config.js, README.md, screenshots/). Run with `python3 -m http.server`.
- `x-plan/` X growth plan (x-plan.md), 58-account scan list, metrics template.
- `outreach/` 51 referral-partner prospects (partners.csv) and short outreach drafts (drafts.md).

**Open items:** buy the domain, host the site (e.g. Cloudflare Pages), connect form to Google Sheet, set real contact email, create X account, pick LinkedIn profile for outreach, review drafts.
