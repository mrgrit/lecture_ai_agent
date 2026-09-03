# -*- coding: utf-8 -*-
"""lab-claude-code.md 에서 실습 카드별 bash 블록을 순서대로 뽑아 낸다."""
import json
import re

SKIP = ("claude.ai/install.sh",)          # 이미 설치돼 있으므로 건너뛴다

md = open("modules/lab-claude-code.md", encoding="utf-8").read()
lines = md.split("\n")

labs, cur, fenced, lang, buf = [], None, False, "", []
for ln in lines:
    if ln.startswith("```"):
        if not fenced:
            fenced, lang, buf = True, ln[3:].strip(), []
        else:
            fenced = False
            if lang == "bash" and cur is not None:
                code = "\n".join(buf)
                if not any(s in code for s in SKIP):
                    cur["blocks"].append(code)
        continue
    if fenced:
        buf.append(ln)
        continue
    m = re.match(r"^## (C\d-\d+)\.\s*(.+)$", ln)
    if m:
        cur = {"lab": m.group(1), "title": m.group(2), "blocks": []}
        labs.append(cur)
        continue
    if ln.startswith("## 마치며"):
        cur = {"lab": "C-END", "title": "마치며", "blocks": []}
        labs.append(cur)
        continue
    if ln.startswith("## 이해도 점검"):
        cur = None

# 'claude' 단독 실행(대화형 로그인 안내)은 제외한다
for l in labs:
    l["blocks"] = [b for b in l["blocks"] if b.strip() != "claude"]

# 자리표시자가 든 블록은 복사·붙여넣기로 돌지 않는다. 있으면 즉시 실패시킨다.
BAD = ('"..."', "<질문", "<위에서", "<세션", "<잡 ", "<이름", "<PATH")
for l in labs:
    for i, b in enumerate(l["blocks"]):
        for pat in BAD:
            assert pat not in b, "%s 블록%d 에 자리표시자 %r 이 있다" % (l["lab"], i, pat)

json.dump(labs, open("cclabcmds.json", "w"), ensure_ascii=False, indent=1)
print("실습 %d개 · bash 블록 %d개" % (len(labs), sum(len(l["blocks"]) for l in labs)))
for l in labs:
    print("  %-6s %2d블록  %s" % (l["lab"], len(l["blocks"]), l["title"][:44]))
