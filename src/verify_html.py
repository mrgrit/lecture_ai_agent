# -*- coding: utf-8 -*-
"""Page-level checks on index.html: placeholders, anchors, lab cards, CSS coverage."""
import re
import sys

html = open("../index.html", encoding="utf-8").read()
css = html.split("</style>")[0]
fail = []


def bad(m):
    fail.append(m)
    print("FAIL " + m)


for ph in ("@@QUIZ@@", "@@EX@@", "@@INDEX@@", "PLACEHOLDER", "<!-- MODULE-",
           "<!-- LAB -->", "<!-- LABCC -->", "<!-- LABSTEP -->"):
    if ph in html:
        bad("leftover placeholder: %s" % ph)

ids = set(re.findall(r'\sid="([^"]+)"', html))
for href in sorted(set(re.findall(r'href="#([^"]+)"', html))):
    if href not in ids:
        bad("dangling anchor #%s" % href)

labs = re.findall(r'<section class="lab" id="(lab-[lcs]\d-\d+)"', html)
if len(labs) != 69:
    bad("expected 69 lab cards, found %d" % len(labs))
for pre, n in (("l", 23), ("c", 23), ("s", 23)):
    k = len([x for x in labs if x.startswith("lab-" + pre)])
    if k != n:
        bad("track %s: expected %d labs, found %d" % (pre.upper(), n, k))
if len(labs) != len(set(labs)):
    bad("duplicate lab ids")

defined = set(re.findall(r"\.([A-Za-z][\w-]*)", css))
used = set()
for attr in re.findall(r'class="([^"]+)"', html):
    used.update(attr.split())
for c in sorted(used - defined):
    if c.startswith(("d-", "lab", "mod", "toc", "fig", "m")):
        bad("class used but not defined: .%s" % c)

declared = set(re.findall(r"(--[\w-]+)\s*:", css))
for tok in sorted(set(re.findall(r"var\((--[\w-]+)", css))):
    if tok not in declared:
        bad("css var never declared: %s" % tok)

for u in sorted(set(re.findall(r'(?:src|href)="(https?://[^"]+)"', html))):
    if not u.startswith(("https://agentfactory.panaversity.org",
                         "https://github.com/NousResearch",
                         "https://hermes-agent.nousresearch.com",
                         "https://claude.com/claude-code",
                         "https://claude.ai/install.sh")):
        bad("unexpected external reference: %s" % u)
if re.search(r'<(script|link)[^>]+(src|href)="https?://', html):
    bad("external asset reference (CSP unsafe)")

meta = html.count('<div class="lab-meta">')
if meta != len(labs):
    bad("lab-meta strips: %d (expected %d)" % (meta, len(labs)))

print("\nfigures %d · labs %d · quiz %d · exercises %d · tables %d · %d bytes"
      % (html.count('<figure class="diagram"'), len(labs),
         html.count("<details>"), html.count('class="exercise"'),
         html.count("<table>"), len(html.encode())))
print("RESULT: %s (%d problems)" % ("OK" if not fail else "PROBLEMS", len(fail)))
sys.exit(1 if fail else 0)
