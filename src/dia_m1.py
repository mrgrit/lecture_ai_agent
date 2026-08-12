# -*- coding: utf-8 -*-
"""Module 1 diagrams — Skills & Connectors."""
from svglib import *   # noqa

W = 720
D = {}


def reg(uid, w, h, aria, body):
    D[uid] = svg(uid, w, h, aria, body)


# ---------------------------------------------------------------- 1. kitchen
def _kitchen():
    u, o = "kitchen-analogy", []
    pills = [("채팅 메시지", "이번 한 번, 무엇을"),
             ("Skill", "매번, 어떻게"),
             ("Connector", "실제 앱에 닿는 손")]
    for i, (t, s) in enumerate(pills):
        x = i * 244
        o.append(box(x, 4, 232, 50, t, [s], cls="d-accent" if i else "d-box", r=25))
    # left panel: connector = kitchen
    p, ix, iy, iw, _ = panel(0, 78, 350, 152, "Connector = 주방", "도구와 재료가 갖춰진 공간")
    o.append(p)
    for i, nm in enumerate(["Google Drive", "Gmail", "Slack", "이슈 트래커"]):
        bx = ix + (i % 2) * 160
        by = iy + 8 + (i // 2) * 42
        o.append(box(bx, by, 150, 34, nm, cls="d-box", tsize=11.5))
    # right panel: skill = recipe card
    p, ix, iy, iw, _ = panel(370, 78, 350, 152, "Skill = 레시피 카드", "우리 가게의 고유한 순서")
    o.append(p)
    for i, s in enumerate(["① 단위를 통일한다", "② 항목별로 묶는다",
                           "③ 기준 초과를 표시한다", "④ 지정 양식으로 낸다"]):
        o.append(text(ix + 4, iy + 20 + i * 21, s, 11.5, "start", "d-t"))
    o.append(arrow_a(175, 232, 300, 272, u))
    o.append(arrow_a(545, 232, 420, 272, u))
    o.append(box(160, 274, 400, 52, "둘이 합쳐지면",
                 ["내 방식대로, 매번 같은 품질"], cls="d-strong"))
    return "".join(o), 340


reg("kitchen-analogy", W, _kitchen()[1],
    "채팅 메시지·Skill·Connector 세 가지 역할과 주방 비유. 커넥터는 주방, 스킬은 레시피 카드이며 둘이 합쳐져야 같은 품질이 나온다.",
    _kitchen()[0])


# ---------------------------------------------------------------- 2. auto vs slash
def _auto():
    u, o = "auto-vs-slash", []
    steps = [("사용자가 평소 말로 작업을 설명한다", []),
             ("AI가 켜진 모든 스킬의 description을 훑는다", ["일치 여부만 판단"]),
             ("일치한 스킬이 스스로 로드되어 발동한다", ["명령어 불필요"])]
    for i, (t, s) in enumerate(steps):
        x = i * 257
        o.append(box(x, 8, 206, 88, t, s, cls="d-accent" if i == 2 else "d-box", tsize=11.5))
        o.append(numchip(x + 16, 22, i + 1))
        if i < 2:
            o.append(arrow_a(x + 208, 52, x + 255, 52, u))
    o.append(note(360, 122, "실제 사용의 약 90%가 이 자동 경로 — 그래서 날카로운 description이 핵심이다", W))
    o.append(line(0, 146, 720, 146, "d-rule", dash=True))
    o.append(hdr(360, 172, "특정 스킬을 강제로 지정하고 싶을 때"))
    o.append(box(0, 186, 350, 76, "말로 지목한다",
                 ["“내 브랜드-보이스 스킬을 써 줘”", "Claude.ai 포함 모든 환경에서 동작"]))
    o.append(box(370, 186, 350, 76, "슬래시( / )를 입력해 메뉴에서 고른다",
                 ["Cowork · Office 추가 기능에서 제공"]))
    return "".join(o), 276


reg("auto-vs-slash", W, _auto()[1],
    "스킬은 기본적으로 자동 발동한다. 사용자가 말로 작업을 설명하면 AI가 description을 훑어 일치하는 스킬을 스스로 로드하며, 이름 지목과 슬래시 명령은 강제 지정용 보조 수단이다.",
    _auto()[0])


# ---------------------------------------------------------------- 3. capabilities toggle
def _cap():
    u, o = "capabilities-toggle", []
    o.append('<rect x="0" y="0" width="640" height="226" rx="10" class="d-panel"/>')
    o.append(text(18, 30, "설정 (Settings)", 13.5, "start", "d-t", "700"))
    for i, (t, act) in enumerate([("General", 0), ("Capabilities", 1), ("Connectors", 0)]):
        x = 18 + i * 92
        if act:
            o.append('<rect x="%g" y="44" width="86" height="26" rx="6" class="d-accent"/>' % x)
        o.append(text(x + 43, 61, t, 11.5, "middle", "d-t" if act else "d-t d-dim",
                      "700" if act else None))
    o.append(line(18, 80, 622, 80, "d-rule"))
    # row 1 — on
    o.append(text(18, 106, "Code execution and file creation", 12.5, "start", "d-t", "700"))
    o.append(toggle(578, 95, True))
    o.append(text(18, 126, "코드를 실행하고 문서 · 스프레드시트 · 프레젠테이션 · PDF를 만들고 편집한다.",
                 11, "start", "d-t d-dim"))
    o.append(chip_c(78, 136, "스킬 사용에 필수", cls="d-chip-a", tcls="d-chip-a-t"))
    o.append(line(18, 168, 622, 168, "d-rule", dash=True))
    # row 2 — off
    o.append(text(18, 192, "Allow network egress", 12.5, "start", "d-t d-dim", "700"))
    o.append(toggle(578, 181, False))
    o.append(text(18, 210, "외부 네트워크로 나가는 통신을 허용한다. 기본은 꺼짐.",
                 11, "start", "d-t d-dim"))
    o.append(note(320, 250, "Skills 목록 관리는 이 화면이 아니라 Customize → Skills 메뉴에 있다", 640))
    return "".join(o), 264


reg("capabilities-toggle", 640, _cap()[1],
    "설정의 Capabilities 탭에서 Code execution and file creation 토글을 켜면 문서·표·슬라이드·PDF를 만드는 내장 스킬이 동작한다. 네트워크 송신 토글은 기본 꺼짐이다.",
    _cap()[0])


# ---------------------------------------------------------------- 4. skills shelf
def _shelf():
    u, o = "skills-shelf", []
    o.append('<rect x="0" y="0" width="720" height="252" rx="10" class="d-panel"/>')
    # left rail
    o.append(line(140, 12, 140, 240, "d-rule"))
    o.append('<rect x="10" y="20" width="120" height="28" rx="6" class="d-accent"/>')
    o.append(text(24, 39, "Skills", 12, "start", "d-t", "700"))
    o.append(text(24, 71, "Connectors", 12, "start", "d-t d-dim"))
    o.append(text(24, 99, "Plugins", 12, "start", "d-t d-dim"))
    o.append(text(24, 130, "Customize 메뉴", 10.5, "start", "d-t d-dim"))
    # list
    o.append(text(158, 30, "개인 스킬", 12.5, "start", "d-t", "700"))
    o.append(box(462, 16, 26, 22, "+", cls="d-accent", tsize=13))
    o.append(box(400, 44, 150, 52, None, cls="d-panel-2"))
    o.append(text(412, 62, "Browse skills", 11, "start", "d-t"))
    o.append(text(412, 84, "Create skill", 11, "start", "d-t"))
    o.append(box(158, 46, 220, 30, "skill-creator", cls="d-accent", tsize=11.5))
    for i, f in enumerate(["SKILL.md", "agents/", "assets/", "references/", "scripts/"]):
        o.append(text(184, 98 + i * 20, "└ " + f, 10.5, "start", "d-t d-dim"))
    # detail
    o.append(line(568, 12, 568, 240, "d-rule"))
    o.append(text(584, 30, "상세", 12, "start", "d-t", "700"))
    o.append(chip_c(640, 44, "Anthropic 관리", cls="d-chip"))
    o.append(text(584, 86, "트리거 방식", 10.5, "start", "d-t d-dim"))
    o.append(text(584, 104, "슬래시 명령 + 자동", 11, "start", "d-t"))
    o.append(note(360, 274, "Word · Excel · PowerPoint · PDF 스킬이 이 목록에 없는 것은 정상이다 — 그것들은 선반이 아니라 엔진 쪽(Capabilities)에 산다", W))
    return "".join(o), 300


reg("skills-shelf", W, _shelf()[1],
    "Customize의 Skills 화면. 새 계정에는 skill-creator 하나만 있고, + 버튼에서 Browse skills와 Create skill을 고를 수 있다. 오피스 파일 스킬은 이 목록이 아니라 Capabilities 토글에 들어 있다.",
    _shelf()[0])


# ---------------------------------------------------------------- 5. connectors directory
def _conn():
    u, o = "connectors-directory", []
    o.append('<rect x="0" y="0" width="720" height="212" rx="10" class="d-panel"/>')
    for i, (t, act) in enumerate([("Skills", 0), ("Connectors", 1), ("Plugins", 0)]):
        x = 16 + i * 88
        if act:
            o.append('<rect x="%g" y="14" width="82" height="26" rx="6" class="d-accent"/>' % x)
        o.append(text(x + 41, 31, t, 11.5, "middle", "d-t" if act else "d-t d-dim",
                      "700" if act else None))
    o.append(chip_c(348, 17, "Anthropic & Partners", cls="d-chip"))
    o.append(box(504, 14, 200, 26, "🔍  검색", cls="d-box", tsize=11, tweight=None))
    o.append(line(16, 54, 704, 54, "d-rule"))
    cards = ["Google Drive", "Gmail", "Slack", "Notion",
             "Figma", "Microsoft 365", "Atlassian", "Canva"]
    for i, nm in enumerate(cards):
        x = 16 + (i % 4) * 173
        y = 68 + (i // 4) * 68
        o.append(box(x, y, 163, 56, nm, cls="d-box", tsize=11.5))
        o.append(text(x + 150, y + 18, "+", 13, "middle", "d-t d-acc", "700"))
        if nm == "Figma":
            o.append(chip_c(x + 52, y + 32, "Interactive", cls="d-chip-a", tcls="d-chip-a-t", h=17))
    o.append(note(360, 236, "Interactive 배지가 붙은 커넥터는 텍스트 대신 대화 안에 라이브 보드·캔버스를 직접 그려 준다", W))
    return "".join(o), 252


reg("connectors-directory", W, _conn()[1],
    "커넥터 디렉터리 화면. Skills·Connectors·Plugins 탭 아래에 Google Drive, Gmail, Slack, Notion 등 기성 커넥터 카드가 격자로 진열되고 각 카드의 + 버튼으로 추가한다.",
    _conn()[0])


# ---------------------------------------------------------------- 6. together pipeline
def _together():
    u, o = "together-pipeline", []
    o.append(box(80, 6, 560, 50, "“내 Drive의 이번 달 장부로 거래처 월간 요약을 만들어 줘”",
                 ["한 문장짜리 요청"], cls="d-strong", tsize=12))
    stages = [("Connector — 실제 데이터를 가져온다",
               ["Drive의 장부 파일, Gmail의 지난 분기 자료"]),
              ("Skill — 내 방식대로 다듬는다",
               ["통화 표기 · 지출 항목별 묶음 · 기준 초과 표시 · 4개 섹션 양식"]),
              ("나 — 검토한다",
               ["두 시간짜리 붙여넣기 작업이 2분짜리 검토로"])]
    y = 92
    for i, (t, s) in enumerate(stages):
        o.append(arrow_a(360, y - 32, 360, y - 4, u))
        o.append(box(80, y, 560, 64, t, s, cls="d-accent" if i < 2 else "d-strong"))
        o.append(numchip(102, y + 20, i + 1))
        y += 96
    o.append(note(360, y - 6,
                  "한 문장이 들어가면, 한 번도 복사·붙여넣기하지 않은 실데이터로 완성된 결과물이 나온다", W))
    return "".join(o), y + 12


reg("together-pipeline", W, _together()[1],
    "커넥터가 실데이터를 가져오고 스킬이 그것을 내 방식대로 다듬으며 사람은 검토만 하는 3단 파이프라인. 한 문장 요청이 완성된 보고서가 되어 나온다.",
    _together()[0])


# ---------------------------------------------------------------- 7. which do I need
def _which():
    u, o = "which-do-i-need", []
    o.append(hdr(360, 16, "반복적이고 귀찮은 작업 — 마찰이 어디에 있는가?"))
    o.append(text(150, 48, "가로: 다른 앱에서 데이터를 매번 복사해 오는가?", 11, "start", "d-t d-dim"))
    o.append(box(150, 60, 280, 30, "아니오", cls="d-panel-2", tsize=11.5))
    o.append(box(440, 60, 280, 30, "예", cls="d-panel-2", tsize=11.5))
    o.append(box(0, 96, 140, 104, "‘어떻게’를", ["매번 다시", "설명하지 않는다"],
                 cls="d-panel-2", tsize=11.5))
    o.append(box(0, 208, 140, 104, "‘어떻게’를", ["매번 다시", "설명한다"],
                 cls="d-panel-2", tsize=11.5))
    cells = [(150, 96, "둘 다 아님", ["한 번뿐인 질문은", "좋은 프롬프트면 충분"], "d-box"),
             (440, 96, "Connector", ["장부 · 메일 · 지난주 티켓을", "가져오는 것이 마찰"], "d-accent"),
             (150, 208, "Skill", ["브랜드 말투 · 보고서 양식 ·", "SOAP 노트 · 체크리스트"], "d-accent"),
             (440, 208, "둘 다", ["실데이터를 내 방식으로 —", "월말 정산, 주간 콘텐츠 배치"], "d-strong")]
    for x, y, t, s, c in cells:
        o.append(box(x, y, 280, 104, t, s, cls=c, tsize=14))
    o.append(note(360, 336, "필요 없는 커넥터는 열어 둔 문이다. 워크플로가 실제로 쓰는 앱만 연결하라 — 범위(scope)가 곧 안전이다", W))
    return "".join(o), 352


reg("which-do-i-need", W, _which()[1],
    "느끼는 마찰로 진단하는 2×2 표. 방법을 매번 설명하면 Skill, 데이터를 매번 복사해 오면 Connector, 둘 다면 둘 다, 어느 쪽도 아니면 좋은 프롬프트 하나로 충분하다.",
    _which()[0])


# ---------------------------------------------------------------- 8. SKILL.md anatomy
def _anatomy():
    u, o = "skillmd-anatomy", []
    p, ix, iy, iw, _ = panel(0, 8, 320, 300, "lab-report-formatter/", "스킬 폴더 하나")
    o.append(p)
    blocks = [(iy + 4, 62, "frontmatter", ["name: lab-report-formatter", "description: …"], "d-accent"),
              (iy + 74, 108, "본문 (지침)", ["1. 단위를 SI로 통일한다", "2. 실험 항목별로 묶는다",
                                          "3. 오차 5% 초과를 표시한다", "4. 4개 섹션으로 출력한다"], "d-box"),
              (iy + 194, 62, "선택 폴더", ["references/  assets/  scripts/"], "d-panel-2")]
    for y, h, t, s, c in blocks:
        o.append(box(ix, y, iw, h, t, s, cls=c, tsize=11.5))
    levels = [(20, "레벨 1 — 항상 로드", ["name과 description만 유지한다.", "AI가 관련성을 판단하는 근거."]),
              (122, "레벨 2 — 요청이 일치할 때 로드", ["전체 지침을 그때 펼쳐 읽는다."]),
              (224, "레벨 3 — 필요한 순간에만 로드", ["참고 문서 · 템플릿 · 스크립트."])]
    for y, t, s in levels:
        o.append(box(400, y, 320, 84, t, s, cls="d-box", tsize=12))
    o.append(arrow_a(320, 78, 398, 62, u))
    o.append(arrow_a(320, 150, 398, 164, u))
    o.append(arrow_a(320, 250, 398, 266, u))
    o.append(note(360, 330, "progressive disclosure — 스킬을 수십 개 설치해도 대화가 느려지지 않는 이유", W))
    return "".join(o), 346


reg("skillmd-anatomy", W, _anatomy()[1],
    "SKILL.md의 세 부분과 progressive disclosure의 세 단계. frontmatter는 항상 로드되고, 본문은 요청이 일치할 때, 참고 폴더는 필요한 순간에만 로드된다.",
    _anatomy()[0])


# ---------------------------------------------------------------- 9. save skill
def _save():
    u, o = "save-skill", []
    p, ix, iy, iw, _ = panel(0, 8, 300, 208, "대화", "skill-creator가 작업을 마쳤다")
    o.append(p)
    o.append(box(ix, iy + 6, iw, 96, "lab-report-formatter",
                 ["주간 실습 보고서를", "학과 표준 양식으로 정리한다"], cls="d-box", tsize=12))
    o.append(box(ix + 78, iy + 116, 116, 30, "Save skill", cls="d-strong", tsize=11.5))
    p, ix2, iy2, iw2, _ = panel(330, 8, 390, 208, "lab-report-formatter / SKILL.md", "미리보기")
    o.append(p)
    for i, f in enumerate(["SKILL.md", "references/error-threshold.md", "scripts/unit_convert.py"]):
        o.append(text(ix2 + 4, iy2 + 20 + i * 22, "└ " + f, 11, "start", "d-t d-dim"))
    o.append(box(ix2, iy2 + 78, iw2, 56, "description",
                 ["“실습 보고서”, “주간 보고서” 요청 시 사용"], cls="d-accent", tsize=11))
    o.append(box(ix2 + 125, iy2 + 146, 112, 28, "Save skill", cls="d-strong", tsize=11.5))
    o.append(arrow_a(360, 226, 360, 256, u))
    o.append(box(110, 258, 500, 56, "개인 스킬 목록(Customize → Skills)에 추가",
                 ["‘Added by You’로 표시되고 즉시 켜진다 — 압축도 업로드도 필요 없다"],
                 cls="d-strong", tsize=12))
    return "".join(o), 328


reg("save-skill", W, _save()[1],
    "skill-creator가 만든 스킬은 Save skill 버튼 한 번으로 개인 스킬 목록에 추가되고 즉시 켜진다.",
    _save()[0])


# ---------------------------------------------------------------- 10. five surfaces
def _surf():
    u, o = "five-surfaces", []
    o.append(box(0, 20, 250, 110, "여기서 시작 — Claude.ai",
                 ["웹 · 모바일", "버튼과 토글만으로 전 과정 수행", "설치 불필요"], cls="d-strong"))
    o.append(arrow_a(252, 75, 336, 75, u, "필요해지면 이동"))
    p, ix, iy, iw, _ = panel(340, 10, 380, 130, "내 컴퓨터에서", "각 쌍의 앞은 상용, 뒤는 오픈소스")
    o.append(p)
    o.append(box(ix, iy + 6, iw, 38, "Cowork / OpenWork", ["비개발자용 데스크톱 — 내 실제 파일에 작업"],
                 cls="d-box", tsize=11.5))
    o.append(box(ix, iy + 52, iw, 38, "Claude Code / OpenCode", ["터미널 — 코드를 다루는 사람용"],
                 cls="d-box", tsize=11.5))
    o.append(box(0, 164, 350, 92, "이식 가능 — SKILL.md",
                 ["오픈 표준이라 같은 파일이", "OpenAI Codex CLI, Google Gemini CLI에서도 동작한다"],
                 cls="d-ok", tsize=12))
    o.append(box(370, 164, 350, 92, "이식 불가 — Custom GPT · Gem",
                 ["각각 ChatGPT와 Google 앱 안에서만 산다.", "한 도구만 쓴다면 충분하지만 옮겨 가지 않는다"],
                 cls="d-warn", tsize=12))
    return "".join(o), 270


reg("five-surfaces", W, _surf()[1],
    "Claude.ai에서 시작해 필요할 때 Cowork/OpenWork나 Claude Code/OpenCode로 옮겨 간다. SKILL.md는 오픈 표준이라 함께 이사 가지만 Custom GPT와 Gem은 해당 제품 안에서만 동작한다.",
    _surf()[0])
