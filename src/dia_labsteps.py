# -*- coding: utf-8 -*-
"""Step-by-step lab-track diagrams — one command, one check."""
from svglib import *   # noqa

W = 720
D = {}


def reg(uid, w, h, aria, body):
    D[uid] = svg(uid, w, h, aria, body)


# ------------------------------------------------------- 1. shape of one step
def _shape():
    u, o = "s-step-shape", []
    PH = 352

    s, ix, iy, iw, _ = panel(0, 0, 330, PH, "C 트랙 — 한 덩어리",
                             "붙여넣고 결과를 기다린다", chip="검증용")
    o.append(s)
    code = ['claude -p "..." \\', '  --output-format json |', 'python3 -c "',
            '  import sys, json', '  d = json.load(sys.stdin)', "  print(d['usage'][...])", '"']
    o.append('<rect x="%g" y="%g" width="%g" height="%g" rx="7" class="d-bad-box"/>'
             % (ix, iy + 4, iw, 132))
    for i, ln in enumerate(code):
        o.append(text(ix + 12, iy + 26 + i * 15.5, ln, 10.5, "start", "d-t d-mono"))
    o.append(text(ix, iy + 160, "여기서 학생이 멈춘다", 11.5, "start", "d-t d-bad", "700"))
    o.append(note(ix + iw / 2, iy + 182,
                  "에이전트를 배우러 와서 JSON 파싱 코드를 해석하고 있다. "
                  "실습의 주제와 상관없는 곳에서 시간이 샌다.", iw, size=10.5))
    o.append(box(ix, iy + 234, iw, 34, "결과 한 덩어리 · 어디서 틀렸는지 모른다",
                 cls="d-warn", tsize=11))

    s2, jx, jy, jw, _ = panel(370, 0, 350, PH, "S 트랙 — 한 줄씩",
                              "명령 하나 · 확인 하나 · 다음", chip="따라 하기용",
                              chip_cls="d-chip-a")
    o.append(s2)
    steps = [('claude -p "..." > 답.txt', "답이 파일로 간다"),
             ("cat 답.txt", "눈으로 본다"),
             ("grep -c '⟪마커⟫' 답.txt", "1 이면 성공"),
             ('grep -o \'"num_turns":[0-9]*\'', "턴 수를 본다")]
    y = jy + 2
    for i, (cmd, why) in enumerate(steps):
        o.append(numchip(jx + 12, y + 17, i + 1))
        o.append(box(jx + 30, y, jw - 30, 34, cmd, cls="d-box", tsize=10.5,
                     tcls="d-t d-mono"))
        o.append(text(jx + 36, y + 48, "→ " + why, 10, "start", "d-t d-dim"))
        if i < len(steps) - 1:
            o.append(arrow_a(jx + 12, y + 30, jx + 12, y + 54, u))
        y += 58
    o.append(box(jx, jy + 234, jw, 34, "틀린 단계에서 바로 멈춘다", cls="d-ok", tsize=11))

    o.append(line(0, PH + 18, W, PH + 18, "d-rule", dash=True))
    o.append(hdr(360, PH + 42, "두 트랙은 같은 스물세 개다. 다른 것은 쪼갠 크기뿐이다."))
    return "".join(o), PH + 56


reg("s-step-shape", W, _shape()[1],
    "왼쪽은 C 트랙의 한 덩어리 방식으로, 파이썬 JSON 파싱 코드가 명령에 섞여 있어 학생이 그 코드를 해석하다 멈춘다. 결과도 한 덩어리로 나와 어디서 틀렸는지 알기 어렵다. 오른쪽은 S 트랙의 한 줄씩 방식으로, 답을 파일로 받고, 눈으로 보고, 마커를 세고, 턴 수를 보는 네 단계가 각각 하나의 명령과 하나의 확인으로 이어진다. 틀린 단계에서 바로 멈춘다. 두 트랙은 같은 스물세 개이고 다른 것은 쪼갠 크기뿐이다.",
    _shape()[0])


# ------------------------------------------------------ 2. who does what
def _who():
    u, o = "s-who-does-what", []
    o.append(hdr(360, 16, "한 실습 안에서 일을 나누는 방식"))

    cols = [("셸이 한다", "d-accent",
             ["폴더와 파일 만들기", "결과 판정 (grep -c)", "개수 세기 (sort | uniq -c)",
              "합계 (awk)", "훅과 루프 스크립트"]),
            ("클로드코드가 한다", "d-ok",
             ["요청을 이해하고 도구를 고르기", "커넥터 코드 작성 (S1-3)",
              "고장난 코드 고치기 (S2-4)", "명세대로 구현 (S5-1)", "모호한 곳 질문하기 (S5-2)"]),
            ("아무도 안 한다", "d-warn",
             ["JSON 파싱 코드 읽기", "채점 스크립트 해석하기",
              "집계 프로그램 작성하기", "— 이 트랙에서는 전부 없앴다"])]
    cw, gap = 228, 18
    for i, (t, cls, items) in enumerate(cols):
        x = i * (cw + gap)
        o.append(box(x, 34, cw, 34, t, cls=cls, tsize=12))
        y = 82
        for it in items:
            o.append(text(x + 10, y, "· " + it if not it.startswith(("—", " ")) else it,
                          10.5, "start", "d-t" if i < 2 else "d-t d-dim"))
            y += 19

    o.append(line(0, 196, W, 196, "d-rule", dash=True))
    o.append(box(0, 212, 350, 62, "판정은 셸이 한다",
                 ["\"된 것 같다\" 는 판정이 아니다.", "grep -c 가 1 을 내야 성공이다"],
                 cls="d-ok", tsize=11.5))
    o.append(box(370, 212, 350, 62, "만들기는 에이전트가 한다",
                 ["명세를 정확히 쓰는 것이", "이 트랙에서 배우는 진짜 기술이다"],
                 cls="d-accent", tsize=11.5))
    return "".join(o), 286


reg("s-who-does-what", W, _who()[1],
    "한 실습 안에서 일을 세 갈래로 나눈다. 셸이 하는 일은 폴더와 파일 만들기, grep 으로 결과 판정, sort 와 uniq 로 개수 세기, awk 로 합계, 훅과 루프 스크립트다. 클로드코드가 하는 일은 요청을 이해하고 도구를 고르기, 커넥터 코드 작성, 고장난 코드 고치기, 명세대로 구현, 모호한 곳 질문하기다. 아무도 하지 않는 일은 JSON 파싱 코드 읽기, 채점 스크립트 해석, 집계 프로그램 작성이며 이 트랙에서는 전부 없앴다. 판정은 셸이 하고 만들기는 에이전트가 한다.",
    _who()[0])


# ------------------------------------------------------ 3. loop pieces
def _loop():
    u, o = "s-loop-pieces", []
    o.append(hdr(360, 16, "셸 40줄로 만드는 루프 — 네 조각"))

    parts = [("S3-1", "틱", "깨어나서 할 일이", "있는지만 본다", "exit 10 = 있다"),
             ("S3-2", "게이트", "지난번과 같으면", "모델을 안 부른다", "sha256sum 비교"),
             ("S3-3", "상태", "어디까지 했는지", "파일에 남긴다", "cursor.txt"),
             ("S3-4", "예산", "폭주를 멈춘다", "턴 사이에 검사한다", "--max-budget-usd")]
    bw, gap = 165, 20
    for i, (lid, t, a, b, c) in enumerate(parts):
        x = i * (bw + gap)
        o.append(chip_c(x + bw / 2, 34, lid))
        o.append(box(x, 58, bw, 88, t, [a, b], cls="d-accent" if i < 3 else "d-warn",
                     tsize=12.5, ssize=10))
        o.append(note(x + bw / 2, 164, c, bw, size=10))
        if i < len(parts) - 1:
            o.append(arrow_a(x + bw + 2, 102, x + bw + gap - 3, 102, u))

    o.append(line(0, 186, W, 186, "d-rule", dash=True))
    o.append(box(0, 202, 344, 74, "게이트가 절약하는 양",
                 ["5분마다 도는 루프 = 하루 288틱.", "실제 변화가 3번이면 3번만 부른다"],
                 cls="d-ok", tsize=11.5))
    o.append(box(376, 202, 344, 74, "프롬프트 최적화로는 못 가는 자리",
                 ["안 부르는 것이 가장 큰 절약이다.", "그다음이 작은 모델, 그다음이 도구 줄이기"],
                 cls="d-box", tsize=11.5))
    o.append(hdr(360, 300, "Claude Code 에는 스케줄러가 없다. 없으면 만든다."))
    return "".join(o), 314


reg("s-loop-pieces", W, _loop()[1],
    "셸로 만드는 루프는 네 조각이다. S3-1의 틱은 깨어나서 할 일이 있는지만 보고 종료 코드 10으로 신호한다. S3-2의 게이트는 관측 결과의 해시가 지난번과 같으면 모델을 부르지 않는다. S3-3의 상태는 어디까지 했는지를 커서 파일에 남긴다. S3-4의 예산은 폭주를 멈추며 턴 사이에 검사된다. 5분마다 도는 루프는 하루 288틱인데 실제 변화가 세 번이면 세 번만 부른다. 안 부르는 것이 가장 큰 절약이고 그다음이 작은 모델, 그다음이 도구 줄이기다. 프롬프트 최적화로는 갈 수 없는 자리다.",
    _loop()[0])


# ------------------------------------------------- 4. one spec, two languages
def _spec():
    u, o = "s-spec-two-langs", []
    o.append(hdr(360, 16, "같은 명세 하나에서 갈라지는 두 구현"))

    o.append(box(260, 34, 200, 74, "spec.md",
                 ["기능 요구사항 · 경계 사례", "수용 기준 · 범위 밖"],
                 cls="d-accent", tsize=12.5, ssize=10))

    o.append(arrow_a(300, 110, 175, 146, u, "C 트랙", lab_dy=-4, lab_dx=-14))
    o.append(arrow_a(420, 110, 545, 146, u, "S 트랙", lab_dy=-4, lab_dx=14))

    o.append(box(60, 148, 230, 66, "duration.py", ["파이썬 함수", "ValueError 를 낸다"],
                 cls="d-box", tsize=12, ssize=10))
    o.append(box(430, 148, 230, 66, "duration.sh", ["셸 스크립트", "종료 코드 1 로 끝난다"],
                 cls="d-box", tsize=12, ssize=10))

    o.append(arrow(175, 216, 300, 250, u))
    o.append(arrow(545, 216, 420, 250, u))
    o.append(box(240, 252, 240, 52, "같은 수용 기준 17개",
                 ["구현이 달라도 판정은 하나다"], cls="d-ok", tsize=12, ssize=10))

    o.append(line(0, 322, W, 322, "d-rule", dash=True))
    o.append(box(0, 336, 350, 66, "명세는 언어를 모른다",
                 ["\"1h30m 은 5400\" 은 파이썬에도", "셸에도 똑같이 성립한다"],
                 cls="d-ok", tsize=11.5))
    o.append(box(370, 336, 350, 66, "명세가 언어를 아는 곳도 있다",
                 ["오류를 예외로 낼 것인가", "종료 코드로 낼 것인가 — 이건 정해야 한다"],
                 cls="d-warn", tsize=11.5))
    return "".join(o), 414


reg("s-spec-two-langs", W, _spec()[1],
    "하나의 spec.md 에서 두 구현이 갈라진다. C 트랙은 파이썬 함수 duration.py 로 만들어 ValueError 를 내고, S 트랙은 셸 스크립트 duration.sh 로 만들어 종료 코드 1 로 끝난다. 두 구현은 같은 수용 기준 17개로 판정된다. 구현이 달라도 판정은 하나다. 명세는 대체로 언어를 모르며 1h30m 이 5400 이라는 것은 파이썬에도 셸에도 똑같이 성립한다. 다만 오류를 예외로 낼 것인지 종료 코드로 낼 것인지처럼 명세가 언어를 알아야 하는 곳도 있고, 그건 명세에서 정해야 한다.",
    _spec()[0])
