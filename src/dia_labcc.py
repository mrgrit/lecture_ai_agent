# -*- coding: utf-8 -*-
"""Lab-track diagrams — hands-on with Claude Code."""
from svglib import *   # noqa

W = 720
D = {}


def reg(uid, w, h, aria, body):
    D[uid] = svg(uid, w, h, aria, body)


# ---------------------------------------------------------------- 1. lab map
def _map():
    u, o = "cc-lab-map", []
    groups = [("실습 0", "준비", "3개", "설치 · 관측"),
              ("실습 1", "스킬과 커넥터", "4개", "모듈 1"),
              ("실습 2", "하니스", "5개", "모듈 2"),
              ("실습 3", "루프", "4개", "모듈 3"),
              ("실습 4", "기억과 그래프", "3개", "모듈 4"),
              ("실습 5", "명세 주도 개발", "4개", "모듈 5")]
    bw, gap = 108, 14
    for i, (g, t, n, sub) in enumerate(groups):
        x = i * (bw + gap)
        o.append(box(x, 26, bw, 78, t, [n], cls="d-accent" if i else "d-box",
                     tsize=11.5, ssize=10))
        o.append(chip_c(x + bw / 2, 4, g))
        o.append(note(x + bw / 2, 122, sub, bw + 12, size=9.5))
        if i < len(groups) - 1:
            o.append(arrow_a(x + bw + 1, 65, x + bw + gap - 2, 65, u))
    o.append(line(0, 146, W, 146, "d-rule", dash=True))
    o.append(hdr(360, 172, "스물세 개를 다 하면 손에 남는 여덟 조각"))
    pieces = ["스킬", "커넥터", "권한·훅", "게이트", "감시 루프", "상태 파일",
              "발자국 그래프", "근거 검증기"]
    pw, pg = 84, 6
    for i, p in enumerate(pieces):
        o.append(box(i * (pw + pg), 186, pw, 40, p, cls="d-box", tsize=11))
    o.append(banner(120, 240, 480, 40, "조립하면 = 밤새 도는 신뢰할 수 있는 에이전트"))
    return "".join(o), 292


reg("cc-lab-map", W, _map()[1],
    "Claude Code 실습편은 준비 3개, 스킬과 커넥터 4개, 하니스 5개, 루프 4개, 기억과 그래프 3개, 명세 주도 개발 4개로 구성되며 각각 강의 모듈 1에서 5에 대응한다. 스물세 개를 마치면 스킬·커넥터·권한과 훅·게이트·감시 루프·상태 파일·발자국 그래프·근거 검증기 여덟 조각이 남고, 이를 조립하면 밤새 도는 에이전트가 된다.",
    _map()[0])


# ---------------------------------------------------------------- 2. hook points
def _hooks():
    u, o = "cc-hook-points", []
    o.append(hdr(360, 16, "한 턴 안에서 훅이 끼어드는 자리"))
    stops = ["사용자 요청", "모델이 도구를 고름", "도구 실행", "결과 반영",
             "끝내려 함", "턴 종료"]
    bw, gap = 108, 14
    for i, t in enumerate(stops):
        x = i * (bw + gap)
        o.append(box(x, 40, bw, 52, t, cls="d-box", tsize=11))
        if i < len(stops) - 1:
            o.append(arrow(x + bw, 66, x + bw + gap - 2, 66, u))
    o.append(box(122, 112, 200, 62, "PreToolUse",
                 ["실행되기 직전에 가로챈다", "C2-3 · rm 차단 훅"],
                 cls="d-accent", tsize=11.5))
    o.append(arrow_a(222, 112, 222, 96, u))
    o.append(box(462, 112, 200, 62, "Stop",
                 ["끝내려 할 때 가로챈다", "C2-4 · 테스트 게이트"],
                 cls="d-accent", tsize=11.5))
    o.append(arrow_a(562, 112, 562, 96, u))
    o.append(line(0, 190, W, 190, "d-rule", dash=True))
    o.append(box(0, 204, 350, 66, "막으면 무슨 일이 일어나나",
                 ["도구는 실행되지 않고, 표준 에러에 쓴 문장이",
                  "모델에게 전달된다 → 모델이 대안을 찾는다"],
                 cls="d-ok", tsize=11.5))
    o.append(box(370, 204, 350, 66, "훅이 없으면 어떻게 되나",
                 ["기본 동작은 '그냥 실행' 이다.",
                  "훅 파일의 존재를 바깥에서 보장해야 한다"],
                 cls="d-warn", tsize=11.5))
    return "".join(o), 282


reg("cc-hook-points", W, _hooks()[1],
    "한 턴은 사용자 요청, 모델의 도구 선택, 도구 실행, 결과 반영, 종료 시도, 턴 종료로 진행된다. PreToolUse 훅은 도구가 실행되기 직전을 가로채고, Stop 훅은 에이전트가 끝내려 할 때를 가로챈다. 막으면 표준 에러에 쓴 차단 사유가 모델에게 전달되어 모델이 대안을 찾으며, 훅 파일이 없으면 기본 동작은 그냥 실행이므로 파일의 존재를 바깥에서 보장해야 한다.",
    _hooks()[0])


# ---------------------------------------------------------------- 3. gate effect
def _gate():
    u, o = "cc-gate-effect", []
    o.append(hdr(360, 16, "감시 게이트가 있을 때와 없을 때 (실측)"))
    rows = [("1회차 · 최초 관측", 13.0, "모델 호출", True),
            ("2회차 · 변화 없음", 0.2, "억제 — 모델 호출 없음", False),
            ("3회차 · 편지 1통 추가", 20.0, "모델 호출", True)]
    x0, scale = 176, 400 / 20.0
    for i, (label, sec, note_s, hot) in enumerate(rows):
        y = 44 + i * 52
        o.append(text(168, y + 22, label, 11.5, "end", "d-t", "700"))
        bw = max(sec * scale, 4)
        o.append('<rect x="%g" y="%g" width="%g" height="%g" rx="5" class="%s"/>'
                 % (x0, y + 6, bw, 28, "d-accent" if hot else "d-ok"))
        o.append(text(x0 + bw + 10, y + 25,
                      "%s초" % ("%.1f" % sec if sec < 1 else int(sec)),
                      11.5, "start", "d-t", "700"))
        o.append(text(716, y + 25, note_s, 10.5, "end", "d-t d-dim"))
    o.append(line(0, 206, W, 206, "d-rule", dash=True))
    o.append(box(0, 220, 350, 70, "억제된 한 틱이 아낀 것",
                 ["응답 한 번이 아니라 문맥 전송 한 번 전체",
                  "평균 2만 캐시 읽기 토큰"],
                 cls="d-ok", tsize=11.5))
    o.append(box(370, 220, 350, 70, "게이트가 무력화되는 경우",
                 ["관측 출력에 시각·난수가 섞이면",
                  "매 틱이 '변화' 가 되어 절약이 0이 된다"],
                 cls="d-warn", tsize=11.5))
    return "".join(o), 302


reg("cc-gate-effect", W, _gate()[1],
    "감시 게이트 실측 결과. 최초 관측은 약 13초로 모델을 호출했고, 변화가 없는 2회차는 0.2초로 모델 호출 없이 억제되었으며, 편지가 추가된 3회차는 약 20초로 다시 모델을 호출했다. 억제된 한 틱이 아낀 것은 응답 한 번이 아니라 평균 2만 캐시 읽기 토큰에 해당하는 문맥 전송 전체다. 관측 출력에 시각이나 난수가 섞이면 매 틱이 변화로 판정되어 절약이 사라진다.",
    _gate()[0])


# ---------------------------------------------------------------- 4. resume loop
def _resume():
    u, o = "cc-resume-loop", []
    o.append(hdr(360, 16, "깨어날 때마다 하나씩, 끝나면 스스로 멈춘다"))
    runs = [("1회차", "커서 0 → 1", "done.md 1줄", True),
            ("2회차", "커서 1 → 2", "done.md 2줄", True),
            ("3회차", "커서 2 → 3", "done.md 3줄", True),
            ("4회차", "커서 3 유지", "아무것도 안 함", False)]
    bw, gap = 168, 16
    for i, (t, c, r, act) in enumerate(runs):
        x = i * (bw + gap)
        o.append(box(x, 38, bw, 76, t, [c, r],
                     cls="d-accent" if act else "d-ok", tsize=12, ssize=10.5))
        if i < 3:
            o.append(arrow_a(x + bw + 1, 76, x + bw + gap - 2, 76, u))
    o.append(check(700, 76, 9))
    o.append(note(360, 134,
                  "Hermes 는 잡마다 notepad 를 내장 제공한다. Claude Code 에는 없으므로 state.json 을 직접 만든다",
                  W - 20))
    o.append(line(0, 158, W, 158, "d-rule", dash=True))
    o.append(box(0, 172, 232, 76, "상태가 없으면",
                 ["매번 처음부터 하거나", "한 일을 또 한다"],
                 cls="d-bad-box", tsize=11.5))
    o.append(box(244, 172, 232, 76, "상태가 있으면",
                 ["어디까지 했는지 알고", "이어서 한다"],
                 cls="d-ok", tsize=11.5))
    o.append(box(488, 172, 232, 76, "종료 조건이 없으면",
                 ["없는 항목을 지어내거나", "영원히 돈다"],
                 cls="d-warn", tsize=11.5))
    return "".join(o), 260


reg("cc-resume-loop", W, _resume()[1],
    "상태를 쓰는 이어하기 루프. 1회차에 커서가 0에서 1로 오르며 done.md 한 줄이 생기고, 2회차와 3회차가 같은 식으로 진행되어 세 줄이 되며, 4회차는 커서가 항목 수에 도달해 아무것도 하지 않고 끝난다. Hermes 는 notepad 를 내장 제공하지만 Claude Code 에서는 state.json 을 직접 만든다. 상태가 없으면 매번 처음부터 하거나 한 일을 또 하고, 종료 조건이 없으면 없는 항목을 지어내거나 영원히 돈다.",
    _resume()[0])


# ---------------------------------------------------------------- 5. three memories
def _mem():
    u, o = "cc-three-memories", []
    o.append(hdr(360, 16, "기억의 세 층과 각각의 수명"))
    layers = [("문맥", "모델의 입력", "한 턴", "다음 호출에서 사라진다", "d-bad-box"),
              ("대화 기록", "~/.claude/projects/*.jsonl", "한 세션",
               "--continue 로만 이어진다", "d-accent"),
              ("프로젝트 기억", "CLAUDE.md", "영구",
               "모든 세션이 자동으로 읽는다", "d-ok")]
    for i, (t, where, life, note_s, cls) in enumerate(layers):
        y = 40 + i * 72
        o.append(box(0, y, 200, 56, t, [where], cls=cls, tsize=12, ssize=9.5))
        o.append(arrow_a(202, y + 28, 250, y + 28, u))
        o.append(box(252, y, 132, 56, life, cls="d-box", tsize=12))
        o.append(text(400, y + 32, note_s, 11, "start", "d-t d-dim"))
    o.append(line(0, 262, W, 262, "d-rule", dash=True))
    o.append(box(0, 276, 350, 68, "왜 git 으로 추적해야 하나",
                 ["CLAUDE.md 는 에이전트도 쓸 수 있다.",
                  "잘못 적히면 이후 모든 세션이 그것을 믿는다"],
                 cls="d-warn", tsize=11.5))
    o.append(box(370, 276, 350, 68, "자동화에서 --continue 가 위험한 이유",
                 ["'마지막 대화' 라는 암묵적 대상을 쓴다.",
                  "--session-id 로 명시하는 편이 옳다"],
                 cls="d-warn", tsize=11.5))
    return "".join(o), 356


reg("cc-three-memories", W, _mem()[1],
    "기억은 세 층이다. 문맥은 모델의 입력으로 한 턴만 살고 다음 호출에서 사라진다. 대화 기록은 홈 폴더의 프로젝트별 JSONL 파일에 한 세션 동안 남고 --continue 로만 이어진다. 프로젝트 기억은 CLAUDE.md 로 영구히 남으며 모든 세션이 자동으로 읽는다. CLAUDE.md 는 에이전트도 쓸 수 있어 잘못 적히면 이후 모든 세션이 믿게 되므로 git 으로 추적해야 하고, 자동화에서는 마지막 대화라는 암묵적 대상을 쓰는 --continue 보다 --session-id 로 명시하는 편이 옳다.",
    _mem()[0])


# ---------------------------------------------------------------- 6. grounded
def _grounded():
    u, o = "cc-grounded-cc", []
    o.append(hdr(360, 16, "주장마다 근거를 달고, 근거를 기계가 대조한다"))
    o.append(box(0, 36, 200, 78, "source.md", ["원문 — 유일한 진실"], cls="d-box"))
    o.append(arrow_a(202, 75, 258, 75, u, "--json-schema"))
    o.append(box(260, 36, 200, 78, "claims.json",
                 ["claim: 주장 한 문장", "quote: 원문에서 그대로 복사"],
                 cls="d-accent", tsize=12, ssize=10.5))
    o.append(arrow_a(462, 75, 518, 75, u))
    o.append(box(520, 36, 200, 78, "check_claims.py",
                 ["quote 가 source.md 안에", "문자 그대로 있는가"],
                 cls="d-strong", tsize=12, ssize=10.5))
    o.append(box(376, 152, 150, 44, "exit 0 · PASS", cls="d-ok", tsize=12))
    o.append(box(556, 152, 164, 44, "exit 1 · 근거 없음", cls="d-bad-box", tsize=12))
    o.append(arrow_a(612, 118, 470, 148, u))
    o.append(arrow_a(628, 118, 636, 148, u))
    o.append(line(0, 208, W, 208, "d-rule", dash=True))
    o.append(box(0, 222, 350, 76, "이 검증기에는 LLM 이 없다",
                 ["문자열 포함 검사뿐 — 결과가 결정적이고",
                  "절대 거짓말하지 않는다"],
                 cls="d-ok", tsize=11.5))
    o.append(box(370, 222, 350, 76, "환각은 창작이 아니라 미세한 변형이다",
                 ["'도입하지 않는다' 에서 '않는다' 가 빠지면",
                  "정반대가 된다. 사람 눈으로는 안 잡힌다"],
                 cls="d-warn", tsize=11.5))
    return "".join(o), 310


reg("cc-grounded-cc", W, _grounded()[1],
    "근거 기반 검증 흐름. 원문 source.md 에서 요약을 만들되 --json-schema 로 출력을 강제해 claims.json 에 주장과 원문에서 그대로 복사한 근거를 쌍으로 남기고, check_claims.py 가 근거 문자열이 원문 안에 문자 그대로 있는지 대조해 종료 코드 0 또는 1 을 낸다. 이 검증기에는 LLM 이 없어 결과가 결정적이며, 환각의 흔한 형태가 완전한 창작이 아니라 부정어가 빠지는 식의 미세한 변형이므로 문자열 대조가 필요하다.",
    _grounded()[0])


# ---------------------------------------------------------------- 7. spec vs none
def _sdd():
    u, o = "cc-spec-vs-none", []
    o.append(hdr(360, 16, "같은 시험지로 채점한 두 라운드"))
    o.append(note(360, 32, "시험지 15문항은 두 라운드 시작 전에 미리 만들고, 에이전트에게 보여 주지 않는다", W - 40))

    iy = 56
    o.append(panel(0, iy, 350, 150, "라운드 A · 한 줄 요청",
                   "\"1h30m 을 초로 바꾸는 함수 만들어라\"", cls="d-bad-box")[0])
    o.append(panel(370, iy, 350, 150, "라운드 B · 명세 요청",
                   "spec.md 38줄을 먼저 쓰고 시킨다", cls="d-ok")[0])

    for x0, passed, total, code, tag in ((14, 11, 15, "코드 12줄", "d-bad-s"),
                                         (384, 15, 15, "코드 31줄", "d-ok-s")):
        for i in range(total):
            cx = x0 + 8 + (i % 8) * 39
            cy = iy + 74 + (i // 8) * 26
            if i < passed:
                o.append(check(cx, cy, 7))
            else:
                o.append(cross(cx, cy, 7))
        o.append(text(x0 + 8, iy + 134, "%d/%d 통과 · %s" % (passed, total, code),
                      11.5, "start", "d-t", "700"))

    o.append(line(0, 220, W, 220, "d-rule", dash=True))
    o.append(box(0, 234, 350, 78, "A 의 실패는 전부 경계 사례다",
                 ["대문자 · 빈 문자열 · 중복 단위 · 소수.",
                  "코드가 틀린 게 아니라 답한 질문이 좁았다"],
                 cls="d-warn", tsize=11.5))
    o.append(box(370, 234, 350, 78, "명세 38줄 > 코드 12줄",
                 ["명세를 안 썼다면 그 38줄만큼의 결정을",
                  "모델이 대신 했다. 사라진 게 아니다"],
                 cls="d-ok", tsize=11.5))
    return "".join(o), 324


reg("cc-spec-vs-none", W, _sdd()[1],
    "같은 함수를 두 번 만들어 미리 만든 열다섯 문항 시험지로 채점한 결과. 한 줄로 요청한 라운드 A 는 열한 문항을 통과하고 코드는 열두 줄이며, 명세 서른여덟 줄을 먼저 쓴 라운드 B 는 열다섯 문항을 모두 통과하고 코드는 서른한 줄이다. 라운드 A 의 실패는 전부 대문자, 빈 문자열, 중복 단위, 소수 같은 경계 사례이며 코드가 틀린 것이 아니라 답한 질문이 좁았던 것이다. 명세가 코드보다 길지만, 명세를 쓰지 않았다면 그만큼의 결정을 모델이 대신 한 것이다.",
    _sdd()[0])


# ---------------------------------------------------------------- 8. drift sections
def _drift():
    u, o = "cc-drift-sections", []
    o.append(hdr(360, 16, "절을 구분하지 않으면 금지가 약속으로 읽힌다"))

    o.append(box(0, 40, 208, 128, "spec.md",
                 ["## 기능 요구사항", "## 경계 사례와 규칙", "## 수용 기준",
                  "## 범위 밖  ← 금지 목록"],
                 cls="d-box", tsize=12, ssize=10))
    o.append(box(0, 180, 208, 46, "duration.py", ["'d' 단위 · 공백 허용 추가됨"],
                 cls="d-bad-box", tsize=12, ssize=10))

    o.append(arrow_a(210, 96, 262, 96, u))
    o.append(panel(264, 40, 456, 88, "순진한 검사기",
                   "명세 전체에서 '일' · '공백' 을 찾는다 → 둘 다 있다 → 통과",
                   cls="d-bad-box")[0])
    o.append(box(292, 84, 130, 32, "표류 0건", cls="d-bad-box", tsize=11.5))
    o.append(text(438, 105, "틀린 답이다. 단어가 있던 자리가 '범위 밖' 이었다",
                  10.5, "start", "d-t d-dim"))

    o.append(arrow_a(210, 202, 262, 202, u))
    o.append(panel(264, 146, 456, 88, "절 인식 검사기",
                   "약속한 절과 금지한 절을 따로 본다",
                   cls="d-ok")[0])
    o.append(box(292, 190, 130, 32, "CONFLICT 2건", cls="d-ok", tsize=11.5))
    o.append(text(438, 211, "금지된 것이 코드에 있다고 정확히 판정한다",
                  10.5, "start", "d-t d-dim"))

    o.append(line(0, 248, W, 248, "d-rule", dash=True))
    o.append(box(0, 262, 350, 76, "게이트는 초과 표류를 못 잡는다",
                 ["테스트는 있는 것만 검사한다.",
                  "수용 기준 17개는 전부 통과했다"],
                 cls="d-warn", tsize=11.5))
    o.append(box(370, 262, 350, 76, "판정기를 신뢰하는 유일한 근거",
                 ["그것이 실패를 잡는 것을",
                  "본 적이 있다는 사실"],
                 cls="d-ok", tsize=11.5))
    return "".join(o), 350


reg("cc-drift-sections", W, _drift()[1],
    "명세 표류 검사기의 두 버전 비교. 명세에는 기능 요구사항, 경계 사례와 규칙, 수용 기준, 그리고 금지 목록인 범위 밖 절이 있고, 코드에는 범위 밖에 적힌 일 단위와 공백 허용이 추가되어 있다. 순진한 검사기는 명세 전체에서 단어만 찾아 표류 0건이라는 틀린 답을 내는데, 그 단어가 있던 자리가 범위 밖 절이었기 때문이다. 절을 구분하는 검사기는 약속한 절과 금지한 절을 따로 보아 CONFLICT 두 건을 정확히 잡는다. 테스트 게이트는 있는 것만 검사하므로 초과 표류를 잡지 못하며, 판정기를 신뢰하는 유일한 근거는 그것이 실패를 잡는 것을 본 적이 있다는 사실이다.",
    _drift()[0])
