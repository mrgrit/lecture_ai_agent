# -*- coding: utf-8 -*-
"""Assemble the four Korean course modules into one static HTML page."""
import re
import html as H
import dia_m1, dia_m2, dia_m3, dia_m4

DIA = {}
for m in (dia_m1, dia_m2, dia_m3, dia_m4):
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
]

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
    cap = ('<figcaption><span class="fig-no">그림 %d.</span> %s '
           '<span class="fig-src">원본 도판: <code>%s</code></span></figcaption>'
           % (FIGNO[0], esc(d.get("제목", "")), esc(d.get("원본", ""))))
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


def convert(md, mod):
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
            out.append("<h4>%s</h4>" % inline(ln[4:].strip()))
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

    # quiz block → details/summary
    quiz = re.search(r"## 이해도 점검\n(.*?)(?=\n## |\Z)", md_rest, re.S)
    quiz_html = ""
    if quiz:
        qs = re.findall(
            r"\*\*Q?\d+\.\s*(.+?)\*\*\s*\n+\s*답[:：]\s*(.+?)(?=\n\s*\*\*Q?\d+\.|\Z)",
            quiz.group(1), re.S)
        items = []
        for q, a in qs:
            items.append('<details><summary>%s</summary><div class="answer">%s</div></details>'
                         % (inline(" ".join(q.split())), inline(" ".join(a.split()))))
        quiz_html = '<div class="quiz">%s</div>' % "".join(items)
        assert len(items) >= 5, (mod["file"], len(items))
        md_rest = md_rest.replace(quiz.group(0), "\n## 이해도 점검\n@@QUIZ@@\n")

    # exercises → cards (title may sit on the same line as the body)
    ex = re.search(r"## 실습 과제\n(.*?)(?=\n## |\Z)", md_rest, re.S)
    ex_html = ""
    if ex:
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
        ex_html = "".join(cards)
        assert len(blocks) >= 2, (mod["file"], len(blocks))
        md_rest = md_rest.replace(ex.group(0), "\n## 실습 과제\n@@EX@@\n")

    body, toc = convert(md_rest, mod)
    body = body.replace("<p>@@QUIZ@@</p>", quiz_html).replace("<p>@@EX@@</p>", ex_html)

    obj_html = ""
    if obj_items:
        obj_html = ('<div class="objectives"><h3>학습 목표</h3><ul>%s</ul></div>'
                    % "".join("<li>%s</li>" % inline(x) for x in obj_items))

    head = (
        '<section class="module %s" id="mod%d">'
        '<div class="mod-head"><span class="mod-chip">MODULE %d</span>'
        '<h2 class="mod-title">%s</h2><p class="mod-lede">%s</p>'
        '<p class="mod-src">원자료: <a href="%s" target="_blank" rel="noopener">%s</a> '
        '— 아래 본문은 이 문서의 개념을 한국어로 요약·재구성한 학습 자료다.</p></div>%s%s'
        '<hr class="mod-end"></section>'
        % (mod["cls"], mod["n"], mod["n"], esc(title), esc(mod["lede"]),
           mod["src"], esc(mod["srcname"]), obj_html, body))
    return head, toc, title


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
    tpl = tpl.replace("<!-- TOC-PLACEHOLDER -->", "".join(tocs))
    tpl = tpl.replace("<!-- MAP-PLACEHOLDER -->", "".join(cards))
    for k, b in enumerate(bodies):
        tpl = tpl.replace("<!-- MODULE-%d -->" % (k + 1), b)
    open("../index.html", "w", encoding="utf-8").write(tpl)
    print("index.html", len(tpl), "bytes ·", FIGNO[0], "figures")


if __name__ == "__main__":
    main()
