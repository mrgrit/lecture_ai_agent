# -*- coding: utf-8 -*-
"""Module 5 diagrams — Spec-Driven Development."""
from svglib import *   # noqa

W = 720
D = {}


def reg(uid, w, h, aria, body):
    D[uid] = svg(uid, w, h, aria, body)


# ---------------------------------------------------------------- 1. two loops
def _two_loops():
    u, o = "two-loops-sdd", []
    p, ix, iy, iw, _ = panel(0, 8, 350, 244, "바이브 코딩", "만들면서 생각한다", chip="나선")
    o.append(p)
    cx, cy = ix + iw / 2, iy + 74
    for i, (t, dx, dy) in enumerate([("한 문장 던지기", 0, -58), ("코드가 나온다", 96, 20),
                                     ("“이게 아닌데”", -96, 20)]):
        o.append(box(cx + dx - 74, cy + dy - 18, 148, 36, t, cls="d-box", tsize=11))
    o.append(path("M %g %g C %g %g %g %g %g %g" % (cx + 60, cy - 44, cx + 110, cy - 40,
                                                   cx + 118, cy - 14, cx + 100, cy - 2), u))
    o.append(path("M %g %g C %g %g %g %g %g %g" % (cx + 40, cy + 46, cx - 4, cy + 62,
                                                   cx - 44, cy + 60, cx - 62, cy + 46), u))
    o.append(path("M %g %g C %g %g %g %g %g %g" % (cx - 100, cy - 2, cx - 118, cy - 16,
                                                   cx - 110, cy - 40, cx - 62, cy - 44), u))
    o.append(note(cx, iy + 172, "반복할수록 원래 뭘 원했는지가 흐려진다", iw - 6))

    p, ix, iy, iw, _ = panel(370, 8, 350, 244, "명세 주도 개발", "먼저 생각하고 적어 둔다",
                             chip="기준점", chip_cls="d-chip-a")
    o.append(p)
    o.append(box(ix, iy + 4, iw, 44, "spec.md — 합의된 것", cls="d-strong", tsize=12))
    o.append(arrow_a(ix + iw / 2, iy + 50, ix + iw / 2, iy + 68, u))
    o.append(box(ix, iy + 70, iw / 2 - 8, 40, "만든다", cls="d-box", tsize=11.5))
    o.append(box(ix + iw / 2 + 8, iy + 70, iw / 2 - 8, 40, "명세와 대조한다", cls="d-ok", tsize=11.5))
    o.append(arrow(ix + iw / 2 - 8, iy + 90, ix + iw / 2 + 6, iy + 90, u))
    o.append(path_a("M %g %g C %g %g %g %g %g %g"
                    % (ix + iw - 40, iy + 112, ix + iw - 40, iy + 140,
                       ix + 40, iy + 140, ix + 40, iy + 116), u))
    o.append(note(ix + iw / 2, iy + 172, "구멍이 보이면 코드가 아니라 명세로 돌아간다", iw - 6))
    o.append(banner(60, 268, 600, 42, "결과물을 버리게 됐을 때 짜증이 난다면, 이미 왼쪽이 안전한 지점을 지난 것이다"))
    return "".join(o), 322


reg("two-loops-sdd", W, _two_loops()[1],
    "바이브 코딩은 한 문장 던지기, 코드가 나온다, 이게 아닌데를 반복하는 나선이라 반복할수록 원래 목표가 흐려진다. 명세 주도 개발은 합의된 spec.md를 기준점으로 두고 만들기와 대조하기의 짧은 루프를 돌며, 구멍이 보이면 코드가 아니라 명세로 돌아간다. 결과물을 버릴 때 짜증이 난다면 이미 바이브 코딩이 안전한 지점을 지난 것이다.",
    _two_loops()[0])


# ---------------------------------------------------------------- 2. inversion
def _inversion():
    u, o = "spec-inversion", []
    p, ix, iy, iw, _ = panel(0, 8, 350, 200, "예전 모델", "명세는 비계다")
    o.append(p)
    o.append(box(ix, iy + 6, iw, 40, "명세", ["코딩이 시작되면 낡기 시작한다"], cls="d-box",
                 tsize=12, ssize=10))
    o.append(arrow(ix + iw / 2, iy + 48, ix + iw / 2, iy + 70, u, "안내", lab_dy=-3, lab_dx=22))
    o.append(box(ix, iy + 72, iw, 46, "코드", ["여기에 진실이 있다"], cls="d-strong",
                 tsize=12, ssize=10))
    o.append(cross(ix + 22, iy + 26, 8))
    o.append(note(ix + iw / 2, iy + 142, "곧 아무도 명세를 안 본다", iw - 6))

    p, ix, iy, iw, _ = panel(370, 8, 350, 200, "SDD 모델", "명세가 원천이다",
                             chip="유지된다", chip_cls="d-chip-a")
    o.append(p)
    o.append(box(ix, iy + 6, iw, 46, "명세", ["여기에 진실이 있다"], cls="d-strong",
                 tsize=12, ssize=10))
    o.append(arrow_a(ix + iw / 2, iy + 54, ix + iw / 2, iy + 76, u, "생성", lab_dy=-3, lab_dx=22))
    o.append(box(ix, iy + 78, iw, 40, "코드", ["명세로부터 나온 출력"], cls="d-box",
                 tsize=12, ssize=10))
    o.append(path_a("M %g %g C %g %g %g %g %g %g"
                    % (ix + iw - 14, iy + 98, ix + iw + 4, iy + 84,
                       ix + iw + 4, iy + 40, ix + iw - 14, iy + 30), u))
    o.append(note(ix + iw / 2, iy + 142, "동작이 바뀌면 명세를 먼저 고친다", iw - 6))
    o.append(line(0, 222, W, 222, "d-rule", dash=True))
    o.append(hdr(360, 248, "명세가 반드시 답해야 하는 세 가지"))
    for i, (t, s) in enumerate([("왜", "무슨 문제를, 누구를 위해"),
                                ("무엇", "다 됐을 때 무엇이 참인가"),
                                ("무엇을 안 하는가", "범위 밖을 명시한다")]):
        o.append(box(i * 244, 262, 232, 56, t, [s], cls="d-accent" if i == 2 else "d-box",
                     tsize=12, ssize=10.5))
    return "".join(o), 330


reg("spec-inversion", W, _inversion()[1],
    "예전 모델에서 명세는 코드를 안내하는 비계여서 코딩이 시작되면 낡고 곧 아무도 보지 않으며 진실은 코드에 있다. SDD 모델에서는 명세가 진실이고 코드는 명세로부터 생성된 출력이며, 동작이 바뀌면 명세를 먼저 고친다. 명세는 왜, 무엇, 그리고 무엇을 만들지 않는가 세 가지에 반드시 답해야 한다.",
    _inversion()[0])


# ---------------------------------------------------------------- 3. precision
def _precision():
    u, o = "precision-test", []
    o.append(banner(90, 4, 540, 40, "유능한 사람이 이 줄을 지키면서도 엉뚱한 것을 만들 수 있는가?"))
    rows = [("약함", "사용자는 잊어버린 비밀번호를 재설정할 수 있다",
             "방법 · 유효기간 · 재사용 · 실패 응답이 전부 열려 있다", "d-bad-box", False),
            ("조금 나음", "이메일 링크로 재설정한다. 링크는 30분 후 만료된다",
             "두 가지가 고정됐다. 아직 재사용과 응답이 남았다", "d-warn", False),
            ("강함", "링크는 한 번만 동작하고 30분 후 만료된다. 만료된 링크는 안내를 보여 준다. 응답은 가입 여부를 드러내지 않는다",
             "오해할 여지가 없다", "d-ok", True)]
    y = 58
    for label, txt, why, cls, ok in rows:
        o.append(box(0, y, 96, 62, label, cls=cls, tsize=12))
        o.append(box(104, y, 480, 62, txt, cls="d-box", tsize=11, tweight=None))
        o.append((check if ok else cross)(614, y + 20, 9))
        o.append(note(660, y + 46, "통과" if ok else "조인다", 100, size=10))
        o.append(text(596, y + 46, "", 10, "start", "d-t"))
        y += 72
    o.append(line(0, y + 4, W, y + 4, "d-rule", dash=True))
    o.append(note(360, y + 30, "정밀하게 쓰다 보면 빠진 요구사항(가입 여부 노출 금지)이 저절로 드러난다 — 이게 이 시험의 진짜 효용이다", W - 20))
    o.append(hdr(360, y + 58, "명세는 쓸 말이 없을 때가 아니라 오해할 것이 없을 때 끝난다"))
    return "".join(o), y + 76


reg("precision-test", W, _precision()[1],
    "정밀도 시험은 모든 요구사항 줄에 유능한 사람이 이 줄을 지키면서도 엉뚱한 것을 만들 수 있는가를 묻는다. 약한 문장은 방법과 유효기간과 실패 응답이 열려 있고, 조인 문장은 링크가 한 번만 동작하고 만료되며 응답이 가입 여부를 드러내지 않는다고 못 박는다. 정밀하게 쓰다 보면 빠진 요구사항이 저절로 드러나며, 명세는 오해할 것이 없을 때 끝난다.",
    _precision()[0])


# ---------------------------------------------------------------- 4. three levels
def _levels():
    u, o = "three-levels-sdd", []
    o.append(hdr(360, 16, "규율이 올라가는 세 단계 — 아래에서 시작해 위로 자란다"))
    rows = [("Spec-as-Source", "명세가 곧 원천. 코드는 다시 뽑을 수 있는 출력",
             "성숙하고 규율이 잡힌 팀", "d-warn", "현장 증거 가장 적음"),
            ("Spec-Anchored", "동작이 바뀌면 명세를 먼저 고치고 코드를 다시 뽑는다",
             "몇 달 이상 유지할 것", "d-accent", "이 강좌의 목표"),
            ("Spec-First", "처음에 한 번 쓰고 만든다. 이후 표류를 허용",
             "대부분의 기능 · 기본값", "d-ok", "여기서 시작한다")]
    y = 40
    for name, defn, when, cls, tag in rows:
        o.append(box(0, y, 232, 66, name, cls=cls, tsize=13))
        o.append(box(240, y, 300, 66, defn, cls="d-box", tsize=11, tweight=None))
        o.append(box(548, y, 172, 66, when, cls="d-panel-2", tsize=10.5, tweight=None))
        o.append(chip_c(116, y - 12, tag, cls="d-chip"))
        y += 84
    o.append(arrow_a(116, 268, 116, 132, u))
    o.append(line(0, y + 4, W, y + 4, "d-rule", dash=True))
    o.append(box(0, y + 18, W, 62, "Spec-as-Source에 대한 정직한 단서",
                 ["운영 중인 시스템에서 에이전트 생성 코드는 사람이 쓴 코드보다 빨리 낡는다.",
                  "코드를 읽을 의무를 줄이는 것이 아니라 오히려 늘린다."],
                 cls="d-warn", tsize=12, ssize=11))
    return "".join(o), y + 92


reg("three-levels-sdd", W, _levels()[1],
    "SDD는 세 단계다. Spec-First는 처음에 한 번 쓰고 이후 표류를 허용하는 기본값이고, Spec-Anchored는 동작이 바뀔 때마다 명세를 먼저 고치고 코드를 다시 뽑으며 몇 달 이상 유지할 것에 쓴다. Spec-as-Source는 명세가 곧 원천인 최상위 단계지만 현장 증거가 가장 적고, 에이전트 생성 코드가 빨리 낡으므로 코드를 읽을 의무를 오히려 늘린다. Spec-First에서 시작해 Spec-Anchored로 자란다.",
    _levels()[0])


# ---------------------------------------------------------------- 5. method
def _method():
    u, o = "sdd-method", []
    o.append(box(120, 6, 480, 52, "Phase 0 — 헌법 (Constitution)",
                 ["모든 명세 위에 있는 프로젝트 전체의 규칙"], cls="d-strong", tsize=13, ssize=11))
    for x in (100, 288, 476):
        o.append(line(x + 40, 58, x + 40, 78, "d-rule", dash=True))
    phases = [("1. 조사", "지형을 그린다", "한 쪽짜리 결과 문서"),
              ("2. 명세", "무엇과 왜", "spec.md"),
              ("3. 확인", "AI가 나를 취조", "오해할 것이 없는 명세"),
              ("4. 빌드", "계획 → 작게 → 대조", "코드 + 통과한 검사")]
    bw, gap = 168, 16
    for i, (t, s, out) in enumerate(phases):
        x = i * (bw + gap)
        o.append(box(x, 84, bw, 80, t, [s], cls="d-accent", tsize=13, ssize=11))
        o.append(numchip(x + 18, 100, i + 1))
        o.append(note(x + bw / 2, 182, out, bw + 6, size=10))
        if i < 3:
            o.append(arrow_a(x + bw + 1, 124, x + bw + gap - 2, 124, u))
    o.append(path_a("M 640 202 C 640 236 80 236 80 172", u))
    o.append(note(360, 250, "빌드 중에 발견된 구멍은 코드가 아니라 명세로 되돌아간다 — 그래야 명세가 계속 참이다", W - 20))
    o.append(line(0, 274, W, 274, "d-rule", dash=True))
    o.append(box(0, 288, 350, 62, "헌법은 법이 아니다",
                 ["지속되는 맥락일 뿐 — 대체로 따르지만 항상은 아니다"], cls="d-warn", tsize=12, ssize=10.5))
    o.append(box(370, 288, 350, 62, "절대 규칙은 기계로 받친다",
                 ["테스트 · 훅 · CI · 권한 · 사람의 검토 (모듈 2)"], cls="d-ok", tsize=12, ssize=10.5))
    return "".join(o), 362


reg("sdd-method", W, _method()[1],
    "헌법이 모든 명세 위에 있고 그 아래로 조사, 명세, 확인, 빌드 네 단계가 이어진다. 조사는 한 쪽짜리 결과 문서를, 명세는 spec.md를, 확인은 오해할 것이 없는 명세를, 빌드는 코드와 통과한 검사를 낸다. 빌드 중 발견된 구멍은 코드가 아니라 명세로 되돌아간다. 헌법은 법이 아니라 지속되는 맥락이므로, 절대 깨지면 안 되는 규칙은 테스트와 훅과 CI와 권한과 사람의 검토로 받쳐야 한다.",
    _method()[0])


# ---------------------------------------------------------------- 6. constitution
def _const():
    u, o = "constitution-anatomy", []
    p, ix, iy, iw, _ = panel(0, 8, 430, 296, "헌법 — 세 개의 절", "CLAUDE.md · AGENTS.md · 프로젝트 지침")
    o.append(p)
    secs = [("원칙", ["영리함보다 평이한 표현", "직접 만들기보다 검증된 라이브러리"], "여기서는 항상 무엇이 참인가"),
            ("제약", ["스택: 지금 있는 것을 벗어나지 않는다", "published/ 는 절대 건드리지 않는다"], "기존 기술과 금지 구역"),
            ("완료의 정의", ["동작이 명세와 일치한다", "병합 전에 사람이 diff를 검토한다"], "무엇을 다 됐다고 하는가")]
    yy = iy + 4
    for t, items, sub in secs:
        o.append(box(ix, yy, iw, 74, t, items, cls="d-box", tsize=12, ssize=10))
        o.append(text(ix + iw - 4, yy + 14, sub, 9.5, "end", "d-t d-dim"))
        yy += 82
    p2, jx, jy, jw, _ = panel(450, 8, 270, 296, "적정 규모", "규칙마다 이 질문을 한다",
                              chip="판정", chip_cls="d-chip-a")
    o.append(p2)
    o.append(box(jx, jy + 4, jw, 52, "이 규칙을 빼면 AI가 실수를 할 수 있는가?",
                 cls="d-strong", tsize=11.5, tweight="700"))
    o.append(box(jx, jy + 64, jw, 58, "아니오 → 뺀다",
                 ["“깔끔한 코드를 작성한다”는", "지켜도 엉망을 만들 수 있다"], cls="d-bad-box", tsize=11.5, ssize=10))
    o.append(box(jx, jy + 130, jw, 58, "예 → 남긴다",
                 ["“published/ 를 건드리지 않는다”는", "빼면 실제로 사고가 난다"], cls="d-ok", tsize=11.5, ssize=10))
    o.append(note(jx + jw / 2, jy + 214, "너무 빡빡하면 숨이 막히고", jw - 4, size=10))
    o.append(note(jx + jw / 2, jy + 230, "너무 헐거우면 없느니만 못하다", jw - 4, size=10))
    return "".join(o), 316


reg("constitution-anatomy", W, _const()[1],
    "헌법은 원칙, 제약, 완료의 정의 세 절로 이루어진다. 원칙은 여기서는 항상 무엇이 참인가를, 제약은 기존 기술과 금지 구역을, 완료의 정의는 무엇을 다 됐다고 할지를 적는다. 규칙마다 이 규칙을 빼면 AI가 실수를 할 수 있는가를 묻고, 아니면 뺀다. 깔끔한 코드를 작성한다는 지켜도 엉망을 만들 수 있어 탈락하고, published 폴더를 건드리지 않는다는 빼면 실제로 사고가 나므로 남긴다.",
    _const()[0])


# ---------------------------------------------------------------- 7. spec anatomy
def _spec():
    u, o = "spec-anatomy", []
    o.append(hdr(360, 16, "명세의 여섯 절 — 그리고 의도적으로 없는 것"))
    items = [("① 목표", "왜 하는가, 2~3문장"),
             ("② 사용자 시나리오", "X를 하면 Y를 얻는다"),
             ("③ 기능 요구사항", "무시하면 눈에 띄게 실패할 만큼 구체적으로"),
             ("④ 경계 사례와 규칙", "빈 값 · 큰 값 · 중복 · 깨진 형식 · 권한 없음"),
             ("⑤ 범위 밖", "이것이 하지 않는 것 — 건너뛰지 말 것"),
             ("⑥ 수용 기준", "“다 됐다”를 말하는 점검 목록")]
    for i, (t, s) in enumerate(items):
        x = (i % 2) * 368
        y = 40 + (i // 2) * 64
        o.append(box(x, y, 352, 54, t, [s], cls="d-accent" if i in (4, 5) else "d-box",
                     tsize=12, ssize=10.5))
    o.append(line(0, 244, W, 244, "d-rule", dash=True))
    o.append(box(0, 258, 350, 84, "여기 쓰면 안 되는 것",
                 ["데이터베이스 선택 · 프레임워크 선택 · 파일 배치", "이건 전부 계획(plan)의 몫이다"],
                 cls="d-bad-box", tsize=12, ssize=10.5))
    o.append(box(370, 258, 350, 84, "왜 빼는가",
                 ["“S3에 저장한다”라고 쓰면 서버를 옮길 때 명세를 다시 쓴다.",
                  "“영구 보관되고 원본 이름으로 받을 수 있다”는 그대로 참이다."],
                 cls="d-ok", tsize=12, ssize=10.5))
    return "".join(o), 354


reg("spec-anatomy", W, _spec()[1],
    "명세는 목표, 사용자 시나리오, 기능 요구사항, 경계 사례와 규칙, 범위 밖, 수용 기준 여섯 절로 이루어진다. 데이터베이스 선택과 프레임워크 선택과 파일 배치는 여기 쓰지 않고 계획으로 미룬다. S3에 저장한다고 쓰면 서버를 옮길 때 명세를 다시 써야 하지만, 영구 보관되고 원본 이름으로 받을 수 있다고 쓰면 합의가 그대로 참으로 남기 때문이다.",
    _spec()[0])


# ---------------------------------------------------------------- 8. threshold
def _thr():
    u, o = "sdd-threshold", []
    o.append(hdr(360, 16, "경계선은 일부러 낮게 그어져 있다"))
    o.append(line(300, 36, 300, 254, "d-rule"))
    o.append(chip_c(300, 30, "문턱", cls="d-chip-a", tcls="d-chip-a-t"))
    left = ["일회용 스크립트나 사소한 손질", "오늘 쓰고 버린다", "되돌리기 한 번이면 끝",
            "한 문장으로 완전히 명확하다"]
    right = ["여러 파일 · 모듈 · 데이터를 건드린다", "나중의 나 또는 남이 유지한다",
             "틀리면 돈 · 데이터 · 신뢰가 나간다", "요구사항이 흐릿해서 못을 박아야 한다",
             "여러 사람이 “완료”에 합의해야 한다"]
    o.append(text(146, 58, "그냥 바이브로", 12, "middle", "d-t", "700"))
    for i, s in enumerate(left):
        o.append(box(0, 70 + i * 44, 284, 36, s, cls="d-box", tsize=10.5, tweight=None))
    o.append(text(510, 58, "SDD를 쓴다", 12, "middle", "d-t d-acc", "700"))
    for i, s in enumerate(right):
        o.append(box(316, 70 + i * 44, 404, 36, s, cls="d-accent", tsize=10.5, tweight=None))
    o.append(line(0, 270, W, 270, "d-rule", dash=True))
    o.append(note(360, 292, "상태 · 권한 · 데이터 모델 · 돈 · 남의 기대가 끼어드는 순간 구조가 값을 한다", W - 20))
    o.append(note(360, 314, "초보자는 보상이 나오기 직전, 가장 답답한 순간에 그만둔다", W - 20))
    return "".join(o), 330


reg("sdd-threshold", W, _thr()[1],
    "SDD를 쓸지 말지를 가르는 문턱은 일부러 낮게 그어져 있다. 왼쪽은 일회용 스크립트, 오늘 쓰고 버릴 것, 되돌리기 한 번이면 끝나는 것, 한 문장으로 명확한 것이다. 오른쪽은 여러 파일을 건드리고, 남이 유지하고, 틀리면 돈과 신뢰가 나가고, 요구사항이 흐릿하고, 여러 사람이 완료에 합의해야 하는 것이다. 상태와 권한과 데이터 모델과 돈과 남의 기대가 끼어드는 순간 구조가 값을 한다.",
    _thr()[0])


# ---------------------------------------------------------------- 9. drift
def _drift():
    u, o = "spec-drift", []
    o.append(hdr(360, 16, "아무도 거짓말하지 않았는데 명세가 거짓이 된다"))
    steps = [("① 급해서", "코드에서 이메일 제목을 직접 고쳤다", "d-box"),
             ("② 그대로", "spec.md 에는 옛 제목이 남아 있다", "d-warn"),
             ("③ 3주 뒤", "새 팀원이 명세를 믿고 코드를 되돌린다", "d-bad-box")]
    bw, gap = 228, 18
    for i, (t, s, cls) in enumerate(steps):
        x = i * (bw + gap)
        o.append(box(x, 40, bw, 76, t, [s], cls=cls, tsize=12, ssize=10.5))
        if i < 2:
            o.append(arrow_a(x + bw + 1, 78, x + bw + gap - 2, 78, u))
    o.append(note(360, 138, "대가는 버그 하나를 찾는 시간이다. 그리고 다음번에는 아무도 명세를 믿지 않는다", W - 20))
    o.append(line(0, 158, W, 158, "d-rule", dash=True))
    o.append(box(90, 172, 540, 52, "동작 변경은 같은 커밋 안에서 spec.md 에도 들어간다",
                 cls="d-strong", tsize=13))
    o.append(note(360, 244, "이 습관 하나가 Spec-First 를 Spec-Anchored 로 바꾼다", W - 20))
    return "".join(o), 260


reg("spec-drift", W, _drift()[1],
    "명세 표류는 급해서 코드에서만 고치고 명세를 그대로 두는 데서 시작한다. 3주 뒤 새 팀원이 명세를 믿고 잘 돌아가던 코드를 되돌리며, 대가는 버그 하나를 찾는 시간이고 다음번에는 아무도 명세를 믿지 않게 된다. 동작 변경을 같은 커밋 안에서 spec.md 에도 반영하는 습관 하나가 Spec-First 를 Spec-Anchored 로 바꾼다.",
    _drift()[0])


# ---------------------------------------------------------------- 10. two readers
def _readers():
    u, o = "two-readers-one-bill", []
    o.append(box(180, 6, 360, 54, "나쁜 설계",
                 ["엉킨 의존성 · 세 군데에 흩어진 같은 규칙 · 거짓말하는 이름"],
                 cls="d-bad-box", tsize=13, ssize=10.5))
    o.append(arrow_a(300, 62, 200, 92, u))
    o.append(arrow_a(420, 62, 520, 92, u))
    o.append(box(0, 96, 350, 86, "독자 1 — 사람",
                 ["이 시스템이 여전히 말이 되는지 판단해야 한다",
                  "→ 검토가 느려지고 판단이 약해진다"], cls="d-box", tsize=12.5, ssize=10.5))
    o.append(box(370, 96, 350, 86, "독자 2 — 에이전트",
                 ["다음 주에 이것을 고쳐야 한다",
                  "→ 컨텍스트를 더 태우고 잘못 짐작하고 재시도한다"], cls="d-accent", tsize=12.5, ssize=10.5))
    o.append(banner(140, 198, 440, 40, "같은 결함, 두 장의 청구서"))
    o.append(line(0, 256, W, 256, "d-rule", dash=True))
    o.append(hdr(360, 280, "좋은 설계의 독자는 사라진 것이 아니라 늘어났다"))
    o.append(note(360, 304, "그러니 규율은 “코드 대신 명세”가 아니다 — 무엇을 합의하고, 어떻게를 생성하고, 나온 것을 가서 본다", W - 20))
    return "".join(o), 320


reg("two-readers-one-bill", W, _readers()[1],
    "엉킨 의존성과 흩어진 규칙과 거짓말하는 이름 같은 나쁜 설계는 두 독자에게 동시에 청구된다. 사람 독자는 시스템이 말이 되는지 판단해야 하는데 검토가 느려지고 판단이 약해지며, 에이전트 독자는 다음 주에 이것을 고쳐야 하는데 컨텍스트를 더 태우고 잘못 짐작하고 재시도한다. 좋은 설계의 독자는 사라진 것이 아니라 늘어났으며, 규율은 코드 대신 명세가 아니라 무엇을 합의하고 어떻게를 생성하고 나온 것을 가서 보는 것이다.",
    _readers()[0])
