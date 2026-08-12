# -*- coding: utf-8 -*-
"""Module 2 diagrams — Harness Engineering."""
from svglib import *   # noqa

W = 720
D = {}


def reg(uid, w, h, aria, body):
    D[uid] = svg(uid, w, h, aria, body)


# ------------------------------------------------- 1. same model, two outcomes
def _same():
    u, o = "same-model-two-outcomes", []
    o.append(hdr(155, 20, "하니스 없이"))
    o.append(hdr(545, 20, "하니스와 함께"))
    o.append(line(360, 8, 360, 470, "d-rule", dash=True))
    LX, LW = 15, 280
    o.append(box(LX, 40, LW, 40, "프롬프트", cls="d-panel-2", tsize=12))
    o.append(box(LX, 226, LW, 40, "모델", cls="d-strong", tsize=13))
    o.append(box(LX, 380, LW, 46, "무엇이든 나온다", cls="d-warn", tsize=12))
    o.append(arrow(155, 82, 155, 224, u))
    o.append(arrow(155, 268, 155, 378, u))
    o.append(note(155, 112, "사이에 아무것도 없다", LW))
    o.append(note(155, 452, "제한 없음 · 증명 없음 · 기록 없음", LW, cls="d-t d-bad"))
    RX, RW = 385, 320
    stack = [(40, "프롬프트", [], "d-panel-2"),
             (100, "Inform — 규칙 파일 · skill · 도구 설명", [], "d-box"),
             (160, "Constrain — permission · sandbox", [], "d-box"),
             (226, "모델", [], "d-strong"),
             (292, "Verify — hook · 테스트 · typed output", [], "d-box")]
    for y, t, s, c in stack:
        o.append(box(RX, y, RW, 40, t, s, cls=c, tsize=12 if y != 226 else 13))
    for a, b in [(80, 98), (140, 158), (200, 224), (266, 290)]:
        o.append(arrow(545, a, 545, b, u))
    o.append(arrow_a(500, 332, 465, 378, u))
    o.append(arrow_a(590, 332, 625, 378, u))
    o.append(box(385, 380, 152, 46, "통과", ["증명된 결과"], cls="d-ok", tsize=12))
    o.append(box(553, 380, 152, 46, "실패", ["사람에게 표시"], cls="d-warn", tsize=12))
    o.append(note(545, 452, "나쁜 행동은 불가능해지고, 나쁜 작업은 보이게 된다", RW))
    o.append(banner(0, 480, 720, 42, "같은 모델, 다른 날, 같은 결과 — 그것이 하니스가 주는 것"))
    return "".join(o), 534


reg("same-model-two-outcomes", W, _same()[1],
    "같은 모델도 하니스 유무에 따라 결과가 달라진다. 하니스가 없으면 프롬프트에서 모델을 거쳐 무엇이든 그대로 나오지만, 하니스가 있으면 정보·제한 층을 지나 모델에 닿고 검증 층을 통과해야 결과가 되며 실패는 사람에게 표시된다.",
    _same()[0])


# ------------------------------------------------- 2. compounding curve
def _curve():
    u, o = "compounding-curve", []
    X0, X1, Y0, Y1 = 56, 690, 46, 268
    def px(n): return X0 + n * (X1 - X0) / 30.0
    def py(p): return Y1 - p * (Y1 - Y0)
    o.append(hdr(360, 18, "더 좋은 모델은 단계별 수치를 조금 올린다. 하니스는 연쇄 자체를 공격한다"))
    for pct in (0, 25, 50, 75, 100):
        y = py(pct / 100.0)
        o.append(line(X0, y, X1, y, "d-grid"))
        o.append(text(X0 - 10, y + 4, "%d%%" % pct, 10, "end", "d-t d-dim"))
    for n in (0, 5, 10, 15, 20, 25, 30):
        o.append(text(px(n), Y1 + 20, str(n), 10, "middle", "d-t d-dim"))
    o.append(line(X0, Y1, X1, Y1, "d-axis"))
    o.append(text(360, Y1 + 42, "실행 단계 수", 11, "middle", "d-t d-dim"))
    o.append(text(X0 - 40, 30, "성공률", 11, "start", "d-t d-dim"))
    for rate, cls, dash in ((0.99, "d-line", True), (0.95, "d-line-a", False)):
        pts = " ".join("%g,%g" % (px(n), py(rate ** n)) for n in range(31))
        o.append('<polyline points="%s" class="%s" fill="none"%s/>'
                 % (pts, cls, ' stroke-dasharray="5 4"' if dash else ""))
    o.append('<circle cx="%g" cy="%g" r="4.5" class="d-dot-a"/>' % (px(20), py(0.95 ** 20)))
    o.append(text(px(20) + 12, py(0.95 ** 20) + 4, "20단계 ≈ 36%", 11.5, "start", "d-t d-acc", "700"))
    o.append('<circle cx="%g" cy="%g" r="4" class="d-dot"/>' % (px(20), py(0.99 ** 20)))
    o.append(text(px(20) + 12, py(0.99 ** 20) + 4, "99%/단계 → 20단계 ≈ 82%", 11, "start", "d-t d-dim"))
    o.append(text(px(9), py(0.95 ** 9) + 22, "95%/단계", 11.5, "middle", "d-t d-acc", "700"))
    o.append(note(360, 322, "단계별로는 95% 성공하는 시스템이 20단계 작업의 3분의 2 가까이를 실패한다", W))
    return "".join(o), 340


reg("compounding-curve", W, _curve()[1],
    "단계별 성공률을 연쇄한 누적 실패 곡선. 단계별 95%는 20단계에서 약 36%로, 99%도 약 82%로 떨어진다.",
    _curve()[0])


# ------------------------------------------------- 3. inner / outer harness
def _rings():
    u, o = "inner-outer-harness", []
    o.append('<rect x="14" y="14" width="692" height="292" rx="14" class="d-box" stroke-dasharray="6 5"/>')
    o.append(text(30, 36, "루프 층 — 하트비트 · 비트 · 상태 파일 (다음 모듈)", 11.5, "start", "d-t d-dim", "700"))
    o.append('<rect x="60" y="52" width="600" height="228" rx="12" class="d-accent"/>')
    o.append(text(76, 74, "Outer harness — 내가 설정하고 구축한다", 12.5, "start", "d-t", "700"))
    o.append(chip_c(600, 60, "이 모듈의 무대", cls="d-chip-a", tcls="d-chip-a-t"))
    o.append('<rect x="140" y="92" width="440" height="130" rx="10" class="d-panel-2"/>')
    o.append(text(156, 114, "Inner harness — 모델 제작사가 만든다", 12, "start", "d-t", "700"))
    o.append(text(156, 132, "선택만 가능하고 편집은 불가능하다", 10.5, "start", "d-t d-dim"))
    o.append(box(230, 144, 260, 40, "모델", cls="d-strong", tsize=13))
    x = 156
    for lb in ["도구 호출", "컨텍스트 창", "안전 훈련"]:
        s, w = chip(x, 194, lb)
        o.append(s)
        x += w + 8
    x = 76
    for lb in ["도구", "permission", "hook", "검사", "로그"]:
        s, w = chip(x, 240, lb, cls="d-chip-a", tcls="d-chip-a-t")
        o.append(s)
        x += w + 8
    o.append(note(360, 330, "고치기 전에, 이 버그가 어느 링에 사는지부터 확인하라 — 프롬프트는 이번 작업을 위한 것이고 하니스는 모든 작업에 걸쳐 참이어야 하는 것을 위한 것이다", W))
    return "".join(o), 352


reg("inner-outer-harness", W, _rings()[1],
    "모델을 감싸는 두 개의 링. 안쪽 inner harness는 제작사가 만들어 선택만 가능하고, 바깥 outer harness는 사용자가 도구·permission·hook·검사·로그로 직접 구축한다.",
    _rings()[0])


# ------------------------------------------------- 4. five verbs
def _verbs():
    u, o = "five-verbs", []
    cards = [("Constrain", "제한", ["permission과 sandbox로", "할 수 있는 일을 좁힌다"]),
             ("Inform", "정보 제공", ["규칙 파일 · skill ·", "도구 설계로 필요한 것을 준다"]),
             ("Verify", "검증", ["hook · 테스트 ·", "typed output으로 증명한다"]),
             ("Correct", "교정", ["checkpoint로 실행을 복구하고", "ratchet으로 규칙을 조인다"]),
             ("Escalate", "이관", ["판단할 수 없으면 게이트와", "로그로 사람에게 보낸다"])]
    for i, (en, ko, subs) in enumerate(cards):
        x = i * 146
        o.append(box(x, 22, 136, 150, None, cls="d-box"))
        o.append(numchip(x + 68, 22, i + 1))
        o.append(text(x + 68, 62, en, 13, "middle", "d-t d-acc", "700"))
        o.append(text(x + 68, 80, ko, 11, "middle", "d-t d-dim"))
        o.append(line(x + 20, 92, x + 116, 92, "d-rule"))
        yy = 110
        for s in subs:
            for ln in wrap(s, 10.5, 118):
                o.append(text(x + 68, yy, ln, 10.5, "middle", "d-t"))
                yy += 15
    o.append(banner(0, 188, 720, 44, "가드레일은 하니스에 산다. 프롬프트에 살지 않는다."))
    return "".join(o), 244


reg("five-verbs", W, _verbs()[1],
    "하니스 엔지니어링의 다섯 동사 — 제한, 정보 제공, 검증, 교정, 이관. 가드레일은 프롬프트가 아니라 하니스에 산다.",
    _verbs()[0])


# ------------------------------------------------- 5. hook timeline
def _hook():
    u, o = "hook-timeline", []
    Y = 116
    o.append(line(20, Y, 700, Y, "d-axis"))
    o.append(text(20, Y - 46, "세션 시작", 11.5, "start", "d-t d-dim", "700"))
    o.append('<circle cx="24" cy="%g" r="5" class="d-dot"/>' % Y)
    # gate 1
    o.append('<rect x="150" y="%g" width="9" height="84" rx="3" class="d-gate"/>' % (Y - 42))
    o.append(text(154, Y - 54, "PreToolUse", 12, "middle", "d-t d-acc", "700"))
    o.append(text(154, Y + 60, "게이트 — 행동을 차단할 수 있다", 10.5, "middle", "d-t d-dim"))
    o.append(box(190, Y - 24, 176, 48, "도구 실행", ["Edit · Bash"], cls="d-strong", tsize=12))
    # post hook
    o.append('<circle cx="410" cy="%g" r="6" class="d-dot-a"/>' % Y)
    o.append(text(410, Y - 22, "PostToolUse", 12, "middle", "d-t d-acc", "700"))
    o.append(path_a("M 410 %g C 410 %g 452 %g 486 %g" % (Y + 8, Y + 62, Y + 74, Y + 74), u))
    o.append(box(488, Y + 50, 212, 48, "다음 턴의 입력이 된다",
                 ["에이전트가 스스로 고친다"], cls="d-accent", tsize=11.5))
    o.append(text(398, Y + 52, "피드백 — 되돌릴 수 없다", 10.5, "end", "d-t d-dim", halo=True))
    # gate 2
    o.append('<rect x="646" y="%g" width="9" height="84" rx="3" class="d-gate"/>' % (Y - 42))
    o.append(text(651, Y - 54, "Stop", 12, "middle", "d-t d-acc", "700"))
    o.append(text(716, Y - 74, "게이트 — 종료를 거부할 수 있다", 10.5, "end", "d-t d-dim"))
    o.append(note(360, 258, "벽은 행동 앞에 서고, 피드백은 행동 뒤에 흐른다. hook을 실행하는 주체는 모델이 아니라 하니스이므로 에이전트는 어느 쪽도 건너뛸 수 없다", W))
    return "".join(o), 292


reg("hook-timeline", W, _hook()[1],
    "한 비트의 타임라인 위에서 PreToolUse와 Stop은 행동과 종료를 차단하는 게이트로, PostToolUse는 되돌릴 수 없는 대신 다음 턴의 입력이 되는 피드백으로 작동한다.",
    _hook()[0])


# ------------------------------------------------- 6. failure class triage
def _triage():
    u, o = "failure-class-triage", []
    o.append(text(100, 20, "증상", 11.5, "middle", "d-t d-dim", "700"))
    o.append(text(330, 20, "failure class", 11.5, "middle", "d-t d-dim", "700"))
    o.append(text(600, 20, "고칠 표면", 11.5, "middle", "d-t d-dim", "700"))
    rows = [("몰랐다", "CONTEXT", "inform", "규칙 파일 · skill · 도구 설명"),
            ("금지된 것을 했다", "CONSTRAINT", "constrain", "permission 규칙 · sandbox · 울타리"),
            ("나쁜 작업이 완료로 통과", "VERIFICATION", "verify", "hook · 필수 CI · typed output"),
            ("재료는 맞는데 순서가 틀림", "PLANNING", "구조", "더 작은 작업 · 단계 상한 · subagent 분할")]
    y = 34
    for sym, cls_, verb, fix in rows:
        o.append(box(0, y, 200, 56, sym, cls="d-panel-2", tsize=11.5))
        o.append(arrow(202, y + 28, 228, y + 28, u))
        o.append(box(230, y, 200, 56, cls_ + " FAILURE", cls="d-accent", tsize=12))
        o.append(chip_c(330, y + 34, verb, cls="d-chip-a", tcls="d-chip-a-t", h=17))
        o.append(arrow(432, y + 28, 458, y + 28, u))
        o.append(box(460, y, 260, 56, fix, cls="d-box", tsize=11.5))
        y += 68
    o.append(note(360, y + 18, "class를 명명하고 그 표면에 수정을 써라. 같은 모양의 실패가 두 번 일어난다면 첫 번째 분류가 틀렸던 것이다", W))
    return "".join(o), y + 40


reg("failure-class-triage", W, _triage()[1],
    "에이전트 실패를 네 가지 class로 분류하는 지도. 증상에서 class를 거쳐 고쳐야 할 하니스 표면으로 이어진다.",
    _triage()[0])


# ------------------------------------------------- 7. the ratchet
def _ratchet():
    u, o = "the-ratchet", []
    o.append(box(240, 10, 240, 46, "① 에이전트가 실패한다", cls="d-warn", tsize=12))
    o.append(box(486, 92, 234, 78, "② failure class를 명명한다",
                 ["몰랐나 · 안 막혔나 ·", "안 검사됐나 · 계획이 나빴나"], cls="d-box", tsize=12))
    o.append(box(240, 206, 240, 78, "③ 그 class의 표면에 수정을 써넣는다",
                 ["규칙 · 울타리 · hook · 작업 분할"], cls="d-box", tsize=12))
    o.append(box(0, 92, 234, 78, "④ 하니스가 영구적으로 조여진다",
                 ["역회전에 잠긴다"], cls="d-ok", tsize=12))
    o.append(box(268, 108, 184, 62, "RATCHET", ["한 방향으로만 돈다"], cls="d-strong", tsize=13))
    o.append(path_a("M 482 34 C 560 34 603 52 603 88", u))
    o.append(path_a("M 603 174 C 603 214 540 240 484 244", u))
    o.append(path_a("M 238 244 C 180 240 117 214 117 174", u))
    o.append(path_a("M 117 88 C 117 52 162 34 238 34", u))
    o.append(text(600, 208, "다음 실패는", 10.5, "middle", "d-t d-dim", halo=True))
    o.append(text(120, 208, "새로운 실패다", 10.5, "middle", "d-t d-dim", halo=True))
    o.append(note(360, 316, "모델은 실행 사이에 아무것도 배우지 않는다. 여러분의 시스템이 배우는 곳은 하니스다", W))
    return "".join(o), 336


reg("the-ratchet", W, _ratchet()[1],
    "실수를 영구 부품으로 바꾸는 래칫 순환. 실패 → class 명명 → 해당 표면 수정 → 하니스가 조여짐으로 돌며 역회전하지 않는다.",
    _ratchet()[0])


# ------------------------------------------------- 8. eight boxes, two owners
def _eight():
    u, o = "eight-boxes-two-owners", []
    lg = [("도구 안에 산다", "d-own-tool"), ("플랫폼에 산다", "d-own-plat"), ("저장소 파일에 산다", "d-own-repo")]
    x = 130
    for lb, c in lg:
        o.append('<rect x="%g" y="8" width="13" height="13" rx="3" class="%s"/>' % (x, 8))
        o.append('<rect x="%g" y="8" width="13" height="13" rx="3" class="%s"/>' % (x, c))
        o.append(text(x + 19, 19, lb, 10.5, "start", "d-t d-dim"))
        x += tw(lb, 10.5) + 52
    o.append(hdr(180, 48, "Claude Code"))
    o.append(hdr(540, 48, "OpenCode"))
    rows = [("Deny 목록", "settings.json", "d-own-tool", "opencode.json", "d-own-tool"),
            ("울타리(sandbox)", "도구 내장", "d-own-tool", "컨테이너 · CI 러너", "d-own-plat"),
            ("적고 잘 설명된 도구", "도구 설정", "d-own-tool", "mcp 설정", "d-own-tool"),
            ("차단형 hook", "PreToolUse · Stop", "d-own-tool", "pre-commit · 필수 CI", "d-own-plat"),
            ("Typed verdict", "리뷰어 스킬", "d-own-repo", "리뷰어 스킬", "d-own-repo"),
            ("이관 경로", "HARNESS.md", "d-own-repo", "HARNESS.md", "d-own-repo"),
            ("실제로 읽을 로그", "세션 로그", "d-own-tool", "CI 워크플로 로그", "d-own-plat"),
            ("돌아갈 길", "/rewind · git", "d-own-tool", "git 커밋", "d-own-repo")]
    y = 62
    for name, l, lc, r, rc in rows:
        o.append(text(4, y + 22, name, 11, "start", "d-t d-dim"))
        o.append(box(150, y, 210, 34, l, cls=lc, tsize=11, tweight=None))
        o.append(box(430, y, 220, 34, r, cls=rc, tsize=11, tweight=None))
        y += 42
    o.append(note(360, y + 16, "같은 여덟 상자, 다른 주인 — 속성은 그대로 이전되고 주소만 바뀐다", W))
    return "".join(o), y + 36


reg("eight-boxes-two-owners", W, _eight()[1],
    "최소 안전 하니스의 여덟 상자를 Claude Code와 OpenCode에서 각각 누가 소유하는지 비교한다. 같은 항목이라도 도구·플랫폼·저장소 중 어디에 사는지가 달라진다.",
    _eight()[0])
