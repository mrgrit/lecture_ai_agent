# -*- coding: utf-8 -*-
"""Assemble the four Korean course modules into one static HTML page."""
import re
import html as H
import dia_m1, dia_m2, dia_m3, dia_m4, dia_m5, dia_lab, dia_labcc

DIA = {}
for m in (dia_m1, dia_m2, dia_m3, dia_m4, dia_m5, dia_lab, dia_labcc):
    DIA.update(m.D)

MODS = [
    dict(n=1, cls="m1", file="modules/module1-skills-connectors.md",
         short="스킬과 커넥터",
         lede="AI에게 한 번 가르쳐 두고, 내 앱과 데이터에 연결한다. 프로그래밍 없이 시작하는 에이전트 활용의 기초.",
         src="https://agentfactory.panaversity.org/docs/skills-connectors-crash-course",
         srcname="Skills & Connectors Crash Course"),
    dict(n=2, cls="m2", file="modules/module2-harness-engineering.md",
         short="하니스 엔지니어링",
         lede="같은 모델이 왜 어떤 날은 성공하고 어떤 날은 테스트를 지워 버리는가. 모델을 신뢰할 수 있는 에이전트로 만드는 층을 설계한다.",
         src="https://agentfactory.panaversity.org/docs/harness-engineering-crash-course",
         srcname="Harness Engineering Crash Course"),
    dict(n=3, cls="m3", file="modules/module3-loop-engineering.md",
         short="루프 엔지니어링",
         lede="사람이 매번 시동을 거는 대화에서, 스스로 깨어나 일하고 검증하고 기억하는 루프로. 자율 실행의 설계법.",
         src="https://agentfactory.panaversity.org/docs/loop-engineering-crash-course",
         srcname="Loop Engineering Crash Course"),
    dict(n=4, cls="m4", file="modules/module4-graph-engineering.md",
         short="그래프 엔지니어링",
         lede="에이전트는 잊지만 그래프는 잊지 않는다. 여러 에이전트가 공유하는, 출처가 딸린 기억을 만든다.",
         src="https://agentfactory.panaversity.org/docs/graph-engineering-crash-course",
         srcname="Graph Engineering Crash Course"),
    dict(n=5, cls="m5", file="modules/module5-spec-driven-development.md",
         short="명세 주도 개발",
         lede="어떻게를 만들기 전에 무엇을 합의한다. 네 모듈이 '어떻게'를 다뤘다면 이 모듈은 그 앞에 오는 '무엇을'을 다룬다.",
         src="https://agentfactory.panaversity.org/docs/spec-driven-development-crash-course",
         srcname="Spec-Driven Development Crash Course"),
]

LABS = [
    dict(n=6, cls="m6", file="modules/lab-hermes.md", pre="L",
         short="실습편 · Hermes",
         lede="설치부터 근거 검증기까지, 스물세 개의 실습으로 다섯 모듈을 손으로 확인한다. 학교 GPU 서버의 로컬 모델을 쓰므로 학생 부담이 없다.",
         tool='사용 도구: <a href="https://github.com/NousResearch/hermes-agent" '
              'target="_blank" rel="noopener">Hermes Agent</a> (Nous Research, 오픈소스) '
              '— 아래 모든 명령과 기대 결과는 Hermes 0.20.0 · qwen3.8:27b 환경에서 실제로 실행해 확인한 것이다.'),
    dict(n=7, cls="m7", file="modules/lab-claude-code.md", pre="C",
         short="실습편 · Claude Code",
         lede="같은 스물세 개를 Claude Code로 한 번 더. 번호까지 일대일로 맞췄으므로 두 트랙을 나란히 비교할 수 있다.",
         tool='사용 도구: <a href="https://claude.com/claude-code" '
              'target="_blank" rel="noopener">Claude Code</a> (Anthropic) '
              '— 아래 모든 명령과 기대 결과는 Claude Code 2.1.259 · claude-haiku-4-5 환경에서 실제로 실행해 확인한 것이다.'),
]

# 각 모듈 상단 배너에 걸 실습 링크 (모듈 번호 → [(lab id, 라벨), ...])
MOD_LABS = {
    1: [("1-1", "첫 스킬 만들고 발동 증명하기"),
        ("1-2", "스킬끼리 관계 맺기"),
        ("1-3", "커넥터 직접 만들어 붙이기"),
        ("1-4", "모델을 바꾸면 얼마나 좋아지나")],
    2: [("2-1", "승인 사다리 판정해 보기"),
        ("2-2", "폴더 규칙으로 제약 걸기"),
        ("2-3", "위험한 명령 막는 훅"),
        ("2-4", "테스트 게이트"),
        ("2-5", "공급망 감사")],
    3: [("3-1", "조용한 하트비트"),
        ("3-2", "변화가 있을 때만 깨우기"),
        ("3-3", "이어서 하는 루프"),
        ("3-4", "비용을 숫자로 보기")],
    4: [("4-1", "세션을 넘는 기억"),
        ("4-2", "기억·발자국 그래프 열어 보기"),
        ("4-3", "근거 검증기 만들기")],
    5: [("5-1", "명세 있을 때와 없을 때"),
        ("5-2", "AI가 나를 인터뷰하게 하기"),
        ("5-3", "수용 기준을 게이트에 연결"),
        ("5-4", "명세 표류 만들고 잡기")],
}

FIGNO = [0]


def esc(s):
    return H.escape(s, quote=False)


def inline(s):
    """Markdown inline: code, bold, links."""
    out, i, n = [], 0, len(s)
    while i < n:
        c = s[i]
        if c == "`":
            j = s.find("`", i + 1)
            if j > 0:
                out.append("<code>%s</code>" % H.escape(s[i + 1:j]))
                i = j + 1
                continue
        if s.startswith("**", i):
            j = s.find("**", i + 2)
            if j > 0:
                out.append("<strong>%s</strong>" % inline(s[i + 2:j]))
                i = j + 2
                continue
        if c == "[":
            m = re.match(r"\[([^\]]+)\]\(([^)]+)\)", s[i:])
            if m:
                out.append('<a href="%s" target="_blank" rel="noopener">%s</a>'
                           % (H.escape(m.group(2), quote=True), inline(m.group(1))))
                i += m.end()
                continue
        out.append(esc(c))
        i += 1
    return "".join(out)


def figure(block, mod):
    d = dict(re.findall(r"^(id|원본|제목|내용): (.*)$", block, re.M))
    uid = d.get("id", "")
    if uid not in DIA:
        return ""
    FIGNO[0] += 1
    src = d.get("원본", "")
    if src.startswith("("):          # 실습편 그림은 대응하는 원본 도판이 없다
        src_html = '<span class="fig-src">이 강좌에서 새로 작도한 그림</span>'
    elif src.lower().endswith((".png", ".jpg", ".jpeg", ".webp", ".svg")):
        src_html = '<span class="fig-src">원본 도판: <code>%s</code></span>' % esc(src)
    else:                            # 파일명을 확인할 수 없는 원문 삽화
        src_html = '<span class="fig-src">원본 도판: %s</span>' % esc(src)
    cap = ('<figcaption><span class="fig-no">그림 %d.</span> %s %s</figcaption>'
           % (FIGNO[0], esc(d.get("제목", "")), src_html))
    return ('<figure class="diagram" id="fig-%s"><div class="fig-scroll">%s</div>%s</figure>'
            % (uid, DIA[uid], cap))


def render_table(rows):
    out = ['<div class="tbl-wrap"><table>']
    head = rows[0]
    out.append("<thead><tr>%s</tr></thead><tbody>"
               % "".join("<th>%s</th>" % inline(c) for c in head))
    for r in rows[2:]:
        out.append("<tr>%s</tr>" % "".join("<td>%s</td>" % inline(c) for c in r))
    out.append("</tbody></table></div>")
    return "".join(out)


def split_row(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def convert(md, mod, sub_tag="h4"):
    """Markdown → HTML for one module body. Returns (html, [(id,title)])."""
    lines = md.split("\n")
    out, toc = [], []
    i, n = 0, len(lines)
    sec = 0
    while i < n:
        ln = lines[i]
        # diagram block
        if ln.strip() == ":::diagram":
            j = i + 1
            buf = []
            while j < n and lines[j].strip() != ":::":
                buf.append(lines[j])
                j += 1
            out.append(figure("\n".join(buf), mod))
            i = j + 1
            continue
        # fenced code
        if ln.startswith("```"):
            j = i + 1
            buf = []
            while j < n and not lines[j].startswith("```"):
                buf.append(lines[j])
                j += 1
            out.append("<pre><code>%s</code></pre>" % H.escape("\n".join(buf)))
            i = j + 1
            continue
        # headings
        if ln.startswith("## "):
            t = ln[3:].strip()
            sec += 1
            sid = "m%d-s%d" % (mod["n"], sec)
            toc.append((sid, t))
            m = re.match(r"^(\d+)\.\s*(.+)$", t)
            if m:
                out.append('<h3 class="lesson" id="%s"><span class="no">%s</span>'
                           '<span>%s</span></h3>' % (sid, m.group(1), inline(m.group(2))))
            else:
                out.append('<h3 class="lesson plain" id="%s"><span>%s</span></h3>'
                           % (sid, inline(t)))
            i += 1
            continue
        if ln.startswith("### "):
            out.append("<%s>%s</%s>" % (sub_tag, inline(ln[4:].strip()), sub_tag))
            i += 1
            continue
        if ln.startswith("> "):          # lab meta strip lines are pulled out earlier
            i += 1
            continue
        if ln.startswith("# "):
            i += 1
            continue
        if ln.strip() == "---":
            i += 1
            continue
        # table
        if ln.startswith("|"):
            rows = []
            while i < n and lines[i].startswith("|"):
                rows.append(split_row(lines[i]))
                i += 1
            out.append(render_table(rows))
            continue
        # list
        if re.match(r"^\s*[-*]\s+", ln):
            items = []
            while i < n and re.match(r"^\s*[-*]\s+", lines[i]):
                items.append(re.sub(r"^\s*[-*]\s+", "", lines[i]))
                i += 1
            out.append("<ul>%s</ul>" % "".join("<li>%s</li>" % inline(x) for x in items))
            continue
        if re.match(r"^\s*\d+\.\s+", ln):
            items = []
            while i < n and re.match(r"^\s*\d+\.\s+", lines[i]):
                items.append(re.sub(r"^\s*\d+\.\s+", "", lines[i]))
                i += 1
            out.append("<ol>%s</ol>" % "".join("<li>%s</li>" % inline(x) for x in items))
            continue
        if not ln.strip():
            i += 1
            continue
        # paragraph
        buf = [ln]
        i += 1
        while i < n and lines[i].strip() and not re.match(
                r"^(#|\||```|:::|\s*[-*]\s|\s*\d+\.\s|---$)", lines[i]):
            buf.append(lines[i])
            i += 1
        out.append("<p>%s</p>" % inline(" ".join(x.strip() for x in buf)))
    return "".join(out), toc


def extract_quiz(md_rest, where, minimum=5):
    """Pull the 이해도 점검 block out and render it as details/summary cards."""
    quiz = re.search(r"## 이해도 점검\n(.*?)(?=\n## |\Z)", md_rest, re.S)
    if not quiz:
        return md_rest, ""
    qs = re.findall(
        r"\*\*Q?\d+\.\s*(.+?)\*\*\s*\n+\s*답[:：]\s*(.+?)(?=\n\s*\*\*Q?\d+\.|\Z)",
        quiz.group(1), re.S)
    items = ['<details><summary>%s</summary><div class="answer">%s</div></details>'
             % (inline(" ".join(q.split())), inline(" ".join(a.split()))) for q, a in qs]
    assert len(items) >= minimum, (where, len(items))
    md_rest = md_rest.replace(quiz.group(0), "\n## 이해도 점검\n@@QUIZ@@\n")
    return md_rest, '<div class="quiz">%s</div>' % "".join(items)


def extract_exercises(md_rest, where, minimum=2):
    """Pull the 실습 과제 block out and render it as cards."""
    ex = re.search(r"## 실습 과제\n(.*?)(?=\n## |\Z)", md_rest, re.S)
    if not ex:
        return md_rest, ""
    raw = ex.group(1)
    first = re.search(r"\*\*과제 \d+\.", raw)
    lead = raw[:first.start()].strip() if first else ""
    blocks = re.findall(r"\*\*과제 (\d+)\.\s*(.+?)\*\*\s*(.*?)(?=\n\s*\*\*과제 \d+\.|\Z)",
                        raw, re.S)
    cards = []
    if lead:
        cards.append("<p>%s</p>" % inline(" ".join(lead.split())))
    for num, head, body in blocks:
        cards.append('<div class="exercise"><div class="ex-no">과제 %s</div>'
                     '<h4>%s</h4><p>%s</p></div>'
                     % (num, inline(head.strip().rstrip(".")),
                        inline(" ".join(body.split()))))
    assert len(blocks) >= minimum, (where, len(blocks))
    md_rest = md_rest.replace(ex.group(0), "\n## 실습 과제\n@@EX@@\n")
    return md_rest, "".join(cards)


def build_module(mod):
    md = open(mod["file"], encoding="utf-8").read()
    title = re.search(r"^# (.+)$", md, re.M).group(1)
    title = re.sub(r"^모듈 \d+\.\s*", "", title)

    # objectives block
    obj = re.search(r"## 학습 목표\n(.*?)(?=\n## )", md, re.S)
    obj_items = re.findall(r"^- (.+)$", obj.group(1), re.M) if obj else []
    md_rest = md
    if obj:
        md_rest = md.replace(obj.group(0), "")

    md_rest, quiz_html = extract_quiz(md_rest, mod["file"])
    md_rest, ex_html = extract_exercises(md_rest, mod["file"])

    body, toc = convert(md_rest, mod)
    body = body.replace("<p>@@QUIZ@@</p>", quiz_html).replace("<p>@@EX@@</p>", ex_html)

    obj_html = ""
    if obj_items:
        obj_html = ('<div class="objectives"><h3>학습 목표</h3><ul>%s</ul></div>'
                    % "".join("<li>%s</li>" % inline(x) for x in obj_items))

    labs = MOD_LABS.get(mod["n"], [])
    lab_html = ""
    if labs:
        rows = []
        for lab in LABS:
            pre = lab["pre"]
            links = "".join('<a href="#lab-%s%s">%s%s %s</a>'
                            % (pre.lower(), i, pre, i, esc(t)) for i, t in labs)
            rows.append('<p class="mod-labs %s"><span class="t">%s로 →</span>%s</p>'
                        % (lab["cls"], esc(lab["short"].split(" · ")[-1]), links))
        lab_html = "".join(rows)

    head = (
        '<section class="module %s" id="mod%d">'
        '<div class="mod-head"><span class="mod-chip">MODULE %d</span>'
        '<h2 class="mod-title">%s</h2><p class="mod-lede">%s</p>'
        '<p class="mod-src">원자료: <a href="%s" target="_blank" rel="noopener">%s</a> '
        '— 아래 본문은 이 문서의 개념을 한국어로 요약·재구성한 학습 자료다.</p>%s</div>%s%s'
        '<hr class="mod-end"></section>'
        % (mod["cls"], mod["n"], mod["n"], esc(title), esc(mod["lede"]),
           mod["src"], esc(mod["srcname"]), lab_html, obj_html, body))
    return head, toc, title


# ------------------------------------------------------------------ lab track

META_ICONS = {"대응": "대응", "소요": "소요", "선행": "선행", "확인": "확인"}


def lab_card(head_line, body_md, mod):
    """One `## Lx-y. 제목` block → a lab card."""
    m = re.match(r"^([LC]\d-\d+)\.\s*(.+)$", head_line)
    lid, title = m.group(1), m.group(2)
    anchor = "lab-" + lid.lower()

    rows = re.findall(r"^>\s*(\S+)\s*\|\s*(.+?)\s*$", body_md, re.M)
    body_md = re.sub(r"^>\s*\S+\s*\|.*$", "", body_md, flags=re.M)
    meta = ""
    if rows:
        meta = ('<div class="lab-meta">%s</div>'
                % "".join('<div class="row"><span class="k">%s</span>'
                          '<span class="v">%s</span></div>'
                          % (esc(META_ICONS.get(k, k)), inline(v)) for k, v in rows))

    body, _ = convert(body_md, mod, sub_tag="h5")
    return ('<section class="lab" id="%s"><h4 class="lab-h">'
            '<span class="lid">%s</span><span>%s</span></h4>%s%s</section>'
            % (anchor, esc(lid), inline(title), meta, body)), anchor, lid, title


def build_lab(mod):
    md = open(mod["file"], encoding="utf-8").read()
    title = re.search(r"^# (.+)$", md, re.M).group(1)
    title = re.sub(r"^실습편\.\s*", "", title)

    md_rest, quiz_html = extract_quiz(md, mod["file"], minimum=6)
    md_rest, ex_html = extract_exercises(md_rest, mod["file"], minimum=3)

    # split at every `## ` heading — but never inside a fenced code block
    # (SKILL.md heredocs in the labs contain their own `## ` lines)
    parts, cur, fenced = [], None, False
    for ln in md_rest.split("\n"):
        if ln.startswith("```"):
            fenced = not fenced
        if not fenced and ln.startswith("## "):
            cur = [ln[3:]]
            parts.append(cur)
            continue
        if cur is not None:
            cur.append(ln)
    parts = ["\n".join(p) for p in parts]
    out, toc, index, sec = [], [], [], 0
    for part in parts:
        head_line, _, rest = part.partition("\n")
        head_line = head_line.strip()
        if re.match(r"^[LC]\d-\d+\.", head_line):
            html, anchor, lid, ltitle = lab_card(head_line, rest, mod)
            out.append(html)
            index.append((anchor, lid, ltitle))
            continue
        sec += 1
        sid = "m%d-s%d" % (mod["n"], sec)
        toc.append((sid, re.sub(r"\s+—.*$", "", head_line)))
        cls = "lab-group" if re.match(r"^실습 \d", head_line) else "lesson plain"
        out.append('<h3 class="%s" id="%s"><span>%s</span></h3>' % (cls, sid, inline(head_line)))
        body, _ = convert(rest, mod)
        body = body.replace("<p>@@QUIZ@@</p>", quiz_html).replace("<p>@@EX@@</p>", ex_html)
        out.append(body)

    idx_html = ('<div class="tbl-wrap"><table><thead><tr><th>번호</th><th>실습</th></tr></thead>'
                '<tbody>%s</tbody></table></div>'
                % "".join('<tr><td><a href="#%s">%s</a></td><td>%s</td></tr>'
                          % (a, esc(l), inline(t)) for a, l, t in index))
    body = "".join(out).replace("@@INDEX@@", idx_html)

    head = (
        '<section class="module %s" id="mod%d">'
        '<div class="mod-head"><span class="mod-chip">LAB TRACK</span>'
        '<h2 class="mod-title">%s</h2><p class="mod-lede">%s</p>'
        '<p class="mod-src">%s</p>'
        '</div>%s<hr class="mod-end"></section>'
        % (mod["cls"], mod["n"], esc(title), esc(mod["lede"]), mod["tool"], body))
    return head, toc, title, index


def main():
    tpl = open("template.html", encoding="utf-8").read()
    bodies, tocs, cards = [], [], []
    for mod in MODS:
        h, toc, title = build_module(mod)
        bodies.append(h)
        links = "".join('<li><a href="#%s">%s</a></li>' % (i, esc(t)) for i, t in toc)
        tocs.append('<div class="toc-mod %s"><a class="toc-mod-title" href="#mod%d">'
                    '<span class="dot"></span>%d. %s</a><ol>%s</ol></div>'
                    % (mod["cls"], mod["n"], mod["n"], esc(mod["short"]), links))
        cards.append('<a class="card %s" href="#mod%d"><span class="mod-no">MODULE %d</span>'
                     '<h3>%s</h3><p>%s</p></a>'
                     % (mod["cls"], mod["n"], mod["n"], esc(mod["short"]), esc(mod["lede"])))
    for lab, slot in zip(LABS, ("<!-- LAB -->", "<!-- LABCC -->")):
        lab_html, lab_toc, lab_title, lab_index = build_lab(lab)
        links = "".join('<li><a href="#%s">%s</a></li>' % (i, esc(t)) for i, t in lab_toc)
        tocs.append('<div class="toc-mod %s"><a class="toc-mod-title" href="#mod%d">'
                    '<span class="dot"></span>%s</a><ol>%s</ol></div>'
                    % (lab["cls"], lab["n"], esc(lab["short"]), links))
        cards.append('<a class="card %s" href="#mod%d">'
                     '<span class="mod-no">LAB TRACK · 실습 %d개</span>'
                     '<h3>%s</h3><p>%s</p></a>'
                     % (lab["cls"], lab["n"], len(lab_index),
                        esc(lab["short"]), esc(lab["lede"])))
        tpl = tpl.replace(slot, lab_html)

    tpl = tpl.replace("<!-- TOC-PLACEHOLDER -->", "".join(tocs))
    tpl = tpl.replace("<!-- MAP-PLACEHOLDER -->", "".join(cards))
    for k, b in enumerate(bodies):
        tpl = tpl.replace("<!-- MODULE-%d -->" % (k + 1), b)
    open("../index.html", "w", encoding="utf-8").write(tpl)
    print("index.html", len(tpl), "bytes ·", FIGNO[0], "figures")


if __name__ == "__main__":
    main()
