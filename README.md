# AI 에이전트 엔지니어링 — 한국어 강좌

AI 에이전트를 실무 수준으로 다루기 위한 한국어 강좌 웹사이트입니다.
개념을 다루는 **5개 모듈**과, 그것을 직접 만들어 보는 **세 벌의 실습편(각 23개, 총 69개 실습)** 으로 구성됩니다.

**보기 → https://mrgrit.github.io/lecture_ai_agent/**

## 구성

| 모듈 | 주제 | 내용 |
|---|---|---|
| 1 | 스킬과 커넥터 | Skill/Connector의 차이, SKILL.md 구조, progressive disclosure, 자동 발동, 안전 수칙 |
| 2 | 하니스 엔지니어링 | 다섯 동사(constrain·inform·verify·correct·escalate), permission, sandbox, hook, ratchet |
| 3 | 루프 엔지니어링 | 에이전틱 루프 해부, 하트비트, 스케줄 루틴, 검증 사다리, 스파인, 케이던스와 비용 |
| 4 | 그래프 엔지니어링 | commit DAG와 knowledge graph, 추출 파이프라인, subgraph retrieval, grounded checker |
| 5 | 명세 주도 개발 | 바이브 코딩과 SDD, 정밀도 시험, 헌법, 조사·명세·확인·빌드 4단계, 명세 표류 |
| 실습편 L | Hermes로 직접 해보기 | 설치·서버 연결 → 스킬 → 커넥터 → 승인·훅 → 게이트 → 감시 루프 → 메모장 → 기억 그래프 → 근거 검증기 → 명세와 표류 검사 |
| 실습편 C | Claude Code로 직접 해보기 | 같은 스물세 개를 Claude Code로. 실습당 한 덩어리 스크립트 |
| 실습편 S | 같은 것을 한 줄씩 | 같은 스물세 개를 약 200단계로 쪼갠 것. 읽어야 할 파이썬 코드가 없다 |

각 모듈은 학습 목표 · 본문 강의 · 개념 그림 · 핵심 용어 · 이해도 점검(문답) · 실습 과제로 구성됩니다.
그림 70개는 모두 인라인 SVG로 직접 그렸으며 라이트/다크 테마를 함께 지원합니다.

## 세 벌의 실습편에 대하여

같은 스물세 개 실습을 세 벌로 준비했고, **번호까지 일대일로 맞췄습니다.**
`L2-3`(Hermes) · `C2-3`(Claude Code) · `S2-3`(한 줄씩)은 같은 개념을 확인합니다.
각 모듈 상단에 세 트랙의 해당 실습으로 가는 링크가 나란히 있습니다.

**L과 C는 도구가 다르고, C와 S는 진행 방식이 다릅니다.**

개념이 도구에 종속되지 않는다는 것을 말로 설명하는 대신, 같은 것을 두 번 만들어 보게 하는 것이 L↔C 구성의 이유입니다.
"훅"은 특정 제품의 기능이 아니라 에이전트 설계의 개념이고,
Hermes는 `hooks.pre_tool_call`, Claude Code는 `PreToolUse` 라고 부를 뿐입니다.

| | 실습편 L (Hermes) | 실습편 C (Claude Code) | 실습편 S (한 줄씩) |
|---|---|---|---|
| 비용 | 학교 GPU 서버, 학생 부담 0원 | 개인 구독 또는 API 요금 | C와 같음 |
| 모델 | `qwen3.8:27b` (로컬) | `claude-haiku-4-5` | `claude-haiku-4-5` |
| 작업 폴더 | `~/hermes-lab` | `~/cc-lab` | `~/cc-step` |
| 한 실습의 명령 블록 | 3~6개 | 3~6개 | 8~18개 |
| 읽어야 할 파이썬 | 있음 | 있음 | **없음** |
| 쓰임 | 무료·오프라인 트랙 | 시연·복습·자동 검증 | **수업에서 따라 하기** |

세 트랙 모두 실습 0(준비) 3개, 실습 1(스킬·커넥터) 4개, 실습 2(하니스) 5개,
실습 3(루프) 4개, 실습 4(기억·그래프) 3개, 실습 5(명세 주도 개발) 4개로 나뉘며
각각 모듈 1~5에 대응합니다.

### 실습편 S를 따로 만든 이유

실습편 C의 명령에는 `python3` 가 85번 나오고 그중 44번이 `python3 -c "..."` 인라인 코드입니다. 대부분 JSON을 파싱해 보기 좋게 출력하는 코드입니다.
검증에는 이 방식이 가장 좋지만, 수업에서는 **에이전트를 배우러 온 학생이 JSON 파싱 코드를 해석하게 됩니다.**

실습편 S는 같은 스물세 개를 다시 쓰면서 그것을 전부 없앴습니다.

- JSON 읽기 → `grep -o '"total_cost_usd":[0-9.]*'` 한 줄
- 채점·집계 → `grep` · `sort` · `uniq -c` · `awk` 한 줄
- 만드는 프로그램 → 파이썬 대신 셸 (`slugify.sh`, `duration.sh`)
- MCP 커넥터 → 코드를 주지 않고 **클로드코드에게 명세를 주고 만들게 함**
- 각 단계마다 "무엇이 보여야 하는지" 한 줄

C 트랙은 지우지 않고 그대로 두었습니다. 강사가 수업 전에 환경을 한 번에 점검할 때,
학생이 막혔을 때 정답 전체를 볼 때, 같은 일을 파이썬으로 어떻게 하는지 비교할 때 필요하기 때문입니다.
S 트랙의 모든 실습 카드에서 짝이 되는 C 트랙 실습으로 갈 수 있습니다.

### 검증 환경

**모든 명령과 기대 결과는 아래 환경에서 실제로 실행해 확인한 것입니다.**

| 항목 | 실습편 L | 실습편 C · S |
|---|---|---|
| 에이전트 | Hermes 0.20.0 (Python 3.11) | Claude Code 2.1.2xx (native, linux-x64) |
| 모델 | `qwen3.8:27b` (27.3B, Q4_K_M) | `claude-haiku-4-5` (비교 실습만 `sonnet`) |
| 추론 서버 | Ollama 0.32.13, OpenAI 호환 엔드포인트 | Anthropic API |
| 실행 방식 | `hermes chat` · `hermes cron` | `claude -p` 비대화 모드 |
| 의존성 | Hermes 설치본 | 파이썬 표준 라이브러리만 (MCP 서버 포함) |
| OS | Linux, bash | Linux, bash |

문서에 적힌 소요 시간도 실측값입니다. 다른 모델이나 서버에서는 시간이 달라지지만 결과의 모양은 같아야 합니다.

실습편 L의 서버 주소는 강의용 예시이므로 각자 환경에 맞게 `config.yaml`의 `model.base_url`을 바꿔 쓰면 됩니다.
실습편 C·S는 전역 설정(`~/.claude/`)을 건드리지 않고 프로젝트 폴더 안의 `.claude/` 에서만 동작하도록 구성했습니다.
두 트랙의 작업 폴더가 다르므로 둘 다 해도 서로 간섭하지 않습니다.

## 원자료와 저작권

본 강좌의 한국어 본문은 Panaversity *Agent Factory*의 공개 문서 5편의 개념을
학습 목적으로 **요약·재구성한 2차 학습 자료**이며, 원문의 축자 번역이 아닙니다.

- [Skills & Connectors Crash Course](https://agentfactory.panaversity.org/docs/skills-connectors-crash-course)
- [Harness Engineering Crash Course](https://agentfactory.panaversity.org/docs/harness-engineering-crash-course)
- [Loop Engineering Crash Course](https://agentfactory.panaversity.org/docs/loop-engineering-crash-course)
- [Graph Engineering Crash Course](https://agentfactory.panaversity.org/docs/graph-engineering-crash-course)
- [Spec-Driven Development Crash Course](https://agentfactory.panaversity.org/docs/spec-driven-development-crash-course)

모든 그림은 원본 도판을 복제하지 않고 동일한 개념을 한국어 라벨로 새로 그린 것이며,
각 그림 설명에 대응하는 원본 도판 파일명을 병기했습니다. 원저작물의 권리는 원저작자에게 있습니다.

세 실습편은 위 문서와 별개로 새로 작성한 원본 자료입니다.
Hermes Agent는 Nous Research의 오픈소스 프로젝트이고, Claude Code는 Anthropic의 제품입니다.

## 빌드

`index.html`은 `src/`에서 생성됩니다.

```bash
cd src
python3 verify.py       # 70개 SVG의 XML 적합성·CSS 클래스·경계·텍스트 충돌 검사
python3 build.py        # modules/*.md + dia_*.py → ../index.html
python3 verify_html.py  # 앵커·플레이스홀더·실습 카드 수·CSS 커버리지·외부 리소스 검사
```

- `src/modules/module1..5-*.md` — 모듈별 한국어 강의 원고 (다이어그램 명세 포함)
- `src/modules/lab-hermes.md`, `lab-claude-code.md`, `lab-cc-steps.md` — 세 실습편 원고
- `src/dia_m1..5.py`, `dia_lab.py`, `dia_labcc.py`, `dia_labsteps.py` — 70개 다이어그램의 SVG 정의
- `src/svglib.py` — 다이어그램 작도 헬퍼
- `src/build.py` — 마크다운 → 단일 HTML 조립
- `src/verify.py` — 다이어그램 정적 검사 (빌드 전에 실행)
- `src/verify_html.py` — 완성된 페이지 검사 (빌드 후에 실행)
- `src/verify-labs/` — 실습편 C·S의 명령을 문서에서 뽑아 실제로 실행하고 결과를 기계로 검사하는 하니스

## 실습편 C·S의 검증 방법

두 트랙 모두 문서에 적힌 `bash` 블록을 그대로 뽑아 순서대로 실행하고,
실습마다 "무엇이 참이면 성공인가"를 기계가 검사하는 방식으로 확인했습니다.

```bash
cd src/verify-labs
# 격리 홈을 만든다 (.claude 는 링크 = 로그인 공유, .claude.json 은 복사본 = 실제 홈 보호)
mkdir -p shome && ln -s ~/.claude shome/.claude && cp ~/.claude.json shome/.claude.json

python3 extract_cc.py && python3 runcc.py   # 실습편 C — 94개 블록 · 24개 구간
python3 extract_s.py  && python3 runs.py    # 실습편 S — 240개 블록 · 24개 구간

rm shome/.claude && rm -rf shome            # 링크를 먼저 지운다
```

> 두 스크립트는 실제로 모델을 호출하므로 요금이 발생합니다(아래 표 참고).

두 트랙 모두 **완전히 빈 환경에서 처음부터 끝까지 여러 번** 돌려(C 트랙 3회, S 트랙 4회), 마지막 회차에 24개 구간 전부 통과하는 것을 확인했습니다.

| | 실습편 C | 실습편 S |
|---|---|---|
| bash 블록 | 94개 | 240개 |
| 전체 검증 소요 | 14분 | 13분 |
| 모델 호출 | 44회 | 48회 |
| 1회 통과 비용 (목록가) | 약 $2.5 | 약 $2 |
| 모델을 안 부르는 실습 | `C0-1` `C3-1` `C4-2` | `S0-1` `S3-1` `S4-2` |

**두 트랙 모두, 실패한 것은 전부 문서의 잘못이었고 고친 뒤 실습 본문에 교훈으로 남겼습니다.**

실습편 C에서 나온 것: 스킬을 끄는 잘못된 방법, MCP 서버의 한글 이스케이프, `tee /dev/stderr` 의 덮어쓰기,
`C2-2`에서 심은 폴더 규칙이 `C5-1`을 깨뜨린 일, `CLAUDE.md` 준수율이 100%가 아니라는 것.

실습편 S에서 새로 나온 것: 승인해 줄 사람이 없는데 에이전트가 승인을 기다린 일(`S2-4`·`S5-1`·`S5-3`·`S5-4` — 회차마다 다른 곳에서 났고,
결국 설정 파일 대신 명령줄 `--allowedTools` 로 못 박아 해결), 폴더 규칙의 첫 줄이 슬래시 명령의 첫 줄을 밀어낸 일(`S5-2`),
서브에이전트가 절을 덧붙이며 마커를 흘린 일(`S2-5`), 계획 모드가 빈 폴더를 몇 분씩 뒤진 일(`S5-1`),
`work/` 규칙 때문에 파일이 엉뚱한 곳에 생긴 일(`S5-3`), `cut -c` 가 한글을 바이트로 자른 일(`S2-2`).

**스물세 개를 순서대로 쌓으면 하니스가 서로 간섭하기 시작합니다.** 그 간섭이 S 트랙의 실패 목록이 되었고,
그대로 실습 내용이 되었습니다.

외부 리소스를 전혀 참조하지 않는 단일 HTML 파일이므로, 파일 하나만 복사해도 오프라인에서 그대로 열립니다.
