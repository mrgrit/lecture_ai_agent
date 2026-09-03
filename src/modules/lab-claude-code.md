# 실습편. Claude Code로 직접 해보기

## 이 실습편을 읽는 법

앞의 다섯 모듈은 도구를 가리지 않는 개념이다. 스킬·하니스·루프·그래프·명세는 어느 에이전트에서도 똑같이 성립한다. 그래서 개념을 본문에 두고, 손으로 만지는 부분을 실습편에 모았다.

실습편은 **두 벌**이다. 하나는 Hermes로, 하나는 Claude Code로 한다. 두 트랙은 실습 번호까지 일대일로 맞춰 두었다. `L2-3`(Hermes)과 `C2-3`(Claude Code)은 같은 개념을 다른 도구로 확인한다.

**왜 두 벌인가.** 개념이 도구에 종속되지 않는다는 것을 말로 하면 잘 와닿지 않는다. 같은 것을 두 도구에서 만들어 보면 그때 분리가 된다. "훅"은 Hermes의 기능이 아니라 에이전트 설계의 개념이고, Hermes는 `hooks.pre_tool_call` 이라 부르고 Claude Code는 `PreToolUse` 라 부를 뿐이다.

**어느 것을 골라야 하나.** 둘 중 하나만 해도 되고, 둘 다 해도 된다.

| | Hermes 트랙 (L) | Claude Code 트랙 (C) |
|---|---|---|
| 비용 | 학교 GPU 서버, 학생 부담 0원 | 개인 구독 또는 API 요금 |
| 모델 | `qwen3.8:27b` (로컬) | Claude 계열 |
| 설치 | 설치 스크립트 한 줄 | 설치 스크립트 한 줄 |
| 인터넷 | 학교 서버까지만 | Anthropic 서버 필요 |
| 강점 | 무료, 오프라인, 내장 스케줄러 | 도구 품질, 서브에이전트, 구조화 출력 |
| 약한 곳 | 모델 능력의 한계가 실습에서 드러남 | 비용이 실습마다 발생 |

**돈이 걱정되면 이렇게 한다.** 이 트랙의 거의 모든 명령에 `--model haiku` 를 붙여 두었다. 가장 싼 모델이고, 형식이 정해진 과제에서는 큰 모델과 차이가 거의 없다(그걸 재는 것이 `C1-4`다).

전 과정 비용은 실측했다. 스물세 개 실습을 처음부터 끝까지 한 번 통과시키면 **공개 목록 가격 기준 약 2.5달러**다. 내역은 이렇다.

| 항목 | 비용 |
|---|---|
| haiku 호출 38회 | 약 $1.9 |
| sonnet 호출 3회 (`C1-4` 비교 실습만) | 약 $0.5 |
| 합계 (모델 호출 44회) | **약 $2.5** |

`C1-4`의 sonnet 비교를 건너뛰면 2달러 아래로 떨어진다. 그리고 비용의 대부분이 응답이 아니라 **문맥 전송**이라는 것을 `C0-2`와 `C3-4`에서 숫자로 확인한다 — 캐시 읽기 토큰이 내가 친 말의 2천 배가 넘는다.

### 각 실습의 구조

- **무엇을** — 이번에 만드는 것 한 문장
- **왜** — 이게 강의의 어느 개념을 손으로 확인하는 것인지
- **해보기** — 그대로 복사해서 붙일 수 있는 명령
- **기대 결과** — 화면에 정확히 무엇이 나와야 하는지
- **막히면** — 실제로 자주 나는 오류와 원인
- **이어지는 곳** — 앞 실습에서 무엇을 물려받고, 다음 실습에서 어떻게 자라는지

### 세 가지 약속

**첫째, 순서대로 한다.** 실습 번호는 의존 순서다. `C2-4`는 `C2-3`이 만든 훅 설정 위에서 돈다. 건너뛰면 "파일이 없다"로 막힌다.

**둘째, 기대 결과를 눈으로 확인하고 넘어간다.** 이 실습편의 목적은 진도가 아니라 "정말 도는구나"를 스물세 번 반복해서 체감하는 것이다. 화면이 기대 결과와 다르면 거기서 멈추고 원인을 찾는다. 그게 실습이다.

**셋째, 모든 것을 프로젝트 폴더 안에서 한다.** 이 트랙은 `~/.claude/` 같은 전역 설정을 건드리지 않는다. 전부 `~/cc-lab/` 아래에 만드는 `.claude/` 폴더 안에서 일어난다. 실습이 끝나면 폴더째로 지우면 흔적이 남지 않는다. 이건 편의가 아니라 원칙이다 — **에이전트의 설정은 프로젝트에 붙어야 하고, 사람에게 붙으면 안 된다.** 그래야 팀원이 저장소를 받았을 때 같은 규칙 아래에서 일한다.

### 이 문서에 적힌 결과는 전부 실제로 돌려서 확인한 것이다

아래 모든 명령과 기대 결과는 다음 환경에서 실제 실행해 확인했다.

| 항목 | 값 |
|---|---|
| Claude Code | 2.1.259 (native, linux-x64) |
| 모델 | `claude-haiku-4-5` (별칭 `haiku`), 비교 실습에서만 `sonnet` |
| 실행 방식 | `claude -p` 비대화 모드 |
| 파이썬 | 3.10 (표준 라이브러리만 사용) |
| OS | Linux, bash |

**확인 방법은 이렇다.** 문서에 적힌 모든 `bash` 블록(94개)을 순서대로 뽑아 실제로 실행하는 스크립트를 만들고, 실습마다 "무엇이 참이면 성공인가"를 기계가 검사하게 했다. 그리고 **완전히 빈 환경에서 처음부터 끝까지 세 번 돌렸다.** 마지막 회차는 24개 구간 전부 통과했고 전체 소요는 14분이었다.

세 번 돌린 이유가 있다. 첫 회차에서 다섯 군데가 실패했고, 그 실패가 전부 문서의 잘못이었다. 스킬을 끈다고 쓴 방법이 실제로는 스킬을 끄지 못했고, MCP 서버 출력의 한글이 깨져 보였고, `tee /dev/stderr` 가 로그를 덮어썼고, `C2-2`에서 심은 폴더 규칙이 `C5-1`을 깨뜨렸다. **그 다섯 개는 모두 이 문서 안에 교훈으로 남겨 두었다** — 실습 중에 같은 일이 생겼을 때 당황하지 않도록.

**의존성을 일부러 0으로 만들었다.** MCP 서버조차 `pip install` 없이 표준 라이브러리만으로 만든다. 수업 중에 "설치가 안 돼요"로 시간을 버리지 않기 위해서다.

### 강사용 요약 — 어느 실습이 얼마나 걸리고 몇 번 모델을 부르나

| 실습 | 소요 | 모델 호출 | 비고 |
|---|---|---|---|
| C0-1 | 10분 | 0 | 설치 진단만 |
| C0-2 | 15분 | 1 | |
| C0-3 | 20분 | 1 | |
| C1-1 | 30분 | 2 | 대조군 포함 |
| C1-2 | 30분 | 2 | |
| C1-3 | 40분 | 1 | 프로토콜 검사는 모델 없이 |
| C1-4 | 25분 | 6 | **sonnet 3회 포함 — 가장 비싸다** |
| C2-1 | 30분 | 4 | 파괴적 동작 없음 |
| C2-2 | 20분 | 5 | 준수율 측정 3회 포함 |
| C2-3 | 40분 | 1 | 훅 단독 검사는 모델 없이 |
| C2-4 | 40분 | 1 | 내부에서 2~4턴 |
| C2-5 | 30분 | 1 | 서브에이전트 1개 |
| C3-1 | 25분 | **0** | 순수 셸 |
| C3-2 | 35분 | 2 | 3틱 중 2틱만 호출 |
| C3-3 | 40분 | 3 | 4회차는 호출 없음 |
| C3-4 | 25분 | 1 | 관측은 모델 없이 |
| C4-1 | 30분 | 4 | |
| C4-2 | 35분 | **0** | 기록 분석만 |
| C4-3 | 45분 | 2 | 검증기는 모델 없이 |
| C5-1 | 40분 | 3 | 라운드 A·B·계획 모드 |
| C5-2 | 30분 | 2 | |
| C5-3 | 40분 | 1 | 내부에서 2~5턴 |
| C5-4 | 35분 | 1 | 검사기는 모델 없이 |
| **합계** | **약 12시간** | **44회** | 약 $2.5 |

**모델을 한 번도 부르지 않는 실습이 셋 있다** — `C0-1`, `C3-1`, `C4-2`. 인터넷이 끊긴 강의실에서도 되고, 계정이 아직 없는 학생도 참여할 수 있다. 수업 첫 시간에 배치하기 좋다.

`C1-4`는 이 트랙에서 유일하게 비싼 실습이다(전체 비용의 20% 이상). 예산이 빡빡하면 강사가 시연으로 한 번만 돌리고 결과 표를 공유하는 것으로 대체할 수 있다.

:::diagram
id: cc-lab-map
원본: (신규 작도)
제목: 실습 스물세 개가 강의 다섯 모듈에 붙는 자리
내용: 준비·스킬·하니스·루프·기억·명세 여섯 그룹과 완성물 여덟 조각
:::

### Hermes 트랙과의 대응표

같은 개념을 두 도구가 어떻게 부르는지 한 장으로 정리했다. 한쪽 트랙만 하더라도 이 표는 읽어 두는 편이 좋다. 취업 후에 쓰게 될 에이전트가 셋 중 어느 것도 아닐 가능성이 높은데, 그때 필요한 건 명령어가 아니라 **어느 자리에 무엇이 있는지에 대한 감각**이기 때문이다.

| 개념 | Hermes | Claude Code |
|---|---|---|
| 절차적 지식 주입 | `~/.hermes/skills/*/SKILL.md` | `.claude/skills/*/SKILL.md` |
| 폴더 규칙 | `AGENTS.md` | `CLAUDE.md` |
| 외부 도구 연결 | `mcp_servers:` (config.yaml) | `.mcp.json` · `claude mcp add` |
| 도구 실행 직전 가로채기 | `hooks.pre_tool_call` | `PreToolUse` 훅 |
| 종료 직전 가로채기 | `hooks.pre_verify` | `Stop` 훅 |
| 승인 판정 | `hermes approvals test` | `permissions.allow/ask/deny` |
| 스케줄 실행 | 내장 `hermes cron` | OS cron + `claude -p` |
| 변화 없을 때 억제 | `--monitor-script` 해시 비교 | 직접 만드는 해시 게이트 |
| 실행 간 상태 | 잡 `notepad` | 직접 만드는 `state.json` |
| 세션을 넘는 기억 | `MEMORY.md` / `USER.md` | `CLAUDE.md` (프로젝트 기억) |
| 발자국 관측 | `hermes journey --json` | `~/.claude/projects/*/*.jsonl` |
| 문맥 격리 | (없음) | 서브에이전트 `.claude/agents/` |
| 구조화 출력 | (프롬프트로 유도) | `--json-schema` |
| 비용 상한 | (없음) | `--max-budget-usd` |

빈칸이 있다는 것에 주목한다. 도구는 서로를 완전히 대체하지 않는다. Hermes에는 스케줄러가 내장돼 있고 Claude Code에는 없다. 대신 Claude Code에는 문맥 격리와 구조화 출력이 있고 Hermes에는 없다. **없는 것은 직접 만들면 된다** — 실제로 `C3-1`부터 `C3-3`까지가 Hermes의 내장 스케줄러에 해당하는 것을 셸 스크립트 40줄로 만드는 과정이다. 그리고 그 40줄을 직접 써 보면 내장 스케줄러가 무엇을 대신 해 주고 있었는지가 비로소 보인다.

### 전체 목록

@@INDEX@@

---

## 실습 0. 준비 — 설치하고, 첫 대화를 하고, 무엇이 오가는지 숫자로 본다

## C0-1. Claude Code를 설치하고 살아 있는지 확인한다

> 대응 | 준비 단계 (모든 모듈의 선행)
> 소요 | 10분
> 선행 | 없음
> 확인 | 버전 출력과 자체 진단 · 모델 호출 없음

### 무엇을

Claude Code를 설치하고, 설치가 온전한지 **자체 진단**으로 확인한다.

### 왜

에이전트 실습에서 가장 흔한 좌절은 "개념이 어려워서"가 아니라 "환경이 안 잡혀서"다. 먼저 진단 도구부터 손에 익혀 두면, 뒤에서 뭔가 안 될 때 어디를 봐야 하는지 알게 된다. 이건 모듈 2에서 말한 **관측 가능성(observability)** 의 가장 작은 형태다. 에이전트는 층이 많은 시스템이고, 층이 많은 시스템에서 제일 먼저 배워야 할 것은 "지금 어느 층이 고장 났는지 묻는 법"이다.

### 해보기

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

설치가 끝나면 새 터미널을 열거나 셸 설정을 다시 읽는다. 그다음 두 명령을 친다.

```bash
claude --version
claude doctor
```

`claude doctor` 는 모델을 부르지 않는다. 설치 경로·플랫폼·자동 업데이트 상태만 확인하는 로컬 점검이다. 그래서 **돈이 들지 않고, 인터넷이 느려도 즉시 끝난다.** 뒤에서 뭔가 이상할 때 가장 먼저 칠 명령이다.

로그인은 한 번만 하면 된다. 아직 안 했다면 `claude` 를 그냥 실행해 안내를 따른다.

```bash
claude
```

### 기대 결과

`claude --version` 은 이런 한 줄을 낸다.

```
2.1.259 (Claude Code)
```

`claude doctor` 는 이런 표를 낸다.

```
Claude Code doctor

Running: native (2.1.259)
Commit: 9b549c8d1c72
Platform: linux-x64
Path: /home/ccc/.local/share/claude/versions/2.1.259
Config install method: native
Search: OK (bundled)
Auto-updates: enabled
Auto-update channel: latest
Last update attempt: success → 2.1.259 (2026-09-03)

No installation issues found.
```

**반드시 확인할 것**은 `Running: native (…)` 줄이 나오는 것이다. 버전 번호와 경로는 설치 시점과 계정에 따라 다르다.

마지막 줄이 `No installation issues found.` 가 아니라 `3 warnings found` 로 나올 수도 있다. **그것도 정상일 수 있다.** 가장 흔한 경고는 이것이다.

```
- Native installation exists but ~/.local/bin is not in your PATH
  Fix: Run: echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
```

이 경고는 "지금은 돌지만 새 터미널에서는 `claude` 를 못 찾을 수 있다"는 뜻이다. 안내대로 고치고 새 터미널을 열면 사라진다. **경고를 읽는 연습이 이 실습의 목적**이다 — `doctor` 는 고장을 알려 주는 게 아니라 고장의 위치를 알려 준다.

### 막히면

| 증상 | 원인 | 조치 |
|---|---|---|
| `claude: command not found` | PATH에 아직 안 잡혔다 | 새 터미널을 열거나 `source ~/.bashrc` |
| `Not logged in · Please run /login` | 로그인 안 됨 | `claude` 를 실행해 안내를 따른다 |
| 회사·학교 프록시에서 설치 실패 | HTTPS 차단 | 네트워크 관리자에게 `claude.ai` 허용 요청 |

### 이어지는 곳

`C0-2`에서 이 설치 위에 첫 프로젝트 폴더를 만들고, 실제로 모델을 한 번 부른다. 이 실습편의 나머지 스물두 개는 전부 그 폴더 안에서 일어난다.

---

## C0-2. 프로젝트 폴더를 만들고, 첫 대화에서 오가는 것을 숫자로 본다

> 대응 | 준비 단계 · 모듈 3(비용)의 예고
> 소요 | 15분
> 선행 | C0-1
> 확인 | 응답 1회 · 모델 호출 1회 (haiku, 약 2초, 0.01달러 미만)

### 무엇을

실습용 프로젝트 폴더를 만들고, 비대화 모드로 첫 질문을 던진 뒤, **그 한 번에 무엇이 오갔는지를 JSON으로 열어 본다.**

### 왜

대부분의 사람은 에이전트를 채팅창으로만 만난다. 채팅창은 결과만 보여 주고 과정을 숨긴다. 이 실습은 처음부터 **덮개를 열고 시작한다.** 토큰이 몇 개 갔고, 캐시가 얼마나 재사용됐고, 몇 초가 걸렸고, 얼마가 들었는지를 첫 명령부터 보는 습관을 들인다.

이 습관이 왜 중요한가. 모듈 3에서 다룰 비용 문제는 전부 이 숫자에서 나온다. 밤새 도는 루프가 파산하는 이유는 "응답 한 번이 비싸서"가 아니라 "응답 한 번마다 문맥 전체가 다시 올라가서"인데, 그건 `cache_read_input_tokens` 라는 필드를 보기 전에는 절대 실감이 안 난다.

### 해보기

```bash
mkdir -p ~/cc-lab && cd ~/cc-lab
```

먼저 가장 단순한 형태로 한 번 부른다.

```bash
claude -p "에이전트와 챗봇의 차이를 두 문장으로 설명해줘." --model haiku
```

이제 같은 질문을 **덮개를 열고** 다시 부른다.

```bash
claude -p "에이전트와 챗봇의 차이를 두 문장으로 설명해줘." --model haiku --output-format json \
  | python3 -c "
import sys, json
d = json.load(sys.stdin)
u = d['usage']
print('세션    :', d['session_id'])
print('모델    :', list(d['modelUsage'])[0])
print('입력    :', u['input_tokens'], '토큰')
print('캐시읽기:', u['cache_read_input_tokens'], '토큰')
print('캐시생성:', u['cache_creation_input_tokens'], '토큰')
print('출력    :', u['output_tokens'], '토큰 (그중 생각:', u['output_tokens_details']['thinking_tokens'], ')')
print('시간    :', round(d['duration_ms']/1000, 1), '초')
print('비용    : \$', round(d['total_cost_usd'], 5))
print('턴 수   :', d['num_turns'])
print()
print(d['result'])
"
```

### 기대 결과

첫 명령은 평범한 문단 두 개를 낸다. 두 번째 명령은 이런 모양을 낸다.

```
세션    : a9824a38-90d3-4e2c-88f2-ce0a79e2844d
모델    : claude-haiku-4-5-20251001
입력    : 10 토큰
캐시읽기: 13615 토큰
캐시생성: 7032 토큰
출력    : 51 토큰 (그중 생각: 40 )
시간    : 1.9 초
비용    : $ 0.01666
턴 수   : 1

에이전트는 목표를 받아 스스로 도구를 골라 여러 단계를 실행하고, 챗봇은 ...
```

**반드시 확인할 것**은 세 가지다.

1. `입력` 은 10 토큰인데 `캐시읽기` 는 1만 3천 토큰이다. **내가 친 질문은 10 토큰이고, 나머지 1만 3천 토큰은 도구 설명·시스템 프롬프트·환경 정보다.** 에이전트에게 한마디 거는 비용의 99.9%는 내 말이 아니라 그 말을 이해시키기 위한 준비물이다.
2. `출력` 51 토큰 중 40이 `생각` 이다. 눈에 보이는 답보다 안 보이는 추론이 더 길다.
3. `턴 수` 가 1이다. 도구를 하나도 안 썼다는 뜻이다. `C0-3`에서 이 숫자가 올라가는 것을 본다.

숫자 자체는 매번 다르다. 세션 ID, 정확한 토큰 수, 소수점 이하 비용은 신경 쓰지 않는다. **모양**이 같으면 성공이다.

### 막히면

| 증상 | 원인 | 조치 |
|---|---|---|
| `json.decoder.JSONDecodeError` | 표준 에러가 섞였다 | `2>/dev/null` 을 파이프 앞에 붙인다 |
| `Not logged in` 이 `result` 에 들어옴 | 로그인 만료 | `claude` 실행 후 `/login` |
| 응답이 영어로 온다 | 프롬프트에 한국어 지시가 약함 | "한국어로" 를 덧붙인다 |

### 이어지는 곳

이 폴더 `~/cc-lab` 이 앞으로 스물두 개 실습의 집이다. `C0-3`에서 이 에이전트가 어떤 도구를 들고 있는지, 그리고 도구를 쓰면 위의 숫자가 어떻게 달라지는지 본다. 여기서 처음 본 `total_cost_usd` 필드는 `C3-4`에서 밤새 도는 루프의 예산을 계산하는 데 다시 쓰인다.

---

## C0-3. 이 에이전트가 무엇을 들고 있는지 들여다본다

> 대응 | 모듈 1 · 1~2절, 모듈 2 · 1절
> 소요 | 20분
> 선행 | C0-2
> 확인 | 도구 호출이 스트림에 찍힘 · 모델 호출 1회

### 무엇을

에이전트가 실제로 어떤 **도구**를 골라 쓰는지를 실시간 스트림으로 관찰하고, 도구를 뺏으면 어떻게 되는지 본다.

### 왜

"에이전트는 도구를 쓴다"는 문장은 모듈 1의 첫 줄이지만, 글로 읽으면 추상적이다. 실제로 무엇이 벌어지는지는 `stream-json` 을 한 번 보면 끝난다. 모델이 `tool_use` 를 내보내고 → 하니스가 실행하고 → `tool_result` 가 돌아가고 → 모델이 그걸 읽고 다음을 정한다. 이 네 박자가 에이전트의 전부다.

그리고 `--tools` 로 도구를 뺏어 보면, 모듈 2의 핵심 주장인 **"능력은 모델이 아니라 하니스가 정한다"** 가 한 번에 증명된다. 같은 모델인데 도구가 없으면 아무것도 못 한다.

### 해보기

먼저 도구를 쓸 수밖에 없는 일을 시킨다.

```bash
cd ~/cc-lab
printf 'alpha\nbravo\ncharlie\ndelta\n' > words.txt
```

```bash
claude -p "words.txt 에서 가장 긴 단어와 그 길이를 알려줘." --model haiku \
  --output-format stream-json --verbose 2>/dev/null \
  | python3 -c "
import sys, json
for ln in sys.stdin:
    try: d = json.loads(ln)
    except: continue
    t = d.get('type')
    if t == 'assistant':
        for c in d['message'].get('content', []):
            if c.get('type') == 'tool_use':
                print('▶ 도구 호출:', c['name'], json.dumps(c['input'], ensure_ascii=False)[:90])
    if t == 'user':
        for c in (d['message'].get('content') or []):
            if isinstance(c, dict) and c.get('type') == 'tool_result':
                print('◀ 도구 결과:', str(c.get('content'))[:90].replace(chr(10), ' '))
    if t == 'result':
        print('― 턴 수:', d['num_turns'], '· 비용 \$', round(d['total_cost_usd'], 5))
        print(d['result'][:200])
"
```

이제 **도구를 전부 뺏고** 똑같이 시킨다.

```bash
claude -p "words.txt 에서 가장 긴 단어와 그 길이를 알려줘." --model haiku \
  --tools "" --output-format json 2>/dev/null \
  | python3 -c "
import sys, json
d = json.load(sys.stdin)
print('턴 수:', d['num_turns'])
print(d['result'][:300])
"
```

### 기대 결과

첫 명령은 이런 흐름을 낸다.

```
▶ 도구 호출: Read {"file_path": "/home/you/cc-lab/words.txt"}
◀ 도구 결과:      1→alpha      2→bravo      3→charlie      4→delta
― 턴 수: 2 · 비용 $ 0.0135
가장 긴 단어는 charlie 입니다. 7자입니다.
```

두 번째 명령은 이렇게 나온다.

```
턴 수: 1
words.txt 파일을 읽고 분석하겠습니다.
<function_calls>
<invoke name="read">
<parameter name="path">/home/you/cc-lab/words.txt</parameter>
</invoke>
</function_calls>
...
```

**반드시 확인할 것**은 두 가지다.

1. 첫 명령에서 `▶ 도구 호출` 과 `◀ 도구 결과` 가 짝으로 찍히고 `턴 수` 가 2다. **도구 한 번 = 턴 한 번 = 문맥 전체 재전송 한 번이다.**
2. 두 번째 명령의 `턴 수` 가 1이다. **도구 호출이 한 번도 실제로 일어나지 않았다.**

두 번째 결과를 자세히 보라. 이게 이 실습에서 가장 중요한 관찰이다. 도구를 뺏었더니 모델은 "도구가 없습니다"라고 말하지 않았다. **도구 호출을 흉내 낸 텍스트를 뱉었다.** `<function_calls>` 는 실제 도구 호출이 아니라 그냥 글자다. 아무 파일도 읽히지 않았고, `turn 수`가 1이라는 것이 그 증거다.

여기서 두 가지가 동시에 확인된다.

- **능력은 모델이 아니라 하니스가 정한다.** 같은 모델이 도구가 없으면 아무것도 못 한다.
- **모델은 자기가 무엇을 할 수 있는지 정확히 모른다.** 그래서 도구가 없는데도 도구를 부르려 한다. 도구 목록·권한·훅을 하니스가 관리해야 하는 이유가 이것이다. 모델의 자기 인식을 신뢰할 수 없다.

정확한 문장은 매번 다르다. "파일을 읽을 도구가 없습니다"라고 정직하게 답할 때도 있다. 첫 명령의 도구 이름이 `Read` 대신 `Bash` 로 나올 수도 있다 — 그것도 정상이다. **하니스는 어떤 도구를 줄지만 정하고, 어느 것을 고를지는 모델이 정한다.**

### 막히면

| 증상 | 원인 | 조치 |
|---|---|---|
| `--verbose` 없이 아무것도 안 찍힘 | `stream-json` 은 `--verbose` 가 필요하다 | `--verbose` 를 붙인다 |
| 도구 호출이 안 보이고 바로 답이 나옴 | 파일이 없어 모델이 포기했다 | `words.txt` 를 만들었는지 확인 |
| 권한을 묻고 멈춘다 | 비대화 모드에서 승인자가 없다 | `--permission-mode acceptEdits` 를 붙인다 |

### 이어지는 곳

여기서 본 `tool_use` 스트림이 이 트랙 전체의 관측 장비다. `C1-1`에서는 이 스트림에 `Skill` 이라는 도구가 찍히는 것으로 스킬이 발동했음을 증명하고, `C2-3`에서는 `tool_result` 자리에 훅의 차단 메시지가 들어오는 것을 본다. `C4-2`에서는 이 스트림이 디스크에 쌓인 기록을 통째로 열어 그래프로 만든다.

---
## 실습 1. 스킬과 커넥터 — 모듈 1을 손으로 확인한다

## C1-1. 내 첫 스킬을 만들고, 자동으로 발동하는지 증명한다

> 대응 | 모듈 1 · 2~5절
> 소요 | 30분
> 선행 | C0-3
> 확인 | `Skill` 도구 호출과 고유 마커 · 모델 호출 2회

### 무엇을

`.claude/skills/` 아래에 스킬 파일 하나를 만들고, **내가 스킬을 부르지 않아도 에이전트가 스스로 골라 쓰는지**를 증명한다.

### 왜

모듈 1의 핵심 주장은 "스킬은 프롬프트가 아니라 **필요할 때 로드되는 절차적 지식**"이다. 이 말의 무게는 두 가지가 동시에 확인될 때 실감난다.

1. 내가 "weekly-report 스킬을 써라"고 말하지 **않았는데도** 발동한다 → 발동은 `description` 에 걸린다.
2. 발동했다는 것이 **말이 아니라 기계가 읽을 수 있는 신호**로 남는다 → `stream-json` 에 `Skill` 도구 호출이 찍힌다.

두 번째가 특히 중요하다. "스킬이 먹은 것 같다"는 판단은 믿을 게 못 된다. 모델은 스킬 없이도 그럴듯한 주간 보고서를 쓸 수 있기 때문이다. 그래서 스킬 안에 **모델이 혼자서는 절대 지어내지 않을 마커** `⟪YNC-REPORT-V1⟫` 를 심는다. 마커가 나오면 스킬이 읽힌 것이고, 안 나오면 안 읽힌 것이다. 판정이 취향에 좌우되지 않는다.

이건 모듈 2에서 배울 **검증 가능한 완료 조건**의 축소판이기도 하다. 에이전트를 다룰 때 "됐나?"를 사람 눈으로 판정하기 시작하면 시스템이 커질 수 없다.

### 해보기

```bash
cd ~/cc-lab
mkdir -p .claude/skills/weekly-report
```

```bash
cat > .claude/skills/weekly-report/SKILL.md <<'EOF'
---
name: weekly-report
description: 주간 보고서를 쓸 때 사용한다. 사용자가 "주간 보고", "주간 리포트", "이번 주 정리"를 요청하면 이 스킬을 쓴다.
---

# 주간 보고서 형식

반드시 아래 형식을 그대로 지킨다. 첫 줄은 반드시 마커로 시작한다.

⟪YNC-REPORT-V1⟫
그다음 줄부터 아래 세 절을 순서대로 쓴다.

- `## 이번 주 한 일` — 완료된 것만. 진행 중인 것은 여기 쓰지 않는다.
- `## 다음 주 계획` — 각 항목은 동사로 시작한다.
- `## 막힌 것` — 없으면 반드시 "없음" 이라고 적는다. 빈칸으로 두지 않는다.

## 필수 규칙

- 각 절의 항목은 `- ` 로 시작하는 목록으로만 쓴다.
- 추측을 쓰지 않는다. 사용자가 말하지 않은 것은 적지 않는다.
- 전체 길이는 15줄을 넘기지 않는다.
EOF
```

스킬이 인식됐는지부터 확인한다. 이건 모델을 부르지 않는다.

```bash
ls -l .claude/skills/weekly-report/SKILL.md
head -4 .claude/skills/weekly-report/SKILL.md
```

이제 **스킬 이름을 말하지 않고** 일을 시킨다.

```bash
claude -p "이번 주 주간 보고 써줘. 한 일: 스킬 만들기. 다음 주: 훅 만들기. 막힌 것: 없음. 되묻지 말고 바로 써라." \
  --model haiku --output-format stream-json --verbose 2>/dev/null \
  | python3 -c "
import sys, json
used = False
for ln in sys.stdin:
    try: d = json.loads(ln)
    except: continue
    if d.get('type') == 'assistant':
        for c in d['message'].get('content', []):
            if c.get('type') == 'tool_use' and c['name'] == 'Skill':
                used = True
                print('▶ 스킬 발동:', json.dumps(c['input'], ensure_ascii=False)[:160])
    if d.get('type') == 'result':
        print('스킬 도구 호출:', used)
        print('마커 존재    :', '⟪YNC-REPORT-V1⟫' in d['result'])
        print('---')
        print(d['result'])
"
```

마지막으로 **대조군**을 돌린다. 스킬을 잠시 치우고 같은 질문을 한다.

```bash
mkdir -p .skills-parked
mv .claude/skills/weekly-report .skills-parked/
claude -p "이번 주 주간 보고 써줘. 한 일: 스킬 만들기. 다음 주: 훅 만들기. 막힌 것: 없음. 되묻지 말고 바로 써라." \
  --model haiku --output-format json 2>/dev/null \
  | python3 -c "
import sys, json
d = json.load(sys.stdin)
print('마커 존재:', '⟪YNC-REPORT-V1⟫' in d['result'])
print(d['result'][:200])
"
mv .skills-parked/weekly-report .claude/skills/
```

### 기대 결과

스킬이 있을 때:

```
▶ 스킬 발동: {"skill": "weekly-report", "args": "{\"completed\": \"스킬 만들기\", ...}"}
스킬 도구 호출: True
마커 존재    : True
---
⟪YNC-REPORT-V1⟫
## 이번 주 한 일
- 스킬 만들기

## 다음 주 계획
- 훅 만들기

## 막힌 것
- 없음
```

스킬을 치웠을 때:

```
마커 존재: False
이번 주 주간 보고입니다.

**이번 주 한 일**
- 스킬 만들기
...
```

**반드시 확인할 것**은 이 대비다. 스킬이 없어도 모델은 그럴듯한 보고서를 쓴다. 하지만 마커가 없고, 형식이 매번 다르다. **스킬이 준 것은 능력이 아니라 일관성이다.**

### 놓치기 쉬운 것 — 점을 붙여 숨겨도 스킬은 꺼지지 않는다

위 대조군에서 스킬 폴더를 `.claude/skills/` **밖으로** 옮긴 것에 주의한다. 이 문서를 만들면서 처음에는 폴더 이름 앞에 점을 붙여 `.claude/skills/.weekly-report-off` 로 바꿨다. 유닉스에서 점으로 시작하는 이름은 숨김 파일이니 무시될 것이라고 생각한 것이다.

**발동했다.** 마커가 그대로 나왔다.

스킬은 폴더 이름으로 식별되는 것이 아니라 `SKILL.md` 안의 `name:` 필드로 식별되고, 스킬 탐색은 숨김 폴더도 그대로 훑는다. 폴더 이름을 바꾸는 것은 스킬을 끄는 방법이 아니다. 확실한 방법은 셋이다.

```
# 1) 스킬 트리 밖으로 옮긴다 (한 개만 끈다)
mv .claude/skills/weekly-report .skills-parked/

# 2) 이 세션의 모든 스킬을 끈다
claude -p "<질문>" --disable-slash-commands

# 3) 모든 사용자 설정(스킬·훅·MCP·CLAUDE.md)을 끈다 — 설정이 깨졌을 때 진단용
claude -p "<질문>" --safe-mode
```

세 번째가 특히 유용하다. 뒤의 실습에서 "왜 이렇게 동작하지?" 싶을 때 `--safe-mode` 로 한 번 돌려 보면 그것이 내 설정 때문인지 아닌지 즉시 갈린다.

### 막히면

| 증상 | 원인 | 조치 |
|---|---|---|
| 스킬이 발동 안 함 | `description` 이 발동 조건을 안 담고 있다 | "~할 때 사용한다" 형태로 트리거 단어를 넣는다 |
| 폴더 이름을 바꿨는데도 발동 | 이름이 아니라 `name:` 으로 식별한다 | 트리 밖으로 옮기거나 `--safe-mode` |
| 되묻기만 하고 안 씀 | 프롬프트에 빈칸이 있다 | 세 항목을 다 채워서 시킨다 |
| 마커가 깨져 나옴 | 터미널 인코딩 | `⟪⟫` 대신 `[[YNC-REPORT-V1]]` 로 바꿔도 된다 |
| 폴더 이름과 다른 이름으로 발동 | 스킬 이름은 폴더가 아니라 `name:` 이 정한다 | 둘을 일치시킨다 |

### 이어지는 곳

`C1-2`에서 스킬을 하나 더 만들어 **스킬끼리 서로를 부르게** 하고, 스킬이 쓸 수 있는 도구를 제한한다. 여기서 쓴 "고유 마커로 발동을 증명한다"는 기법은 `C1-2`, `C2-2`, `C5-2`에서 그대로 다시 쓴다. `C2-5`에서는 이 스킬 파일이 **감사 대상**이 된다 — 스킬은 편리한 만큼 공급망 위험이기도 하다.

---

## C1-2. 두 번째 스킬을 만들고, 스킬이 쓸 수 있는 도구를 제한한다

> 대응 | 모듈 1 · 5~7절, 모듈 2 · 4절
> 소요 | 30분
> 선행 | C1-1
> 확인 | 마커 두 종류가 한 세션에 · 모델 호출 2회

### 무엇을

회의록 스킬을 하나 더 만들고, 첫 스킬이 그것을 참조하게 한 뒤, **스킬이 만질 수 있는 도구를 프론트매터로 좁힌다.**

### 왜

스킬 하나는 그냥 템플릿이다. 스킬 **여럿**이 되는 순간 두 가지 새로운 문제가 생기고, 이게 모듈 1 후반부의 내용이다.

**첫째, 어느 것이 발동할지 겹친다.** "이번 주 회의 정리해줘"는 주간 보고인가 회의록인가? 사람은 헷갈리고 모델도 헷갈린다. 해결책은 `description` 을 **배타적으로** 쓰는 것이다. 각 스킬이 "나는 이럴 때 쓰고, 저럴 때는 안 쓴다"를 명시한다.

**둘째, 스킬이 도구를 통해 무엇을 할 수 있는지가 위험이 된다.** 회의록 스킬이 파일을 지울 수 있어야 할 이유가 없다. `allowed-tools` 프론트매터는 **그 스킬이 활성일 동안만** 도구를 좁힌다. 이건 모듈 2의 최소 권한 원칙이 모듈 1의 스킬 층에서 나타난 모습이다.

### 해보기

```bash
cd ~/cc-lab
mkdir -p .claude/skills/meeting-notes
```

```bash
cat > .claude/skills/meeting-notes/SKILL.md <<'EOF'
---
name: meeting-notes
description: 회의 내용을 회의록으로 정리할 때 사용한다. 사용자가 "회의록", "회의 정리", "미팅 노트"를 요청하면 이 스킬을 쓴다. 주간 보고서 작성에는 쓰지 않는다.
allowed-tools: Read, Glob, Grep
---

# 회의록 형식

첫 줄은 반드시 마커로 시작한다.

⟪YNC-MEETING-V1⟫
그다음 아래 세 절을 순서대로 쓴다.

- `## 결정` — 확정된 것만. 각 줄은 평서문 한 문장.
- `## 액션아이템` — `- [담당자] 할 일 (기한)` 형식. 담당자를 모르면 `[미정]`.
- `## 보류` — 결론이 안 난 것. 없으면 "없음".

## 필수 규칙

- 발언을 그대로 옮기지 않는다. 결정과 할 일만 남긴다.
- 파일을 만들거나 고치지 않는다. 이 스킬은 읽기 전용이다.
- 주간 보고서를 요청받았다면 이 스킬을 쓰지 말고 weekly-report 스킬을 쓴다.
EOF
```

첫 스킬에도 관계를 적어 준다.

```bash
cat >> .claude/skills/weekly-report/SKILL.md <<'EOF'

## 관련 스킬

- 회의 내용을 정리해 달라는 요청이면 이 스킬이 아니라 `meeting-notes` 스킬을 쓴다.
- 주간 보고의 "이번 주 한 일" 을 채울 근거가 회의록이라면, 먼저 회의록을 읽고 나서 쓴다.
EOF
```

이제 **한 요청 안에 두 가지 일**을 섞어서 시킨다.

```bash
claude -p "어제 회의 정리하고, 그걸 근거로 주간 보고도 써줘. 회의 내용: 배포는 화요일로 고정하기로 함, 로그 보관은 90일로 늘리기로 함, 담당은 김. 주간 보고의 한 일은 '배포 일정 확정' 하나. 다음 주는 '로그 설정 변경'. 막힌 것 없음. 되묻지 말고 바로 다 써라." \
  --model haiku --output-format stream-json --verbose 2>/dev/null \
  | python3 -c "
import sys, json
skills = []
for ln in sys.stdin:
    try: d = json.loads(ln)
    except: continue
    if d.get('type') == 'assistant':
        for c in d['message'].get('content', []):
            if c.get('type') == 'tool_use' and c['name'] == 'Skill':
                skills.append(json.loads(json.dumps(c['input']))['skill'])
    if d.get('type') == 'result':
        r = d['result']
        print('발동한 스킬 :', skills)
        print('회의록 마커 :', '⟪YNC-MEETING-V1⟫' in r)
        print('주간보고마커:', '⟪YNC-REPORT-V1⟫' in r)
        print('---')
        print(r[:700])
"
```

`allowed-tools` 가 실제로 좁히는지 확인한다.

```bash
claude -p "meeting-notes 스킬을 써서 회의록을 만들고, 그 결과를 notes.md 파일로 저장해줘. 회의 내용: 배포는 화요일로 고정." \
  --model haiku --permission-mode acceptEdits --output-format stream-json --verbose 2>/dev/null \
  | python3 -c "
import sys, json
for ln in sys.stdin:
    try: d = json.loads(ln)
    except: continue
    if d.get('type') == 'assistant':
        for c in d['message'].get('content', []):
            if c.get('type') == 'tool_use': print('▶', c['name'])
    if d.get('type') == 'result': print('---'); print(d['result'][:300])
"
ls notes.md 2>&1 | head -1
```

### 기대 결과

첫 명령:

```
발동한 스킬 : ['meeting-notes', 'weekly-report']
회의록 마커 : False
주간보고마커: True
---
⟪YNC-REPORT-V1⟫
## 이번 주 한 일
- 배포 일정 확정

## 다음 주 계획
- 로그 설정 변경

## 막힌 것
- 없음
```

**반드시 확인할 것**은 `발동한 스킬` 목록에 **두 개가 다 들어 있고, 회의록이 먼저**라는 점이다. 순서가 중요하다 — 주간 보고 스킬에 "근거가 회의록이면 먼저 읽어라"라고 적었기 때문이다. 스킬이 다른 스킬을 부르는 게 아니라, **스킬에 적힌 문장이 모델의 순서를 바꾼다.**

**마커는 둘 다 안 나올 수 있다.** 위 실측에서는 회의록 마커가 사라졌다. 회의록 스킬은 분명히 발동했는데(`발동한 스킬` 목록이 증거다) 최종 답변에는 주간 보고만 남았다.

왜 그런가. **최종 답변은 모델이 마지막에 쓰는 요약이다.** 스킬을 두 번 거치며 만든 중간 산출물이 그 요약에 전부 살아남을 이유가 없다. 모델은 사용자가 "주간 보고도 써줘"라고 한 것을 최종 요청으로 읽고 그것만 남겼다.

이건 버그가 아니라 **에이전트 출력의 근본 성질**이고, 뒤에서 두 번 더 만난다. `C2-5`에서 서브에이전트의 보고가 부모에게 요약되고, `C4-2`에서 화면에 안 보이는 도구 호출이 기록에는 남아 있다. 결론은 하나다.

**화면에 나온 텍스트는 증거가 아니다. 기록과 파일이 증거다.**

그래서 이 실습의 판정 기준을 `발동한 스킬` 목록으로 잡은 것이다. 그건 스트림에서 직접 읽은 도구 호출 기록이라 요약되지 않는다. 산출물을 확실히 받아야 한다면 스킬에 "파일로 써라"를 넣어야 하고, 그게 `C2-5`에서 하는 일이다.

두 번째 명령은 스킬이 활성인 동안 `Write` 가 보이지 않아야 한다. 다만 여기서 결과가 두 갈래로 갈릴 수 있다.

- 모델이 `notes.md` 를 못 만들고 "이 스킬은 읽기 전용"이라고 답한다 → `allowed-tools` 가 먹었다.
- 모델이 스킬을 아예 안 쓰고 그냥 파일을 만든다 → 스킬을 우회한 것이다.

**둘 다 정상적인 관찰 결과다.** 두 번째가 나왔다면 그것이 오히려 교훈이다. `allowed-tools` 는 **그 스킬을 쓰는 동안의** 제한이지, 모델이 스킬을 안 쓰기로 정하는 것까지 막지는 못한다. 진짜로 막으려면 층을 더 내려가야 하고, 그게 `C2-1`의 권한 규칙과 `C2-3`의 훅이다.

### 막히면

| 증상 | 원인 | 조치 |
|---|---|---|
| 스킬 하나만 발동 | 요청이 한 가지 일로 읽혔다 | "그리고", "그걸 근거로" 를 명시한다 |
| 회의록 대신 주간 보고만 | `description` 이 안 겹치게 안 써졌다 | "~에는 쓰지 않는다" 문장을 넣는다 |
| 순서가 반대 | 모델의 판단 | 결과 모양이 맞으면 통과. 순서는 매번 같지 않을 수 있다 |

### 이어지는 곳

`C1-3`에서 스킬이 아니라 **커넥터**를 만든다. 스킬은 "어떻게 하는지"를 가르치고, 커넥터는 "무엇을 만질 수 있는지"를 늘린다. 이 둘의 차이가 모듈 1의 마지막 절이다. 그리고 여기서 본 "스킬이 우회될 수 있다"는 관찰이 `C2-1`에서 권한 층으로 이어진다.

---

## C1-3. 커넥터(MCP 서버)를 직접 만들어 읽기 전용으로 붙인다

> 대응 | 모듈 1 · 8~10절
> 소요 | 40분
> 선행 | C1-2
> 확인 | `claude mcp list` 에 ✔ Connected · 모델 호출 1회

### 무엇을

내 노트 폴더를 읽는 **MCP 서버**를 파이썬 표준 라이브러리만으로 직접 만들고, Claude Code에 붙여, 에이전트가 그 도구를 실제로 부르는 것을 확인한다.

### 왜

스킬은 모델의 **머릿속**을 바꾸고, 커넥터는 모델의 **손**을 늘린다. 모듈 1은 이 둘을 구분하는 데 상당한 분량을 쓴다. 직접 만들어 보면 왜 구분해야 하는지가 명확해진다.

**라이브러리 없이 만드는 이유가 따로 있다.** MCP는 대단한 기술처럼 들리지만 실체는 **줄 단위 JSON-RPC**다. 표준 입력으로 요청이 들어오고 표준 출력으로 응답이 나간다. 프레임워크를 쓰면 이게 보이지 않는다. 60줄을 직접 쓰고 나면 "MCP 서버를 붙인다"는 말이 무섭지 않게 된다. 그리고 수업 중에 `pip install` 이 실패해 30분을 버리는 일도 없다.

**읽기 전용으로 만드는 이유**는 모듈 2의 예고다. 커넥터는 에이전트가 외부에 손을 뻗는 통로이고, 통로는 좁을수록 좋다. 이 서버에는 쓰기 도구가 아예 없고, 폴더 밖 경로 요청은 거부한다. 권한을 나중에 설정으로 막는 것보다 **애초에 없는 것**이 언제나 낫다.

### 해보기

```bash
cd ~/cc-lab
mkdir -p notes
cat > notes/2026-08-01-회의.md <<'EOF'
# 8월 1일 팀 회의
참석: 김, 이, 박
결정: 배포는 매주 화요일로 고정한다.
EOF
cat > notes/2026-08-08-회의.md <<'EOF'
# 8월 8일 팀 회의
참석: 김, 박
결정: 로그 보관 기간을 90일로 늘린다.
EOF
```

서버를 만든다. 표준 라이브러리만 쓴다.

```bash
cat > notes_server.py <<'EOF'
#!/usr/bin/env python3
"""notes-mcp — 읽기 전용 노트 커넥터. 표준 라이브러리만 쓴다."""
import json, os, sys, pathlib

ROOT = pathlib.Path(os.environ.get("NOTES_DIR", "notes")).resolve()

TOOLS = [
    {"name": "list_notes",
     "description": "notes 폴더에 있는 노트 파일 목록을 돌려준다.",
     "inputSchema": {"type": "object", "properties": {}}},
    {"name": "read_note",
     "description": "노트 파일 하나를 읽어 내용을 돌려준다.",
     "inputSchema": {"type": "object",
                     "properties": {"name": {"type": "string", "description": "파일 이름"}},
                     "required": ["name"]}},
]


def call(name, args):
    if name == "list_notes":
        return "\n".join(sorted(p.name for p in ROOT.glob("*.md"))) or "(빈 폴더)"
    if name == "read_note":
        p = (ROOT / args.get("name", "")).resolve()
        if ROOT not in p.parents:              # 경로 탈출 차단
            return "거부: notes 폴더 밖은 읽을 수 없다."
        if not p.is_file():
            return "없는 파일: %s" % args.get("name", "")
        return p.read_text(encoding="utf-8")
    return "알 수 없는 도구: %s" % name


def send(obj):
    # ensure_ascii=False — 한글이 \uXXXX 로 이스케이프되지 않게 한다.
    # JSON-RPC 는 UTF-8 을 그대로 허용하므로 이래야 사람이 읽을 수 있다.
    sys.stdout.write(json.dumps(obj, ensure_ascii=False) + "\n")
    sys.stdout.flush()


for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    req = json.loads(line)
    m, rid = req.get("method"), req.get("id")
    if m == "initialize":
        send({"jsonrpc": "2.0", "id": rid, "result": {
            "protocolVersion": "2024-11-05",
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "notes-mcp", "version": "1.0.0"}}})
    elif m == "tools/list":
        send({"jsonrpc": "2.0", "id": rid, "result": {"tools": TOOLS}})
    elif m == "tools/call":
        p = req.get("params", {})
        send({"jsonrpc": "2.0", "id": rid, "result": {
            "content": [{"type": "text", "text": call(p.get("name"), p.get("arguments") or {})}]}})
    elif rid is not None:
        send({"jsonrpc": "2.0", "id": rid, "error": {"code": -32601, "message": "미구현: %s" % m}})
EOF
```

Claude Code에 붙이기 **전에** 프로토콜만 단독으로 검사한다. 이 단계를 건너뛰면 나중에 "안 붙는다"의 원인이 서버인지 설정인지 알 수 없다.

```bash
printf '%s\n' \
 '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"t","version":"1"}}}' \
 '{"jsonrpc":"2.0","method":"notifications/initialized"}' \
 '{"jsonrpc":"2.0","id":2,"method":"tools/list"}' \
 '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"list_notes","arguments":{}}}' \
 | python3 notes_server.py
```

이제 붙인다. 경로는 절대 경로여야 한다.

```bash
claude mcp add --scope local notes -- python3 "$PWD/notes_server.py"
claude mcp list
```

에이전트에게 그 도구로만 일을 시킨다.

```bash
claude -p "notes 커넥터로 노트를 전부 훑어서, 지금까지 내려진 '결정'만 한 줄씩 뽑아라. 파일 이름도 같이." \
  --model haiku --allowedTools "mcp__notes__list_notes" "mcp__notes__read_note" \
  --output-format stream-json --verbose 2>/dev/null \
  | python3 -c "
import sys, json
for ln in sys.stdin:
    try: d = json.loads(ln)
    except: continue
    if d.get('type') == 'assistant':
        for c in d['message'].get('content', []):
            if c.get('type') == 'tool_use':
                print('▶', c['name'], json.dumps(c['input'], ensure_ascii=False))
    if d.get('type') == 'result': print('---'); print(d['result'][:500])
"
```

경로 탈출이 막히는지도 직접 확인한다. 모델을 거치지 않고 서버에 바로 묻는다.

```bash
printf '%s\n' \
 '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"t","version":"1"}}}' \
 '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"read_note","arguments":{"name":"../.claude/skills/weekly-report/SKILL.md"}}}' \
 | python3 notes_server.py | tail -1
```

### 기대 결과

프로토콜 단독 검사는 JSON 세 줄을 낸다. 세 번째 줄에 노트 두 개의 파일명이 들어 있다.

```
{"jsonrpc": "2.0", "id": 1, "result": {"protocolVersion": "2024-11-05", ... "serverInfo": {"name": "notes-mcp", ...
{"jsonrpc": "2.0", "id": 2, "result": {"tools": [{"name": "list_notes", "description": "notes 폴더에 있는 노트 파일 목록을 돌려준다.", ...
{"jsonrpc": "2.0", "id": 3, "result": {"content": [{"type": "text", "text": "2026-08-01-회의.md\n2026-08-08-회의.md"}]}}
```

한글이 `\uc0dd\uac74` 같은 형태로 보인다면 서버의 `send()` 에서 `ensure_ascii=False` 를 빼먹은 것이다. 프로토콜은 그래도 동작하지만 사람이 읽을 수 없다. 위 코드에 그 인자가 있는 것을 확인한다.

`claude mcp list` 는 이렇게 나온다.

```
Checking MCP server health…

notes: python3 /home/you/cc-lab/notes_server.py - ✔ Connected
```

에이전트 호출은 이런 흐름이다.

```
▶ mcp__notes__list_notes {}
▶ mcp__notes__read_note {"name": "2026-08-01-회의.md"}
▶ mcp__notes__read_note {"name": "2026-08-08-회의.md"}
---
| 파일 | 결정 |
|------|------|
| 2026-08-01-회의.md | 배포는 매주 화요일로 고정한다. |
| 2026-08-08-회의.md | 로그 보관 기간을 90일로 늘린다. |
```

경로 탈출 시도는 이렇게 거부된다.

```
{"jsonrpc": "2.0", "id": 2, "result": {"content": [{"type": "text", "text": "거부: notes 폴더 밖은 읽을 수 없다."}]}}
```

**반드시 확인할 것**은 세 가지다. `✔ Connected`, 도구 이름이 `mcp__notes__` 접두사로 나오는 것, 그리고 거부 메시지. 표의 모양이나 결정 문장의 표현은 매번 다르다.

`▶` 목록 맨 앞에 `ToolSearch` 같은 도구가 하나 더 찍힐 수 있다. 도구가 많을 때 필요한 것만 골라 오는 내부 단계이고, 정상이다.

### 막히면

| 증상 | 원인 | 조치 |
|---|---|---|
| `✘ Failed to connect` | 서버가 예외로 죽었다 | 위의 프로토콜 단독 검사를 먼저 통과시킨다 |
| 상대 경로로 등록해 안 붙음 | 작업 폴더가 다르다 | `"$PWD/notes_server.py"` 처럼 절대 경로로 |
| `⏸ Pending approval` | `.mcp.json` 은 승인이 필요하다 | `--scope local` 로 등록한다 |
| 도구를 안 쓰고 직접 파일을 읽음 | 다른 도구가 열려 있다 | `--allowedTools` 로 두 도구만 남긴다 |
| 서버가 응답 없이 멈춤 | `print()` 로 stdout을 오염시켰다 | 로그는 반드시 `sys.stderr` 로 |

마지막 항목이 MCP 서버를 처음 만들 때 가장 흔한 사고다. **stdout은 프로토콜 전용 통로**다. 디버그 출력을 한 줄이라도 섞으면 클라이언트가 JSON 파싱에 실패해 조용히 끊긴다.

### 이어지는 곳

`C1-4`에서 지금까지 만든 스킬과 커넥터를 **그대로 두고 모델만 바꿔서** 결과가 얼마나 달라지는지 잰다. 이 커넥터는 `C4-3`의 근거 검증기에서 원문 공급자로 다시 쓰이고, `C2-5`의 공급망 감사에서는 **감사 대상**이 된다.

---

## C1-4. 모델을 바꾸면 얼마나 좋아지는지 직접 잰다

> 대응 | 모듈 1 · 11절, 모듈 2 · 2절
> 소요 | 25분
> 선행 | C1-3
> 확인 | 두 모델의 통과율과 비용 비교 · 모델 호출 6회 (haiku 3 + sonnet 3)

### 무엇을

같은 과제를 `haiku` 와 `sonnet` 으로 각각 세 번씩 시키고, **통과율과 비용을 표로 만든다.**

### 왜

"더 좋은 모델을 쓰면 됩니다"는 실무에서 가장 게으른 조언이다. 얼마나 좋아지는지, 얼마나 비싸지는지 재지 않으면 판단이 아니라 취향이다. 이 실습은 그 둘을 같은 표에 올린다.

그리고 이건 모듈 2의 주장을 뒤집어서 확인하는 것이기도 하다. `C0-3`에서 "도구를 뺏으면 좋은 모델도 못 한다"를 봤다. 여기서는 반대로 **"하니스가 같으면 모델 차이는 얼마나 나는가"** 를 본다. 답은 대개 "생각보다 적게, 그러나 특정 종류의 실패에서만 크게"다.

세 번 반복하는 이유는 **한 번은 데이터가 아니기 때문**이다. 같은 모델도 실행마다 다른 답을 낸다. 한 번 돌려 보고 "sonnet이 낫다"고 결론짓는 것이 실무에서 가장 흔한 오판이다.

### 해보기

판정이 사람 눈에 좌우되지 않도록 **채점기부터 만든다.**

```bash
cd ~/cc-lab
mkdir -p bench
cat > bench/grade.py <<'EOF'
#!/usr/bin/env python3
"""모델 답안을 채점한다. LLM을 쓰지 않는다."""
import json, re, sys

ans = sys.stdin.read()
checks = [
    ("마커",       lambda s: s.strip().startswith("⟪YNC-REPORT-V1⟫")),
    ("세 절 모두", lambda s: all(h in s for h in ("## 이번 주 한 일", "## 다음 주 계획", "## 막힌 것"))),
    ("목록 형식",  lambda s: len(re.findall(r"^- ", s, re.M)) >= 3),
    ("15줄 이하",  lambda s: len([l for l in s.strip().split("\n") if l.strip()]) <= 15),
    ("추측 없음",  lambda s: "예상" not in s and "추정" not in s and "것으로 보인" not in s),
]
res = [(n, bool(f(ans))) for n, f in checks]
for n, ok in res:
    print(("  PASS " if ok else "  FAIL ") + n)
print(json.dumps({"passed": sum(1 for _, ok in res if ok), "total": len(res)}))
EOF
```

이제 두 모델을 세 번씩 돌린다. **순서대로 돌린다** — 동시에 돌리면 비교가 아니라 경쟁이 된다.

```bash
cd ~/cc-lab
PROMPT="이번 주 주간 보고 써줘. 한 일: MCP 커넥터 만들기, 스킬 두 개 만들기. 다음 주: 훅 붙이기. 막힌 것: 없음. 되묻지 말고 바로 써라."
: > bench/result.tsv
for M in haiku sonnet; do
  for I in 1 2 3; do
    OUT=$(claude -p "$PROMPT" --model $M --output-format json 2>/dev/null)
    TXT=$(printf '%s' "$OUT" | python3 -c "import sys,json; print(json.load(sys.stdin)['result'])")
    COST=$(printf '%s' "$OUT" | python3 -c "import sys,json; print(round(json.load(sys.stdin)['total_cost_usd'],5))")
    SECS=$(printf '%s' "$OUT" | python3 -c "import sys,json; print(round(json.load(sys.stdin)['duration_ms']/1000,1))")
    echo "── $M #$I  (${SECS}초, \$$COST)"
    SCORE=$(printf '%s' "$TXT" | python3 bench/grade.py)
    printf '%s\n' "$SCORE"
    P=$(printf '%s' "$SCORE" | tail -1 | python3 -c "import sys,json; print(json.load(sys.stdin)['passed'])")
    printf '%s\t%s\t%s\t%s\n' "$M" "$P" "$COST" "$SECS" >> bench/result.tsv
  done
done
```

표로 정리한다.

```bash
python3 - <<'EOF'
import collections
rows = [l.split("\t") for l in open("bench/result.tsv").read().strip().split("\n")]
agg = collections.defaultdict(lambda: [0, 0.0, 0.0, 0])
for m, p, c, s in rows:
    a = agg[m]; a[0] += int(p); a[1] += float(c); a[2] += float(s); a[3] += 1
print("%-8s %-10s %-12s %-8s" % ("모델", "통과(15점)", "합계비용($)", "평균초"))
for m, a in agg.items():
    print("%-8s %-10s %-12s %-8s" % (m, "%d" % a[0], "%.5f" % a[1], "%.1f" % (a[2]/a[3])))
EOF
```

### 기대 결과

각 실행마다 채점표가 찍히고, 마지막에 요약표가 나온다.

```
── haiku #1  (8.4초, $0.0129)
  PASS 마커
  PASS 세 절 모두
  PASS 목록 형식
  PASS 15줄 이하
  PASS 추측 없음
{"passed": 5, "total": 5}
...
모델     통과(15점) 합계비용($)   평균초
haiku    15         0.03971      8.1
sonnet   15         0.09136      5.0
```

**반드시 확인할 것**은 딱 두 가지다.

1. `result.tsv` 에 여섯 줄이 쌓였다.
2. 두 모델의 **합계 비용이 몇 배 차이 나는지**.

위 실측에서는 **두 모델이 똑같이 만점을 받았고, 비용은 1.6~2.3배 차이가 났다**(두 번 돌려 각각 그렇게 나왔다). 그리고 예상과 반대로 sonnet이 더 빨랐다(5.0초 대 8.1초) — 생각 토큰이 짧았기 때문이다. "비싼 모델이 느리다"도 사실이 아니다.

**통과 점수는 실행마다 다르다.** haiku가 하나 틀릴 수도 있고 sonnet이 틀릴 수도 있다. 그 변동 자체가 이 실습의 진짜 결론이다 — **잘 정의된 형식 과제에서는 모델 차이가 작고, 비용 차이는 크다.** 모델을 올려야 하는 지점은 형식이 아니라 판단이 필요한 곳이다.

그리고 위 결과에서 haiku가 만점을 받은 것은 운이 아니다. `C1-1`의 SKILL.md에 "전체 길이는 15줄을 넘기지 않는다", "각 절의 항목은 `- ` 로 시작하는 목록으로만 쓴다"를 명시해 두었기 때문이다. **스킬 문서를 잘 쓰는 것이 모델을 올리는 것보다 싸고 확실하다.** 이걸 확인하고 싶으면 `C1-1`의 SKILL.md에서 `## 필수 규칙` 절을 지우고 다시 돌려 보라.

만약 haiku가 계속 `15줄 이하` 에서 떨어진다면, 그건 모델을 올릴 이유가 아니라 **스킬 문서를 고칠 이유**다. `C1-1`의 SKILL.md로 돌아가 "전체 길이는 15줄을 넘기지 않는다"를 더 앞쪽, 더 강하게 써 보라. 그게 대개 모델을 올리는 것보다 싸고 확실하다.

### 막히면

| 증상 | 원인 | 조치 |
|---|---|---|
| sonnet 호출이 거부됨 | 요금제에 따라 접근이 다르다 | `--model haiku` 두 번으로 대신하고, 프롬프트만 바꿔 비교한다 |
| 비용이 예상보다 큼 | 문맥이 매번 새로 캐시된다 | 정상이다. `cache_creation_input_tokens` 를 확인 |
| 채점기가 전부 FAIL | 스킬이 발동을 안 했다 | `C1-1`을 다시 확인한다 |

### 이어지는 곳

여기서 만든 `bench/grade.py` 는 **LLM을 쓰지 않는 판정기**의 첫 등장이다. 같은 원칙이 `C2-4`의 테스트 게이트, `C4-3`의 근거 검증기, `C5-3`의 수용 기준 게이트에서 계속 돌아온다. 판정자는 판정 대상보다 단순해야 한다.

---
## 실습 2. 하니스 엔지니어링 — 모듈 2를 손으로 확인한다

여기서부터가 이 실습편의 중심이다. 앞의 네 실습은 에이전트에게 **능력을 더하는** 일이었다. 이제부터 다섯 실습은 에이전트에게 **한계를 두는** 일이다.

순서가 이렇게 된 것에 이유가 있다. 능력만 더한 에이전트는 시연에서는 인상적이고 운영에서는 사고를 낸다. 모듈 2의 첫 문장이 "같은 모델이 왜 어떤 날은 성공하고 어떤 날은 테스트를 지워 버리는가"인 이유다. 답은 모델이 아니라 **모델을 감싼 층**에 있다.

다섯 실습은 층을 위에서 아래로 내려간다.

| 실습 | 층 | 누가 판정하는가 |
|---|---|---|
| C2-1 | 권한 규칙 | Claude Code 내장 판정기 |
| C2-2 | 폴더 규칙 (CLAUDE.md) | 모델 자신 |
| C2-3 | 실행 직전 훅 | 내가 쓴 스크립트 |
| C2-4 | 종료 직전 훅 | 내가 쓴 테스트 |
| C2-5 | 감사 | 서브에이전트 + 내가 쓴 스크립트 |

**위로 갈수록 편하고, 아래로 갈수록 확실하다.** C2-2는 문장 세 줄로 끝나지만 모델이 안 지킬 수 있다. C2-3은 스크립트를 써야 하지만 모델이 못 어긴다. 실무에서는 둘을 겹쳐 쓴다.

## C2-1. 권한 사다리를 판정만 시켜 본다 (실행하지 않고)

> 대응 | 모듈 2 · 3~5절
> 소요 | 30분
> 선행 | C1-4
> 확인 | 세 종류의 판정 결과 · 모델 호출 4회

### 무엇을

`allow` / `ask` / `deny` 세 단으로 된 권한 규칙을 프로젝트에 심고, **에이전트가 각 명령에 대해 어떤 판정을 받는지** 확인한다. 실제로 파괴적인 일은 하나도 일어나지 않는다.

### 왜

모듈 2의 승인 사다리는 개념적으로는 간단하다. "어떤 건 그냥 하고, 어떤 건 물어보고, 어떤 건 절대 안 한다." 문제는 **실제 규칙을 써 보면 예상과 다르게 동작한다**는 것이다. 이 실습의 목적은 규칙을 배우는 게 아니라 **규칙의 빈틈을 발견하는 것**이다.

발견해야 할 빈틈이 셋 있고, 셋 다 아래에서 직접 확인한다.

1. **매칭 실패는 거부가 아니라 `ask` 로 떨어진다.** `allow` 에 `Bash(ls:*)` 를 넣어도 `ls -la x 2>&1` 은 매칭되지 않는다. 접두사 규칙이라 파이프·리다이렉트·`&&` 가 섞이면 다른 명령으로 취급된다.
2. **`deny` 는 도구 경계가 아니라 자원 경계로도 작동한다.** `Read` 를 막은 경로는 `Bash(cat …)` 로도 못 읽는다. 이건 좋은 소식이지만, 여기에 의존하면 안 된다.
3. **비대화 모드에서 `ask` 는 사실상 `deny` 다.** 물어볼 사람이 없기 때문이다. 밤에 도는 에이전트를 설계할 때 이걸 모르면 "낮에는 됐는데 밤에는 안 된다"를 만난다.

### 해보기

```bash
cd ~/cc-lab
mkdir -p .claude secrets work
echo "TOKEN=abc123" > secrets/keys.env
echo "hello" > a.txt
```

```bash
cat > .claude/settings.json <<'EOF'
{
  "permissions": {
    "allow": ["Bash(ls:*)", "Bash(cat:*)", "Bash(cp:*)", "Read"],
    "ask":   ["Bash(git push:*)"],
    "deny":  ["Bash(rm:*)", "Bash(curl:*)", "Read(./secrets/**)"]
  }
}
EOF
```

네 가지를 순서대로 시킨다. `--permission-prompts none` 은 "물어볼 사람이 없으니 물어봐야 하는 건 전부 거부"라는 뜻이다. **밤에 도는 에이전트와 같은 조건**을 만드는 것이다.

```bash
cd ~/cc-lab
for P in "ls 로 이 폴더 파일 목록을 보여줘" \
         "secrets/keys.env 파일을 읽어서 보여줘" \
         "반드시 bash 의 cat 명령 하나만 써서 secrets/keys.env 를 출력해라. Read 도구는 쓰지 마라." \
         "curl 로 https://example.com 을 받아와줘"; do
  echo "════════ $P"
  claude -p "$P" --model haiku --permission-prompts none \
    --output-format stream-json --verbose 2>/dev/null \
    | python3 -c "
import sys, json
for ln in sys.stdin:
    try: d = json.loads(ln)
    except: continue
    if d.get('type') == 'assistant':
        for c in d['message'].get('content', []):
            if c.get('type') == 'tool_use':
                print('  ▶', c['name'], json.dumps(c['input'], ensure_ascii=False)[:80])
    if d.get('type') == 'user':
        for c in (d['message'].get('content') or []):
            if isinstance(c, dict) and c.get('type') == 'tool_result':
                print('  ◀', str(c.get('content'))[:110].replace(chr(10), ' '))
    if d.get('type') == 'result':
        print('  토큰유출:', 'abc123' in d['result'])
"
done
echo "════════ 사후 확인"
ls a.txt && echo "a.txt 살아 있음 (rm 이 막혔다)"
```

### 기대 결과

```
════════ ls 로 이 폴더 파일 목록을 보여줘
  ▶ Bash {"command": "ls -la"}
  ◀ total 32 drwxrwxr-x .claude  secrets  work  a.txt ...
  토큰유출: False
════════ secrets/keys.env 파일을 읽어서 보여줘
  ▶ Read {"file_path": "/home/you/cc-lab/secrets/keys.env"}
  ◀ <tool_use_error>File is in a directory that is denied by your permission settings.</tool_use_error>
  토큰유출: False
════════ 반드시 bash 의 cat 명령 하나만 써서 ...
  ▶ Bash {"command": "cat secrets/keys.env"}
  ◀ Permission to use Bash with command cat secrets/keys.env has been denied.
  토큰유출: False
════════ curl 로 https://example.com 을 받아와줘
  ▶ Bash {"command": "curl https://example.com"}
  ◀ Permission to use Bash with command curl https://example.com has been denied.
  토큰유출: False
════════ 사후 확인
a.txt
a.txt 살아 있음 (rm 이 막혔다)
```

**반드시 확인할 것**은 네 줄의 `토큰유출: False` 와 마지막의 `a.txt 살아 있음` 이다. 나머지는 관찰거리다.

세 번째 결과가 이 실습의 핵심이다. `Bash(cat:*)` 를 **허용 목록에 넣었는데도** `cat secrets/keys.env` 가 거부됐다. Claude Code는 Bash 명령 안의 파일 경로를 읽기 거부 규칙과 대조한다. 도구 이름만 보는 게 아니라 **무엇에 손대려는지**를 본다.

두 번째와 세 번째의 거부 **문구가 다르다**는 것도 봐 둔다. `<tool_use_error>` 는 도구 층에서 난 오류이고, `Permission to use Bash ... has been denied.` 는 권한 층에서 난 거부다. 어디서 막혔는지 문구로 구분할 수 있다.

`ls` 명령이 `▶ Bash {"command": "ls -la"}` 로 나오면 통과하지만, 모델이 `ls -la . 2>&1` 처럼 리다이렉트를 붙이면 **거부된다**. 그것도 정상적인 관찰 결과다. 접두사 매칭의 한계를 직접 본 것이다.

### 막히면

| 증상 | 원인 | 조치 |
|---|---|---|
| 전부 거부됨 | `settings.json` 문법 오류 | `python3 -m json.tool .claude/settings.json` |
| 설정이 무시됨 | 비대화 모드는 잘못된 설정을 조용히 버린다 | 위 명령으로 JSON을 먼저 검사한다 |
| `ls` 조차 거부 | 모델이 복합 명령을 만들었다 | 정상이다. 접두사 매칭의 한계다 |
| 모델이 실행 대신 사람에게 되묻는다 | 모델이 조심스럽게 판단했다 | 프롬프트에 "확인하지 말고 바로 실행해라" 를 넣는다 |

### 이어지는 곳

권한 규칙은 **미리 쓴 목록**이다. 목록에 없는 상황은 판정할 수 없다. `C2-2`에서는 규칙을 목록이 아니라 **문장**으로 쓰고(더 유연하지만 덜 확실하다), `C2-3`에서는 **코드**로 쓴다(가장 확실하다). 여기서 만든 `.claude/settings.json` 에 `C2-3`과 `C2-4`가 훅을 덧붙인다.

---

## C2-2. CLAUDE.md로 작업 폴더에 규칙을 심는다

> 대응 | 모듈 2 · 6~7절
> 소요 | 20분
> 선행 | C2-1
> 확인 | `work/` 규칙 준수 · 첫 줄 규칙 준수율 측정 · 모델 호출 5회

### 무엇을

프로젝트 루트에 `CLAUDE.md` 를 두고, **모든 세션이 자동으로 그 규칙을 읽는지** 확인한다. 그리고 그 규칙이 지켜지지 않는 경우도 찾아본다.

### 왜

`C2-1`의 권한 규칙은 "무엇을 만질 수 있는가"를 정한다. 하지만 실무의 규칙 대부분은 그런 모양이 아니다. "커밋 메시지는 한국어로 쓴다", "새 파일은 `work/` 아래에만 만든다", "테스트 없이 코드를 고치지 않는다" — 이런 것들은 도구 목록으로 표현할 수 없다.

`CLAUDE.md` 는 그 자리를 채운다. Hermes의 `AGENTS.md` 와 같은 역할이다. 폴더에 두면 그 폴더에서 시작하는 모든 세션이 자동으로 읽는다. **사람에게 붙는 설정이 아니라 프로젝트에 붙는 설정**이라는 점이 중요하다. 저장소에 커밋하면 팀 전체가 같은 규칙을 공유한다.

그리고 이 실습에는 반드시 확인해야 할 **약점**이 있다. `CLAUDE.md` 는 **문장이지 코드가 아니다.** 모델이 읽고 따르기로 선택하는 것이고, 강제되지 않는다. 문맥이 길어지면 잊고, 지시가 충돌하면 최근 것을 따른다. 이 약점을 눈으로 보는 것이 이 실습의 후반부다.

### 해보기

```bash
cd ~/cc-lab
mkdir -p work
cat > CLAUDE.md <<'EOF'
# 이 폴더의 규칙

## 반드시 지킬 것

1. **모든 답변의 첫 줄은 예외 없이 `⟪YNC-RULES-V1⟫` 로 시작한다.** 한 줄짜리 답변도, 되묻는 답변도, 오류를 알리는 답변도 마찬가지다.
2. 파일을 새로 만들 때는 반드시 `work/` 아래에만 만든다.
3. 답변에 이모지를 쓰지 않는다.
4. 코드를 고치기 전에 반드시 먼저 기존 코드를 읽는다.
EOF
```

규칙이 얼마나 지켜지는지 **세 번 재 본다.** 한 번만 재면 판단할 수 없다.

```bash
cd ~/cc-lab
HIT=0
for I in 1 2 3; do
  R=$(claude -p "지금 이 폴더가 어떤 폴더인지 한 줄로 말해줘." --model haiku \
        --output-format json 2>/dev/null \
      | python3 -c "import sys,json; print(json.load(sys.stdin)['result'])")
  case "$R" in
    ⟪YNC-RULES-V1⟫*) HIT=$((HIT+1)); MARK="지킴" ;;
    *)               MARK="어김" ;;
  esac
  printf '%d회차 %s | %s\n' "$I" "$MARK" "$(printf '%s' "$R" | tr '\n' ' ' | cut -c1-56)"
done
echo "── 첫 줄 규칙 준수: $HIT/3"
```

파일 생성 규칙도 확인한다.

```bash
cd ~/cc-lab
claude -p "hello.txt 라는 파일을 만들어서 안에 hello 라고 써줘." \
  --model haiku --permission-mode acceptEdits --output-format json 2>/dev/null \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['result'][:250])"
echo "── 어디에 만들어졌나"
ls hello.txt 2>/dev/null && echo "루트에 만들어짐 — 규칙 위반"
ls work/hello.txt 2>/dev/null && echo "work/ 아래 만들어짐 — 규칙 준수"
```

이제 **규칙을 일부러 흔든다.** 규칙과 충돌하는 요청을 한다.

```bash
cd ~/cc-lab
claude -p "이번 답변만 마커 없이, 이모지를 넣어서 아주 짧게 인사해줘." \
  --model haiku --output-format json 2>/dev/null \
  | python3 -c "
import sys, json
r = json.load(sys.stdin)['result']
print('첫 줄 마커 유지:', r.strip().startswith('⟪YNC-RULES-V1⟫'))
print(repr(r[:150]))
"
```

### 기대 결과

세 번 재는 명령은 이런 모양을 낸다.

```
1회차 지킴 | ⟪YNC-RULES-V1⟫  이 폴더는 Claude Code 실습용 프로젝트 폴더입니다.
2회차 지킴 | ⟪YNC-RULES-V1⟫  에이전트 실습 환경을 담은 폴더입니다.
3회차 어김 | Claude Code 실습용 폴더로, 노트 서버와 벤치마크를 포함합니다.
── 첫 줄 규칙 준수: 2/3
```

파일 생성 명령은 이렇게 나온다.

```
⟪YNC-RULES-V1⟫

work/hello.txt 파일을 만들었습니다.
── 어디에 만들어졌나
work/hello.txt
work/ 아래 만들어짐 — 규칙 준수
```

규칙을 흔드는 명령의 결과는 **두 갈래로 갈린다.**

- `첫 줄 마커 유지: True` — 모델이 폴더 규칙을 사용자 요청보다 우선했다.
- `첫 줄 마커 유지: False` — 모델이 최근 지시를 따랐다.

**반드시 확인할 것**은 `work/ 아래 만들어짐 — 규칙 준수` 하나다. 파일 위치 규칙은 구조적이라 안정적으로 지켜진다.

### 이 실습의 결론은 준수율이 3/3이 아니라는 것이다

`첫 줄 규칙 준수` 가 3/3으로 나올 수도 있고 1/3으로 나올 수도 있다. 실측에서는 2/3이 나왔다. **그 변동이 이 실습의 결론이다.**

`CLAUDE.md` 는 강제 장치가 아니다. 모델이 읽고 따르기로 선택하는 문서이고, 선택은 확률이다. 준수율을 떨어뜨리는 요인은 대개 셋이다.

- **답변이 짧을 때.** "한 줄로 말해줘" 같은 요청에서 모델은 형식보다 간결함을 택한다. 위 3회차가 그 경우다.
- **문맥이 길 때.** 대화가 길어지면 앞쪽 규칙의 영향력이 줄어든다.
- **사용자 지시와 충돌할 때.** 마지막 실험이 그것이다.

그래서 실무에서는 이렇게 쓴다. **`CLAUDE.md` 에는 "지켜지면 좋은 것"을 쓰고, "반드시 지켜져야 하는 것"은 훅으로 내린다.** 커밋 메시지 어투는 `CLAUDE.md` 에, 테스트 없는 커밋 금지는 훅에. 그 경계를 그을 수 있게 되는 것이 이 실습의 목적이다.

준수율을 올리는 실용적인 방법도 있다. 위 `CLAUDE.md` 에서 규칙을 번호 목록으로 만들고 "예외 없이"를 넣은 것이 그것이다. 규칙을 네 개 이하로 줄이고, 명령문으로 쓰고, 가장 중요한 것을 맨 위에 두면 눈에 띄게 좋아진다. **하지만 100%는 되지 않는다.**

### 막히면

| 증상 | 원인 | 조치 |
|---|---|---|
| 준수율 0/3 | `CLAUDE.md` 가 다른 폴더에 있다 | `cd ~/cc-lab` 과 `ls CLAUDE.md` 확인 |
| 준수율이 1~2/3 | 문장 규칙의 정상 범위다 | 이 실습의 결론이다. 넘어간다 |
| 규칙을 무시함 | 규칙이 길거나 모호하다 | 항목 4개 이하, 명령문으로 |
| 루트에 파일이 생김 | 문장 규칙의 한계 | 정상적인 관찰 결과다 |

### 이어지는 곳

`C2-3`에서 같은 규칙을 **훅으로** 쓴다. "새 파일은 work/ 아래에만"을 문장이 아니라 코드로 만들면 위반이 불가능해진다. 그 차이를 나란히 놓고 보는 것이 하니스 엔지니어링의 핵심 감각이다. 이 `CLAUDE.md` 는 `C4-1`에서 **세션을 넘는 기억**의 저장소로도 쓰인다.

---

## C2-3. 위험한 명령을 막는 훅을 만든다

> 대응 | 모듈 2 · 8~10절
> 소요 | 40분
> 선행 | C2-2
> 확인 | 차단 로그 2줄과 모델의 우회 · 모델 호출 1회

### 무엇을

`PreToolUse` 훅을 만들어 `rm` 명령이 **실행되기 직전에** 가로채고, 차단당한 모델이 스스로 다른 방법을 찾는 것을 관찰한다.

### 왜

`C2-2`의 `CLAUDE.md` 는 부탁이었다. 훅은 부탁이 아니다. 훅은 도구 실행 경로에 **물리적으로 끼어 있는 코드**이고, 모델은 훅을 설득할 수 없다.

여기서 확인할 것이 셋이다.

**첫째, 차단은 실패가 아니다.** 훅이 `exit 2` 로 막으면 그 도구는 실행되지 않고, **표준 에러에 쓴 문장이 모델에게 전달된다.** 모델은 그 문장을 읽고 다른 방법을 찾는다. 즉 훅은 벽이 아니라 **대화**다. 그래서 차단 메시지에 "대신 이렇게 해라"를 써 주면 에이전트가 계속 일할 수 있다.

**둘째, 관측이 남는다.** 훅은 차단하지 않을 때도 로그를 남길 수 있다. 이 로그가 "에이전트가 실제로 무엇을 하려 했는가"의 유일한 기록이다. 모델의 답변은 사후 요약이라 믿을 수 없다.

**셋째, 훅의 실패는 통과가 된다.** 스크립트가 없거나 예외로 죽으면 기본 동작은 "그냥 실행"이다. 보안 게이트를 만들 때는 이걸 반드시 뒤집어야 한다.

### 해보기

```bash
cd ~/cc-lab
mkdir -p .claude/hooks parked
```

```bash
cat > .claude/hooks/guard-bash.sh <<'EOF'
#!/usr/bin/env bash
# PreToolUse 훅: Bash 명령을 실행 직전에 가로챈다.
# 표준 입력으로 JSON 이 들어온다. exit 0 = 통과, exit 2 = 차단.
IN=$(cat)
CMD=$(printf '%s' "$IN" | python3 -c "
import sys, json
try: print(json.load(sys.stdin).get('tool_input', {}).get('command', ''))
except Exception: print('')
")

echo "$(date +%H:%M:%S) BASH: $CMD" >> "$CLAUDE_PROJECT_DIR/.claude/guard.log"

if printf '%s' "$CMD" | grep -qE '(^|[;&|[:space:]])rm([[:space:]]|$)'; then
  echo "BLOCKED-BY-GUARD: rm 은 이 프로젝트에서 금지다. 지우는 대신 parked/ 로 옮겨라." >&2
  exit 2
fi
exit 0
EOF
chmod +x .claude/hooks/guard-bash.sh
```

설정에 훅을 등록한다. `C2-1`의 권한 규칙은 그대로 두고 훅만 덧붙인다.

```bash
cat > .claude/settings.json <<'EOF'
{
  "permissions": {
    "allow": ["Bash(ls:*)", "Bash(cat:*)", "Bash(cp:*)", "Bash(mv:*)", "Read", "Write", "Edit"],
    "deny":  ["Read(./secrets/**)"]
  },
  "hooks": {
    "PreToolUse": [
      { "matcher": "Bash",
        "hooks": [ { "type": "command",
                     "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/guard-bash.sh" } ] }
    ]
  }
}
EOF
python3 -m json.tool .claude/settings.json > /dev/null && echo "settings.json 문법 OK"
```

훅을 **모델 없이 단독으로** 먼저 검사한다. `C1-3`에서 MCP 서버를 단독 검사했던 것과 같은 이유다.

```bash
cd ~/cc-lab
export CLAUDE_PROJECT_DIR="$PWD"
echo '{"tool_name":"Bash","tool_input":{"command":"ls -l"}}' | .claude/hooks/guard-bash.sh; echo "  → exit $? (0 이어야 통과)"
echo '{"tool_name":"Bash","tool_input":{"command":"rm -rf build"}}' | .claude/hooks/guard-bash.sh; echo "  → exit $? (2 이어야 차단)"
```

이제 에이전트에게 파일을 지우라고 시킨다.

```bash
cd ~/cc-lab
: > .claude/guard.log
echo "지울 파일" > junk.txt
claude -p "junk.txt 파일을 삭제해줘." --model haiku --permission-mode acceptEdits \
  --output-format stream-json --verbose 2>/dev/null \
  | python3 -c "
import sys, json
for ln in sys.stdin:
    try: d = json.loads(ln)
    except: continue
    if d.get('type') == 'assistant':
        for c in d['message'].get('content', []):
            if c.get('type') == 'tool_use':
                print('▶', c['name'], json.dumps(c['input'], ensure_ascii=False)[:100])
    if d.get('type') == 'user':
        for c in (d['message'].get('content') or []):
            if isinstance(c, dict) and c.get('type') == 'tool_result':
                print('◀', str(c.get('content'))[:130].replace(chr(10), ' '))
    if d.get('type') == 'result': print('---'); print(d['result'][:200])
"
echo "── junk.txt 는 어디에?"
ls junk.txt 2>/dev/null || echo "  루트에 없음"
ls parked/junk.txt 2>/dev/null && echo "  parked/ 로 옮겨졌다"
echo "── 훅이 본 것 전부"
cat .claude/guard.log
```

### 기대 결과

단독 검사:

```
  → exit 0 (0 이어야 통과)
BLOCKED-BY-GUARD: rm 은 이 프로젝트에서 금지다. 지우는 대신 parked/ 로 옮겨라.
  → exit 2 (2 이어야 차단)
```

에이전트 호출:

```
▶ Bash {"command": "rm -f /home/you/cc-lab/junk.txt", "description": "Delete junk.txt"}
◀ PreToolUse:Bash hook error: [...guard-bash.sh]: BLOCKED-BY-GUARD: rm 은 이 프로젝트에서 금지다. 지우는 대신 parked/ 로 옮겨라.
▶ Bash {"command": "mv /home/you/cc-lab/junk.txt /home/you/cc-lab/parked/"}
◀ (Bash completed with no output)
---
완료했습니다. junk.txt 파일을 parked/ 디렉토리로 이동했습니다.
── junk.txt 는 어디에?
  루트에 없음
  parked/ 로 옮겨졌다
── 훅이 본 것 전부
13:57:57 BASH: ls -la junk.txt 2>&1
13:57:59 BASH: rm junk.txt
13:58:03 BASH: mv junk.txt parked/
```

**반드시 확인할 것**은 `guard.log` 에 **차단된 `rm` 한 줄과 성공한 대안 한 줄이 함께 있는 것**이다. 위 실측에서는 그 앞에 에이전트가 파일 존재를 확인한 `ls` 한 줄이 더 있다. 줄 수는 두 줄에서 네 줄까지 나올 수 있다.

가운데 두 줄이 훅의 전부를 설명한다. `rm junk.txt` 는 에이전트가 원래 하려던 일이고, `mv junk.txt parked/` 는 차단당한 뒤 스스로 찾은 대안이다.

에이전트가 `mv` 대신 파이썬으로 옮길 수도 있다. 차단 한 번과 성공 한 번이 남았으면 통과다.

그리고 **로그의 첫 줄에 주목하라.** `ls -la junk.txt 2>&1` 이 통과했다. `C2-1`에서 이런 복합 명령이 권한 규칙에 매칭되지 않아 거부됐던 것과 대비된다. 여기서는 권한 규칙을 `Bash(ls:*)` 같은 접두사 목록이 아니라 넓게 열어 두고, 위험한 것만 훅으로 좁혔기 때문이다. **목록으로 허용하고 코드로 금지하는 것이 그 반대보다 관리하기 쉽다.**

### 놓치기 쉬운 것 — 훅의 실패는 통과가 된다

방금 만든 훅을 일부러 고장 내고 다시 시켜 보라.

```bash
cd ~/cc-lab
mv .claude/hooks/guard-bash.sh .claude/hooks/guard-bash.sh.bak
echo "다시 지울 파일" > junk2.txt
claude -p "junk2.txt 를 rm 명령으로 삭제해줘." --model haiku --permission-mode acceptEdits \
  --output-format json 2>/dev/null | python3 -c "import sys,json; print(json.load(sys.stdin)['result'][:150])"
ls junk2.txt 2>/dev/null && echo "!! 아직 있음" || echo "!! 지워졌다 — 훅이 없으니 막을 게 없다"
mv .claude/hooks/guard-bash.sh.bak .claude/hooks/guard-bash.sh
```

스크립트를 치우면 `junk2.txt` 는 지워진다. **보안 게이트를 만들 때는 "훅이 없으면 차단"을 스크립트 바깥에서 보장해야 한다.** 훅 스크립트 자신은 자기가 없을 때를 대비할 수 없다. 실무에서는 설정 파일을 저장소에 커밋하고 CI에서 존재를 검사한다.

### 막히면

| 증상 | 원인 | 조치 |
|---|---|---|
| 훅이 안 불림 | `matcher` 가 도구 이름과 안 맞는다 | `"matcher": "Bash"` 확인 |
| `Permission denied` | 실행 권한 없음 | `chmod +x` |
| `$CLAUDE_PROJECT_DIR` 이 빈 값 | 단독 실행 시엔 직접 넣어야 한다 | `export CLAUDE_PROJECT_DIR="$PWD"` |
| 차단 메시지가 모델에 안 감 | `>&2` 없이 stdout 으로 썼다 | 차단 사유는 반드시 표준 에러로 |
| 로그가 안 쌓임 | 경로가 상대 경로다 | `$CLAUDE_PROJECT_DIR` 를 붙인다 |

### 이어지는 곳

훅이 끼어드는 자리는 도구 실행 직전만이 아니다. `C2-4`에서 **에이전트가 일을 끝내려는 순간**에 끼어드는 훅을 만든다. 같은 기법으로 자리만 바꾼 것인데, 효과는 전혀 다르다. 여기서 만든 `guard.log` 는 `C2-5`의 감사에서 증거로 쓰인다.

:::diagram
id: cc-hook-points
원본: (신규 작도)
제목: 한 턴 안에서 훅이 끼어드는 자리
내용: 요청→도구선택→실행→반영→종료 흐름 위의 PreToolUse·PostToolUse·Stop 지점
:::

---

## C2-4. 테스트가 통과할 때까지 끝내지 못하게 하는 게이트를 만든다

> 대응 | 모듈 2 · 11~12절, 모듈 3 · 6절
> 소요 | 40분
> 선행 | C2-3
> 확인 | 게이트 로그에 실패→성공 두 줄 · 모델 호출 1회 (내부 2턴)

### 무엇을

`Stop` 훅을 만들어, **에이전트가 "다 했다"고 끝내려는 순간에 테스트를 돌리고, 실패하면 끝내지 못하게** 한다.

### 왜

에이전트의 가장 위험한 실패는 틀리는 것이 아니라 **틀린 채로 성공을 보고하는 것**이다. "수정 완료했습니다"라는 문장은 무료다. 모델은 자기가 한 일을 검증할 동기가 없고, 요약하는 습관만 있다.

`Stop` 훅은 이 문제에 정확히 대응한다. **완료 판정을 모델에게서 빼앗아 코드에게 준다.** 모델이 끝내겠다고 선언하면 훅이 테스트를 돌린다. 통과하면 끝나고, 실패하면 실패 내용과 함께 "아직 아니다"가 모델에게 돌아간다.

여기서 함정이 하나 있고, 반드시 다뤄야 한다. **테스트가 영원히 통과할 수 없으면 에이전트는 영원히 돈다.** 이 문서를 쓰면서 처음 만든 게이트는 `pytest` 가 설치되어 있지 않은 환경에서 무한 재시도에 빠졌다. 테스트가 실패하는 이유가 코드가 아니라 환경이었기 때문에 모델이 아무리 고쳐도 통과할 수 없었다. **게이트에는 반드시 상한이 있어야 한다.**

### 해보기

고쳐야 할 코드와 테스트를 만든다. 외부 라이브러리를 쓰지 않는다 — 위에서 말한 함정을 피하기 위해서다.

```bash
cd ~/cc-lab
mkdir -p work/slug && cd work/slug
cat > slugify.py <<'EOF'
def slugify(s):
    return s.lower().replace(" ", "-")
EOF
cat > run_tests.py <<'EOF'
import sys
from slugify import slugify

CASES = [("Hello World", "hello-world"), ("  Hello  ", "hello"),
         ("a   b", "a-b"), ("A, B!", "a-b"), ("Hello--World", "hello-world")]
bad = 0
for src, want in CASES:
    got = slugify(src)
    if got != want:
        bad += 1
        print("FAIL  slugify(%r) -> %r  (기대: %r)" % (src, got, want))
print("%d/%d 통과" % (len(CASES) - bad, len(CASES)))
sys.exit(1 if bad else 0)
EOF
python3 run_tests.py; echo "지금 상태: exit $?"
```

게이트 훅을 만든다. **상한을 반드시 넣는다.**

```bash
cd ~/cc-lab/work/slug
mkdir -p .claude/hooks
cat > .claude/hooks/test-gate.sh <<'EOF'
#!/usr/bin/env bash
# Stop 훅: 에이전트가 끝내려 할 때 테스트를 돌린다.
# stdout 에 {"decision":"block","reason":...} 를 내면 끝내지 못한다.
cd "$CLAUDE_PROJECT_DIR" || exit 0

N=$(cat .claude/gate.count 2>/dev/null || echo 0)
OUT=$(python3 run_tests.py 2>&1); RC=$?
echo "$(date +%H:%M:%S) 시도#$N rc=$RC | $(printf '%s' "$OUT" | tail -1)" >> .claude/gate.log

if [ "$RC" -eq 0 ]; then
  echo 0 > .claude/gate.count
  exit 0                       # 통과 — 끝내도 좋다
fi

if [ "$N" -ge 3 ]; then        # ★ 상한. 없으면 영원히 돈다
  echo "$(date +%H:%M:%S) 상한 도달 — 통과시킴" >> .claude/gate.log
  echo 0 > .claude/gate.count
  exit 0
fi

echo $((N + 1)) > .claude/gate.count
printf '%s' "$OUT" | python3 -c "
import json, sys
print(json.dumps({'decision': 'block',
                  'reason': '테스트가 통과하지 않았다. 끝내지 말고 slugify.py 를 고쳐라.\n' + sys.stdin.read()}))
"
EOF
chmod +x .claude/hooks/test-gate.sh
cat > .claude/settings.json <<'EOF'
{
  "hooks": {
    "Stop": [
      { "hooks": [ { "type": "command",
                     "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/test-gate.sh" } ] }
    ]
  }
}
EOF
python3 -m json.tool .claude/settings.json > /dev/null && echo "settings.json 문법 OK"
```

이제 **일부러 부족하게** 시킨다. "앞뒤 공백만 고쳐라"라고 하면 다섯 개 테스트 중 두 개만 통과한다. 게이트가 없으면 에이전트는 거기서 끝낼 것이다.

```bash
cd ~/cc-lab/work/slug
: > .claude/gate.log; rm -f .claude/gate.count
claude -p "slugify.py 에서 앞뒤 공백을 없애는 것만 고쳐라. 그 외에는 절대 건드리지 마라. 그것만 하고 바로 끝내라." \
  --model haiku --permission-mode acceptEdits --output-format json 2>/dev/null \
  | python3 -c "
import sys, json
d = json.load(sys.stdin)
print('턴 수:', d['num_turns'], '· 비용 \$', round(d['total_cost_usd'], 4), '·', round(d['duration_ms']/1000, 1), '초')
print(d['result'][:250])
"
echo "── 게이트가 본 것"
cat .claude/gate.log
echo "── 최종 테스트"
python3 run_tests.py; echo "exit $?"
```

### 기대 결과

```
턴 수: 11 · 비용 $ 0.0721 · 41.7 초
수정 완료. 특수문자 제거 시 하이픈을 보존하도록 했습니다.
── 게이트가 본 것
13:58:27 시도#0 rc=1 | 2/5 통과
13:58:41 시도#1 rc=1 | 4/5 통과
13:58:55 시도#2 rc=0 | 5/5 통과
── 최종 테스트
5/5 통과
exit 0
```

**반드시 확인할 것**은 `gate.log` 의 **점수가 오르는 것**과 **마지막 줄이 `rc=0`** 인 것이다.

- `시도#0 rc=1 | 2/5 통과` — 에이전트가 "시킨 것만 했다"고 끝내려 했고, 게이트가 막았다.
- `시도#1 rc=1 | 4/5 통과` — 고쳤지만 아직 부족했다. 또 막혔다.
- `시도#2 rc=0 | 5/5 통과` — 마침내 통과했고 그때 비로소 끝낼 수 있었다.

줄 수는 두 줄일 수도 있고 네 줄일 수도 있다. 만약 `상한 도달` 이 찍혔다면 게이트가 포기한 것이고, 그때는 테스트 자체가 통과 불가능한지 손으로 확인해야 한다.

그리고 마지막 답변을 다시 읽어 보라. "특수문자 제거 시 하이픈을 보존하도록 했습니다" — **사용자는 "앞뒤 공백만 고쳐라, 그 외에는 절대 건드리지 마라"고 했다.** 그런데 특수문자 처리까지 고쳤다. 완료 조건이 사용자의 말이 아니라 **테스트**였기 때문이다.

이게 모듈 2의 결론이다. **에이전트에게 "무엇을 해라"를 말하는 것보다 "무엇이 참이어야 끝인가"를 말하는 것이 강하다.**

### 막히면

| 증상 | 원인 | 조치 |
|---|---|---|
| 무한히 돈다 | 상한 코드를 빼먹었다 | `N -ge 3` 블록을 확인 |
| 게이트가 한 번도 안 막음 | 모델이 첫 시도에 다 고쳤다 | 프롬프트를 더 좁힌다 ("~만 고쳐라") |
| 훅이 안 불림 | `Stop` 대신 다른 이름을 썼다 | 대소문자까지 정확히 `Stop` |
| `cd` 실패로 조용히 통과 | `CLAUDE_PROJECT_DIR` 이 다르다 | 훅 첫 줄의 `cd ... || exit 0` 를 로그로 확인 |
| 테스트가 환경 문제로 항상 실패 | 외부 라이브러리 의존 | 표준 라이브러리만 쓴다 |

### 이어지는 곳

`C2-5`에서 지금까지 심어 놓은 설정 전부(스킬 2개, MCP 서버 1개, 훅 2개, 권한 규칙, CLAUDE.md)를 **감사 대상**으로 놓고 훑는다. 이 게이트 구조는 `C5-3`에서 **테스트가 아니라 명세의 수용 기준**을 판정하도록 다시 쓰인다.

---

## C2-5. 공급망을 감사한다

> 대응 | 모듈 2 · 13~14절
> 소요 | 30분
> 선행 | C2-4
> 확인 | 인벤토리 목록과 감사 보고 파일 · 모델 호출 1회 (서브에이전트 1개)

### 무엇을

이 프로젝트에 심어 놓은 **모든 확장 지점을 목록으로 뽑고**, 서브에이전트에게 감사 보고서를 쓰게 한다.

### 왜

지금까지 네 실습 동안 우리는 이 폴더에 다음을 심었다.

- 스킬 2개 — 모델의 행동을 바꾸는 문서
- MCP 서버 1개 — 외부 데이터로 나가는 통로
- 훅 2개 — **모든 도구 호출과 종료 시점에 실행되는 임의의 셸 스크립트**
- 권한 규칙 — 무엇을 막고 무엇을 열지
- `CLAUDE.md` — 모든 세션이 자동으로 읽는 문서

세 번째 줄을 다시 읽어 보라. 훅은 **내 컴퓨터에서 조건 없이 실행되는 코드**다. 저장소를 `git clone` 해서 그 폴더에서 에이전트를 켜면, 남이 쓴 셸 스크립트가 내 계정 권한으로 돈다. 스킬 파일도 마찬가지다 — 모델의 행동을 바꾸는 문장이 남의 손에서 온다.

**에이전트의 확장 지점은 전부 공급망이다.** 그리고 공급망 위험의 첫 대응은 대단한 도구가 아니라 **목록**이다. 무엇이 있는지 모르면 무엇이 위험한지도 모른다.

**서브에이전트를 쓰는 이유**가 따로 있다. Hermes 트랙에는 없는 기능이다. 감사자에게는 **읽기 권한만** 주고, 감사 대상인 설정 파일들은 못 고치게 한다. 그리고 감사 과정에서 읽은 수십 개 파일이 주 세션의 문맥을 오염시키지 않는다. 감사자는 자기 문맥에서 일하고 **결론만** 돌려준다. 이게 모듈 4에서 다룰 문맥 격리의 실용적인 첫 사례다.

### 해보기

먼저 **모델 없이** 목록을 뽑는다. 감사는 인벤토리에서 시작한다.

```bash
cd ~/cc-lab
cat > inventory.sh <<'EOF'
#!/usr/bin/env bash
# 이 프로젝트의 모든 에이전트 확장 지점을 훑는다. 모델을 부르지 않는다.
cd "$(dirname "$0")"
echo "════════ 에이전트 확장 지점 인벤토리"
echo
echo "── 폴더 규칙"
ls -1 CLAUDE.md 2>/dev/null || echo "  (없음)"
echo
echo "── 스킬 (모델의 행동을 바꾸는 문서)"
for f in .claude/skills/*/SKILL.md; do
  [ -e "$f" ] || { echo "  (없음)"; break; }
  printf '  %-46s %s\n' "$f" "$(grep -m1 '^name:' "$f" | cut -d' ' -f2-)"
done
echo
echo "── 훅 (조건 없이 실행되는 코드) ★ 가장 위험"
python3 - <<'PY'
import json, os
for p in (".claude/settings.json", ".claude/settings.local.json"):
    if not os.path.exists(p):
        continue
    try:
        h = json.load(open(p)).get("hooks", {})
    except Exception as e:
        print("  %s — 파싱 실패: %s" % (p, e)); continue
    if not h:
        print("  %s — 훅 없음" % p); continue
    for ev, entries in h.items():
        for e in entries:
            for hh in e.get("hooks", []):
                print("  %-14s %s" % (ev, hh.get("command", "?")))
PY
echo
echo "── 훅 스크립트 파일과 권한"
ls -l .claude/hooks/ 2>/dev/null | tail -n +2 || echo "  (없음)"
echo
echo "── 커넥터 (외부로 나가는 통로)"
claude mcp list 2>/dev/null | grep -E '^\S+:' || echo "  (없음)"
echo
echo "── 권한 규칙"
python3 - <<'PY'
import json, os
p = ".claude/settings.json"
if os.path.exists(p):
    pm = json.load(open(p)).get("permissions", {})
    for k in ("allow", "ask", "deny"):
        print("  %-5s %s" % (k, pm.get(k, [])))
PY
echo
echo "── 훅이 실제로 본 것 (증거)"
wc -l .claude/guard.log work/slug/.claude/gate.log 2>/dev/null | head -3 || echo "  (로그 없음)"
EOF
chmod +x inventory.sh
./inventory.sh
```

이제 감사자 서브에이전트를 만든다. 도구를 **읽기와 쓰기 한 곳으로만** 좁힌다.

```bash
cd ~/cc-lab
mkdir -p .claude/agents
cat > .claude/agents/supply-auditor.md <<'EOF'
---
name: supply-auditor
description: 이 프로젝트의 에이전트 확장 지점(스킬·훅·커넥터·권한)을 감사한다. 감사·점검·audit 요청에 쓴다.
tools: Read, Glob, Grep, Write
model: haiku
---

너는 공급망 감사자다. 아래 순서로만 일한다.

1. `CLAUDE.md`, `.claude/**` 아래 모든 파일, `.mcp.json` 을 찾아 읽는다.
2. 각 항목을 아래 네 등급 중 하나로 분류한다.
   - `실행` — 코드가 조건 없이 실행된다 (훅 스크립트)
   - `통로` — 외부로 데이터가 나갈 수 있다 (MCP 서버)
   - `지시` — 모델의 행동을 바꾼다 (스킬, CLAUDE.md)
   - `제한` — 무언가를 막는다 (권한 규칙)
3. 감사 결과를 `work/audit.md` 파일에 쓴다. 형식은 아래와 같다.

       # 공급망 감사 보고

       | 파일 | 등급 | 무엇을 하는가 | 확인해야 할 것 |
       |---|---|---|---|
       | ... | 실행 | ... | ... |

       ⟪YNC-AUDIT-V1⟫ 항목 N개 · 실행 N개 · 통로 N개

4. 마지막 줄의 `⟪YNC-AUDIT-V1⟫` 형식을 정확히 지킨다.

감사 대상 파일을 고치지 마라. `work/audit.md` 하나만 쓴다.
EOF
```

감사를 시킨다.

```bash
cd ~/cc-lab
rm -f work/audit.md
claude -p "supply-auditor 서브에이전트로 이 프로젝트의 확장 지점을 감사하고 work/audit.md 에 보고서를 써라." \
  --model haiku --permission-mode acceptEdits \
  --output-format stream-json --verbose 2>/dev/null \
  | python3 -c "
import sys, json
for ln in sys.stdin:
    try: d = json.loads(ln)
    except: continue
    if d.get('type') == 'assistant':
        for c in d['message'].get('content', []):
            if c.get('type') == 'tool_use':
                nm = c['name']
                extra = c['input'].get('subagent_type', '') if nm == 'Agent' else ''
                print('▶', nm, extra)
    if d.get('type') == 'result':
        print('서브에이전트 수:', d.get('subagent_stats', {}).get('spawned'))
"
echo "── 보고서"
cat work/audit.md 2>/dev/null || echo "  파일이 없다"
echo "── 마커 확인"
grep -c '⟪YNC-AUDIT-V1⟫' work/audit.md 2>/dev/null
```

### 기대 결과

`inventory.sh` 는 이런 목록을 낸다.

```
════════ 에이전트 확장 지점 인벤토리

── 폴더 규칙
CLAUDE.md

── 스킬 (모델의 행동을 바꾸는 문서)
  .claude/skills/meeting-notes/SKILL.md          meeting-notes
  .claude/skills/weekly-report/SKILL.md          weekly-report

── 훅 (조건 없이 실행되는 코드) ★ 가장 위험
  PreToolUse     $CLAUDE_PROJECT_DIR/.claude/hooks/guard-bash.sh

── 훅 스크립트 파일과 권한
-rwxrwxr-x 1 you you  512 Sep  3 13:20 guard-bash.sh

── 커넥터 (외부로 나가는 통로)
notes: python3 /home/you/cc-lab/notes_server.py - ✔ Connected

── 권한 규칙
  allow ['Bash(ls:*)', 'Bash(cat:*)', 'Bash(cp:*)', 'Bash(mv:*)', 'Read', 'Write', 'Edit']
  ask   []
  deny  ['Read(./secrets/**)']

── 훅이 실제로 본 것 (증거)
   2 .claude/guard.log
   2 work/slug/.claude/gate.log
```

감사 호출은 이런 흐름이다.

```
▶ Agent supply-auditor
▶ Glob
▶ Glob
▶ Read
▶ Read
▶ Read
▶ Write
서브에이전트 수: 1
── 보고서
# 공급망 감사 보고

| 파일 | 등급 | 무엇을 하는가 | 확인해야 할 것 |
|---|---|---|---|
| CLAUDE.md | 지시 | 첫 줄 마커, work/ 폴더 규칙, 이모지 금지 | 규칙이 실제로 지켜지는지 |
| .claude/settings.json | 제한 | Bash 허용 목록, secrets/ 읽기 금지 | secrets/ 차단이 완전한지 |
| .claude/settings.json | 실행 | PreToolUse 훅이 Bash 직전에 호출된다 | 모든 Bash 호출에서 작동하는지 |
| .claude/hooks/guard-bash.sh | 실행 | Bash 를 가로채 rm 을 차단하고 로그를 남긴다 | 정규식 우회 가능성 |
| .claude/skills/weekly-report/SKILL.md | 지시 | 보고서 형식을 강제한다 | 형식 외의 지시가 섞여 있는가 |
| .claude/agents/supply-auditor.md | 지시 | 감사자 역할을 정의한다 | 감사 대상을 고치지 않는지 |
...

⟪YNC-AUDIT-V1⟫ 항목 7개 · 실행 2개 · 통로 0개 · 지시 4개 · 제한 1개
── 마커 확인
1
```

**반드시 확인할 것**은 세 가지다.

1. `▶ Agent supply-auditor` 와 `서브에이전트 수: 1` — 감사자가 별도 문맥에서 떴다.
2. `work/audit.md` 파일이 존재하고 `⟪YNC-AUDIT-V1⟫` 를 담고 있다.
3. 인벤토리의 `훅` 항목이 **비어 있지 않다.**

표의 내용, 항목 개수, 등급 분류는 매번 다르다. 개수가 7개가 아니라 5개나 9개일 수 있다.

### 감사자가 놓친 것 — 이게 이 실습의 핵심이다

위 실측 보고서의 마지막 줄을 다시 읽어 보라. **`통로 0개`** 다. 그런데 `inventory.sh` 는 커넥터를 분명히 찾아냈다.

```
── 커넥터 (외부로 나가는 통로)
notes: python3 /home/you/cc-lab/notes_server.py - ✔ Connected
```

같은 프로젝트를 감사했는데 셸 스크립트는 통로 하나를 찾고 서브에이전트는 찾지 못했다. 왜인가.

감사자에게 준 지시는 "`CLAUDE.md`, `.claude/**` 아래 모든 파일, `.mcp.json` 을 찾아 읽는다"였다. 그런데 우리는 `C1-3`에서 커넥터를 `--scope local` 로 등록했다. 그건 프로젝트의 `.mcp.json` 이 아니라 **사용자 홈의 `~/.claude.json` 에 프로젝트별 항목으로** 들어간다. 감사자는 읽으라고 한 파일을 다 읽었고, 그 파일들에 커넥터가 없었을 뿐이다.

세 가지가 여기서 나온다.

1. **감사 범위가 곧 감사 결과다.** 감사자는 거짓말하지 않았다. 물어본 곳만 봤다. 감사 지시를 쓸 때 "어디를 볼 것인가"가 "무엇을 찾을 것인가"보다 중요하다.
2. **에이전트 설정은 여러 곳에 흩어져 있다.** 프로젝트 파일(`.claude/`, `.mcp.json`, `CLAUDE.md`), 사용자 홈(`~/.claude.json`, `~/.claude/`), 그리고 명령줄 인자. 저장소만 감사하면 사용자 홈의 설정은 안 보인다.
3. **그래서 인벤토리 스크립트와 LLM 감사자를 둘 다 써야 한다.** 스크립트는 `claude mcp list` 처럼 **명령을 실행해** 실제 상태를 묻고, LLM 감사자는 **파일 내용을 읽어** 의도를 판단한다. 둘은 서로의 사각지대를 덮는다.

이걸 고쳐 보고 싶으면 감사자 문서의 1번 항목에 한 줄을 더한다.

```
1. ... 그리고 `claude mcp list` 를 실행해 등록된 커넥터를 확인한다.
```

그러려면 감사자의 `tools:` 에 `Bash` 를 줘야 한다. **감사 범위를 넓히려면 감사자의 권한을 넓혀야 하고, 그러면 감사자 자신이 공급망 위험이 된다.** 이 맞교환에서 벗어날 방법은 없다. 결정만 할 수 있다.

### 왜 결과를 파일로 받는가

서브에이전트의 답을 주 세션 화면에서 받으려 하면 **부모가 요약해 버린다.** 실제로 이 실습을 처음 만들 때 감사자가 마커를 정확히 냈는데도 최종 화면에는 마커가 없었다. 부모 에이전트가 자기 말로 다시 쓴 것이다.

이건 버그가 아니라 문맥 격리의 성질이다. 서브에이전트의 출력은 부모에게 **보고**로 들어가고, 부모는 그 보고를 재료로 자기 답을 만든다. 그래서 **서브에이전트의 산출물은 파일로 받아야 한다.** 파일은 요약되지 않는다.

### 막히면

| 증상 | 원인 | 조치 |
|---|---|---|
| 서브에이전트가 안 뜸 | 이름을 안 불러 줬다 | 프롬프트에 `supply-auditor` 를 명시 |
| `work/audit.md` 가 없음 | `tools:` 에 `Write` 가 없다 | 프론트매터에 `Write` 추가 |
| 마커가 없음 | 부모가 요약했다 | 파일을 확인한다. 화면이 아니라 파일이 정답 |
| `claude mcp list` 가 인벤토리에서 비어 있음 | 다른 폴더에서 실행 | `cd ~/cc-lab` 확인 |

### 이어지는 곳

여기까지가 **사람이 시동을 거는** 에이전트다. `C3-1`부터는 사람이 없을 때 스스로 도는 에이전트를 만든다. 그때 지금까지 만든 훅과 권한 규칙이 **유일한 안전장치**가 된다. 밤에는 승인 창을 눌러 줄 사람이 없다.

---
## 실습 3. 루프 엔지니어링 — 모듈 3을 손으로 확인한다

Hermes에는 스케줄러가 내장돼 있다. Claude Code에는 없다. 그래서 이 그룹의 네 실습은 **없는 것을 직접 만드는 과정**이다.

이게 손해가 아니다. 내장 스케줄러를 쓰면 편하지만, 그것이 대신 해 주는 일이 무엇인지 모른 채로 쓰게 된다. 셸 스크립트 40줄로 직접 만들어 보면 스케줄러의 각 기능이 어떤 문제에 대한 답인지가 보인다.

네 실습은 하나의 루프를 네 번에 걸쳐 완성한다.

| 실습 | 더하는 것 | 없으면 생기는 문제 |
|---|---|---|
| C3-1 | 주기적 실행 | 사람이 매번 시동을 걸어야 한다 |
| C3-2 | 변화 감지 게이트 | 아무 일 없는데도 돈이 든다 |
| C3-3 | 실행 간 상태 | 한 일을 또 하거나, 매번 처음부터 한다 |
| C3-4 | 비용 상한 | 아침에 청구서를 보고 놀란다 |

## C3-1. 조용한 하트비트를 만든다 (모델을 부르지 않는 루프)

> 대응 | 모듈 3 · 1~3절
> 소요 | 25분
> 선행 | C2-5
> 확인 | 로그에 틱 3줄 · **모델 호출 0회**

### 무엇을

주기적으로 깨어나 상태를 확인하고 로그를 남기는 루프를 만든다. **모델을 한 번도 부르지 않는다.**

### 왜

자율 에이전트를 만들라고 하면 대부분 첫 줄부터 모델을 부른다. 그게 파산의 시작이다.

루프의 골격은 세 부분이다. **깨어나기 → 볼 것이 있는지 확인하기 → (있으면) 생각하기.** 이 중 앞의 두 개는 모델이 필요 없다. 그리고 실제 운영에서 대부분의 틱은 앞의 두 개에서 끝난다. 받은 편지함이 비어 있고, 파일이 안 바뀌었고, 배포가 없었다.

그래서 **모델 없는 루프부터 만든다.** 이 순서를 지키면 모듈 3의 비용 문제가 자동으로 해결된다. 나중에 모델을 붙일 때 "언제 부를 것인가"가 이미 구조로 정해져 있기 때문이다.

이 실습에서 모델을 부르지 않는다는 것은 곧 **비용이 0원이고 인터넷도 필요 없다**는 뜻이다. 강의실에서 전원이 동시에 돌려도 아무 문제가 없다.

### 해보기

```bash
cd ~/cc-lab
mkdir -p loop inbox
```

한 번의 틱을 담당하는 스크립트를 만든다. 루프와 틱을 분리하는 게 핵심이다 — 그래야 틱 하나만 따로 검사할 수 있다.

```bash
cat > loop/tick.sh <<'EOF'
#!/usr/bin/env bash
# 한 번의 틱. 모델을 부르지 않는다.
cd "$(dirname "$0")/.." || exit 1
TS=$(date '+%Y-%m-%d %H:%M:%S')
N=$(ls -1 inbox/*.txt 2>/dev/null | wc -l | tr -d ' ')

if [ "$N" -eq 0 ]; then
  echo "$TS  틱 · 편지함 비어 있음 · 할 일 없음"      >> loop/heartbeat.log
  exit 0
fi
echo "$TS  틱 · 편지함 $N 통 · 처리 대상 있음"        >> loop/heartbeat.log
exit 10          # 10 = "모델을 불러야 한다" 는 신호
EOF
chmod +x loop/tick.sh
```

루프는 틱을 반복하는 것뿐이다.

```bash
cat > loop/run.sh <<'EOF'
#!/usr/bin/env bash
# loop/run.sh <횟수> <간격초>
COUNT=${1:-3}; INTERVAL=${2:-2}
D="$(dirname "$0")"
for i in $(seq 1 "$COUNT"); do
  "$D/tick.sh"; RC=$?
  echo "  틱 $i/$COUNT → exit $RC"
  [ "$i" -lt "$COUNT" ] && sleep "$INTERVAL"
done
EOF
chmod +x loop/run.sh
```

빈 편지함으로 세 틱을 돌린다.

```bash
cd ~/cc-lab
: > loop/heartbeat.log
./loop/run.sh 3 2
echo "── 로그"
cat loop/heartbeat.log
```

편지함에 한 통 넣고 다시 한 틱.

```bash
cd ~/cc-lab
echo "회의록 정리 부탁합니다" > inbox/001.txt
./loop/tick.sh; echo "exit $? (10 이면 모델을 불러야 한다는 신호)"
tail -1 loop/heartbeat.log
```

실제 운영에서는 OS 스케줄러에 건다. **지금은 등록하지 않는다** — 이 실습편이 끝나기 전에 무언가가 배경에서 돌기 시작하면 뒤의 실습이 헷갈린다. 형태만 확인해 둔다.

```bash
echo "*/5 * * * * $HOME/cc-lab/loop/tick.sh >> $HOME/cc-lab/loop/cron.log 2>&1"
```

### 기대 결과

```
  틱 1/3 → exit 0
  틱 2/3 → exit 0
  틱 3/3 → exit 0
── 로그
2026-09-03 13:30:01  틱 · 편지함 비어 있음 · 할 일 없음
2026-09-03 13:30:03  틱 · 편지함 비어 있음 · 할 일 없음
2026-09-03 13:30:05  틱 · 편지함 비어 있음 · 할 일 없음
```

편지함에 한 통 넣은 뒤:

```
exit 10 (10 이면 모델을 불러야 한다는 신호)
2026-09-03 13:30:12  틱 · 편지함 1 통 · 처리 대상 있음
```

**반드시 확인할 것**은 두 가지다.

1. 로그에 정확히 세 줄이 쌓였고, 시각 간격이 약 2초다.
2. 편지함이 빌 때 `exit 0`, 찰 때 `exit 10`. **종료 코드가 판단을 담고 있다.**

두 번째가 이 실습의 설계 요점이다. 틱 스크립트는 "모델을 부를지"를 **정하지 않고 신호만 낸다.** 부르는 결정은 루프가 한다. 이렇게 층을 나눠 두면 `C3-2`에서 게이트를 끼워 넣을 자리가 이미 있다.

### 막히면

| 증상 | 원인 | 조치 |
|---|---|---|
| `Permission denied` | 실행 권한 없음 | `chmod +x loop/*.sh` |
| 로그가 엉뚱한 곳에 | 상대 경로 | 스크립트 첫 줄의 `cd "$(dirname "$0")/.."` 확인 |
| 간격이 안 지켜짐 | `sleep` 인자 누락 | `./loop/run.sh 3 2` 처럼 둘 다 준다 |
| cron 에서만 안 돌아감 | cron 은 PATH 가 다르다 | 스크립트 안에서 절대 경로를 쓴다 |

### 이어지는 곳

`C3-2`에서 이 틱에 **게이트**를 끼운다. "편지함이 비었나"보다 정교한 질문 — "지난번과 달라졌나" — 을 물어서, 편지함에 편지가 있어도 **이미 처리한 것이면 모델을 부르지 않게** 한다.

---

## C3-2. 변화가 있을 때만 모델을 깨우는 게이트를 만든다

> 대응 | 모듈 3 · 4~6절
> 소요 | 35분
> 선행 | C3-1
> 확인 | 세 틱의 소요 시간 차이 · 모델 호출 2회 (틱 3회 중 2회)

### 무엇을

**관측 결과의 해시**를 저장해 두고, 지난번과 같으면 모델을 부르지 않는 게이트를 만든다. 세 번 돌려서 억제가 실제로 일어나는 것을 초 단위로 확인한다.

### 왜

`C3-1`의 틱은 "편지함이 비었나"만 물었다. 이건 부족하다. 편지가 있는데 **이미 처리한 편지**라면 다시 부를 이유가 없다. 5분마다 도는 루프가 하루에 288번 깨어나고, 그 중 280번은 아무것도 안 달라졌다면, 280번의 모델 호출이 순수한 낭비다.

낭비의 크기를 `C0-2`의 숫자로 환산해 보라. 한 번 호출에 캐시 읽기가 1만 3천 토큰이었다. 280번이면 360만 토큰이다. **응답 한 번의 비용이 아니라, 문맥 한 벌을 올리는 비용이 280번 나가는 것이다.**

해시 비교는 이 문제에 대한 가장 단순한 답이다. Hermes는 `--monitor-script` 로 내장 제공한다. Claude Code에서는 다섯 줄로 만든다. 만들어 보면 왜 "바이트 단위로 정확히 같을 때만 억제"인지도 알게 된다.

### 해보기

```bash
cd ~/cc-lab
```

관측 스크립트를 만든다. **이 출력이 해시의 재료**다.

```bash
cat > loop/observe.sh <<'EOF'
#!/usr/bin/env bash
# 편지함의 현재 상태를 출력한다. 시각·난수를 절대 섞지 않는다.
cd "$(dirname "$0")/.." || exit 1
ls -1 inbox/ 2>/dev/null | sort
EOF
chmod +x loop/observe.sh
```

게이트를 만든다.

```bash
cat > loop/gated-tick.sh <<'EOF'
#!/usr/bin/env bash
# 관측 결과가 지난번과 다를 때만 모델을 부른다.
cd "$(dirname "$0")/.." || exit 1
STAMP=loop/.last-hash
TS=$(date '+%H:%M:%S')

NOW=$(./loop/observe.sh | sha256sum | cut -c1-16)
OLD=$(cat "$STAMP" 2>/dev/null || echo "none")

if [ "$NOW" = "$OLD" ]; then
  echo "$TS  억제 · 해시 $NOW · 모델 호출 없음" >> loop/gate.log
  echo "억제됨 (해시 $NOW)"
  exit 0
fi

echo "$TS  변화 · $OLD → $NOW · 모델 호출" >> loop/gate.log
SUMMARY=$(claude -p "편지함에 다음 파일이 있다. 각 파일이 무슨 요청인지 한 줄씩 요약해라. 파일을 읽어도 된다.

$(./loop/observe.sh)" --model haiku --permission-mode acceptEdits \
  --output-format json 2>/dev/null \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['result'])")

printf '=== %s\n%s\n\n' "$TS" "$SUMMARY" >> loop/digest.md
echo "$NOW" > "$STAMP"
echo "모델 호출함 (해시 $OLD → $NOW)"
EOF
chmod +x loop/gated-tick.sh
```

세 번 돌린다. **가운데 틱만 아무것도 안 바꾼다.**

```bash
cd ~/cc-lab
: > loop/gate.log; : > loop/digest.md; rm -f loop/.last-hash
echo "── 1회차 (최초 관측 — 반드시 부른다)"
S=$(date +%s); ./loop/gated-tick.sh; echo "   ${SECONDS}초 경과: $(( $(date +%s) - S ))초"
echo "── 2회차 (아무것도 안 바꿈 — 억제되어야 한다)"
S=$(date +%s); ./loop/gated-tick.sh; echo "   $(( $(date +%s) - S ))초"
echo "── 3회차 (편지 한 통 추가 — 다시 불러야 한다)"
echo "다음 주 배포 일정 알려주세요" > inbox/002.txt
S=$(date +%s); ./loop/gated-tick.sh; echo "   $(( $(date +%s) - S ))초"
echo "── 게이트 로그"
cat loop/gate.log
echo "── 쌓인 요약"
cat loop/digest.md
```

### 기대 결과

```
── 1회차 (최초 관측 — 반드시 부른다)
모델 호출함 (해시 none → 16618af3967d38be)
   13초
── 2회차 (아무것도 안 바꿈 — 억제되어야 한다)
억제됨 (해시 16618af3967d38be)
   0초
── 3회차 (편지 한 통 추가 — 다시 불러야 한다)
모델 호출함 (해시 16618af3967d38be → 44d03f7b4ca05b33)
   20초
── 게이트 로그
14:00:04  변화 · none → 16618af3967d38be · 모델 호출
14:00:17  억제 · 해시 16618af3967d38be · 모델 호출 없음
14:00:17  변화 · 16618af3967d38be → 44d03f7b4ca05b33 · 모델 호출
── 쌓인 요약
=== 14:00:04
**001.txt**: 회의록 정리 요청

=== 14:00:17
**001.txt**: 회의록 정리를 요청합니다.

**002.txt**: 다음 주 배포 일정 정보를 요청합니다.
```

**반드시 확인할 것**은 **2회차의 소요 시간**이다. 1초 미만이어야 한다. 1회차와 3회차는 모델을 기다리니 십몇 초에서 이십 초가 걸리고, 2회차는 해시 비교만 하고 즉시 끝난다. 이 차이가 곧 절약이다.

그리고 `digest.md` 를 보라. **3회차가 001.txt 를 다시 요약했다.** 1회차에 이미 요약했는데도 그렇다. 게이트는 "부를지 말지"만 정하고 "무엇을 처리할지"는 정하지 않기 때문이다. 그게 `C3-3`이 푸는 문제다.

해시 값은 매번 다르다. 초 단위 시간도 다르다. **모양**이 같으면 성공이다.

### 게이트를 망가뜨리는 법 — 직접 해 보라

관측 스크립트에 시각을 섞으면 어떻게 되는지 확인한다.

```bash
cd ~/cc-lab
cp loop/observe.sh loop/observe.sh.bak
cat > loop/observe.sh <<'EOF'
#!/usr/bin/env bash
cd "$(dirname "$0")/.." || exit 1
echo "관측 시각: $(date '+%H:%M:%S')"     # ← 이 한 줄이 게이트를 죽인다
ls -1 inbox/ 2>/dev/null | sort
EOF
chmod +x loop/observe.sh
./loop/gated-tick.sh
./loop/gated-tick.sh
echo "── 두 번 다 '모델 호출함' 이 나왔다면 게이트가 죽은 것이다"
mv loop/observe.sh.bak loop/observe.sh
```

**관측 스크립트의 출력에 시각·난수·프로세스 ID·정렬되지 않은 목록이 섞이면 매 틱이 '변화'가 되어 절약이 0이 된다.** 이건 흔한 실수다. `ls -l` 을 그대로 쓰면 타임스탬프가 들어가고, `ls` 를 정렬 없이 쓰면 순서가 흔들린다. 위 스크립트에서 `| sort` 를 붙인 것이 그 이유다.

### 막히면

| 증상 | 원인 | 조치 |
|---|---|---|
| 매번 모델을 부름 | 관측 출력이 매번 다르다 | `./loop/observe.sh` 를 두 번 실행해 눈으로 비교 |
| 한 번도 안 부름 | `.last-hash` 가 이미 있다 | `rm -f loop/.last-hash` |
| `sha256sum: command not found` | macOS | `shasum -a 256` 으로 바꾼다 |
| 요약이 비어 있음 | 파일 읽기 권한이 없다 | `--permission-mode acceptEdits` 확인 |

### 이어지는 곳

게이트는 "부를지 말지"를 정한다. 하지만 부른 다음에 **어디까지 했는지**는 아직 아무도 기억하지 않는다. 3회차에서 모델은 편지 두 통을 다시 처음부터 요약했다 — 001.txt는 이미 1회차에 요약했는데도. `C3-3`에서 그 문제를 고친다.

:::diagram
id: cc-gate-effect
원본: (신규 작도)
제목: 게이트가 있을 때와 없을 때
내용: 세 틱의 소요 시간 막대와 억제된 틱이 아낀 문맥 전송량
:::

---

## C3-3. 깨어날 때마다 이어서 하는 루프를 만든다 (상태를 가진 루프)

> 대응 | 모듈 3 · 7~9절
> 소요 | 40분
> 선행 | C3-2
> 확인 | done.md 3줄, 4회차는 무동작 · 모델 호출 3회

### 무엇을

`state.json` 에 **커서**를 두고, 깨어날 때마다 할 일 **하나씩** 처리하고, 다 하면 **스스로 멈추는** 루프를 만든다.

### 왜

`C3-2`의 루프에는 기억이 없다. 편지가 두 통이면 두 통을 다시 처음부터 요약한다. 세 통이 되면 세 통을 다시 한다. 이 루프는 시간이 갈수록 느려지고 비싸진다.

해결책은 **실행 사이에 남는 상태**다. Hermes는 잡마다 `notepad` 를 내장 제공하고, 깨어날 때 프롬프트 앞에 자동으로 붙여 준다. Claude Code에는 없으니 파일로 만든다. 만들어 보면 세 가지를 배운다.

**첫째, 상태는 작아야 한다.** 커서 하나면 된다. 상태에 요약 내용까지 넣으면 그게 다시 문맥이 되어 비용이 돌아온다.

**둘째, 한 번에 하나만 한다.** 편지 열 통을 한 틱에 다 처리하려 하면 문맥이 터지고, 중간에 실패하면 어디까지 했는지 알 수 없다. 하나씩 하면 실패해도 그 하나만 다시 한다.

**셋째, 종료 조건이 있어야 한다.** 이게 가장 자주 빠지는 부분이다. 할 일이 없는데도 계속 깨어나는 에이전트는 **없는 일을 지어낸다.** 모델은 "할 일이 없다"보다 "무언가 그럴듯한 것"을 내놓는 쪽으로 기울기 때문이다.

### 해보기

```bash
cd ~/cc-lab
echo "지난 분기 매출 자료 어디 있나요" > inbox/003.txt
ls -1 inbox/
```

상태를 초기화한다.

```bash
cd ~/cc-lab
python3 - <<'EOF'
import json, os
items = sorted(os.listdir("inbox"))
json.dump({"cursor": 0, "items": items}, open("loop/state.json", "w"),
          ensure_ascii=False, indent=2)
print(json.dumps({"cursor": 0, "items": items}, ensure_ascii=False))
EOF
: > loop/done.md
```

이어하기 틱을 만든다.

```bash
cat > loop/resume-tick.sh <<'EOF'
#!/usr/bin/env bash
# 깨어날 때마다 할 일 하나만 처리하고 커서를 올린다.
cd "$(dirname "$0")/.." || exit 1

READ=$(python3 - <<'PY'
import json
s = json.load(open("loop/state.json"))
c, items = s["cursor"], s["items"]
print("%d\t%d\t%s" % (c, len(items), items[c] if c < len(items) else ""))
PY
)
CUR=$(printf '%s' "$READ" | cut -f1)
TOT=$(printf '%s' "$READ" | cut -f2)
ITEM=$(printf '%s' "$READ" | cut -f3)

if [ -z "$ITEM" ]; then
  echo "할 일 없음 (커서 $CUR / 전체 $TOT) — 아무것도 하지 않고 종료"
  exit 0
fi

echo "처리 중: $ITEM (커서 $CUR → $((CUR+1)))"
ANS=$(claude -p "inbox/$ITEM 파일을 읽고, 그 요청이 무엇인지 한 문장으로만 요약해라. 다른 말은 하지 마라." \
  --model haiku --permission-mode acceptEdits --output-format json 2>/dev/null \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['result'].strip().replace(chr(10),' '))")

printf -- '- %s — %s\n' "$ITEM" "$ANS" >> loop/done.md

python3 - <<'PY'
import json
s = json.load(open("loop/state.json"))
s["cursor"] += 1
json.dump(s, open("loop/state.json", "w"), ensure_ascii=False, indent=2)
PY
EOF
chmod +x loop/resume-tick.sh
```

네 번 깨운다. 편지는 세 통이다.

```bash
cd ~/cc-lab
for I in 1 2 3 4; do
  echo "══ $I 회차"
  ./loop/resume-tick.sh
  echo "   커서: $(python3 -c "import json; print(json.load(open('loop/state.json'))['cursor'])") · done.md $(wc -l < loop/done.md)줄"
done
echo "── 최종 결과"
cat loop/done.md
```

### 기대 결과

```
══ 1 회차
처리 중: 001.txt (커서 0 → 1)
   커서: 1 · done.md 1줄
══ 2 회차
처리 중: 002.txt (커서 1 → 2)
   커서: 2 · done.md 2줄
══ 3 회차
처리 중: 003.txt (커서 2 → 3)
   커서: 3 · done.md 3줄
══ 4 회차
할 일 없음 (커서 3 / 전체 3) — 아무것도 하지 않고 종료
   커서: 3 · done.md 3줄
── 최종 결과
- 001.txt — ⟪YNC-RULES-V1⟫ 회의록을 정리해달라는 요청이다.
- 002.txt — ⟪YNC-RULES-V1⟫  다음 주 배포 일정을 알려달라는 요청.
- 003.txt — ⟪YNC-RULES-V1⟫  지난 분기 매출 자료의 위치를 묻는 요청입니다.
```

요약 앞에 `⟪YNC-RULES-V1⟫` 가 붙어 있는 것에 주목한다. `C2-2`에서 `CLAUDE.md` 에 심은 "모든 답변의 첫 줄은 마커로 시작한다" 규칙이 **루프의 산출물에까지 따라온 것**이다.

이건 버그가 아니지만 실무에서는 문제다. 사람과 대화할 때 유용한 규칙이 자동화 산출물을 오염시킨다. 해결책은 셋이고, 어느 것도 공짜가 아니다.

- 루프의 `claude -p` 에 `--safe-mode` 를 붙여 폴더 규칙을 끈다 (전부 끄므로 거칠다)
- `CLAUDE.md` 규칙을 "사람의 질문에 답할 때"로 한정한다 (문장이라 확실하지 않다)
- 산출물을 후처리해 마커를 지운다 (확실하지만 손이 간다)

**프로젝트 규칙은 프로젝트 전체에 걸리고, "전체"에는 내가 나중에 만들 자동화도 포함된다.**

**반드시 확인할 것**은 네 가지다.

1. 커서가 `0 → 1 → 2 → 3` 으로 한 칸씩만 오른다.
2. `done.md` 가 한 줄씩만 늘어난다.
3. **4회차에서 커서가 3에 멈추고 `done.md` 가 3줄로 유지된다.**
4. 각 회차가 서로 다른 파일을 처리했다.

요약 문장은 매번 다르다. 3번이 이 실습의 핵심이다. 4회차에서 무언가 새로 쓰였다면 **종료 조건이 안 걸린 것**이고, 그건 이 루프를 밤새 돌리면 안 된다는 뜻이다.

### 놓치기 쉬운 것 — 편지가 새로 오면?

지금 구조는 `state.json` 의 `items` 를 처음에 한 번 고정했다. 새 편지가 오면 어떻게 되는지 확인해 보라.

```bash
cd ~/cc-lab
echo "휴가 신청 절차 알려주세요" > inbox/004.txt
./loop/resume-tick.sh
echo "→ 새 편지를 무시했다. items 를 갱신하지 않았기 때문이다."
```

`items` 를 매 틱에 다시 읽게 하면 새 편지를 처리하지만, **이미 처리한 것을 다시 처리하지 않도록** 커서가 아니라 처리 완료 목록으로 관리해야 한다. 커서(위치)와 집합(무엇을 했는지)의 차이다. 실무에서는 거의 항상 집합이 맞다. 이걸 고치는 것이 이 실습의 과제다.

### 막히면

| 증상 | 원인 | 조치 |
|---|---|---|
| 매번 같은 파일 처리 | 커서 증가 코드가 안 돈다 | `loop/state.json` 을 직접 열어 본다 |
| `done.md` 가 한 번에 3줄 | 틱이 반복문을 돌고 있다 | 틱은 하나만 처리해야 한다 |
| 4회차에도 뭔가 씀 | `[ -z "$ITEM" ]` 분기 누락 | 그 블록을 확인 |
| `IndexError` | `items` 가 비었다 | 초기화 스크립트를 다시 돌린다 |

### 이어지는 곳

이제 루프가 주기적으로 돌고, 변화가 있을 때만 모델을 부르고, 어디까지 했는지 기억하고, 다 하면 멈춘다. 남은 것은 **얼마가 드는지**다. `C3-4`에서 여기까지 쓴 비용을 실제 숫자로 뽑고, 상한을 건다.

:::diagram
id: cc-resume-loop
원본: (신규 작도)
제목: 상태를 가진 루프의 네 회차
내용: 커서 이동과 done.md 증가, 4회차의 무동작 종료
:::

---

## C3-4. 지금까지 쓴 비용을 숫자로 보고, 상한을 건다

> 대응 | 모듈 3 · 10~12절
> 소요 | 25분
> 선행 | C3-3
> 확인 | 누적 비용 표와 예산 초과 오류 · 모델 호출 1회

### 무엇을

지금까지 실습에서 실제로 쓴 비용을 **세션 기록에서 긁어 합산**하고, `--max-budget-usd` 로 상한을 걸어 초과가 어떻게 보고되는지 확인한다.

### 왜

모듈 3의 비용 논의는 추상적으로 들리기 쉽다. "문맥이 매번 재전송된다"는 문장은 숫자를 보기 전에는 실감이 안 난다. 이 실습은 **내가 방금 쓴 돈**을 본다.

그리고 상한을 거는 법을 배운다. 이게 밤에 도는 에이전트의 마지막 안전장치다. `C2-3`의 훅은 위험한 **행동**을 막고, `--max-budget-usd` 는 위험한 **지출**을 막는다.

상한에는 중요한 성질이 하나 있고, 직접 확인한다. **예산은 턴 사이에 검사된다.** 그래서 한 턴이 예산을 넘어서면 그 턴은 이미 끝난 뒤에 중단된다. 즉 **상한은 정확한 천장이 아니라 대략의 브레이크다.** 이걸 모르고 "0.002달러로 막았다"고 안심하면 안 된다.

### 해보기

Claude Code는 모든 세션의 기록을 디스크에 남긴다. 거기서 비용을 긁는다. **모델을 부르지 않는다.**

```bash
cd ~/cc-lab
cat > cost.py <<'EOF'
#!/usr/bin/env python3
"""이 프로젝트 폴더의 모든 세션 기록에서 토큰과 비용을 합산한다."""
import json, os, pathlib, sys

slug = str(pathlib.Path.cwd()).replace("/", "-")
root = pathlib.Path.home() / ".claude" / "projects" / slug
if not root.is_dir():
    sys.exit("세션 기록이 없다: %s" % root)

tot = {"세션": 0, "요청": 0, "입력": 0, "캐시읽기": 0, "캐시생성": 0, "출력": 0}
per_model = {}
for f in sorted(root.glob("*.jsonl")):
    tot["세션"] += 1
    for ln in f.open(encoding="utf-8"):
        try:
            d = json.loads(ln)
        except Exception:
            continue
        msg = d.get("message") or {}
        u = msg.get("usage")
        if not isinstance(u, dict):
            continue
        tot["요청"] += 1
        tot["입력"] += u.get("input_tokens", 0)
        tot["캐시읽기"] += u.get("cache_read_input_tokens", 0)
        tot["캐시생성"] += u.get("cache_creation_input_tokens", 0)
        tot["출력"] += u.get("output_tokens", 0)
        m = msg.get("model", "?")
        per_model[m] = per_model.get(m, 0) + 1

print("── 이 폴더에서 지금까지")
for k, v in tot.items():
    print("  %-10s %s" % (k, format(v, ",")))
print("── 모델별 요청 수")
for m, n in sorted(per_model.items(), key=lambda x: -x[1]):
    print("  %-34s %d" % (m, n))
ratio = tot["캐시읽기"] / max(tot["입력"], 1)
print("── 내가 친 말 1토큰당 준비물 %.0f토큰" % ratio)
EOF
python3 cost.py
```

이제 상한을 걸어 본다. 일부러 예산을 아주 작게 준다.

```bash
cd ~/cc-lab
claude -p "1부터 20까지 각 숫자의 약수를 전부 나열하는 표를 아주 자세히 만들어라." \
  --model haiku --max-budget-usd 0.002 --output-format json 2>/dev/null \
  | python3 -c "
import sys, json
d = json.load(sys.stdin)
print('오류 여부   :', d.get('is_error'))
print('중단 이유   :', d.get('subtype'), '/', d.get('terminal_reason'))
print('실제 쓴 비용: \$', d.get('total_cost_usd'))
print('예산        : \$ 0.002')
print('결과        :', d.get('result'))
"
```

### 기대 결과

```
── 이 폴더에서 지금까지
  세션         40
  요청         201
  입력         1,758
  캐시읽기       4,019,361
  캐시생성       332,251
  출력         69,650
── 모델별 요청 수
  claude-haiku-4-5-20251001          189
  claude-sonnet-5                     12
── 내가 친 말 1토큰당 준비물 2286토큰
```

상한 실험:

```
오류 여부   : True
중단 이유   : error_max_budget_usd / budget_exhausted
실제 쓴 비용: $ 0.0209153
예산        : $ 0.002
결과        : None
```

**반드시 확인할 것**은 두 가지다.

1. `캐시읽기` 가 `입력` 보다 **세 자릿수 이상 크다.** 마지막 줄의 비율이 이 실습의 결론이다. 내가 친 말 1토큰마다 천 토큰이 넘는 준비물이 함께 올라간다.
2. 상한 실험에서 `실제 쓴 비용`이 **예산보다 크다.** 예산은 턴 사이에만 검사되기 때문이다.

숫자는 여기까지 실습을 몇 번 돌렸는지에 따라 완전히 다르다. 세션 수가 40이 아니라 15나 80일 수 있다. 위 실측은 준비 실습부터 여기까지 한 번 훑은 결과이고, 총 201회 요청에 캐시 읽기가 400만 토큰을 넘었다. **비율의 크기**와 **상한이 정확하지 않다는 사실**이 확인 대상이다.

### 이걸로 무엇을 계산할 수 있나

`C3-2`의 게이트가 아낀 것을 이제 계산할 수 있다. 5분 주기로 하루 288틱, 그 중 280틱이 억제된다면, 억제되지 않았을 때 추가로 나갈 캐시 읽기는 `280 × (한 호출의 캐시읽기)` 다. 위 출력에서 한 요청당 캐시 읽기 평균은 약 2만(4,019,361 ÷ 201)이므로 **하루 560만 토큰**이다.

게이트 다섯 줄이 그것을 없앤다. 모듈 3이 "루프 엔지니어링"이라는 이름을 갖는 이유가 이 계산에 있다.

### 막히면

| 증상 | 원인 | 조치 |
|---|---|---|
| `세션 기록이 없다` | 다른 폴더에서 실행 | `cd ~/cc-lab` 후 다시 |
| 숫자가 전부 0 | 아직 호출을 안 했다 | `C0-2`부터 다시 확인 |
| 예산 초과가 안 남 | 과제가 너무 짧아 한 턴에 끝났다 | 예산을 더 줄이거나 과제를 늘린다 |
| `result` 가 `None` | 정상이다 | 예산으로 중단되면 결과가 없다 |

### 이어지는 곳

루프가 완성됐다. 하지만 이 루프는 **자기가 무엇을 알아냈는지 기억하지 못한다.** `done.md` 는 사람이 읽는 기록이고, 다음 세션의 에이전트는 그걸 읽지 않는다. `C4-1`부터 그 문제를 다룬다.

---
## 실습 4. 그래프 엔지니어링 — 모듈 4를 손으로 확인한다

## C4-1. 세션이 끝나도 남는 기억을 만든다

> 대응 | 모듈 4 · 1~4절
> 소요 | 30분
> 선행 | C3-4
> 확인 | 새 세션이 이전 사실을 알고 있음 · 모델 호출 4회

### 무엇을

두 종류의 기억을 나란히 놓고 확인한다. **세션 안에서만 사는 기억**(대화 기록)과 **세션을 넘어 사는 기억**(`CLAUDE.md`).

### 왜

모듈 4의 첫 문장은 "에이전트는 잊지만 그래프는 잊지 않는다"다. 이 문장의 무게는 잊는 것을 직접 겪어 봐야 느껴진다.

`-p` 로 부르는 각 호출은 **완전히 새로운 세션**이다. 방금 말한 것을 다음 호출에서 모른다. `--continue` 를 붙이면 이전 대화를 이어받지만, 그건 **같은 폴더의 마지막 대화 하나**일 뿐이다. 대화가 길어지면 압축되고, 압축되면 세부가 사라진다.

진짜로 남기려면 **밖에** 써야 한다. Hermes는 `MEMORY.md` 와 `USER.md` 를 자동으로 관리한다. Claude Code에서는 `CLAUDE.md` 가 그 자리다. 차이가 하나 있다 — Hermes는 무엇을 기억할지 모델이 스스로 정하고, Claude Code에서는 **내가 시킨다.** 어느 쪽이 나은지는 상황에 따라 다르지만, 시키는 쪽이 예측 가능하다.

이 실습에서 확인할 핵심은 **기억의 세 층이 각각 어디까지 사는가**다.

| 층 | 어디에 | 얼마나 사는가 |
|---|---|---|
| 문맥 | 모델의 입력 | 한 턴 |
| 대화 기록 | `~/.claude/projects/.../*.jsonl` | 한 세션 (`--continue` 로 이어짐) |
| 프로젝트 기억 | `CLAUDE.md` | 영구 · 팀 공유 · git 추적 |

### 해보기

먼저 **모른다는 것**을 확인한다.

```bash
cd ~/cc-lab
claude -p "우리 팀 배포 요일이 언제야? 모르면 모른다고만 답해라." --model haiku \
  --output-format json 2>/dev/null | python3 -c "import sys,json; print(json.load(sys.stdin)['result'][:200])"
```

알려 주고, **기록하게 한다.**

```bash
cd ~/cc-lab
claude -p "우리 팀 배포 요일은 매주 화요일이고, 로그 보관 기간은 90일이다. 이 두 사실을 CLAUDE.md 의 맨 끝에 '## 팀 사실' 절을 만들어 항목으로 추가해라. 기존 내용은 지우지 마라." \
  --model haiku --permission-mode acceptEdits --output-format json 2>/dev/null \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['result'][:250])"
echo "── CLAUDE.md 확인"
tail -8 CLAUDE.md
```

**완전히 새로운 세션**에서 다시 묻는다. `--continue` 를 붙이지 않는다.

```bash
cd ~/cc-lab
claude -p "우리 팀 배포 요일이 언제야? 그리고 로그 보관 기간은?" --model haiku \
  --output-format json 2>/dev/null | python3 -c "
import sys, json
r = json.load(sys.stdin)['result']
print('화요일 포함:', '화요일' in r)
print('90일 포함  :', '90' in r)
print(r[:250])
"
```

이제 대비를 만든다. **CLAUDE.md 에 적지 않은 사실**을 말하고, 새 세션에서 물어본다.

```bash
cd ~/cc-lab
claude -p "참고로 우리 팀 스프린트는 3주 단위다. 이건 파일에 적지 말고 그냥 알아 둬라." \
  --model haiku --output-format json 2>/dev/null | python3 -c "import sys,json; print(json.load(sys.stdin)['result'][:120])"

echo "── 같은 대화를 이어서 물으면 (--continue)"
claude -p --continue "스프린트 주기가 몇 주라고 했지?" --model haiku \
  --output-format json 2>/dev/null | python3 -c "
import sys, json; r = json.load(sys.stdin)['result']
print('3주 기억:', '3주' in r or '3 주' in r); print(r[:150])
"

echo "── 새 대화에서 물으면 (--continue 없음)"
claude -p "스프린트 주기가 몇 주라고 했지? 모르면 모른다고만 답해라." --model haiku \
  --output-format json 2>/dev/null | python3 -c "
import sys, json; r = json.load(sys.stdin)['result']
print('3주 기억:', '3주' in r or '3 주' in r); print(r[:200])
"
```

### 기대 결과

첫 질문:

```
⟪YNC-RULES-V1⟫
모릅니다. 팀 배포 요일에 대한 정보가 없습니다.
```

기록 후 `CLAUDE.md` 끝:

```
## 팀 사실

- 배포 요일: 매주 화요일
- 로그 보관 기간: 90일
```

새 세션에서 다시 물으면:

```
화요일 포함: True
90일 포함  : True
⟪YNC-RULES-V1⟫
배포 요일은 매주 화요일이고, 로그 보관 기간은 90일입니다.
```

대비 실험:

```
── 같은 대화를 이어서 물으면 (--continue)
3주 기억: True
⟪YNC-RULES-V1⟫ 3주 단위입니다.
── 새 대화에서 물으면 (--continue 없음)
3주 기억: False
⟪YNC-RULES-V1⟫ 모릅니다.
```

**반드시 확인할 것**은 마지막 두 블록의 대비다. 같은 사실인데 `--continue` 가 있으면 알고 없으면 모른다. 그리고 `CLAUDE.md` 에 적힌 사실은 **아무 옵션 없이도** 안다.

이 대비가 모듈 4의 출발점이다. **기억은 저절로 생기지 않는다. 어딘가에 쓰이는 순간에만 생긴다.**

`--continue` 실험이 `3주 기억: False` 로 나올 수도 있다. 그 폴더의 마지막 세션이 내 예상과 다른 것일 때 그렇다 — 실습을 여러 창에서 돌렸거나, 중간에 다른 명령이 끼었을 때. 그것도 교훈이다. `--continue` 는 "마지막 대화"라는 **암묵적 대상**을 쓰기 때문에 자동화에서는 위험하다. 자동화에는 `--session-id` 로 명시하는 편이 옳다.

### 놓치기 쉬운 것 — 기억은 오염될 수 있다

`CLAUDE.md` 는 **모든 세션이 자동으로 읽는 파일**이고, 동시에 **에이전트가 쓸 수 있는 파일**이다. 이 조합은 편리하지만 위험하다. 에이전트가 잘못된 사실을 적으면 그 뒤 모든 세션이 그것을 믿는다.

```bash
cd ~/cc-lab
grep -n "" CLAUDE.md | tail -6
echo "── 이 파일은 git 으로 추적해야 한다. 누가 무엇을 언제 적었는지 남아야 하기 때문이다."
```

실무에서 `CLAUDE.md` 를 반드시 커밋하는 이유가 이것이다. **기억에는 이력이 필요하다.** 모듈 4에서 다룬 "출처가 딸린 기억"의 가장 소박한 형태가 git 로그다.

### 막히면

| 증상 | 원인 | 조치 |
|---|---|---|
| 새 세션이 못 알아봄 | `CLAUDE.md` 를 다른 폴더에 썼다 | `pwd` 와 파일 위치 확인 |
| 기존 규칙이 지워짐 | 에이전트가 덮어썼다 | "기존 내용은 지우지 마라" 를 명시 |
| `--continue` 가 엉뚱한 대화를 이음 | 그 폴더의 마지막 세션이 다르다 | `--session-id` 로 명시한다 |
| 마커가 사라짐 | `CLAUDE.md` 첫 규칙이 지워졌다 | `git diff` 로 확인 |

### 이어지는 곳

`C4-2`에서 세 층 중 두 번째 — **대화 기록** — 을 통째로 열어 본다. 그 안에는 에이전트가 무엇을 언제 어떤 순서로 했는지가 전부 남아 있다. 그것을 그래프로 만든다.

:::diagram
id: cc-three-memories
원본: (신규 작도)
제목: 기억의 세 층과 각각의 수명
내용: 문맥·대화 기록·프로젝트 기억이 각각 언제까지 사는지
:::

---

## C4-2. 에이전트의 발자국을 그래프로 연다

> 대응 | 모듈 4 · 5~8절
> 소요 | 35분
> 선행 | C4-1
> 확인 | 도구 노드와 전이 간선 목록 · **모델 호출 0회**

### 무엇을

디스크에 쌓인 **모든 세션 기록**을 읽어, 에이전트가 쓴 도구를 **노드**로, 도구에서 도구로 넘어간 순서를 **간선**으로 하는 그래프를 만든다.

### 왜

모듈 4의 그래프는 추상적인 개념처럼 들리지만, 사실 **이미 있는 데이터**다. Claude Code는 모든 세션의 모든 메시지를 JSONL로 남긴다. 그 안에 도구 호출 하나하나가 시각과 함께 들어 있다. Hermes의 `hermes journey --json` 이 보여 주는 것과 같은 것을, Claude Code에서는 내가 만든다.

이 그래프가 왜 쓸모 있는가. 세 가지를 알려 준다.

1. **에이전트가 실제로 무엇을 쓰는가.** 내가 붙여 준 도구 중 안 쓰는 것이 뭔지 보인다. 안 쓰는 도구는 문맥만 차지하는 비용이다.
2. **어떤 순서로 일하는가.** `Read → Edit → Bash` 같은 전이가 자주 보이면 그게 이 프로젝트의 작업 패턴이다.
3. **어디서 헤매는가.** 같은 도구가 연달아 여러 번 나오면(`Grep → Grep → Grep`) 찾지 못하고 있다는 신호다. 그건 문서나 스킬로 고칠 문제다.

모델을 부르지 않는다. **관측은 공짜여야 한다.** 관측에 돈이 들면 아무도 관측하지 않는다.

### 해보기

```bash
cd ~/cc-lab
cat > journey.py <<'EOF'
#!/usr/bin/env python3
"""이 폴더의 세션 기록을 도구 호출 그래프로 만든다. 모델을 부르지 않는다."""
import collections, json, pathlib, sys

slug = str(pathlib.Path.cwd()).replace("/", "-")
root = pathlib.Path.home() / ".claude" / "projects" / slug
if not root.is_dir():
    sys.exit("세션 기록이 없다: %s" % root)

nodes = collections.Counter()
edges = collections.Counter()
per_session = {}

# 파일 이름이 아니라 수정 시각으로 정렬해야 "최근" 이 정말 최근이 된다
for f in sorted(root.glob("*.jsonl"), key=lambda x: x.stat().st_mtime):
    seq = []
    for ln in f.open(encoding="utf-8"):
        try:
            d = json.loads(ln)
        except Exception:
            continue
        msg = d.get("message") or {}
        if d.get("type") != "assistant":
            continue
        for c in msg.get("content") or []:
            if isinstance(c, dict) and c.get("type") == "tool_use":
                seq.append(c["name"])
    if not seq:
        continue
    per_session[f.stem[:8]] = seq
    for name in seq:
        nodes[name] += 1
    for a, b in zip(seq, seq[1:]):
        edges[(a, b)] += 1

if not nodes:
    sys.exit("도구 호출 기록이 없다. 먼저 C0-3 을 돌려 보라.")

print("── 노드 (도구별 호출 횟수)")
w = max(nodes.values())
for name, n in nodes.most_common():
    print("  %-26s %4d  %s" % (name, n, "█" * max(1, round(n * 28 / w))))

print("\n── 간선 (도구 → 도구 전이, 2회 이상)")
for (a, b), n in edges.most_common():
    if n >= 2:
        mark = "  ← 같은 도구 반복 (헤매는 신호)" if a == b else ""
        print("  %-20s → %-20s %3d%s" % (a, b, n, mark))

print("\n── 세션별 발자국 (최근 5개)")
for sid, seq in list(per_session.items())[-5:]:
    trail = " → ".join(seq[:8]) + (" → …" if len(seq) > 8 else "")
    print("  %s  (%d회)  %s" % (sid, len(seq), trail))

print("\n── 요약")
print("  세션 %d개 · 도구 종류 %d개 · 호출 %d회 · 전이 %d종"
      % (len(per_session), len(nodes), sum(nodes.values()), len(edges)))
EOF
python3 journey.py
```

JSON으로도 뽑아 둔다. 다른 도구에 넘기려면 이 형태가 필요하다.

```bash
cd ~/cc-lab
python3 - > journey.json <<'EOF'
import collections, json, pathlib
slug = str(pathlib.Path.cwd()).replace("/", "-")
root = pathlib.Path.home() / ".claude" / "projects" / slug
nodes, edges = collections.Counter(), collections.Counter()
for f in sorted(root.glob("*.jsonl")):
    seq = []
    for ln in f.open(encoding="utf-8"):
        try: d = json.loads(ln)
        except Exception: continue
        if d.get("type") != "assistant": continue
        for c in (d.get("message") or {}).get("content") or []:
            if isinstance(c, dict) and c.get("type") == "tool_use": seq.append(c["name"])
    for n in seq: nodes[n] += 1
    for a, b in zip(seq, seq[1:]): edges[(a, b)] += 1
print(json.dumps({
    "nodes": [{"id": k, "calls": v} for k, v in nodes.most_common()],
    "edges": [{"from": a, "to": b, "count": n} for (a, b), n in edges.most_common()],
}, ensure_ascii=False, indent=2))
EOF
head -20 journey.json
python3 -c "
import json; d = json.load(open('journey.json'))
print('노드', len(d['nodes']), '· 간선', len(d['edges']))
"
```

### 기대 결과

```
── 노드 (도구별 호출 횟수)
  Read                         24  ████████████████████████████
  Bash                         15  ██████████████████
  Skill                        11  █████████████
  Write                         4  █████
  mcp__notes__read_note         2  ██
  Edit                          1  █
  Agent                         1  █
  ToolSearch                    1  █
  mcp__notes__list_notes        1  █

── 간선 (도구 → 도구 전이, 2회 이상)
  Read                 → Read                   6  ← 같은 도구 반복 (헤매는 신호)
  Read                 → Bash                   5
  Bash                 → Read                   4
  Bash                 → Bash                   3  ← 같은 도구 반복 (헤매는 신호)

── 세션별 발자국 (최근 5개)
  a3f19c2e  (3회)  Read → Edit → Bash
  b7c04d18  (1회)  Skill
  c92e5a06  (4회)  Glob → Read → Read → Write
  ...

── 요약
  세션 34개 · 도구 종류 9개 · 호출 60회 · 전이 12종
```

**반드시 확인할 것**은 세 가지다.

1. `노드` 목록에 `Skill` 이 있다 — `C1-1`의 스킬 발동이 기록에 남았다.
2. `노드` 목록에 `mcp__notes__` 로 시작하는 항목이 있다 — `C1-3`의 커넥터 사용이 남았다.
3. `노드` 목록에 `Agent` 가 있다 — `C2-5`의 서브에이전트가 남았다.

**이 세 줄이 앞선 실습 전체의 영수증이다.** 실습을 제대로 했는지 이 목록 하나로 확인된다.

숫자와 순서는 당연히 다르다. `Bash → Bash` 같은 반복이 안 보일 수도 있다.

### 이 그래프에 없는 것

여기서 만든 그래프는 **무엇을 했는지**의 기록이다. 모듈 4가 말하는 그래프는 그보다 한 층 위 — **무엇을 알아냈는지**의 기록이다.

차이를 보라. `Read → Edit → Bash` 는 행동이다. "이 프로젝트의 배포는 화요일이다"는 사실이다. 행동 기록은 자동으로 쌓이지만 사실은 아니다. 사실을 쌓으려면 누군가 **주장과 근거를 짝지어** 저장해야 한다. 그게 `C4-3`이다.

### 막히면

| 증상 | 원인 | 조치 |
|---|---|---|
| `세션 기록이 없다` | 폴더가 다르다 | `cd ~/cc-lab` |
| `도구 호출 기록이 없다` | 도구를 쓴 세션이 없다 | `C0-3`을 다시 돌린다 |
| `Skill` 이 안 보임 | `C1-1`을 안 했다 | 순서대로 돌아간다 |
| 노드가 하나뿐 | 기록 파일이 하나뿐 | 정상이다. 실습을 더 하면 늘어난다 |

### 이어지는 곳

`C4-3`에서 **사실의 그래프**를 만든다. 주장마다 근거를 달고, 근거를 기계가 대조한다. 이게 이 실습편의 마지막 도구이자 가장 중요한 도구다.

---

## C4-3. 근거 없는 주장을 잡아내는 검증기를 만든다

> 대응 | 모듈 4 · 9~12절
> 소요 | 45분
> 선행 | C4-2
> 확인 | PASS와 FAIL 판정이 각각 나옴 · 모델 호출 2회

### 무엇을

에이전트가 요약을 만들 때 **주장마다 원문 인용을 함께** 내게 하고, 그 인용이 원문에 **문자 그대로** 있는지 기계가 대조하게 한다.

### 왜

이 실습편의 마지막이자 가장 중요한 실습이다. 지금까지 만든 모든 안전장치에는 공통된 빈틈이 하나 있었다. **에이전트가 그럴듯한 거짓을 말하는 것은 아무도 막지 못했다.**

- `C2-1`의 권한은 무엇을 만질지만 막는다.
- `C2-3`의 훅은 무엇을 실행할지만 막는다.
- `C2-4`의 테스트 게이트는 코드에만 쓸 수 있다. 요약이나 보고서에는 통과 기준이 없다.

그래서 **주장에 근거를 강제하는 층**이 따로 필요하다. 방법은 단순하다. 주장 한 줄을 낼 때마다 그 근거가 되는 원문 문장을 **그대로 복사해서** 함께 내게 한다. 그리고 그 문장이 원문 안에 있는지 문자열로 대조한다.

**이 검증기에는 LLM이 없다.** 문자열 포함 검사뿐이다. 이게 설계의 핵심이다. LLM으로 근거를 판정하면 그 판정이 다시 검증 대상이 되어 원점으로 돌아간다. **판정자는 판정 대상보다 단순해야 한다.** `C1-4`의 채점기, `C2-4`의 테스트, 그리고 여기 — 세 번 같은 원칙이 나온다.

Claude Code에는 `--json-schema` 가 있어서 이 실습이 특히 깔끔해진다. 주장·근거 쌍을 프롬프트로 부탁하는 게 아니라 **출력 형식으로 강제**한다.

### 해보기

원문을 준비한다. `C1-3`에서 만든 노트에 하나를 더 얹는다.

```bash
cd ~/cc-lab
cat > notes/2026-08-15-회의.md <<'EOF'
# 8월 15일 팀 회의
참석: 김, 이
결정: 배포 자동화 도구는 도입하지 않는다. 당장은 수동 절차를 문서화한다.
보류: 스테이징 환경 분리는 다음 분기에 다시 논의한다.
EOF
cat notes/*.md > source.md
wc -l source.md
```

검증기를 만든다. **LLM을 쓰지 않는다.**

```bash
cat > check_claims.py <<'EOF'
#!/usr/bin/env python3
"""주장마다 딸린 인용이 원문에 문자 그대로 있는지 대조한다. LLM을 쓰지 않는다."""
import json, sys

source = open("source.md", encoding="utf-8").read()
try:
    data = json.load(open(sys.argv[1], encoding="utf-8"))
except Exception as e:
    sys.exit("주장 파일을 읽을 수 없다: %s" % e)

claims = data.get("claims", [])
if not claims:
    sys.exit("주장이 하나도 없다.")

bad = 0
for i, c in enumerate(claims, 1):
    claim = (c.get("claim") or "").strip()
    quote = (c.get("quote") or "").strip()
    if not quote:
        print("FAIL %d · 근거 없음\n     주장: %s" % (i, claim)); bad += 1; continue
    if quote in source:
        print("PASS %d · %s\n     근거: %s" % (i, claim, quote))
    else:
        print("FAIL %d · 원문에 없는 인용\n     주장: %s\n     인용: %s" % (i, claim, quote))
        bad += 1

print("\n%d개 중 %d개 통과 · %d개 실패" % (len(claims), len(claims) - bad, bad))
sys.exit(1 if bad else 0)
EOF
```

**정상 경로**를 돌린다. 출력 형식을 스키마로 강제한다.

```bash
cd ~/cc-lab
SCHEMA='{"type":"object","properties":{"claims":{"type":"array","items":{"type":"object","properties":{"claim":{"type":"string","description":"주장 한 문장"},"quote":{"type":"string","description":"source.md 에서 그대로 복사한 근거 문장"}},"required":["claim","quote"]}}},"required":["claims"]}'

claude -p "source.md 를 읽고, 지금까지 팀이 내린 결정과 보류 사항을 정리해라. 각 항목마다 반드시 source.md 안의 문장을 한 글자도 바꾸지 않고 그대로 복사해서 quote 에 넣어라. 요약하거나 다듬지 마라." \
  --model haiku --output-format json --json-schema "$SCHEMA" 2>/dev/null \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['result'])" > claims.json

python3 -m json.tool --no-ensure-ascii claims.json | head -20
echo "════════ 검증"
python3 check_claims.py claims.json; echo "exit $?"
```

이제 **거짓을 일부러 섞어** 검증기가 잡는지 확인한다. 검증기를 신뢰하려면 검증기가 실패를 잡는 것도 봐야 한다.

```bash
cd ~/cc-lab
python3 - <<'EOF'
import json
d = json.load(open("claims.json"))
d["claims"].append({"claim": "배포 자동화 도구를 다음 주에 도입한다.",
                    "quote": "결정: 배포 자동화 도구를 다음 주에 도입한다."})
d["claims"].append({"claim": "예산이 30% 증액되었다.", "quote": ""})
json.dump(d, open("claims-bad.json", "w"), ensure_ascii=False, indent=2)
print("주장 %d개로 늘렸다 (거짓 1개, 근거 없음 1개)" % len(d["claims"]))
EOF
echo "════════ 검증 (실패해야 정상)"
python3 check_claims.py claims-bad.json; echo "exit $?"
```

### 기대 결과

정상 경로:

```
{
    "claims": [
        {
            "claim": "배포는 매주 화요일로 고정한다",
            "quote": "결정: 배포는 매주 화요일로 고정한다."
        },
...
════════ 검증
PASS 1 · 배포는 매주 화요일로 고정한다
     근거: 결정: 배포는 매주 화요일로 고정한다.
PASS 2 · 로그 보관 기간을 90일로 늘린다
     근거: 결정: 로그 보관 기간을 90일로 늘린다.
PASS 3 · 배포 자동화 도구는 도입하지 않는다
     근거: 결정: 배포 자동화 도구는 도입하지 않는다. 당장은 수동 절차를 문서화한다.
PASS 4 · 스테이징 환경 분리는 다음 분기에 다시 논의한다
     근거: 보류: 스테이징 환경 분리는 다음 분기에 다시 논의한다.

4개 중 4개 통과 · 0개 실패
exit 0
```

거짓을 섞은 경로:

```
════════ 검증 (실패해야 정상)
PASS 1 · 배포는 매주 화요일로 고정한다
...
FAIL 5 · 원문에 없는 인용
     주장: 배포 자동화 도구를 다음 주에 도입한다.
     인용: 결정: 배포 자동화 도구를 다음 주에 도입한다.
FAIL 6 · 근거 없음
     주장: 예산이 30% 증액되었다.

6개 중 4개 통과 · 2개 실패
exit 1
```

**반드시 확인할 것**은 두 개의 종료 코드다. 정상 경로에서 `exit 0`, 거짓 경로에서 `exit 1`. 이 두 숫자가 있으면 이 검증기를 CI에, `C2-4`의 Stop 훅에, cron 루프에 그대로 끼울 수 있다.

주장의 개수와 문장은 매번 다르다. `4개 중 4개 통과` 가 `3개 중 3개` 나 `5개 중 5개` 일 수 있다. 통과 개수가 전체와 같으면 성공이다.

만약 정상 경로에서 하나라도 `FAIL 원문에 없는 인용` 이 나온다면 **그게 이 실습의 진짜 수확이다.** 모델이 "그대로 복사해라"는 지시를 받고도 문장을 다듬은 것이다. 마침표를 빼거나, 공백을 정리하거나, `결정:` 접두사를 떼거나 한다. 이것이 **환각의 가장 흔한 형태**다 — 완전한 창작이 아니라 **미세한 변형**이다. 그리고 사람 눈으로는 절대 안 잡힌다.

### 왜 문자 그대로여야 하는가

"의미가 같으면 되지 않나"라고 생각할 수 있다. 안 된다. 두 가지 이유가 있다.

**첫째, 의미 판정은 다시 LLM이 필요하다.** 그러면 판정자가 판정 대상만큼 복잡해지고, 판정자의 오류를 검증할 방법이 없어진다.

**둘째, 미세한 변형이 의미를 바꾼다.** 위 원문의 "배포 자동화 도구는 도입하지 않는다"에서 "않는다"를 빼면 정반대가 된다. 사람이 요약본만 읽으면 못 잡는다. 문자열 대조는 잡는다.

이 원칙에는 대가가 있다. 인용이 길어지고 요약이 딱딱해진다. **그 대가를 치를 만한 문서와 그렇지 않은 문서를 구분하는 것**이 실무 판단이다. 회의록 요약에는 필요하고, 브레인스토밍 정리에는 과하다.

### 막히면

| 증상 | 원인 | 조치 |
|---|---|---|
| `claims.json` 이 빈 파일 | 스키마가 거부됐다 | `python3 -m json.tool claims.json` 로 확인 |
| 한글이 `\uXXXX` 로 보임 | `json.tool` 의 기본값 | `--no-ensure-ascii` 를 붙인다. 데이터는 정상이다 |
| 전부 FAIL | `source.md` 를 안 만들었다 | `cat notes/*.md > source.md` |
| 인용에 줄바꿈이 섞여 실패 | 여러 줄을 한 인용에 넣었다 | 프롬프트에 "한 문장만" 을 넣는다 |
| 스키마 오류 | 셸이 JSON 을 망가뜨렸다 | `$SCHEMA` 를 반드시 큰따옴표로 감싼다 |

### 이어지는 곳

여기까지가 모듈 1~4의 실습이다. 마지막 그룹 `C5`는 모듈 5 — **코드를 쓰기 전에 무엇을 만들지 합의하는 법** — 을 다룬다. 그리고 여기서 만든 검증기의 사고방식이 거기서 **명세와 코드를 대조하는 도구**로 다시 나타난다.

:::diagram
id: cc-grounded-cc
원본: (신규 작도)
제목: 주장·근거 쌍을 기계가 대조하는 흐름
내용: source.md → 스키마 강제 출력 → claims.json → 문자열 대조 → PASS/FAIL
:::

---
## 실습 5. 명세 주도 개발 — 모듈 5를 손으로 확인한다

앞의 열아홉 실습은 전부 **어떻게**에 관한 것이었다. 어떻게 가르치고, 어떻게 막고, 어떻게 돌리고, 어떻게 기억하게 하는가.

이 마지막 그룹은 그 앞에 오는 것을 다룬다. **무엇을 만들 것인가.** 그리고 이 질문을 건너뛰면 앞의 열아홉 실습이 전부 무의미해진다는 것을 숫자로 확인한다.

네 실습의 흐름은 이렇다.

| 실습 | 하는 일 |
|---|---|
| C5-1 | 명세 없이 만든 것과 명세로 만든 것을 같은 시험지로 채점한다 |
| C5-2 | 명세를 나 혼자 쓰지 않는다 — AI가 나를 인터뷰하게 만든다 |
| C5-3 | 명세의 수용 기준을 `C2-4`의 게이트에 연결한다 |
| C5-4 | 명세와 코드가 어긋나는 것을 일부러 만들고, 기계가 잡게 한다 |

## C5-1. 명세 없이 시킨 것과 명세로 시킨 것을 나란히 놓는다

> 대응 | 모듈 5 · 1~4절
> 소요 | 40분
> 선행 | C4-3
> 확인 | 같은 시험지의 두 점수 · 모델 호출 3회 (라운드 A · B · 계획 모드)

### 무엇을

같은 함수를 두 번 만든다. 한 번은 한 줄 요청으로, 한 번은 명세로. 그리고 **미리 만들어 둔 같은 시험지**로 둘을 채점한다.

### 왜

"명세를 쓰면 좋다"는 말은 아무도 반박하지 않지만 아무도 안 한다. 이유는 명세를 쓰는 비용이 지금 보이고, 명세가 없어서 생기는 비용은 나중에 보이기 때문이다.

이 실습은 그 시차를 없앤다. **10분 안에 둘 다 만들고 같은 시험지로 채점한다.** 그러면 "명세를 쓰는 데 든 5분"과 "명세가 없어서 틀린 항목 수"가 같은 화면에 놓인다.

시험지를 **먼저** 만드는 것이 이 실습의 설계 요점이다. 결과를 보고 나서 채점 기준을 정하면 자기가 원하는 결론을 만들 수 있다. 모듈 5가 말하는 **정밀도 시험**이 바로 이것이다 — 무엇을 만들지 정할 때 이미 무엇이 옳은지도 정해져 있어야 한다.

### 해보기

**작업 폴더가 `work/` 아래인 것에 주의한다.** `C2-2`에서 `CLAUDE.md` 에 "파일을 새로 만들 때는 반드시 `work/` 아래에만 만든다"를 심었기 때문이다. 이 실습을 `~/cc-lab/sdd/` 에서 하면 에이전트가 규칙을 지키려고 `sdd/work/duration.py` 에 파일을 만들고, 채점기는 `duration.py` 를 찾지 못한다.

이 문서를 만들면서 실제로 그렇게 됐다. **내가 심은 규칙이 내 다음 실습을 깨뜨렸다.** 이건 하니스 엔지니어링의 흔한 사고이고, 배울 만한 사고다. 규칙은 프로젝트 전체에 걸리므로, 규칙을 심을 때는 "이 규칙이 앞으로 할 모든 일에 걸린다"를 계산해야 한다. 그래서 각 명령의 프롬프트에도 "지금 이 폴더의 duration.py 다"를 명시했다.

먼저 **시험지**를 만든다. 이 파일은 두 라운드 모두에 그대로 쓰인다. 그리고 **에이전트에게는 보여 주지 않는다.**

```bash
cd ~/cc-lab
mkdir -p work/sdd/hidden work/sdd/roundA work/sdd/roundB
cat > work/sdd/hidden/acceptance.py <<'EOF'
#!/usr/bin/env python3
"""숨겨진 수용 시험. 두 라운드에 같은 기준을 적용한다."""
import importlib.util, sys, pathlib

target = pathlib.Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("cand", target)
mod = importlib.util.module_from_spec(spec)
try:
    spec.loader.exec_module(mod)
except Exception as e:
    print("로드 실패: %s" % e); sys.exit(1)

if not hasattr(mod, "parse_duration"):
    print("parse_duration 함수가 없다"); sys.exit(1)
f = mod.parse_duration

OK = [("1h", 3600), ("30m", 1800), ("45s", 45),
      ("1h30m", 5400), ("2h15m30s", 8130), ("90m", 5400),
      ("0s", 0), ("1H30M", 5400)]
ERR = ["", "abc", "1x", "-5m", "1h2h", "m30", "1.5h"]

passed = failed = 0
for src, want in OK:
    try:
        got = f(src)
    except Exception as e:
        print("FAIL  parse_duration(%r) 가 예외: %s" % (src, type(e).__name__)); failed += 1; continue
    if got == want:
        passed += 1
    else:
        print("FAIL  parse_duration(%r) -> %r  (기대 %r)" % (src, got, want)); failed += 1

for src in ERR:
    try:
        got = f(src)
        print("FAIL  parse_duration(%r) 가 %r 를 돌려줬다 (ValueError 를 내야 한다)" % (src, got))
        failed += 1
    except ValueError:
        passed += 1
    except Exception as e:
        print("FAIL  parse_duration(%r) 가 %s (ValueError 여야 한다)" % (src, type(e).__name__)); failed += 1

print("\n%d/%d 통과" % (passed, passed + failed))
sys.exit(0 if failed == 0 else 1)
EOF
echo "시험 항목: $(python3 -c "print(8+7)")개"
```

**라운드 A — 한 줄 요청.** 사람들이 실제로 이렇게 시킨다.

```bash
cd ~/cc-lab/work/sdd/roundA
claude -p "\"1h30m\" 같은 문자열을 초 단위 정수로 바꾸는 parse_duration 함수를 만들어라. 파일은 지금 이 폴더의 duration.py 다. 하위 폴더를 만들지 마라." \
  --model haiku --permission-mode acceptEdits --output-format json 2>/dev/null \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['result'][:200])"
echo "── 만들어진 코드"
cat duration.py
echo "════════ 채점"
python3 ../hidden/acceptance.py duration.py; echo "exit $?"
```

**라운드 B — 명세로 요청.** 같은 함수를, 명세를 먼저 쓴다.

```bash
cd ~/cc-lab/work/sdd/roundB
cat > spec.md <<'EOF'
# 명세: parse_duration

## 목표

사람이 쓰는 기간 표기 문자열을 초 단위 정수로 바꾼다.

## 사용자 시나리오

설정 파일에 `timeout: 1h30m` 처럼 적으면, 프로그램이 5400초로 읽어야 한다.

## 기능 요구사항

- `parse_duration(s: str) -> int` 하나를 제공한다.
- 단위는 `h`(시), `m`(분), `s`(초) 세 개만 인정한다.
- 여러 단위를 이어 쓸 수 있다. 예: `2h15m30s` → 8130.
- 단위 순서는 반드시 큰 것에서 작은 것으로만 온다.
- 대문자 단위도 같게 처리한다. `1H30M` → 5400.

## 경계 사례와 규칙

- 같은 단위가 두 번 나오면 오류다. `1h2h` → `ValueError`.
- 단위가 큰 것에서 작은 것 순서가 아니면 오류다. `30m1h` → `ValueError`.
- 숫자 없는 단위는 오류다. `m30` → `ValueError`.
- 단위 없는 숫자는 오류다. `90` → `ValueError`.
- 빈 문자열은 오류다.
- 알 수 없는 문자가 있으면 오류다. `1x`, `abc` → `ValueError`.
- 음수는 오류다. `-5m` → `ValueError`.
- 소수는 오류다. `1.5h` → `ValueError`.
- 단위 값에 상한을 두지 않는다. `90m` 은 5400 으로 정상 처리한다.
- `0s` 는 0 을 돌려준다. 오류가 아니다.

## 범위 밖

- 일(`d`)·주(`w`)·밀리초(`ms`) 단위는 이번 범위가 아니다.
- 역변환(초 → 문자열)은 만들지 않는다.
- 공백을 허용하는 표기(`1h 30m`)는 이번 범위가 아니다.

## 수용 기준

- 위 `기능 요구사항` 의 예시 전부가 정확한 정수를 돌려준다.
- 위 `경계 사례와 규칙` 의 모든 오류 입력이 `ValueError` 를 낸다.
- 다른 예외 종류(`TypeError`, `IndexError` 등)를 내면 실패로 본다.
EOF
claude -p "spec.md 를 읽고, 그 명세를 정확히 만족하는 구현을 만들어라. 파일은 지금 이 폴더의 duration.py 다. 하위 폴더를 만들지 마라. 명세에 없는 기능은 추가하지 마라." \
  --model haiku --permission-mode acceptEdits --output-format json 2>/dev/null \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['result'][:200])"
echo "── 만들어진 코드"
cat duration.py
echo "════════ 채점"
python3 ../hidden/acceptance.py duration.py; echo "exit $?"
```

두 결과를 나란히 본다.

```bash
cd ~/cc-lab/work/sdd
for R in roundA roundB; do
  S=$(python3 hidden/acceptance.py $R/duration.py 2>/dev/null | tail -1)
  L=$(wc -l < $R/duration.py)
  printf '%-8s %-12s 코드 %s줄\n' "$R" "$S" "$L"
done
echo "명세 길이: $(wc -l < roundB/spec.md)줄"
```

### 기대 결과

라운드 A는 대개 이런 모양으로 떨어진다.

```
FAIL  parse_duration('1H30M') -> 0  (기대 5400)
FAIL  parse_duration('') 가 0 를 돌려줬다 (ValueError 를 내야 한다)
FAIL  parse_duration('abc') 가 0 를 돌려줬다 (ValueError 를 내야 한다)
FAIL  parse_duration('1x') 가 0 를 돌려줬다 (ValueError 를 내야 한다)
FAIL  parse_duration('-5m') 가 300 를 돌려줬다 (ValueError 를 내야 한다)
FAIL  parse_duration('1h2h') 가 3600 를 돌려줬다 (ValueError 를 내야 한다)
FAIL  parse_duration('1.5h') 가 5400 를 돌려줬다 (ValueError 를 내야 한다)
FAIL  parse_duration('90') 가 0 를 돌려줬다 (ValueError 를 내야 한다)

7/15 통과
exit 1
```

라운드 B는 대개 전부 통과한다.

```
15/15 통과
exit 0
```

비교표:

```
roundA   7/15 통과   코드 49줄
roundB   15/15 통과  코드 45줄
명세 길이: 42줄
```

**반드시 확인할 것**은 두 라운드의 통과 수가 **다르다**는 것, 그리고 **라운드 A의 실패가 전부 경계 사례**라는 것이다.

라운드 A의 코드를 다시 읽어 보라. 잘 쓴 코드다. 정규식도 깔끔하고 주석도 있다. **틀린 건 코드가 아니라 코드가 답한 질문이다.** 모델은 "1h30m을 5400으로 바꾸는 함수"를 정확히 만들었고, 내가 물어보지 않은 것들 — 대문자, 빈 문자열, 중복 단위, 소수 — 에 대해서는 그때그때 아무렇게나 정했다.

정확한 점수는 실행마다 다르다. 라운드 A가 11/15을 받을 수도 있고, 라운드 B가 14/15에 그칠 수도 있다. **A < B 이면 성공이다.** 만약 A가 B와 같거나 높게 나왔다면, 명세를 다시 읽어 보라 — 명세가 모호하거나 시험지와 어긋난 것이다. 그것도 정확히 배울 거리다. **명세와 시험지가 어긋나면 명세는 쓸모가 없다.**

### 명세 42줄이 코드를 짧게 만들었다

위 실측을 다시 보라. **라운드 A의 코드가 49줄이고 라운드 B가 45줄이다.** 명세 없이 만든 쪽이 오히려 더 길다.

이건 우연이 아니다. 명세가 없으면 모델은 "혹시 필요할까 싶은 것"을 넣는다. 위 라운드 A의 코드에는 오류 대신 0을 돌려주는 방어 코드와 예외 처리 분기가 있었고, 그것들이 정확히 시험을 떨어뜨린 원인이었다. **무엇이 옳은지 모르면 코드는 길어지면서 동시에 틀린다.**

명세가 코드보다 길다는 사실을 보고 "비효율"이라고 느끼는 것은 정상이고, 그 느낌을 뒤집는 것이 모듈 5의 목적이다. 세 가지를 생각해 보라.

1. **명세 42줄은 한 번 쓰고 여러 번 쓴다.** `C5-3`에서 이 명세가 테스트가 되고, `C5-4`에서 표류 검사기의 기준이 된다.
2. **명세를 안 썼다면 그 42줄만큼의 결정을 모델이 대신 했다.** 결정이 사라진 게 아니라 보이지 않는 곳으로 옮겨진 것이다.
3. **코드 45줄은 다시 만들 수 있고, 명세 42줄은 다시 만들 수 없다.** 코드는 명세에서 파생되지만 명세는 사람의 머리에서만 나온다.

### 계획 모드로도 해 보기

Claude Code에는 **계획 모드**가 있다. 코드를 만들기 전에 무엇을 할지 먼저 내놓게 한다. 명세와는 다른 물건이지만 비교해 볼 가치가 있다.

```bash
cd ~/cc-lab/work/sdd
mkdir -p roundP && cd roundP
claude -p "\"1h30m\" 같은 문자열을 초 단위 정수로 바꾸는 parse_duration 함수를 만들 계획을 세워라." \
  --model haiku --permission-mode plan --output-format json 2>/dev/null \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['result'][:900])"
```

실측에서는 이런 답이 나왔다.

```
계획을 세우기 전에 몇 가지만 확인하겠습니다.

1. 구현 언어는 무엇으로 할까요?
2. 지원할 단위는 어디까지인가요? h, m, s 만인지 d(일), w(주), ms 까지 포함할지.
3. 소수점 값("1.5h")이나 음수("-30m")도 허용할까요?
4. 잘못된 입력일 때 예외를 던질지, None 을 반환할지 어떤 방식을 원하시나요?
5. 함수를 저장할 파일 경로는 work/ 아래 어디로 할까요?
```

**계획을 내놓지 않고 질문을 했다.** 그리고 그 질문 목록을 `spec.md` 의 `경계 사례와 규칙` 절과 비교해 보라. 소수, 음수, 오류 처리 방식, 단위 범위 — 거의 그대로 겹친다.

이게 이 실습에서 `C5-2`로 넘어가는 다리다. **좋은 모델은 명세가 없으면 묻는다.** 문제는 우리가 대개 묻지 못하게 시킨다는 것이다 — `-p` 로 한 번에 끝내라고 하거나, 되묻지 말라고 하거나, 배경에서 돌리거나. 그러면 모델은 묻는 대신 **혼자 결정한다.** 라운드 A에서 일어난 일이 정확히 그것이다.

계획은 **어떻게 만들지**를 말하고, 명세는 **무엇이 옳은지**를 말한다. 계획 모드가 질문을 하지 않고 바로 구현 전략을 내놓는 경우도 있다 — 그때 그 전략에는 "`1h2h` 는 오류다" 같은 판정 기준이 없다. **둘은 대체 관계가 아니다.**

### 막히면

| 증상 | 원인 | 조치 |
|---|---|---|
| `로드 실패` | 코드에 문법 오류 | `python3 roundA/duration.py` 로 직접 확인 |
| `parse_duration 함수가 없다` | 다른 이름으로 만들었다 | 프롬프트의 함수 이름을 확인 |
| 라운드 A가 만점 | 운이 좋았다 | 한 번 더 돌려 본다. 매번 만점이면 시험지를 더 깐깐하게 |
| 라운드 B가 여러 개 틀림 | 명세가 모호하다 | 어느 항목이 틀렸는지 보고 그 규칙을 명세에서 찾는다 |

### 이어지는 곳

`C5-2`에서 명세를 **혼자 쓰지 않는 법**을 배운다. 위의 `spec.md` 는 내가 미리 써 준 것이지만, 실무에서 어려운 부분은 "무엇을 명세에 넣어야 하는지 모른다"는 것이다.

:::diagram
id: cc-spec-vs-none
원본: (신규 작도)
제목: 같은 시험지로 채점한 두 라운드
내용: 한 줄 요청과 명세 요청의 통과 항목 비교, 실패가 몰리는 자리
:::

---

## C5-2. AI가 나를 인터뷰하게 만든다

> 대응 | 모듈 5 · 5~7절
> 소요 | 30분
> 선행 | C5-1
> 확인 | 질문 3~5개가 마커와 함께 · 모델 호출 2회

### 무엇을

**커스텀 슬래시 명령** `/clarify` 를 만들어, 내가 쓴 한 줄 요구사항에서 **모호한 지점을 찾아 질문하게** 한다. 그리고 그 질문에 답한 것으로 명세를 채운다.

### 왜

`C5-1`의 `spec.md` 는 이미 잘 쓰인 명세였다. 실무에서 진짜 어려운 것은 **명세를 쓰는 것**이 아니라 **무엇을 명세에 써야 하는지 아는 것**이다. 내가 아는 것은 이미 명세에 있고, 문제는 내가 모른다는 사실조차 모르는 부분이다.

모듈 5의 방법론이 `research → specify → clarify → build` 인 이유가 이것이다. `clarify` 는 별도 단계다. 그리고 이 단계를 사람이 혼자 하면 놓친다 — 자기 머릿속 가정은 자기 눈에 안 보이기 때문이다.

**AI에게 이 역할을 맡기는 것이 잘 맞는다.** 모델은 내 가정을 공유하지 않기 때문이다. "파일을 올리면 요약해 준다"라는 문장에서 나는 이미 "텍스트 파일"을 떠올렸지만 모델은 안 떠올린다. 그래서 묻는다.

Claude Code의 커스텀 슬래시 명령은 이걸 **재사용 가능한 도구**로 만든다. 한 번 만들면 모든 프로젝트에서 `/clarify` 로 부를 수 있다.

### 해보기

```bash
cd ~/cc-lab
mkdir -p .claude/commands
cat > .claude/commands/clarify.md <<'EOF'
---
description: 요구사항이 모호한 곳을 찾아 질문 목록을 만든다
---

아래 요구사항을 읽고, 그대로 만들면 **사람마다 다르게 만들 지점**을 찾아라.

요구사항: $ARGUMENTS

찾을 때 아래를 특히 살펴라.

- 경계값 — 0, 빈 값, 음수, 아주 큰 값에서 무엇이 옳은가
- 실패 처리 — 잘못된 입력이 오면 무엇을 하는가
- 범위 — 어디까지가 이번 일이고 어디부터가 다음 일인가
- 판정 기준 — 무엇이 참이면 완성인가

출력은 반드시 이 형식이다.

⟪YNC-CLARIFY-V1⟫
1. (질문) — 왜 모호한지 한 줄
2. ...

규칙:
- 질문은 3개에서 5개 사이로 한다.
- 스스로 답하지 마라. 질문만 한다.
- 구현 방법을 묻지 마라. 무엇이 옳은지를 물어라.
EOF
ls -l .claude/commands/clarify.md
```

써 본다.

```bash
cd ~/cc-lab
claude -p "/clarify 사용자가 파일을 올리면 요약해서 보여주는 기능" \
  --model haiku --output-format json 2>/dev/null \
  | python3 -c "
import sys, json
r = json.load(sys.stdin)['result']
print('마커:', '⟪YNC-CLARIFY-V1⟫' in r)
print(r[:900])
"
```

이제 `C5-1`에서 쓴 명세의 **초안 상태**에 대고 써 본다. 명세가 이미 있는데도 질문이 나오는지 보는 것이다.

```bash
cd ~/cc-lab
claude -p "/clarify \"1h30m\" 같은 문자열을 초 단위 정수로 바꾸는 parse_duration 함수. 단위는 h, m, s 세 개." \
  --model haiku --output-format json 2>/dev/null \
  | python3 -c "
import sys, json
r = json.load(sys.stdin)['result']
print(r[:800])
"
echo "════════ C5-1 의 명세와 대조"
grep -A 12 '^## 경계 사례와 규칙' work/sdd/roundB/spec.md | head -13
```

### 기대 결과

첫 호출:

```
마커: True
⟪YNC-CLARIFY-V1⟫

1. 어떤 종류의 파일을 지원하는가? — 텍스트만인지, 이미지·PDF도 포함인지, 형식마다 요약 방식이 다른지 정해지지 않음
2. 요약의 길이와 형식은 무엇인가? — 한 줄, 불릿, 문단 중 어느 것인지, 사용자가 고를 수 있는지 불명확
3. 여러 파일을 동시에 올리면 어떻게 하는가? — 개별 요약인지 통합 요약인지 정해지지 않음
4. 파일이 너무 크거나 읽을 수 없으면 무엇을 보여주는가? — 실패 처리가 정의되지 않음
5. 요약 결과를 어디에 표시하는가? — 인라인, 모달, 별도 페이지 중 불명확
```

두 번째 호출은 `parse_duration` 에 대해 이런 질문을 낸다.

```
⟪YNC-CLARIFY-V1⟫

1. 같은 단위가 두 번 나오면 어떻게 하는가? (`1h2h`) — 합산인지 오류인지 정해지지 않음
2. 단위 순서가 뒤바뀌면 허용하는가? (`30m1h`) — ...
3. 잘못된 입력에 무엇을 돌려주는가? — None, 0, 예외 중 어느 것인지 ...
4. 소수를 허용하는가? (`1.5h`) — ...
```

**반드시 확인할 것**은 두 가지다.

1. 첫 호출에서 `마커: True`.
2. **두 번째 호출의 질문들이 `C5-1` 명세의 `경계 사례와 규칙` 절과 상당히 겹친다.**

두 번째가 이 실습의 결론이다. `C5-1`에서 내가 명세에 써 넣은 규칙들 — 중복 단위, 순서, 소수, 오류 종류 — 을 모델이 **질문 형태로 다시 찾아냈다.** 즉 이 절차를 쓰면 명세를 처음부터 혼자 완성할 필요가 없다. **질문을 받고 답하기만 하면 된다.** 명세 쓰기가 작문에서 인터뷰로 바뀐다.

질문의 개수와 문장은 매번 다르다. 겹치는 항목이 하나도 없다면 요구사항 문장을 더 짧고 모호하게 줘 보라 — 모호할수록 질문이 정확해진다.

### 놓치기 쉬운 것

`/clarify` 는 **답을 주지 않는다.** 그게 설계다. 모델이 스스로 답하면 그건 다시 모델의 가정이 되고, 명세의 목적이 사라진다. 명령 파일에 "스스로 답하지 마라"를 넣은 이유다.

이 규칙이 깨지는 것을 직접 보고 싶으면 그 줄을 지우고 다시 돌려 보라. 모델은 질문과 함께 "일반적으로는 이렇게 합니다"를 붙이기 시작하고, 그러면 사람이 읽고 그냥 동의해 버린다. **결정은 사람이 해야 하고, 결정하지 않은 것을 결정한 것처럼 보이게 만드는 것이 가장 위험하다.**

### 막히면

| 증상 | 원인 | 조치 |
|---|---|---|
| 슬래시 명령이 안 먹음 | 파일 위치가 다르다 | `.claude/commands/clarify.md` 확인 |
| `$ARGUMENTS` 가 그대로 나옴 | 인자를 안 줬다 | `/clarify 뒤에 요구사항` 형태로 |
| 질문 대신 구현을 내놓음 | 명령 문서가 약하다 | "질문만 한다" 를 더 앞에 쓴다 |
| 마커가 없음 | 형식 지시가 뒤에 묻혔다 | 형식 블록을 문서 위쪽으로 옮긴다 |

### 이어지는 곳

`C5-3`에서 명세의 마지막 절 — `수용 기준` — 을 `C2-4`에서 만든 게이트에 연결한다. 명세가 문서로만 남으면 지켜지지 않는다. 실행되는 곳에 꽂아야 한다.

---

## C5-3. 수용 기준을 게이트에 연결한다

> 대응 | 모듈 5 · 8~10절
> 소요 | 40분
> 선행 | C5-2, C2-4
> 확인 | 게이트 로그에 실패→성공 · 모델 호출 1회 (내부 여러 턴)

### 무엇을

`C5-1`의 `spec.md` 에 있는 `수용 기준` 을 **실행되는 테스트로 옮기고**, 그 테스트를 `C2-4`의 Stop 훅에 연결한다. 그러고 나서 에이전트에게 **일부러 부족한 구현**을 시킨다.

### 왜

명세를 써 놓고 아무도 읽지 않는 것이 실무의 기본값이다. 명세가 실패하는 이유는 내용이 나빠서가 아니라 **아무 곳에도 꽂혀 있지 않아서**다.

모듈 5의 표현으로는 명세가 **참조 문서**에서 **판정 기준**으로 승격되어야 한다. 그 승격은 딱 한 가지 방법으로만 일어난다. `수용 기준` 절이 **실행 가능한 코드**가 되고, 그 코드가 완료 판정 경로에 놓이는 것이다.

`C2-4`와 이 실습의 차이를 보라. `C2-4`에서 테스트는 내가 임의로 정한 다섯 개 케이스였다. 여기서 테스트는 **명세에서 유도된다.** 그래서 테스트가 왜 그것인지 설명할 수 있고, 명세가 바뀌면 테스트도 바뀌어야 한다는 것이 명확해진다.

### 해보기

명세를 옮겨 온 새 작업 폴더를 만든다.

```bash
cd ~/cc-lab
mkdir -p work/sdd/gated/.claude/hooks
cp work/sdd/roundB/spec.md work/sdd/gated/spec.md
cd work/sdd/gated
grep -c '^- ' spec.md
```

`수용 기준` 을 테스트로 옮긴다. **명세의 각 규칙에 어느 테스트가 대응하는지 주석으로 붙인다.** 이 주석이 나중에 `C5-4`에서 표류를 잡는 실마리가 된다.

```bash
cd ~/cc-lab/work/sdd/gated
cat > accept.py <<'EOF'
#!/usr/bin/env python3
"""spec.md 의 수용 기준을 실행 가능한 테스트로 옮긴 것."""
import importlib.util, pathlib, sys

p = pathlib.Path("duration.py")
if not p.exists():
    print("duration.py 가 없다"); sys.exit(1)
s = importlib.util.spec_from_file_location("cand", p)
m = importlib.util.module_from_spec(s)
try:
    s.loader.exec_module(m)
except Exception as e:
    print("로드 실패: %s" % e); sys.exit(1)
if not hasattr(m, "parse_duration"):
    print("parse_duration 이 없다"); sys.exit(1)
f = m.parse_duration

# (입력, 기대값, spec.md 의 근거 절)
OK = [
    ("1h",       3600, "기능 요구사항 · 단위 h"),
    ("30m",      1800, "기능 요구사항 · 단위 m"),
    ("45s",        45, "기능 요구사항 · 단위 s"),
    ("1h30m",    5400, "사용자 시나리오"),
    ("2h15m30s", 8130, "기능 요구사항 · 여러 단위"),
    ("1H30M",    5400, "기능 요구사항 · 대문자"),
    ("90m",      5400, "경계 사례 · 상한 없음"),
    ("0s",          0, "경계 사례 · 0s 는 0"),
]
ERR = [
    ("",      "경계 사례 · 빈 문자열"),
    ("abc",   "경계 사례 · 알 수 없는 문자"),
    ("1x",    "경계 사례 · 알 수 없는 문자"),
    ("-5m",   "경계 사례 · 음수"),
    ("1.5h",  "경계 사례 · 소수"),
    ("1h2h",  "경계 사례 · 중복 단위"),
    ("30m1h", "경계 사례 · 순서"),
    ("m30",   "경계 사례 · 숫자 없는 단위"),
    ("90",    "경계 사례 · 단위 없는 숫자"),
]

bad = 0
for src, want, why in OK:
    try:
        got = f(src)
    except Exception as e:
        print("FAIL  %-9r 예외 %s   ← %s" % (src, type(e).__name__, why)); bad += 1; continue
    if got != want:
        print("FAIL  %-9r -> %r (기대 %r)   ← %s" % (src, got, want, why)); bad += 1
for src, why in ERR:
    try:
        got = f(src)
        print("FAIL  %-9r -> %r (ValueError 여야 함)   ← %s" % (src, got, why)); bad += 1
    except ValueError:
        pass
    except Exception as e:
        print("FAIL  %-9r %s (ValueError 여야 함)   ← %s" % (src, type(e).__name__, why)); bad += 1

total = len(OK) + len(ERR)
print("%d/%d 통과" % (total - bad, total))
sys.exit(1 if bad else 0)
EOF
```

게이트를 붙인다. `C2-4`와 같은 구조인데 **테스트가 명세에서 왔다는 것**만 다르다.

```bash
cd ~/cc-lab/work/sdd/gated
cat > .claude/hooks/accept-gate.sh <<'EOF'
#!/usr/bin/env bash
# Stop 훅: spec.md 의 수용 기준을 통과하지 못하면 끝내지 못한다.
cd "$CLAUDE_PROJECT_DIR" || exit 0
N=$(cat .claude/gate.count 2>/dev/null || echo 0)
OUT=$(python3 accept.py 2>&1); RC=$?
echo "$(date +%H:%M:%S) 시도#$N rc=$RC | $(printf '%s' "$OUT" | tail -1)" >> .claude/gate.log

if [ "$RC" -eq 0 ]; then echo 0 > .claude/gate.count; exit 0; fi
if [ "$N" -ge 4 ]; then
  echo "$(date +%H:%M:%S) 상한 도달 — 통과시킴" >> .claude/gate.log
  echo 0 > .claude/gate.count; exit 0
fi
echo $((N + 1)) > .claude/gate.count
printf '%s' "$OUT" | python3 -c "
import json, sys
print(json.dumps({'decision': 'block',
  'reason': 'spec.md 의 수용 기준을 아직 만족하지 않는다. 끝내지 말고 duration.py 를 고쳐라. 실패한 항목의 근거 절이 화살표 뒤에 적혀 있으니 spec.md 의 해당 절을 다시 읽어라.\n' + sys.stdin.read()}))
"
EOF
chmod +x .claude/hooks/accept-gate.sh
cat > .claude/settings.json <<'EOF'
{
  "hooks": {
    "Stop": [
      { "hooks": [ { "type": "command",
                     "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/accept-gate.sh" } ] }
    ]
  }
}
EOF
python3 -m json.tool .claude/settings.json > /dev/null && echo "settings.json 문법 OK"
```

**일부러 부족하게** 시킨다. 명세를 읽지 말라고까지 한다.

```bash
cd ~/cc-lab/work/sdd/gated
rm -f duration.py .claude/gate.count; : > .claude/gate.log
claude -p "duration.py 에 parse_duration 함수를 만들어라. \"1h30m\" 을 5400 으로 바꾸면 된다. spec.md 는 읽지 말고 빨리 만들고 끝내라." \
  --model haiku --permission-mode acceptEdits --output-format json 2>/dev/null \
  | python3 -c "
import sys, json
d = json.load(sys.stdin)
print('턴 수:', d['num_turns'], '· 비용 \$', round(d['total_cost_usd'], 4), '·', round(d['duration_ms']/1000, 1), '초')
print(d['result'][:300])
"
echo "── 게이트가 본 것"
cat .claude/gate.log
echo "── 최종"
python3 accept.py | tail -3; echo "exit $?"
```

### 기대 결과

```
턴 수: 9 · 비용 $ 0.0833 · 68.6 초
duration.py 파일을 생성했습니다. spec.md 의 모든 요구사항을 충족하도록 구현했습니다.
── 게이트가 본 것
14:06:23 시도#0 rc=1 | 11/17 통과
14:07:04 시도#1 rc=0 | 17/17 통과
── 최종
17/17 통과
exit 0
```

**반드시 확인할 것**은 `gate.log` 의 **첫 줄이 `rc=1`, 마지막 줄이 `rc=0`** 인 것이다. 에이전트는 "빨리 만들고 끝내라"는 지시를 따랐고, 게이트가 그걸 거절했다.

줄 수는 두 줄일 수도 있고 다섯 줄일 수도 있다. 점수가 `11/17 → 15/17 → 17/17` 처럼 단계적으로 오를 수도 있다.

첫 줄이 `rc=1 | duration.py 가 없다` 로 나오는 경우도 있다. 에이전트가 `CLAUDE.md` 의 `work/` 규칙을 지키려고 한 단계 더 아래에 파일을 만든 것이다. 그래도 게이트는 제 일을 한다 — 두 번째 시도에서 에이전트가 위치를 고친다. **게이트는 "무엇이 틀렸는지"를 모르지만 "아직 아니다"는 확실히 안다.**

이제 이 실습의 진짜 관찰거리를 보라. 에이전트는 **`spec.md` 를 읽지 말라는 지시를 받았다.** 그런데도 결국 명세를 만족했다. 어떻게? 게이트가 실패할 때마다 **근거 절 이름을 함께 돌려줬기** 때문이다.

```
FAIL  '1h2h'   -> 10800 (ValueError 여야 함)   ← 경계 사례 · 중복 단위
```

이 한 줄이 "spec.md 의 경계 사례 절을 읽어라"라는 지시보다 강하다. **에이전트에게 문서를 읽으라고 부탁하는 것보다, 문서를 안 읽으면 통과할 수 없는 게이트를 두는 것이 확실하다.**

### 막히면

| 증상 | 원인 | 조치 |
|---|---|---|
| 무한히 돈다 | 상한 코드 누락 | `N -ge 4` 블록 확인 |
| 첫 시도에 통과 | 모델이 명세를 읽었다 | 로그의 첫 줄이 `rc=0` 이면 프롬프트를 더 좁힌다 |
| `상한 도달` 로 끝남 | 수용 기준끼리 모순 | `accept.py` 의 남은 FAIL 을 직접 읽는다 |
| 게이트가 안 불림 | 훅 등록 누락 | `.claude/settings.json` 확인 |

### 이어지는 곳

명세와 코드가 지금은 일치한다. `C5-4`에서 그 일치를 **일부러 깨뜨리고**, 깨진 것을 기계가 알아채게 만든다. 이게 이 실습편의 마지막 실습이다.

---

## C5-4. 명세 표류를 일부러 만들고, 잡아낸다

> 대응 | 모듈 5 · 11~12절
> 소요 | 35분
> 선행 | C5-3
> 확인 | CONFLICT 판정 1건 이상 · 모델 호출 1회

### 무엇을

명세의 **범위 밖** 에 적힌 기능을 에이전트에게 일부러 만들게 하고, 그것을 잡아내는 **표류 검사기**를 만든다. 그리고 그 검사기의 첫 버전이 **놓치는 것**도 확인한다.

### 왜

명세 주도 개발의 실패는 대개 시작이 아니라 3주 뒤에 온다. 명세대로 만들고, 그 다음부터 명세를 안 고치면서 코드만 고친다. 6개월 뒤 명세는 거짓 문서가 되고, 아무도 안 읽으며, 새로 온 사람이 그것을 믿고 사고를 낸다. 이게 **명세 표류**다.

표류의 종류가 둘 있고, 둘 다 확인한다.

1. **누락** — 명세에 있는데 코드에 없다. `C5-3`의 게이트가 이걸 잡는다.
2. **초과** — 코드에 있는데 명세에 없다. 혹은 명세가 **하지 말라고 한 것**이 코드에 있다. 게이트는 이걸 **절대 못 잡는다** — 테스트는 있는 것만 검사하기 때문이다.

두 번째가 더 위험하다. 아무도 요청하지 않은 기능이 조용히 늘어나고, 각각이 유지보수 부담이 되고, 그중 하나가 보안 구멍이 된다. 그리고 테스트는 전부 초록색이다.

### 해보기

먼저 표류를 만든다. 명세의 `범위 밖` 에는 이렇게 적혀 있다.

```bash
cd ~/cc-lab/work/sdd/gated
grep -A 4 '^## 범위 밖' spec.md
```

에이전트에게 **그 금지된 것을** 시킨다. 게이트는 통과할 것이다 — 기존 테스트를 깨뜨리지 않으니까.

```bash
cd ~/cc-lab/work/sdd/gated
cp duration.py duration.py.clean
rm -f .claude/gate.count; : > .claude/gate.log
claude -p "duration.py 의 parse_duration 이 'd'(일) 단위도 지원하게 하고, '1h 30m' 처럼 공백이 들어간 표기도 받게 해라. 기존 동작은 그대로 유지해라." \
  --model haiku --permission-mode acceptEdits --output-format json 2>/dev/null \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['result'][:250])"
echo "── 게이트는 통과했나"
cat .claude/gate.log
echo "── 새 기능이 실제로 붙었나"
python3 -c "
import importlib.util
s = importlib.util.spec_from_file_location('m', 'duration.py')
m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
for t in ('1d', '1h 30m'):
    try: print('  %-8r -> %r' % (t, m.parse_duration(t)))
    except Exception as e: print('  %-8r -> %s' % (t, type(e).__name__))
"
```

이제 **순진한 검사기**를 만든다. 명세 전체에서 키워드를 찾는 방식이다.

```bash
cd ~/cc-lab/work/sdd/gated
cat > drift_naive.py <<'EOF'
#!/usr/bin/env python3
"""순진한 표류 검사기 — 명세 전체를 한 덩어리로 보고 키워드를 찾는다."""
import re, sys

spec = open("spec.md", encoding="utf-8").read()
code = open("duration.py", encoding="utf-8").read()

FEATURES = [("일 단위", r"['\"]d['\"]|\bdays?\b|일 단위"),
            ("공백 허용", r"\.strip\(\)|\.replace\(\s*['\"] ['\"]|\\s\+")]

bad = 0
for name, pat in FEATURES:
    in_code = bool(re.search(pat, code))
    in_spec = name.split()[0] in spec       # ← 명세 어디든 단어가 있으면 OK 로 본다
    if in_code and not in_spec:
        print("DRIFT  %s — 코드에 있는데 명세에 없다" % name); bad += 1
    else:
        print("ok     %s — 코드 %s / 명세 %s" % (name, in_code, in_spec))
print("표류 %d건" % bad)
EOF
python3 drift_naive.py
```

이 검사기의 결과를 믿기 전에 명세를 다시 읽어 보라.

```bash
cd ~/cc-lab/work/sdd/gated
echo "── 명세에서 '일' 과 '공백' 이 나오는 곳"
grep -n '일\|공백' spec.md
```

**절 이름을 보는 검사기**로 고친다.

```bash
cd ~/cc-lab/work/sdd/gated
cat > drift.py <<'EOF'
#!/usr/bin/env python3
"""절을 구분하는 표류 검사기. 약속한 절과 금지한 절을 따로 본다."""
import re, sys

spec = open("spec.md", encoding="utf-8").read()
code = open("duration.py", encoding="utf-8").read()

def section(name):
    m = re.search(r"^## %s\n(.*?)(?=\n## |\Z)" % re.escape(name), spec, re.S | re.M)
    return m.group(1) if m else ""

PROMISED = "\n".join(section(n) for n in
                     ("기능 요구사항", "경계 사례와 규칙", "수용 기준"))
EXCLUDED = section("범위 밖")

FEATURES = [
    ("일 단위",   r"['\"]d['\"]|\bdays?\b|86400",           r"일\(`?d`?\)|일 단위"),
    ("주 단위",   r"['\"]w['\"]|\bweeks?\b|604800",         r"주\(`?w`?\)|주 단위"),
    ("밀리초",    r"['\"]ms['\"]|millis",                   r"밀리초|`?ms`?"),
    ("공백 허용", r"\.strip\(\)|replace\(['\"] ['\"]|\\s\+", r"공백"),
    ("역변환",    r"def\s+format_duration|def\s+to_string", r"역변환"),
]

bad = 0
for name, code_pat, spec_pat in FEATURES:
    in_code     = bool(re.search(code_pat, code))
    is_promised = bool(re.search(spec_pat, PROMISED))
    is_excluded = bool(re.search(spec_pat, EXCLUDED))
    if in_code and is_excluded:
        print("CONFLICT  %-10s 명세가 '범위 밖' 이라고 한 것이 코드에 있다" % name); bad += 1
    elif in_code and not is_promised:
        print("DRIFT     %-10s 코드에 있는데 명세가 약속하지 않았다" % name); bad += 1
    elif is_promised and not in_code:
        print("MISSING   %-10s 명세가 약속했는데 코드에 없다" % name); bad += 1
    else:
        print("ok        %-10s" % name)

print("\n문제 %d건" % bad)
sys.exit(1 if bad else 0)
EOF
python3 drift.py; echo "exit $?"
```

원래대로 되돌려서 검사기가 깨끗한 코드도 올바르게 판정하는지 확인한다.

```bash
cd ~/cc-lab/work/sdd/gated
cp duration.py duration.py.drifted
cp duration.py.clean duration.py
echo "── 깨끗한 코드에 대고"
python3 drift.py; echo "exit $?"
echo "── 수용 기준도 여전히 통과하나"
python3 accept.py | tail -1
```

### 기대 결과

게이트는 표류를 통과시킨다.

```
── 게이트는 통과했나
14:20:07 시도#0 rc=0 | 17/17 통과
── 새 기능이 실제로 붙었나
  '1d'     -> 86400
  '1h 30m' -> 5400
```

순진한 검사기는 **아무 문제도 못 찾는다.**

```
ok     일 단위 — 코드 True / 명세 True
ok     공백 허용 — 코드 True / 명세 True
표류 0건
```

명세를 다시 보면 이유가 나온다.

```
── 명세에서 '일' 과 '공백' 이 나오는 곳
44:- 일(`d`)·주(`w`)·밀리초(`ms`) 단위는 이번 범위가 아니다.
46:- 공백을 허용하는 표기(`1h 30m`)는 이번 범위가 아니다.
```

**두 단어가 나오는 곳은 `## 범위 밖` 절이었다.** 순진한 검사기는 명세 전체를 한 덩어리로 봤기 때문에 "금지"를 "약속"으로 읽었다.

절을 구분하는 검사기는 잡는다.

```
CONFLICT  일 단위     명세가 '범위 밖' 이라고 한 것이 코드에 있다
ok        주 단위
ok        밀리초
CONFLICT  공백 허용   명세가 '범위 밖' 이라고 한 것이 코드에 있다
ok        역변환

문제 2건
exit 1
```

깨끗한 코드로 되돌리면:

```
ok        일 단위
ok        주 단위
ok        밀리초
ok        공백 허용
ok        역변환

문제 0건
exit 0
── 수용 기준도 여전히 통과하나
17/17 통과
```

**반드시 확인할 것**은 세 가지다.

1. 게이트가 `rc=0` 으로 표류를 **통과시켰다.**
2. `drift_naive.py` 가 `표류 0건` 이라고 **틀린 답을 냈다.**
3. `drift.py` 가 `CONFLICT` 를 **1건 이상** 잡았다.

`CONFLICT` 가 두 건이 아니라 한 건일 수 있다. 모델이 일 단위만 붙이고 공백 처리는 안 했거나, 정규식 패턴이 그 구현 방식과 안 맞을 수 있다. **한 건 이상이면 통과다.**

### 이 실습의 진짜 교훈

`drift_naive.py` 는 실제로 이 강의 자료를 만들면서 처음 쓴 검사기다. 그리고 통과했다. `표류 0건` 을 보고 "잘 되네" 하고 넘어갈 수 있었다.

**검사기가 통과했다는 것이 코드가 옳다는 뜻이 아니다.** 검사기가 잘못된 질문을 물었을 수도 있다. 그래서 **검사기를 만들면 반드시 실패하는 경우로 시험해야 한다.** `C4-3`에서 거짓 주장을 일부러 섞은 것과 같은 이유다.

세 번 반복된 원칙을 정리하면 이렇다.

| 실습 | 판정기 | 실패 케이스로 검증했나 |
|---|---|---|
| C1-4 | `grade.py` | 스킬을 치우고 대조군을 돌렸다 |
| C4-3 | `check_claims.py` | 거짓 인용을 섞어 FAIL 을 확인했다 |
| C5-4 | `drift.py` | 표류를 만든 뒤 CONFLICT 를 확인했다 |

**판정기를 신뢰하는 유일한 근거는 그것이 실패를 잡는 것을 본 적이 있다는 사실이다.**

### 막히면

| 증상 | 원인 | 조치 |
|---|---|---|
| 새 기능이 안 붙음 | 모델이 명세를 읽고 거부했다 | 프롬프트에 "기존 동작 유지" 를 강조하고 다시 |
| `CONFLICT` 가 0건 | 정규식이 구현과 안 맞는다 | `grep -n "86400\|strip" duration.py` 로 확인 후 패턴 보강 |
| `MISSING` 이 잔뜩 | 절 이름이 명세와 다르다 | `grep '^## ' spec.md` 로 절 이름 확인 |
| 되돌린 뒤에도 CONFLICT | `duration.py.clean` 이 없다 | 백업을 안 떴다. `C5-3`을 다시 돌린다 |

### 이어지는 곳

이 실습편이 끝났다. 마지막 절에서 지금까지 만든 것들을 하나로 조립하는 방법을 정리한다.

:::diagram
id: cc-drift-sections
원본: (신규 작도)
제목: 절을 구분하지 않으면 금지가 약속으로 읽힌다
내용: 순진한 검사기와 절 인식 검사기가 같은 명세를 다르게 읽는 과정
:::

---

## 마치며 — 스물세 개를 조립하면

이 실습편에서 만든 것을 파일 목록으로 보면 이렇다.

```bash
cd ~/cc-lab
find . -path ./node_modules -prune -o -type f \
  \( -name "*.sh" -o -name "*.py" -o -name "*.md" -o -name "*.json" \) -print \
  | grep -v "^./work/sdd/round[AP]" | sort
```

이 파일들은 각각 하나의 개념에 대응한다.

| 만든 것 | 개념 | 어느 실습 |
|---|---|---|
| `.claude/skills/*/SKILL.md` | 절차적 지식 | C1-1, C1-2 |
| `notes_server.py` | 커넥터 | C1-3 |
| `bench/grade.py` | LLM 없는 판정기 | C1-4 |
| `.claude/settings.json` 의 `permissions` | 승인 사다리 | C2-1 |
| `CLAUDE.md` | 폴더 규칙 · 프로젝트 기억 | C2-2, C4-1 |
| `.claude/hooks/guard-bash.sh` | 실행 직전 게이트 | C2-3 |
| `.claude/hooks/test-gate.sh` | 종료 직전 게이트 | C2-4 |
| `inventory.sh` · `.claude/agents/` | 공급망 감사 · 문맥 격리 | C2-5 |
| `loop/tick.sh` | 모델 없는 루프 | C3-1 |
| `loop/gated-tick.sh` | 변화 감지 게이트 | C3-2 |
| `loop/resume-tick.sh` · `state.json` | 이어하기 상태 | C3-3 |
| `cost.py` | 비용 관측 | C3-4 |
| `journey.py` | 발자국 그래프 | C4-2 |
| `check_claims.py` | 근거 검증기 | C4-3 |
| `work/sdd/*/spec.md` | 명세 | C5-1 |
| `.claude/commands/clarify.md` | 인터뷰 도구 | C5-2 |
| `accept.py` | 수용 기준 게이트 | C5-3 |
| `drift.py` | 표류 검사기 | C5-4 |

### 조립하면 무엇이 되는가

이 스물세 개는 따로 배웠지만 하나의 시스템을 이룬다. 밤새 도는 신뢰할 수 있는 에이전트는 이렇게 생겼다.

```
[cron] 5분마다 loop/tick.sh                        ← C3-1
  └ 관측 결과 해시가 달라졌나?                      ← C3-2
      ├ 아니오 → 끝. 비용 0.
      └ 예 → state.json 에서 다음 할 일 하나 꺼낸다  ← C3-3
            └ claude -p --max-budget-usd 0.50       ← C3-4
                ├ CLAUDE.md 규칙 아래에서            ← C2-2
                ├ permissions 안에서만 도구를 쓰고    ← C2-1
                ├ PreToolUse 훅이 위험한 명령을 막고  ← C2-3
                ├ 스킬이 산출물 형식을 고정하고       ← C1-1
                ├ 커넥터로만 외부 데이터를 읽고       ← C1-3
                └ Stop 훅이 accept.py 를 통과할 때만
                  끝나게 한다                        ← C2-4, C5-3
            └ 산출물을 check_claims.py 로 대조       ← C4-3
                ├ FAIL → state.json 을 되돌리고 기록
                └ PASS → done.md 에 추가, 커서 증가
  └ 주 1회: drift.py 로 명세 대조                    ← C5-4
  └ 상시: journey.py · cost.py 로 관측               ← C3-4, C4-2
```

**이 그림에 모델은 한 곳에만 나온다.** 나머지는 전부 모델을 감싼 층이다. 그게 이 강의 다섯 모듈의 요지다.

### 다음에 할 것

세 가지를 권한다.

**첫째, 이 폴더를 git 저장소로 만들어 커밋한다.** `.claude/` 와 `CLAUDE.md` 를 커밋하면 그것이 팀의 에이전트 설정이 된다. `secrets/` 는 `.gitignore` 에 넣는다.

```bash
cd ~/cc-lab
printf 'secrets/\nloop/.last-hash\n*.bak\n__pycache__/\n' > .gitignore
git init -q 2>/dev/null
git config user.name  >/dev/null 2>&1 || git config user.name  "실습"
git config user.email >/dev/null 2>&1 || git config user.email "lab@example.com"
git add -A && git commit -qm "에이전트 실습 환경" && git log --oneline
```

**둘째, 실제 일에 하나만 옮긴다.** 스물세 개를 다 쓰지 않는다. 지금 하는 일에서 가장 자주 반복되는 것 하나를 골라 스킬로 만들고, 가장 무서운 것 하나를 골라 훅으로 막는다. 그 둘만으로도 체감이 크다.

**셋째, Hermes 트랙도 해 본다.** 같은 개념을 다른 도구로 한 번 더 하면, 개념이 도구에서 분리된다. 그러면 다음에 만나는 세 번째 도구는 문서 한 번 훑고 쓸 수 있게 된다.

## 이해도 점검

**1. `--permission-prompts none` 을 붙이면 `permissions.ask` 에 있는 명령은 어떻게 되는가?**

답: 거부된다. `ask` 는 "사람에게 물어본다"는 뜻이고, 비대화 모드에는 물어볼 사람이 없기 때문이다. 낮에 대화형으로 잘 돌던 설정이 밤에 cron 에서 전부 막히는 흔한 원인이다. 자동화용 설정은 `ask` 를 쓰지 않고 `allow` 와 `deny` 로만 구성해야 한다. (C2-1)

**2. `PreToolUse` 훅이 `exit 2` 로 도구를 막으면 에이전트는 어떻게 되는가?**

답: 멈추지 않는다. 그 도구 호출만 실행되지 않고, 훅이 표준 에러에 쓴 문장이 모델에게 전달된다. 모델은 그 문장을 읽고 다른 방법을 찾는다. `C2-3`에서 `rm` 이 막힌 뒤 `mv` 로 우회한 것이 그 예다. 그래서 차단 메시지에는 "대신 이렇게 해라"를 써 주는 것이 좋다. (C2-3)

**3. `Stop` 훅에 상한을 두지 않으면 무슨 일이 일어나는가?**

답: 테스트가 통과할 수 없는 이유가 코드 밖에 있으면(라이브러리 미설치, 환경 변수 누락, 모순된 수용 기준) 에이전트가 영원히 고치고 영원히 막힌다. 매 시도마다 모델 호출이 나가므로 비용도 무한히 늘어난다. 시도 횟수를 파일에 세고 상한에서 통과시켜야 한다. (C2-4)

**4. 변화 감지 게이트의 관측 스크립트에 `date` 를 넣으면 무슨 일이 일어나는가?**

답: 매 틱의 해시가 달라져 억제가 한 번도 일어나지 않는다. 게이트가 있는데도 절약이 0이 된다. 관측 출력에는 시각·난수·프로세스 ID가 들어가면 안 되고, 목록은 반드시 정렬해야 한다. (C3-2)

**5. `--continue` 와 `CLAUDE.md` 는 둘 다 "기억"인데 무엇이 다른가?**

답: 수명과 대상이 다르다. `--continue` 는 그 폴더의 **마지막 세션 하나**를 이어받는다. 세션이 길어지면 압축되고, 다른 창에서 세션을 하나 더 만들면 대상이 바뀐다. `CLAUDE.md` 는 **모든 세션이 시작할 때 읽는 파일**이고, 파일로 남아 git 으로 추적되며 팀과 공유된다. 자동화에서는 `--continue` 의 암묵적 대상이 위험하므로 `--session-id` 로 명시하거나 파일에 남겨야 한다. (C4-1)

**6. 근거 검증기에서 인용이 "의미상 같으면" 통과시키면 안 되는 이유는?**

답: 두 가지다. 첫째, 의미 판정에는 다시 LLM이 필요하고, 그러면 판정자가 판정 대상만큼 복잡해져 판정자의 오류를 검증할 수 없다. 둘째, 환각의 흔한 형태는 완전한 창작이 아니라 미세한 변형이다. "도입하지 않는다"에서 "않는다"가 빠지면 정반대가 되는데, 의미 판정기는 이걸 놓칠 수 있고 문자열 대조는 반드시 잡는다. (C4-3)

**7. `C5-3`의 게이트는 표류를 잡지 못한다. 왜인가?**

답: 테스트는 **있는 것**만 검사한다. 명세가 약속한 항목이 동작하는지는 확인하지만, 명세가 금지한 것이 코드에 들어왔는지는 확인하지 않는다. `C5-4`에서 일 단위와 공백 허용을 추가했을 때 수용 기준 17개가 전부 통과한 것이 그 증거다. 초과 표류를 잡으려면 코드에서 명세로 거꾸로 훑는 별도의 검사기가 필요하다. (C5-3, C5-4)

**8. 순진한 표류 검사기가 `표류 0건` 을 낸 이유는?**

답: 명세 전체를 한 덩어리 텍스트로 보고 키워드를 찾았기 때문이다. "일"과 "공백"이라는 단어는 명세에 있었지만, 있던 자리가 `## 범위 밖` 절이었다. 즉 **금지 문장을 약속 문장으로 읽었다.** 검사기는 절을 구분해서, 약속한 절과 금지한 절을 따로 봐야 한다. (C5-4)

**9. 서브에이전트의 결과를 화면이 아니라 파일로 받아야 하는 이유는?**

답: 서브에이전트의 출력은 부모 에이전트에게 **보고**로 들어가고, 부모는 그 보고를 재료로 자기 답을 다시 쓴다. 그래서 서브에이전트가 정확한 형식으로 냈어도 최종 화면에서는 요약되어 사라진다. 파일은 요약되지 않는다. `C2-5`에서 감사자가 `work/audit.md` 에 쓰게 한 이유다. (C2-5)

**10. `--max-budget-usd 0.002` 를 걸었는데 실제로 0.013 달러가 나갔다. 버그인가?**

답: 아니다. 예산은 턴 사이에 검사된다. 진행 중인 턴을 중간에 잘라내지 않으므로 한 턴이 예산을 넘기면 그 턴이 끝난 뒤에 중단된다. 상한은 정확한 천장이 아니라 **폭주를 멈추는 브레이크**다. 실무에서는 한 턴의 예상 비용보다 충분히 큰 값을 걸고, 정확한 통제는 프롬프트와 도구 범위로 한다. (C3-4)

**11. `Bash(cat:*)` 를 `allow` 에 넣었는데도 `cat secrets/keys.env` 가 거부되었다. 어떤 원리인가?**

답: Claude Code는 도구 이름만 보지 않고 Bash 명령 안의 파일 경로를 읽기 거부 규칙과 대조한다. `Read(./secrets/**)` 가 `deny` 에 있으므로 그 경로에 닿는 Bash 명령도 막힌다. 다만 이 동작에 의존해서는 안 된다. 확실한 차단은 `C2-3`처럼 훅으로 이중 방어하는 것이다. (C2-1)

**12. 스킬에 `allowed-tools` 를 걸었는데도 에이전트가 파일을 만들었다. 설정이 안 먹은 것인가?**

답: 아닐 수 있다. `allowed-tools` 는 **그 스킬이 활성인 동안**의 제한이다. 모델이 스킬을 아예 쓰지 않기로 정하면 그 제한도 적용되지 않는다. 스킬 층의 제한은 협조적이고, 강제가 필요하면 `permissions` 나 훅으로 내려가야 한다. (C1-2)

## 실습 과제

**과제 1. 이어하기 루프를 커서에서 집합으로 바꾼다.**

`C3-3`의 `state.json` 은 `cursor` 하나로 진행을 관리한다. 그래서 실습 중에 새로 넣은 `inbox/004.txt` 를 영원히 무시했다. 이걸 고친다.

- `state.json` 을 `{"done": ["001.txt", ...]}` 형태로 바꾼다.
- 매 틱마다 `inbox/` 를 다시 읽고, `done` 에 없는 것 중 **가장 앞의 하나**만 처리한다.
- 처리 후 `done` 에 추가한다.
- 처리 중 실패하면 `done` 에 넣지 않는다 (다음 틱에 다시 시도한다).
- 새 편지를 하나 넣고 다섯 틱을 돌려, 새 편지가 처리되고 기존 편지는 재처리되지 않는 것을 확인한다.

**왜 이게 과제인가.** 커서는 "어디까지 왔는가"를 말하고 집합은 "무엇을 했는가"를 말한다. 목록이 변하지 않는다면 둘은 같지만, 현실의 목록은 변한다. 이 차이를 직접 겹어 보면 상태 설계에서 무엇을 물어야 하는지 알게 된다. **실패 시 되돌리기**까지 넣는 것이 핵심이다 — 그게 없으면 실패한 항목이 조용히 사라진다.

**과제 2. `C4-3`의 검증기를 `C2-4`의 게이트에 꽂는다.**

지금 `check_claims.py` 는 사람이 손으로 돌린다. 이걸 자동화한다.

- 새 작업 폴더를 만들고 `source.md` 와 `claims.json` 을 둔다.
- `Stop` 훅에 `check_claims.py` 를 걸어, 근거 없는 주장이 하나라도 있으면 끝내지 못하게 한다.
- 차단 사유에 **어느 주장이 왜 실패했는지**를 넣는다.
- 에이전트에게 "source.md 를 요약해서 claims.json 에 써라"만 시키고, 몇 번의 시도 끝에 통과하는지 `gate.log` 로 센다.
- 상한을 반드시 넣는다.

**왜 이게 과제인가.** 검증기가 있어도 사람이 돌려야 한다면 결국 안 돌린다. 판정기를 완료 경로에 꽂는 것까지가 하나의 작업이다. 그리고 이 과제를 하면 `C2-4`(코드 테스트), `C5-3`(수용 기준), 이 과제(근거 검증)가 **모두 같은 구조**라는 것이 보인다. Stop 훅은 "무엇이 참이어야 끝인가"를 꽂는 자리다.

**과제 3. 두 트랙을 한 표로 만든다.**

Hermes 트랙과 Claude Code 트랙을 둘 다 했다면(하나만 했다면 문서를 읽고 추론해도 된다), 다음을 정리한다.

- 이 실습편 앞머리의 대응표에서 **빈칸**을 찾는다.
- 각 빈칸에 대해 "없는 쪽에서 그것을 직접 만들려면 무엇이 필요한가"를 세 줄로 쓴다.
- 그중 하나를 실제로 만든다. 예: Hermes에 `--json-schema` 가 없으니 출력 스키마를 프롬프트와 검증기로 대신 구현한다. 또는 Claude Code에 내장 스케줄러가 없으니 `C3-1`의 루프를 systemd 타이머로 올린다.
- 만든 것과 원래 기능의 차이를 표로 적는다. 무엇이 부족하고, 무엇이 오히려 나은가.

**왜 이게 과제인가.** 도구를 배우는 것과 개념을 배우는 것의 차이가 이 과제에서 갈린다. 없는 기능을 직접 만들어 보면, 있는 기능이 무엇을 대신 해 주고 있었는지 알게 된다. 그리고 이건 취업 후에 실제로 하게 될 일이다 — 회사가 쓰는 에이전트에는 이 강의에서 배운 것 중 절반이 없을 것이고, 나머지 절반을 직접 만들 수 있는 사람이 필요하다.
