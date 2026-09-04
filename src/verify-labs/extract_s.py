# -*- coding: utf-8 -*-
"""lab-cc-steps.md 를 실행 가능한 형태로 옮긴다.

문서는 사람이 하는 그대로 적혀 있다. 셸에 치는 것은 ```bash 블록이고,
클로드코드 창에 치는 말은 ```prompt 블록이다. 이 스크립트는

  * ```bash   → 그대로 실행한다
  * ```prompt → 같은 말을 `claude -p` 로 보낸다 (사람 대신 기계가 창을 대신한다)

로 옮긴다. **프롬프트 문구는 문서에 적힌 것을 한 글자도 바꾸지 않는다.**
울타리 뒤의 꼬리표가 그 프롬프트를 어떤 조건으로 보낼지 정한다.

    ```prompt              기본 (haiku)
    ```prompt write        파일을 쓰게 한다
    ```prompt sonnet write 큰 모델로
    ```prompt continue     직전 대화를 이어서
    ```prompt plan         계획만 세우게 한다
    ```prompt noperm       승인 프롬프트를 끈다 (권한 실습)
    ```prompt schema       $SCHEMA 로 출력 모양을 못 박는다
    ```prompt out=파일     답을 그 파일로 보낸다
"""
import json
import re

SKIP = ("claude.ai/install.sh",)          # 이미 설치돼 있으므로 건너뛴다

WRITE = '--permission-mode acceptEdits --allowedTools "Read" "Write" "Edit" "Bash"'

# 대화창 전용 내장 명령. 이건 기계가 대신할 수 없다.
# (`/clarify` 처럼 프로젝트가 만든 명령은 `-p` 로도 돈다.)
BUILTIN = {"exit", "quit", "cost", "context", "skills", "mcp", "permissions",
           "hooks", "memory", "resume", "help", "model", "clear", "status", "doctor"}


def interactive_only(code):
    t = code.strip()
    if t.startswith("#"):
        return True                    # '#' 는 기억 추가 — 창 전용
    if not t.startswith("/"):
        return False
    return t[1:].split()[0].split("\n")[0] in BUILTIN


# 대화창을 여는 형태만 인정한다. `claude --version` 같은 것은 그냥 명령이다.
OPEN = re.compile(r"^\s*claude(\s+--model\s+\S+|\s+--permission-mode\s+\S+|\s+--safe-mode|\s+--disable-slash-commands)*\s*$")


def opens_window(code):
    """대화창을 여는 줄인가. `claude`, `claude --model haiku` 같은 것."""
    lines = [l for l in code.strip().split("\n") if l.strip()]
    if not lines:
        return None
    last = lines[-1]
    # `cd ... && claude --model haiku` 형태도 받는다
    tail = last.split("&&")[-1].strip()
    if not OPEN.match(tail):
        return None
    m = re.search(r"--model\s+(\S+)", tail)
    return {"model": m.group(1) if m else "haiku",
            "plan": "--permission-mode plan" in tail,
            "prefix": "&&".join(last.split("&&")[:-1]).strip()}


def to_command(text, tags, win=None, first=True):
    model = "sonnet" if "sonnet" in tags else (win or {}).get("model", "haiku")
    opts = ["--model " + model]
    # 창 안에서 이어 치는 말은 같은 대화다. 기계는 --continue 로 잇는다.
    if "continue" in tags or (win is not None and not first):
        opts.insert(0, "--continue")
    if "write" in tags:
        opts.append(WRITE)
    if "plan" in tags:
        opts.append("--permission-mode plan --max-budget-usd 0.2")
    if "noperm" in tags:
        opts.append("--permission-prompts none")
    if "schema" in tags:
        opts.append('--json-schema "$SCHEMA"')
    out = ""
    for t in tags:
        if t.startswith("out="):
            out = " > " + t[4:]
    return ("claude -p \"$(cat <<'YNCPROMPT'\n%s\nYNCPROMPT\n)\" %s 2>/dev/null%s"
            % (text, " ".join(opts), out))


md = open("modules/lab-cc-steps.md", encoding="utf-8").read()

labs, cur, fence, tags, buf = [], None, None, [], []
window, first_in_window = None, True
for ln in md.split("\n"):
    if ln.startswith("```"):
        if fence is None:
            info = ln[3:].strip().split()
            fence = info[0] if info else ""
            tags = info[1:]
            buf = []
        else:
            code = "\n".join(buf)
            if cur is not None and not any(s in code for s in SKIP):
                if fence == "bash":
                    w = opens_window(code)
                    if w is not None:
                        # 창을 여는 줄은 기계가 대신할 수 없다.
                        # 앞에 붙은 `cd ...` 만 살려서 실행한다.
                        window, first_in_window = w, True
                        if w["prefix"]:
                            cur["blocks"].append(w["prefix"])
                        cur["windows"] += 1
                    else:
                        cur["blocks"].append(code)
                        cur["shell"].append(code)
                elif fence == "prompt":
                    # 슬래시 명령과 '#' 기억 추가는 대화창 전용이라 기계가 대신할 수 없다.
                    # 'skip' 꼬리표가 붙은 것도 보여 주기용이라 실행하지 않는다.
                    if code.strip() in ("/exit", "/quit"):
                        window, first_in_window = None, True
                        cur["slash"] += 1
                    elif not interactive_only(code) and "skip" not in tags:
                        cur["blocks"].append(
                            to_command(code, tags, window, first_in_window))
                        first_in_window = False
                        cur["prompts"] += 1
                    else:
                        cur["slash"] += 1
            fence = None
        continue
    if fence is not None:
        buf.append(ln)
        continue
    m = re.match(r"^## (S\d-\d+)\.\s*(.+)$", ln)
    if m:
        cur = {"lab": m.group(1), "title": m.group(2), "blocks": [], "shell": [], "prompts": 0, "slash": 0, "windows": 0}
        labs.append(cur)
        window, first_in_window = None, True
        continue
    if ln.startswith("## 마치며"):
        cur = {"lab": "S-END", "title": "마치며", "blocks": [], "shell": [], "prompts": 0, "slash": 0, "windows": 0}
        labs.append(cur)
        continue
    if ln.startswith("## 이해도 점검"):
        cur = None



# 셸 블록에 자리표시자가 있으면 복사·붙여넣기로 돌지 않는다. 있으면 즉시 실패시킨다.
# (프롬프트 블록은 모델에게 보내는 글이라 따옴표·말줄임표가 정상적으로 들어간다.)
BAD = ('"..."', '"질문"', "<질문", "<위에서", "<세션", "<잡 ", "<이름", "<PATH", "<붙여넣기>")
for l in labs:
    for i, b in enumerate(l["shell"]):
        for pat in BAD:
            assert pat not in b, "%s 셸블록%d 에 자리표시자 %r 이 있다" % (l["lab"], i, pat)
    del l["shell"]

json.dump(labs, open("slabcmds.json", "w"), ensure_ascii=False, indent=1)
print("실습 %d개 · 실행 블록 %d개 (그중 프롬프트 %d개)"
      % (len(labs), sum(len(l["blocks"]) for l in labs), sum(l["prompts"] for l in labs)))
for l in labs:
    print("  %-6s %2d블록 · 창 %d개 · 프롬프트 %2d개 · 슬래시 %d개  %s"
          % (l["lab"], len(l["blocks"]), l["windows"], l["prompts"], l["slash"],
             l["title"][:40]))
