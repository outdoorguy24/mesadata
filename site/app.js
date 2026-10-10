/* Mesa Data Labs estimate funnel — vanilla JS, no build step.
   All tunable values live in config.js (window.SITE_CONFIG). */
(function () {
  "use strict";
  var C = window.SITE_CONFIG;
  var E = C.estimate;

  /* ---------- brand fill ---------- */
  document.querySelectorAll("[data-brand]").forEach(function (el) { el.textContent = C.brand.name; });
  document.querySelectorAll("[data-tagline]").forEach(function (el) { el.textContent = C.brand.tagline; });
  document.querySelectorAll("[data-year]").forEach(function (el) { el.textContent = C.brand.year; });
  document.querySelectorAll("[data-email]").forEach(function (el) { el.textContent = C.brand.contactEmail; el.href = "mailto:" + C.brand.contactEmail; });
  document.title = "What is my company's data worth? | " + C.brand.name;

  /* ---------- helpers ---------- */
  function opts(map) { return Object.keys(map).map(function (k) { var v = map[k]; return { value: k, label: typeof v === "string" ? v : v.label, hint: v.examples, icon: v.icon }; }); }
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function money(n) {
    if (n >= 1e6) return "$" + (Math.round(n / 1e5) / 10).toString().replace(/\.0$/, "") + "M";
    return "$" + Math.round(n / 1000) + "K";
  }

  /* ---------- questions (order follows the funnel) ---------- */
  var QUESTIONS = [
    { id: "situation", title: "What is going on with the company right now?", help: "This helps us decide how quickly to review.",
      options: [
        { value: "normal", label: "Operating normally" },
        { value: "capital", label: "Looking for capital without giving up equity" },
        { value: "sale", label: "Considering a sale or merger" },
        { value: "selling", label: "Currently being sold" },
        { value: "acquired", label: "Recently acquired" },
        { value: "winding", label: "Winding down" }
      ] },
    { id: "offline", title: "When do the old systems go offline?", help: "Records can only be licensed while they still exist.",
      options: [
        { value: "already", label: "Already offline" },
        { value: "30d", label: "Within 30 days" },
        { value: "1-3m", label: "In 1 to 3 months" },
        { value: "3-6m", label: "In 3 to 6 months" },
        { value: "none", label: "More than 6 months out, or no plans" }
      ] },
    { id: "access", title: "Can you still get into those systems?", help: "Exports and backups count.", options: opts(E.access) },
    { id: "staff", title: "How many full-time employees in the U.S.?", help: "W-2 staff. If the company has closed, use its last full year.", options: opts(E.staff) },
    { id: "industry", title: "Which industry fits best?", help: "Buyers ask for some industries more than others.", options: opts(E.industry) },
    { id: "systems", title: "Which systems does the company run on?", help: "Pick all that apply.", multi: true, options: opts(E.systems) },
    { id: "years", title: "How many years of history do those systems hold?", help: "Count what the systems hold today, not the age of the company.", options: opts(E.years) },
    { id: "work", title: "What work gets recorded in them?", help: "Pick all that apply. This is what buyers look at first.", multi: true, options: opts(E.work) }
  ];

  /* ---------- estimate formula (see config.js for the written version) ---------- */
  function computeEstimate(a) {
    var staff = E.staff[a.staff], years = E.years[a.years], ind = E.industry[a.industry], acc = E.access[a.access];
    if (!staff || !years || !ind || !acc) return null;
    var sysSum = (a.systems || []).reduce(function (s, k) { return s + (E.systems[k] ? E.systems[k].value : 0); }, 0);
    var systemsF = 0.5 + sysSum;
    var workF = Math.min(E.workMax, E.workBase + E.workPerItem * (a.work || []).length);
    var mid = staff.value * years.value * E.ratePerStaffYear * ind.value * systemsF * workF * acc.value;
    var round = function (n) { return Math.max(E.minimumShown, Math.round(n / E.roundTo) * E.roundTo); };
    var fit = "Strong potential fit";
    if (staff.fit === "limited") fit = "Limited fit";
    else if (ind.fit === "possible" || years.value < 3 || acc.value < 0.7 || (a.systems || []).length < 2) fit = "Good potential fit";
    return {
      gone: !!acc.gone, mid: mid,
      low: round(mid * E.rangeLow), high: round(mid * E.rangeHigh), fit: fit,
      factors: [
        ["U.S. full-time staff", staff.value + " (" + staff.label + ")"],
        ["Years of history", years.value + " (capped at 15)"],
        ["Rate per staff-year", "$" + E.ratePerStaffYear],
        ["Industry", "\u00d7 " + ind.value],
        ["Systems", "\u00d7 " + systemsF.toFixed(2)],
        ["Kinds of work", "\u00d7 " + workF.toFixed(2)],
        ["Access to old data", "\u00d7 " + acc.value]
      ]
    };
  }

  /* ---------- state + persistence ---------- */
  var blank = function () { return { step: 0, view: "quiz", answers: {}, contact: {}, waitlistEmail: "" }; };
  var state = load() || blank();
  function load() { try { return JSON.parse(localStorage.getItem(C.storageKey)); } catch (e) { return null; } }
  function save() { try { localStorage.setItem(C.storageKey, JSON.stringify(state)); } catch (e) {} }

  var body = document.getElementById("quizBody");
  var nav = document.getElementById("quizNav");
  var nextBtn = document.getElementById("nextBtn");
  var backBtn = document.getElementById("backBtn");
  var bar = document.getElementById("progressBar");
  var plabel = document.getElementById("progressLabel");
  var resumeBox = document.getElementById("resume");

  /* resume banner */
  var hasProgress = Object.keys(state.answers || {}).length > 0 && state.view !== "done";
  if (hasProgress) {
    resumeBox.hidden = false;
    resumeBox.querySelector("[data-resume-step]").textContent = Math.min(state.step + 1, QUESTIONS.length);
  }
  resumeBox.addEventListener("click", function (e) {
    var act = e.target.getAttribute("data-action");
    if (act === "restart") { state = blank(); save(); }
    if (act) { resumeBox.hidden = true; document.getElementById("quiz").hidden = false; render(); }
  });

  function answered(q) {
    var v = state.answers[q.id];
    return q.multi ? Array.isArray(v) && v.length > 0 : !!v;
  }

  function render() {
    if (state.view === "result") return renderResult();
    if (state.view === "waitlist") return renderWaitlist();
    if (state.view === "done") return renderDone();
    var q = QUESTIONS[state.step];
    var pct = (state.step / QUESTIONS.length) * 100;
    bar.style.width = pct + "%";
    plabel.textContent = "Question " + (state.step + 1) + " of " + QUESTIONS.length;
    nav.hidden = false;
    backBtn.style.visibility = state.step === 0 ? "hidden" : "visible";
    var cur = state.answers[q.id];
    var html = '<fieldset class="q"><legend><h3 class="q-title">' + esc(q.title) + '</h3></legend>' +
      '<p class="q-help">' + esc(q.help) + '</p><div class="options' + (q.options.some(function (o) { return o.icon; }) ? " with-icons" : "") + '">';
    q.options.forEach(function (o) {
      var sel = q.multi ? (cur || []).indexOf(o.value) > -1 : cur === o.value;
      html += '<button type="button" class="option' + (sel ? " selected" : "") + '" data-value="' + esc(o.value) + '" aria-pressed="' + sel + '">' +
        (o.icon ? '<span class="arch-icon small"><svg viewBox="0 0 48 48"><use href="#' + o.icon + '"/></svg></span>' : '') +
        '<span class="opt-text"><span class="opt-label">' + esc(o.label) + '</span>' + (o.hint ? '<span class="opt-hint">' + esc(o.hint) + '</span>' : '') + '</span>' +
        '<span class="opt-mark" aria-hidden="true"><svg viewBox="0 0 48 48"><use href="#i-check"/></svg></span></button>';
    });
    html += "</div></fieldset>";
    body.innerHTML = html;
    nextBtn.textContent = state.step === QUESTIONS.length - 1 ? "See my estimate" : "Continue";
    nextBtn.disabled = !answered(q);

    body.querySelectorAll(".option").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var v = btn.getAttribute("data-value");
        if (q.multi) {
          var arr = (state.answers[q.id] || []).slice();
          var i = arr.indexOf(v); if (i > -1) arr.splice(i, 1); else arr.push(v);
          state.answers[q.id] = arr; save(); render();
        } else {
          state.answers[q.id] = v; save(); render();
          setTimeout(next, 220);
        }
      });
    });
  }

  function next() {
    var q = QUESTIONS[state.step];
    if (!answered(q)) return;
    if (q.id === "staff" && E.staff[state.answers.staff].notAFit) { state.view = "waitlist"; save(); return render(); }
    if (state.step < QUESTIONS.length - 1) state.step++;
    else state.view = "result";
    save(); render(); focusCard();
  }
  function back() { if (state.step > 0) { state.step--; save(); render(); } }
  nextBtn.addEventListener("click", function () { next(); });
  backBtn.addEventListener("click", back);

  function focusCard() {
    var card = document.getElementById("quiz");
    var top = card.getBoundingClientRect().top;
    if (top < 0 || top > window.innerHeight * 0.6) card.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  function urgent() {
    var a = state.answers;
    return a.offline === "already" || a.offline === "30d" || a.situation === "winding" || a.situation === "selling";
  }

  function renderResult() {
    bar.style.width = "100%"; plabel.textContent = "Your estimate"; nav.hidden = true;
    var r = computeEstimate(state.answers);
    var c = state.contact || {};
    var head;
    if (!r || r.gone) {
      head = '<div class="result"><p class="eyebrow">Your estimate</p><h3 class="result-range small">We can&rsquo;t estimate a range yet.</h3>' +
        '<p class="result-note">If the systems and their backups are gone, there is usually nothing left to license. If you think backups may exist somewhere, request a review and we&rsquo;ll tell you honestly whether it is worth looking.</p></div>';
    } else {
      head = '<div class="result"><p class="eyebrow">Illustrative range</p>' +
        '<p class="result-range">' + money(r.low) + ' <span>to</span> ' + money(r.high) + '</p>' +
        '<p class="fit-badge' + (r.fit === "Limited fit" ? " limited" : "") + '">' + r.fit + '</p>' +
        (urgent() ? '<p class="urgent">Time-sensitive. We prioritize reviews where systems are closing soon.</p>' : '') +
        '<p class="result-note">Based on headcount, years of history, systems and the kinds of work recorded. Not an offer. Final price is set by buyers after review. No files required.</p>' +
        '<details class="breakdown"><summary>See the math</summary><table>' +
        r.factors.map(function (f) { return "<tr><td>" + esc(f[0]) + "</td><td>" + esc(f[1]) + "</td></tr>"; }).join("") +
        '<tr class="total"><td>Midpoint</td><td>' + money(r.mid) + '</td></tr></table>' +
        '<p class="fine">Range = midpoint \u00d7 ' + E.rangeLow + ' to midpoint \u00d7 ' + E.rangeHigh + ', rounded.</p></details></div>';
    }
    body.innerHTML = head +
      '<form class="contact" id="contactForm" novalidate>' +
      '<h3 class="q-title">Request a review</h3><p class="q-help">We&rsquo;ll look at the fit and reply by email. Nothing goes to a buyer without your OK.</p>' +
      field("name", "Full name", "text", c.name, "name") +
      field("email", "Work email", "email", c.email, "email") +
      field("company", "Company", "text", c.company, "organization") +
      field("role", "Your role", "text", c.role, "organization-title") +
      '<p class="form-error" id="formError" role="alert"></p>' +
      '<div class="form-actions"><button type="button" class="btn-link" id="editBtn">Edit answers</button>' +
      '<button type="submit" class="btn btn-primary" id="submitBtn">Request review</button></div></form>';

    var form = document.getElementById("contactForm");
    form.addEventListener("input", function (e) { state.contact[e.target.name] = e.target.value; save(); });
    document.getElementById("editBtn").addEventListener("click", function () { state.view = "quiz"; state.step = QUESTIONS.length - 1; save(); render(); });
    form.addEventListener("submit", function (e) { e.preventDefault(); submitReview(form, r); });
  }

  function field(name, label, type, val, ac) {
    return '<label class="field"><span>' + label + '</span><input name="' + name + '" type="' + type + '" autocomplete="' + ac + '" value="' + esc(val || "") + '" required></label>';
  }

  var FREEMAIL = /@(gmail|yahoo|hotmail|outlook|aol|icloud|proton|protonmail|live|msn)\./i;

  /* ---------- SUBMIT (STUBBED) ----------
     Builds a JSON payload and POSTs it to C.submitEndpoint.
     While the endpoint contains "REPLACE_ME" no network call is made;
     the payload is logged to the console instead. Wire up a real endpoint
     (form service, serverless function, CRM webhook) in config.js. */
  function submitReview(form, r) {
    var err = document.getElementById("formError");
    var c = state.contact;
    err.textContent = "";
    if (!c.name || !c.company || !c.role) { err.textContent = "Please fill in every field."; return; }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(c.email || "")) { err.textContent = "Please enter a valid email address."; return; }
    if (FREEMAIL.test(c.email)) { err.textContent = "Please use your work email so we can match it to the company."; return; }

    var payload = {
      brand: C.brand.name, submittedAt: new Date().toISOString(),
      contact: c, answers: state.answers,
      estimate: r && !r.gone ? { low: r.low, high: r.high, fit: r.fit } : null
    };
    var btn = document.getElementById("submitBtn");
    btn.disabled = true; btn.textContent = "Sending\u2026";
    postJSON(C.submitEndpoint, payload).then(function () {
      state.view = "done"; save(); render();
    }).catch(function () {
      btn.disabled = false; btn.textContent = "Request review";
      err.textContent = "Something went wrong sending that. Your answers are saved; please try again.";
    });
  }

  function postJSON(url, payload) {
    if (url.indexOf("REPLACE_ME") > -1) {
      console.info("[stub] Would POST to", url, payload);
      return new Promise(function (res) { setTimeout(res, 600); });
    }
    return fetch(url, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) })
      .then(function (res) { if (!res.ok) throw new Error("HTTP " + res.status); return res; });
  }

  function renderWaitlist() {
    bar.style.width = "100%"; plabel.textContent = "Thanks for checking"; nav.hidden = true;
    body.innerHTML = '<div class="endstate"><span class="arch-icon"><svg viewBox="0 0 48 48"><use href="#i-saguaro"/></svg></span>' +
      '<h3 class="q-title">Not a fit right now.</h3>' +
      '<p class="q-help">Buyers we work with are looking for companies with 50 or more U.S. full-time staff, ideally 100+. If that changes, or buyers start asking for smaller companies, we&rsquo;ll let you know.</p>' +
      '<form class="contact" id="waitForm" novalidate>' + field("wemail", "Work email", "email", state.waitlistEmail, "email") +
      '<p class="form-error" id="waitError" role="alert"></p>' +
      '<div class="form-actions"><button type="button" class="btn-link" id="wBack">Change my answer</button><button class="btn btn-primary" type="submit">Join the waitlist</button></div></form></div>';
    document.getElementById("wBack").addEventListener("click", function () { state.view = "quiz"; save(); render(); });
    document.getElementById("waitForm").addEventListener("submit", function (e) {
      e.preventDefault();
      var v = e.target.wemail.value.trim();
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v)) { document.getElementById("waitError").textContent = "Please enter a valid email address."; return; }
      state.waitlistEmail = v; save();
      postJSON(C.waitlistEndpoint, { email: v, answers: state.answers, submittedAt: new Date().toISOString() }).then(function () {
        body.innerHTML = '<div class="endstate"><span class="arch-icon"><svg viewBox="0 0 48 48"><use href="#i-sun"/></svg></span><h3 class="q-title">You&rsquo;re on the list.</h3><p class="q-help">We&rsquo;ll email ' + esc(v) + ' only if something changes for companies your size.</p></div>';
      });
    });
  }

  function renderDone() {
    bar.style.width = "100%"; plabel.textContent = "Request received"; nav.hidden = true;
    var c = state.contact || {};
    body.innerHTML = '<div class="endstate"><span class="arch-icon"><svg viewBox="0 0 48 48"><use href="#i-sun"/></svg></span>' +
      '<h3 class="q-title">Thanks, ' + esc((c.name || "").split(" ")[0] || "we have it") + '.</h3>' +
      '<p class="q-help">We&rsquo;ll review ' + esc(c.company || "your company") + ' and reply to ' + esc(c.email || "you") + '. Nothing goes to a buyer without your OK.</p>' +
      '<button type="button" class="btn-link" id="newBtn">Start a new estimate</button></div>';
    document.getElementById("newBtn").addEventListener("click", function () { state = blank(); save(); render(); });
  }

  /* ---------- examples (same formula) ---------- */
  var exWrap = document.getElementById("examplesList");
  var exIcons = ["i-erp", "i-mesa", "i-code"];
  exWrap.innerHTML = C.examples.map(function (ex, i) {
    var r = computeEstimate(ex.answers);
    return '<article class="example"><span class="arch-icon"><svg viewBox="0 0 48 48"><use href="#' + exIcons[i % 3] + '"/></svg></span>' +
      '<p class="tag">Hypothetical example</p><h3>' + esc(ex.title) + '</h3><p>' + esc(ex.detail) + '</p>' +
      '<p class="ex-fit">' + r.fit + '</p><p class="ex-range">' + money(r.low) + ' to ' + money(r.high) + '</p></article>';
  }).join("");

  // Expose for debugging / testing
  window.MesaEstimate = { compute: computeEstimate, state: function () { return state; } };

  if (!hasProgress) render();
  else document.getElementById("quiz").hidden = true;
})();
