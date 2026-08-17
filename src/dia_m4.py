# -*- coding: utf-8 -*-
"""Module 4 diagrams — Graph Engineering."""
from svglib import *   # noqa

W = 720
D = {}


def reg(uid, w, h, aria, body):
    D[uid] = svg(uid, w, h, aria, body)


def node(cx, cy, label, r=22, cls="d-node", tcls="d-t", size=10):
    return ('<circle cx="%g" cy="%g" r="%g" class="%s"/>%s'
            % (cx, cy, r, cls, text(cx, cy + size * 0.36, label, size, "middle", tcls, "700")))


# ------------------------------------------------- 1. series map
def _series():
    u, o = "series-map", []
    cards = [("루프 엔지니어링", ["비트 · 스파인 · ratchet", "maker–checker"], "선수 과목", "d-box"),
             ("하네스 엔지니어링", ["권한 · 훅 ·", "typed output"], "선수 과목", "d-box"),
             ("그래프 엔지니어링", ["commit DAG · knowledge graph", "· 거버넌스"], "현재 위치", "d-strong"),
             ("검증자 신뢰", ["골드 세트 · 루브릭 ·", "드리프트"], "다음 과정", "d-panel-2"),
             ("랩톱 떠나기", ["headless · 스케줄 ·", "관리형 런타임"], "다음 과정", "d-panel-2")]
    for i, (t, subs, badge, cls) in enumerate(cards):
        x = i * 146
        o.append(box(x, 22, 130, 118, None, cls=cls))
        o.append(numchip(x + 65, 22, i + 1))
        for j, ln in enumerate(wrap(t, 11.5, 116)):
            o.append(text(x + 65, 58 + j * 15, ln, 11.5, "middle", "d-t", "700"))
        ty = 58 + len(wrap(t, 11.5, 116)) * 15 + 4
        for s in subs:
            for ln in wrap(s, 10, 118):
                o.append(text(x + 65, ty, ln, 10, "middle", "d-t d-dim"))
                ty += 13
        o.append(chip_c(x + 65, 130, badge,
                        cls="d-chip-a" if i == 2 else "d-chip",
                        tcls="d-chip-a-t" if i == 2 else "d-chip-t", h=18))
        if i < 4:
            o.append(arrow(x + 131, 80, x + 144, 80, u))
    p, ix, iy, iw, _ = panel(0, 160, 720, 104, "이 모듈이 전제하는 네 용어")
    o.append(p)
    terms = [("비트(beat)", "루프의 1회 완주"), ("스파인(spine)", "먼저 읽고 나중에 쓰는 상태 파일"),
             ("ratchet", "개선된 것만 유지하는 규칙"), ("worktree", "에이전트별 격리 작업 폴더")]
    for i, (t, s) in enumerate(terms):
        x = ix + (i % 2) * 356
        y = iy + 14 + (i // 2) * 24
        o.append(text(x, y, t, 11, "start", "d-t", "700"))
        o.append(text(x + tw(t, 11) + 8, y, "— " + s, 10.5, "start", "d-t d-dim"))
    return "".join(o), 278


reg("series-map", W, _series()[1],
    "커리큘럼 안에서 이 모듈의 위치. 루프 엔지니어링과 하네스 엔지니어링이 선수 과목이고, 그래프 엔지니어링이 현재 위치이며, 검증자 신뢰와 랩톱 떠나기가 다음 과정이다.",
    _series()[0])


# ------------------------------------------------- 2. transcript vs graph
def _tvg():
    u, o = "transcript-vs-graph", []
    p, ix, iy, iw, _ = panel(0, 8, 340, 268, "transcript", "세션과 함께 죽는 기억")
    o.append(p)
    for i in range(3):
        x = ix + i * 108
        o.append(box(x, iy + 10, 96, 44, "에이전트 %d" % (i + 1), cls="d-box", tsize=11))
        o.append(box(x + 8, iy + 66, 80, 56, "대화", ["두루마리"], cls="d-panel-2", tsize=10.5))
    for i in range(2):
        x = ix + 96 + i * 108
        o.append(line(x + 4, iy + 94, x + 20, iy + 94, "d-line", dash=True))
        o.append(cross(x + 12, iy + 94, 6))
    o.append(note(170, iy + 150,
                  "각자 배우고 각자 잊는다. 공유하려면 transcript 전체를 복사해야 하고 컨텍스트 윈도우는 가득 찬다", 300, cls="d-t d-bad"))
    p, ix, iy, iw, _ = panel(360, 8, 360, 268, "그래프", "세션보다 오래 사는 기억")
    o.append(p)
    for i in range(3):
        o.append(box(ix + i * 116, iy + 6, 104, 32, "에이전트 %d" % (i + 1), cls="d-box", tsize=10.5))
    cx, cy = 540, iy + 116
    o.append('<rect x="%g" y="%g" width="300" height="104" rx="10" class="d-accent"/>' % (cx - 150, cy - 52))
    nodes = [(cx - 100, cy - 24, "Entity"), (cx + 8, cy - 26, "Claim"),
             (cx + 108, cy - 6, "Source"), (cx - 78, cy + 30, "Commit"), (cx + 26, cy + 32, "Eval")]
    for a, b in [(0, 1), (1, 2), (0, 3), (1, 4)]:
        o.append(line(nodes[a][0], nodes[a][1], nodes[b][0], nodes[b][1], "d-edge"))
    o.append(text(cx - 44, cy - 30, "supports", 9, "middle", "d-t d-dim", halo=True))
    o.append(text(cx + 66, cy - 8, "about", 9, "middle", "d-t d-dim", halo=True))
    for x, y, lb in nodes:
        o.append(node(x, y, lb, 24, "d-node", size=9.5))
    o.append(arrow_a(420, iy + 40, 470, cy - 56, u))
    o.append(text(400, iy + 66, "타입 있는", 9.5, "start", "d-t d-acc"))
    o.append(text(400, iy + 78, "소규모 기록 쓰기", 9.5, "start", "d-t d-acc"))
    o.append(arrow(640, cy - 56, 668, iy + 40, u))
    o.append(text(660, iy + 72, "제한된", 9.5, "middle", "d-t d-dim"))
    o.append(text(660, iy + 84, "subgraph 읽기", 9.5, "middle", "d-t d-dim"))
    o.append(note(540, iy + 194, "모든 edge가 지니는 것 — provenance: source + run + confidence", 340))
    o.append(banner(0, 288, 720, 40, "에이전트는 잊지만, 그래프는 잊지 않는다"))
    return "".join(o), 340


reg("transcript-vs-graph", W, _tvg()[1],
    "transcript 메모리에서는 에이전트들이 각자 배우고 각자 잊지만, 그래프 메모리에서는 타입이 있는 기록을 함께 쓰고 필요한 subgraph만 읽어 간다.",
    _tvg()[0])


# ------------------------------------------------- 3. two graphs
def _twog():
    u, o = "two-graphs", []
    p, ix, iy, iw, _ = panel(0, 8, 350, 210, "commit DAG", "작업을 기억한다", chip="구성상의 사실", chip_cls="d-chip-a")
    o.append(p)
    ys = iy + 44
    for i in range(5):
        x = ix + 24 + i * 62
        o.append(node(x, ys, "c%d" % (i + 1), 18, "d-node-a", size=10))
        if i:
            o.append(arrow(x - 62 + 19, ys, x - 19, ys, u))
    o.append(text(ix + 272, ys + 36, "유지됨: 최고 지표", 10, "middle", "d-t d-acc", "700"))
    for i, (sx, dy) in enumerate([(1, 56), (3, 56)]):
        x = ix + 24 + sx * 62
        o.append(line(x, ys + 18, x + 34, ys + dy - 12, "d-line", dash=True))
        o.append(node(x + 46, ys + dy, "", 15, "d-node-dim"))
        o.append(cross(x + 46, ys + dy, 7))
        o.append(text(x + 46, ys + dy + 30, ["되돌림", "크래시"][i], 9.5, "middle", "d-t d-dim"))
    p, ix, iy, iw, _ = panel(370, 8, 350, 210, "knowledge graph", "사실을 기억한다",
                             chip="증거 딸린 claim", chip_cls="d-chip-a")
    o.append(p)
    o.append(box(ix + 96, iy + 8, 128, 34, "claim_244", cls="d-panel-2", tsize=10.5))
    o.append(box(ix + 96, iy + 62, 128, 34, "claim_301", cls="d-node-a", tsize=10.5))
    o.append(box(ix, iy + 122, 130, 34, "entity_pg_api", cls="d-box", tsize=10.5))
    o.append(box(ix + 190, iy + 118, 130, 44, "ci_log", ["confidence 0.9"],
                 cls="d-src", tsize=10.5, ssize=9))
    o.append(arrow_a(ix + 160, iy + 60, ix + 160, iy + 44, u))
    o.append(text(ix + 168, iy + 54, "supersedes", 9.5, "start", "d-t d-acc", "700"))
    o.append(arrow(ix + 130, iy + 96, ix + 78, iy + 120, u))
    o.append(text(ix + 78, iy + 112, "about", 9.5, "middle", "d-t d-dim", halo=True))
    o.append(arrow(ix + 190, iy + 96, ix + 240, iy + 120, u))
    o.append(text(ix + 244, iy + 110, "supported_by", 9.5, "middle", "d-t d-dim", halo=True))
    p, ix, iy, iw, _ = panel(90, 228, 540, 92, "잇되, 합치지 않는다", dash=True, cls="d-panel-2")
    o.append(p)
    o.append(box(ix + 200, iy + 8, 130, 34, "run_77", cls="d-strong", tsize=11))
    o.append(box(ix, iy + 8, 150, 34, "commit_9d2f", cls="d-node-a", tsize=10.5))
    o.append(box(ix + 380, iy + 8, 150, 34, "claim_301", cls="d-node-a", tsize=10.5))
    o.append(arrow(ix + 198, iy + 25, ix + 154, iy + 25, u, "modified", lab_dy=-7))
    o.append(arrow(ix + 332, iy + 25, ix + 376, iy + 25, u, "produced", lab_dy=-7))
    o.append(text(ix + 74, iy + 60, "작업 계보", 10, "middle", "d-t d-dim"))
    o.append(text(ix + 456, iy + 60, "도메인 지식", 10, "middle", "d-t d-dim"))
    o.append(note(360, 352, "실험 노트와 백과사전 — 둘 다 유지하고, 상호 참조하고, 절대 합치지 않는다. supersedes는 대체이지 삭제가 아니다", W))
    return "".join(o), 370


reg("two-graphs", W, _twog()[1],
    "작업을 기억하는 commit DAG와 사실을 기억하는 knowledge graph는 서로 다른 그래프다. run 노드가 둘을 잇지만 둘을 합치지는 않는다.",
    _twog()[0])


# ------------------------------------------------- 4. ratchet to DAG
def _r2d():
    u, o = "ratchet-to-dag", []
    steps = ["학습 코드 수정", "커밋", "약 5분 학습", "지표 측정"]
    for i, s in enumerate(steps):
        x = i * 132
        o.append(box(x, 16, 120, 40, s, cls="d-box", tsize=11))
        if i < 3:
            o.append(arrow(x + 122, 36, x + 130, 36, u))
    o.append(chip_c(596, 26, "🔒 평가 스크립트는 동결(frozen)", cls="d-chip-a", tcls="d-chip-a-t"))
    o.append(arrow_a(430, 58, 380, 82, u))
    o.append(arrow_a(470, 58, 520, 82, u))
    o.append(chip_c(300, 84, "개선됨: 브랜치 전진", cls="d-chip-a", tcls="d-chip-a-t", h=22))
    o.append(chip_c(580, 84, "같거나 나쁨: git reset", cls="d-chip-w", tcls="d-chip-w-t", h=22))
    y0 = 122
    p, ix, iy, iw, _ = panel(0, y0, 232, 186, "Git 브랜치", "유지된 것만", chip="검증됨")
    o.append(p)
    for i in range(4):
        x = ix + 24 + i * 50
        o.append(node(x, iy + 34, "c%d" % (i + 1), 16, "d-node-a", size=9.5))
        if i:
            o.append(arrow(x - 50 + 17, iy + 34, x - 17, iy + 34, u))
    for i in range(3):
        o.append(node(ix + 40 + i * 62, iy + 96, "?", 14, "d-node-dim"))
    o.append(note(116, iy + 132, "reset: 브랜치에서 사라진다", 200))
    p, ix, iy, iw, _ = panel(244, y0, 232, 186, "시도 로그", "모든 시도", chip="완전함")
    o.append(p)
    rows = [("c2", "0.81", "유지"), ("—", "0.79", "폐기"), ("c3", "0.84", "유지"), ("—", "—", "크래시")]
    o.append(text(ix, iy + 14, "커밋", 10, "start", "d-t d-dim", "700"))
    o.append(text(ix + 80, iy + 14, "지표", 10, "start", "d-t d-dim", "700"))
    o.append(text(ix + 150, iy + 14, "상태", 10, "start", "d-t d-dim", "700"))
    for i, (c, m, st) in enumerate(rows):
        yy = iy + 36 + i * 20
        o.append(text(ix, yy, c, 10.5, "start", "d-t"))
        o.append(text(ix + 80, yy, m, 10.5, "start", "d-t"))
        o.append(text(ix + 150, yy, st, 10.5, "start", "d-t d-dim"))
    o.append(box(ix, iy + 122, iw, 30, "의도적으로 Git 미추적", cls="d-panel-2", tsize=10.5))
    p, ix, iy, iw, _ = panel(488, y0, 232, 186, "DAG", "대안이 살아 있다", chip="순회 가능", chip_cls="d-chip-a")
    o.append(p)
    pts = [(ix + 30, iy + 30, 1), (ix + 96, iy + 22, 1), (ix + 160, iy + 40, 1),
           (ix + 66, iy + 80, 0), (ix + 132, iy + 92, 0), (ix + 190, iy + 84, 1)]
    for a, b in [(0, 1), (1, 2), (0, 3), (1, 4), (2, 5)]:
        o.append(line(pts[a][0], pts[a][1], pts[b][0], pts[b][1], "d-edge"))
    for x, y, ok in pts:
        o.append(node(x, y, "", 13, "d-node-a" if ok else "d-node-w"))
        if not ok:
            o.append(cross(x, y, 6))
    o.append(text(ix + 100, iy + 132, "폐기된 결과도 여전히 node다", 10, "middle", "d-t d-dim"))
    o.append(text(ix + 100, iy + 148, "children · leaves · lineage", 10, "middle", "d-t d-acc", "700"))
    o.append(note(360, 356, "Git은 성공을, 로그는 시도를 보관한다. 그러나 나중의 에이전트가 둘 다 질의하게 해 주는 것은 그래프뿐이다", W))
    return "".join(o), 372


reg("ratchet-to-dag", W, _r2d()[1],
    "ratchet은 Git 브랜치에 성공만, 시도 로그에 모든 시도를 남긴다. DAG는 폐기된 대안까지 node로 살려 두어 나중의 에이전트가 계보를 순회할 수 있게 한다.",
    _r2d()[0])


# ------------------------------------------------- 5. extraction pipeline
def _extract():
    u, o = "extraction-pipeline", []
    p, ix, iy, iw, _ = panel(0, 8, 150, 250, "① 문서")
    o.append(p)
    for i, f in enumerate(["onboarding.md", "incident-0712.md", "meeting-notes.md"]):
        o.append(box(ix, iy + 6 + i * 42, iw, 34, f, cls="d-src", tsize=10, tweight=None))
    o.append(note(75, iy + 146, "라벨 없음, 골드 코퍼스 없음", 140))
    o.append(arrow_a(152, 130, 168, 130, u))
    p, ix, iy, iw, _ = panel(170, 8, 186, 250, "② 추출", "저렴한 모델 · schema 제약")
    o.append(p)
    for i, s in enumerate(["박지훈 수석 (플랫폼팀 리드)", "지훈 박 (장애 대응 총괄)",
                           "J. Park (온보딩 멘토)", "김민준 (백엔드, 2023 입사)",
                           "김민준 (UX 디자이너, 2025 입사)"]):
        o.append(box(ix, iy + 4 + i * 32, iw, 26, s, cls="d-box", tsize=9, tweight=None))
    o.append(note(263, iy + 178, "description이 다음 단계의 열쇠", 176))
    o.append(arrow_a(358, 130, 374, 130, u))
    p, ix, iy, iw, _ = panel(376, 8, 200, 250, "③ 해소", "강한 모델 · 추론 과제")
    o.append(p)
    o.append(box(ix, iy + 4, iw, 74, "canonical: 박지훈",
                 ["alias 셋을 유지한 채", "하나로 병합한다"], cls="d-ok", tsize=10.5))
    o.append(check(ix + 14, iy + 18))
    o.append(box(ix, iy + 88, iw, 80, "병합하지 않는다",
                 ["동명이인 김민준 둘 —", "이름은 같고", "description이 다르다"], cls="d-warn", tsize=10.5, dash=True))
    o.append(cross(ix + 14, iy + 102, 6))
    o.append(note(476, iy + 196, "가역적 — 근거와 confidence를 보존한다", 200))
    o.append(arrow_a(578, 130, 594, 130, u))
    p, ix, iy, iw, _ = panel(596, 8, 124, 250, "④ 조립")
    o.append(p)
    o.append(node(ix + 30, iy + 26, "박지훈", 24, "d-node-a", size=9))
    o.append(node(ix + 30, iy + 92, "장애", 22, "d-node", size=9))
    o.append(node(ix + 86, iy + 60, "src", 18, "d-src-n", size=9))
    o.append(line(ix + 30, iy + 50, ix + 30, iy + 70, "d-edge"))
    o.append(line(ix + 46, iy + 36, ix + 72, iy + 52, "d-edge"))
    o.append(line(ix + 46, iy + 84, ix + 72, iy + 70, "d-edge"))
    o.append(box(ix, iy + 128, iw, 76, "모든 edge가 지니는 것",
                 ["source_doc", "confidence", "produced_by"], cls="d-accent", tsize=10))
    o.append(note(360, 292, "잘못된 병합(false merge)이 파국적 실패다 — alias를 보존하고, 근거를 보존하고, 되돌릴 수 있게 하라", W))
    return "".join(o), 310


reg("extraction-pipeline", W, _extract()[1],
    "문서에서 질의 가능한 그래프까지의 네 단계 — 추출, 해소, 조립. 저렴한 모델이 표면형을 뽑고 강한 모델이 동일 인물을 병합하되 동명이인은 분리한 채로 두며, 모든 edge는 출처와 확신도를 지닌다.",
    _extract()[0])


# ------------------------------------------------- 6. subgraph retrieval
def _sub():
    u, o = "subgraph-retrieval", []
    p, ix, iy, iw, _ = panel(0, 8, 200, 250, "전체 그래프", "약 5만 edge")
    o.append(p)
    import math
    pts = []
    for i in range(26):
        a = i * 2.399
        r = 8 + (i % 7) * 8.5
        pts.append((ix + 86 + r * math.cos(a) * 1.5, iy + 78 + r * math.sin(a)))
    for i in range(0, 24, 2):
        o.append(line(pts[i][0], pts[i][1], pts[i + 2][0], pts[i + 2][1], "d-edge-dim"))
    for i, (x, y) in enumerate(pts):
        hot = i in (4, 17)
        o.append('<circle cx="%g" cy="%g" r="%g" class="%s"/>'
                 % (x, y, 6 if hot else 4, "d-node-a" if hot else "d-node-dim"))
    o.append(note(100, iy + 172, "이걸 통째로 덤프하는 것은 예전 실패의 개명일 뿐이다", 186))
    o.append(arrow_a(202, 110, 236, 110, u, "해소 · 확장", lab_dy=-8))
    p, ix, iy, iw, _ = panel(238, 8, 254, 250, "과업의 subgraph", "entity 2개 · 2홉 · 허용된 edge만")
    o.append(p)
    o.append(box(ix, iy + 6, 108, 34, "업체_한빛부품", cls="d-node-a", tsize=10))
    o.append(box(ix + 128, iy + 6, 98, 34, "모듈_PM3", cls="d-box", tsize=10))
    o.append(box(ix + 128, iy + 66, 98, 34, "장애_0712", cls="d-node-a", tsize=10))
    o.append(box(ix, iy + 66, 108, 34, "계약서.pdf", cls="d-src", tsize=10))
    o.append(arrow(ix + 110, iy + 23, ix + 126, iy + 23, u, "supplied", lab_dy=-6))
    o.append(arrow(ix + 177, iy + 42, ix + 177, iy + 64, u))
    o.append(text(ix + 182, iy + 56, "involved_in", 9, "start", "d-t d-dim"))
    o.append(line(ix + 54, iy + 42, ix + 54, iy + 64, "d-edge"))
    o.append(box(ix, iy + 116, iw, 62, "충돌도 함께 간다",
                 ["두 source가 납품 일자에 대해", "어긋난다 — 워커는 둘 다 본다"], cls="d-warn", tsize=10.5))
    o.append(arrow_a(494, 110, 528, 110, u, "직렬화", lab_dy=-8))
    p, ix, iy, iw, _ = panel(530, 8, 190, 250, "워커가 받는 것", "평문 triple · 안정적 ID")
    o.append(p)
    tri = ["e1041 업체_한빛부품", "      supplied 모듈_PM3", "e1042 모듈_PM3",
           "      involved_in 장애_0712", "e1043 claim_88", "      from 계약서.pdf",
           "e1044 ⚑ 충돌 e1045"]
    for i, t in enumerate(tri):
        o.append('<text x="%g" y="%g" font-size="9" class="d-mono">%s</text>'
                 % (ix, iy + 16 + i * 17, esc(t)))
    o.append(chip_c(625, iy + 152, "5만 edge가 아니라 triple 스무 줄",
                    cls="d-chip-a", tcls="d-chip-a-t", h=18))
    o.append(note(360, 282, "해소하고, 확장하고, 검증된 것을 우선하고, 충돌을 포함하고, 예산 안에서 직렬화하고, ID를 붙인다", W))
    return "".join(o), 300


reg("subgraph-retrieval", W, _sub()[1],
    "전체 그래프를 통째로 넘기는 대신 과업이 언급한 entity에서 2홉만 확장한 subgraph를 만들고, 충돌까지 포함해 평문 triple 스무 줄로 직렬화해 워커에게 건넨다.",
    _sub()[0])


# ------------------------------------------------- 7. grounded checker
def _gc():
    u, o = "grounded-checker", []
    o.append(chip_c(88, 8, "maker의 주장", cls="d-chip-a", tcls="d-chip-a-t"))
    o.append(box(0, 34, 720, 40, "“한빛부품이 납품한 모듈이 7월 12일 장애의 원인 부품이다”",
                 cls="d-strong", tsize=12.5))
    o.append(arrow_a(300, 76, 210, 104, u))
    o.append(arrow_a(420, 76, 510, 104, u))
    o.append(text(360, 92, "필요한 edge로 분해", 10.5, "middle", "d-t d-acc", "700", halo=True))
    p, ix, iy, iw, _ = panel(0, 106, 350, 122, "필요 edge 1 — 발견됨")
    o.append(p)
    o.append(check(ix + 300, iy - 30))
    o.append(box(ix, iy + 6, 130, 34, "업체_한빛부품", cls="d-node-a", tsize=10.5))
    o.append(box(ix + 190, iy + 6, 130, 34, "모듈_PM3", cls="d-box", tsize=10.5))
    o.append(arrow(ix + 132, iy + 23, ix + 188, iy + 23, u, "supplied", lab_dy=-6))
    o.append(text(ix, iy + 62, "e1041 · source: 계약서.pdf · confidence 0.94", 10, "start", "d-t d-dim"))
    p, ix, iy, iw, _ = panel(370, 106, 350, 122, "필요 edge 2 — 없음", dash=True, cls="d-warn-p")
    o.append(p)
    o.append(cross(ix + 300, iy - 30))
    o.append(box(ix, iy + 6, 130, 34, "모듈_PM3", cls="d-box", tsize=10.5))
    o.append(box(ix + 190, iy + 6, 130, 34, "장애_0712", cls="d-panel-2", tsize=10.5, dash=True))
    o.append(arrow(ix + 132, iy + 23, ix + 188, iy + 23, u, "involved_in ?", lab_dy=-6, dash=True))
    o.append(text(ix, iy + 62, "그래프에 근거 있는 경로가 존재하지 않는다", 10, "start", "d-t d-dim"))
    o.append(arrow(175, 230, 175, 254, u))
    o.append(arrow(545, 230, 545, 254, u))
    p, ix, iy, iw, _ = panel(0, 256, 350, 132, "grounded 판정 = 작업 지시서")
    o.append(p)
    for i, ln in enumerate(['{ "decision": "revise",',
                            '  "required_evidence": [',
                            '    "모듈_PM3 → 장애_0712" ] }']):
        o.append('<text x="%g" y="%g" font-size="10" class="d-mono">%s</text>'
                 % (ix, iy + 16 + i * 17, esc(ln)))
    o.append(note(175, iy + 82, "maker는 정확히 무엇을 찾을지, 무엇을 철회할지 안다", 320))
    p, ix, iy, iw, _ = panel(370, 256, 350, 132, "ungrounded 판정 = 기분", dash=True, cls="d-panel-2")
    o.append(p)
    o.append(text(ix, iy + 20, "“이 주장은 어딘가 약해 보인다”", 11.5, "start", "d-t d-dim"))
    o.append(note(545, iy + 66, "maker는 리뷰어의 심기를 추측해야 하고, 기억에는 아무것도 남지 않는다", 320, cls="d-t d-bad"))
    o.append(note(360, 410, "maker가 근거를 찾아오면 그래프에 edge가 추가된다 — grounding은 보고서가 아니라 기억을 개선한다", W))
    return "".join(o), 428


reg("grounded-checker", W, _gc()[1],
    "grounded checker는 maker의 주장을 필요한 edge로 분해해 하나는 출처와 확신도까지 확인하고 다른 하나는 경로 없음을 밝혀, 무엇을 찾아야 하는지 지시하는 판정을 낸다.",
    _gc()[0])


# ------------------------------------------------- 8. loop to graph
def _l2g():
    u, o = "loop-to-graph", []
    p, ix, iy, iw, _ = panel(0, 8, 246, 320, "루프 하나", "이전 모듈")
    o.append(p)
    o.append(chip_c(123, iy, "하트비트 — 평일 오전 9시", cls="d-chip-a", tcls="d-chip-a-t"))
    for i, s in enumerate(["1 탐색", "2 구현", "3 검증", "4 커밋"]):
        o.append(box(ix + 30, iy + 32 + i * 38, iw - 60, 30, s, cls="d-box", tsize=11))
        if i < 3:
            o.append(arrow(123, iy + 62 + i * 38, 123, iy + 68 + i * 38, u))
    o.append(box(ix, iy + 190, iw, 34, "스파인 — progress.md", cls="d-accent", tsize=11))
    o.append(arrow(123, iy + 184, 123, iy + 188, u))
    o.append(note(123, iy + 246, "맹점: 루프는 자기 지표만 볼 수 있어 그것을 조작하게 되고, 자기 목표를 의심할 수 없다", 230, cls="d-t d-bad"))
    o.append(arrow_a(248, 168, 272, 168, u, "합성", lab_dy=-8))
    p, ix, iy, iw, _ = panel(274, 8, 446, 320, "그래프", "루프를 감시하는 루프들, 앵커에 접지됨")
    o.append(p)
    o.append(text(ix, iy + 10, "빠른 루프 (최적화)", 10.5, "start", "d-t d-dim", "700"))
    o.append(box(ix, iy + 18, 190, 44, "분류 루프", ["maker"], cls="d-ok", tsize=11))
    o.append(box(ix + 228, iy + 18, 190, 44, "리뷰 루프", ["counter-metric 담당"], cls="d-ok", tsize=11))
    o.append(arrow(ix + 192, iy + 40, ix + 226, iy + 40, u, "PR", lab_dy=-6))
    o.append(line(ix, iy + 74, ix + iw, iy + 74, "d-rule", dash=True))
    o.append(text(ix, iy + 92, "느린 루프 (감시자를 감시)", 10.5, "start", "d-t d-dim", "700"))
    o.append(box(ix, iy + 100, 250, 48, "감사 루프 — 주 1회",
                 ["“숫자가 아직 현실에 닿아 있는가?”"], cls="d-warn", tsize=11))
    o.append(line(ix + 60, iy + 98, ix + 60, iy + 64, "d-line", dash=True))
    o.append(box(ix + 274, iy + 100, 144, 48, "human gate",
                 ["목표를 소유한다"], cls="d-strong", tsize=11))
    o.append(arrow_a(ix + 252, iy + 124, ix + 272, iy + 124, u))
    o.append(line(ix, iy + 160, ix + iw, iy + 160, "d-rule", dash=True))
    o.append(text(ix, iy + 178, "앵커 (누구도 반박할 수 없는 것)", 10.5, "start", "d-t d-dim", "700"))
    o.append(box(ix, iy + 186, iw, 60, "실제로 실행된 테스트 · 실제 사용자 · 실제로 입금된 매출",
                 ["🔒 frozen node: 평가 스크립트 — 루프가 튜닝할 수 없다"], cls="d-anchor", tsize=11))
    o.append(arrow(ix + 340, iy + 152, ix + 340, iy + 184, u))
    o.append(banner(0, 344, 720, 40, "오래가는 축은 루프 대 그래프가 아니라 접지됨 대 접지 안 됨이다"))
    return "".join(o), 396


reg("loop-to-graph", W, _l2g()[1],
    "루프 하나는 자기 지표만 보는 맹점이 있다. 그래프에서는 빠른 실행 루프를 느린 감사 루프가 감시하고, 규칙 변경은 인간 게이트를 거치며, 모든 것이 반박 불가능한 현실 앵커에 접지된다.",
    _l2g()[0])


# ------------------------------------------------- 9. graph build
def _build():
    u, o = "graph-build", []
    p, ix, iy, iw, _ = panel(0, 8, 210, 176, "maker", "비트 1회")
    o.append(p)
    o.append(note(105, iy + 16, "일을 한 뒤, 확립한 것을 나중의 에이전트가 열어 볼 수 있는 source 딸린 claim 하나로 기록한다", 190, cls="d-t"))
    o.append(note(105, iy + 96, "세션 잡담은 progress.md에 남긴다", 190))
    o.append(arrow_a(212, 96, 246, 96, u, "쓴다", lab_dy=-8))
    p, ix, iy, iw, _ = panel(248, 8, 224, 176, "graph/")
    o.append(p)
    for i, (f, s) in enumerate([("entities.json", "루프들이 이야기하는 node"),
                                ("claims.json", "영수증 달린 edge"),
                                ("runs.json", "어느 비트가 무엇을 썼는가")]):
        o.append(box(ix, iy + 4 + i * 42, iw, 36, f, [s], cls="d-box", tsize=10.5))
    o.append(arrow(508, 96, 474, 96, u, "읽는다", lab_dy=-8, dash=True))
    p, ix, iy, iw, _ = panel(510, 8, 210, 176, "reviewer")
    o.append(p)
    o.append(note(615, iy + 16, "모든 사실 진술에 claim id를 인용하거나, 찾지 못한 증거를 지목하며 REVISE를 반환한다", 190, cls="d-t"))
    o.append(note(615, iy + 96, "‘그럴듯함’은 인용이 아니다", 190, cls="d-t d-bad"))
    o.append(box(248, 192, 224, 40, "🔒 모든 claim은 source · produced_by · supersedes · created를 지닌다",
                 cls="d-accent", tsize=10))
    o.append(box(0, 192, 210, 40, "pre-commit hook", ["jq가 schema 위반 커밋을 차단한다"],
                 cls="d-warn", tsize=10.5, dash=True))
    o.append(arrow(212, 212, 246, 212, u, "지킨다", lab_dy=-8))
    o.append(box(510, 192, 210, 40, "append-only", ["옛 claim은 절대 편집하지 않는다"], cls="d-box", tsize=10.5))
    p, ix, iy, iw, _ = panel(0, 244, 720, 92, "3주 뒤 이것이 사 주는 것")
    o.append(p)
    o.append('<text x="%g" y="%g" font-size="10.5" class="d-mono">%s</text>'
             % (ix, iy + 16, esc('jq \'.claims[] | select(.superseded_by==null)\' graph/claims.json')))
    o.append(note(360, iy + 44, "한 줄, 한 답, 영수증 하나 — 체인지로그 루프가 목격한 적 없는 수정을 보고할 수 있다", 660))
    o.append(note(360, 356, "reviewer edge는 거버넌스, hook은 frozen node, source 참조는 앵커다", W))
    return "".join(o), 374


reg("graph-build", W, _build()[1],
    "최소 그래프 빌드 — JSON 파일 셋과 pre-commit hook 하나, 그리고 maker와 reviewer 프롬프트 둘. maker가 영수증 딸린 claim을 쓰고 reviewer는 claim id를 인용하며 hook이 schema를 지킨다.",
    _build()[0])


# ------------------------------------------------- 10. choosing a level
def _stairs():
    u, o = "choosing-a-level", []
    labels = [("zero-shot", "단순 저위험 질문"), ("루프", "출력을 검사할 수 있을 때"),
              ("체인", "순서가 안정적일 때"), ("라우터", "분류가 명확할 때"),
              ("병렬 워커", "단위가 독립적일 때"), ("orchestrator–workers", "분해가 과업마다 다를 때"),
              ("commit DAG", "대안이 살아 있어야 할 때"), ("knowledge graph", "사실이 세션을 넘어야 할 때"),
              ("동적 워크플로", "초대형 병렬 작업")]
    SW, SH, X0, Y0 = 52, 27, 44, 300
    for i, (t, s) in enumerate(labels):
        x = X0 + i * SW
        y = Y0 - (i + 1) * SH
        cls = "d-strong" if i in (6, 7) else ("d-warn" if i == 8 else "d-box")
        o.append('<rect x="%g" y="%g" width="%g" height="%g" rx="4" class="%s"/>' % (x, y, SW, SH, cls))
        o.append(text(x + SW / 2, y + 18, str(i + 1), 12, "middle", "d-t", "700"))
        o.append(text(x + SW + 6, y + 12, t, 10.5, "start", "d-t", "700"))
        o.append(text(x + SW + 6, y + 24, s, 9.5, "start", "d-t d-dim"))
    o.append(arrow_a(30, 296, 30, 56, u))
    o.append('<g transform="rotate(-90 18 176)">%s</g>'
             % text(18, 176, "비용 · 지연 · 기계 장치 증가", 10.5, "middle", "d-t d-acc", "700"))
    p, ix, iy, iw, _ = panel(0, 314, 720, 74, "이 모듈은 7·8번 계단이다")
    o.append(p)
    o.append(note(360, iy + 14, "7번은 4절(모든 계보를 살려 두기), 8번은 5~8절(사실을 지키기). 9번은 둘 다에 실제 예산이 필요하며, 1~6번은 이전 두 모듈의 내용이다", 660))
    o.append(chip_c(360, 394, "실행 전에 예산을 선언하라 — 최대 워커 · 토큰 · 비용 · 그래프 쓰기, 그리고 완료를 선언하기 위한 최소 증거",
                    cls="d-chip-a", tcls="d-chip-a-t", h=26))
    return "".join(o), 432


reg("choosing-a-level", W, _stairs()[1],
    "구조의 아홉 계단. zero-shot에서 동적 워크플로까지 올라갈수록 비용과 지연과 기계 장치가 늘어나며, 이 모듈은 commit DAG와 knowledge graph에 해당하는 7·8번 계단이다.",
    _stairs()[0])
