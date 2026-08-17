# AI 에이전트 엔지니어링 — 한국어 강좌

AI 에이전트를 실무 수준으로 다루기 위한 한국어 강좌 웹사이트입니다.
개념을 다루는 **4개 모듈**과, 그것을 오픈소스 에이전트 Hermes로 직접 만들어 보는 **19개 실습**으로 구성됩니다.

**보기 → https://mrgrit.github.io/lecture_ai_agent/**

## 구성

| 모듈 | 주제 | 내용 |
|---|---|---|
| 1 | 스킬과 커넥터 | Skill/Connector의 차이, SKILL.md 구조, progressive disclosure, 자동 발동, 안전 수칙 |
| 2 | 하니스 엔지니어링 | 다섯 동사(constrain·inform·verify·correct·escalate), permission, sandbox, hook, ratchet |
| 3 | 루프 엔지니어링 | 에이전틱 루프 해부, 하트비트, 스케줄 루틴, 검증 사다리, 스파인, 케이던스와 비용 |
| 4 | 그래프 엔지니어링 | commit DAG와 knowledge graph, 추출 파이프라인, subgraph retrieval, grounded checker |
| 실습편 | Hermes로 직접 해보기 | 설치·서버 연결 → 스킬 → 커넥터 → 승인·훅 → 게이트 → 감시 루프 → 메모장 → 기억 그래프 → 근거 검증기 |

각 모듈은 학습 목표 · 본문 강의 · 개념 그림 · 핵심 용어 · 이해도 점검(문답) · 실습 과제로 구성됩니다.
그림 48개는 모두 인라인 SVG로 직접 그렸으며 라이트/다크 테마를 함께 지원합니다.

## 실습편에 대하여

실습편은 [Hermes Agent](https://github.com/NousResearch/hermes-agent)(Nous Research, 오픈소스)를 사용합니다.
로컬 LLM 서버에 연결해 무료로 돌릴 수 있어 수업용으로 적합합니다.

실습 19개는 실습 0(준비) 3개, 실습 1(스킬·커넥터) 4개, 실습 2(하니스) 5개,
실습 3(루프) 4개, 실습 4(기억·그래프) 3개로 나뉘며 각각 모듈 1~4에 대응합니다.
각 모듈 상단에 해당 실습으로 가는 링크가 있습니다.

**모든 명령과 기대 결과는 아래 환경에서 실제로 실행해 확인한 것입니다.**

| 항목 | 값 |
|---|---|
| Hermes | 0.20.0 (2026.8.3), Python 3.11 |
| 모델 | `qwen3.8:27b` (27.3B, Q4_K_M) |
| 추론 서버 | Ollama 0.32.13, OpenAI 호환 엔드포인트 |
| OS | Linux, bash |

문서에 적힌 소요 시간도 실측값입니다. 다른 모델이나 서버에서는 시간이 달라지지만 결과의 모양은 같아야 합니다.
실습 서버 주소는 강의용 예시이므로 각자 환경에 맞게 `config.yaml`의 `model.base_url`을 바꿔 쓰면 됩니다.

## 원자료와 저작권

본 강좌의 한국어 본문은 Panaversity *Agent Factory*의 공개 문서 4편의 개념을
학습 목적으로 **요약·재구성한 2차 학습 자료**이며, 원문의 축자 번역이 아닙니다.

- [Skills & Connectors Crash Course](https://agentfactory.panaversity.org/docs/skills-connectors-crash-course)
- [Harness Engineering Crash Course](https://agentfactory.panaversity.org/docs/harness-engineering-crash-course)
- [Loop Engineering Crash Course](https://agentfactory.panaversity.org/docs/loop-engineering-crash-course)
- [Graph Engineering Crash Course](https://agentfactory.panaversity.org/docs/graph-engineering-crash-course)

모든 그림은 원본 도판을 복제하지 않고 동일한 개념을 한국어 라벨로 새로 그린 것이며,
각 그림 설명에 대응하는 원본 도판 파일명을 병기했습니다. 원저작물의 권리는 원저작자에게 있습니다.

실습편은 위 문서와 별개로 새로 작성한 원본 자료입니다.
Hermes Agent는 Nous Research의 오픈소스 프로젝트입니다.

## 빌드

`index.html`은 `src/`에서 생성됩니다.

```bash
cd src
python3 verify.py       # 48개 SVG의 XML 적합성·CSS 클래스·경계·텍스트 충돌 검사
python3 build.py        # modules/*.md + dia_*.py → ../index.html
python3 verify_html.py  # 앵커·플레이스홀더·CSS 커버리지·외부 리소스 검사
```

- `src/modules/*.md` — 모듈별 한국어 강의 원고 + 실습편 원고(다이어그램 명세 포함)
- `src/dia_m1..4.py`, `src/dia_lab.py` — 48개 다이어그램의 SVG 정의
- `src/svglib.py` — 다이어그램 작도 헬퍼
- `src/build.py` — 마크다운 → 단일 HTML 조립
- `src/verify.py` — 다이어그램 정적 검사 (빌드 전에 실행)
- `src/verify_html.py` — 완성된 페이지 검사 (빌드 후에 실행)

외부 리소스를 전혀 참조하지 않는 단일 HTML 파일이므로, 파일 하나만 복사해도 오프라인에서 그대로 열립니다.
