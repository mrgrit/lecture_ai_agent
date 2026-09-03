# -*- coding: utf-8 -*-
"""Static checks: XML well-formedness, CSS class/token coverage, viewBox bounds, text collisions."""
import re, sys, xml.etree.ElementTree as ET
import dia_m1, dia_m2, dia_m3, dia_m4, dia_m5, dia_lab, dia_labcc

DIA = {}
for m in (dia_m1, dia_m2, dia_m3, dia_m4, dia_m5, dia_lab, dia_labcc):
    DIA.update(m.D)

css = open("template.html", encoding="utf-8").read()
defined = set(re.findall(r"\.(d-[a-z0-9-]+)", css)) | set(re.findall(r"\.(dia)\b", css))
tokens = set(re.findall(r"(--[a-z0-9-]+)\s*:", css))
used_tokens = set(re.findall(r"var\((--[a-z0-9-]+)", css))
fail = 0

# 1) XML well-formedness + class coverage + bounds
NS = "{http://www.w3.org/2000/svg}"
for uid, s in sorted(DIA.items()):
    try:
        root = ET.fromstring(s)
    except ET.ParseError as e:
        print("XML FAIL %-24s %s" % (uid, e)); fail += 1; continue
    for cl in re.findall(r'class="([^"]+)"', s):
        for c in cl.split():
            if c.startswith("d-") and c not in defined:
                print("CLASS  FAIL %-24s undefined .%s" % (uid, c)); fail += 1
    vb = [float(x) for x in root.get("viewBox").split()]
    W, H = vb[2], vb[3]
    for el in root.iter():
        t = el.tag[len(NS):] if el.tag.startswith(NS) else el.tag
        if t == "rect":
            x, y = float(el.get("x", 0)), float(el.get("y", 0))
            w, h = float(el.get("width", 0)), float(el.get("height", 0))
            if x < -0.5 or y < -0.5 or x + w > W + 0.5 or y + h > H + 0.5:
                print("BOUNDS FAIL %-24s rect %.1f,%.1f %.1fx%.1f > %gx%g" % (uid, x, y, w, h, W, H))
                fail += 1

for t in sorted(used_tokens - tokens):
    print("TOKEN  FAIL undefined %s" % t); fail += 1

# 2) text bounds + pairwise collisions
def tw(s, size):
    w = 0.0
    for ch in s:
        o = ord(ch)
        if o >= 0x1100: w += size
        elif ch in " .,:;'|!ilj()[]": w += size * .31
        elif ch.isdigit(): w += size * .56
        elif ch.isupper(): w += size * .65
        else: w += size * .54
    return w

for uid, s in sorted(DIA.items()):
    root = ET.fromstring(s)
    vb = [float(x) for x in root.get("viewBox").split()]
    W, H = vb[2], vb[3]
    boxes = []
    rotated = set()
    for g in root.iter(NS + 'g'):
        if 'rotate' in (g.get('transform') or ''):
            rotated.update(id(c) for c in g.iter())
    for el in root.iter():
        t = el.tag[len(NS):] if el.tag.startswith(NS) else el.tag
        if t != "text" or not (el.text or "").strip() or id(el) in rotated:
            continue
        # skip rotated groups (parent transform) — handled visually
        size = float(el.get("font-size", 11))
        x, y = float(el.get("x", 0)), float(el.get("y", 0))
        w = tw(el.text, size)
        a = el.get("text-anchor", "start")
        x0 = x - w / 2 if a == "middle" else (x - w if a == "end" else x)
        b = (x0, y - size * .78, x0 + w, y + size * .24, el.text)
        boxes.append(b)
        if b[0] < -1 or b[2] > W + 1 or b[1] < -1 or b[3] > H + 1:
            print("TEXT   FAIL %-24s '%s' out of %gx%g by %.1f" %
                  (uid, el.text[:26], W, H, max(-b[0], b[2] - W, -b[1], b[3] - H)))
            fail += 1
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            a, b = boxes[i], boxes[j]
            ox = min(a[2], b[2]) - max(a[0], b[0])
            oy = min(a[3], b[3]) - max(a[1], b[1])
            if ox > 2.5 and oy > 2.5:
                print("OVERLAP FAIL %-22s '%s' × '%s' (%.1f×%.1f)" %
                      (uid, a[4][:20], b[4][:20], ox, oy))
                fail += 1

print("\n%d diagrams checked · %d problems" % (len(DIA), fail))
sys.exit(1 if fail else 0)
