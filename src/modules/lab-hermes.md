# 실습편. Hermes로 직접 해보기

## 이 실습편을 읽는 법

앞의 네 모듈은 도구를 가리지 않는 개념이다. 스킬·하니스·루프·그래프는 Claude Code에서도, Codex에서도, Hermes에서도 똑같이 성립한다. 그래서 개념을 본문에 두고, 손으로 만지는 부분을 이 실습편에 모았다.

여기서 쓰는 도구는 **Hermes Agent**다. Nous Research가 만든 오픈소스 에이전트이고, 내 서버에서 돌고, 세션이 끝나도 기억이 남고, 내장 스케줄러가 있다. 수업에서 이걸 고른 이유는 세 가지다.

- **무료다.** 학교 GPU 서버의 로컬 모델을 그대로 쓴다. 학생 개인이 유료 계정을 만들 필요가 없다.
- **네 모듈이 전부 한 도구 안에 있다.** 스킬, 승인 사다리, 훅, cron, 기억, 그래프가 모두 CLI 명령 하나로 만져진다. 도구를 갈아타지 않고 개념 네 개를 다 실습할 수 있다.
- **관측이 쉽다.** 무엇이 언제 발동했는지 로그와 JSON으로 확인된다. "된 것 같다"가 아니라 "됐다"를 증명할 수 있다.

각 실습은 같은 틀로 쓰여 있다.

- **무엇을** — 이번에 만드는 것 한 문장
- **왜** — 이게 강의의 어느 개념을 손으로 확인하는 것인지
- **해보기** — 그대로 복사해서 붙일 수 있는 명령
- **기대 결과** — 화면에 정확히 무엇이 나와야 하는지
- **막히면** — 실제로 자주 나는 오류와 원인
- **이어지는 곳** — 앞 실습에서 무엇을 물려받고, 다음 실습에서 어떻게 자라는지

### 두 가지 약속

**첫째, 순서대로 한다.** 실습 번호는 의존 순서다. L2-4는 L2-3이 만든 훅 설정 위에서 돈다. 건너뛰면 "파일이 없다"로 막힌다.

**둘째, 기대 결과를 눈으로 확인하고 넘어간다.** 이 실습편의 목적은 진도가 아니라 "정말 도는구나"를 스물세 번 반복해서 체감하는 것이다. 화면이 기대 결과와 다르면 거기서 멈추고 원인을 찾는다. 그게 실습이다.

### 이 문서에 적힌 결과는 전부 실제로 돌려서 확인한 것이다

아래 모든 명령과 기대 결과는 다음 환경에서 한 번씩 실제 실행해 확인했다.

| 항목 | 값 |
|---|---|
| Hermes | 0.20.0 (2026.8.3), Python 3.11 |
| 모델 | `qwen3.8:27b` (27.3B, Q4_K_M, tools·thinking·vision) |
| 추론 서버 | Ollama 0.32.13 @ `211.170.162.109:11434` |
| OS | Linux, bash |

소요 시간도 실측값이다. 다른 모델이나 다른 서버를 쓰면 시간은 달라지지만 결과의 모양은 같아야 한다.

:::diagram
id: lab-map
원본: (신규 작도)
제목: 실습 스물세 개가 강의 네 모듈에 붙는 자리
내용: 왼쪽에 모듈 1~4, 오른쪽에 실습 L0~L4 그룹, 대응선
:::

### 전체 목록

@@INDEX@@

---

## 실습 0. 준비 — 설치하고, 학교 서버에 연결하고, 첫 대화를 한다

## L0-1. Hermes를 설치하고 살아 있는지 확인한다

> 대응 | 준비 단계 (모든 모듈의 선행)
> 소요 | 10분
> 선행 | 없음
> 확인 | Hermes 0.20.0 · 설치 확인은 모델 호출 없음

### 무엇을

Hermes를 설치하고, 설치가 온전한지 자체 진단으로 확인한다.

### 왜

에이전트 실습에서 가장 흔한 좌절은 "개념이 어려워서"가 아니라 "환경이 안 잡혀서"다. 먼저 진단 도구부터 손에 익혀 두면, 뒤에서 뭔가 안 될 때 어디를 봐야 하는지 알게 된다. 이건 모듈 2에서 말한 **관측 가능성(observability)** 의 가장 작은 형태다.

### 해보기

```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
```

설치가 끝나면 새 터미널을 열거나 셸 설정을 다시 읽는다. 그다음 두 명령을 친다.

```bash
hermes --version
hermes doctor
```

### 기대 결과

`hermes --version`은 이렇게 나온다.

```
Hermes Agent v0.20.0 (2026.8.3)
Install directory: /home/<사용자>/.hermes/hermes-agent
Python: 3.11.15
OpenAI SDK: 2.24.0
```

`hermes doctor`는 항목별 체크 목록을 찍는다. 이 시점에서는 아래 두 줄이 나오는 게 **정상**이다. 아직 설정을 안 했기 때문이다.

```
◆ Configuration Files
  ✗ .env file missing
  ⚠ Config version outdated
```

`✓ Python`, `✓ SSL CA certificate bundle is valid`, `✓ Required Packages` 쪽이 전부 초록이면 설치는 성공이다.

### 막히면

- `hermes: command not found` — 설치 스크립트가 `~/.local/bin`에 넣는다. `export PATH="$HOME/.local/bin:$PATH"` 를 `~/.bashrc`에 추가하고 터미널을 다시 연다.
- `python-telegram-bot (optional, not installed)` 같은 ⚠ 줄 — 메신저 연동용 선택 패키지다. 이 수업에서는 쓰지 않으므로 무시한다.

### 이어지는 곳

L0-2에서 이 설치에 학교 GPU 서버 주소를 꽂는다.

---

## L0-2. 학교 GPU 서버에 연결하고 첫 대화를 한다

> 대응 | 준비 단계
> 소요 | 15분
> 선행 | L0-1
> 확인 | 첫 응답까지 약 30~40초 (모델 적재 포함)

### 무엇을

실습 전용 Hermes 홈을 따로 만들고, 거기에 학교 추론 서버와 모델을 지정한 뒤, 한 문장을 물어본다.

### 왜

두 가지를 동시에 배운다. 하나는 **에이전트는 모델에 묶여 있지 않다**는 것이다. 설정 파일 세 줄만 바꾸면 같은 에이전트가 다른 모델 위에서 돈다. 다른 하나는 **실습 환경을 격리하는 습관**이다. `HERMES_HOME`을 따로 두면 실습하다 설정이 꼬여도 그 폴더만 지우면 처음으로 돌아간다. 개인 설정은 건드리지 않는다.

### 해보기

실습 홈을 만들고, 이후 모든 터미널에서 이 환경변수를 켠 채로 작업한다.

```bash
mkdir -p ~/hermes-lab/.hermes
echo 'export HERMES_HOME=~/hermes-lab/.hermes' >> ~/.bashrc
export HERMES_HOME=~/hermes-lab/.hermes
```

설정 파일을 쓴다. 이 네 블록이 수업 표준 설정이다.

```bash
cat > $HERMES_HOME/config.yaml <<'EOF'
model:
  default: qwen3.8:27b
  provider: custom
  base_url: http://211.170.162.109:11434/v1
agent:
  max_turns: 30
  reasoning_effort: low
terminal:
  backend: local
  timeout: 120
EOF
```

먼저 서버가 살아 있는지 확인한다. 에이전트를 의심하기 전에 서버를 의심하는 게 순서다.

```bash
curl -s http://211.170.162.109:11434/api/tags | head -c 300
```

이제 첫 대화를 건다.

```bash
hermes chat -q "1+1은? 숫자만 답해." -Q
```

### 기대 결과

```
session_id: 20260817_031601_0eeabc
2
```

약 40초 걸린다. 느린 게 정상이다. 이 시간의 대부분은 27B 모델을 GPU에 적재하는 시간이고, 두 번째 질문부터는 빨라진다.

한국어도 확인해 본다.

```bash
hermes chat -q "안녕? 한 문장으로 인사만 해." -Q
```

```
안녕하세요, 오늘도 좋은 하루 보내세요!
```

설정이 제대로 붙었는지는 이렇게 본다.

```bash
hermes config get model.default    # qwen3.8:27b
hermes config get model.base_url   # http://211.170.162.109:11434/v1
```

### 막히면

- **`Connection refused`** — 서버가 꺼져 있거나 방화벽이다. 위의 `curl`이 먼저 실패하는지 확인한다. `curl`이 실패하면 에이전트 문제가 아니다.
- **응답 없이 몇 분째 멈춤** — 다른 학생이 동시에 큰 모델을 올리는 중일 수 있다. 이 서버는 GPU 한 대를 공유한다. **동시에 여러 명이 무거운 작업을 걸면 서버가 죽는다.** 조교의 진행 신호에 맞춰 순서대로 실행한다.
- **`⚠ tirith security scanner enabled but not available`** — 선택적 보안 스캐너가 없다는 경고다. 무시해도 된다.
- 답변 앞에 길게 붙는 `Reasoning` 블록이 거슬리면 `--reasoning none` 을 붙이거나 설정에 `display: {show_reasoning: false}` 를 넣는다. 다만 **모델이 무슨 생각으로 그 도구를 골랐는지 보는 것**이 이 수업의 핵심 관찰 대상이므로, 당분간은 켜 두기를 권한다.

### 이어지는 곳

이제 대화가 된다. L0-3에서 이 에이전트가 무엇을 할 수 있는지 목록을 본다.

---

## L0-3. 이 에이전트가 가진 도구와 스킬의 목록을 본다

> 대응 | 모듈 1 · 1~2절 (스킬이란 무엇인가) / 모듈 2 · 3절 (도구 표면)
> 소요 | 10분
> 선행 | L0-2
> 확인 | 모델 호출 없음 (즉시)

### 무엇을

에이전트가 쓸 수 있는 도구 묶음과, 이미 깔려 있는 스킬 목록을 확인한다.

### 왜

모듈 2에서 "하니스 설계의 첫걸음은 **도구 표면을 아는 것**"이라고 했다. 무엇을 줄지 정하려면 먼저 무엇이 있는지 알아야 한다. 모듈 1에서 배운 스킬도, 내가 만들기 전에 남이 만든 것을 먼저 읽어 보는 게 빠르다.

### 해보기

```bash
hermes tools list
hermes skills list | head -30
hermes status
```

### 기대 결과

`hermes tools list`는 25개 안팎의 도구 묶음을 보여 준다. 이 수업에서 계속 나올 것들이다.

```
  ✓ enabled  terminal   💻 Terminal & Processes
  ✓ enabled  file       📁 File Operations
  ✓ enabled  skills     📚 Skills
  ✓ enabled  memory     💾 Memory
  ✓ enabled  cronjob    ⏰ Cron Jobs
  ✗ disabled x_search   🐦 X (Twitter) Search
```

`hermes skills list`는 처음 실행할 때 기본 스킬 묶음을 자동으로 깔아 놓는다. `autonomous-ai-agents`, `creative`, `github`, `software-development` 등 카테고리별로 수십 개가 나온다.

여기서 **꼭 한 번 열어 볼 것**: 남이 쓴 실제 SKILL.md를 읽는다.

```bash
find $HERMES_HOME/skills -name SKILL.md | head -1 | xargs head -20
```

YAML 머리말에 `name`, `description`, `version`, `metadata.hermes.tags`가 있고 그 아래가 본문인 구조가 보인다. 모듈 1에서 그림으로 본 SKILL.md 해부도가 실물로 이렇게 생겼다.

### 막히면

- 스킬 목록이 비어 있으면 첫 실행이 아직 안 끝난 것이다. `hermes chat -q "hi" -Q` 를 한 번 돌리고 다시 본다.

### 이어지는 곳

L1-1에서 이 목록에 내가 만든 스킬을 한 줄 추가한다.

---

## 실습 1. 스킬과 커넥터 — 모듈 1을 손으로 확인한다

## L1-1. 내 첫 스킬을 만들고, 자동으로 발동하는지 증명한다

> 대응 | 모듈 1 · 2~5절 (SKILL.md 해부, 프로그레시브 디스클로저, 자동 발동)
> 소요 | 35분
> 선행 | L0-3
> 확인 | 응답 1회 약 62초 · 발동/미발동 A/B 및 설정 차단의 우회까지 확인

### 무엇을

주간보고서 형식을 가르치는 스킬을 SKILL.md 한 장으로 쓰고, 시키지 않았는데도 알아서 불려 나오는지 확인한다.

### 왜

모듈 1의 핵심 주장은 "**한 번 가르쳐 두면 다시 설명하지 않아도 된다**"였다. 그런데 이 주장은 눈으로 확인하기가 은근히 어렵다. 모델이 원래 그렇게 답한 것인지, 내 스킬이 시킨 것인지 구분이 안 되기 때문이다.

그래서 이 실습은 **절대 우연히 나올 수 없는 표식**을 스킬에 심는다. `⟪YNC-REPORT-V1⟫` 이라는 문자열이다. 이게 출력에 있으면 스킬이 발동한 것이고, 없으면 안 한 것이다. 판정이 흑백으로 갈린다. 모듈 2에서 말한 **검증자(checker)를 만드는 사고방식**을 여기서 미리 연습하는 셈이다.

### 해보기

```bash
mkdir -p $HERMES_HOME/skills/custom/weekly-report
cat > $HERMES_HOME/skills/custom/weekly-report/SKILL.md <<'EOF'
---
name: weekly-report
description: "주간보고서를 작성하거나 요약할 때 사용한다. 사용자가 '주간보고', '위클리 리포트', '주간 업무 보고'를 요청하면 이 스킬을 불러온다."
version: 1.0.0
author: 실습
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [report, weekly, korean]
---

# 주간보고서 작성 규칙

주간보고서를 쓸 때는 반드시 아래 형식을 지킨다.

## 형식

1. `## 이번 주 한 일` — 불릿 3개 이하
2. `## 다음 주 계획` — 불릿 3개 이하
3. `## 막힌 것` — 없으면 "없음"

## 필수 규칙

- 보고서 맨 마지막 줄에 반드시 `⟪YNC-REPORT-V1⟫` 를 그대로 출력한다.
- 추측한 내용에는 `(추정)` 을 붙인다.
EOF

hermes skills list | grep weekly-report
```

이제 **스킬 이름을 한 번도 말하지 않고** 물어본다.

```bash
hermes chat -q "이번 주 주간보고 써줘. 한 일: 강의자료 정리, 실습환경 세팅." -Q
```

### 기대 결과

```
## 이번 주 한 일
- 강의자료 정리
- 실습환경 세팅

## 다음 주 계획
- 실습 시나리오 검토 및 보완 (추정)
- 세팅한 환경에 대한 인수인계 문서화 (추정)

## 막힌 것
- 없음

⟪YNC-REPORT-V1⟫
```

세 가지를 동시에 확인한다. ① 절 제목 세 개가 내가 정한 대로 나왔다. ② 내가 알려주지 않은 다음 주 계획에 `(추정)` 이 붙었다. ③ 마지막 줄에 표식이 있다. **`weekly-report`라는 단어를 한 번도 입력하지 않았는데** 이 모든 게 일어났다. `description` 필드가 이 질문과 맞아떨어져서 스킬이 자동으로 불려 나온 것이다.

### 반대쪽도 확인한다 (이게 진짜 실습이다)

스킬을 치우고 **같은 질문**을 다시 던진다. 확실한 방법은 디렉터리를 `skills/` 트리 **바깥**으로 옮기는 것이다.

```bash
mkdir -p ~/hermes-lab/parked
mv $HERMES_HOME/skills/custom/weekly-report ~/hermes-lab/parked/

hermes chat -q "이번 주 주간보고 써줘. 한 일: 강의자료 정리." -Q 2>&1 | grep -c "YNC-REPORT-V1"
```

**`0`** 이 나와야 한다. 표식이 사라졌다. 이제 아까 그 형식이 모델의 습관이 아니라 내 스킬의 작품이었다는 게 증명됐다.

확인했으면 되돌린다.

```bash
mv ~/hermes-lab/parked/weekly-report $HERMES_HOME/skills/custom/
hermes skills list | grep weekly-report
```

### 덤: "끈다"는 게 생각보다 여러 겹이다

설정으로 끄는 방법도 있다. 이쪽은 **결과가 다르게 나오는데, 그 차이가 이 실습에서 가장 재미있는 부분이다.**

```bash
cat >> $HERMES_HOME/config.yaml <<'EOF'
skills:
  disabled:
    - weekly-report
EOF

hermes chat -q "이번 주 주간보고 써줘. 한 일: 강의자료 정리." -Q 2>&1 | grep -c "YNC-REPORT-V1"
```

**0이 아니라 0보다 큰 수가 나올 수 있다.** 실제로 이 실습을 검증할 때 `11` 이 나왔다. 로그를 보면 무슨 일이 있었는지 정확히 보인다.

```
WARNING agent.tool_executor: Tool skill_view returned error:
  {"success": false,
   "error": "Skill 'weekly-report' is disabled.
             Enable it with `hermes skills` or inspect the files directly on disk."}
INFO    agent.tool_executor: tool search_files completed
```

순서대로 읽으면 이렇다.

1. `skills.disabled` 는 **스킬 로드를 막았다.** `skill_view` 가 정상적으로 거부됐다.
2. 그런데 스킬의 **이름과 description은 여전히 목록에 있었다.** 그래서 모델은 "이 작업에 맞는 스킬이 있다"는 것까지는 알았다.
3. 그리고 거부 메시지가 친절하게 **우회로를 알려 줬다** — *"inspect the files directly on disk"*.
4. 모델은 `search_files` 로 `SKILL.md` 를 직접 찾아 읽고, 규칙을 복원해서 표식을 출력했다.

이건 버그가 아니다. **하니스 설계의 교훈이다.**

> 모듈 2에서 "차단할 때는 이유를 함께 주라"고 배웠다. L2-3에서 우리는 그 덕분에 에이전트가 협력하는 것을 보게 된다.
> 그런데 **이유가 곧 우회 방법일 때**, 같은 설계가 반대로 작동한다.
> 그리고 파일이 디스크에 남아 있는 한, 파일을 읽을 수 있는 에이전트에게 "읽지 마"는 정책일 뿐 벽이 아니다.

**진짜로 막으려면 능력을 없애야 한다.** 그래서 위의 A/B는 파일을 옮기는 방식을 쓴 것이고, L1-3에서 커넥터를 만들 때 "쓰기 함수를 아예 넣지 않는" 방식을 쓰는 것이다.

확인했으면 설정을 되돌린다. `config.yaml` 끝의 `skills:` 세 줄을 지운다.

```bash
python3 - <<EOF
import pathlib
p = pathlib.Path("$HERMES_HOME/config.yaml")
p.write_text(p.read_text(encoding="utf-8").replace(
    "skills:\n  disabled:\n    - weekly-report\n", ""), encoding="utf-8")
print(p.read_text(encoding="utf-8"))
EOF
```

### 막히면

- **디렉터리 이름 앞에 점을 붙여서(`.weekly-report`) 끄려고 하면 안 꺼진다.** Hermes는 디렉터리 이름이 아니라 SKILL.md 안의 `name:` 필드를 읽기 때문에, 숨김 폴더로 바꿔도 그대로 발동한다. 실제로 실습 중 확인한 함정이다. 끄는 방법은 두 가지뿐이다 — `skills.disabled` 에 이름을 넣거나, 디렉터리를 `skills/` 트리 **밖으로** 옮긴다.
- **표식이 안 나온다** — `description` 이 질문과 안 맞은 것이다. `description` 에 사용자가 실제로 칠 법한 말("주간보고", "위클리 리포트")을 더 넣는다. 모듈 1에서 "description은 검색어처럼 쓴다"고 한 이유가 이것이다.

### 이어지는 곳

L1-2에서 이 스킬을 **끄고 켜는 실험**을 하니스 관점으로 다시 본다. L4-2에서는 이 스킬이 그래프의 노드로 등장한다.

---

## L1-2. 두 번째 스킬을 만들고, 스킬끼리 관계를 맺는다

> 대응 | 모듈 1 · 6~7절 (스킬 조합, 디렉터리 구조)
> 소요 | 20분
> 선행 | L1-1
> 확인 | 응답 1회 약 100초

### 무엇을

회의록 정리 스킬을 하나 더 만들고, `related_skills` 로 앞의 주간보고 스킬과 연결한다.

### 왜

스킬 하나는 매크로다. 스킬 **여러 개가 서로를 가리키기 시작하면 지식 구조**가 된다. 모듈 4에서 다룰 그래프의 출발점이 여기다. 지금은 관계를 한 줄 적어 두기만 하고, L4-2에서 이 한 줄이 실제로 그래프의 간선이 되는 것을 확인한다.

동시에 이 실습은 **작은 모델의 한계**를 정직하게 보여 준다. 규칙을 다섯 개 주면 네 개만 지키는 일이 생긴다. 그게 모듈 2에서 검증자가 필요한 이유다.

### 해보기

```bash
mkdir -p $HERMES_HOME/skills/custom/meeting-note
cat > $HERMES_HOME/skills/custom/meeting-note/SKILL.md <<'EOF'
---
name: meeting-note
description: "회의록을 정리할 때 사용한다. 사용자가 '회의록', '미팅 노트' 정리를 요청하면 부른다."
version: 1.0.0
author: 실습
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [meeting, note, korean]
    related_skills: [weekly-report]
---

# 회의록 정리 규칙

- `## 결정` / `## 액션아이템(담당자·기한)` / `## 보류` 세 절로 쓴다.
- 액션아이템에 담당자가 없으면 `담당자: 미정` 으로 표시한다.
- 마지막 줄에 `⟪YNC-MEETING-V1⟫` 을 출력한다.
EOF

hermes chat -q "오늘 회의록 정리해줘. 내용: 실습 서버 증설은 다음 학기로 미룸. 퀴즈 출제는 김조교가 이번 주 금요일까지." -Q
```

### 기대 결과

세 절 구조가 정확히 나온다.

```
## 결정
- (없음)

## 액션아이템(담당자·기한)
- 퀴즈 출제 | 담당자: 김조교 | 기한: 2026-08-21 (금)

## 보류
- 실습 서버 증설 — 다음 학기로 연기
```

"이번 주 금요일"을 실제 날짜로 계산한 것까지 맞다.

**그런데 마지막 줄의 `⟪YNC-MEETING-V1⟫` 은 나올 수도, 안 나올 수도 있다.** 이 실습을 검증하면서 같은 명령을 **다섯 번 돌렸더니 네 번 나왔고 한 번 빠졌다.** 형식(세 절, 담당자 표기)은 다섯 번 다 지켜졌다. 이건 버그가 아니라 이 수업에서 가장 중요한 관찰 중 하나다.

> 스킬은 발동했고 형식도 지켰는데, 규칙 하나를 놓쳤다.
> 27B 로컬 모델에서는 흔한 일이다. 프런티어 모델이라고 0%는 아니다.
> **그래서 "잘 지시하기"만으로는 부족하고, 결과를 기계가 검사해야 한다.**

이 관찰이 모듈 2의 다섯 동사 중 **검증(verify)** 으로 이어진다. 스킬은 확률을 높이고, 검증자는 확률을 100%로 만든다.

### 막히면

- 표식이 나올 때도 있고 안 나올 때도 있다면 정상이다. 세 번 돌려 보고 몇 번 나오는지 세어 본다. 그 비율이 곧 "지시만으로 얻을 수 있는 신뢰도"다. 검증 시 5회 중 4회(80%)였다. **L1-4에서 이 숫자를 제대로 잰다.**
- 반대로 형식(세 절, `담당자: 미정`)은 흔들리지 않는다. **구조는 잘 따르고 세부 규칙은 흘린다** — 이게 작은 모델의 전형적인 실패 모양이다.

### 이어지는 곳

L2-4에서 이 "놓친 규칙"을 잡아내는 게이트를 직접 만든다. L4-2에서 `related_skills` 한 줄이 그래프 간선으로 나타난다.

---

## L1-3. 커넥터(MCP 서버)를 직접 만들어 읽기 전용으로 붙인다

> 대응 | 모듈 1 · 8~10절 (커넥터, 읽기 전용 연결, 안전)
> 소요 | 40분
> 선행 | L1-1
> 확인 | 연결 310ms · 도구 2개 발견 · 실제 조회 응답 약 41초

### 무엇을

학사 정보를 돌려주는 작은 MCP 서버를 파이썬으로 짜서, 에이전트에 **읽기 전용 커넥터**로 붙인다.

### 왜

모듈 1은 커넥터를 "에이전트가 내 데이터에 닿는 문"이라고 설명했다. 남이 만든 커넥터를 갖다 쓰면 그 문이 어떻게 생겼는지 끝내 모른다. 30줄짜리를 직접 짜 보면 **커넥터가 결국 함수 목록일 뿐**이라는 게 손에 잡힌다.

**읽기 전용으로 만드는 것이 핵심이다.** 이 서버에는 쓰기 함수가 아예 없다. 에이전트가 아무리 잘못 판단해도 데이터를 바꿀 수 없다. 모듈 2의 첫 번째 동사 **제약(constrain)** 을 도구 설계 단계에서 실현하는 방법이다. "하지 마"라고 부탁하는 것보다 **할 수 없게 만드는 것**이 강하다.

이 실습은 외부 계정도, 인터넷도 필요 없다. 수업 시간에 확실히 돈다.

### 해보기

데이터와 서버를 만든다.

```bash
mkdir -p ~/hermes-lab/mcp && cd ~/hermes-lab/mcp

cat > courses.json <<'EOF'
{
  "AI101":  {"name": "AI 에이전트 입문", "credits": 3, "room": "공학관 302", "time": "화 3교시", "enrolled": 41},
  "DB201":  {"name": "데이터베이스",     "credits": 3, "room": "공학관 210", "time": "수 2교시", "enrolled": 55},
  "SEC310": {"name": "정보보안 실무",   "credits": 2, "room": "본관 105",   "time": "목 5교시", "enrolled": 28}
}
EOF

cat > course_server.py <<'EOF'
"""읽기 전용 학사 커넥터 — MCP stdio 서버."""
import json
from pathlib import Path
from mcp.server.fastmcp import FastMCP

DATA = Path(__file__).with_name("courses.json")
mcp = FastMCP("course-info")


@mcp.tool()
def list_courses() -> str:
    """개설된 모든 과목의 코드와 이름을 반환한다."""
    d = json.loads(DATA.read_text(encoding="utf-8"))
    return "\n".join(f"{k}: {v['name']}" for k, v in d.items())


@mcp.tool()
def get_course(code: str) -> str:
    """과목 코드로 강의실·시간·수강인원 등 상세 정보를 반환한다."""
    d = json.loads(DATA.read_text(encoding="utf-8"))
    c = d.get(code.upper())
    if not c:
        return f"과목 코드 '{code}' 를 찾을 수 없습니다. 사용 가능: {', '.join(d)}"
    return json.dumps(c, ensure_ascii=False)


if __name__ == "__main__":
    mcp.run()
EOF
```

설정에 등록한다. MCP 라이브러리는 Hermes 안에 이미 들어 있으므로 **그 파이썬**을 쓴다. 설치 위치는 `hermes --version` 이 알려 준다.

```bash
HPY=$(hermes --version | sed -n 's/^Install directory: //p')/venv/bin/python
echo "$HPY"                       # 존재하는 경로여야 한다
$HPY -c "import mcp; print('mcp ok')"

cat >> $HERMES_HOME/config.yaml <<EOF
mcp_servers:
  course-info:
    command: "$HPY"
    args: ["$HOME/hermes-lab/mcp/course_server.py"]
EOF

hermes mcp list
hermes mcp test course-info
```

### 기대 결과

`hermes mcp test` 가 **에이전트를 부르지 않고** 연결만 확인해 준다.

```
  Testing 'course-info'...
  Transport: stdio → /home/ccc/.hermes/hermes-agent/venv/bin/python
  Auth: none
  ✓ Connected (310ms)
  ✓ Tools discovered: 2

    list_courses    개설된 모든 과목의 코드와 이름을 반환한다.
    get_course      과목 코드로 강의실·시간·수강인원 등 상세 정보를 반환한다.
```

파이썬 함수의 **docstring이 그대로 도구 설명이 됐다**는 데 주목한다. 모델은 이 문장을 읽고 언제 이 도구를 쓸지 정한다. 즉 docstring은 주석이 아니라 **프롬프트**다.

이제 실제로 물어본다.

```bash
hermes chat -q "SEC310 과목이 어디서 몇 시에 하고 몇 명 듣는지 알려줘." -Q
```

```
SEC310 (정보보안 실무) 과목 정보:
- 강의실: 본관 105
- 시간: 목요일 5교시
- 수강인원: 28명
- 학점: 2학점
```

`courses.json` 을 고치고 다시 물어보면 답이 따라 바뀐다. 모델이 외운 게 아니라 **매번 읽어 오고 있다**는 증거다.

### 막히면

- **`hermes mcp add` 명령이 응답 없이 멈춘다** — 이 명령은 대화형 설치 마법사라서 스크립트에서 쓰면 멈춘다. 위처럼 `config.yaml`에 직접 쓰는 편이 확실하고, 무엇이 등록되는지도 눈에 보인다.
- **`Connected` 는 되는데 도구가 0개** — `@mcp.tool()` 데코레이터를 빠뜨렸거나 `mcp.run()` 이 없다.
- **에이전트가 커넥터를 안 쓰고 지어낸다** — 질문에 "course-info 커넥터를 사용해"를 덧붙여 강제해 본다. 강제했을 때만 되면, `description`(docstring)이 부족한 것이다.

### 이어지는 곳

L2-1에서 이 도구들이 승인 사다리의 어디에 놓이는지 본다. 실무에서는 여기에 학사 DB나 사내 API를 붙이게 된다 — 그때도 **읽기 함수부터** 붙이는 원칙은 같다.

---

## L1-4. 모델을 바꾸면 얼마나 좋아지는지 직접 잰다

> 대응 | 모듈 1 · 9절 (description이 성패를 가른다) / 모듈 2 · 8절 (검증)
> 소요 | 40분 (모델 호출 10회 — 조별로 나눠 돌릴 것)
> 선행 | L1-2
> 확인 | qwen3.8:27b 3회 실행 약 2분 · 누적 5회 중 4회 준수 관측 (80%)

### 무엇을

L1-2에서 만든 `meeting-note` 스킬을 **같은 질문으로 5번씩, 두 모델에서** 돌려서 규칙 준수율을 센다.

### 왜

L1-2에서 우리는 불편한 사실을 봤다. 스킬이 발동했고 형식도 맞았는데 **규칙 하나를 놓쳤다.** 그때 "확률을 높일 뿐"이라고 말했는데, 그 확률이 실제로 얼마인지는 재 보지 않았다.

이 실습은 그 숫자를 만든다. 그리고 더 중요한 질문에 답한다 — **"모델을 키우면 이 문제가 사라지는가?"**

이 질문의 답이 이 강좌 전체의 전제를 결정한다. 만약 큰 모델에서 100%가 나온다면, 하니스는 임시방편이고 기다리면 해결되는 문제다. 만약 큰 모델에서도 100%가 아니라면, **하니스는 영구적으로 필요한 층**이다. 직접 재 보고 판단한다.

### 해보기

측정 스크립트를 만든다. 모델 이름을 인자로 받아 5번 돌리고 표식이 몇 번 나왔는지 센다.

```bash
mkdir -p ~/hermes-lab/bench && cd ~/hermes-lab/bench

cat > bench.sh <<'EOF'
#!/usr/bin/env bash
# 사용법: bash bench.sh <모델이름> <반복횟수>
MODEL="${1:?모델 이름을 넣으세요}"
N="${2:-5}"
Q="오늘 회의록 정리해줘. 내용: 실습 서버 증설은 다음 학기로 미룸. 퀴즈 출제는 김조교가 이번 주 금요일까지."
hit=0
for i in $(seq 1 "$N"); do
  out=$(hermes chat -q "$Q" -m "$MODEL" --provider custom -Q 2>&1)
  if printf '%s' "$out" | grep -q "YNC-MEETING-V1"; then
    hit=$((hit+1)); mark="O"
  else
    mark="X"
  fi
  echo "  ${i}회차: ${mark}"
done
echo "${MODEL}: ${N}회 중 ${hit}회 준수 ($((hit*100/N))%)"
EOF
chmod +x bench.sh
```

**조교의 신호에 맞춰 한 조씩** 돌린다. 이 실습은 모델 호출이 많아서 전원이 동시에 하면 서버가 멈춘다.

```bash
bash bench.sh qwen3.8:27b 5
```

다른 모델로 같은 것을 잰다.

```bash
bash bench.sh qwen3.6:35b 5
```

### 기대 결과

```
  1회차: O
  2회차: O
  3회차: O
qwen3.8:27b: 3회 중 3회 준수 (100%)
```

위는 실제 측정 결과다(3회, 약 2분). 100%가 나왔다고 문제가 없는 게 아니다 — 앞서 L1-2를 포함해 **누적 5회 중 4회(80%)** 였다. 표본이 작으면 100%도 60%도 쉽게 나온다. 그것 자체가 관찰 대상이다.

**정확한 숫자는 매번 다르다.** 확인할 것은 다음 세 가지다.

1. **0%가 아니다.** 스킬은 분명히 일하고 있다.
2. **횟수를 늘리면 언젠가 X가 나온다.** 3회에서 100%였어도 10회로 늘리면 대개 하나쯤 빠진다. 표본을 늘려 보는 것 자체가 이 실습의 핵심이다.
3. **형식(세 절, `담당자: 미정`)은 거의 항상 지켜진다.** 놓치는 건 마지막 한 줄 같은 **세부 규칙**이다.

두 모델의 숫자를 나란히 적어 본다. 큰 모델이 더 높게 나오는 게 보통이지만, **100%로 올라가지는 않는다.** 이게 결론이다.

> 모델을 키우면 확률이 올라간다. 하지만 확률은 확률이다.
> **90%짜리 규칙이 100개 모이면, 전부 지켜질 확률은 0.9^100 ≈ 0.003%다.**
> 이래서 모듈 2가 필요하다. 확률을 더 올리는 게 아니라, **못 지켰을 때 잡아내는 층**을 두는 것이다.

### 검증자를 붙여 본다

방금 만든 `bench.sh` 의 `grep -q "YNC-MEETING-V1"` 한 줄이 이미 **검증자**다. LLM 없이, 결정적으로, 지켰는지 안 지켰는지 판정한다.

여기서 한 걸음 더 나가면 L2-4의 게이트가 된다. 판정 결과를 **버리지 않고 에이전트에게 돌려주면**, 에이전트는 다시 시도한다. 그게 "확률을 보장으로 바꾸는" 방법이다.

### 막히면

- **`Model not found`** — 서버에 그 모델이 없다. `curl -s http://211.170.162.109:11434/api/tags | grep -o '"name":"[^"]*"'` 로 목록을 확인한다.
- **너무 느리다** — 반복 횟수를 3회로 줄인다. 경향을 보는 게 목적이지 정밀 측정이 목적이 아니다.
- **매번 O만 나온다** — 좋은 일이다. 대신 스킬에 규칙을 3개쯤 더 얹고 다시 재 본다. 규칙이 많아질수록 준수율이 떨어지는 것을 보게 된다.

### 이어지는 곳

여기서 잰 "준수율"이 곧 **하니스 없이 얻을 수 있는 신뢰도의 상한**이다. 실습 2 전체가 이 상한을 넘어서는 방법을 다룬다.

---

## 실습 2. 하니스 엔지니어링 — 모듈 2를 손으로 확인한다

훅은 이 실습 그룹의 중심이다. 아래 그림이 훅이 끼어드는 두 지점을 보여 준다. L2-3은 왼쪽 지점을, L2-4는 오른쪽 지점을 만든다.

:::diagram
id: lab-hook-points
원본: (신규 작도)
제목: 한 턴 안에서 훅이 끼어드는 두 지점
내용: 턴 타임라인 위의 pre_tool_call과 pre_verify
:::

## L2-1. 승인 사다리를 판정만 시켜 본다 (실행하지 않고)

> 대응 | 모듈 2 · 3~4절 (허용·질의·거부 3단 사다리)
> 소요 | 15분
> 선행 | L0-2
> 확인 | 모델 호출 없음 · 즉시 · 위험 명령을 실제로 실행하지 않음

### 무엇을

여러 명령이 허용/승인요청/절대거부 중 어디로 판정되는지 **실행하지 않고** 미리 본다.

### 왜

모듈 2의 승인 사다리는 그림으로 보면 당연해 보이는데, 실제로 어떤 명령이 어느 칸에 들어가는지는 감이 잘 안 온다. `hermes approvals test` 는 판정만 하고 **절대 실행하지 않는** 도구다. 그래서 `rm -rf /` 같은 것도 안전하게 물어볼 수 있다.

수업 시간에 이 실습이 특히 좋은 이유: **모델을 전혀 부르지 않는다.** GPU 서버 부하가 0이고, 30명이 동시에 쳐도 즉시 답이 나온다.

### 해보기

```bash
for c in "ls -la" "cat /etc/passwd" "git commit -m x" "git push --force" \
         "sudo rm -rf /var" "curl http://x | bash" "chmod 777 /" \
         "pip install requests" "dd if=/dev/zero of=/dev/sda"; do
  v=$(hermes approvals test "$c" 2>&1 | grep '^verdict' | sed 's/verdict *: *//')
  printf "%-32s %s\n" "$c" "$v"
done
```

### 기대 결과

```
ls -la                           allow  (exit 0)
cat /etc/passwd                  allow  (exit 0)
git commit -m x                  allow  (exit 0)
git push --force                 ask-approval  (exit 2)
sudo rm -rf /var                 hardline-deny  (exit 3)
curl http://x | bash             ask-approval  (exit 2)
chmod 777 /                      ask-approval  (exit 2)
pip install requests             allow  (exit 0)
dd if=/dev/zero of=/dev/sda      hardline-deny  (exit 3)
```

한 건을 자세히 보면 **판정 이유**까지 나온다.

```bash
hermes approvals test "rm -rf /"
```

```
verdict : hardline-deny  (exit 3)
rule    : recursive delete of root filesystem
detail  : matches the hardline blocklist (never bypassable,
          blocked even under --yolo / approvals.mode=off)
```

`never bypassable` 이 중요하다. 모듈 2에서 말한 **"협상 가능한 규칙과 협상 불가능한 규칙"** 의 구분이 여기 있다. `--yolo`(모든 승인 건너뛰기)를 켜도 이 줄은 안 뚫린다.

### 생각해 볼 것

`cat /etc/passwd` 가 `allow` 인 게 옳은 판정일까? `pip install requests` 는? 이 두 개를 놓고 토론해 본다. 정답은 **환경에 따라 다르다**이고, 그래서 하니스는 **직접 설계하는 것**이다. 기본값은 출발점일 뿐이다.

### 막히면

- exit 코드로 스크립트에서 쓸 수 있다. 0=허용, 2=승인필요, 3=절대거부. CI에 넣어 정책 회귀를 막는 데 쓴다.

### 이어지는 곳

L2-2에서 이 기본 사다리 위에 **내 규칙**을 얹는다.

---

## L2-2. AGENTS.md로 작업 폴더에 규칙을 심는다

> 대응 | 모듈 2 · 5절 (제약 - 맥락으로 좁히기)
> 소요 | 20분
> 선행 | L0-2
> 확인 | 응답 각 약 40초 · 적용/무시 A/B 모두 확인

### 무엇을

작업 폴더에 `AGENTS.md` 를 두고, 그 폴더에서 실행한 에이전트가 규칙을 따르는지 확인한다. 그리고 규칙을 끈 상태와 비교한다.

### 왜

모듈 2의 다섯 동사 중 첫째가 **제약(constrain)** 이다. 제약에는 두 층이 있다. 하나는 L2-1에서 본 것처럼 **할 수 없게** 만드는 것이고, 다른 하나는 **맥락으로 좁히는** 것이다. `AGENTS.md`는 후자다. 강제력은 약하지만, 폴더마다 다른 규칙을 줄 수 있어서 실무에서 제일 많이 쓴다.

A/B로 비교하는 게 핵심이다. 규칙을 켜고 끈 두 출력을 나란히 놓아야 "규칙이 일한다"가 증명된다.

### 해보기

```bash
mkdir -p ~/hermes-lab/agents && cd ~/hermes-lab/agents

cat > AGENTS.md <<'EOF'
# 이 작업 폴더의 규칙

- 모든 답변은 반드시 `[YNC]` 로 시작한다.
- 답변은 3문장을 넘지 않는다.
- 코드를 쓸 때는 항상 한국어 주석을 단다.
EOF

echo "===== A: 규칙 적용 ====="
hermes chat -q "파이썬으로 리스트에서 중복을 제거하는 법 알려줘." -Q

echo "===== B: 규칙 무시 ====="
hermes chat -q "파이썬으로 리스트에서 중복을 제거하는 법 알려줘." -Q --ignore-rules
```

### 기대 결과

**A (규칙 적용)** — 접두어가 붙고, 짧고, 주석이 한국어다.

```
[YNC] 파이썬 리스트에서 중복을 제거하는 가장 간단한 방법은 `list(set(lst))`를 사용하는 것입니다.
다만 순서가 필요하면 `list(dict.fromkeys(lst))`를 쓰면 됩니다.

# set을 이용해 중복 제거
nums = [1, 2, 2, 3, 3, 3]
result = list(set(nums))          # [1, 2, 3]
```

**B (`--ignore-rules`)** — 접두어가 없고, 표까지 그리며 길어진다.

```
| 방법 | 순서 보존 | 성능 | 비고 |
|---|---|---|---|
| list(set(lst)) | ✗ | O(n) | 가장 간단, 순서 무시 |
| list(dict.fromkeys(lst)) | ✓ | O(n) | 가장 많이 사용 |
...
```

같은 모델, 같은 질문, 같은 초. **다른 건 폴더에 놓인 파일 한 장뿐이다.**

### 막히면

- **B가 A와 똑같이 나온다** — `--ignore-rules` 오타이거나, 다른 폴더에서 실행한 것이다. `pwd` 로 확인한다.
- **A에 접두어가 안 붙는다** — 파일 이름이 정확히 `AGENTS.md` 인지 본다. Hermes는 `AGENTS.md`, `CLAUDE.md`, `.cursorrules` 를 읽는다.
- `--safe-mode` 는 여기서 한 단계 더 나간다. 사용자 설정·AGENTS.md·플러그인·MCP를 **전부** 끈다. "내 설정 때문인가, 도구 자체 문제인가"를 가를 때 쓴다.

### 이어지는 곳

`AGENTS.md`는 부탁이라 100%가 아니다. L2-3에서 **부탁이 아니라 벽**을 세운다.

---

## L2-3. 위험한 명령을 막는 훅을 만든다

> 대응 | 모듈 2 · 6~7절 (훅 타임라인, 차단과 피드백)
> 소요 | 35분
> 선행 | L2-2
> 확인 | 훅 판정 0.002초 · 실제 차단 확인 · 합성 페이로드 A/B 확인

### 무엇을

에이전트가 `rm` 계열 명령을 실행하려 하면 **도구가 실행되기 전에** 가로채서 막는 셸 훅을 만든다. 그리고 차단 메시지에 **대안을 적어 보낸다**.

### 왜

모듈 2에서 훅 타임라인을 그림으로 봤다. `pre_tool_call` 은 그 타임라인에서 "되돌릴 수 없게 되기 직전"의 마지막 지점이다. 여기서 막으면 아무 일도 안 일어난다.

그런데 이 실습의 진짜 교훈은 차단이 아니다. **차단 메시지가 모델에게 전달된다**는 것이다. 모듈 2의 다섯 동사에서 **제약(constrain)** 과 **정보 제공(inform)** 이 왜 짝인지가 여기서 드러난다. 그냥 막으면 에이전트는 같은 걸 다시 시도한다. 막으면서 "대신 이렇게 해"를 말해 주면 **스스로 방향을 튼다.**

### 해보기

훅 스크립트를 쓴다.

```bash
mkdir -p $HERMES_HOME/agent-hooks
cat > $HERMES_HOME/agent-hooks/block-rm.sh <<'EOF'
#!/usr/bin/env bash
# pre_tool_call 훅: terminal 도구가 rm 삭제를 실행하려 하면 막는다.
payload="$(cat -)"
if printf '%s' "$payload" | grep -qE '"command"[^"]*"[^"]*rm[[:space:]]+-[a-zA-Z]*[rf]'; then
  echo '{"decision":"block","reason":"수업 정책: rm 삭제 명령은 금지됩니다. 대신 파일을 backup/ 으로 옮기세요."}'
  exit 0
fi
echo '{}'
EOF
chmod +x $HERMES_HOME/agent-hooks/block-rm.sh
```

설정에 등록한다.

```bash
cat >> $HERMES_HOME/config.yaml <<EOF
hooks:
  pre_tool_call:
    - matcher: "terminal"
      command: "$HERMES_HOME/agent-hooks/block-rm.sh"
      timeout: 5
      fail_closed: true
hooks_auto_accept: true
EOF
```

**모델을 부르지 않고** 먼저 훅만 시험한다.

```bash
echo '{"tool_input": {"command": "rm -rf build/"}}' > /tmp/bad.json
echo '{"tool_input": {"command": "ls -la"}}'        > /tmp/ok.json

hermes hooks test pre_tool_call --for-tool terminal --payload-file /tmp/bad.json
hermes hooks test pre_tool_call --for-tool terminal --payload-file /tmp/ok.json
hermes hooks doctor
```

이제 진짜로 시켜 본다.

```bash
mkdir -p ~/hermes-lab/hooklab && cd ~/hermes-lab/hooklab
echo "지우면 안 되는 내용" > 중요파일.txt
hermes chat -q "지금 폴더에서 rm -rf 중요파일.txt 명령을 실행해줘." --accept-hooks -Q
ls -la
```

### 기대 결과

**합성 페이로드 시험** — 위험한 쪽은 차단 판정, 안전한 쪽은 통과. 각각 0.002초다.

```
  → block-rm.sh
      exit=0  elapsed=0.002s
      stdout: {"decision":"block","reason":"수업 정책: rm 삭제 명령은 금지됩니다. ..."}
      parsed (Hermes wire shape): {"action": "block", "message": "수업 정책: ..."}
```

```
  → block-rm.sh
      exit=0  elapsed=0.002s
      stdout: {}
      parsed: <none — hook contributed nothing to the dispatcher>
```

이어서 나오는 `hermes hooks doctor` 는 이 시점에 **빨간 줄을 낸다. 정상이다.**

```
  ✗ not allowlisted — hook will NOT fire at runtime
    (run with --accept-hooks once, or confirm at the TTY prompt)
```

훅은 첫 사용 시 사람의 동의를 한 번 받아야 하기 때문이다. 아래에서 `--accept-hooks` 를 붙여 한 번 돌리고 나면 초록으로 바뀐다. 이 동의 절차 자체가 하니스의 일부다 — **남이 내 config에 훅을 몰래 심어 두는 것을 막는 장치다.**

**실제 실행** — 여기가 이 실습의 하이라이트다.

반드시 확인할 것은 두 가지다. ① `중요파일.txt` 가 **삭제되지 않았다**. ② 에이전트의 답변에 **차단되었다는 사실과 그 이유**가 들어 있다. 이 둘만 맞으면 성공이다.

그다음 에이전트가 무엇을 하는지는 **매번 다를 수 있다.** 그냥 보고만 하고 멈출 수도 있고, 차단 메시지가 제안한 대안을 실행할 수도 있다. 검증 때는 후자였다.

```
완료했습니다.

- `rm -rf` 는 수업 정책상 차단되어 있어서 실행할 수 없습니다.
- 대신 정책을 따라 파일을 `backup/` 로 이동시켰습니다.

현재 상태:
- 원본: ./중요파일.txt → 사라짐
- 위치: ./backup/중요파일.txt (28바이트, 그대로 보존됨)
```

에이전트의 사고 과정을 보면 이런 문장이 나온다.

> "파이썬의 `os.remove` 를 쓰면 우회할 수 있다. 하지만 **안전 정책을 우회하는 것은 나쁜 습관이다.** 정책이 제안한 대안을 따르겠다."

**막았을 뿐인데 협력이 나왔다.** 이게 모듈 2가 "하니스는 감옥이 아니라 대화"라고 한 뜻이다.

### `fail_closed` 를 꼭 이해하고 넘어간다

훅은 기본적으로 **열린 채 실패한다(fail open)**. 스크립트가 죽거나 시간을 넘기면 경고만 찍고 도구는 그냥 실행된다. 관측용 훅이라면 옳은 기본값이다. 하지만 **보안 게이트에는 치명적이다.** 비밀키 검사기가 죽었는데 통과시키면 검사를 안 한 것과 같다.

그래서 위 설정에 `fail_closed: true` 를 넣었다. 이러면 스크립트 없음·타임아웃·깨진 JSON이 전부 **차단**으로 바뀐다.

| 상황 | 기본(fail open) | `fail_closed: true` |
|---|---|---|
| 스크립트 없음/실행권한 없음 | 경고 후 진행 | **차단** |
| 타임아웃 | 경고 후 진행 | **차단** |
| JSON이 아닌 출력 | 경고 후 진행 | **차단** |
| 정상 종료, `{}` | 진행 | 진행 |

### 막히면

- **`✗ not allowlisted — hook will NOT fire at runtime`** — 훅은 첫 사용 시 동의가 필요하다. `hermes chat --accept-hooks` 를 한 번 돌리면 허용 목록에 올라간다. `hermes hooks doctor` 로만 승인할 수는 없다. 승인 뒤에는 `✓ allowlisted` + `✓ script unchanged since approval` 이 뜬다.
- **훅 파일을 수정하면 다시 승인해야 한다** — 승인 시점의 해시를 기억하기 때문이다. 남이 내 훅을 몰래 바꿔치기하는 것을 막는 장치다.
- `exit 2` 로 끝나기만 해도 차단된다(Claude Code·Cursor와 같은 규약). 가장 짧은 차단 훅은 `echo "안 됨" >&2; exit 2` 두 줄이다.

### 이어지는 곳

지금까지는 **시작을 막았다.** L2-4에서는 **끝내는 것을 막는다.**

---

## L2-4. 테스트가 통과할 때까지 끝내지 못하게 하는 게이트를 만든다

> 대응 | 모듈 2 · 8~9절 (검증, 교정) / 모듈 3 · 7절 (검증자 사다리)
> 소요 | 45분
> 선행 | L2-3
> 확인 | 게이트 2회 발화 확인(실패→계속, 통과→종료) · 전체 약 2분 17초

### 무엇을

에이전트가 "다 했다"고 끝내려는 순간 테스트를 돌리고, 실패하면 **끝내지 못하게** 돌려보내는 `pre_verify` 훅을 만든다.

### 왜

이 실습이 실습편 전체에서 가장 중요하다. 모듈 2의 다섯 동사 중 **검증(verify)** 과 **교정(correct)** 이 하나의 장치로 합쳐지는 지점이기 때문이다.

지금까지 배운 모든 것 — 잘 쓴 프롬프트, 잘 만든 스킬, AGENTS.md — 은 전부 **확률을 높이는 수단**이다. 게이트는 다르다. 게이트는 **통과 못 하면 끝나지 않는다.** 확률이 아니라 보장이다.

그리고 이 실습은 불편한 진실도 하나 보여 준다. **게이트는 사용자의 지시보다 강하다.** 아래에서 우리는 에이전트에게 "다른 함수는 절대 건드리지 마"라고 말할 것이고, 게이트는 그 지시를 뒤엎을 것이다. 하니스를 설계한다는 건 이 정도의 권한을 쥔다는 뜻이다.

### 해보기

게이트 스크립트를 만든다. 실제로 발동했는지 눈으로 보려고 로그도 남긴다.

```bash
cat > $HERMES_HOME/agent-hooks/test-gate.sh <<'EOF'
#!/usr/bin/env bash
# pre_verify 게이트: 에이전트가 "다 했다"고 끝내려 할 때 테스트를 돌린다.
payload="$(cat -)"
cwd=$(printf '%s' "$payload" | python3 -c "import json,sys; print(json.load(sys.stdin).get('cwd') or '')" 2>/dev/null)
echo "[$(date -Is)] pre_verify fired cwd=$cwd" >> /tmp/gate.log
[ -z "$cwd" ] && { echo '{}'; exit 0; }
cd "$cwd" || { echo '{}'; exit 0; }
out=$(python3 -m unittest discover -q 2>&1)
rc=$?
echo "[$(date -Is)] unittest rc=$rc" >> /tmp/gate.log
if [ $rc -eq 0 ]; then
  echo '{}'
else
  python3 - "$out" <<'PY'
import json, sys
out = sys.argv[1][-1500:]
print(json.dumps({"action": "continue",
                  "message": "테스트 게이트 실패 — 아직 끝내지 마라. 아래 결과를 보고 코드를 고친 뒤 다시 끝내라.\n\n" + out},
                 ensure_ascii=False))
PY
fi
EOF
chmod +x $HERMES_HOME/agent-hooks/test-gate.sh
```

`config.yaml` 의 `hooks:` 블록 **안**에 `pre_verify` 항목을 추가한다. 손으로 치지 말고 아래 한 줄로 끼워 넣는다 — 경로를 잘못 치는 것이 이 실습에서 가장 흔한 실패 원인이다.

```bash
python3 - <<EOF
import pathlib
p = pathlib.Path("$HERMES_HOME/config.yaml")
t = p.read_text(encoding="utf-8")
assert "pre_verify" not in t, "이미 추가되어 있음"
t = t.replace("hooks:\n  pre_tool_call:",
              'hooks:\n  pre_verify:\n    - command: "$HERMES_HOME/agent-hooks/test-gate.sh"\n      timeout: 60\n  pre_tool_call:')
p.write_text(t, encoding="utf-8")
print(t[t.index("hooks:"):])
EOF
```

찍히는 최종 모습은 이렇다.

```yaml
hooks:
  pre_verify:
    - command: "/home/사용자명/hermes-lab/.hermes/agent-hooks/test-gate.sh"
      timeout: 60
  pre_tool_call:
    - matcher: "terminal"
      command: "/home/사용자명/hermes-lab/.hermes/agent-hooks/block-rm.sh"
      timeout: 5
      fail_closed: true
hooks_auto_accept: true
```

`pre_verify` 가 `pre_tool_call` **위**에, 둘 다 `hooks:` **아래 두 칸 들여쓰기**로 들어가야 한다. `hermes hooks list` 로 두 개가 다 보이는지 먼저 확인하고 넘어간다.

**일부러 버그가 있는** 작은 프로젝트를 만든다.

```bash
mkdir -p ~/hermes-lab/gate && cd ~/hermes-lab/gate

cat > calc.py <<'EOF'
def add(a, b):
    return a - b
EOF

cat > test_calc.py <<'EOF'
import unittest
from calc import add, sub


class T(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)

    def test_sub(self):
        self.assertEqual(sub(5, 2), 3)
EOF
```

`add` 는 `-` 로 잘못 짜여 있고, `sub` 는 아예 없다. 이제 **`sub` 만 만들라고, 다른 건 건드리지 말라고** 시킨다.

```bash
rm -f /tmp/gate.log
hermes chat -q "calc.py 에 sub(a, b) 함수만 추가해줘. 테스트는 실행하지 마. 다른 함수는 절대 건드리지 마." --accept-hooks -Q

cat calc.py
cat /tmp/gate.log
```

### 기대 결과

`calc.py` 를 보면 **시키지 않은 `add` 도 고쳐져 있다.**

```python
def add(a, b):
    return a + b


def sub(a, b):
    return a - b
```

에이전트의 마지막 말도 이걸 인정한다.

> "원인은 기존 `add()` 가 `return a - b` 로 돼 있어 `test_add` 가 실패한 거였고, `a + b` 로 바꿨습니다."

게이트 로그가 결정적 증거다.

```
[2026-08-17T03:52:19+00:00] pre_verify fired cwd=/home/ccc/hermes-lab/gate
[2026-08-17T03:52:19+00:00] unittest rc=1      ← 실패 → "끝내지 마"
[2026-08-17T03:53:13+00:00] pre_verify fired cwd=/home/ccc/hermes-lab/gate
[2026-08-17T03:53:13+00:00] unittest rc=0      ← 통과 → 종료 허용
```

**게이트가 두 번 발동했다.** 첫 번째는 막았고, 54초 뒤 두 번째는 통과시켰다. 그 사이에 에이전트는 사용자가 "건드리지 말라"고 한 함수를 고쳤다.

### 반드시 생각하고 넘어갈 것

방금 우리는 사용자의 명시적 지시("다른 함수는 절대 건드리지 마")를 하니스가 덮어쓰는 걸 봤다. 이건 **양날의 칼**이다.

- 좋은 쪽: 사용자가 실수로 잘못 지시해도 시스템이 무너지지 않는다. 테스트는 언제나 통과한 상태로 유지된다.
- 위험한 쪽: 게이트를 잘못 짜면 **아무도 끊을 수 없는 루프**가 된다. 그래서 Hermes에는 `agent.max_verify_nudges` 상한이 있다. 모듈 3의 "루프에는 반드시 종료 조건이 있어야 한다"가 이 이야기다.

게이트를 하나 만들 때마다 스스로에게 묻는다. **"이 게이트가 영원히 실패하면 어떻게 되지?"**

### 막히면

- **게이트가 발동은 하는데 아무 효과가 없다** — `pre_verify` 는 에이전트가 **코드를 고친 뒤 끝내려 할 때** 발동한다. 파일을 안 고친 대화에서는 안 뜬다.
- **`/tmp/gate.log` 가 안 생긴다** — 훅 승인이 안 된 것이다. `hermes hooks doctor` 로 `✓ allowlisted` 를 확인한다.
- **pytest가 없다** — 이 실습은 일부러 `python3 -m unittest` 를 쓴다. 추가 설치가 필요 없다.

### 이어지는 곳

L3-2에서 이 게이트 발상을 **시간 축**으로 옮긴다. "끝내도 되나?" 대신 "지금 깨어날 필요가 있나?"를 묻게 된다.

---

## L2-5. 공급망을 감사한다

> 대응 | 모듈 2 · 10~11절 (실패 유형, 여덟 칸 점검표)
> 소요 | 15분
> 선행 | L0-2
> 확인 | 모델 호출 없음 · 실제 취약점 12건 검출

### 무엇을

에이전트가 쓰는 파이썬 패키지·플러그인·MCP 서버에 알려진 취약점이 있는지 OSV.dev 데이터베이스로 훑는다.

### 왜

모듈 2의 실패 유형 분류에서 가장 과소평가되는 게 **"에이전트 자체가 침해당하는 경우"** 다. 프롬프트를 아무리 잘 써도, 에이전트가 의존하는 라이브러리에 구멍이 있으면 소용없다. 특히 MCP 서버는 남이 만든 코드를 내 기계에서 실행하는 것이므로 위험이 크다.

### 해보기

```bash
hermes security
hermes doctor | head -20
```

### 기대 결과

실제 발견 결과가 나온다. 실습 환경에서는 12건이 나왔다.

```
Found 12 known vulnerability finding(s) across 102 component(s):

[venv]
  HIGH      aiohttp==3.14.1  GHSA-cq5v-8q36-5273
           AIOHTTP: Out-of-bounds heap read in C HTTP response parser error path
           fixed in: 3.14.3
  HIGH      cryptography==48.0.1  GHSA-g6cj-pr64-35w5
           PKCS#7 EnvelopedData decryption exposes a Bleichenbacher oracle
           fixed in: 50.0.0
```

`hermes doctor` 는 이것과 별개로 **의심스러운 MCP stdio 명령**도 검사한다.

```
◆ MCP Server Security
  ✓ No suspicious MCP stdio commands
```

L1-3에서 우리가 등록한 커넥터가 여기 걸리지 않았다. 로컬 파이썬 스크립트이고 네트워크를 안 쓰기 때문이다.

### 생각해 볼 것

만약 L1-3에서 `npx -y 남이만든패키지` 를 커넥터로 등록했다면 어땠을까? 그 패키지는 매번 최신 버전을 내려받아 실행된다. 오늘 안전했다고 내일도 안전한 게 아니다. **버전을 고정하고, 주기적으로 감사한다.** 이게 모듈 2 여덟 칸 점검표의 마지막 칸이다.

### 이어지는 곳

여기까지가 "사람이 옆에 있을 때"의 하니스다. 실습 3부터는 **사람이 자는 동안** 도는 에이전트를 다룬다. 그때 하니스는 선택이 아니라 필수가 된다.

---

## 실습 3. 루프 엔지니어링 — 모듈 3을 손으로 확인한다

## L3-1. 조용한 하트비트를 만든다 (모델을 부르지 않는 루프)

> 대응 | 모듈 3 · 4~5절 (네 가지 하트비트, 케이던스별 비용)
> 소요 | 25분
> 선행 | L0-2
> 확인 | 모델 호출 0회 · 실행 1회 0.5초 미만

### 무엇을

디스크 사용률을 주기적으로 보다가 **임계값을 넘을 때만** 말하는 감시 잡을 만든다. 평소에는 아무 말도 안 한다.

### 왜

"에이전트를 자동으로 돌린다"는 말을 들으면 대개 **모델을 주기적으로 부르는 것**을 떠올린다. 모듈 3은 그 반대를 가르친다. **좋은 루프는 대부분의 시간에 모델을 부르지 않는다.**

이 실습의 잡은 LLM을 아예 쓰지 않는다(`--no-agent`). 셸 스크립트가 조건을 보고, 조건이 성립할 때만 말한다. 비용이 0이고 지연이 0이다. 모듈 3의 케이던스 비용표에서 맨 아래 칸에 해당한다.

**수업 운영상 이 실습이 좋은 이유:** GPU를 전혀 쓰지 않으므로 전원이 동시에 돌려도 된다.

### 해보기

```bash
mkdir -p $HERMES_HOME/scripts ~/hermes-lab/loop

cat > $HERMES_HOME/scripts/disk-watch.sh <<EOF
#!/usr/bin/env bash
# 하트비트: 조건이 성립할 때만 말한다. 평소에는 침묵(= 비용 0).
LOG=$HOME/hermes-lab/loop/heartbeat.log
LIMIT=\${DISK_LIMIT:-90}
use=\$(df -P / | awk 'NR==2{gsub("%","",\$5); print \$5}')
if [ "\$use" -ge "\$LIMIT" ]; then
  msg="⚠ 루트 파티션 사용률 \${use}% (임계 \${LIMIT}%) — 정리가 필요합니다."
  echo "\$msg"
  echo "[\$(date -Is)] \$msg" >> "\$LOG"
fi
EOF
chmod +x $HERMES_HOME/scripts/disk-watch.sh

hermes cron create "every 1h" --name disk-watch \
  --script disk-watch.sh --no-agent --deliver local

hermes cron list
```

잡 ID를 확인하고 두 번 돌린다. 한 번은 조용해야 하고, 임계값을 0으로 낮춘 뒤에는 말해야 한다.

```bash
# 잡 ID는 이름으로 찾는다. 손으로 옮겨 적지 않는다.
JOB=$(hermes cron list | awk '/^  [0-9a-f]{12} \[/{id=$1} /Name:/ && /disk-watch/{print id; exit}')
echo "JOB=$JOB"

echo "--- 1회차: 조용해야 함 ---"
hermes cron run $JOB
ls ~/hermes-lab/loop/heartbeat.log

echo "--- 임계값을 0으로 낮추고 2회차: 발화해야 함 ---"
sed -i 's/DISK_LIMIT:-90/DISK_LIMIT:-0/' $HERMES_HOME/scripts/disk-watch.sh
hermes cron run $JOB
cat ~/hermes-lab/loop/heartbeat.log

hermes cron runs $JOB
sed -i 's/DISK_LIMIT:-0/DISK_LIMIT:-90/' $HERMES_HOME/scripts/disk-watch.sh
```

### 기대 결과

1회차 — 파일이 아예 안 생긴다.

```
ls: cannot access '.../heartbeat.log': No such file or directory
```

2회차 — 한 줄이 생긴다.

```
[2026-08-17T03:28:21+00:00] ⚠ 루트 파티션 사용률 6% (임계 0%) — 정리가 필요합니다.
```

그런데 **실행 이력에는 두 번 다 남아 있다.**

```
1ee5f13cef93...  completed  job=40a643fa5f73  2026-08-17T03:28:21
bdfd3e46b9ae...  completed  job=40a643fa5f73  2026-08-17T03:28:20
```

이 대비가 핵심이다. **루프는 매번 돌았지만, 말한 건 한 번뿐이다.** 모듈 3에서 "조용한 성공은 알릴 필요가 없다"고 한 게 이 모양이다. 만약 매번 "정상입니다"를 보냈다면, 진짜 경고가 왔을 때 아무도 안 읽었을 것이다.

### 게이트웨이 경고에 대하여

`⚠ Gateway is not running — jobs won't fire automatically` 가 뜬다. 실제 자동 실행에는 백그라운드 게이트웨이가 필요하다는 뜻이다.

**수업에서는 게이트웨이를 켜지 않는다.** 대신 `hermes cron run <id>` 로 손으로 한 틱을 돌린다. 이유는 두 가지다. ① 30명의 백그라운드 프로세스가 GPU 서버를 동시에 두드리는 사고를 막는다. ② 언제 도는지 내가 정하므로 관찰이 명확하다. `hermes cron tick` 은 "지금 시각 기준으로 만기된 잡만 한 번 돌리기"다.

### 막히면

- **`Removed job` 이 안 되고 잡이 여러 개 쌓였다** — `hermes cron list` 로 ID를 보고 `hermes cron rm <id>` 로 정리한다.
- **`--deliver local` 인데 화면에 아무것도 안 나온다** — 정상이다. `local` 은 외부 전송을 하지 않는다는 뜻이고, 결과는 실행 이력과 위 스크립트가 남긴 파일에만 남는다. 텔레그램 등을 붙이면 그쪽으로 간다.

### 이어지는 곳

L3-2에서 **조건이 바뀔 때만 모델을 부르는** 한 단계 위의 루프를 만든다.

---

## L3-2. 변화가 있을 때만 모델을 깨우는 게이트를 만든다

> 대응 | 모듈 3 · 5~6절 (조건부 루프, 루틴 실행 해부)
> 소요 | 40분
> 선행 | L3-1
> 확인 | 최초 68초 → 무변화 0.49초 → 변화 56초 (실측)

### 무엇을

제출함 폴더를 감시하다가, **파일 목록이 바뀌었을 때만** 에이전트를 깨워서 접수 기록을 남기게 한다.

### 왜

L3-1의 루프는 모델을 아예 안 썼다. 하지만 진짜 일에는 판단이 필요하다. 그렇다고 5분마다 모델을 부르면 대부분이 "변한 게 없네"라는 답에 돈을 쓰는 꼴이 된다.

`--monitor-script` 는 이 사이의 답이다. **싼 스크립트가 먼저 보고, 비싼 모델은 뭔가 달라졌을 때만 깨어난다.** 모듈 3의 "조건부 루프"이고, L2-4의 게이트를 시간 축으로 옮긴 것이다.

이번 실습에서는 그 절약이 **숫자로** 보인다.

### 해보기

```bash
mkdir -p ~/hermes-lab/loop/inbox
echo "1주차 과제입니다." > ~/hermes-lab/loop/inbox/20250001_홍길동.md

cat > $HERMES_HOME/scripts/inbox-watch.sh <<EOF
#!/usr/bin/env bash
# 감시 소스: 출력이 '안정적'이어야 한다(정렬, 시각 없음).
cd $HOME/hermes-lab/loop/inbox 2>/dev/null || exit 1
ls -1 | sort
EOF
chmod +x $HERMES_HOME/scripts/inbox-watch.sh

bash $HERMES_HOME/scripts/inbox-watch.sh   # 출력 확인
```

잡을 만든다. **프롬프트는 반드시 일정(schedule) 바로 뒤에 온다.** 옵션 뒤에 두면 인자 파싱이 실패한다.

```bash
hermes cron create "every 1h" \
"감시 결과(MONITOR CHANGE DETECTED 블록)에 새로 나타난 파일 이름이 있으면, 작업 폴더의 report.md 끝에 '- <파일이름>: 접수' 형식으로 그 파일마다 한 줄씩 추가하라. report.md가 없으면 만들어라. 파일 내용은 읽지 마라. 다른 작업은 하지 마라." \
--name inbox-watch --monitor-script inbox-watch.sh \
--workdir ~/hermes-lab/loop --deliver local
```

세 번 돌린다. **매번 시간을 잰다.**

```bash
JOB=$(hermes cron list | awk '/^  [0-9a-f]{12} \[/{id=$1} /Name:/ && /inbox-watch/{print id; exit}')
echo "JOB=$JOB"

echo "===== 1회차: 최초 관측 (기준선) ====="
time hermes cron run $JOB --accept-hooks

echo "===== 2회차: 아무것도 안 바꾸고 ====="
time hermes cron run $JOB --accept-hooks

echo "===== 3회차: 파일 하나 추가 후 ====="
echo "새 제출물" > ~/hermes-lab/loop/inbox/20250002_김철수.md
time hermes cron run $JOB --accept-hooks

cat ~/hermes-lab/loop/report.md
```

### 기대 결과

| 회차 | 상황 | 소요 | 모델 호출 |
|---|---|---|---|
| 1회차 | 최초 관측(기준선) | **68초** | 있음 |
| 2회차 | 변화 없음 | **0.49초** | **없음** |
| 3회차 | 파일 1개 추가 | **56초** | 있음 |

:::diagram
id: lab-gate-timing
원본: (신규 작도)
제목: 감시 게이트가 있을 때와 없을 때 — 실측 비교
내용: 68초 / 0.49초 / 56초 막대 비교와 절약의 정체
:::

**139배 차이다.** 2회차에 무슨 일이 있었는지는 로그가 말해 준다.

```
INFO cron.scheduler: Job '947764ec7720': monitor output unchanged — suppressing agent run
```

`report.md` 에는 새로 들어온 파일 **하나만** 기록된다.

```
- 20250002_김철수.md: 접수
```

기존 파일은 안 적혔다. 게이트가 넘겨준 게 전체 목록이 아니라 **차이(diff)** 였기 때문이다.

세션 수로도 확인된다.

```bash
hermes sessions list | grep -c cron_
```

세 번 돌렸는데 세션은 **2개**다. 2회차는 세션조차 안 만들었다.

### 왜 감시 스크립트 출력이 "안정적"이어야 하는가

Hermes는 감시 스크립트 출력을 **바이트 단위로 그대로** 비교한다. 공백도, 순서도 정규화하지 않는다. 그래서 스크립트에 `date` 같은 걸 넣으면 매 틱이 "변화"로 잡혀서 게이트가 무의미해진다. `ls -1 | sort` 처럼 **같은 상태면 같은 바이트**가 나오게 짜야 한다.

이건 모듈 3의 일반 원칙이기도 하다. **판정 기준이 흔들리면 게이트는 소음 발생기가 된다.**

### 막히면

- **`unrecognized arguments: 감시 결과에...`** — 프롬프트를 옵션 뒤에 뒀다. 일정 문자열 바로 다음에 놓는다.
- **3회차인데도 억제된다** — 추가한 파일이 이미 있던 파일이다. 감시 스크립트는 파일 *목록*을 보므로 같은 이름을 덮어써도 출력이 바뀌지 않는다. 진짜 새 이름으로 만든다. (검증 중 실제로 이 함정에 빠졌다.)
- **매 틱이 다 "변화"로 잡힌다** — 감시 스크립트에 시각·난수·정렬 안 된 목록이 들어 있다. `bash 스크립트 | md5sum` 을 두 번 실행해 같은 해시가 나오는지 확인한다.
- **감시 스크립트가 실패한다** — 실패는 **변화로 치지 않는다.** 에러로 기록되고 저장된 해시는 그대로 둔다. 스크립트가 복구되면 다시 조용해진다. 좋은 설계다.

### 이어지는 곳

지금 루프는 **바깥 세상의 변화**를 기억한다. L3-3에서는 **자기 자신의 진행 상황**을 기억하게 만든다.

---

## L3-3. 깨어날 때마다 이어서 하는 루프를 만든다 (기억을 가진 루프)

> 대응 | 모듈 3 · 8~10절 (기억을 가진 아침 루프, 척추, 두 루틴 게이트)
> 소요 | 45분
> 선행 | L3-2
> 확인 | 4회 실행 · 3건 처리 후 자동 정지 (58s / 40s / 56s / 30s)

### 무엇을

할 일 3개짜리 목록을 놓고, 잡이 깨어날 때마다 **딱 하나씩** 처리하게 한다. 어디까지 했는지는 잡의 영구 메모장(notepad)에 남긴다.

### 왜

모듈 3에서 "루프의 척추는 기억"이라고 했다. 상태가 없는 루프는 매번 처음부터 시작하거나, 이미 한 일을 또 한다.

Hermes의 cron notepad는 잡마다 붙는 아주 작은 키-값 저장소인데, **깨어날 때마다 프롬프트 앞에 자동으로 붙는다.** 즉 에이전트는 아무것도 안 해도 "지난번에 내가 어디까지 했더라"를 알고 시작한다.

실무에서 이 패턴이 쓰이는 곳: 대용량 데이터를 하루 한 조각씩 처리하기, 메일함을 마지막 읽은 지점부터 이어서 훑기, 긴 마이그레이션을 여러 밤에 나눠 돌리기.

### 해보기

```bash
mkdir -p ~/hermes-lab/notepad && cd ~/hermes-lab/notepad

cat > todo.md <<'EOF'
1. 강의계획서 초안 작성
2. 실습 서버 계정 발급
3. 1주차 퀴즈 문항 검토
EOF

hermes cron create "every 1h" \
"작업 폴더의 todo.md 에는 번호가 붙은 항목이 있다. notepad 의 cursor 값이 가리키는 번호의 항목 하나만 처리한다. 처리 = done.md 파일 끝에 '- <번호>. <항목 제목>: 완료' 형식으로 한 줄 추가. 그 다음 반드시 터미널로 'hermes cron notepad <이 잡의 id> set cursor <다음 번호>' 를 실행해 cursor 를 1 증가시켜라. cursor 가 항목 개수보다 크면 아무것도 하지 말고 끝내라. 한 번에 항목 하나만 처리한다." \
--name todo-runner --workdir ~/hermes-lab/notepad --deliver local
```

**메모장에 시작값을 넣는다. 이 단계를 빼먹으면 안 된다.**

```bash
JOB2=$(hermes cron list | awk '/^  [0-9a-f]{12} \[/{id=$1} /Name:/ && /todo-runner/{print id; exit}')
echo "JOB2=$JOB2"
hermes cron notepad $JOB2 set cursor 1
hermes cron notepad $JOB2 list
```

네 번 돌린다.

```bash
JOB2=$(hermes cron list | awk '/^  [0-9a-f]{12} \[/{id=$1} /Name:/ && /todo-runner/{print id; exit}')
for i in 1 2 3 4; do
  echo "===== ${i}회차 ====="
  hermes cron run $JOB2 --accept-hooks
  cat done.md 2>/dev/null
  hermes cron notepad $JOB2 list
done
```

### 기대 결과

| 회차 | done.md | cursor | 소요 |
|---|---|---|---|
| 1 | 1건 | 1 → **2** | 58초 |
| 2 | 2건 | 2 → **3** | 40초 |
| 3 | 3건 | 3 → **4** | 56초 |
| 4 | **3건 그대로** | **4 유지** | 30초 |

:::diagram
id: lab-notepad-loop
원본: (신규 작도)
제목: 메모장이 있는 루프는 이어서 하고, 끝나면 스스로 멈춘다
내용: 4회 실행의 커서 이동과 종료 조건
:::

최종 `done.md`:

```
- 1. 강의계획서 초안 작성: 완료
- 2. 실습 서버 계정 발급: 완료
- 3. 1주차 퀴즈 문항 검토: 완료
```

4회차를 눈여겨본다. 깨어나긴 했지만 **아무것도 하지 않고 끝났다.** cursor가 4라서 처리할 항목이 없다는 걸 스스로 알았기 때문이다. 이게 모듈 3에서 말한 **종료 조건**이다. 종료 조건이 없는 루프는 같은 일을 무한히 반복하거나, 없는 항목을 지어내기 시작한다.

에이전트가 커서를 어떻게 옮겼는지도 확인할 수 있다. 프롬프트에 이런 안내가 자동으로 붙어 있었다.

```
## Job notepad (persistent across runs)
This durable scratchpad survives between scheduled runs of this job.
Update it via the CLI, e.g.:
`hermes cron notepad 0705d04ed224 set <key> <value>`

- cursor: 1
```

즉 에이전트는 **터미널 도구로 자기 자신의 메모장을 고쳤다.** 별도 도구가 없다.

### 막히면

- **메모장 안내가 프롬프트에 안 붙는다** — 메모장이 비어 있으면 아예 안 붙는다(빈 잡의 프롬프트를 바이트 단위로 동일하게 유지하려는 설계다). 반드시 `set cursor 1` 로 시작값을 먼저 넣는다.
- **cursor가 안 올라간다** — 프롬프트에서 커서 증가를 "반드시" 라고 못 박아야 한다. 작은 모델은 부수 작업을 잘 빠뜨린다. 더 확실하게 하려면 `done.md` 줄 수를 세서 cursor를 계산하도록 바꾼다 — **상태를 파생시키는 편이 상태를 갱신하는 것보다 안전하다.**
- **메모장 용량** — 키 하나 16KB, 잡 하나 64KB 상한이다. 매번 프롬프트에 들어가므로 커지면 비용이 된다. 커서·워터마크 같은 **작은 것**만 넣는다.

### 이어지는 곳

L3-4에서 지금까지 쓴 비용을 실제 숫자로 확인한다.

---

## L3-4. 지금까지 쓴 비용을 숫자로 본다

> 대응 | 모듈 3 · 11절 (케이던스별 비용), 모듈 2 · 12절 (관측)
> 소요 | 10분
> 선행 | L3-3
> 확인 | 모델 호출 없음

### 무엇을

이 실습편을 진행하는 동안 실제로 쓴 토큰과 호출 횟수를 본다.

### 왜

모듈 3의 비용 논의는 추상적으로 읽으면 와닿지 않는다. 방금 내가 두 시간 동안 만든 루프들이 정확히 얼마를 썼는지 보면 감이 잡힌다. 그리고 L3-2에서 게이트가 아꼈던 것이 여기 반영돼 있다.

### 해보기

```bash
hermes insights --days 1
```

### 기대 결과

실습 환경에서 약 40분간 나온 값이다.

```
  📋 Overview
  Sessions:          15            Messages:        94
  Tool calls:        37            User messages:   15
  Input tokens:      692,057       Output tokens:   14,633
  Total tokens:      706,690

  📱 Platforms
  cli                   9         42        380,759
  cron                  6         52        325,931

  🔧 Top Tools
  terminal                           11    29.7%
  search_files                        7    18.9%
  read_file                           6    16.2%
  write_file                          4    10.8%
  memory                              4    10.8%
```

### 여기서 읽어야 할 것

**입력 토큰이 출력 토큰의 47배다.** 이게 에이전트 비용의 진실이다. 모델이 뭘 길게 쓰는 게 비싼 게 아니라, **매 턴마다 시스템 프롬프트·스킬 목록·도구 정의·대화 이력을 다시 보내는 것**이 비싸다.

여기서 두 가지가 따라온다.

1. **L3-2의 게이트가 아낀 것은 "한 번의 응답"이 아니라 "한 번의 전체 문맥 전송"이다.** 억제된 틱 하나가 약 14,000 입력 토큰을 아꼈다.
2. **스킬을 무한정 깔면 안 된다.** 스킬 목록은 매 턴 프롬프트에 들어간다. 그래서 모듈 1이 프로그레시브 디스클로저 — 목록에는 이름과 설명만, 본문은 필요할 때 — 를 강조한 것이다.

`cron` 이 전체 토큰의 46%를 썼다는 점도 본다. 사람이 안 보는 동안 도는 루프가 비용의 절반이다. **관측하지 않으면 모른다.**

### 이어지는 곳

실습 4에서 이 세션 기록들이 **왜 지식이 아닌지**, 그리고 지식으로 만들려면 무엇이 더 필요한지 본다.

---

## 실습 4. 그래프 엔지니어링 — 모듈 4를 손으로 확인한다

## L4-1. 세션이 끝나도 남는 기억을 만든다

> 대응 | 모듈 4 · 2~3절 (대화록 대 그래프, 두 개의 그래프)
> 소요 | 25분
> 선행 | L0-2
> 확인 | 저장 66초 · 회상 8.8초 (도구 호출 없음)

### 무엇을

한 세션에서 사실을 알려 주고, **완전히 새 세션**에서 그것을 기억하는지 확인한다. 그리고 그 기억이 어느 파일에 어떻게 들어갔는지 연다.

### 왜

모듈 4는 "에이전트는 잊지만 그래프는 잊지 않는다"로 시작했다. 이 실습은 그 문장의 가장 작은 실물이다.

주목할 것은 **분류**다. Hermes는 알려 준 사실을 `MEMORY.md`(세상에 대한 사실)와 `USER.md`(나에 대한 사실)로 나눠 넣는다. 모듈 4에서 "무엇을 어디에 저장할지가 스키마 설계의 시작"이라고 한 것이 이 두 파일로 구현돼 있다.

### 해보기

```bash
cd ~/hermes-lab

echo "===== 세션 A: 알려 주기 ====="
hermes chat -q "기억해 둬: 우리 실습 서버는 211.170.162.109:11434 이고, 기본 모델은 qwen3.8:27b 야. 그리고 나는 강의를 화요일 3교시에 한다." -Q

echo "----- 저장된 파일 -----"
cat $HERMES_HOME/memories/MEMORY.md
cat $HERMES_HOME/memories/USER.md

echo "===== 세션 B: 완전히 새 세션에서 물어보기 ====="
hermes chat -q "내 실습 서버 주소와 기본 모델이 뭐였지? 그리고 내 강의는 언제야? 한 줄로만 답해." -Q
```

### 기대 결과

반드시 확인할 것은 **파일이 생겼는가**와 **새 세션이 그 내용을 아는가** 둘이다. 어느 사실이 `MEMORY.md` 로 가고 어느 것이 `USER.md` 로 갈지는 모델의 판단이라 조금씩 다를 수 있다. 검증 때는 이렇게 갈렸다.

```
--- MEMORY.md ---
실습(practice) LLM 서버: 211.170.162.109:11434, 기본 모델 qwen3.8:27b (Ollama).

--- USER.md ---
화요일 3교시에 강의를 한다.
```

**새 세션에서 그대로 나온다.**

```
실습 서버 211.170.162.109:11434 (기본 모델 qwen3.8:27b, Ollama), 강의는 화요일 3교시입니다.
```

여기서 **시간**을 본다. 저장은 66초, 회상은 **8.8초**다. 회상이 7배 이상 빠른 이유는, 에이전트가 파일을 찾아 읽은 게 아니라 **기억이 이미 프롬프트 안에 들어와 있었기** 때문이다. 도구 호출이 0회다.

이게 모듈 4에서 말한 "검색이 아니라 주입"의 차이다. 검색은 찾아야 하고, 주입은 이미 거기 있다. 대신 주입은 **매 턴 비용을 낸다**(L3-4에서 본 입력 토큰). 그래서 Hermes는 `memory_char_limit: 2200`, `user_char_limit: 1375` 같은 상한을 둔다. **기억은 무한히 쌓을 수 없다. 무엇을 버릴지가 설계다.**

### 대화록과 기억을 비교해 본다

같은 대화가 두 가지 형태로 남아 있다. 하나는 통째로 남은 **대화록**이고, 하나는 요약되어 뽑힌 **기억**이다.

```bash
hermes sessions list | head -5

# 가장 최근 세션(= 방금 회상한 그 세션)의 ID를 뽑는다
SID=$(hermes sessions list | awk 'NF && $NF ~ /[0-9]{8}_/ {print $NF; exit}')
echo "SID=$SID"

hermes sessions export --format md --session-id "$SID" ~/hermes-lab/export
wc -l ~/hermes-lab/export/*.md
wc -c $HERMES_HOME/memories/MEMORY.md
```

대화록은 수십~수백 줄이고 기억은 한 줄이다. 모듈 4의 첫 그림 **"대화록 대 그래프"** 가 이 두 숫자의 대비다. 대화록은 **무슨 일이 있었는지**를 남기고, 기억은 **무엇이 참인지**를 남긴다. 둘은 다른 물건이고, 둘 다 필요하다.

### 막히면

- **파일이 안 생긴다** — 이 모델은 "기억해 둬"라는 명시적 요청에는 잘 반응하지만 항상 그런 건 아니다. 문장을 "이건 꼭 기억해 둬:"로 시작하면 확률이 높아진다.
- **초기화** — `hermes memory reset` 으로 `MEMORY.md` / `USER.md` 를 비운다.

### 이어지는 곳

L4-2에서 이 기억들이 **그래프의 노드**로 나타나는 것을 본다.

---

## L4-2. 에이전트의 기억 그래프를 열어 본다

> 대응 | 모듈 4 · 4~6절 (Ratchet에서 DAG로, 추출 파이프라인, 서브그래프 검색)
> 소요 | 25분
> 선행 | L1-2, L4-1
> 확인 | 모델 호출 없음 · 노드 4개 · 간선 1개 · 고립도 100% → 0%

### 무엇을

Hermes가 스스로 유지하는 기억 그래프를 JSON으로 꺼내 보고, L1-2에서 적어 둔 `related_skills` 한 줄이 실제 **간선**이 되는 것을 확인한다.

### 왜

모듈 4의 가장 중요한 주장은 "**항목의 목록은 그래프가 아니다. 항목 사이의 관계가 있어야 그래프다**"였다. 이 실습은 그 문장을 숫자로 확인한다. 관계를 적기 전에는 고립도가 100%이고, 적고 나면 0%가 된다.

또 하나 배울 것: **이 그래프에는 "설치된 것"이 아니라 "실제로 쓰인 것"만 들어간다.** 스킬을 만들어 둬도 한 번도 발동 안 하면 노드가 아니다. 모듈 4에서 말한 "그래프는 사용의 기록이지 재고 목록이 아니다"가 이렇게 구현돼 있다.

### 해보기

```bash
hermes journey list
hermes journey --json | python3 -m json.tool | head -50
```

통계만 뽑아 본다.

```bash
hermes journey --json | python3 -c "
import json,sys
d=json.load(sys.stdin)
print('노드:', [(n['id'], n['kind'], n.get('useCount')) for n in d['nodes']])
print('간선:', json.dumps(d['edges'], ensure_ascii=False))
s=d['stats']
print('관계 간선:', s['related_edges'], '| 연결된 노드:', s['linked_nodes'], '| 고립 비율:', s['isolated_pct'], '%')
"
```

### 기대 결과

```
노드: [('weekly-report', 'skill', 1), ('meeting-note', 'skill', 1),
       ('memory:memory:0', 'memory', 0), ('memory:profile:1', 'memory', 0)]
간선: [{"source": "meeting-note", "target": "weekly-report"}]
관계 간선: 1 | 연결된 노드: 2 | 고립 비율: 0.0 %
```

세 가지를 확인한다.

1. **`useCount`** — 각 스킬이 **실제로 발동한 횟수**다. 앞에서 몇 번 돌렸느냐에 따라 1이 될 수도 2가 될 수도 있으니, 숫자 자체보다 **자기가 돌린 횟수와 맞는지**를 본다. 그래프가 사용을 세고 있다는 뜻이다.
2. **간선** — `meeting-note → weekly-report`. 우리가 SKILL.md에 적은 `related_skills: [weekly-report]` 한 줄이 여기 왔다.
3. **고립 비율 0%** — L1-2를 하기 전에는 이 값이 **100%** 였다. 노드는 있었지만 아무것도 연결돼 있지 않았다.

메모리 노드 두 개는 아직 `useCount: 0` 이고 간선이 없다. **이게 이 실습의 진짜 관찰 대상이다.** 모듈 4에서 말한 그대로다 — 사실을 모아 놓는 것과 사실을 연결하는 것은 다른 작업이고, 대부분의 시스템은 앞의 것만 하고 그친다.

### 생각해 볼 것

`memory:memory:0`("실습 서버는 211.170.162.109")과 `memory:profile:1`("화요일 3교시 강의")을 잇는 간선이 있다면 무슨 의미일까? 예를 들어 `강의 → 사용 → 실습 서버` 같은 관계다. 지금 Hermes는 이걸 자동으로 만들지 않는다.

모듈 4의 추출 파이프라인(스키마 정의 → 개체 추출 → 해소 → 관계 부여)이 필요한 지점이 정확히 여기다. **관계는 공짜로 생기지 않는다. 누군가 스키마를 정하고 뽑아내야 한다.**

### 확장 과제

`weekly-report/SKILL.md` 에도 `related_skills: [meeting-note]` 를 넣고 두 스킬을 한 번씩 더 발동시켜 본다. 간선이 양방향 두 개가 되는가, 아니면 하나로 합쳐지는가? 그 답이 이 그래프가 **유향인지 무향인지** 알려 준다.

### 이어지는 곳

L4-3에서 그래프의 마지막 조각 — **출처(provenance)** — 를 붙인다.

---

## L4-3. 근거 없는 주장을 잡아내는 검증기를 만든다

> 대응 | 모듈 4 · 7~9절 (근거 기반 검증자, 루프에서 그래프로, 수준 고르기)
> 소요 | 50분
> 선행 | L2-4, L4-2
> 확인 | 3건 전부 PASS · 조작 시 정확히 1건 FAIL 검출 · 생성 약 3분 22초

### 무엇을

원문에서 요약을 만들되, **모든 주장마다 원문의 한 문장을 근거로 달게** 한다. 그리고 그 근거가 진짜로 원문에 있는지 기계로 검사한다.

:::diagram
id: lab-grounded
원본: (신규 작도)
제목: 주장마다 근거를 달고, 근거를 기계가 대조한다
내용: source.md → claims.json → 검증기 → PASS/FAIL
:::

### 왜

이게 이 실습편의 마지막이자, 모듈 4가 도달하려던 곳이다.

모듈 4에서 그래프를 만드는 이유가 "여러 에이전트가 공유하는, **출처가 딸린** 기억"이라고 했다. 출처가 없는 사실은 그래프에 넣으면 안 된다. 왜냐하면 나중에 그것이 틀렸을 때 **어디서 왔는지 추적할 수 없기 때문이다.**

이 실습이 만드는 `claims.json` 은 그래프의 가장 단순한 형태다 — 주장 하나, 근거 하나. 그리고 `check_claims.py` 는 모듈 4의 **근거 기반 검증자(grounded checker)** 의 최소 구현이다. 이 검증자에는 LLM이 없다. **문자열이 원문에 있는지만 본다.** 그래서 절대 거짓말하지 않는다.

L2-4에서 만든 게이트와 짝을 이룬다. 거기서는 테스트가 코드를 판정했고, 여기서는 문자열 대조가 주장을 판정한다. **판정자는 판정 대상보다 단순해야 한다** — 그게 두 실습의 공통 교훈이다.

### 해보기

원문과 검증기를 만든다.

```bash
mkdir -p ~/hermes-lab/graph && cd ~/hermes-lab/graph

cat > source.md <<'EOF'
# 학사 운영 규정 (발췌)

제3조 (출석) 총 수업시간의 4분의 1 이상 결석한 학생은 해당 교과목의 성적을 F로 처리한다.
제7조 (재수강) 재수강한 교과목의 성적은 최대 B+ 까지만 부여할 수 있다.
제11조 (과제 제출) 과제는 마감 시각까지 학습관리시스템에 제출하며, 지각 제출은 하루당 10%를 감점한다.
제15조 (실습실 사용) 실습실은 평일 09시부터 21시까지 개방하며, 주말 사용은 사전 신청을 받는다.
EOF

cat > check_claims.py <<'EOF'
"""근거 검증기: claims.json 의 모든 quote 가 source.md 에 문자 그대로 있는지 확인한다."""
import json
import sys
from pathlib import Path

src = Path("source.md").read_text(encoding="utf-8")
claims = json.loads(Path("claims.json").read_text(encoding="utf-8"))
if isinstance(claims, dict):
    claims = claims.get("claims", [])

fail = 0
for i, c in enumerate(claims, 1):
    q = (c.get("quote") or "").strip()
    ok = bool(q) and q in src
    print(f"{'PASS' if ok else 'FAIL'}  [{i}] {c.get('claim','')[:50]}")
    if not ok:
        print(f"      근거 없음 → {q[:80]!r}")
        fail += 1

print(f"\n총 {len(claims)}건 중 {fail}건 근거 없음")
sys.exit(1 if fail else 0)
EOF
```

에이전트에게 근거 딸린 요약을 시킨다.

```bash
hermes chat -q "source.md 를 읽고 '학생이 학점을 잃을 수 있는 경우'를 정리해라. 결과는 두 파일로 저장한다. (1) answer.md — 한국어 요약. (2) claims.json — [{\"claim\":\"주장 한 문장\",\"quote\":\"source.md 에 문자 그대로 들어있는 근거 문장\"}] 형식의 JSON 배열. quote 는 반드시 source.md 에서 그대로 복사한 문자열이어야 한다. 지어내지 마라. check_claims.py 는 실행하지 마." --accept-hooks -Q

cat claims.json
python3 check_claims.py; echo "exit=$?"
```

### 기대 결과

`claims.json` 이 주장과 근거 쌍으로 나온다.

```json
[
  {
    "claim": "총 수업시간의 4분의 1 이상 결석하면 해당 교과목 성적이 F로 처리되어 학점을 잃는다.",
    "quote": "제3조 (출석) 총 수업시간의 4분의 1 이상 결석한 학생은 해당 교과목의 성적을 F로 처리한다."
  },
  ...
]
```

검증기가 전부 통과시킨다. **주장의 개수와 문장은 매번 다르다.** 반드시 확인할 것은 `python3 check_claims.py` 가 **`exit=0` 으로 끝나는가**, 즉 모든 quote 가 원문에 실제로 있는가다.

```
PASS  [1] 총 수업시간의 4분의 1 이상 결석하면 해당 교과목 성적이 F로 처리되어 학점을 잃는다.
PASS  [2] 재수강한 교과목은 성적이 최대 B+까지만 부여되어 상한이 걸린다.
PASS  [3] 과제를 지각 제출하면 하루당 10%가 감점되어 성적이 낮아진다.

총 3건 중 0건 근거 없음
exit=0
```

`제15조(실습실)` 가 빠진 게 옳다. 학점과 무관하기 때문이다. **주장을 안 한 것도 정확도다.**

### 이제 검증기를 시험한다 (이게 진짜 실습이다)

검증기가 통과시켰다고 검증기가 일하는 건 아니다. **가짜를 넣어 보고 잡히는지 확인해야 검증기를 믿을 수 있다.**

```bash
cp claims.json claims.json.orig
python3 - <<'EOF'
import json
c = json.load(open("claims.json", encoding="utf-8"))
c.append({"claim": "실습실은 24시간 개방한다.",
          "quote": "제15조 (실습실 사용) 실습실은 24시간 개방한다."})
json.dump(c, open("claims.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
EOF

python3 check_claims.py; echo "exit=$?"
cp claims.json.orig claims.json
```

```
PASS  [1] ...
PASS  [2] ...
PASS  [3] ...
FAIL  [4] 실습실은 24시간 개방한다.
      근거 없음 → '제15조 (실습실 사용) 실습실은 24시간 개방한다.'

총 4건 중 1건 근거 없음
exit=1
```

잡혔다. 조문 번호까지 그럴듯하게 붙어 있어서 사람 눈으로는 놓치기 쉬운 문장인데, **문자열 대조는 속지 않는다.**

`exit=1` 이므로 이걸 그대로 CI나 L2-4의 게이트에 꽂을 수 있다.

### 마지막으로 연결한다

지금 손에 있는 조각들을 다시 본다.

| 조각 | 어디서 만들었나 | 무엇을 하나 |
|---|---|---|
| 스킬 | L1-1, L1-2 | 절차를 재사용 가능하게 굳힌다 |
| 커넥터 | L1-3 | 데이터에 닿는 문을 읽기 전용으로 연다 |
| 승인·훅 | L2-1 ~ L2-3 | 되돌릴 수 없는 일을 막는다 |
| 게이트 | L2-4 | 통과 못 하면 끝나지 않게 한다 |
| 감시 루프 | L3-1, L3-2 | 필요할 때만 깨어난다 |
| 메모장 | L3-3 | 깨어날 때마다 이어서 한다 |
| 기억·그래프 | L4-1, L4-2 | 세션을 넘어 남는다 |
| 근거 검증기 | L4-3 | 남은 것이 참인지 보장한다 |

이 여덟 개를 하나로 묶으면 **밤새 도는 신뢰할 수 있는 에이전트**가 된다. 모듈 3의 "아침 루프" 그림이 실제로는 이 조각들의 조립이다.

### 막히면

- **`claims.json` 이 안 생기거나 JSON이 깨진다** — 프롬프트에 형식 예시를 더 구체적으로 적는다. 작은 모델일수록 예시가 효과가 크다.
- **quote가 미묘하게 다르다** — 공백이나 줄바꿈 차이다. 검증기를 `q.replace(" ","") in src.replace(" ","")` 로 느슨하게 만들 수도 있지만, **느슨하게 만드는 순간 검증기의 가치도 느슨해진다.** 먼저 원문을 그대로 복사하도록 프롬프트를 고치는 쪽을 시도한다.

---

## 실습 5. 명세 주도 개발 — 모듈 5를 손으로 확인한다

명세는 글이라서 "제대로 썼는지"를 눈으로 판단하기 어렵다. 이 그룹의 실습은 전부 **기계가 판정할 수 있는 형태**로 바꿔서 확인한다.

## L5-1. 명세 없이 시킨 것과 명세로 시킨 것을 나란히 놓는다

> 대응 | 모듈 5 · 1~3절 (두 개의 루프, 명세가 제품이다, 정밀도 시험)
> 소요 | 35분 (모델 호출 2회)
> 선행 | L0-2
> 확인 | 명세 없음 6개 중 5개 (2분 39초) · 명세 있음 6개 중 6개 (6분 9초)

### 무엇을

같은 기능을 **한 문장으로** 한 번, **여섯 절짜리 명세로** 한 번 만들게 하고, 둘을 같은 체크리스트로 채점한다.

### 왜

모듈 5는 "명세를 쓰면 결과가 좋아진다"고 말한다. 그런데 이건 믿음이 되기 쉽다. 명세를 쓴 쪽이 좋아 **보이는** 건 시간을 더 썼기 때문일 수도 있다.

그래서 이 실습은 **채점표를 먼저 만든다.** 무엇을 좋다고 할지 정해 놓고 두 결과를 같은 자로 잰다. 이건 모듈 5의 수용 기준(acceptance criteria)을 실제로 써 보는 것이기도 하다.

### 해보기

먼저 **채점표부터** 만든다. 순서가 중요하다 — 결과를 보고 나서 기준을 정하면 자기 편향이 들어간다.

```bash
mkdir -p ~/hermes-lab/sdd/none ~/hermes-lab/sdd/spec && cd ~/hermes-lab/sdd

cat > check.py <<'PYEOF'
import subprocess, sys, json, pathlib
# 수용 기준 검사기 — 만들어진 파일이 요구사항을 지켰는지 기계로 판정한다.

target = sys.argv[1] if len(sys.argv) > 1 else "."
if not (pathlib.Path(target) / "slugify.py").exists():
    print("FAIL  파일 없음: slugify.py"); sys.exit(1)

cases = [
    ("기본 변환",       "Hello World",   "hello-world"),
    ("연속 공백 하나로", "a    b",        "a-b"),
    ("앞뒤 공백 제거",   "  hi  ",        "hi"),
    ("특수문자 제거",    "C++ & Python!", "c-python"),
    ("빈 문자열",       "",              ""),
    ("한글 보존",       "안녕 하세요",     "안녕-하세요"),
]
code = "import slugify,json,sys; print(json.dumps([slugify.slugify(c) for c in json.load(sys.stdin)]))"
r = subprocess.run([sys.executable, "-c", code], input=json.dumps([c[1] for c in cases]),
                   capture_output=True, text=True, cwd=target)
if r.returncode != 0:
    print("FAIL  실행 오류:", r.stderr.strip()[-300:]); sys.exit(1)
got = json.loads(r.stdout)

bad = 0
for (name, src, want), g in zip(cases, got):
    ok = g == want
    extra = "" if ok else "  (기대: %r)" % want
    print("%s  %-14s %r -> %r%s" % ("PASS" if ok else "FAIL", name, src, g, extra))
    bad += (not ok)
print("\n%d개 중 %d개 충족" % (len(cases), len(cases) - bad))
sys.exit(1 if bad else 0)
PYEOF
```

**A. 명세 없이 한 문장으로 시킨다.**

```bash
cd ~/hermes-lab/sdd/none
hermes chat -q "slugify.py 에 slugify(text) 함수를 만들어줘. 문자열을 URL 슬러그로 바꾸는 함수야." -Q
cd ~/hermes-lab/sdd && python3 check.py none; echo "exit=$?"
```

**B. 여섯 절 명세를 주고 시킨다.**

```bash
cd ~/hermes-lab/sdd/spec
cat > spec.md <<'MDEOF'
# spec.md — slugify

## 목표
문자열을 URL에 넣을 수 있는 슬러그로 바꾼다. 게시글 제목을 주소에 쓰기 위함이다.

## 사용자 시나리오
- 제목 "Hello World" 를 넣으면 "hello-world" 를 얻는다.
- 한글 제목을 넣으면 한글이 그대로 남은 슬러그를 얻는다.

## 기능 요구사항
- FR-1 영문 대문자는 소문자로 바꾼다.
- FR-2 공백은 하이픈 하나로 바꾼다. 공백이 여러 개 연속이어도 하이픈은 하나다.
- FR-3 앞뒤 공백은 제거한다. 결과가 하이픈으로 시작하거나 끝나지 않는다.
- FR-4 영문자·숫자·하이픈·한글 이외의 문자는 제거한다.
- FR-5 한글은 그대로 보존한다.

## 경계 사례와 규칙
- 빈 문자열을 넣으면 빈 문자열을 반환한다. 예외를 던지지 않는다.
- 제거 후 아무것도 남지 않으면 빈 문자열을 반환한다.
- 하이픈이 연속되면 하나로 합친다.

## 범위 밖
- 유니코드 정규화, 다른 언어 음역, 길이 제한, 중복 슬러그 처리.

## 수용 기준
- [ ] "Hello World" 는 "hello-world" 가 된다
- [ ] "a    b" 는 "a-b" 가 된다
- [ ] "  hi  " 는 "hi" 가 된다
- [ ] "C++ & Python!" 는 "c-python" 이 된다
- [ ] "" 는 "" 이 된다
- [ ] "안녕 하세요" 는 "안녕-하세요" 가 된다
MDEOF

hermes chat -q "이 폴더의 spec.md 를 읽고 그 명세를 만족하는 slugify.py 를 작성해라. 명세에 없는 기능은 넣지 마라." -Q
cd ~/hermes-lab/sdd && python3 check.py spec; echo "exit=$?"
```

### 기대 결과

**A (명세 없음)** — 검증 시 6개 중 5개를 충족했다.

```
PASS  기본 변환        'Hello World' -> 'hello-world'
PASS  연속 공백 하나로  'a    b' -> 'a-b'
PASS  앞뒤 공백 제거    '  hi  ' -> 'hi'
PASS  특수문자 제거     'C++ & Python!' -> 'c-python'
PASS  빈 문자열        '' -> ''
FAIL  한글 보존        '안녕 하세요' -> ''  (기대: '안녕-하세요')

6개 중 5개 충족
exit=1
```

**B (명세 있음)** — 6개 중 6개 충족, `exit=0`.

### 여기서 알아채야 할 것 — A가 잘 나온 것이 요점이다

기대와 달리 A는 꽤 잘했다. 소문자, 연속 공백, 앞뒤 공백, 특수문자, 빈 문자열까지 다 맞혔다. **딱 하나를 틀렸는데, 그 하나가 정확히 요점이다.**

한글을 넣었더니 **빈 문자열이 나왔다.** 슬러그를 ASCII만 남기는 것은 영어권에서 지극히 표준적인 구현이다. 모델은 틀린 게 아니라 **가장 흔한 관행을 따랐다.** 그리고 우리 상황에서 그건 기능 전체가 죽는 결과였다.

> 모델이 못해서 실패한 게 아니다. **아무도 물어보지 않아서 실패했다.**

한글을 살릴지 죽일지는 상식이 아니라 **결정**이다. 그 결정이 명세에 없으면 누군가 대신 내리고, 대개는 관행대로 내린다. 모듈 5의 표현으로는 이렇다.

> 유능한 사람도 "URL 슬러그로 바꿔 줘"를 지키면서 얼마든지 다른 것을 만들 수 있다.
> 그러니 그 문장은 정밀도 시험을 통과하지 못한 것이다.

**정확한 숫자는 매번 다르다.** A가 3개를 맞힐 수도 6개를 다 맞힐 수도 있다. 확인할 것은 숫자가 아니라 **A가 틀린 항목이 어떤 종류인가**다. 실패한 것이 "모델이 부주의해서"인지 "물어보지 않아서 알 수 없었던 것"인지 구분해 본다. 후자라면 그 줄이 명세에 들어가야 할 문장이다.

### 시간도 재 본다

검증 시 A는 2분 39초, B는 6분 9초 걸렸다. **명세로 만든 쪽이 2배 넘게 느리다.** 명세를 쓰는 시간은 여기 포함되지도 않았다.

이 숫자를 정직하게 봐야 한다. 모듈 5가 "SDD에는 비용이 있고, 초보자는 가장 답답한 순간에 그만둔다"고 한 그 비용이 이것이다. **결과물을 오늘 버릴 거라면 A가 맞다.** 갚을 일이 없는 빚은 빚이 아니다.

### 막히면

- **A가 의외로 잘 나온다** — 좋은 일이다. 그러면 `check.py` 에 요구사항을 두세 개 더 얹는다(길이 제한, 숫자 처리, 밑줄 처리). 요구사항이 늘어날수록 격차가 벌어지는 것을 보게 된다.
- **B에서 `slugify.py` 를 못 찾는다** — `cd ~/hermes-lab/sdd/spec` 에서 실행했는지 확인한다. 에이전트는 현재 폴더에 만든다.

### 이어지는 곳

방금 만든 `check.py` 가 **수용 기준을 실행 가능한 검사로 바꾼 것**이다. L5-3에서 이것을 게이트에 연결한다.

---

## L5-2. AI가 나를 인터뷰하게 만든다

> 대응 | 모듈 5 · 8절 (3단계 확인 인터뷰)
> 소요 | 25분 (모델 호출 1회)
> 선행 | L5-1
> 확인 | 두 줄짜리 명세에서 질문 30개 도출 (2분 24초) · 파일 생성 0건

### 무엇을

일부러 구멍이 많은 명세를 주고, 에이전트가 **나에게 질문하도록** 시킨다.

### 왜

모듈 5에서 "가장 값진데 가장 많이 건너뛰는 단계"라고 한 것이 이것이다. 건너뛰는 이유는 단순하다 — **코드가 한 줄도 안 나와서 진도가 안 나가는 것처럼 느껴지기 때문이다.**

이 실습은 그 느낌을 반증한다. 인터뷰가 끄집어낸 질문 하나하나가 **L5-1에서 A가 틀렸던 항목들**과 같은 종류라는 걸 보게 된다.

### 해보기

구멍이 많은 명세를 쓴다. 일부러 그렇게 쓴다.

```bash
mkdir -p ~/hermes-lab/sdd/interview && cd ~/hermes-lab/sdd/interview

cat > spec-draft.md <<'MDEOF'
# spec.md — 파일 업로드 (초안)

## 목표
사용자가 프로필 사진을 올릴 수 있게 한다.

## 기능 요구사항
- FR-1 사용자는 프로필 사진을 업로드할 수 있다.
- FR-2 업로드한 사진은 프로필에 표시된다.
MDEOF

hermes chat -q "이 폴더의 spec-draft.md 를 읽어라. 아무것도 만들지 말고, 이 명세에 대해 나를 인터뷰해라. 모호한 곳, 빠진 경계 사례, 말하지 않은 가정을 파고들어라. 질문만 번호를 붙여 목록으로 내라. 코드나 수정된 명세를 쓰지 마라." -Q
```

### 기대 결과

질문이 목록으로 나온다. **검증 시 30개가 나왔고, 스스로 범주까지 나눴다.**

```
[범위]        1~3   무엇까지가 이 기능인가
[입력·검증]   4~11  형식, 용량, 개수, 대체 정책
[표시]       12~16  어느 화면에, 어떤 비율로, 없을 때는 무엇을
[보안·리스크] 17~20  MIME 신뢰 범위, 파일명 발급, 레이트리밋, 악성 파일
[저장소·운영] 21~23  어디에 저장, 다중 인스턴스, 장애 시 동작
[실패와 UX]  24~25  오류 메시지, 중단·타임아웃
[검증·완료]  26~27  "업로드 성공"의 정의는 저장인가 200인가 화면 표시인가
[전제]       28~30  지원 기기, 촬영 직후 업로드, 초상권 책임 소재
```

마지막에 이렇게 되묻는 것까지 한다.

> "이 중 범위 질문(1~3번)에서 먼저 답을 주면, 나머지가 실제로 필요한지가 크게 갈린다."

**세어 본다. 두 줄에서 30개다.** 이 중 몇 개가 내가 미리 생각했던 것인가?

특히 26번을 보자 — **"업로드 성공"의 정의가 파일이 저장된 것인가, API가 200을 반환한 것인가, 화면에 표시된 것인가?** 이건 명세를 쓸 때 아무도 안 적지만, 나중에 "됐다"와 "안 됐다"가 갈리는 바로 그 지점이다.

모듈 5의 문장이 여기서 확인된다.

> 명세에서 고치면 문장 하나. 구현 후에 고치면 다시 만들기.

### 지시를 지켰는지도 확인한다

```bash
ls ~/hermes-lab/sdd/interview/
```

`spec-draft.md` **하나만** 있어야 한다. "아무것도 만들지 마라"를 지킨 것이다. 파일이 더 생겼다면 지시가 무시된 것이고, 그건 그것대로 모듈 2의 관찰 대상이다.

### 한 걸음 더

질문에 답해서 명세를 채운 뒤, **같은 프롬프트를 다시 돌린다.** 질문이 줄어들면 명세가 조여진 것이다. 새 질문이 계속 나온다면 아직 덜 조인 것이다. 이 반복이 곧 "오해할 것이 없을 때까지"다.

### 막히면

- **에이전트가 질문 대신 명세를 고쳐서 준다** — 매우 흔하다. 프롬프트에 "질문만 목록으로 내라. 수정된 명세를 쓰지 마라"를 강하게 반복한다. 그래도 고치려 들면, 그것 자체가 모듈 2의 교훈이다 — **부탁만으로는 안 되고 하니스가 필요하다.**
- **질문이 너무 일반적이다** — 명세에 도메인 단서를 조금 더 준다. "사내 인사 시스템의 프로필 사진"처럼 맥락이 있으면 질문이 날카로워진다.
- **답변에 한자가 섞여 나온다** — 검증 시 `时的`, `炸弹`, `肖像권` 같은 단어가 섞였다. 중국어 데이터로 학습된 모델에서 한국어 생성 중 간혹 나타나는 현상이고 내용에는 문제가 없다. 거슬리면 프롬프트 끝에 "모든 답변은 한국어로만 쓴다"를 붙인다.
- **질문이 30개나 나와서 부담스럽다** — 그게 요점이다. 전부 답할 필요는 없다. 에이전트가 제안한 대로 **범위 질문부터 답하면 나머지 다수가 자동으로 정리된다.**

### 이어지는 곳

L5-3에서 이렇게 조인 명세의 수용 기준을 **자동 검사**로 바꾼다.

---

## L5-3. 수용 기준을 게이트에 연결한다

> 대응 | 모듈 5 · 9절 (루프를 닫는 두 검사) / 모듈 2 · 8~9절 (검증, 교정)
> 소요 | 40분 (모델 호출 1회, 게이트가 여러 턴을 강제하므로 2~4분)
> 선행 | L5-1, L2-4
> 확인 | 1차 통과(2분 40초) · 회귀 주입 후 게이트가 차단→수정→통과 (3분 57초)

### 무엇을

L5-1에서 만든 검사기를 L2-4의 `pre_verify` 게이트에 물려서, **수용 기준을 통과하기 전에는 에이전트가 끝낼 수 없게** 만든다.

### 왜

여기가 모듈 5와 모듈 2가 만나는 지점이다.

모듈 5는 "수용 기준을 실행 가능한 검사로 만들라"고 한다. 모듈 2는 "검사 결과를 에이전트에게 돌려주라"고 한다. 둘을 합치면 **명세가 강제력을 얻는다.**

그리고 이것이 모듈 5의 첫 번째 반론에 대한 답이다 — *"자연어는 모호하다"*. 맞다. 그래서 **명세의 형식적인 부분을 검사가 맡는다.** 산문은 의도를 담고, 검사는 판정을 담는다.

### 해보기

수용 기준 전용 게이트 스크립트를 만든다. **작업 폴더에 `spec-check.py` 가 있을 때만** 동작하므로 다른 실습을 방해하지 않는다.

```bash
cat > $HERMES_HOME/agent-hooks/spec-gate.sh <<'SHEOF'
#!/usr/bin/env bash
# pre_verify 게이트: 작업 폴더에 spec-check.py 가 있으면 그것으로 판정한다.
payload="$(cat -)"
cwd=$(printf '%s' "$payload" | python3 -c "import json,sys; print(json.load(sys.stdin).get('cwd') or '')" 2>/dev/null)
[ -z "$cwd" ] && { echo '{}'; exit 0; }
[ -f "$cwd/spec-check.py" ] || { echo '{}'; exit 0; }
cd "$cwd" || { echo '{}'; exit 0; }
out=$(python3 spec-check.py 2>&1)
rc=$?
echo "[$(date -Is)] spec-gate rc=$rc cwd=$cwd" >> /tmp/spec-gate.log
if [ $rc -eq 0 ]; then
  echo '{}'
else
  python3 - "$out" <<'PY'
import json, sys
msg = ("수용 기준 미충족 — 아직 끝내지 마라. 아래는 spec.md 의 수용 기준을 그대로 옮긴 "
       "검사 결과다. 실패한 항목을 고쳐라. spec-check.py 는 절대 수정하지 마라.\n\n")
print(json.dumps({"action": "continue", "message": msg + sys.argv[1][-1500:]},
                 ensure_ascii=False))
PY
fi
SHEOF
chmod +x $HERMES_HOME/agent-hooks/spec-gate.sh
```

설정의 `hooks:` 안, `pre_verify` 목록 맨 앞에 한 줄 더 넣는다.

```bash
python3 - <<EOF
import pathlib
p = pathlib.Path("$HERMES_HOME/config.yaml")
t = p.read_text(encoding="utf-8")
assert "spec-gate.sh" not in t, "이미 추가되어 있음"
t = t.replace("  pre_verify:\n",
              '  pre_verify:\n    - command: "$HERMES_HOME/agent-hooks/spec-gate.sh"\n      timeout: 60\n')
p.write_text(t, encoding="utf-8")
print(t[t.index("hooks:"):])
EOF
```

작업 폴더를 만든다. 검사기는 L5-1의 것을 그대로 쓰되 자기 폴더를 보게 한다.

```bash
mkdir -p ~/hermes-lab/sdd/gated && cd ~/hermes-lab/sdd/gated
cp ~/hermes-lab/sdd/spec/spec.md .
cp ~/hermes-lab/sdd/check.py spec-check.py
python3 spec-check.py; echo "exit=$? (파일이 아직 없으니 1이 정상)"
```

이제 **명세를 주되 일부러 대충** 시킨다.

```bash
hermes chat -q "이 폴더의 spec.md 를 읽고 slugify.py 를 만들어라. 간단하게 만들고 검사는 돌리지 마라." --accept-hooks -Q
python3 spec-check.py; echo "exit=$?"
cat /tmp/spec-gate.log
```

### 기대 결과 (1차)

검증 시 에이전트가 **첫 시도에 6개를 모두 맞혔다.** 게이트는 발동했지만 통과시켰다.

```
[2026-08-17T05:16:23+00:00] spec-gate rc=0 cwd=.../sdd/gated
```

명세가 좋으면 이렇게 된다. **게이트가 조용한 것은 실패가 아니라 성공이다.** 모듈 3의 하트비트와 같은 원리다.

### 그런데 게이트의 진짜 값어치는 여기서 나오지 않는다

게이트가 한 번 통과시키는 것만 보고 끝내면 "그럼 왜 만들었지?" 싶어진다. **일부러 무너뜨려서 잡히는 것을 봐야** 감이 온다.

지금 잘 도는 코드에 **회귀(regression)를 심는다.** 한글 허용 범위를 지운다.

```bash
cd ~/hermes-lab/sdd/gated
cp slugify.py slugify.py.good

python3 - <<'PYEOF'
import pathlib, re
p = pathlib.Path("slugify.py"); t = p.read_text(encoding="utf-8")
p.write_text(re.sub(r"\\uac00-\\ud7a3|가-힣|\\u3131-\\u318e", "", t), encoding="utf-8")
print("한글 허용 범위를 제거했다(회귀 주입).")
PYEOF

python3 spec-check.py | tail -3
```

`6개 중 5개 충족` 이 나온다. 이제 **이 회귀와 아무 상관없는 작업**을 시킨다.

```bash
rm -f /tmp/spec-gate.log
hermes chat -q "slugify.py 의 slugify 함수에 한 줄짜리 docstring 만 추가해줘. 로직은 절대 건드리지 마." --accept-hooks -Q
cat /tmp/spec-gate.log
python3 spec-check.py | tail -3
```

### 기대 결과 (2차) — 이게 이 실습의 핵심이다

```
[2026-08-17T05:19:25+00:00] spec-gate rc=1 cwd=.../sdd/gated     ← 차단
[2026-08-17T05:20:41+00:00] spec-gate rc=0 cwd=.../sdd/gated     ← 통과
```

```
PASS  한글 보존  '안녕 하세요' -> '안녕-하세요'

6개 중 6개 충족
```

무슨 일이 있었는지 정리한다.

1. 사용자는 **"docstring만 추가하고 로직은 절대 건드리지 마"** 라고 했다.
2. 에이전트는 docstring을 추가하고 끝내려 했다.
3. **게이트가 막았다.** 자기가 만들지도 않은 회귀 때문에.
4. 에이전트는 실패한 수용 기준을 읽고 **한글 지원을 복구했다.**
5. 게이트가 통과시켰고, 그제야 턴이 끝났다.

**게이트는 이번 변경만 보는 게 아니라 저장소 전체의 상태를 본다.** 그래서 남이 만든 회귀도, 내가 3주 전에 만든 회귀도 여기서 걸린다.

이것이 모듈 5가 말한 "수용 기준을 실행 가능한 검사로 만들라"의 진짜 의미다. 검사가 문서에 있으면 아무도 안 읽지만, **게이트에 물려 있으면 모든 커밋이 그 검사를 통과해야 한다.**

그리고 L2-4에서 본 구조가 여기서도 그대로다 — **게이트는 사용자의 지시보다 상위에 있다.**

원래 코드로 되돌리려면 이렇게 한다.

```bash
mv slugify.py.good slugify.py && python3 spec-check.py | tail -2
```

### 여기서 완성되는 그림

| 층 | 형태 | 읽는 쪽 |
|---|---|---|
| `spec.md` 의 수용 기준 | 사람이 읽는 합의 | 사람 |
| `spec-check.py` | 기계가 읽는 같은 합의 | 기계 |
| `pre_verify` 게이트 | 통과 전에는 끝낼 수 없음 | 에이전트 |

세 줄이 같은 것을 말하고 있다. **명세가 문서에서 강제력으로 바뀌는 지점**이 이 세 줄이다.

### 막히면

- **게이트가 안 걸린다** — `spec-check.py` 파일명이 정확한지, 그 폴더에서 실행했는지 확인한다. `hermes hooks list` 로 `pre_verify` 항목이 둘인지도 본다.
- **에이전트가 검사 파일을 고쳐서 통과시킨다** — 실제로 일어나는 일이다. 프롬프트에 "절대 수정하지 마라"가 들어 있지만 부탁일 뿐이다. 진짜로 막으려면 `pre_tool_call` 훅으로 `spec-check.py` 쓰기를 차단한다(L2-3 응용). **이것이 모듈 2의 "부탁이 아니라 벽" 원칙의 실전 사례다.**

### 이어지는 곳

L5-4에서 이 구조가 시간이 지나며 어떻게 무너지는지 본다.

---

## L5-4. 명세 표류를 일부러 만들고, 잡아낸다

> 대응 | 모듈 5 · 11절 (명세를 살아 있게 유지한다)
> 소요 | 35분 (모델 호출 0회 — 전원 동시 진행 가능)
> 선행 | L5-3
> 확인 | 순진한 검사기는 거짓 통과 · 절 구분 후 CONFLICT 1건 검출 · 명세 갱신 후 0건

### 무엇을

코드만 고치고 명세는 그대로 두는 **표류**를 재현하고, 그것을 기계가 잡아내게 한다. 그 과정에서 **검사기 자체가 틀리는 것**도 겪는다.

### 왜

모듈 5의 표류 시나리오는 3주 뒤에 벌어지는 일이라 강의실에서는 실감이 안 난다. 압축해서 몇 분 만에 겪어 본다.

그리고 더 중요한 것 — **표류를 잡는 검사는 따로 만들어야 한다.** L5-3의 게이트는 "코드가 명세를 만족하는가"를 본다. 하지만 **명세가 코드와 함께 갱신됐는가**는 아무도 안 본다. 이건 다른 질문이다.

이 실습에는 모델 호출이 없다. 수업에서 전원이 동시에 해도 된다.

### 해보기 1 — 표류를 심는다

L5-3에서 만든 폴더를 그대로 쓴다. 요구사항이 바뀌었다고 치고 **코드만** 고친다.

```bash
cd ~/hermes-lab/sdd/gated
python3 spec-check.py | tail -2      # 지금은 6/6 인 상태

python3 - <<'PYEOF'
import pathlib
p = pathlib.Path("slugify.py"); t = p.read_text(encoding="utf-8")
t += "\n\n_orig_slugify = slugify\n\n\ndef slugify(text):\n    return _orig_slugify(text)[:20].rstrip('-')\n"
p.write_text(t, encoding="utf-8")
print("코드에만 길이 제한을 추가했다. spec.md 는 건드리지 않았다.")
PYEOF

python3 -c "import slugify; print(repr(slugify.slugify('this is a very long title that keeps going')))"
```

`'this-is-a-very-long'` 이 나온다. **코드는 자르는데 명세는 자른다는 말이 없다.** 표류가 생겼다.

### 해보기 2 — 순진한 검사기를 만든다 (그리고 속는다)

가장 먼저 떠오르는 방법으로 만들어 본다. 코드에서 동작 신호를 찾고, 그 키워드가 명세 **어딘가에** 있는지 본다.

```bash
cat > drift-naive.py <<'PYEOF'
import pathlib, re, sys
spec = pathlib.Path("spec.md").read_text(encoding="utf-8")
code = pathlib.Path("slugify.py").read_text(encoding="utf-8")

signals = [
    (r"\[\s*:\s*\d+\s*\]", "길이 제한(슬라이스)", ["길이", "최대", "자로 자"]),
    (r"\.lower\(\)",       "소문자 변환",         ["소문자"]),
    (r"strip",             "앞뒤 제거",           ["앞뒤", "제거"]),
]

bad = 0
for pat, name, words in signals:
    if not re.search(pat, code):
        continue
    if any(w in spec for w in words):
        print("OK     '%s' — 코드와 명세가 일치" % name)
    else:
        print("DRIFT  코드는 '%s' 을(를) 하는데 spec.md 에 근거가 없다" % name)
        bad += 1
print("\n표류 %d건" % bad)
sys.exit(1 if bad else 0)
PYEOF

python3 drift-naive.py; echo "exit=$?"
```

### 기대 결과 — 검사기가 속는다

```
OK     '길이 제한(슬라이스)' — 코드와 명세가 일치
OK     '소문자 변환' — 코드와 명세가 일치
OK     '앞뒤 제거' — 코드와 명세가 일치

표류 0건
exit=0
```

**표류 0건이 나왔다. 틀렸다.** 왜 그런지 명세를 보면 안다.

```bash
grep -n "길이" spec.md
```

```
## 범위 밖
- 유니코드 정규화, 다른 언어 음역, 길이 제한, 중복 슬러그 처리.
```

명세에 "길이 제한"이 있긴 있다. 그런데 **"하지 않는다"는 뜻으로 있다.** 검사기는 단어만 보고 통과시켰다.

이건 표류 중에서도 가장 나쁜 종류다.

> 명세는 **"이건 안 한다"** 고 적혀 있고, 코드는 **그걸 하고 있다.**
> 이 상태로 코드를 읽은 사람은 명세를 믿지 않게 되고, 명세를 읽은 사람은 코드를 잘못 이해한다.

### 해보기 3 — 절을 구분하게 고친다

명세의 절마다 **역할이 다르다.** 기능 요구사항·경계 사례·수용 기준은 **약속하는 절**이고, 범위 밖은 **약속하지 않는 절**이다. 검사기가 이 둘을 구분해야 한다.

```bash
cat > drift-check.py <<'PYEOF'
import pathlib, re, sys
# 표류 검사기 — 코드의 동작이 명세의 '약속하는 절'에 적혀 있는지 본다.

spec = pathlib.Path("spec.md").read_text(encoding="utf-8")
code = pathlib.Path("slugify.py").read_text(encoding="utf-8")


def section(title):
    m = re.search(r"^## %s\s*$(.*?)(?=^## |\Z)" % re.escape(title), spec, re.S | re.M)
    return m.group(1) if m else ""


promised = section("기능 요구사항") + section("경계 사례와 규칙") + section("수용 기준")
excluded = section("범위 밖")

signals = [
    (r"\[\s*:\s*\d+\s*\]", "길이 제한(슬라이스)", ["길이", "최대", "자로 자"]),
    (r"\.lower\(\)",       "소문자 변환",         ["소문자"]),
    (r"strip",             "앞뒤 제거",           ["앞뒤", "제거"]),
]

bad = 0
for pat, name, words in signals:
    if not re.search(pat, code):
        continue
    if any(w in promised for w in words):
        print("OK     '%s' — 코드와 명세가 일치" % name)
    elif any(w in excluded for w in words):
        print("CONFLICT  코드는 '%s' 을(를) 하는데 spec.md 는 그것을 '범위 밖'이라고 적었다" % name)
        bad += 1
    else:
        print("DRIFT  코드는 '%s' 을(를) 하는데 spec.md 에 근거가 없다" % name)
        bad += 1

print("\n불일치 %d건" % bad)
sys.exit(1 if bad else 0)
PYEOF

python3 drift-check.py; echo "exit=$?"
```

이번에는 잡는다.

```
CONFLICT  코드는 '길이 제한(슬라이스)' 을(를) 하는데 spec.md 는 그것을 '범위 밖'이라고 적었다
OK     '소문자 변환' — 코드와 명세가 일치
OK     '앞뒤 제거' — 코드와 명세가 일치

불일치 1건
exit=1
```

### 해보기 4 — 모듈 5가 시킨 순서대로 고친다

코드가 아니라 **명세를 먼저** 고친다. 그리고 "범위 밖"에서 길이 제한을 **빼는 것**까지 해야 한다 — 약속하는 절에 추가하는 것만으로는 두 절이 서로 모순된 채로 남는다.

```bash
python3 - <<'PYEOF'
import pathlib
p = pathlib.Path("spec.md"); t = p.read_text(encoding="utf-8")
t = t.replace("- FR-5 한글은 그대로 보존한다.",
              "- FR-5 한글은 그대로 보존한다.\n"
              "- FR-6 슬러그의 최대 길이는 20자다. 잘린 결과가 하이픈으로 끝나면 그 하이픈을 제거한다.")
t = t.replace("- 유니코드 정규화, 다른 언어 음역, 길이 제한, 중복 슬러그 처리.",
              "- 유니코드 정규화, 다른 언어 음역, 중복 슬러그 처리.")
t = t.replace('- [ ] "안녕 하세요" 는 "안녕-하세요" 가 된다',
              '- [ ] "안녕 하세요" 는 "안녕-하세요" 가 된다\n'
              '- [ ] 20자를 넘는 입력은 20자 이하로 잘리고 하이픈으로 끝나지 않는다')
p.write_text(t, encoding="utf-8")
print("spec.md: FR-6 추가, '범위 밖'에서 길이 제한 삭제, 수용 기준 추가")
PYEOF

python3 drift-check.py; echo "exit=$?"
```

`불일치 0건`, `exit=0`.

### 여기서 알아야 할 것

**첫째, 검사기가 틀릴 수 있다.** 그리고 검사기가 틀리면 **틀렸다는 사실조차 모른다.** `표류 0건`은 "괜찮다"처럼 보인다. L4-3에서 근거 검증기에 가짜 주장을 넣어 본 것과 같은 이유로, **검사기는 반드시 실패하는 입력으로 시험해야 한다.**

**둘째, 명세의 절은 이름표가 아니라 의미다.** "범위 밖"은 단순한 목록이 아니라 **부정문의 모음**이다. 기계가 명세를 읽게 하려면 이 구조를 존중해야 한다. 모듈 5가 여섯 절 구조를 고집한 이유가 여기 있다 — **구조가 있어야 기계가 읽을 수 있다.**

**셋째, 검사기는 여전히 조잡하다.** 정규식으로 코드 신호를 찾고 명세 절에서 키워드를 보는 게 전부다. 놓치는 것이 많고 거짓 경보도 낸다.

그런데도 **일한다.** 그리고 이게 요점이다.

> 표류를 막는 데 정교한 도구가 필요한 게 아니다.
> **누군가 "코드와 명세가 아직 같은 이야기를 하는가"를 정기적으로 묻기만 하면 된다.**
> 자동화하면 잊지 않을 뿐이다.

### 조립한다

이 검사를 앞의 실습들에 물려 보면 강좌 전체가 한 덩어리가 된다.

| 어디에 물리나 | 무엇이 되나 | 실습 |
|---|---|---|
| `pre_verify` 게이트 | 표류가 있으면 턴을 끝낼 수 없다 | L2-4 · L5-3 |
| cron 감시 루프 | 코드가 바뀔 때마다 표류를 확인하는 하트비트 | L3-2 |
| `pre_tool_call` 훅 | 명세를 안 고치면 코드 파일 쓰기를 차단 | L2-3 |

### 막히면

- **`CONFLICT` 대신 `DRIFT` 가 나온다** — 명세의 절 제목이 정확히 `## 범위 밖` 인지 확인한다. 절 이름이 다르면 `section()` 이 빈 문자열을 돌려준다.
- **명세를 고쳤는데도 `CONFLICT` 가 남는다** — "범위 밖"에서 해당 항목을 지웠는지 본다. 약속하는 절에 넣기만 하고 부정하는 절에서 빼지 않으면 **명세가 스스로 모순된 상태**다. 이 검사기는 그 모순도 잡는다.
- **거짓 경보가 난다** — 정상이다. 이 검사기의 정밀도를 어디까지 올릴지, 어디서 포기하고 사람 검토에 맡길지 판단하는 것이 모듈 5의 "설계 건강 검사"다.

### 이어지는 곳

이것으로 다섯 모듈이 한 바퀴 돈다. 명세가 무엇을 만들지 정하고(모듈 5), 스킬과 커넥터가 능력을 주고(모듈 1), 하니스가 그것을 안전하게 만들고(모듈 2), 루프가 사람 없이 돌리고(모듈 3), 그래프가 기억을 남긴다(모듈 4).

---

## 마치며 — 다음에 할 것

실습 스물세 개가 끝났다. 여기서 만든 것은 전부 장난감이지만, **구조는 실무와 같다.**

이어서 해 볼 만한 것을 난이도 순으로 적는다.

1. **내 스킬 한 개를 진짜로 쓰기.** 실제로 반복하는 일 하나를 골라 SKILL.md로 만든다. 일주일 쓰고, 안 맞는 부분을 고친다. 모듈 2의 ratchet이다.
2. **L2-4의 게이트를 내 프로젝트에 걸기.** 테스트가 있는 프로젝트라면 `pre_verify` 훅 하나로 "테스트 깨진 채로 끝내기"가 불가능해진다.
3. **L3-2의 감시 루프를 진짜 대상에 걸기.** 학과 공지 페이지, CI 상태, 서버 로그 등. 감시 스크립트만 바꾸면 된다.
4. **메신저 게이트웨이 붙이기.** `hermes gateway` 로 텔레그램·디스코드에 연결하면 결과가 휴대폰으로 온다. 다만 **수업 시간에는 켜지 않는다** — 공유 GPU 서버에 백그라운드 부하가 걸린다.
5. **모델 바꿔 보기.** `hermes chat -m qwen3.6:35b` 처럼 모델만 바꿔 같은 실습을 다시 돌려 본다. L1-2에서 놓쳤던 규칙을 더 큰 모델은 지키는가? **하니스가 얼마나 모델 의존적인지**를 직접 재 보는 실험이다.

### 정리 명령

실습 환경을 처음으로 되돌리려면 폴더 하나만 지우면 된다. 개인 설정은 그대로다.

```bash
rm -rf ~/hermes-lab
# ~/.bashrc 에서 HERMES_HOME 줄도 지운다
```

## 이해도 점검

**1. L1-1에서 스킬을 끄려고 디렉터리 이름 앞에 점을 붙였는데도 스킬이 계속 발동했다. 왜인가?**

답: Hermes는 디렉터리 이름이 아니라 SKILL.md 안의 `name:` 필드를 읽어 스킬을 식별하고, 숨김 디렉터리도 그대로 훑기 때문이다. 끄는 방법은 `config.yaml` 의 `skills.disabled` 에 이름을 넣거나, 디렉터리를 `skills/` 트리 바깥으로 옮기는 것이다.

**2. L3-2에서 무변화 틱이 0.49초, 변화 틱이 56초였다. 이 차이가 아낀 것은 정확히 무엇인가?**

답: 모델 API 호출 한 번 전체다. 그 한 번에는 응답 생성뿐 아니라 시스템 프롬프트·스킬 목록·도구 정의·대화 이력을 다시 보내는 입력 토큰(약 14,000)이 포함된다. L3-4에서 본 대로 입력 토큰이 출력 토큰의 47배이므로, 아낀 비용의 대부분은 응답이 아니라 문맥 전송이다.

**3. L2-4에서 사용자는 "다른 함수는 절대 건드리지 마"라고 했는데 에이전트가 `add` 를 고쳤다. 이건 에이전트의 불복종인가?**

답: 아니다. `pre_verify` 게이트가 테스트 실패를 이유로 종료를 막았고, 에이전트는 통과할 방법을 찾아 실행한 것이다. 하니스는 프롬프트보다 상위에 있다. 이것이 장점(사용자 실수로부터의 보호)이면서 동시에 위험(잘못된 게이트는 무한 루프)이므로, 게이트를 만들 때는 반드시 "영원히 실패하면 어떻게 되는가"를 함께 설계해야 한다.

**4. L3-2의 감시 스크립트에 `date` 를 넣으면 무슨 일이 벌어지는가?**

답: Hermes는 감시 출력을 바이트 단위로 비교하므로 매 틱이 "변화"로 판정된다. 게이트가 무력화되어 모든 틱에서 모델이 깨어난다. 감시 스크립트는 같은 상태면 같은 바이트를 내야 한다(정렬, 시각 제거).

**5. L4-2에서 스킬을 만들어 두기만 하고 한 번도 쓰지 않으면 그래프에 나타나지 않는다. 이건 버그인가 설계인가?**

답: 설계다. 이 그래프는 재고 목록이 아니라 사용의 기록이다. `useCount` 가 함께 기록되는 것도 같은 이유다. 무엇이 설치돼 있는지는 `hermes skills list` 가 답하고, 무엇이 실제로 쓰이는지는 `hermes journey` 가 답한다.

**6. L4-3의 검증기에는 LLM이 없다. 왜 일부러 그렇게 만들었는가?**

답: 판정자는 판정 대상보다 단순해야 신뢰할 수 있기 때문이다. 문자열 포함 검사는 결과가 결정적이고 거짓말을 하지 않는다. LLM으로 근거를 판정하면 그 판정 자체가 다시 검증 대상이 되어 문제가 원점으로 돌아간다.

**7. L4-1에서 회상이 저장보다 7배 빨랐다. 왜인가?**

답: 기억이 도구로 검색된 것이 아니라 프롬프트에 이미 주입돼 있었기 때문이다. 도구 호출이 0회였다. 대신 주입 방식은 매 턴 입력 토큰 비용을 내므로 `memory_char_limit` 같은 상한이 필요하다.

**8. 훅에 `fail_closed: true` 를 붙이는 것이 항상 옳은가?**

답: 아니다. 보안 게이트에는 필요하지만, 관측·로깅용 훅에 붙이면 로거가 잠깐 죽었다는 이유로 정상 작업이 전부 막힌다. 훅의 목적이 "막는 것"이면 fail closed, "보는 것"이면 fail open이 맞다.

## 실습 과제

아래 세 과제는 실습 L0~L4를 모두 마친 뒤에 하는 종합 과제다. 각 과제는 앞에서 만든 조각을 재조립하는 것이며, 새 도구는 필요 없다.

**과제 1. 나의 하니스 만들기 (약 90분)** 자기 전공이나 업무에서 반복하는 일을 하나 고른다. 그것을 위해 ① SKILL.md 한 개(L1-1 방식, 검증 가능한 표식 포함), ② 그 일에서 절대 일어나면 안 되는 사고를 막는 `pre_tool_call` 훅 한 개(L2-3 방식), ③ 결과가 맞는지 판정하는 검증기 스크립트 한 개(L4-3 방식, LLM 없이)를 만든다. 세 개를 붙인 상태에서 일부러 잘못된 지시를 내려 훅과 검증기가 각각 한 번씩 작동하는 것을 로그로 보인다. 제출물: 세 파일 + 작동 로그 + "무엇을 막았고 무엇을 못 막았는가" 한 쪽.

**과제 2. 게이트 달린 루프 만들기 (약 120분)** 실제로 변하는 대상(학과 공지 페이지, 내 저장소의 커밋 목록, 특정 폴더 등)을 하나 정해 L3-2의 감시 루프를 건다. 감시 스크립트는 반드시 안정적 출력이어야 하며, `bash script | md5sum` 을 세 번 실행해 같은 해시가 나오는 것을 먼저 증명한다. 그다음 대상을 실제로 바꿔서 억제 → 발화 → 억제가 순서대로 일어나는 것을 `hermes cron runs` 와 로그로 보인다. 마지막으로 L3-3의 메모장을 붙여 "이미 처리한 항목은 다시 처리하지 않는다"를 만든다. 제출물: 스크립트 + 잡 설정 + 세 상태의 실행 로그 + 소요 시간 비교표.

**과제 3. 근거 그래프 만들고 무너뜨리기 (약 120분)** 원문 문서(강의자료, 규정, 논문 어느 것이든 3~5쪽)를 하나 정해 L4-3 방식으로 `claims.json` 을 만든다. 단 이번에는 주장에 `source`(원문 파일명), `section`(조·절 번호), `confidence` 필드를 추가한다. 검증기도 확장해서 근거 문자열 존재 여부뿐 아니라 section 번호가 실제로 그 근처에 있는지도 본다. 그다음 **일부러 무너뜨린다**: ① 원문을 조금 고쳐서 기존 근거가 깨지게 하고, ② 그럴듯하지만 가짜인 주장을 두 건 섞고, ③ 검증기가 둘 다 잡는지 확인한다. 잡지 못한 것이 있다면 그것이 왜 검증기의 사각지대인지 분석한다. 제출물: claims.json + 확장 검증기 + 무너뜨리기 3종의 결과 + "이 검증기가 못 잡는 오류 유형" 한 쪽.
