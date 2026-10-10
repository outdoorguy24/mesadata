# Mesa Data Labs — data-worth estimate funnel (static)

Open `index.html` directly or serve the folder: `python3 -m http.server 8740`.

- `config.js` — brand name/tagline/email, submit + waitlist endpoints, the estimate formula constants, hypothetical examples. Rename the brand here only.
- `app.js` — quiz, estimate, localStorage resume (`mesa-estimate-v1`), stubbed submit (`submitReview` / `postJSON`).
- `styles.css` — palette in `:root`, single font: Zilla Slab (Google Fonts).
- `index.html` — page + inline SVG icon sprite.

Submit is stubbed: while the endpoint contains `REPLACE_ME`, no request is sent and the JSON payload is logged to the console. Put a real URL in `config.js` to POST JSON `{brand, submittedAt, contact, answers, estimate}`.

Formula: midpoint = staff × years × $60 × industry × (0.5 + Σ system weights) × min(1.4, 0.8 + 0.1 × kinds of work) × access. Range = midpoint × 0.6 to × 1.4, rounded to $10K (min $20K). Fewer than 50 staff → waitlist; systems gone → no range.
