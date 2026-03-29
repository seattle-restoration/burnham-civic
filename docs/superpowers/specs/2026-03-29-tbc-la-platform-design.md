# TBC-LA Platform Design Spec

**Date:** 2026-03-29
**Purpose:** Build an LA accountability and campaign intelligence platform on burnhamcivic.org to support Spencer Pratt's 2026 LA mayoral campaign, establish Burnham Civic as a national brand, and serve as the introduction/pitch to Pratt's team.

## 1. Architecture

### Site Structure

```
burnhamcivic.org/la/              <- Hub page (index.html)
burnhamcivic.org/la/lahsa.html    <- LAHSA spending + NGO 990 network
burnhamcivic.org/la/lafd.html     <- Fire response accountability
burnhamcivic.org/la/lapd.html     <- Crime data + staffing
burnhamcivic.org/la/dwp.html      <- Utility spending audit
burnhamcivic.org/la/transit.html  <- Metro/rail + 2028 Olympics readiness
burnhamcivic.org/la/building.html <- Permits, rebuilds, Burnham standard
burnhamcivic.org/la/cabinet.html  <- Shadow cabinet (password-gated)
burnhamcivic.org/la/network.html  <- Top 100 CRM (password-gated)
```

All files live in `/la/` directory within the burnham-civic-site repo. Deployed via GitHub Pages on `main` branch (same as existing site).

### Navigation

Add "LA" to the top nav bar on `index.html` (the Seattle page):

```
SEATTLE | LA | USA | NEWS | INTELLIGENCE | STRATEGY | CONTACT
```

LA hub page gets its own nav:

```
BURNHAM CIVIC / LA
LAHSA | LAFD | LAPD | DWP | TRANSIT | BUILDING | CABINET | NETWORK
```

### Password Gate

- Password: `pratt`
- Applies to: `cabinet.html` and `network.html`
- Implementation: simple modal overlay on page load, cookie `tbc_la_auth` persists 30 days
- Public pages (LAHSA, LAFD, LAPD, DWP, Transit, Building) are fully open
- The hub page shows gated items with a lock icon but they're clickable (gate is on the destination page)

## 2. Daniel Burnham DNA

Every page opens with a Burnham principle applied to LA. This is the philosophical backbone. Burnham rebuilt Chicago after the 1871 fire. Pratt wants to rebuild LA after the 2025 fire. The parallel is the pitch.

### Per-Page Burnham Threads

- **Hub:** "Make no little plans. They have no magic to stir men's blood." The opening line. Sets the tone.
- **LAHSA:** "A noble, logical diagram once recorded will not die." Every dollar must be traced. Every outcome recorded. The diagram is the accountability.
- **LAFD:** "Make no little plans." The Palisades fire proved LA's plans were little. Burnham's fire response: don't just rebuild, rebuild to a standard that prevents the next disaster.
- **LAPD:** "The city must be planned as a whole." Public safety can't be siloed. Burnham's grid connected every district. LA's policing must do the same.
- **DWP:** Burnham planned infrastructure for the next century, not the next election cycle. DWP has been planning for the next rate increase.
- **Transit:** Burnham's 1909 Plan of Chicago created the rail and boulevard system that still works 117 years later. LA's Metro was supposed to be ready for the 2026 World Cup. It wasn't. Apply Burnham's principles: plan for permanence, build for the Olympics and beyond.
- **Building:** Burnham didn't just rebuild after the Chicago fire. He set a standard that made the next city better than the one that burned. LA's post-fire rebuild is the same opportunity.
- **Cabinet:** Burnham assembled his team publicly. The people of Chicago knew who was building their city. Spencer can do the same.
- **Network:** Burnham's Plan of Chicago was funded by the Commercial Club, 328 of the city's most influential business leaders. The coalition came first, then the plan.

## 3. Hub Page (la/index.html)

Same format as burnhamcivic.org Seattle page. Categorized list of operations with one-line descriptions, tags, and links to dedicated pages.

### Content Structure

**Header:**
```
BURNHAM CIVIC / LA
"Make no little plans. They have no magic to stir men's blood."
```

**Intro paragraph:** "Los Angeles is rebuilding. The question is whether it rebuilds to a standard or rebuilds by accident. These pages track the agencies, the spending, the decisions, and the people who will determine the answer. Daniel Burnham rebuilt Chicago after the fire. This is what that looks like for LA."

**ACCOUNTABILITY**
- LAHSA Exposed `HOMELESSNESS` - Where $800M/year goes. NGO contracts, outcomes, fraud indicators. 990 data on every grantee.
- LAFD Response Map `FIRE` - Wildfire response times, station coverage, resource allocation vs. actual fires.
- LAPD by the Numbers `PUBLIC SAFETY` - Crime trends, staffing shortfalls, response times by district.
- DWP Audit `UTILITIES` - Rate increases vs. infrastructure investment. Where the money leaks.

**INFRASTRUCTURE**
- The Train That Wasn't Ready `TRANSIT` - LA Metro promised completion for the 2026 World Cup. It missed. What Burnham's approach to rail would look like for the 2028 Olympics.
- The Standard LA Forgot `CONSTRUCTION` - Permit timelines, inspection backlogs, post-fire rebuild bottlenecks. What a Burnham building standard looks like.

**STRATEGY** (lock icon on these two)
- The Preliminary Cabinet `LEADERSHIP` `GATED` - Name your people before the election. Let LA see who's running what.
- The Network `RECRUITMENT` `GATED` - 100 key leaders. The coalition that wins. (Mini-CRM)

## 4. LAHSA Page (la/lahsa.html)

The flagship accountability page. This is the one that proves TBC's value.

### Data Sources
- **LAHSA contracts/grants:** Public records from lahsa.org, LA Controller open data
- **ProPublica Nonprofit Explorer API:** `https://projects.propublica.org/nonprofits/api/v2/` - free, no auth. Returns 990 filing data by EIN.
- **CA Secretary of State:** nonprofit registration data
- **LA Homeless Services Authority annual reports:** outcome metrics

### What to Display

**NGO Contract Table:**
| Organization | Annual Contract | Program Type | Outcomes Reported | Cost Per Outcome |
|---|---|---|---|---|

**990 Deep Dive (per org):**
- Total revenue (3-year trend)
- Executive compensation (CEO, top 5 paid)
- Program expenses vs. admin/fundraising ratio
- Related organizations and shared board members
- Revenue connections: which orgs are funding which

**Red Flag Indicators:**
- Executive comp > $200K
- Program expense ratio < 65%
- Revenue spike with flat or declining outcomes
- Board member overlap with other LAHSA grantees (self-dealing network)
- New orgs receiving large contracts (< 3 years old, > $1M contract)

**Burnham Framing:** "A noble, logical diagram once recorded will not die." Open with this. The diagram IS the accountability. Trace every dollar from City Hall to the NGO to the program to the person it was supposed to help.

## 5. LAFD Page (la/lafd.html)

### Data Sources
- **LA Open Data Portal (data.lacity.org):** Fire incident data API
- **LAFD annual reports:** Station staffing, apparatus deployment
- **CAL FIRE:** State-level wildfire data
- **News/public records:** Bass administration response timeline

### Content
- Wildfire response timeline (Palisades fire)
- Station coverage map vs. fire-risk zones
- Staffing trends (hiring vs. attrition vs. population growth)
- Equipment/apparatus age and replacement schedule
- Comparison: LAFD budget growth vs. fire outcomes
- Burnham angle: after the Chicago fire, the city didn't just rebuild the fire department. It rebuilt the city so fires couldn't spread. Wider streets, fireproof materials, building codes. LA needs structural solutions, not just more trucks.

## 6. LAPD Page (la/lapd.html)

### Data Sources
- **LAPD CompStat data** (public)
- **data.lacity.org:** Crime data API, use-of-force data
- **LAPD staffing reports:** Sworn officer counts, academy graduation rates

### Content
- Crime trends by category (violent, property, quality-of-life)
- Response time data by district/division
- Staffing: sworn officers vs. authorized strength vs. population
- Budget breakdown: patrol vs. admin vs. special units
- Comparison to other major cities (NYPD, CPD)
- Burnham angle: plan the city as a whole. Connect districts, don't silo them.

## 7. DWP Page (la/dwp.html)

### Data Sources
- **LADWP public reports:** Rate structure, infrastructure spending
- **LA Controller:** DWP transfer to general fund data
- **DWP ratepayer advocate reports**

### Content
- Rate increase history vs. infrastructure investment
- Transfer to general fund (the "DWP tax")
- Major project cost overruns
- Comparison: what ratepayers pay vs. what they get
- Executive compensation at DWP
- Burnham angle: infrastructure planned for the next century, not the next election.

## 8. Transit Page (la/transit.html)

### Data Sources
- **LA Metro:** Project status, ridership data, budget reports
- **Federal Transit Administration:** Grant tracking
- **2028 Olympics transportation plan** (public)

### Content
- World Cup 2026 deadline: what was promised vs. what was delivered
- Current Metro project status (Purple Line, Airport Connector, etc.)
- 2028 Olympics readiness assessment
- Burnham's rail vision applied to LA: what a permanent transit grid looks like vs. event-driven construction
- Cost per mile comparison to other cities

## 9. Building Page (la/building.html)

### Data Sources
- **LADBS (Building & Safety):** Permit data, inspection data
- **data.lacity.org:** Building permit API
- **Post-fire rebuild tracking** (public records)

### Content
- Average permit processing time (new construction, renovation, post-fire rebuild)
- Inspection backlog data
- Post-fire rebuild progress: permits filed vs. issued vs. completed
- Burnham's building standard: what monumental, permanent construction looks like vs. tract housing
- Comparison to other cities' post-disaster rebuild timelines

## 10. Shadow Cabinet Page (la/cabinet.html) - GATED

Password modal on load. Password: `pratt`. Cookie: `tbc_la_auth`, 30-day expiry.

### Roles (each gets a card)
1. **Fire Chief** (LAFD)
2. **Chief of Police** (LAPD)
3. **DWP General Manager**
4. **City Attorney**
5. **LAHSA Executive Director** (or successor agency head)
6. **LA Metro CEO**
7. **Building & Safety Director**
8. **City Administrative Officer** (budget chief)

### Card Layout
Each role card contains:
- **Role title and department**
- **Current holder:** Name, tenure, notable record (brief)
- **What this role controls:** Budget, headcount, key responsibilities
- **Spencer's Pick:** Editable text field (localStorage, key: `tbc_la_cabinet`)
- **Why it matters:** 1-2 sentences on what the right pick changes

### Burnham Framing
"Burnham didn't just draw plans. He assembled the team that could build them. The Commercial Club, the architects, the engineers, the politicians. He named them. Chicago knew who was building their city before the first brick was laid."

The pitch to Pratt: name your cabinet before the election. No other candidate will do this. Voters want to know who's running their city, not just who's sitting in the mayor's chair.

## 11. Network / Mini-CRM Page (la/network.html) - GATED

Same password gate as cabinet page (shares cookie).

### Pre-populated Data
Research and pre-load 100 LA business/property leaders across sectors:
- Real estate / development (top property owners, developers)
- Entertainment industry (studio heads, producers with civic ties)
- Tech (LA-based tech leaders)
- Finance (LA-based fund managers, bank regional heads)
- Construction / trades (AGC members, major GCs)
- Hospitality (hotel owners, restaurant groups)
- Nonprofit / civic (major foundation heads, university presidents)

### CRM Features
- **Contact cards:** Name, company, title, sector, estimated influence tier (A/B/C), public contact info
- **Pipeline status:** Dropdown per contact: `COLD | RESEARCHED | CONTACTED | MEETING | COMMITTED | DONOR`
- **Notes field:** Free text, per contact
- **Last touched:** Date field, per contact
- **Next action:** Free text, per contact
- **Filter/sort:** By status, sector, influence tier, last touched
- **Search:** Name/company text search
- **Export:** CSV download of all contacts + status + notes
- **Import:** JSON upload to merge data

### Data Storage
- All CRM state in localStorage (key: `tbc_la_network`)
- Pre-populated data embedded in HTML as JS object
- User modifications merge on top (never overwrite pre-populated base data)
- Export produces full snapshot including pre-populated + user data

### Burnham Framing
"The Plan of Chicago was not a government project. It was funded by the Commercial Club of Chicago, 328 of the city's most influential business leaders. They didn't wait for City Hall. They built the coalition first, then presented the plan. This is your Commercial Club."

## 12. Design System

### Theme
Neutral/Clean (from CLAUDE.md design system). Same aesthetic as burnhamcivic.org.

### CSS Variables
```css
:root {
  --bg: #fafaf9;
  --surface: #ffffff;
  --border: #e5e5e4;
  --text: #1c1917;
  --text-secondary: #78716c;
  --primary: #16a34a;
  --primary-hover: #15803d;
  --primary-subtle: #f0fdf4;
  --success: #16a34a;
  --warning: #ca8a04;
  --danger: #dc2626;
  --radius: 12px;
  --shadow: 0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04);
}
```

Dark mode via `@media (prefers-color-scheme: dark)`.

### Typography
- System font stack: `-apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', system-ui, sans-serif`
- Headings: `font-weight: 600`, small-caps for section headers (matching Seattle page)
- Burnham quotes in italic serif (`Georgia, 'Times New Roman', serif`)

### Layout
- Max-width container matching Seattle page
- Cards with `var(--radius)` border-radius and `var(--shadow)`
- Tags as inline pill badges (matching Seattle page style: `HOMELESSNESS`, `FIRE`, etc.)
- Lock icon for gated items on hub page
- Responsive breakpoints: 480/768/1024px
- Arrow key navigation on multi-section pages

### Password Modal
- Centered modal, blurred background
- "This section is restricted." + password input + submit button
- On correct password, set cookie `tbc_la_auth=1; max-age=2592000; path=/la/`
- On incorrect, shake animation + "Incorrect password"
- Minimal, clean, no branding clutter

## 13. 990 Lookup Strategy

For every nonprofit referenced on any page:

1. Look up EIN via ProPublica API: `GET /api/v2/search.json?q=ORG_NAME`
2. Get latest 990: `GET /api/v2/organizations/EIN.json`
3. Extract and display:
   - Total revenue, total expenses, net assets
   - Top 5 compensated officers (name, title, compensation)
   - Program service revenue vs. contributions
   - Related organizations listed on Schedule R
4. Flag suspicious patterns (see LAHSA section red flags)
5. Data can be pre-fetched and embedded as JSON in each page (no runtime API calls needed for initial load)

## 14. Implementation Phases

### Phase 1: Hub + LAHSA (highest impact, proves the model)
- Build hub page (la/index.html)
- Build LAHSA page with 990 data
- Add "LA" to main site nav
- Research and embed top LAHSA grantee 990 data

### Phase 2: LAFD + LAPD (Pratt's core issues)
- Build LAFD page with fire incident data
- Build LAPD page with crime/staffing data
- Pull from LA Open Data APIs

### Phase 3: DWP + Transit + Building (infrastructure story)
- Build remaining accountability pages
- Metro/Olympics angle
- Burnham building standard content

### Phase 4: Gated Pages (the closer)
- Build Shadow Cabinet page with role cards
- Build Network/CRM page with pre-populated 100 contacts
- Password gate implementation

### Phase 5: Outreach
- DM Spencer Pratt with link
- Contact his comms team
- Choe as secondary channel when timing is right

## 15. Success Criteria

- Pratt or his team responds to outreach
- At least one page gets referenced or shared by Pratt's campaign
- The LA model validates Burnham Civic as a replicable national platform
- 990 data surfaces at least one genuinely suspicious NGO pattern worth investigating

## 16. Non-Goals

- No backend/server infrastructure (static HTML, GitHub Pages)
- No paid data sources (all free APIs and public records)
- No campaign finance integration (separate legal domain)
- No direct campaign branding (this is Burnham Civic, not "Spencer Pratt for Mayor")
- No Choe involvement until the $50K relationship is funded
