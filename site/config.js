/* =========================================================================
   SITE CONFIG — edit this file to rename the brand, change the endpoint,
   or tune the estimate formula. Nothing else needs to change.
   ========================================================================= */
window.SITE_CONFIG = {
  brand: {
    name: "Mesa Data Labs",
    tagline: "Data licensing for established companies",
    contactEmail: "hello@example.com", // placeholder
    year: 2026
  },

  // Where the "Request review" form POSTs (JSON). Placeholder: while it
  // contains "REPLACE_ME" the submit handler is stubbed and never hits the network.
  submitEndpoint: "https://example.com/api/REPLACE_ME/review-request",
  waitlistEndpoint: "https://example.com/api/REPLACE_ME/waitlist",

  storageKey: "mesa-estimate-v1",

  /* ---------------------------------------------------------------------
     ESTIMATE FORMULA (fully transparent, runs in the browser)

       midpoint = staff × years × ratePerStaffYear
                  × industry × systems × work × access

       staff    = representative US full-time headcount for the chosen band
       years    = years of history held in the systems (capped at 15)
       systems  = 0.5 + sum of weights of the systems selected
       work     = 0.8 + 0.1 per kind of work recorded (max 1.4)
       access   = how much of the old data can still be reached

       low  = midpoint × rangeLow,  high = midpoint × rangeHigh
       Both rounded to roundTo. Illustrative only — buyers set final price.
     --------------------------------------------------------------------- */
  estimate: {
    ratePerStaffYear: 60,   // USD per US full-time employee per year of history
    rangeLow: 0.6,
    rangeHigh: 1.4,
    roundTo: 10000,
    minimumShown: 20000,

    staff: {             // band -> representative headcount
      "lt50":    { label: "Fewer than 50", value: 0,   notAFit: true },
      "50-99":   { label: "50 to 99",      value: 75,  fit: "limited" },
      "100-249": { label: "100 to 249",    value: 175 },
      "250-499": { label: "250 to 499",    value: 375 },
      "500+":    { label: "500 or more",   value: 650 }
    },
    years: {
      "lt2":   { label: "Under 2 years",     value: 1 },
      "2-4":   { label: "2 to 4 years",      value: 3 },
      "5-9":   { label: "5 to 9 years",      value: 7 },
      "10-14": { label: "10 to 14 years",    value: 12 },
      "15+":   { label: "15 years or more",  value: 15 }
    },
    industry: {
      "law":          { label: "Law firm",                       value: 1.25 },
      "accounting":   { label: "Accounting, audit or tax",       value: 1.2 },
      "software":     { label: "Software or IT services",        value: 1.3 },
      "consulting":   { label: "Consulting or professional services", value: 1.1 },
      "finance":      { label: "Financial services",             value: 1.2 },
      "insurance":    { label: "Insurance operations",           value: 1.15 },
      "healthcare":   { label: "Healthcare operator",            value: 1.1 },
      "manufacturing":{ label: "Manufacturer",                   value: 1.0 },
      "distribution": { label: "Wholesale distributor",          value: 0.95 },
      "other":        { label: "Something else",                 value: 0.8, fit: "possible" }
    },
    systems: {           // weights summed, then + 0.5
      "helpdesk": { label: "Help desk or support", examples: "Zendesk, ServiceNow, Freshdesk", value: 0.3,  icon: "i-helpdesk" },
      "crm":      { label: "CRM or sales",         examples: "Salesforce, HubSpot, Dynamics",  value: 0.25, icon: "i-crm" },
      "erp":      { label: "Accounting or ERP",    examples: "NetSuite, SAP, QuickBooks",      value: 0.2,  icon: "i-erp" },
      "code":     { label: "Code and engineering", examples: "GitHub, GitLab, Jira",           value: 0.35, icon: "i-code" },
      "comms":    { label: "Email, chat and drives", examples: "Microsoft 365, Google Workspace, Slack", value: 0.15, icon: "i-comms" }
    },
    workBase: 0.8,
    workPerItem: 0.1,
    workMax: 1.4,
    work: {
      "support":   "Customer support conversations and resolutions",
      "sales":     "Quotes, pipeline and won or lost deals",
      "finance":   "Invoices, payments and financial records",
      "projects":  "Projects, tickets and engineering work",
      "documents": "Contracts, memos, reports and drafted documents",
      "ops":       "Orders, claims, jobs or other operational records"
    },
    access: {
      "all":     { label: "Yes, all of them",       value: 1.0 },
      "some":    { label: "Some of them",           value: 0.75 },
      "exports": { label: "Only exports or backups", value: 0.6 },
      "none":    { label: "No, they are gone",      value: 0, gone: true }
    }
  },

  // Hypothetical examples — computed with the same formula as the quiz.
  examples: [
    {
      title: "A 180-person accounting firm",
      detail: "12 years in NetSuite, Salesforce and a client support desk. All U.S. staff.",
      answers: { staff: "100-249", years: "10-14", industry: "accounting",
                 systems: ["erp", "crm", "helpdesk", "comms"], work: ["support", "sales", "finance", "documents"], access: "all" }
    },
    {
      title: "A 400-person regional manufacturer",
      detail: "15+ years of orders, invoices and quality records in an ERP and shared drives.",
      answers: { staff: "250-499", years: "15+", industry: "manufacturing",
                 systems: ["erp", "comms"], work: ["finance", "ops", "documents"], access: "some" }
    },
    {
      title: "A 120-person software firm, winding down",
      detail: "7 years of GitHub, Jira and Zendesk history. Systems go offline in 60 days.",
      answers: { staff: "100-249", years: "5-9", industry: "software",
                 systems: ["code", "helpdesk", "comms"], work: ["support", "projects", "documents"], access: "all" }
    }
  ]
};
