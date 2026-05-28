#!/usr/bin/env node
/**
 * Send the 1905 Burnham SF plan to Gemini 2.5 Pro and ask it to trace
 * the diagonal boulevards as pixel coordinate polylines, then convert
 * to lat/lon using the page's rectangular georeference bounds.
 */
const fs = require('fs');
const path = require('path');
const https = require('https');

const CFG = JSON.parse(fs.readFileSync(
  path.join(process.env.USERPROFILE || process.env.HOME, '.claude/connectors/gemini/config.json'),
  'utf8'
));

const IMG_PATH = path.join(__dirname, '..', '_assets', 'sf-plan', 'burnham-1905-sf-plan.jpg');
const IMG_W = 1536;
const IMG_H = 1456;

// PLAN_BOUNDS in the HTML: [[37.708, -122.518], [37.815, -122.355]]
const NORTH = 37.815, SOUTH = 37.708, WEST = -122.518, EAST = -122.355;

function pxToLatLon(x, y) {
  const lon = WEST + (x / IMG_W) * (EAST - WEST);
  const lat = NORTH - (y / IMG_H) * (NORTH - SOUTH);
  return [lat, lon];
}

const PROMPT = `You are looking at the 1905 Daniel Burnham master plan for San Francisco.
The image is 1536 pixels wide and 1456 pixels tall.
North is roughly up. Pacific Ocean is on the LEFT, San Francisco Bay is on the RIGHT.
The Golden Gate is at the top. Lake Merced is near the bottom-left. Hunters Point is bottom-right.

Identify the major proposed diagonal boulevards and ring drives in Burnham's plan.
These are the prominent wide streets that cut DIAGONALLY across the rectangular street grid,
plus the curving outer ring boulevard.

For each one, return:
- A short name describing the route (eg "Mountain Boulevard from Civic Center to Twin Peaks")
- An ordered list of (x, y) pixel coordinates representing the centerline polyline,
  starting at one end of the boulevard, with intermediate vertices at any major direction change,
  and ending at the other end.
- A "match" field with one of these IDs from the modern atlas, or "none" if it doesn't match:
  embarcadero, panamerican, mountain, mission, sunset, park, presidio, bernal, telegraph, russian, outer

Look in particular for:
1. The Outer Boulevard (a long curving ring around the western and southern flanks of the city)
2. Boulevards radiating from the Civic Center area (near the Van Ness / Market intersection,
   roughly center-right of the image)
3. A diagonal from Telegraph Hill (upper right) toward the Civic Center (Pan-American Avenue)
4. Ring drives around prominent hills (Twin Peaks, Telegraph Hill, Bernal Heights)
5. The Embarcadero parkway along the bay
6. The connection from Civic Center to Golden Gate Park

Return ONLY a JSON object of this shape, no prose:
{
  "boulevards": [
    {
      "name": "...",
      "match": "...",
      "coords": [[x, y], [x, y], ...]
    }
  ]
}
`;

const imgB64 = fs.readFileSync(IMG_PATH).toString('base64');

const body = JSON.stringify({
  contents: [{
    parts: [
      { text: PROMPT },
      { inline_data: { mime_type: 'image/jpeg', data: imgB64 } }
    ]
  }],
  generationConfig: {
    temperature: 0.2,
    response_mime_type: 'application/json'
  }
});

const url = `${CFG.endpoint}/${CFG.model}:generateContent?key=${CFG.api_key}`;
const u = new URL(url);

const req = https.request({
  hostname: u.hostname,
  path: u.pathname + u.search,
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Content-Length': Buffer.byteLength(body)
  }
}, res => {
  let chunks = [];
  res.on('data', c => chunks.push(c));
  res.on('end', () => {
    const raw = Buffer.concat(chunks).toString('utf8');
    let parsed;
    try { parsed = JSON.parse(raw); }
    catch (e) {
      console.error('FAILED to parse Gemini response:');
      console.error(raw);
      process.exit(1);
    }
    if (parsed.error) {
      console.error('Gemini error:', JSON.stringify(parsed.error, null, 2));
      process.exit(1);
    }
    const text = parsed.candidates?.[0]?.content?.parts?.[0]?.text;
    if (!text) {
      console.error('No text in Gemini response');
      console.error(JSON.stringify(parsed, null, 2));
      process.exit(1);
    }
    let result;
    try { result = JSON.parse(text); }
    catch (e) {
      console.error('Gemini response was not JSON:');
      console.error(text);
      process.exit(1);
    }
    // Convert pixel coords to lat/lon
    const out = (result.boulevards || []).map(b => ({
      name: b.name,
      match: b.match,
      px: b.coords,
      latlon: b.coords.map(([x, y]) => pxToLatLon(x, y))
    }));
    fs.writeFileSync(
      path.join(__dirname, '..', '_assets', 'sf-plan', 'gemini-traces.json'),
      JSON.stringify(out, null, 2)
    );
    console.log('--- GEMINI TRACES ---');
    out.forEach(b => {
      console.log(`\n[${b.match}] ${b.name}`);
      console.log(`  ${b.coords?.length || b.px.length} pts: ` + JSON.stringify(b.latlon));
    });
    console.log(`\nWrote _assets/sf-plan/gemini-traces.json`);
  });
});
req.on('error', e => { console.error('Request error:', e.message); process.exit(1); });
req.write(body);
req.end();
