# AI 에이전트 엔지니어링 — 한국어 강좌

AI 에이전트를 실무 수준으로 다루기 위한 4개 모듈 한국어 강좌 웹사이트입니다.

**보기 → https://mrgrit.github.io/lecture_ai_agent/**

## 구성

| 모듈 | 주제 | 내용 |
|---|---|---|
| 1 | 스킬과 커넥터 | Skill/Connector의 차이, SKILL.md 구조, progressive disclosure, 자동 발동, 안전 수칙 |
| 2 | 하니스 엔지니어링 | 다섯 동사(constrain·inform·verify·correct·escalate), permission, sandbox, hook, ratchet |
| 3 | 루프 엔지니어링 | 에이전틱 루프 해부, 하트비트, 스케줄 루틴, 검증 사다리, 스파인, 케이던스와 비용 |
| 4 | 그래프 엔지니어링 | commit DAG와 knowledge graph, 추출 파이프라인, subgraph retrieval, grounded checker |

각 모듈은 학습 목표 · 본문 강의 · 개념 그림 · 핵심 용어 · 이해도 점검(문답) · 실습 과제로 구성됩니다.
그림 43개는 모두 인라인 SVG로 직접 그렸으며 라이트/다크 테마를 함께 지원합니다.

## 원자료와 저작권

본 강좌의 한국어 본문은 Panaversity *Agent Factory*의 공개 문서 4편의 개념을
학습 목적으로 **요약·재구성한 2차 학습 자료**이며, 원문의 축자 번역이 아닙니다.

- [Skills & Connectors Crash Course](https://agentfactory.panaversity.org/docs/skills-connectors-crash-course)
- [Harness Engineering Crash Course](https://agentfactory.panaversity.org/docs/harness-engineering-crash-course)
- [Loop Engineering Crash Course](https://agentfactory.panaversity.org/docs/loop-engineering-crash-course)
- [Graph Engineering Crash Course](https://agentfactory.panaversity.org/docs/graph-engineering-crash-course)

모든 그림은 원본 도판을 복제하지 않고 동일한 개념을 한국어 라벨로 새로 그린 것이며,
각 그림 설명에 대응하는 원본 도판 파일명을 병기했습니다. 원저작물의 권리는 원저작자에게 있습니다.

## 빌드

`index.html`은 `src/`에서 생성됩니다.

```bash
cd src && python3 build.py    # modules/*.md + dia_m*.py → index.html
```

- `src/modules/*.md` — 모듈별 한국어 강의 원고(다이어그램 명세 포함)
- `src/dia_m1..4.py` — 43개 다이어그램의 SVG 정의
- `src/svglib.py` — 다이어그램 작도 헬퍼
- `src/build.py` — 마크다운 → 단일 HTML 조립
