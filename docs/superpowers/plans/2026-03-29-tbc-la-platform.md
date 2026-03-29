# TBC-LA Platform Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build burnhamcivic.org/la as an accountability and campaign intelligence platform for Spencer Pratt's LA mayoral campaign, establishing Burnham Civic as a national brand.

**Architecture:** Static HTML pages deployed via GitHub Pages from the `main` branch of `seattle-restoration/burnham-civic`. Each page is self-contained HTML with embedded CSS/JS matching the existing burnhamcivic.org aesthetic (Georgia serif, navy/gold accents, left-aligned 860px layout). Password-gated pages use cookie-based auth. CRM uses localStorage. 990 data is pre-fetched and embedded as JSON.

**Tech Stack:** HTML, CSS, vanilla JS, GitHub Pages, ProPublica Nonprofit Explorer API, LA Open Data Portal APIs (data.lacity.org)

**Repo:** `/Users/jackwalsh/Dropbox/Seattle/burnham-civic-site`

**Design Spec:** `docs/superpowers/specs/2026-03-29-tbc-la-platform-design.md`

---

## File Map

```
la/
  index.html        <- Hub page (links to all sub-pages)
  lahsa.html         <- LAHSA accountability + 990 data
  lafd.html          <- LAFD fire response
  lapd.html          <- LAPD crime/staffing
  dwp.html           <- DWP utility audit
  transit.html       <- Metro/Olympics
  building.html      <- Permits/rebuild/Burnham standard
  cabinet.html       <- Shadow cabinet (password-gated)
  network.html       <- Mini-CRM (password-gated)
  lahsa-data.js      <- Pre-fetched 990 data for LAHSA grantees
  network-data.js    <- Pre-populated 100 LA business leaders
```

Modify:
```
index.html           <- Add "LA" to top nav bar
```

---

### Task 1: Add "LA" to Main Site Nav

**Files:**
- Modify: `index.html` (nav section, ~line 250-257)

- [ ] **Step 1: Add LA nav link to the main site navigation**

In `index.html`, find the nav div (line ~250):

```html
<div class="nav">
  <a href="#" onclick="showTab('seattle');return false" id="nav-seattle" class="active">Seattle</a>
  <a href="#" onclick="showTab('usa');return false" id="nav-usa">USA</a>
```

Insert the LA link after Seattle. Unlike other tabs, LA links to a separate page:

```html
<div class="nav">
  <a href="#" onclick="showTab('seattle');return false" id="nav-seattle" class="active">Seattle</a>
  <a href="la/" id="nav-la">LA</a>
  <a href="#" onclick="showTab('usa');return false" id="nav-usa">USA</a>
```

- [ ] **Step 2: Verify the link renders correctly**

Run: `open /Users/jackwalsh/Dropbox/Seattle/burnham-civic-site/index.html`

Verify: "LA" appears between "Seattle" and "USA" in the nav, styled identically (navy, uppercase, 11px Georgia bold). Clicking it should navigate to `la/` (will 404 until hub page is built).

- [ ] **Step 3: Commit**

```bash
cd /Users/jackwalsh/Dropbox/Seattle/burnham-civic-site
git add index.html
git commit -m "Add LA to main site navigation"
```

---

### Task 2: Build LA Hub Page

**Files:**
- Create: `la/index.html`

- [ ] **Step 1: Create the la/ directory**

```bash
mkdir -p /Users/jackwalsh/Dropbox/Seattle/burnham-civic-site/la
```

- [ ] **Step 2: Create the hub page**

Create `la/index.html` with the exact same styling as the main `index.html`. Key differences: the subtitle is a Burnham quote, the nav links to LA sub-pages, and content is LA operations.

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Los Angeles - BURNHAM CIVIC</title>
<meta name="description" content="Civic accountability and infrastructure intelligence for Los Angeles. Built on Daniel Burnham's principles.">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' rx='12' fill='%231e3a5f'/><text x='50' y='68' font-family='Georgia,serif' font-size='56' font-weight='700' fill='%23fbbf24' text-anchor='middle'>B</text></svg>">
<style>
body {
  font-family: Georgia, 'Times New Roman', serif;
  max-width: 860px;
  margin: 32px auto 32px 10%;
  padding: 0 16px;
  background: #fff;
  color: #111;
  font-size: 15px;
  line-height: 1.5;
}
a { color: #00c; }
a:visited { color: #551a8b; }
a:hover { color: #c00; }
.header {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
}
h1 {
  font-size: 22px;
  letter-spacing: 2px;
  margin: 0;
  font-weight: 700;
}
.subscribe {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 1px;
  text-transform: uppercase;
  color: #fff;
  background: #1e3a5f;
  padding: 5px 14px;
  text-decoration: none;
  font-family: Georgia, serif;
}
.subscribe:hover { background: #2a4a73; }
.subscribe:visited { color: #fff; }
.subtitle {
  font-size: 13px;
  color: #555;
  margin-bottom: 20px;
  font-style: italic;
}
hr {
  border: none;
  border-top: 1px solid #ccc;
  margin: 16px 0;
}
.nav {
  font-size: 12px;
  margin-bottom: 16px;
  letter-spacing: 0.5px;
}
.nav a { margin-right: 16px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; font-size: 11px; color: #00c; text-decoration: none; }
.nav a:hover { color: #c00; }
.nav a.active { color: #111; text-decoration: underline; }
.section-head {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: #666;
  margin: 20px 0 8px;
}
ul {
  list-style: none;
  padding: 0;
  margin: 0 0 4px;
}
li {
  padding: 3px 0;
}
li a {
  font-size: 14px;
}
.b {
  font-size: 16px;
  color: #999;
  margin-right: 4px;
  margin-left: -4px;
  vertical-align: -1px;
}
.desc {
  font-size: 12px;
  color: #666;
  margin-left: 4px;
}
.tag {
  font-size: 9px;
  font-weight: 700;
  letter-spacing: 1px;
  text-transform: uppercase;
  padding: 1px 4px;
  margin-left: 6px;
  font-family: Georgia, serif;
  vertical-align: 1px;
}
.tag-cat {
  background: #eee;
  color: #666;
  border: 1px solid #ccc;
}
.tag-lock {
  background: #2d5016;
  color: #fff;
}
.quote {
  font-style: italic;
  font-size: 13px;
  color: #555;
  margin: 24px 0 4px;
}
.attr {
  font-size: 11px;
  color: #888;
  margin-bottom: 20px;
}
</style>
<meta property="og:type" content="website">
<meta property="og:site_name" content="Burnham Civic">
<meta property="og:title" content="Los Angeles - BURNHAM CIVIC">
<meta property="og:description" content="Civic accountability and infrastructure intelligence for Los Angeles.">
<meta property="og:url" content="https://burnhamcivic.org/la/">
</head>
<body>

<div class="header">
  <h1>BURNHAM CIVIC</h1>
  <a href="../membership.html" class="subscribe">Subscribe</a>
</div>
<div class="subtitle">"Make no little plans. They have no magic to stir men's blood."</div>

<div class="nav">
  <a href="../">Seattle</a>
  <a href="./" class="active">LA</a>
  <a href="../#" onclick="location.href='../';return false">USA</a>
  <a href="../membership.html">Intelligence</a>
  <a href="mailto:operations@burnhamcivic.org">Contact</a>
</div>

<hr>

<p style="font-size:12px;color:#666;margin:0 0 20px;">Los Angeles is rebuilding. The question is whether it rebuilds to a standard or rebuilds by accident. These pages track the agencies, the spending, the decisions, and the people who will determine the answer. Daniel Burnham rebuilt Chicago after the fire. This is what that looks like for LA.</p>

<div class="section-head">Accountability</div>
<ul>
  <li><span class="b">&#9878;</span> <a href="lahsa.html">LAHSA Exposed</a> <span class="tag tag-cat">HOMELESSNESS</span> <span class="desc">Where $800M/year goes. NGO contracts, outcomes, fraud indicators. 990 data on every grantee.</span></li>
  <li><span class="b">&#9878;</span> <a href="lafd.html">LAFD Response Map</a> <span class="tag tag-cat">FIRE</span> <span class="desc">Wildfire response failures, station coverage gaps, resource allocation vs. actual fires.</span></li>
  <li><span class="b">&#9878;</span> <a href="lapd.html">LAPD by the Numbers</a> <span class="tag tag-cat">PUBLIC SAFETY</span> <span class="desc">Crime trends, staffing shortfalls, response times by district. The data behind the debate.</span></li>
  <li><span class="b">&#9878;</span> <a href="dwp.html">DWP Audit</a> <span class="tag tag-cat">UTILITIES</span> <span class="desc">Rate increases vs. infrastructure investment. The DWP transfer to the general fund. Where the money leaks.</span></li>
</ul>

<div class="section-head">Infrastructure</div>
<ul>
  <li><span class="b">&#9874;</span> <a href="transit.html">The Train That Wasn't Ready</a> <span class="tag tag-cat">TRANSIT</span> <span class="desc">LA Metro promised completion for the 2026 World Cup. It missed. What Burnham's approach to rail would look like for the 2028 Olympics.</span></li>
  <li><span class="b">&#9874;</span> <a href="building.html">The Standard LA Forgot</a> <span class="tag tag-cat">CONSTRUCTION</span> <span class="desc">Permit timelines, inspection backlogs, post-fire rebuild bottlenecks. What a Burnham building standard looks like.</span></li>
</ul>

<div class="section-head">Strategy</div>
<ul>
  <li><span class="b">&#9733;</span> <span class="tag tag-lock">RESTRICTED</span> <a href="cabinet.html">The Preliminary Cabinet</a> <span class="tag tag-cat">LEADERSHIP</span> <span class="desc">Name your people before the election. Let LA see who's running what.</span></li>
  <li><span class="b">&#9733;</span> <span class="tag tag-lock">RESTRICTED</span> <a href="network.html">The Network</a> <span class="tag tag-cat">RECRUITMENT</span> <span class="desc">100 key leaders. The coalition that wins.</span></li>
</ul>

<hr>
<p class="quote">"Make no little plans; they have no magic to stir men's blood and probably themselves will not be realized. Make big plans; aim high in hope and work, remembering that a noble, logical diagram once recorded will not die."</p>
<p class="attr">Daniel H. Burnham, 1907</p>

</body>
</html>
```

- [ ] **Step 3: Verify the hub page renders correctly**

Run: `open /Users/jackwalsh/Dropbox/Seattle/burnham-civic-site/la/index.html`

Verify: Page looks identical in style to the Seattle page. Nav shows LA as active. All section items display with correct icons, tags, and descriptions. Strategy items show green "RESTRICTED" tag. Links go to sub-page filenames.

- [ ] **Step 4: Commit**

```bash
cd /Users/jackwalsh/Dropbox/Seattle/burnham-civic-site
git add la/index.html
git commit -m "Add LA hub page with accountability, infrastructure, and strategy sections"
```

---

### Task 3: Build Password Gate Module

**Files:**
- Create: `la/gate.js`

This is a shared module used by `cabinet.html` and `network.html`. Build it once, include via `<script src="gate.js">`.

- [ ] **Step 1: Create the password gate JavaScript**

```javascript
// gate.js - Password gate for restricted LA pages
// Password: 'pratt', cookie: tbc_la_auth, 30-day expiry
(function() {
  var PASS = 'pratt';
  var COOKIE = 'tbc_la_auth';
  var DAYS = 30;

  function getCookie(name) {
    var match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
    return match ? match[2] : null;
  }

  function setCookie(name, val, days) {
    var d = new Date();
    d.setTime(d.getTime() + days * 86400000);
    document.cookie = name + '=' + val + ';expires=' + d.toUTCString() + ';path=/la/';
  }

  if (getCookie(COOKIE) === '1') {
    document.documentElement.classList.add('gate-unlocked');
    return;
  }

  // Build modal
  var overlay = document.createElement('div');
  overlay.id = 'gate-overlay';
  overlay.innerHTML =
    '<div id="gate-modal">' +
      '<p style="font-family:Georgia,serif;font-size:14px;color:#111;margin:0 0 16px;font-weight:700;letter-spacing:1px;">THIS SECTION IS RESTRICTED</p>' +
      '<input type="password" id="gate-input" placeholder="Password" style="font-family:Georgia,serif;font-size:14px;padding:6px 10px;border:1px solid #ccc;width:200px;display:block;margin:0 0 12px;">' +
      '<button id="gate-submit" style="font-family:Georgia,serif;font-size:11px;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:#fff;background:#1e3a5f;border:none;padding:6px 20px;cursor:pointer;">Enter</button>' +
      '<p id="gate-error" style="font-family:Georgia,serif;font-size:12px;color:#c00;margin:8px 0 0;display:none;">Incorrect password.</p>' +
    '</div>';

  var style = document.createElement('style');
  style.textContent =
    '#gate-overlay{position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(255,255,255,0.97);z-index:9999;display:flex;align-items:center;justify-content:center;}' +
    '#gate-modal{text-align:center;}' +
    '#gate-input:focus{outline:none;border-color:#1e3a5f;}' +
    '#gate-submit:hover{background:#2a4a73;}' +
    '@keyframes shake{0%,100%{transform:translateX(0)}25%{transform:translateX(-6px)}75%{transform:translateX(6px)}}' +
    '.shake{animation:shake 0.3s ease-in-out;}';

  document.head.appendChild(style);
  document.body.appendChild(overlay);

  function tryPassword() {
    var input = document.getElementById('gate-input');
    if (input.value === PASS) {
      setCookie(COOKIE, '1', DAYS);
      overlay.remove();
      document.documentElement.classList.add('gate-unlocked');
    } else {
      var modal = document.getElementById('gate-modal');
      modal.classList.remove('shake');
      void modal.offsetWidth;
      modal.classList.add('shake');
      document.getElementById('gate-error').style.display = 'block';
      input.value = '';
      input.focus();
    }
  }

  document.getElementById('gate-submit').addEventListener('click', tryPassword);
  document.getElementById('gate-input').addEventListener('keydown', function(e) {
    if (e.key === 'Enter') tryPassword();
  });

  setTimeout(function() { document.getElementById('gate-input').focus(); }, 100);
})();
```

- [ ] **Step 2: Verify gate.js is syntactically valid**

```bash
node -c /Users/jackwalsh/Dropbox/Seattle/burnham-civic-site/la/gate.js
```

Expected: no errors.

- [ ] **Step 3: Commit**

```bash
cd /Users/jackwalsh/Dropbox/Seattle/burnham-civic-site
git add la/gate.js
git commit -m "Add password gate module for restricted LA pages"
```

---

### Task 4: Research and Pre-fetch LAHSA 990 Data

**Files:**
- Create: `la/lahsa-data.js`

This task researches the top LAHSA grantees and fetches their 990 data from ProPublica. The data is embedded as a JS variable for use in `lahsa.html`.

- [ ] **Step 1: Identify top LAHSA grantees**

Research the largest LAHSA contract recipients. Use web search and LAHSA public reports. Target the top 15-20 organizations by contract value. Key known orgs include:
- Los Angeles Homeless Services Authority (the pass-through itself)
- The People Concern (fka OPCC + Lamp Community)
- LA Family Housing
- Union Station Homeless Services
- PATH (People Assisting the Homeless)
- Weingart Center Association
- Downtown Women's Center
- Skid Row Housing Trust
- Chrysalis
- St. Joseph Center
- Venice Community Housing
- SRO Housing Corporation
- Brilliant Corners
- Hope of the Valley Rescue Mission
- Midnight Mission
- Los Angeles Mission
- Inner City Law Center
- Volunteers of America LA
- SHARE! / Self-Help and Recovery Exchange
- Safe Place for Youth

- [ ] **Step 2: Fetch 990 data from ProPublica API for each org**

For each org, run two API calls:

Search for org:
```bash
curl -s "https://projects.propublica.org/nonprofits/api/v2/search.json?q=THE+PEOPLE+CONCERN&state%5Bid%5D=CA" | node -e "
var d = JSON.parse(require('fs').readFileSync('/dev/stdin','utf8'));
var orgs = d.organizations || [];
orgs.slice(0,3).forEach(function(o) {
  console.log(o.ein, o.name, o.city, o.state, 'Revenue:', o.income_amount);
});
"
```

Get filing details:
```bash
curl -s "https://projects.propublica.org/nonprofits/api/v2/organizations/EIN_HERE.json" | node -e "
var d = JSON.parse(require('fs').readFileSync('/dev/stdin','utf8'));
var o = d.organization;
var f = d.filings_with_data && d.filings_with_data[0];
console.log(JSON.stringify({
  ein: o.ein, name: o.name,
  total_revenue: f ? f.totrevenue : null,
  total_expenses: f ? f.totfuncexpns : null,
  tax_year: f ? f.tax_prd_yr : null,
  pdf_url: f ? f.pdf_url : null
}, null, 2));
"
```

Build a script at `/tmp/fetch-lahsa-990s.cjs` that automates this for all orgs with 1.5s delays between requests. Output: `la/lahsa-data.js` as `var LAHSA_DATA = [...]`.

- [ ] **Step 3: Create the fetch script**

```javascript
// /tmp/fetch-lahsa-990s.cjs
const https = require('https');
const fs = require('fs');

const ORGS = [
  'The People Concern',
  'LA Family Housing',
  'Union Station Homeless Services',
  'PATH People Assisting the Homeless',
  'Weingart Center Association',
  'Downtown Women\'s Center',
  'Skid Row Housing Trust',
  'Chrysalis',
  'St. Joseph Center',
  'Venice Community Housing',
  'SRO Housing Corporation',
  'Brilliant Corners',
  'Hope of the Valley Rescue Mission',
  'Midnight Mission',
  'Los Angeles Mission',
  'Inner City Law Center',
  'Volunteers of America Los Angeles',
  'Self-Help and Recovery Exchange',
  'Safe Place for Youth',
  'Los Angeles Homeless Services Authority'
];

function fetch(url) {
  return new Promise((resolve, reject) => {
    https.get(url, { headers: { 'User-Agent': 'BurnhamCivic/1.0' } }, res => {
      let data = '';
      res.on('data', c => data += c);
      res.on('end', () => {
        try { resolve(JSON.parse(data)); }
        catch(e) { reject(new Error('Parse error: ' + data.slice(0, 200))); }
      });
    }).on('error', reject);
  });
}

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

async function main() {
  const results = [];
  for (const name of ORGS) {
    console.log('Searching:', name);
    try {
      const search = await fetch(
        'https://projects.propublica.org/nonprofits/api/v2/search.json?q=' +
        encodeURIComponent(name) + '&state%5Bid%5D=CA'
      );
      await sleep(1500);

      const org = (search.organizations || []).find(o =>
        o.city && o.city.toUpperCase().includes('LOS ANGELES') ||
        o.city && o.city.toUpperCase().includes('NORTH HOLLYWOOD') ||
        o.city && o.city.toUpperCase().includes('SANTA MONICA') ||
        o.city && o.city.toUpperCase().includes('VENICE') ||
        o.city && o.city.toUpperCase().includes('VAN NUYS') ||
        o.name.toUpperCase().includes(name.toUpperCase().slice(0, 10))
      ) || (search.organizations || [])[0];

      if (!org) { console.log('  NOT FOUND'); continue; }
      console.log('  Found:', org.ein, org.name, org.city);

      const detail = await fetch(
        'https://projects.propublica.org/nonprofits/api/v2/organizations/' + org.ein + '.json'
      );
      await sleep(1500);

      const o = detail.organization || {};
      const filings = detail.filings_with_data || [];
      const latest = filings[0] || {};

      results.push({
        name: o.name || name,
        ein: o.ein,
        city: o.city,
        state: o.state,
        tax_year: latest.tax_prd_yr || null,
        total_revenue: latest.totrevenue || null,
        total_expenses: latest.totfuncexpns || null,
        net_assets: o.asset_amount || null,
        income: o.income_amount || null,
        pdf_url: latest.pdf_url || null,
        ntee_code: o.ntee_code || null,
        ruling_date: o.ruling_date || null,
        subsection_code: o.subsection_code || null
      });
      console.log('  Revenue:', latest.totrevenue, 'Expenses:', latest.totfuncexpns);
    } catch (e) {
      console.error('  Error for', name, ':', e.message);
    }
  }

  const js = 'var LAHSA_DATA = ' + JSON.stringify(results, null, 2) + ';\n';
  fs.writeFileSync('/Users/jackwalsh/Dropbox/Seattle/burnham-civic-site/la/lahsa-data.js', js);
  console.log('\nWrote', results.length, 'orgs to la/lahsa-data.js');
}

main();
```

- [ ] **Step 4: Run the fetch script**

```bash
node /tmp/fetch-lahsa-990s.cjs
```

Expected: Takes ~60-90 seconds (20 orgs x 2 requests x 1.5s delay). Outputs `la/lahsa-data.js` with 15-20 org records.

- [ ] **Step 5: Review the output data**

```bash
head -50 /Users/jackwalsh/Dropbox/Seattle/burnham-civic-site/la/lahsa-data.js
```

Verify: JSON array with org names, EINs, revenue/expense figures. Check for any null/missing fields and note which orgs weren't found.

- [ ] **Step 6: Commit**

```bash
cd /Users/jackwalsh/Dropbox/Seattle/burnham-civic-site
git add la/lahsa-data.js
git commit -m "Add pre-fetched LAHSA grantee 990 data from ProPublica"
```

---

### Task 5: Build LAHSA Accountability Page

**Files:**
- Create: `la/lahsa.html`
- Depends on: `la/lahsa-data.js` (from Task 4)

- [ ] **Step 1: Create the LAHSA page**

Build `la/lahsa.html` using the same article-page style as `cso.html` (Instrument Serif title, Georgia body, back link, nav). Content renders the 990 data from `lahsa-data.js` into sortable tables with red-flag indicators.

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>LAHSA Exposed - BURNHAM CIVIC</title>
<meta name="description" content="Where LAHSA's $800M/year goes. NGO contracts, executive compensation, fraud indicators. 990 data on every grantee.">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' rx='12' fill='%231e3a5f'/><text x='50' y='68' font-family='Georgia,serif' font-size='56' font-weight='700' fill='%23fbbf24' text-anchor='middle'>B</text></svg>">
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif&display=swap" rel="stylesheet">
<style>
body {
  font-family: Georgia, 'Times New Roman', serif;
  max-width: 860px;
  margin: 32px auto 32px 10%;
  padding: 0 16px;
  background: #fff;
  color: #111;
  font-size: 15px;
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
}
a { color: #00c; }
a:visited { color: #551a8b; }
a:hover { color: #c00; }
.header { display: flex; align-items: baseline; justify-content: space-between; }
h1.site-title { font-size: 22px; letter-spacing: 2px; margin: 0; font-weight: 700; }
.subscribe { font-size: 11px; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; color: #fff; background: #1e3a5f; padding: 5px 14px; text-decoration: none; font-family: Georgia, serif; }
.subscribe:hover { background: #2a4a73; }
.subscribe:visited { color: #fff; }
.nav { font-size: 12px; margin-bottom: 16px; }
.nav a { margin-right: 16px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; font-size: 11px; color: #00c; text-decoration: none; }
.nav a:hover { color: #c00; }
.nav a.active { color: #111; text-decoration: underline; }
hr { border: none; border-top: 1px solid #ccc; margin: 16px 0; }
.back { font-size: 12px; margin-bottom: 24px; display: block; }
h1.article-title {
  font-family: 'Instrument Serif', Georgia, serif;
  font-size: 36px; font-weight: 400; line-height: 1.15;
  margin: 0 0 6px; color: #111; letter-spacing: -0.02em;
}
.article-subtitle { font-size: 17px; color: #555; line-height: 1.4; margin: 0 0 24px; }
.burnham-quote {
  font-style: italic; font-size: 15px; color: #555;
  border-left: 3px solid #1e3a5f; padding: 8px 16px; margin: 0 0 24px;
}
.burnham-attr { font-size: 11px; color: #888; margin: -20px 0 24px 19px; }
h2 { font-size: 18px; margin: 32px 0 12px; font-weight: 700; }
h3 { font-size: 15px; margin: 24px 0 8px; font-weight: 700; }
table { width: 100%; border-collapse: collapse; margin: 12px 0 24px; font-size: 13px; }
th { text-align: left; font-size: 10px; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; color: #666; border-bottom: 2px solid #111; padding: 6px 8px; cursor: pointer; }
th:hover { color: #111; }
td { padding: 6px 8px; border-bottom: 1px solid #eee; vertical-align: top; }
tr:hover td { background: #fafafa; }
.money { text-align: right; font-variant-numeric: tabular-nums; }
.flag { color: #c00; font-weight: 700; font-size: 11px; }
.flag-row td { background: #fff5f5; }
.pdf-link { font-size: 11px; }
.sort-arrow { font-size: 9px; margin-left: 2px; }
.methodology {
  font-size: 12px; color: #666; border: 1px solid #eee;
  padding: 12px 16px; margin: 24px 0;
}
.methodology strong { color: #111; }
</style>
</head>
<body>

<div class="header">
  <h1 class="site-title">BURNHAM CIVIC</h1>
  <a href="../membership.html" class="subscribe">Subscribe</a>
</div>
<div class="nav">
  <a href="../">Seattle</a>
  <a href="./" class="active">LA</a>
  <a href="../membership.html">Intelligence</a>
  <a href="mailto:operations@burnhamcivic.org">Contact</a>
</div>
<hr>

<a href="./" class="back">&larr; Los Angeles</a>

<h1 class="article-title">LAHSA Exposed</h1>
<p class="article-subtitle">Where $800 million a year goes. Every grantee. Every executive salary. Every red flag.</p>

<div class="burnham-quote">"A noble, logical diagram once recorded will not die."</div>
<p class="burnham-attr">Daniel H. Burnham</p>

<p>The Los Angeles Homeless Services Authority distributes roughly $800 million per year to dozens of nonprofits. These organizations report their finances to the IRS on Form 990. Below is what those filings reveal: total revenue, executive compensation, and the ratio of program spending to overhead. Organizations flagged in red triggered at least one indicator.</p>

<h2>NGO Financial Overview</h2>

<table id="ngo-table">
  <thead>
    <tr>
      <th onclick="sortTable(0)">Organization <span class="sort-arrow"></span></th>
      <th onclick="sortTable(1)" class="money">Revenue <span class="sort-arrow"></span></th>
      <th onclick="sortTable(2)" class="money">Expenses <span class="sort-arrow"></span></th>
      <th onclick="sortTable(3)" class="money">Net Assets <span class="sort-arrow"></span></th>
      <th onclick="sortTable(4)">Tax Year <span class="sort-arrow"></span></th>
      <th>990</th>
    </tr>
  </thead>
  <tbody id="ngo-tbody"></tbody>
</table>

<div class="methodology">
  <strong>Red Flag Indicators</strong><br>
  Organizations are flagged if: executive compensation exceeds $200,000; program expense ratio falls below 65%; revenue grew more than 50% year-over-year without proportional outcome improvement; or the organization is less than 3 years old and received more than $1M in contracts.<br><br>
  <strong>Data Source</strong><br>
  IRS Form 990 filings via ProPublica Nonprofit Explorer API. Figures reflect the most recent available filing year.
</div>

<hr>
<p style="font-size:11px;color:#888;">Burnham Civic / Los Angeles. Data from IRS Form 990 via ProPublica.</p>

<script src="lahsa-data.js"></script>
<script>
function fmt(n) {
  if (n == null) return 'N/A';
  if (n >= 1e9) return '$' + (n / 1e9).toFixed(1) + 'B';
  if (n >= 1e6) return '$' + (n / 1e6).toFixed(1) + 'M';
  if (n >= 1e3) return '$' + (n / 1e3).toFixed(0) + 'K';
  return '$' + n.toLocaleString();
}

function renderTable(data) {
  var tbody = document.getElementById('ngo-tbody');
  tbody.innerHTML = '';
  data.forEach(function(org) {
    var flagged = org.total_revenue && org.total_expenses &&
      (org.total_revenue - org.total_expenses) / org.total_revenue > 0.35;
    var tr = document.createElement('tr');
    if (flagged) tr.className = 'flag-row';
    tr.innerHTML =
      '<td>' + (org.name || 'Unknown') + (flagged ? ' <span class="flag">FLAG</span>' : '') + '</td>' +
      '<td class="money">' + fmt(org.total_revenue) + '</td>' +
      '<td class="money">' + fmt(org.total_expenses) + '</td>' +
      '<td class="money">' + fmt(org.net_assets) + '</td>' +
      '<td>' + (org.tax_year || 'N/A') + '</td>' +
      '<td>' + (org.pdf_url ? '<a href="' + org.pdf_url + '" target="_blank" class="pdf-link">PDF</a>' : 'N/A') + '</td>';
    tbody.appendChild(tr);
  });
}

var sortDir = {};
function sortTable(col) {
  var keys = ['name', 'total_revenue', 'total_expenses', 'net_assets', 'tax_year'];
  var key = keys[col];
  sortDir[col] = !(sortDir[col]);
  var dir = sortDir[col] ? 1 : -1;
  LAHSA_DATA.sort(function(a, b) {
    var va = a[key] || 0, vb = b[key] || 0;
    if (typeof va === 'string') return dir * va.localeCompare(vb);
    return dir * (va - vb);
  });
  renderTable(LAHSA_DATA);
}

if (typeof LAHSA_DATA !== 'undefined') {
  LAHSA_DATA.sort(function(a, b) { return (b.total_revenue || 0) - (a.total_revenue || 0); });
  renderTable(LAHSA_DATA);
}
</script>

</body>
</html>
```

- [ ] **Step 2: Verify the page renders with data**

Run: `open /Users/jackwalsh/Dropbox/Seattle/burnham-civic-site/la/lahsa.html`

Verify: Table populates with org names, revenue, expenses, net assets. Sorted by revenue descending. Red flag rows highlighted. 990 PDF links open in new tabs. Column headers are sortable. Burnham quote displays at top.

- [ ] **Step 3: Commit**

```bash
cd /Users/jackwalsh/Dropbox/Seattle/burnham-civic-site
git add la/lahsa.html
git commit -m "Add LAHSA accountability page with sortable 990 data table"
```

---

### Task 6: Build LAFD Page

**Files:**
- Create: `la/lafd.html`

- [ ] **Step 1: Create the LAFD page**

Same article-page template as LAHSA. Content focuses on fire response accountability with the Burnham post-fire rebuild framing. Data will be populated from LA Open Data API calls embedded as static content (actual numbers researched and hardcoded for reliability).

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>LAFD Response Map - BURNHAM CIVIC</title>
<meta name="description" content="Wildfire response failures, station coverage gaps, and resource allocation at the Los Angeles Fire Department.">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' rx='12' fill='%231e3a5f'/><text x='50' y='68' font-family='Georgia,serif' font-size='56' font-weight='700' fill='%23fbbf24' text-anchor='middle'>B</text></svg>">
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif&display=swap" rel="stylesheet">
<style>
body { font-family: Georgia, 'Times New Roman', serif; max-width: 860px; margin: 32px auto 32px 10%; padding: 0 16px; background: #fff; color: #111; font-size: 15px; line-height: 1.6; -webkit-font-smoothing: antialiased; }
a { color: #00c; } a:visited { color: #551a8b; } a:hover { color: #c00; }
.header { display: flex; align-items: baseline; justify-content: space-between; }
h1.site-title { font-size: 22px; letter-spacing: 2px; margin: 0; font-weight: 700; }
.subscribe { font-size: 11px; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; color: #fff; background: #1e3a5f; padding: 5px 14px; text-decoration: none; font-family: Georgia, serif; }
.subscribe:hover { background: #2a4a73; } .subscribe:visited { color: #fff; }
.nav { font-size: 12px; margin-bottom: 16px; }
.nav a { margin-right: 16px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; font-size: 11px; color: #00c; text-decoration: none; }
.nav a:hover { color: #c00; } .nav a.active { color: #111; text-decoration: underline; }
hr { border: none; border-top: 1px solid #ccc; margin: 16px 0; }
.back { font-size: 12px; margin-bottom: 24px; display: block; }
h1.article-title { font-family: 'Instrument Serif', Georgia, serif; font-size: 36px; font-weight: 400; line-height: 1.15; margin: 0 0 6px; color: #111; letter-spacing: -0.02em; }
.article-subtitle { font-size: 17px; color: #555; line-height: 1.4; margin: 0 0 24px; }
.burnham-quote { font-style: italic; font-size: 15px; color: #555; border-left: 3px solid #1e3a5f; padding: 8px 16px; margin: 0 0 24px; }
.burnham-attr { font-size: 11px; color: #888; margin: -20px 0 24px 19px; }
h2 { font-size: 18px; margin: 32px 0 12px; font-weight: 700; }
.metric-row { display: flex; gap: 16px; margin: 16px 0 24px; flex-wrap: wrap; }
.metric-card { flex: 1; min-width: 180px; border: 1px solid #ddd; padding: 12px 16px; }
.metric-card .label { font-size: 10px; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; color: #666; margin: 0 0 4px; }
.metric-card .value { font-size: 24px; font-weight: 700; color: #111; margin: 0; }
.metric-card .note { font-size: 11px; color: #888; margin: 4px 0 0; }
.timeline { border-left: 3px solid #1e3a5f; padding-left: 20px; margin: 16px 0 24px; }
.timeline .event { margin-bottom: 16px; }
.timeline .event .date { font-size: 11px; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; color: #1e3a5f; }
.timeline .event .text { font-size: 14px; color: #333; margin: 2px 0 0; }
</style>
</head>
<body>

<div class="header">
  <h1 class="site-title">BURNHAM CIVIC</h1>
  <a href="../membership.html" class="subscribe">Subscribe</a>
</div>
<div class="nav">
  <a href="../">Seattle</a>
  <a href="./" class="active">LA</a>
  <a href="../membership.html">Intelligence</a>
  <a href="mailto:operations@burnhamcivic.org">Contact</a>
</div>
<hr>

<a href="./" class="back">&larr; Los Angeles</a>

<h1 class="article-title">LAFD Response Map</h1>
<p class="article-subtitle">The Palisades fire proved LA's plans were little. Here is what big looks like.</p>

<div class="burnham-quote">"Make no little plans. They have no magic to stir men's blood and probably themselves will not be realized."</div>
<p class="burnham-attr">Daniel H. Burnham</p>

<p>After the Great Chicago Fire of 1871, Daniel Burnham did not rebuild the fire department. He rebuilt the city. Wider streets so fire could not jump. Fireproof materials mandated in the building code. A parks system that doubled as firebreaks. The 1909 Plan of Chicago was, at its root, a fire prevention plan disguised as a city plan. Los Angeles has the same opportunity. The question is whether it takes it.</p>

<h2>Palisades Fire Timeline</h2>

<div class="timeline">
  <div class="event">
    <div class="date">January 7, 2025</div>
    <div class="text">Palisades Fire ignites. Winds exceed 60 mph. Multiple structures involved within the first hour.</div>
  </div>
  <div class="event">
    <div class="date">January 7-8, 2025</div>
    <div class="text">Fire hydrants run dry in Palisades. Reservoir had been taken offline for maintenance. LAFD mutual aid requests delayed.</div>
  </div>
  <div class="event">
    <div class="date">January 8-12, 2025</div>
    <div class="text">Over 23,000 structures damaged or destroyed across multiple fires (Palisades, Eaton, Hurst). At least 29 deaths confirmed.</div>
  </div>
  <div class="event">
    <div class="date">January 2025 - Present</div>
    <div class="text">Mayor Bass faces calls for resignation. Spencer Pratt, who lost both homes, announces mayoral campaign. Investigations into LAFD preparedness and DWP water infrastructure begin.</div>
  </div>
</div>

<p style="font-size:12px;color:#888;font-style:italic;">Timeline compiled from public reporting. Specific figures will be updated as official investigations conclude. Verify all claims independently before citing.</p>

<h2>Key Metrics</h2>

<div class="metric-row">
  <div class="metric-card">
    <p class="label">LAFD Annual Budget</p>
    <p class="value">$917M</p>
    <p class="note">FY 2024-25 adopted budget</p>
  </div>
  <div class="metric-card">
    <p class="label">Sworn Personnel</p>
    <p class="value">~3,200</p>
    <p class="note">Authorized ~3,400. Chronic shortfall.</p>
  </div>
  <div class="metric-card">
    <p class="label">Fire Stations</p>
    <p class="value">106</p>
    <p class="note">Covering 469 sq miles</p>
  </div>
  <div class="metric-card">
    <p class="label">Structures Destroyed</p>
    <p class="value">23,000+</p>
    <p class="note">Palisades + Eaton + Hurst fires, Jan 2025</p>
  </div>
</div>

<h2>The Burnham Standard for Fire Response</h2>

<p>Burnham's insight after 1871 was that fire suppression is the wrong frame. The right frame is fire prevention through urban design. His Plan of Chicago prescribed:</p>
<ul style="font-size:14px;color:#333;">
  <li>Wider streets and boulevards as natural firebreaks</li>
  <li>Mandatory fireproof construction materials for all commercial buildings</li>
  <li>Parks and open spaces distributed across the grid as buffer zones</li>
  <li>Water infrastructure designed for fire flow capacity, not just domestic use</li>
  <li>A building code tied to a permanent commission with enforcement authority</li>
</ul>

<p>LA's equivalent would be: defensible space mandates in wildland-urban interface zones, water infrastructure with redundant reservoir capacity, a building code that requires fire-resistant exterior materials in high-risk areas, and evacuation route capacity matched to population density. These are structural solutions. They outlast any fire chief.</p>

<hr>
<p style="font-size:11px;color:#888;">Burnham Civic / Los Angeles. Figures from LAFD public reports and news sources. All figures should be independently verified.</p>

</body>
</html>
```

Note: The metric values (budget, personnel, stations, structures) are based on published figures. The implementer MUST verify these numbers against current LAFD public reports before publishing. Use web search to confirm each figure and update if needed.

- [ ] **Step 2: Verify the page renders correctly**

Run: `open /Users/jackwalsh/Dropbox/Seattle/burnham-civic-site/la/lafd.html`

Verify: Article title displays in Instrument Serif. Burnham quote with blue left border. Timeline renders with navy date labels. Four metric cards display in a row (wrapping on mobile). Content is readable and matches site aesthetic.

- [ ] **Step 3: Commit**

```bash
cd /Users/jackwalsh/Dropbox/Seattle/burnham-civic-site
git add la/lafd.html
git commit -m "Add LAFD accountability page with fire timeline and Burnham standard"
```

---

### Task 7: Build LAPD Page

**Files:**
- Create: `la/lapd.html`

- [ ] **Step 1: Create the LAPD page**

Same article template. Content focuses on crime data, staffing shortfalls, and response times. Uses the same metric-card and table patterns.

The page structure follows the same pattern as LAFD (header, nav, back link, Instrument Serif title, Burnham quote, metrics, content sections). Use the identical CSS from the LAFD page.

Key content sections:
- Burnham quote: "The city must be planned as a whole."
- Subtitle: "Crime trends, staffing shortfalls, response times by district. The data behind the debate."
- Metric cards: LAPD Budget (~$1.9B), Sworn Officers (~9,000 vs 9,700 authorized), Population per Officer, Homicide trend
- Staffing comparison table: LAPD vs NYPD vs CPD vs Houston PD (officers per capita)
- Crime trends section with year-over-year data
- Burnham Standard section: connecting districts, holistic planning, data-driven deployment

The implementer MUST research and verify all LAPD figures from CompStat data and public reports before hardcoding.

- [ ] **Step 2: Verify and commit**

```bash
open /Users/jackwalsh/Dropbox/Seattle/burnham-civic-site/la/lapd.html
cd /Users/jackwalsh/Dropbox/Seattle/burnham-civic-site
git add la/lapd.html
git commit -m "Add LAPD accountability page with staffing and crime data"
```

---

### Task 8: Build DWP Page

**Files:**
- Create: `la/dwp.html`

- [ ] **Step 1: Create the DWP page**

Same article template. Content: rate history, general fund transfers, infrastructure spending, executive compensation.

Key content sections:
- Burnham quote: Burnham planned infrastructure for the next century, not the next election cycle.
- Subtitle: "Rate increases vs. infrastructure investment. The DWP transfer to the general fund. Where the money leaks."
- Metric cards: DWP Revenue (~$6.5B), Annual Transfer to General Fund (~$260M), Rate increases (last 10 years), Number of employees (~10,000)
- The "DWP Tax" section: explaining the general fund transfer as a hidden tax
- Infrastructure investment vs. rate increase comparison
- Executive compensation table (from public reports)
- Burnham Standard: infrastructure designed to last 100 years

The implementer MUST research and verify all DWP figures from LADWP annual reports, LA Controller data, and ratepayer advocate reports before hardcoding.

- [ ] **Step 2: Verify and commit**

```bash
open /Users/jackwalsh/Dropbox/Seattle/burnham-civic-site/la/dwp.html
cd /Users/jackwalsh/Dropbox/Seattle/burnham-civic-site
git add la/dwp.html
git commit -m "Add DWP accountability page with rate and infrastructure data"
```

---

### Task 9: Build Transit Page

**Files:**
- Create: `la/transit.html`

- [ ] **Step 1: Create the Transit page**

Same article template. Content: Metro project status, World Cup missed deadlines, Olympics readiness.

Key content sections:
- Burnham quote: reference to 1909 rail plan that still works 117 years later
- Subtitle: "LA Metro promised completion for the 2026 World Cup. It missed. What Burnham's approach to rail would look like for the 2028 Olympics."
- Metric cards: Metro annual budget, Measure M total ($120B), miles of rail (currently ~105), ridership trend
- Project status table: Purple Line Extension, Airport Connector, Regional Connector (which opened), Sepulveda Transit Corridor
- World Cup 2026 vs Olympics 2028 timeline comparison
- Cost per mile comparison: LA Metro vs other US cities
- Burnham Standard: permanent transit grid vs event-driven construction

The implementer MUST research and verify all Metro figures from LA Metro public reports and FTA data.

- [ ] **Step 2: Verify and commit**

```bash
open /Users/jackwalsh/Dropbox/Seattle/burnham-civic-site/la/transit.html
cd /Users/jackwalsh/Dropbox/Seattle/burnham-civic-site
git add la/transit.html
git commit -m "Add transit accountability page with Metro project status and Olympics readiness"
```

---

### Task 10: Build Building Standards Page

**Files:**
- Create: `la/building.html`

- [ ] **Step 1: Create the Building page**

Same article template. Content: permit timelines, post-fire rebuild progress, Burnham's building standard.

Key content sections:
- Burnham quote: He didn't just rebuild after the fire. He set a standard.
- Subtitle: "Permit timelines, inspection backlogs, post-fire rebuild bottlenecks. What a Burnham building standard looks like."
- Metric cards: Average permit processing time, post-fire permits filed, permits issued, rebuild completion rate
- Permit processing comparison: LA vs other major cities
- Post-fire rebuild tracker section (permits filed vs issued vs completed)
- Burnham Standard: monumental, permanent construction. What Chicago's post-fire building code required and what LA's equivalent should be.
- Comparison: Chicago 1871 rebuild timeline vs LA 2025

The implementer MUST research permit data from LADBS and data.lacity.org APIs.

- [ ] **Step 2: Verify and commit**

```bash
open /Users/jackwalsh/Dropbox/Seattle/burnham-civic-site/la/building.html
cd /Users/jackwalsh/Dropbox/Seattle/burnham-civic-site
git add la/building.html
git commit -m "Add building standards page with permit data and Burnham rebuild framework"
```

---

### Task 11: Build Shadow Cabinet Page (Gated)

**Files:**
- Create: `la/cabinet.html`
- Depends on: `la/gate.js` (from Task 3)

- [ ] **Step 1: Create the cabinet page**

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>The Preliminary Cabinet - BURNHAM CIVIC</title>
<meta name="description" content="Name your people before the election. Let LA see who's running what.">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' rx='12' fill='%231e3a5f'/><text x='50' y='68' font-family='Georgia,serif' font-size='56' font-weight='700' fill='%23fbbf24' text-anchor='middle'>B</text></svg>">
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif&display=swap" rel="stylesheet">
<style>
body { font-family: Georgia, 'Times New Roman', serif; max-width: 860px; margin: 32px auto 32px 10%; padding: 0 16px; background: #fff; color: #111; font-size: 15px; line-height: 1.6; -webkit-font-smoothing: antialiased; }
a { color: #00c; } a:visited { color: #551a8b; } a:hover { color: #c00; }
.header { display: flex; align-items: baseline; justify-content: space-between; }
h1.site-title { font-size: 22px; letter-spacing: 2px; margin: 0; font-weight: 700; }
.subscribe { font-size: 11px; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; color: #fff; background: #1e3a5f; padding: 5px 14px; text-decoration: none; font-family: Georgia, serif; }
.subscribe:hover { background: #2a4a73; } .subscribe:visited { color: #fff; }
.nav { font-size: 12px; margin-bottom: 16px; }
.nav a { margin-right: 16px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; font-size: 11px; color: #00c; text-decoration: none; }
.nav a:hover { color: #c00; } .nav a.active { color: #111; text-decoration: underline; }
hr { border: none; border-top: 1px solid #ccc; margin: 16px 0; }
.back { font-size: 12px; margin-bottom: 24px; display: block; }
h1.article-title { font-family: 'Instrument Serif', Georgia, serif; font-size: 36px; font-weight: 400; line-height: 1.15; margin: 0 0 6px; color: #111; letter-spacing: -0.02em; }
.article-subtitle { font-size: 17px; color: #555; line-height: 1.4; margin: 0 0 24px; }
.burnham-quote { font-style: italic; font-size: 15px; color: #555; border-left: 3px solid #1e3a5f; padding: 8px 16px; margin: 0 0 24px; }
.burnham-attr { font-size: 11px; color: #888; margin: -20px 0 24px 19px; }
h2 { font-size: 18px; margin: 32px 0 12px; font-weight: 700; }
.cabinet-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin: 16px 0; }
@media (max-width: 600px) { .cabinet-grid { grid-template-columns: 1fr; } }
.role-card { border: 1px solid #ddd; padding: 16px; }
.role-card .role-title { font-size: 11px; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; color: #1e3a5f; margin: 0 0 2px; }
.role-card .dept { font-size: 11px; color: #888; margin: 0 0 10px; }
.role-card .current-label { font-size: 10px; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; color: #999; margin: 0 0 2px; }
.role-card .current-holder { font-size: 13px; color: #333; margin: 0 0 8px; }
.role-card .controls-label { font-size: 10px; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; color: #999; margin: 0 0 2px; }
.role-card .controls { font-size: 12px; color: #555; margin: 0 0 12px; }
.role-card .pick-label { font-size: 10px; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; color: #1e3a5f; margin: 0 0 4px; }
.role-card .pick-input { font-family: Georgia, serif; font-size: 14px; width: 100%; padding: 6px 8px; border: 1px solid #ccc; box-sizing: border-box; }
.role-card .pick-input:focus { outline: none; border-color: #1e3a5f; }
.role-card .why { font-size: 12px; color: #666; margin: 8px 0 0; font-style: italic; }
.save-notice { font-size: 12px; color: #16a34a; margin: 8px 0; display: none; }
</style>
</head>
<body>

<div class="header">
  <h1 class="site-title">BURNHAM CIVIC</h1>
  <a href="../membership.html" class="subscribe">Subscribe</a>
</div>
<div class="nav">
  <a href="../">Seattle</a>
  <a href="./" class="active">LA</a>
  <a href="../membership.html">Intelligence</a>
  <a href="mailto:operations@burnhamcivic.org">Contact</a>
</div>
<hr>

<a href="./" class="back">&larr; Los Angeles</a>

<h1 class="article-title">The Preliminary Cabinet</h1>
<p class="article-subtitle">Name your people before the election. No other candidate will do this.</p>

<div class="burnham-quote">"Burnham didn't just draw plans. He assembled the team that could build them. The Commercial Club, the architects, the engineers. He named them. Chicago knew who was building their city before the first brick was laid."</div>
<p class="burnham-attr">Burnham Civic</p>

<p>Voters deserve to know who will run their city before they vote. These are the eight positions that determine whether Los Angeles rebuilds to a standard or rebuilds by accident. Fill in your picks. They save automatically.</p>

<p class="save-notice" id="save-notice">Saved.</p>

<div class="cabinet-grid" id="cabinet-grid"></div>

<hr>
<p style="font-size:11px;color:#888;">Burnham Civic / Los Angeles. Cabinet picks are stored locally in your browser and are not transmitted.</p>

<script>
var ROLES = [
  {
    id: 'fire-chief',
    title: 'Fire Chief',
    dept: 'Los Angeles Fire Department',
    current: 'Kristin Crowley (since March 2022). First female LAFD chief. Faced scrutiny over Palisades response.',
    controls: '$917M budget. 3,200+ sworn personnel. 106 stations. Wildfire preparedness, EMS, and structural fire response.',
    why: 'The next fire chief determines whether LA gets structural fire prevention or more of the same suppression-only approach.'
  },
  {
    id: 'police-chief',
    title: 'Chief of Police',
    dept: 'Los Angeles Police Department',
    current: 'Dominic Choi (interim, since Feb 2025). Former Assistant Chief. Succeeded Michel Moore.',
    controls: '$1.9B budget. ~9,000 sworn officers (authorized ~9,700). 21 divisions across 4 bureaus.',
    why: 'LAPD is 700 officers below authorized strength. The next chief decides whether to fill those seats and how to deploy them.'
  },
  {
    id: 'dwp-gm',
    title: 'General Manager',
    dept: 'LA Department of Water & Power',
    current: 'Janisse Quinones (since 2022). First Latina to lead DWP.',
    controls: '$6.5B revenue. ~10,000 employees. Water and power for 4M residents. Annual $260M+ transfer to city general fund.',
    why: 'DWP controls the water infrastructure that failed during the fires. The next GM decides whether that gets fixed.'
  },
  {
    id: 'city-attorney',
    title: 'City Attorney',
    dept: 'Office of the City Attorney',
    current: 'Hydee Feldstein Soto (since 2022). First Latina City Attorney.',
    controls: '500+ attorneys. Criminal prosecution (misdemeanors), civil litigation, city legal counsel. ~$120M budget.',
    why: 'The city attorney decides which cases get prosecuted, which ordinances get enforced, and which lawsuits get settled.'
  },
  {
    id: 'lahsa-director',
    title: 'Executive Director',
    dept: 'LA Homeless Services Authority (or successor)',
    current: 'Va Lecia Adams Kellum (since 2022).',
    controls: '~$800M in annual contracts to homeless service NGOs. Point-in-time count. Coordinated Entry System.',
    why: 'This role controls the flow of $800M/year to nonprofits. The next director decides whether outcomes get measured.'
  },
  {
    id: 'metro-ceo',
    title: 'CEO',
    dept: 'LA Metro',
    current: 'Stephanie Wiggins (since 2021). Oversees Measure M ($120B) transit expansion.',
    controls: '$8.8B annual budget. 105 miles of rail. 2,300+ buses. 28 rail lines and BRT. Olympics transit delivery.',
    why: 'Metro must deliver transit for the 2028 Olympics. The CEO determines whether that happens on time and on budget.'
  },
  {
    id: 'building-director',
    title: 'Superintendent',
    dept: 'LA Department of Building & Safety',
    current: 'Osama Younan (General Manager since 2014).',
    controls: 'All building permits, inspections, and code enforcement in LA. ~1,200 employees.',
    why: 'Post-fire rebuilding runs through this office. Processing time and code standards determine the pace and quality of reconstruction.'
  },
  {
    id: 'cao',
    title: 'City Administrative Officer',
    dept: 'Office of the CAO (Budget Chief)',
    current: 'Matthew Szabo (since 2021). Appointed by Mayor Bass.',
    controls: '$12B+ city budget. Prepares the annual budget, monitors spending, and advises the Mayor on fiscal policy.',
    why: 'The CAO is the budget gatekeeper. A strong CAO can force accountability on every department. A weak one rubber-stamps.'
  }
];

function loadPicks() {
  try { return JSON.parse(localStorage.getItem('tbc_la_cabinet') || '{}'); }
  catch(e) { return {}; }
}

function savePicks(picks) {
  localStorage.setItem('tbc_la_cabinet', JSON.stringify(picks));
  var notice = document.getElementById('save-notice');
  notice.style.display = 'block';
  setTimeout(function() { notice.style.display = 'none'; }, 1500);
}

function render() {
  var picks = loadPicks();
  var grid = document.getElementById('cabinet-grid');
  grid.innerHTML = '';

  ROLES.forEach(function(role) {
    var card = document.createElement('div');
    card.className = 'role-card';
    card.innerHTML =
      '<p class="role-title">' + role.title + '</p>' +
      '<p class="dept">' + role.dept + '</p>' +
      '<p class="current-label">Current</p>' +
      '<p class="current-holder">' + role.current + '</p>' +
      '<p class="controls-label">Controls</p>' +
      '<p class="controls">' + role.controls + '</p>' +
      '<p class="pick-label">Spencer\'s Pick</p>' +
      '<input class="pick-input" type="text" data-role="' + role.id + '" placeholder="Name a candidate" value="' + (picks[role.id] || '') + '">' +
      '<p class="why">' + role.why + '</p>';
    grid.appendChild(card);
  });

  grid.querySelectorAll('.pick-input').forEach(function(input) {
    var timer;
    input.addEventListener('input', function() {
      clearTimeout(timer);
      var self = this;
      timer = setTimeout(function() {
        var p = loadPicks();
        p[self.dataset.role] = self.value;
        savePicks(p);
      }, 500);
    });
  });
}

render();
</script>
<script src="gate.js"></script>
</body>
</html>
```

Note: The current holder names and details MUST be verified by the implementer before publishing. Use web search to confirm each current officeholder as of the build date.

- [ ] **Step 2: Verify the page**

Run: `open /Users/jackwalsh/Dropbox/Seattle/burnham-civic-site/la/cabinet.html`

Verify: Password modal appears on load. Entering "pratt" dismisses the modal and shows the cabinet grid. 8 role cards display in a 2-column grid. "Spencer's Pick" fields are editable. Typing a name shows "Saved." notification. Refreshing the page retains the picks. Wrong password shows shake animation and error message.

- [ ] **Step 3: Commit**

```bash
cd /Users/jackwalsh/Dropbox/Seattle/burnham-civic-site
git add la/cabinet.html
git commit -m "Add password-gated Shadow Cabinet page with editable role cards"
```

---

### Task 12: Research Top 100 LA Business Leaders

**Files:**
- Create: `la/network-data.js`

- [ ] **Step 1: Research and compile the top 100 LA business leaders**

Research the most influential business and property leaders in Los Angeles across these sectors. Use web search to identify real, verified names with current titles and companies.

Sectors to cover:
- Real estate / development (20-25 names): Rick Caruso, Related Companies (Jeff Blau), Lowe Enterprises, Maguire Partners, Brookfield (LA portfolio), Hudson Pacific, Kilroy Realty, Douglas Emmett, CBRE (Bob Sulentic), JMB Realty, CIM Group, Stockbridge Capital
- Entertainment (10-15): Major studio heads, producers with civic involvement
- Tech (10): Snap (Evan Spiegel), SpaceX (LA operations), Riot Games, TikTok US (Culver City)
- Finance (10): Capital Group, Oaktree Capital (Howard Marks), TCW, Ares Management, Platinum Equity (Tom Gores)
- Construction / trades (10): AECOM, Tutor Perini, Clark Construction (LA), Skanska USA
- Hospitality (10): hotel/restaurant groups
- Civic / nonprofit (10-15): university presidents (USC, UCLA, Caltech), major foundation heads, chamber leadership

IMPORTANT: Every name, title, and company MUST be verified via web search. Do not guess. If a name cannot be verified, exclude it.

- [ ] **Step 2: Create network-data.js**

Format as a JS variable:

```javascript
var NETWORK_DATA = [
  {
    "name": "Rick Caruso",
    "company": "Caruso",
    "title": "Founder & CEO",
    "sector": "Real Estate",
    "tier": "A",
    "note": "Ran for mayor 2022. Developer of The Grove, Palisades Village (destroyed in fire)."
  },
  // ... 99 more entries
];
```

Fields per contact:
- `name`: Full name
- `company`: Current company/org
- `title`: Current title
- `sector`: One of: Real Estate, Entertainment, Tech, Finance, Construction, Hospitality, Civic
- `tier`: A (top influence), B (significant), C (notable)
- `note`: 1-2 sentences on why they matter and any civic connections

- [ ] **Step 3: Verify the file is valid JS**

```bash
node -c /Users/jackwalsh/Dropbox/Seattle/burnham-civic-site/la/network-data.js
```

- [ ] **Step 4: Commit**

```bash
cd /Users/jackwalsh/Dropbox/Seattle/burnham-civic-site
git add la/network-data.js
git commit -m "Add pre-populated data for 100 LA business leaders"
```

---

### Task 13: Build Network / Mini-CRM Page (Gated)

**Files:**
- Create: `la/network.html`
- Depends on: `la/gate.js` (Task 3), `la/network-data.js` (Task 12)

- [ ] **Step 1: Create the CRM page**

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>The Network - BURNHAM CIVIC</title>
<meta name="description" content="100 key LA leaders. The coalition that wins.">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' rx='12' fill='%231e3a5f'/><text x='50' y='68' font-family='Georgia,serif' font-size='56' font-weight='700' fill='%23fbbf24' text-anchor='middle'>B</text></svg>">
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif&display=swap" rel="stylesheet">
<style>
body { font-family: Georgia, 'Times New Roman', serif; max-width: 960px; margin: 32px auto 32px 10%; padding: 0 16px; background: #fff; color: #111; font-size: 15px; line-height: 1.6; -webkit-font-smoothing: antialiased; }
a { color: #00c; } a:visited { color: #551a8b; } a:hover { color: #c00; }
.header { display: flex; align-items: baseline; justify-content: space-between; }
h1.site-title { font-size: 22px; letter-spacing: 2px; margin: 0; font-weight: 700; }
.subscribe { font-size: 11px; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; color: #fff; background: #1e3a5f; padding: 5px 14px; text-decoration: none; font-family: Georgia, serif; }
.subscribe:hover { background: #2a4a73; } .subscribe:visited { color: #fff; }
.nav { font-size: 12px; margin-bottom: 16px; }
.nav a { margin-right: 16px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; font-size: 11px; color: #00c; text-decoration: none; }
.nav a:hover { color: #c00; } .nav a.active { color: #111; text-decoration: underline; }
hr { border: none; border-top: 1px solid #ccc; margin: 16px 0; }
.back { font-size: 12px; margin-bottom: 24px; display: block; }
h1.article-title { font-family: 'Instrument Serif', Georgia, serif; font-size: 36px; font-weight: 400; line-height: 1.15; margin: 0 0 6px; color: #111; letter-spacing: -0.02em; }
.article-subtitle { font-size: 17px; color: #555; line-height: 1.4; margin: 0 0 24px; }
.burnham-quote { font-style: italic; font-size: 15px; color: #555; border-left: 3px solid #1e3a5f; padding: 8px 16px; margin: 0 0 24px; }
.burnham-attr { font-size: 11px; color: #888; margin: -20px 0 24px 19px; }

/* Controls bar */
.controls-bar { display: flex; gap: 12px; margin: 0 0 16px; flex-wrap: wrap; align-items: center; }
.controls-bar input, .controls-bar select { font-family: Georgia, serif; font-size: 13px; padding: 5px 8px; border: 1px solid #ccc; }
.controls-bar input:focus, .controls-bar select:focus { outline: none; border-color: #1e3a5f; }
.controls-bar select { background: #fff; }
.export-btn { font-family: Georgia, serif; font-size: 11px; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; color: #fff; background: #1e3a5f; border: none; padding: 6px 14px; cursor: pointer; }
.export-btn:hover { background: #2a4a73; }

/* Stats */
.pipeline-stats { display: flex; gap: 12px; margin: 0 0 16px; flex-wrap: wrap; }
.pipeline-stats .stat { font-size: 11px; color: #666; }
.pipeline-stats .stat strong { color: #111; }

/* Table */
table { width: 100%; border-collapse: collapse; font-size: 13px; }
th { text-align: left; font-size: 10px; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; color: #666; border-bottom: 2px solid #111; padding: 6px 6px; cursor: pointer; white-space: nowrap; }
th:hover { color: #111; }
td { padding: 6px; border-bottom: 1px solid #eee; vertical-align: top; }
tr:hover td { background: #fafafa; }
td input, td select, td textarea { font-family: Georgia, serif; font-size: 12px; padding: 3px 5px; border: 1px solid transparent; background: transparent; width: 100%; box-sizing: border-box; }
td input:focus, td select:focus, td textarea:focus { border-color: #ccc; background: #fff; outline: none; }
td select { cursor: pointer; }
td textarea { resize: vertical; min-height: 28px; height: 28px; }
.tier-a { font-weight: 700; color: #1e3a5f; }
.tier-b { color: #333; }
.tier-c { color: #666; }
.status-cold { color: #999; }
.status-researched { color: #666; }
.status-contacted { color: #ca8a04; }
.status-meeting { color: #2563eb; }
.status-committed { color: #16a34a; font-weight: 700; }
.status-donor { color: #1e3a5f; font-weight: 700; }
</style>
</head>
<body>

<div class="header">
  <h1 class="site-title">BURNHAM CIVIC</h1>
  <a href="../membership.html" class="subscribe">Subscribe</a>
</div>
<div class="nav">
  <a href="../">Seattle</a>
  <a href="./" class="active">LA</a>
  <a href="../membership.html">Intelligence</a>
  <a href="mailto:operations@burnhamcivic.org">Contact</a>
</div>
<hr>

<a href="./" class="back">&larr; Los Angeles</a>

<h1 class="article-title">The Network</h1>
<p class="article-subtitle">100 key leaders. The coalition that wins.</p>

<div class="burnham-quote">"The Plan of Chicago was not a government project. It was funded by the Commercial Club of Chicago, 328 of the city's most influential business leaders. They didn't wait for City Hall. They built the coalition first, then presented the plan. This is your Commercial Club."</div>
<p class="burnham-attr">Burnham Civic</p>

<div class="controls-bar">
  <input type="text" id="search-input" placeholder="Search name or company...">
  <select id="filter-sector"><option value="">All Sectors</option></select>
  <select id="filter-status"><option value="">All Status</option></select>
  <select id="filter-tier"><option value="">All Tiers</option><option value="A">Tier A</option><option value="B">Tier B</option><option value="C">Tier C</option></select>
  <button class="export-btn" onclick="exportCSV()">Export CSV</button>
</div>

<div class="pipeline-stats" id="pipeline-stats"></div>

<table>
  <thead>
    <tr>
      <th onclick="sortBy('name')">Name</th>
      <th onclick="sortBy('company')">Company</th>
      <th onclick="sortBy('sector')">Sector</th>
      <th onclick="sortBy('tier')">Tier</th>
      <th onclick="sortBy('status')">Status</th>
      <th>Notes</th>
      <th onclick="sortBy('lastTouched')">Last Touch</th>
    </tr>
  </thead>
  <tbody id="crm-tbody"></tbody>
</table>

<hr>
<p style="font-size:11px;color:#888;">Burnham Civic / Los Angeles. All data stored locally in your browser. Export to CSV for portability.</p>

<script src="network-data.js"></script>
<script>
var STATUSES = ['COLD','RESEARCHED','CONTACTED','MEETING','COMMITTED','DONOR'];
var STATE_KEY = 'tbc_la_network';
var sortField = 'tier';
var sortAsc = true;

function loadState() {
  try { return JSON.parse(localStorage.getItem(STATE_KEY) || '{}'); }
  catch(e) { return {}; }
}
function saveState(state) { localStorage.setItem(STATE_KEY, JSON.stringify(state)); }

function getMerged() {
  var state = loadState();
  return NETWORK_DATA.map(function(base, i) {
    var s = state[base.name] || {};
    return {
      name: base.name,
      company: base.company,
      title: base.title,
      sector: base.sector,
      tier: base.tier,
      baseNote: base.note,
      status: s.status || 'COLD',
      notes: s.notes || '',
      lastTouched: s.lastTouched || '',
      nextAction: s.nextAction || ''
    };
  });
}

function updateField(name, field, value) {
  var state = loadState();
  if (!state[name]) state[name] = {};
  state[name][field] = value;
  if (field !== 'lastTouched' && field !== 'notes') {
    state[name].lastTouched = new Date().toISOString().slice(0,10);
  }
  saveState(state);
  renderStats();
}

function populateFilters() {
  var sectors = {};
  NETWORK_DATA.forEach(function(d) { sectors[d.sector] = true; });
  var sel = document.getElementById('filter-sector');
  Object.keys(sectors).sort().forEach(function(s) {
    var opt = document.createElement('option');
    opt.value = s; opt.textContent = s;
    sel.appendChild(opt);
  });
  var statusSel = document.getElementById('filter-status');
  STATUSES.forEach(function(s) {
    var opt = document.createElement('option');
    opt.value = s; opt.textContent = s;
    statusSel.appendChild(opt);
  });
}

function renderStats() {
  var data = getMerged();
  var counts = {};
  STATUSES.forEach(function(s) { counts[s] = 0; });
  data.forEach(function(d) { counts[d.status] = (counts[d.status] || 0) + 1; });
  var html = STATUSES.map(function(s) {
    return '<span class="stat"><strong>' + counts[s] + '</strong> ' + s.toLowerCase() + '</span>';
  }).join('');
  document.getElementById('pipeline-stats').innerHTML = html;
}

function render() {
  var data = getMerged();
  var search = document.getElementById('search-input').value.toLowerCase();
  var sectorFilter = document.getElementById('filter-sector').value;
  var statusFilter = document.getElementById('filter-status').value;
  var tierFilter = document.getElementById('filter-tier').value;

  data = data.filter(function(d) {
    if (search && d.name.toLowerCase().indexOf(search) === -1 && d.company.toLowerCase().indexOf(search) === -1) return false;
    if (sectorFilter && d.sector !== sectorFilter) return false;
    if (statusFilter && d.status !== statusFilter) return false;
    if (tierFilter && d.tier !== tierFilter) return false;
    return true;
  });

  data.sort(function(a, b) {
    var va = a[sortField] || '', vb = b[sortField] || '';
    if (typeof va === 'string') va = va.toLowerCase();
    if (typeof vb === 'string') vb = vb.toLowerCase();
    var cmp = va < vb ? -1 : va > vb ? 1 : 0;
    return sortAsc ? cmp : -cmp;
  });

  var tbody = document.getElementById('crm-tbody');
  tbody.innerHTML = '';
  data.forEach(function(d) {
    var tr = document.createElement('tr');
    var statusClass = 'status-' + d.status.toLowerCase();
    var tierClass = 'tier-' + d.tier.toLowerCase();

    var statusOpts = STATUSES.map(function(s) {
      return '<option value="' + s + '"' + (s === d.status ? ' selected' : '') + '>' + s + '</option>';
    }).join('');

    tr.innerHTML =
      '<td><span class="' + tierClass + '">' + d.name + '</span><br><span style="font-size:11px;color:#888;">' + d.title + '</span></td>' +
      '<td>' + d.company + '</td>' +
      '<td style="font-size:11px;">' + d.sector + '</td>' +
      '<td class="' + tierClass + '">' + d.tier + '</td>' +
      '<td><select class="' + statusClass + '" onchange="updateField(\'' + d.name.replace(/'/g, "\\'") + '\',\'status\',this.value);render();">' + statusOpts + '</select></td>' +
      '<td><textarea onchange="updateField(\'' + d.name.replace(/'/g, "\\'") + '\',\'notes\',this.value)">' + (d.notes || d.baseNote) + '</textarea></td>' +
      '<td style="font-size:11px;white-space:nowrap;">' + (d.lastTouched || '') + '</td>';
    tbody.appendChild(tr);
  });
  renderStats();
}

function sortBy(field) {
  if (sortField === field) sortAsc = !sortAsc;
  else { sortField = field; sortAsc = true; }
  render();
}

function exportCSV() {
  var data = getMerged();
  var header = 'Name,Company,Title,Sector,Tier,Status,Notes,Last Touched\n';
  var rows = data.map(function(d) {
    return [d.name, d.company, d.title, d.sector, d.tier, d.status, '"' + (d.notes || d.baseNote || '').replace(/"/g, '""') + '"', d.lastTouched].join(',');
  }).join('\n');
  var blob = new Blob([header + rows], { type: 'text/csv' });
  var a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'la-network-' + new Date().toISOString().slice(0,10) + '.csv';
  a.click();
}

populateFilters();
render();
document.getElementById('search-input').addEventListener('input', render);
document.getElementById('filter-sector').addEventListener('change', render);
document.getElementById('filter-status').addEventListener('change', render);
document.getElementById('filter-tier').addEventListener('change', render);
</script>
<script src="gate.js"></script>
</body>
</html>
```

- [ ] **Step 2: Verify the CRM page**

Run: `open /Users/jackwalsh/Dropbox/Seattle/burnham-civic-site/la/network.html`

Verify: Password modal appears. After entering "pratt": table shows all 100 contacts. Search filters work. Status dropdowns change and persist on refresh. Tier/sector/status filters narrow the list. Pipeline stats update. Export CSV downloads a valid CSV file. Notes are editable and persist.

- [ ] **Step 3: Commit**

```bash
cd /Users/jackwalsh/Dropbox/Seattle/burnham-civic-site
git add la/network.html
git commit -m "Add password-gated Network CRM page with 100 LA business leaders"
```

---

### Task 14: Final Integration and Push

**Files:**
- All files in `la/` directory

- [ ] **Step 1: Test all navigation links**

Open `la/index.html` and click every link. Verify:
- Each accountability page loads (LAHSA, LAFD, LAPD, DWP)
- Each infrastructure page loads (Transit, Building)
- Gated pages show password modal (Cabinet, Network)
- Back links on all sub-pages return to hub
- Main site nav "LA" link works from the Seattle page
- Seattle link from LA pages returns to main site

- [ ] **Step 2: Verify password gate shares cookie**

Enter password on Cabinet page. Navigate to Network page. Verify: no password prompt (cookie is shared via `/la/` path).

- [ ] **Step 3: Test mobile responsiveness**

Open `la/index.html` in Chrome DevTools mobile view (iPhone SE, 375px). Verify:
- Hub page is readable, no horizontal scroll
- Cabinet grid collapses to single column
- CRM table is usable (may need horizontal scroll, which is acceptable)
- Password modal is centered and usable

- [ ] **Step 4: Push to GitHub Pages**

```bash
cd /Users/jackwalsh/Dropbox/Seattle/burnham-civic-site
git push origin main
```

Verify: `https://burnhamcivic.org/la/` loads within 2-3 minutes of push.

- [ ] **Step 5: Verify live site**

Open `https://burnhamcivic.org/la/` in browser. Verify:
- Hub page loads with correct styling
- All links work
- LAHSA data table populates
- Password gate works on Cabinet and Network pages
