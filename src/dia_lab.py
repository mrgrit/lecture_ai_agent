# -*- coding: utf-8 -*-
"""Lab-track diagrams — hands-on with Hermes."""
from svglib import *   # noqa

W = 720
D = {}


def reg(uid, w, h, aria, body):
    D[uid] = svg(uid, w, h, aria, body)


# ---------------------------------------------------------------- 1. lab map
def _map():
    u, o = "lab-map", []
    groups = [("실습 0", "준비", "3개", "설치 · 서버 연결 · 첫 대화"),
              ("실습 1", "스킬과 커넥터", "4개", "모듈 1"),
              ("실습 2", "하니스", "5개", "모듈 2"),
              ("실습 3", "루프", "4개", "모듈 3"),
              ("실습 4", "기억과 그래프", "3개", "모듈 4")]
    bw, gap = 132, 15
    for i, (g, t, n, sub) in enumerate(groups):
        x = i * (bw + gap)
        o.append(box(x, 26, bw, 78, t, [n], cls="d-accent" if i else "d-box",
                     tsize=12, ssize=10.5))
        o.append(chip_c(x + bw / 2, 4, g))
        o.append(note(x + bw / 2, 122, sub, bw + 10, size=10))
        if i < 4:
            o.append(arrow_a(x + bw + 1, 65, x + bw + gap - 2, 65, u))
    o.append(line(0, 146, W, 146, "d-rule", dash=True))
    o.append(hdr(360, 172, "열아홉 개를 다 하면 손에 남는 여덟 조각"))
    pieces = ["스킬", "커넥터", "승인·훅", "게이트", "감시 루프", "메모장", "기억·그래프", "근거 검증기"]
    pw, pg = 84, 6
    for i, p in enumerate(pieces):
        o.append(box(i * (pw + pg), 186, pw, 40, p, cls="d-box", tsize=11))
    o.append(banner(120, 240, 480, 40, "조립하면 = 밤새 도는 신뢰할 수 있는 에이전트"))
    return "".join(o), 292


reg("lab-map", W, _map()[1],
    "실습편은 준비 3개, 스킬과 커넥터 4개, 하니스 5개, 루프 4개, 기억과 그래프 3개로 구성되며 각각 강의 모듈 1에서 4에 대응한다. 열아홉 개를 마치면 스킬·커넥터·승인과 훅·게이트·감시 루프·메모장·기억 그래프·근거 검증기 여덟 조각이 남고, 이를 조립하면 밤새 도는 에이전트가 된다.",
    _map()[0])


# ---------------------------------------------------------------- 2. hook points
def _hooks():
    u, o = "lab-hook-points", []
    o.append(hdr(360, 16, "한 턴 안에서 훅이 끼어드는 두 지점"))
    stops = [("사용자 요청", 0), ("모델이 도구를 고름", 1), ("도구 실행", 2),
             ("결과 반영", 3), ("끝내려 함", 4), ("턴 종료", 5)]
    bw, gap = 108, 14
    for t, i in stops:
        x = i * (bw + gap)
        cls = "d-box"
        o.append(box(x, 40, bw, 52, t, cls=cls, tsize=11))
        if i < 5:
            o.append(arrow(x + bw, 66, x + bw + gap - 2, 66, u))
    # pre_tool_call gate
    o.append(box(122, 112, 200, 62, "pre_tool_call",
                 ["실행되기 직전에 가로챈다", "L2-3 · rm 차단 훅"], cls="d-accent", tsize=11.5))
    o.append(arrow_a(222, 112, 222, 96, u))
    # pre_verify gate
    o.append(box(462, 112, 200, 62, "pre_verify",
                 ["끝내려 할 때 가로챈다", "L2-4 · 테스트 게이트"], cls="d-accent", tsize=11.5))
    o.append(arrow_a(562, 112, 562, 96, u))
    o.append(line(0, 190, W, 190, "d-rule", dash=True))
    o.append(box(0, 204, 350, 66, "막으면 무슨 일이 일어나나",
                 ["도구는 실행되지 않고, 차단 사유 문장이", "모델에게 전달된다 → 모델이 대안을 찾는다"],
                 cls="d-ok", tsize=11.5))
    o.append(box(370, 204, 350, 66, "fail_closed 를 켜면",
                 ["스크립트 없음 · 타임아웃 · 깨진 JSON 도", "전부 '차단'으로 바뀐다 (보안 게이트의 기본값)"],
                 cls="d-warn", tsize=11.5))
    return "".join(o), 282


reg("lab-hook-points", W, _hooks()[1],
    "한 턴은 사용자 요청, 모델의 도구 선택, 도구 실행, 결과 반영, 종료 시도, 턴 종료로 진행된다. pre_tool_call 훅은 도구가 실행되기 직전을 가로채고, pre_verify 훅은 에이전트가 끝내려 할 때를 가로챈다. 막으면 차단 사유가 모델에게 전달되어 모델이 대안을 찾으며, fail_closed 를 켜면 훅 자체의 실패도 차단으로 처리된다.",
    _hooks()[0])


# ---------------------------------------------------------------- 3. monitor gate timing
def _timing():
    u, o = "lab-gate-timing", []
    o.append(hdr(360, 16, "감시 게이트가 있을 때와 없을 때 (실측)"))
    rows = [("1회차 · 최초 관측", 68.0, "모델 호출", True),
            ("2회차 · 변화 없음", 0.49, "억제 — 모델 호출 없음", False),
            ("3회차 · 파일 1개 추가", 56.0, "모델 호출", True)]
    x0, maxw, scale = 168, 420, 420 / 68.0
    for i, (label, sec, note_s, hot) in enumerate(rows):
        y = 44 + i * 52
        o.append(text(160, y + 22, label, 11.5, "end", "d-t", "700"))
        bw = max(sec * scale, 4)
        o.append('<rect x="%g" y="%g" width="%g" height="%g" rx="5" class="%s"/>'
                 % (x0, y + 6, bw, 28, "d-accent" if hot else "d-ok"))
        o.append(text(x0 + bw + 10, y + 25, "%s초" % ("%.2f" % sec if sec < 1 else int(sec)),
                      11.5, "start", "d-t", "700"))
        o.append(text(x0 + bw + 10, y + 25, "", 11.5, "start", "d-t"))
        o.append(text(716, y + 25, note_s, 10.5, "end", "d-t d-dim"))
    o.append(line(0, 206, W, 206, "d-rule", dash=True))
    o.append(box(0, 220, 350, 70, "억제된 한 틱이 아낀 것",
                 ["응답 한 번이 아니라 문맥 전송 한 번 전체", "약 14,000 입력 토큰"],
                 cls="d-ok", tsize=11.5))
    o.append(box(370, 220, 350, 70, "게이트가 무력화되는 경우",
                 ["감시 스크립트 출력에 시각·난수가 섞이면", "매 틱이 '변화'가 되어 절약이 0이 된다"],
                 cls="d-warn", tsize=11.5))
    return "".join(o), 302


reg("lab-gate-timing", W, _timing()[1],
    "감시 게이트 실측 결과. 최초 관측은 68초로 모델을 호출했고, 변화가 없는 2회차는 0.49초로 모델 호출 없이 억제되었으며, 파일이 추가된 3회차는 56초로 다시 모델을 호출했다. 억제된 한 틱이 아낀 것은 응답 한 번이 아니라 약 14,000 입력 토큰에 해당하는 문맥 전송 전체다. 감시 스크립트 출력에 시각이나 난수가 섞이면 매 틱이 변화로 판정되어 절약이 사라진다.",
    _timing()[0])


# ---------------------------------------------------------------- 4. notepad loop
def _notepad():
    u, o = "lab-notepad-loop", []
    o.append(hdr(360, 16, "깨어날 때마다 하나씩, 끝나면 스스로 멈춘다"))
    runs = [("1회차", "cursor 1 → 2", "done.md 1줄", True),
            ("2회차", "cursor 2 → 3", "done.md 2줄", True),
            ("3회차", "cursor 3 → 4", "done.md 3줄", True),
            ("4회차", "cursor 4 유지", "아무것도 안 함", False)]
    bw, gap = 168, 16
    for i, (t, c, r, act) in enumerate(runs):
        x = i * (bw + gap)
        o.append(box(x, 38, bw, 76, t, [c, r],
                     cls="d-accent" if act else "d-ok", tsize=12, ssize=10.5))
        if i < 3:
            o.append(arrow_a(x + bw + 1, 76, x + bw + gap - 2, 76, u))
    o.append(check(700, 76, 9))
    o.append(note(360, 134, "메모장(notepad)은 잡마다 붙는 작은 키-값 저장소이고, 깨어날 때마다 프롬프트 앞에 자동으로 붙는다", W - 20))
    o.append(line(0, 158, W, 158, "d-rule", dash=True))
    o.append(box(0, 172, 232, 76, "상태가 없으면",
                 ["매번 처음부터 하거나", "한 일을 또 한다"], cls="d-bad-box", tsize=11.5))
    o.append(box(244, 172, 232, 76, "상태가 있으면",
                 ["어디까지 했는지 알고", "이어서 한다"], cls="d-ok", tsize=11.5))
    o.append(box(488, 172, 232, 76, "종료 조건이 없으면",
                 ["없는 항목을 지어내거나", "영원히 돈다"], cls="d-warn", tsize=11.5))
    return "".join(o), 260


reg("lab-notepad-loop", W, _notepad()[1],
    "메모장을 쓰는 이어하기 루프. 1회차에 커서가 1에서 2로 오르며 done.md 한 줄이 생기고, 2회차와 3회차가 같은 식으로 진행되어 세 줄이 되며, 4회차는 커서가 항목 수를 넘어 아무것도 하지 않고 끝난다. 상태가 없으면 매번 처음부터 하거나 한 일을 또 하고, 종료 조건이 없으면 없는 항목을 지어내거나 영원히 돈다.",
    _notepad()[0])


# ---------------------------------------------------------------- 5. grounded checker
def _grounded():
    u, o = "lab-grounded", []
    o.append(hdr(360, 16, "주장마다 근거를 달고, 근거를 기계가 대조한다"))
    o.append(box(0, 36, 200, 78, "source.md", ["원문 — 유일한 진실"], cls="d-box"))
    o.append(arrow_a(202, 75, 258, 75, u, "요약 생성"))
    o.append(box(260, 36, 200, 78, "claims.json",
                 ["claim: 주장 한 문장", "quote: 원문에서 그대로 복사"], cls="d-accent", tsize=12, ssize=10.5))
    o.append(arrow_a(462, 75, 518, 75, u))
    o.append(box(520, 36, 200, 78, "check_claims.py",
                 ["quote 가 source.md 안에", "문자 그대로 있는가"], cls="d-strong", tsize=12, ssize=10.5))
    o.append(box(376, 152, 150, 44, "PASS", cls="d-ok", tsize=12))
    o.append(box(556, 152, 164, 44, "FAIL — 근거 없음", cls="d-bad-box", tsize=12))
    o.append(arrow_a(612, 118, 470, 148, u))
    o.append(arrow_a(628, 118, 636, 148, u))
    o.append(line(0, 208, W, 208, "d-rule", dash=True))
    o.append(box(0, 222, 350, 76, "이 검증기에는 LLM이 없다",
                 ["문자열 포함 검사뿐 — 결과가 결정적이고", "절대 거짓말하지 않는다"],
                 cls="d-ok", tsize=11.5))
    o.append(box(370, 222, 350, 76, "판정자는 대상보다 단순해야 한다",
                 ["LLM으로 근거를 판정하면 그 판정이", "다시 검증 대상이 되어 원점으로 돌아간다"],
                 cls="d-warn", tsize=11.5))
    return "".join(o), 310


reg("lab-grounded", W, _grounded()[1],
    "근거 기반 검증 흐름. 원문 source.md 에서 요약을 생성하되 claims.json 에 주장과 원문에서 그대로 복사한 근거를 쌍으로 남기고, check_claims.py 가 근거 문자열이 원문 안에 문자 그대로 있는지 대조해 PASS 또는 근거 없음 FAIL 을 낸다. 이 검증기에는 LLM이 없어 결과가 결정적이며, 판정자는 판정 대상보다 단순해야 한다는 원칙을 따른다.",
    _grounded()[0])
