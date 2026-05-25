"""Generate the background plate for the court-2026 OG card.
Neoclassical courthouse colonnade (the Washington Temple of Justice), dusk,
deep navy and gold, cinematic and slightly desaturated so the gold deco frame
and type read cleanly on top. Matches the existing Burnham Civic OG look.
"""
import json, os, base64, sys, urllib.request, urllib.error

API_KEY = json.load(open(os.path.expanduser("~/.claude/connectors/gemini/config.json")))["api_key"]
MODEL = "gemini-3-pro-image-preview"
ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "court-bg.png")

PROMPT = (
    "Cinematic wide photograph of a grand neoclassical American courthouse facade at blue-hour dusk, "
    "a long row of tall Corinthian stone columns and a triangular pediment, modeled on the Washington "
    "State Temple of Justice in Olympia. Shot straight on, symmetrical, the colonnade filling the frame. "
    "Deep midnight-navy sky, the stone lit with warm golden uplighting so it glows amber against the blue. "
    "Moody, slightly desaturated, soft fog at the base of the columns, faint reflection on wet plaza stone. "
    "Empty, monumental, dignified. No people, no text, no signage, no flags. Muted contrast in the upper "
    "third of the image so an overlay can sit on top. 16:9 widescreen composition, 1200x630 aspect. "
    "Color palette restricted to deep navy blue (#1e3a5f) and antique gold (#c9a227). Photorealistic, "
    "fine grain, architectural photography, not an illustration."
)


def gen(prompt, out_path):
    body = {"contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {"responseModalities": ["IMAGE"]}}
    req = urllib.request.Request(ENDPOINT, data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            resp = json.loads(r.read())
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {e.read()[:300].decode('utf-8','replace')}"); return False
    for c in resp.get("candidates", []):
        for part in c.get("content", {}).get("parts", []):
            inline = part.get("inlineData") or part.get("inline_data")
            if inline and inline.get("data"):
                open(out_path, "wb").write(base64.b64decode(inline["data"]))
                return True
    print(f"no image: {json.dumps(resp)[:300]}"); return False


if __name__ == "__main__":
    ok = gen(PROMPT, OUT)
    print(f"OK {os.path.getsize(OUT)} bytes -> {OUT}" if ok else "FAILED")
