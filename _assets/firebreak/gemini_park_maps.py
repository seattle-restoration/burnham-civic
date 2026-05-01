"""Generate clean cartographic park maps with neighborhood labels prominent.

Each prompt specifies the park's rough geographic location, the named
neighborhoods to label at approximate positions, and a clean cartographic
style with large readable typography. The park boundary and firebreak
corridor are shown but the neighborhoods are the visual hero.
"""
import json, os, base64, sys, time, urllib.request, urllib.error

API_KEY = json.load(open(os.path.expanduser("~/.claude/connectors/gemini/config.json")))["api_key"]
MODEL = "gemini-3-pro-image-preview"
ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"
HERE = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(HERE, "gemini-raw")
os.makedirs(RAW_DIR, exist_ok=True)

STYLE_BASE = (
    "Clean Edward Tufte-style cartographic illustration of a Los Angeles ridgeline park, hand-drawn ink "
    "and pale watercolor wash on warm cream paper background. Minimal ornament, maximal clarity. "
    "Top-down map view (NOT a perspective view). Soft sepia and pale ochre topographic shading "
    "showing the canyons and ridgelines. North arrow at top right. Scale bar at bottom right. "
    "All neighborhood labels in BOLD LARGE serif typography (Georgia or Caslon style), set in "
    "generous letter-spacing. Each labeled neighborhood gets a thin underline. The park boundary "
    "drawn as a thick warm-green outlined polygon, labeled in serif 'PLA-Firebreak'. The proposed "
    "firebreak corridor drawn as a thick crimson dashed line at the residential interface. "
    "The whole map should read clearly even at thumbnail size. No people, no buildings, no roads "
    "drawn in detail - only neighborhood-name labels at their approximate positions and the "
    "topographic shading. Flat 2D cartographic style, NOT a satellite or aerial photo."
)

PARKS = [
    ("park-01-topanga-crest.png",
     "Subject: Topanga Crest park, Santa Monica Mountains ridgeline above Pacific Palisades. "
     "Label these neighborhoods at their approximate positions on the map: 'PACIFIC PALISADES' "
     "south of the ridge in large bold serif, 'SUNSET MESA' southwest in large serif, 'CASTELLAMMARE' "
     "west on the coastal bluff. Park boundary drawn at the ridgeline center. Firebreak corridor drawn "
     "along the southern park boundary where it meets the residential edge. Pacific Ocean visible at "
     "the southwest corner labeled 'PACIFIC OCEAN' in italic serif."),

    ("park-02-sullivan-canyon.png",
     "Subject: Sullivan Canyon Top park, ridgeline north of Brentwood. "
     "Label these neighborhoods at their approximate positions on the map: 'BRENTWOOD' south of the "
     "ridge in large bold serif, 'BRENTWOOD PARK' southeast in serif, 'KENTER CANYON' east in serif. "
     "Park boundary at the ridgeline center. Firebreak corridor along the southern park boundary "
     "facing the residential edge. The 405 freeway corridor labeled 'I-405' in small italic at far east."),

    ("park-03-mandeville-ridge.png",
     "Subject: Mandeville Ridge park, ridge above Mandeville Canyon. "
     "Label these neighborhoods at their approximate positions on the map: 'MANDEVILLE CANYON' as a "
     "long narrow band running south from the ridge, the canyon road shown as a single line. "
     "'BRENTWOOD' labeled to the southeast. Park boundary at the ridgeline. Firebreak corridor along "
     "the residential interface. Annotation: 'ONE ROAD, 5 MILES DEEP' in small caps near the canyon."),

    ("park-04-sepulveda-crown.png",
     "Subject: Sepulveda Crown park, Santa Monica Mountains crest east of the 405 freeway. "
     "Label these neighborhoods at their approximate positions on the map: 'BEL-AIR (EAST)' south "
     "of the ridge in large bold serif, 'CASIANO' southeast in serif, 'ROSCOMARE' east in serif, "
     "'GETTY CENTER' north in serif. Park boundary at the ridge. Firebreak corridor along the "
     "residential side. The 405 freeway labeled 'I-405' as a thick gray line at the western edge."),

    ("park-05-stone-canyon.png",
     "Subject: Stone Canyon park, north end of Stone Canyon above the Stone Canyon Reservoir. "
     "Label these neighborhoods at their approximate positions: 'BEL-AIR (EAST)' south of the ridge "
     "in large bold serif. Stone Canyon Reservoir labeled 'STONE CANYON RESERVOIR' as a blue oval "
     "at the south. Park boundary at the canyon-head ridge. Annotation in small caps: '1961 BEL "
     "AIR FIRE IGNITION 8:15 AM NOV 6' marked with a small flame symbol at the canyon north end."),

    ("park-06-beverly-glen.png",
     "Subject: Beverly Glen Top park, ridge above Beverly Glen Boulevard. "
     "Label neighborhoods: 'LOWER BEVERLY GLEN' south of ridge in large bold serif, "
     "'BEL-AIR (EAST)' southwest, 'HOLMBY HILLS' south. Beverly Glen Boulevard shown as a single "
     "thin line running through the canyon labeled 'BEVERLY GLEN BLVD' in small italic. "
     "Park boundary at the ridgeline."),

    ("park-07-fryman-upper.png",
     "Subject: Fryman Upper park, Hollywood Hills ridge between San Fernando Valley and the city. "
     "Label these neighborhoods: 'STUDIO CITY' north of the ridge in large bold serif, "
     "'SHERMAN OAKS (EAST)' northwest in large bold serif. Mulholland Drive shown as a thin "
     "line along the ridge labeled 'MULHOLLAND DRIVE' in small italic. Park boundary at the ridge. "
     "Firebreak corridor on the north (Valley) side. Annotation in small caps: 'CROSS MOUNTAIN "
     "TRAIL CORRIDOR' along the spine."),

    ("park-08-coldwater-canyon.png",
     "Subject: Coldwater Canyon park, Hollywood Hills above Coldwater Canyon Drive. "
     "Label neighborhoods: 'STUDIO CITY (SOUTH)' north of the ridge in large bold serif, "
     "'BEVERLY HILLS (NORTH SLOPES)' south in large bold serif, 'BENEDICT CANYON' southeast in serif. "
     "Coldwater Canyon Drive shown as a thin line through the canyon labeled in small italic. "
     "Annotation: 'TREEPEOPLE since 1977' in small caps within the park boundary."),

    ("park-09-runyon-canyon.png",
     "Subject: Runyon Canyon park, Hollywood Hills directly above Hollywood Boulevard. "
     "Label neighborhoods: 'HOLLYWOOD' south of ridge in large bold serif, 'WEST HOLLYWOOD' "
     "southwest in serif, 'SUNSET STRIP' south in serif. Hollywood Boulevard labeled "
     "'HOLLYWOOD BLVD' as a thin line at the south. Park boundary at the ridge. Annotation in "
     "small caps: 'JAN 2025 SUNSET FIRE 43 ACRES' marked with small flame near Solar/Astral Drive."),

    ("park-10-cahuenga-peak.png",
     "Subject: Cahuenga Peak in Griffith Park, the highest point at 1,820 ft. "
     "Label neighborhoods: 'HOLLYWOOD (NORTH SLOPE)' south of peak in large bold serif, "
     "'LAKE HOLLYWOOD' east as a labeled blue oval reservoir, 'TOLUCA LAKE' north in serif. "
     "The Hollywood Sign shown as the simple letters 'HOLLYWOOD' in white block typography near the "
     "peak. Park boundary outlines Griffith Park's western lobe. Peak elevation labeled '1,820 FT'."),

    ("park-11-will-rogers-ridge.png",
     "Subject: Will Rogers Ridge park, the ridge above Pacific Palisades. "
     "Label neighborhoods: 'PACIFIC PALISADES (EAST)' south of the ridge in large bold serif, the "
     "label area shaded faint amber to indicate the 2025 fire footprint. Annotation in small caps: "
     "'99.5% BURNED 2025' across the park area. Park boundary at the ridgeline. Firebreak corridor "
     "on the southern park boundary. Will Rogers Ranch House shown as a small structure symbol "
     "labeled 'RANCH HOUSE (DESTROYED 2025)'."),

    ("park-12-wilacre.png",
     "Subject: Wilacre park, 128 acres on north face of Santa Monica Mountains, MRCA-owned, "
     "demonstration project. "
     "Label neighborhoods: 'STUDIO CITY' north of the ridge in large bold serif, "
     "'SHERMAN OAKS (EAST)' northwest in large bold serif. Park boundary outlines the 128-acre "
     "parcel clearly. The Betty B. Dearing Cross Mountain Trail shown as a dashed crimson line "
     "running through the park labeled 'BETTY B. DEARING TRAIL' in small italic. "
     "Annotation in bold small caps: 'PHASE 0 DEMONSTRATION CORRIDOR' across the bottom. "
     "Connecting parks shown as faint outlines to the east labeled 'COLDWATER', 'FRYMAN', "
     "'FRANKLIN CANYON'."),
]


def gen(prompt: str, out_path: str) -> bool:
    body = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {"responseModalities": ["IMAGE"]},
    }
    req = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            resp = json.loads(r.read())
    except urllib.error.HTTPError as e:
        print(f"  HTTP {e.code}: {e.read()[:300].decode('utf-8','replace')}")
        return False
    except Exception as e:
        print(f"  ERR: {e}")
        return False
    cands = resp.get("candidates", [])
    for c in cands:
        for part in c.get("content", {}).get("parts", []):
            inline = part.get("inlineData") or part.get("inline_data")
            if inline and inline.get("data"):
                img_bytes = base64.b64decode(inline["data"])
                with open(out_path, "wb") as f:
                    f.write(img_bytes)
                return True
    print(f"  no image in response: {json.dumps(resp)[:300]}")
    return False


if __name__ == "__main__":
    only = sys.argv[1] if len(sys.argv) > 1 else None
    success = 0
    for fname, prompt_park in PARKS:
        if only and only not in fname:
            continue
        out_path = os.path.join(RAW_DIR, fname)
        full_prompt = STYLE_BASE + "\n\n" + prompt_park
        print(f"GEN {fname}...")
        ok = gen(full_prompt, out_path)
        if ok:
            print(f"  OK {os.path.getsize(out_path)} bytes")
            success += 1
        time.sleep(2)
    print(f"\n{success}/{len(PARKS)} succeeded")
