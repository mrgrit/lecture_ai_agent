# -*- coding: utf-8 -*-
"""caps/*.txt 를 문서의 @@CAP:이름@@ 자리에 끼워 넣는다."""
import pathlib
import re
import sys

S = pathlib.Path(__file__).resolve().parent
md = S / "modules" / "lab-cc-steps.md"
t = md.read_text(encoding="utf-8")
missing, done = [], 0
for m in sorted(set(re.findall(r"@@CAP:([a-z0-9-]+)@@", t))):
    f = S / "caps" / (m + ".txt")
    if not f.exists() or not f.read_text(encoding="utf-8").strip():
        missing.append(m)
        continue
    t = t.replace("@@CAP:%s@@" % m, f.read_text(encoding="utf-8").rstrip())
    done += 1
md.write_text(t, encoding="utf-8")
print("끼워 넣음 %d개 · 아직 없음 %s" % (done, missing or "없음"))
sys.exit(1 if missing else 0)
