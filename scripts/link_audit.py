"""Link audit for burnhamcivic.org. Walks every .html in the site root,
extracts all href values + data-href values, classifies them, and verifies
internal links resolve to a file that exists. Emits a report to stdout
and writes audit_report.md next to the script."""
import os
import re
import sys
import urllib.parse
from collections import defaultdict

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Match href= ONLY in HTML attribute position (preceded by whitespace, not by . or letter).
# This avoids false positives on JS string concatenation like a.href='mai'+'lto:'+...
# which is an intentional anti-scrape pattern used sitewide for mailto links.
HREF_RX = re.compile(r"""(?<![.\w])href\s*=\s*["']([^"']+)["']""", re.IGNORECASE)
DATA_HREF_RX = re.compile(r"""(?<![.\w])data-href\s*=\s*["']([^"']+)["']""", re.IGNORECASE)
SRC_RX = re.compile(r"""(?<![.\w])(?:src|data-src)\s*=\s*["']([^"']+)["']""", re.IGNORECASE)

def list_html_files(root):
    out = []
    for entry in os.listdir(root):
        full = os.path.join(root, entry)
        if os.path.isfile(full) and entry.lower().endswith(".html"):
            out.append(full)
    return sorted(out)

def file_exists_in_repo(root, link):
    # Strip query and fragment
    link = link.split("#", 1)[0].split("?", 1)[0]
    if not link:
        return True  # pure anchor, fine
    link = urllib.parse.unquote(link)
    if link.startswith("/"):
        link = link[1:]
    target = os.path.normpath(os.path.join(root, link))
    if not target.startswith(root):
        return None  # path traversal, skip
    if os.path.exists(target):
        return True
    # Also try as directory index
    if os.path.isdir(target):
        idx = os.path.join(target, "index.html")
        if os.path.exists(idx):
            return True
    return False

def classify(link):
    l = link.strip()
    if not l:
        return "empty"
    low = l.lower()
    if low.startswith("mailto:"):
        return "mailto"
    if low.startswith("tel:"):
        return "tel"
    if low.startswith("javascript:"):
        return "js"
    if low.startswith("#"):
        return "anchor"
    if low.startswith(("http://", "https://", "//")):
        return "external"
    if low.startswith("data:"):
        return "data"
    return "internal"

def main():
    html_files = list_html_files(ROOT)
    print(f"Scanning {len(html_files)} HTML files in {ROOT}")
    print()

    broken_internal = defaultdict(list)        # file -> [bad_link]
    placeholder_links = defaultdict(list)      # file -> [#, ""]
    data_href_targets = defaultdict(list)      # file -> [(data-href, exists?)]
    external_links = defaultdict(set)          # file -> {url}
    image_misses = defaultdict(list)           # file -> [img path]
    counts = {"internal": 0, "external": 0, "mailto": 0, "anchor": 0, "data_href": 0, "img": 0}

    for fp in html_files:
        rel = os.path.basename(fp)
        try:
            with open(fp, "r", encoding="utf-8") as fh:
                txt = fh.read()
        except UnicodeDecodeError:
            with open(fp, "r", encoding="latin-1") as fh:
                txt = fh.read()

        # href
        for m in HREF_RX.finditer(txt):
            link = m.group(1)
            kind = classify(link)
            if kind == "internal":
                counts["internal"] += 1
                ok = file_exists_in_repo(ROOT, link)
                if ok is False:
                    broken_internal[rel].append(link)
            elif kind == "external":
                counts["external"] += 1
                external_links[rel].add(link)
            elif kind == "mailto":
                counts["mailto"] += 1
            elif kind == "anchor":
                counts["anchor"] += 1
                if link.strip() in ("#", ""):
                    placeholder_links[rel].append(link)
            elif kind == "empty":
                placeholder_links[rel].append("(empty)")

        # data-href (gated link pattern)
        for m in DATA_HREF_RX.finditer(txt):
            counts["data_href"] += 1
            link = m.group(1)
            kind = classify(link)
            if kind == "internal":
                ok = file_exists_in_repo(ROOT, link)
                data_href_targets[rel].append((link, ok))
                if ok is False:
                    broken_internal[rel].append(f"(data-href) {link}")

        # img src + data-src (only local, ignore http/data:)
        for m in SRC_RX.finditer(txt):
            link = m.group(1)
            kind = classify(link)
            if kind == "internal":
                counts["img"] += 1
                ok = file_exists_in_repo(ROOT, link)
                if ok is False:
                    image_misses[rel].append(link)

    # Build report
    lines = []
    lines.append("# Burnham Civic Link Audit")
    lines.append("")
    lines.append(f"- HTML files scanned: **{len(html_files)}**")
    lines.append(f"- Internal href links: {counts['internal']}")
    lines.append(f"- External href links: {counts['external']}")
    lines.append(f"- Anchor (#) links: {counts['anchor']}")
    lines.append(f"- mailto: links: {counts['mailto']}")
    lines.append(f"- data-href (gated) links: {counts['data_href']}")
    lines.append(f"- Local image/src refs: {counts['img']}")
    lines.append("")

    # Broken internal links
    lines.append("## BROKEN internal links")
    if not broken_internal:
        lines.append("None. Every internal href resolves to a file that exists.")
    else:
        total = sum(len(v) for v in broken_internal.values())
        lines.append(f"**{total}** broken internal hrefs across **{len(broken_internal)}** pages.")
        lines.append("")
        for f in sorted(broken_internal):
            lines.append(f"### {f}")
            for link in broken_internal[f]:
                lines.append(f"- `{link}`")
            lines.append("")

    # Broken images
    lines.append("## BROKEN local images")
    if not image_misses:
        lines.append("None.")
    else:
        for f in sorted(image_misses):
            lines.append(f"### {f}")
            for link in image_misses[f]:
                lines.append(f"- `{link}`")
            lines.append("")
    lines.append("")

    # Placeholder href="#" links
    lines.append("## Placeholder `href=\"#\"` and empty hrefs")
    lines.append("These render as visible but unclickable links. Often used in gated items where the real target lives in `data-href`. Worth scanning to confirm intent.")
    if not placeholder_links:
        lines.append("None.")
    else:
        for f in sorted(placeholder_links):
            count = len(placeholder_links[f])
            lines.append(f"- **{f}** has {count} placeholder href")
    lines.append("")

    # data-href summary
    lines.append("## data-href (gated link) targets")
    if not data_href_targets:
        lines.append("None.")
    else:
        for f in sorted(data_href_targets):
            lines.append(f"### {f}")
            for link, ok in data_href_targets[f]:
                mark = "OK" if ok else ("MISSING" if ok is False else "skip")
                lines.append(f"- [{mark}] `{link}`")
            lines.append("")

    # External links (unique, summarised)
    lines.append("## External links (unique by domain)")
    domain_links = defaultdict(set)
    for f, links in external_links.items():
        for u in links:
            try:
                parsed = urllib.parse.urlparse(u)
                dom = parsed.netloc.lower() or "(unparsed)"
            except Exception:
                dom = "(error)"
            domain_links[dom].add(u)
    if not domain_links:
        lines.append("None.")
    else:
        for dom in sorted(domain_links):
            urls = domain_links[dom]
            lines.append(f"### {dom} ({len(urls)} unique URL{'s' if len(urls)!=1 else ''})")
            for u in sorted(urls):
                lines.append(f"- {u}")
            lines.append("")

    report = "\n".join(lines)
    report_path = os.path.join(ROOT, "scripts", "audit_report.md")
    with open(report_path, "w", encoding="utf-8") as fh:
        fh.write(report)
    print(report)
    print()
    print(f"Report written to {report_path}")

if __name__ == "__main__":
    main()
