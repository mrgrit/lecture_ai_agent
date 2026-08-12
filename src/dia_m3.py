# -*- coding: utf-8 -*-
"""Module 3 diagrams — Loop Engineering."""
from svglib import *   # noqa

W = 720
D = {}


def reg(uid, w, h, aria, body):
    D[uid] = svg(uid, w, h, aria, body)


# ------------------------------------------------- 1. prompting -> looping
def _shift():
    u, o = "shift-prompt-to-loop", []
    p, ix, iy, iw, _ = panel(0, 8, 340, 320, "턴 단위 프롬프팅", "사람이 모든 부품을 겸한다")
    o.append(p)
    steps = ["① 프롬프트 입력", "② 에이전트 응답", "③ 사람이 읽는다", "④ 다시 입력"]
    for i, s in enumerate(steps):
        y = iy + 8 + i * 52
        o.append(box(ix + 30, y, iw - 60, 38, s, cls="d-box", tsize=11.5))
        if i < 3:
            o.append(arrow(170, y + 40, 170, y + 50, u))
    o.append(path("M 44 %g C 12 %g 12 %g 44 %g" % (iy + 226, iy + 226, iy + 22, iy + 22), u, dash=True))
    o.append(text(24, iy + 130, "또 다시", 10, "middle", "d-t d-dim", halo=True))
    o.append(text(24, iy + 144, "사람", 10, "middle", "d-t d-dim", halo=True))
    o.append(note(170, 350, "사람이 하트비트 · 검증자 · 기억 장치를 전부 겸한다", 320, cls="d-t d-bad"))
    p, ix, iy, iw, _ = panel(360, 8, 360, 320, "한 번 설계하는 루프", "사람은 게이트에만 선다")
    o.append(p)
    o.append(chip_c(538, iy, "하트비트 — 스케줄 또는 이벤트", cls="d-chip-a", tcls="d-chip-a-t"))
    cyc = [("① 일감 발견", 0), ("② 구현 (maker)", 1), ("③ 검증 (checker)", 2), ("④ 커밋 · PR 생성", 3)]
    for t, i in cyc:
        y = iy + 32 + i * 50
        o.append(box(ix + 62, y, iw - 74, 38, t, cls="d-accent" if i in (1, 2) else "d-box", tsize=11.5))
        if i < 3:
            o.append(arrow(538, y + 40, 538, y + 48, u, "통과" if i == 2 else None, lab_dx=26, lab_dy=8))
    o.append(box(ix, iy + 32, 52, 88, "progress", [".md"], cls="d-panel-2", tsize=10.5))
    o.append(text(ix + 26, iy + 132, "스파인", 10, "middle", "d-t d-dim"))
    o.append(arrow(ix + 26, iy + 146, ix + 26, iy + 190, u, dash=True))
    o.append(text(ix + 4, iy + 166, "처음에 읽고", 9.5, "start", "d-t d-dim"))
    o.append(text(ix + 4, iy + 178, "마지막에 갱신", 9.5, "start", "d-t d-dim"))
    o.append(banner(374, 278, 332, 34, "인간 게이트 — 위험한 결정만 사람에게"))
    return "".join(o), 372


reg("shift-prompt-to-loop", W, _shift()[1],
    "턴 단위 프롬프팅에서는 사람이 하트비트와 검증자와 기억을 모두 겸하지만, 한 번 설계한 루프에서는 하트비트가 비트를 시작하고 checker가 채점하며 사람은 위험한 결정의 게이트에만 선다.",
    _shift()[0])


# ------------------------------------------------- 2. four layers
def _layers():
    u, o = "four-layers", []
    specs = [(0, 0, 720, 214, "④ 루프 엔지니어링", "무엇을, 언제 시작하고, 언제 끝났는지", "d-accent", 1),
             (56, 40, 608, 158, "③ 하네스 엔지니어링", "도구 실행과 오류 처리 — 작은 루프가 여기 산다", "d-panel-2", 0),
             (112, 76, 496, 106, "② 컨텍스트 엔지니어링", "한 턴에 모델이 보는 모든 것", "d-box", 0),
             (168, 110, 384, 56, "① 프롬프트 엔지니어링", "모델에게 보내는 문장", "d-strong", 0)]
    for x, y, w, h, t, s, c, cur in specs:
        o.append('<rect x="%g" y="%g" width="%g" height="%g" rx="10" class="%s"/>' % (x, y, w, h, c))
        o.append(text(x + 14, y + 21, t, 12.5, "start", "d-t", "700"))
        o.append(text(x + 14, y + 37, s, 10.5, "start", "d-t d-dim"))
        if cur:
            o.append(chip_c(640, y + 10, "이 모듈", cls="d-chip-a", tcls="d-chip-a-t"))
    o.append(note(360, 240,
                  "각 계층은 서로 다른 실패를 막는다: 컨텍스트가 없으면 모델이 추측하고, 하네스가 없으면 사람이 유일한 검증자이며, 루프가 없으면 스케줄은 여전히 사람이다", W))
    o.append(banner(60, 268, 600, 40, "유용한 질문 — “나는 어느 계층을 아직 손으로 하고 있는가?”"))
    return "".join(o), 320


reg("four-layers", W, _layers()[1],
    "프롬프트, 컨텍스트, 하네스, 루프 네 계층이 중첩된 구조. 각 계층은 서로 다른 실패를 막으며 이 모듈은 가장 바깥의 루프 계층을 다룬다.",
    _layers()[0])


# ------------------------------------------------- 3. two loops, one name
def _two_loops():
    u, o = "two-loops-one-name", []
    p, ix, iy, iw, _ = panel(0, 8, 330, 322, "큰 루프", "루프 엔지니어링이 설계하는 것")
    o.append(p)
    cards = ["하트비트가 비트를 시작한다",
             "한 비트 = 작업의 완전한 1회 실행",
             "checker가 결과를 채점한다",
             "스파인(progress.md)이 실행 간 기억"]
    for i, c in enumerate(cards):
        y = iy + 6 + i * 54
        o.append(box(ix + 22, y, iw - 22, 42, c,
                     cls="d-strong" if i == 1 else "d-box", tsize=11.5))
    o.append(path_a("M 26 %g C 6 %g 6 %g 26 %g" % (iy + 226, iy + 232, iy + 22, iy + 28), u))
    o.append(text(20, iy + 128, "내일의", 9.5, "middle", "d-t d-acc", halo=True))
    o.append(text(20, iy + 141, "비트", 9.5, "middle", "d-t d-acc", halo=True))
    o.append(arrow_a(332, 118, 356, 118, u, "확대", lab_dy=-8))
    p, ix, iy, iw, _ = panel(358, 8, 362, 322, "작은 루프", "에이전트 런타임 내부 — 하네스 계층")
    o.append(p)
    cyc = ["① 컨텍스트 구성", "② 모델의 결정", "③ 도구 실행", "④ 결과를 컨텍스트에 추가"]
    for i, c in enumerate(cyc):
        y = iy + 6 + i * 44
        o.append(box(ix, y, iw, 34, c, cls="d-box", tsize=11.5))
        if i < 3:
            o.append(arrow(539, y + 36, 539, y + 42, u))
    o.append(path("M %g %g C %g %g %g %g %g %g"
                  % (ix + iw - 6, iy + 178, ix + iw + 10, iy + 178,
                     ix + iw + 10, iy + 16, ix + iw - 6, iy + 16), u, dash=True))
    o.append(box(ix, iy + 194, iw, 48, "모델이 도구를 그만 요청하면 비트가 끝난다",
                 ["제어가 큰 루프(checker → 스파인)로 돌아간다"], cls="d-accent", tsize=11.5))
    o.append(note(539, 342, "작은 루프에는 하트비트도 스파인도 없다 — 비트가 끝나면 아무것도 기억하지 못한다", 350))
    return "".join(o), 368


reg("two-loops-one-name", W, _two_loops()[1],
    "이름이 같은 두 루프. 큰 루프는 하트비트와 비트와 스파인으로 이루어지고, 작은 루프는 에이전트 런타임 안에서 컨텍스트 구성과 도구 실행을 반복하다가 끝나면 아무것도 기억하지 못한다.",
    _two_loops()[0])


# ------------------------------------------------- 4. loop anatomy
def _anatomy():
    u, o = "loop-anatomy", []
    cards = [("하트비트", ["스케줄 · 이벤트가", "각 비트를 시작한다", "없으면 1회 실행"]),
             ("워크트리", ["격리 —", "과제당 체크아웃 하나"]),
             ("스킬", ["프로젝트 지식의 문서화", "맨바닥 시작 방지"]),
             ("서브에이전트", ["만드는 자와", "검사하는 자의 분리"]),
             ("커넥터", ["MCP로 실제 도구에 도달", "제안이 아니라 행동"])]
    for i, (t, subs) in enumerate(cards):
        x = i * 146
        o.append(box(x, 20, 136, 128, None, cls="d-box"))
        o.append(numchip(x + 68, 20, i + 1))
        o.append(text(x + 68, 56, t, 12.5, "middle", "d-t", "700"))
        yy = 78
        for s in subs:
            for ln in wrap(s, 10.5, 118):
                o.append(text(x + 68, yy, ln, 10.5, "middle", "d-t d-dim"))
                yy += 15
        o.append(line(x + 68, 150, x + 68, 176, "d-rule", dash=True))
    o.append(box(0, 178, 720, 74, "⑥ 상태와 기억 — 스파인",
                 ["CLAUDE.md / AGENTS.md + progress.md, 또는 외부 보드.",
                  "모델은 실행 사이 모든 것을 잊지만 저장소는 잊지 않는다. 스파인이 없으면 루프도 없다."],
                 cls="d-accent"))
    o.append(arrow_a(360, 254, 360, 282, u))
    o.append(box(130, 284, 460, 46, "인간 게이트",
                 ["안전한 작업은 커밋 · PR로, 위험하거나 불확실한 작업은 사람에게"], cls="d-strong", tsize=12))
    return "".join(o), 344


reg("loop-anatomy", W, _anatomy()[1],
    "루프의 다섯 부품(하트비트·워크트리·스킬·서브에이전트·커넥터)이 스파인이라는 넓은 상태 막대 위에 서 있고, 각 비트의 끝은 인간 게이트로 이어진다.",
    _anatomy()[0])


# ------------------------------------------------- 5. two paths
def _paths():
    u, o = "two-paths", []
    p, ix, iy, iw, _ = panel(0, 8, 350, 216, "내장형", "예: Claude Code")
    o.append(p)
    x, y = ix, iy + 8
    for lb in ["/loop", "/goal", "/schedule", "Routines", "--worktree", "서브에이전트 폴더", "Channels"]:
        s, cw = chip(x, y, lb, cls="d-chip-a", tcls="d-chip-a-t")
        if x + cw > ix + iw:
            x, y = ix, y + 26
            s, cw = chip(x, y, lb, cls="d-chip-a", tcls="d-chip-a-t")
        o.append(s)
        x += cw + 6
    o.append(note(175, y + 48,
                  "스케줄러 · 검증자 · 격리가 제품에 내장되어 설정만 하면 된다. 클라우드 루틴은 노트북을 닫아도 돌지만 계정별 일일 실행 한도가 있다", 322))
    p, ix, iy, iw, _ = panel(370, 8, 350, 216, "조립형", "예: OpenCode + 운영체제")
    o.append(p)
    x, y = ix, iy + 8
    for lb in ["opencode run", "serve/attach", "cron · launchd", "작업 스케줄러", "GitHub Actions", "커스텀 에이전트", "mcp 설정"]:
        s, cw = chip(x, y, lb)
        if x + cw > ix + iw:
            x, y = ix, y + 26
            s, cw = chip(x, y, lb)
        o.append(s)
        x += cw + 6
    o.append(note(545, y + 48,
                  "도구는 워커만 제공하고 비트를 시작시키는 것은 운영체제나 CI다. 설정은 더 필요하지만 통제권이 크고 벤더 클라우드가 필요 없다", 322))
    o.append(banner(0, 236, 720, 44, "하트비트는 관리형 루틴이든 cron 한 줄이든 하트비트다 — 루프의 모양을 배우면 도구를 넘어 이전된다"))
    return "".join(o), 292


reg("two-paths", W, _paths()[1],
    "같은 루프를 만드는 두 경로. 내장형은 스케줄러와 격리가 제품에 들어 있어 설정만 하면 되고, 조립형은 운영체제나 CI가 비트를 점화하는 대신 통제권이 크다.",
    _paths()[0])


# ------------------------------------------------- 6. four heartbeats
def _hb():
    u, o = "four-heartbeats", []
    o.append(line(10, 30, 710, 30, "d-axis"))
    o.append(text(10, 20, "사람이 붙잡고 있음", 10.5, "start", "d-t d-dim"))
    o.append(text(710, 20, "사람 없이 돎", 10.5, "end", "d-t d-dim"))
    cards = [("인세션", ["세션이 열려 있는 동안", "타이머로 반복하고,", "세션을 닫으면 정지"], "주방 타이머"),
             ("조건부", ["검증된 조건이 참이 될 때까지", "반복하고 검사가", "통과하면 정지"], "맛보는 사람이 됐다고 할 때까지"),
             ("스케줄", ["노트북이 닫혀 있어도", "시계에 맞춰 실행", "(루틴 · cron · Actions)"], "자명종"),
             ("이벤트 구동", ["PR 열림 · 메시지 도착 같은", "사건이 발생하는", "순간에 반응"], "초인종")]
    for i, (t, subs, an) in enumerate(cards):
        x = i * 182
        o.append(box(x, 44, 172, 150, None, cls="d-accent" if i >= 2 else "d-box"))
        o.append(numchip(x + 86, 44, i + 1))
        o.append(text(x + 86, 80, t, 13, "middle", "d-t", "700"))
        yy = 100
        for s in subs:
            o.append(text(x + 86, yy, s, 10.5, "middle", "d-t d-dim"))
            yy += 15
        o.append(line(x + 20, 156, x + 152, 156, "d-rule"))
        for j, ln in enumerate(wrap("비유: " + an, 10, 150)):
            o.append(text(x + 86, 172 + j * 13, ln, 10, "middle", "d-t"))
    o.append(note(360, 216, "루프가 한 번 점화되는 것을 비트(beat)라고 부른다", W))
    return "".join(o), 232


reg("four-heartbeats", W, _hb()[1],
    "루프를 깨우는 네 가지 하트비트 — 인세션, 조건부, 스케줄, 이벤트 구동 — 을 사람이 붙잡고 있는 정도에 따라 배열한 그림.",
    _hb()[0])


# ------------------------------------------------- 7. routine run anatomy
def _routine():
    u, o = "routine-run-anatomy", []
    p, ix, iy, iw, _ = panel(0, 8, 232, 300, "① 지속되는 것", "저장된 설정")
    o.append(p)
    for i, (t, s) in enumerate([("프롬프트", "자기완결적, 스킬을 가리킴"),
                                ("모델 선택", "작업 난이도에 맞게"),
                                ("저장소", "기본은 claude/* 브랜치에만"),
                                ("환경", "네트워크 · 변수 · 설치"),
                                ("커넥터", "필요 없는 것은 제거"),
                                ("트리거", "스케줄 · API · GitHub 이벤트")]):
        o.append(box(ix, iy + 4 + i * 38, iw, 32, t + " — " + s, cls="d-box", tsize=10.5, tweight=None))
    o.append(arrow(234, 150, 250, 150, u))
    p, ix, iy, iw, _ = panel(252, 8, 232, 300, "② 일시적인 것", "실행 1회", dash=True, cls="d-panel-2")
    o.append(p)
    o.append(box(ix, iy + 4, iw, 96, "새 클론에서 시작",
                 ["커밋된 컨텍스트(progress.md,", "SKILL.md)를 먼저 읽고", "프롬프트를 끝까지 수행한다"],
                 cls="d-box", tsize=11.5))
    o.append(box(ix, iy + 108, iw, 52, "중간 승인 없음", ["이전 실행의 기억도 없음"], cls="d-box", tsize=11.5))
    o.append(box(ix, iy + 168, iw, 78, "실행이 끝나면 소멸",
                 ["작업 트리 · 미푸시 편집 ·", "임시 파일 · 세션 전부"], cls="d-warn", tsize=11.5))
    o.append(arrow(486, 150, 502, 150, u))
    p, ix, iy, iw, _ = panel(504, 8, 216, 300, "③ 살아남는 것", "실행의 세 출구")
    o.append(p)
    for i, (t, s) in enumerate([("claude/* 브랜치 푸시", ["사람이 검토하는 PR", "— 인간 게이트"]),
                                ("커넥터 행동", ["메시지 · 티켓,", "내 계정 명의로"]),
                                ("실행 기록", ["초록 상태 ≠", "과제 성공"])]):
        o.append(box(ix, iy + 6 + i * 82, iw, 70, t, s, cls="d-ok" if i == 0 else "d-box", tsize=11.5))
    o.append(note(360, 328, "상태는 저장소에 산다. 새 클론은 상태를 운반할 뿐 보관하지 않는다", W))
    return "".join(o), 344


reg("routine-run-anatomy", W, _routine()[1],
    "스케줄된 루틴 실행 한 회의 해부. 저장된 설정은 지속되고, 실행 자체는 새 클론에서 시작해 끝나면 소멸하며, 브랜치 푸시와 커넥터 행동과 실행 기록만 살아남는다.",
    _routine()[0])


# ------------------------------------------------- 8. checker ladder
def _ladder():
    u, o = "checker-ladder", []
    o.append(text(10, 20, "가장 강한 검증", 11, "start", "d-t d-dim", "700"))
    o.append(text(710, 20, "가장 약한 검증", 11, "end", "d-t d-dim", "700"))
    o.append(line(10, 30, 710, 30, "d-axis"))
    cards = [("통과하는 테스트", "코드", ["테스트 러너와 린터가", "기계적으로 판정한다"], "증명", "d-ok", 96),
             ("기계적 검사", "문서", ["깨진 링크 · 빠진 그림 ·", "금지어 · 제목 구조"], "부분 증명", "d-box", 150),
             ("기준표와 합격선", "주관적 산출물", ["리뷰어 에이전트가 채점한다", "“95점 미만이면 멈추지 마라”"], "주장 — 증명 아님", "d-warn", 220)]
    for i, (t, kind, subs, cchip, cls, gw) in enumerate(cards):
        x = i * 244
        o.append(box(x, 44, 232, 118, None, cls=cls))
        o.append(numchip(x + 22, 62, i + 1))
        o.append(text(x + 116, 70, t, 12.5, "middle", "d-t", "700"))
        o.append(text(x + 116, 86, kind, 10.5, "middle", "d-t d-dim"))
        for j, s in enumerate(subs):
            o.append(text(x + 116, 108 + j * 15, s, 10.5, "middle", "d-t"))
        o.append(chip_c(x + 116, 140, cchip, cls="d-chip-a", tcls="d-chip-a-t"))
        o.append(line(x + 116, 164, x + 116, 194, "d-rule", dash=True))
        o.append('<rect x="%g" y="196" width="8" height="46" rx="2" class="d-gate"/>' % (x + 116 - gw / 2))
        o.append('<rect x="%g" y="196" width="8" height="46" rx="2" class="d-gate"/>' % (x + 116 + gw / 2 - 8))
        o.append(text(x + 116, 262, "인간 게이트 폭", 10, "middle", "d-t d-dim"))
    o.append(note(360, 292, "검증자가 약할수록 더 많은 작업이 인간 게이트를 지난다 — 문이 넓어진다", W))
    return "".join(o), 310


reg("checker-ladder", W, _ladder()[1],
    "검증 사다리. 통과하는 테스트는 증명, 기계적 검사는 부분 증명, 기준표 채점은 주장에 그치며 검증이 약할수록 사람이 통과시켜야 할 인간 게이트의 폭이 넓어진다.",
    _ladder()[0])


# ------------------------------------------------- 9. verification homes
def _homes():
    u, o = "verification-homes", []
    o.append(text(10, 20, "내가 점화한다", 11, "start", "d-t d-dim", "700"))
    o.append(text(710, 20, "나 없이 점화된다", 11, "end", "d-t d-dim", "700"))
    o.append(line(10, 30, 710, 30, "d-axis"))
    cards = [("단독 실행", "하트비트: 나", ["작업 후 의도적으로 호출", "(보안 스캔 · 접근성 감사)", "비용: 기억해야 하는 한 턴"], "d-box"),
             ("내장", "하트비트: 일을 만드는 스킬", ["스킬 끝에 붙어", "요청 없이 실행된다", "내가 편집 가능한 스킬 한정"], "d-box"),
             ("체인", "하트비트: 직전 스킬", ["스킬이 끝나며 다음을 호출", "습관이 계약이 된다", "유연성과 토큰이 대가"], "d-box"),
             ("모든 PR에", "하트비트: PR 이벤트", ["누구의 변경이든 같은 관문", "개인 인프라가", "팀 인프라가 된다"], "d-strong")]
    for i, (t, hb, subs, cls) in enumerate(cards):
        x = i * 182
        o.append(box(x, 46, 172, 152, None, cls=cls))
        o.append(numchip(x + 86, 46, i + 1))
        o.append(text(x + 86, 82, t, 13, "middle", "d-t", "700"))
        o.append(chip_c(x + 86, 90, hb, cls="d-chip-a", tcls="d-chip-a-t", h=18))
        for j, s in enumerate(subs):
            o.append(text(x + 86, 132 + j * 15, s, 10.5, "middle", "d-t d-dim"))
    o.append(arrow_a(174, 214, 190, 214, u))
    o.append(note(176, 236, "매번 돌리고 있음을 발견하면 영구적인 집으로 옮긴다", 340))
    o.append(arrow_a(538, 214, 554, 214, u))
    o.append(note(544, 236, "체인이 내 작업에서 안정된 뒤에만 팀 관문으로 올린다", 340))
    return "".join(o), 268


reg("verification-homes", W, _homes()[1],
    "검증 스킬이 사는 네 곳 — 단독 실행, 내장, 체인, 모든 PR — 을 누가 점화하는지에 따라 배열하고 승급 조건을 표시한 그림.",
    _homes()[0])


# ------------------------------------------------- 10. the spine
def _spine():
    u, o = "the-spine", []
    for i, (x, t, mid) in enumerate([(20, "실행 1 — 월요일 9시", "② 일한다"),
                                     (390, "실행 2 — 화요일 9시", "② 월요일의 작업 위에 쌓는다")]):
        p, ix, iy, iw, _ = panel(x, 8, 310, 160, t, None, cls="d-panel-2", dash=True)
        o.append(p)
        for j, s in enumerate(["① 스파인을 먼저 읽는다", mid, "③ 스파인을 마지막에 갱신한다"]):
            o.append(box(ix, iy + 4 + j * 38, iw, 32, s,
                         cls="d-accent" if j != 1 else "d-box", tsize=11, tweight=None))
    o.append(cross(360, 88, 9))
    o.append(note(360, 112, "세션 종료 —", 120, cls="d-t d-bad"))
    o.append(note(360, 126, "모델의 기억은 지워진다", 130, cls="d-t d-bad"))
    o.append(arrow_a(60, 200, 60, 172, u))
    o.append(text(66, 196, "시작 시 읽기", 10, "start", "d-t d-acc"))
    o.append(arrow_a(280, 172, 280, 200, u))
    o.append(text(286, 196, "종료 시 쓰기", 10, "start", "d-t d-dim"))
    o.append(arrow_a(430, 200, 430, 172, u))
    o.append(arrow_a(650, 172, 650, 200, u))
    p, ix, iy, iw, _ = panel(0, 202, 720, 128, "저장소 — 세션보다 오래 산다")
    o.append(p)
    o.append(box(ix, iy + 4, 340, 62, "CLAUDE.md / AGENTS.md",
                 ["다이어리의 앞쪽 — 항구적 교훈", "매 실행 시작 시 읽는다"], cls="d-box", tsize=11.5))
    o.append(box(ix + 352, iy + 4, 340, 62, "progress.md",
                 ["다이어리의 뒤쪽 — 시도 · 통과 · 미결", "매 실행 끝에 갱신한다"], cls="d-box", tsize=11.5))
    o.append(path_a("M 470 176 C 300 176 180 196 172 216", u, dash=True))
    o.append(text(352, 166, "반복된 실수? 교훈은 다이어리 앞쪽으로", 10, "middle", "d-t d-acc", halo=True))
    o.append(note(360, 350, "스파인이 없으면 루프도 없다", W, cls="d-t"))
    return "".join(o), 364


reg("the-spine", W, _spine()[1],
    "두 번의 실행 사이에서 모델의 기억은 지워지지만 저장소는 남는다. 각 실행은 스파인을 먼저 읽고 마지막에 갱신하며, 반복된 실수의 교훈은 규칙 파일로 승격된다.",
    _spine()[0])


# ------------------------------------------------- 11. dreaming loop
def _dream():
    u, o = "dreaming-loop", []
    p, ix, iy, iw, _ = panel(0, 8, 200, 300, "일하는 루프들", "매일")
    o.append(p)
    for i, t in enumerate(["아침 트리아지", "PR 리뷰어", "야간 체인지로그 작성기"]):
        o.append(box(ix, iy + 6 + i * 40, iw, 32, t, cls="d-box", tsize=11))
    o.append(box(ix, iy + 140, iw, 84, "내일의 실행은",
                 ["개선된 규칙을 읽으므로", "더 예리하게 시작한다"], cls="d-ok", tsize=11, dash=True))
    o.append(arrow(202, 80, 236, 80, u, "기록을 쓴다", lab_dy=-8))
    p, ix, iy, iw, _ = panel(238, 8, 220, 300, "저장소 = 스파인")
    o.append(p)
    o.append(box(ix, iy + 4, iw, 46, "progress.md · 실행 로그",
                 ["비트당 날짜 있는 항목"], cls="d-box", tsize=11))
    o.append(box(ix, iy + 58, iw, 40, "dreaming-state.md",
                 ["마지막 검토 배치의 날짜"], cls="d-panel-2", tsize=11, dash=True))
    o.append(box(ix, iy + 106, iw, 92, "CLAUDE.md / AGENTS.md + 스킬",
                 ["모든 미래 실행이 읽는", "최고 레버리지의 쓰기.", "게이트를 통해서만 변경된다"], cls="d-strong", tsize=11))
    o.append(arrow(460, 80, 494, 80, u, "읽는다", lab_dy=-8, dash=True))
    p, ix, iy, iw, _ = panel(496, 8, 224, 300, "드리밍 루프", "하트비트: 주 1회")
    o.append(p)
    for i, (t, s) in enumerate([("① 새 로그 읽기", "dreaming-state.md 이후"),
                                ("② 반복 탐색", "같은 실패가 두 번 이상?"),
                                ("③ 근거 있는 패턴만 채택", "한 번은 소음, 세 번은 교훈"),
                                ("④ PR로 작성", "직접 편집 금지, 근거 첨부"),
                                ("⑤ 인간 게이트", "병합 또는 기각")]):
        o.append(box(ix, iy + 4 + i * 50, iw, 42, t, [s],
                     cls="d-strong" if i == 4 else ("d-accent" if i == 3 else "d-box"), tsize=11))
    o.append(path_a("M 500 %g C 470 %g 470 %g 462 %g" % (270, 270, 200, 196), u))
    o.append(text(470, 240, "병합된 교훈", 10, "middle", "d-t d-acc", halo=True))
    o.append(note(360, 330, "이 루프는 다른 모든 루프를 조종하는 규칙을 고쳐 쓴다. 게이트 없이 돌려선 안 되는 마지막 루프다", W))
    return "".join(o), 348


reg("dreaming-loop", W, _dream()[1],
    "일하는 루프들이 저장소에 기록을 쌓으면 주 1회 도는 드리밍 루프가 반복 실패를 찾아 규칙 수정안을 PR로 올리고, 사람이 병합한 교훈만 모든 미래 실행에 반영된다.",
    _dream()[0])


# ------------------------------------------------- 12. morning loop
def _morning():
    u, o = "morning-loop", []
    o.append(chip_c(360, 6, "하트비트 — 평일 9시마다", cls="d-chip-a", tcls="d-chip-a-t", h=24))
    steps = [(40, "① progress.md 읽기", ["스파인 — 어제까지의 상태"]),
             (108, "② 일감 찾기, 최대 5건", ["밤사이 CI 실패 · 열린 이슈 · 새 보안 권고"]),
             (176, "③ 자기만의 워크트리에서 수정안 작성", ["maker"]),
             (244, "④ 별도 리뷰어의 채점", ["checker — 별도 에이전트"])]
    for y, t, s in steps:
        o.append(box(190, y, 340, 52, t, s, cls="d-box", tsize=12))
        if y < 244:
            o.append(arrow(360, y + 54, 360, y + 64, u))
    o.append(arrow_a(310, 298, 200, 330, u, "FAIL 또는 위험", lab_dy=-10))
    o.append(arrow_a(410, 298, 530, 330, u, "PASS + 저위험", lab_dy=-10))
    o.append(box(34, 332, 306, 62, "⑤b progress.md의 ‘사람 필요’ 절에 기록",
                 ["PR 없음 — 사람이 나중에 결정한다"], cls="d-warn", tsize=11.5))
    o.append(box(380, 332, 340, 62, "⑤a PR 열기",
                 ["사람이 검토한다 — 인간 게이트"], cls="d-ok", tsize=11.5))
    o.append(arrow(190, 396, 300, 422, u))
    o.append(arrow(550, 396, 420, 422, u))
    o.append(box(190, 424, 340, 46, "⑥ progress.md 갱신", ["내일이 읽는다"], cls="d-accent", tsize=12))
    o.append(path_a("M 188 447 C 90 447 16 438 16 396 L 16 108 C 16 78 90 66 188 66", u, dash=True))
    o.append(text(104, 250, "다음 후보,", 10, "middle", "d-t d-acc", halo=True))
    o.append(text(104, 264, "그리고 내일 9시", 10, "middle", "d-t d-acc", halo=True))
    o.append(note(360, 494, "일어나 보면 PR 두 개와 플래그된 결정 하나. 당신은 아무것도 입력하지 않았다", W))
    return "".join(o), 512


reg("morning-loop", W, _morning()[1],
    "아침 유지보수 루프 한 비트의 흐름도. 스파인을 읽고 일감을 찾아 워크트리에서 수정한 뒤 리뷰어가 채점하고, 통과한 것은 PR로 위험한 것은 사람 필요 목록으로 갈라진 뒤 스파인 갱신에서 합류한다.",
    _morning()[0])


# ------------------------------------------------- 13. cost by cadence
def _cost():
    u, o = "cost-by-cadence", []
    o.append(hdr(360, 20, "세 막대 모두 비트당 비용은 같다(약 0.2달러). 다른 것은 빈도뿐이다"))
    base, top = 300, 44
    bars = [("평일 하루 5회", "월 약 100비트", 20, "월 약 20달러", "d-box"),
            ("매시간, 밤낮으로", "월 약 720비트", 150, "월 약 150달러", "d-box"),
            ("5분마다, 밤낮으로", "월 약 8,600비트", 1800, "월 약 1,800달러", "d-warn")]
    for i, (t, beats, cost, lab, cls) in enumerate(bars):
        cx = 140 + i * 220
        h = max(6, cost / 1800.0 * (base - top))
        o.append('<rect x="%g" y="%g" width="120" height="%g" rx="5" class="%s"/>'
                 % (cx - 60, base - h, h, cls))
        o.append(text(cx, base - h - 10, lab, 12, "middle", "d-t d-acc", "700"))
        o.append(text(cx, base + 22, t, 11.5, "middle", "d-t", "700"))
        o.append(text(cx, base + 38, beats, 10.5, "middle", "d-t d-dim"))
    o.append(line(30, base, 690, base, "d-axis"))
    o.append(text(580, 128, "비트 수는 100배 이상,", 10.5, "middle", "d-t d-dim"))
    o.append(text(580, 143, "추가 가치는 없다", 10.5, "middle", "d-t d-dim"))
    o.append(note(360, 366, "비용은 어떤 명령을 썼는가가 아니라 얼마나 자주 도는가에서 나온다", W))
    return "".join(o), 384


reg("cost-by-cadence", W, _cost()[1],
    "같은 루프라도 케이던스에 따라 월 비용이 20달러, 150달러, 1800달러로 갈린다. 비용은 명령이 아니라 빈도에서 나온다.",
    _cost()[0])


# ------------------------------------------------- 14. three loops
def _three():
    u, o = "three-loops", []
    specs = [(0, 0, 720, 232, "③ 외부 루프 — 날 단위", "실제 사용자가 쓰고, 그 행동이 다음 수정을 알려 준다", "운전자: 세상", "d-panel-2"),
             (60, 44, 600, 152, "② 피드백 루프 — 시간 단위", "사람이 써 보고, 바꿀 것을 정하고, 명세를 갱신한다", "운전자: 나", "d-box"),
             (124, 90, 472, 78, "① 코딩 루프 — 분 단위", "명세를 만족할 때까지 쓰고 · 테스트하고 · 고친다", "운전자: 에이전트", "d-accent")]
    for x, y, w, h, t, s, drv, c in specs:
        o.append('<rect x="%g" y="%g" width="%g" height="%g" rx="10" class="%s"/>' % (x, y, w, h, c))
        o.append(text(x + 14, y + 21, t, 12.5, "start", "d-t", "700"))
        o.append(text(x + 14, y + 38, s, 10.5, "start", "d-t d-dim"))
        o.append(text(x + w - 14, y + 21, drv, 10.5, "end", "d-t d-dim", "700"))
    o.append(chip_c(360, 176, "명세와 평가(evals)가 사람의 결정을 코드로 나른다", cls="d-chip-a", tcls="d-chip-a-t"))
    o.append(chip_c(360, 204, "바깥의 피드백이 사람에게 돌아온다", cls="d-chip"))
    o.append(chip_c(240, 148, "이 모듈이 가르친 루프", cls="d-chip-a", tcls="d-chip-a-t"))
    o.append(note(360, 262, "에이전트는 세 루프를 다 돌 수 없다. 사람에게는 컨텍스트 우위가 있다", W))
    return "".join(o), 282


reg("three-loops", W, _three()[1],
    "분 단위 코딩 루프, 시간 단위 피드백 루프, 날 단위 외부 루프가 중첩된 구조. 안쪽만 에이전트가 돌리고 바깥 두 개의 운전자는 사람과 세상이다.",
    _three()[0])


# ------------------------------------------------- 15. two routine gate
def _gate():
    u, o = "two-routine-gate", []
    o.append(note(360, 18, "루틴은 중간에 멈춰 물어볼 수 없다. 그래서 게이트는 루틴 안이 아니라 루틴 사이에 짓는다", W, cls="d-t"))
    o.append(box(0, 40, 224, 120, "① 루틴 A — 초안 작성자",
                 ["스케줄이나 GitHub 이벤트로 점화",
                  "claude/* 브랜치 · 요약 메시지 ·", "임시 저장 메일 · 배포 계획을",
                  "사람이 읽을 곳에 올리되 배포는 하지 않는다"], cls="d-box", tsize=12))
    o.append(arrow_a(226, 100, 246, 100, u))
    o.append(box(248, 40, 224, 120, "② 사람의 결정",
                 ["초안을 읽고", "승인 또는 기각을 고른다", "— 인간 게이트"], cls="d-strong", tsize=12))
    o.append(arrow_a(474, 100, 494, 100, u, "승인", lab_dy=-8))
    o.append(box(496, 40, 224, 120, "③ 루틴 B — 실행자",
                 ["승인이 API 트리거(/fire 엔드포인트", "POST)로 B를 점화한다",
                  "검토된 행동을 수행:", "발송 · 병합 · 배포"], cls="d-ok", tsize=12))
    o.append(path("M 360 162 C 360 200 250 200 130 206", u, dash=True))
    o.append(box(0, 208, 300, 56, "기각",
                 ["초안은 초안으로 남고 아무것도 나가지 않으며", "progress.md의 ‘사람 필요’ 절에 기록된다"],
                 cls="d-warn", tsize=11.5))
    return "".join(o), 280


reg("two-routine-gate", W, _gate()[1],
    "루틴 A가 초안을 올리고 사람이 승인하면 API 트리거가 루틴 B를 점화해 실제 행동을 수행한다. 기각하면 초안은 그대로 남고 사람 필요 목록에 기록된다.",
    _gate()[0])
