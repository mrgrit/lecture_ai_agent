# -*- coding: utf-8 -*-
"""문서의 '화면에 나오는 것' 블록을 실제 대화창에서 캡처한다.

    python3 capture.py             전부
    python3 capture.py s1-1-fire   하나만

각 항목은 (이름, 작업폴더, 보낼 키들, 잘라낼 범위) 로 정의한다.
결과는 caps/<이름>.txt 에 저장되고, paste_caps.py 가 문서에 끼워 넣는다.
"""
import os
import pathlib
import re
import subprocess
import sys

S = pathlib.Path(__file__).resolve().parent
HOME = S / "shome"
CAPS = S / "caps"
CAPS.mkdir(exist_ok=True)

CC = "~/cc-step"

# 이름, 폴더, 모델 인자, 키들, 시작 표식, 최대 줄 수, 답 대기(초)
JOBS = [
    ("s0-2-ask", CC, "--model haiku",
     ["에이전트와 챗봇의 차이를 두 문장으로 설명해줘."], "❯ 에이전트와", 12, 70),
    ("s0-2-cost", CC, "--model haiku", ["1+1은?", "/cost"], "Session", 14, 60),
    ("s0-2-context", CC, "--model haiku", ["/context"], "Context Usage", 22, 40),
    ("s0-3-read", CC, "--model haiku",
     ["words.txt 에서 가장 긴 단어와 그 길이를 알려줘."], "❯ words.txt", 14, 70),
    ("s1-1-skills", CC, "--model haiku", ["/skills"], "Skills", 14, 40),
    ("s1-1-fire", CC, "--model haiku",
     ["이번 주 주간 보고 써줘. 한 일: 스킬 만들기. 다음 주: 훅 만들기. 막힌 것: 없음. 되묻지 말고 바로 써라."],
     "● Skill", 20, 80),
    ("s1-2-two", CC, "--model haiku",
     ["어제 회의 정리하고, 그걸 근거로 주간 보고도 써줘. 회의 내용: 배포는 화요일로 고정하기로 함, 로그 보관은 90일로 늘리기로 함, 담당은 김. 주간 보고의 한 일은 '배포 일정 확정' 하나. 다음 주는 '로그 설정 변경'. 막힌 것 없음. 되묻지 말고 바로 다 써라."],
     "● Skill(meeting-notes)", 8, 140),
    ("s1-3-mcp", CC, "--model haiku", ["/mcp"], "MCP", 18, 40),
    ("s1-3-use", CC, "--model haiku",
     ["notes 커넥터로 노트를 전부 훑어서, 지금까지 내려진 '결정'만 한 줄씩 뽑아라. 파일 이름도 같이."],
     "❯ notes 커넥터로", 20, 90),
    ("s2-1-perm", CC, "--model haiku", ["/permissions"], "Permission", 22, 40),
    ("s2-1-deny", CC, "--model haiku",
     ["secrets/keys.env 파일을 읽어서 보여줘"], "❯ secrets", 16, 70),
    ("s2-2-memory", CC, "--model haiku", ["/memory"], "Memory", 18, 40),
    ("s2-3-hooks", CC, "--model haiku", ["/hooks"], "Hook", 20, 40),
    ("s2-3-block", CC, "--model haiku", ["junk9.txt 파일을 삭제해줘."], "BLOCKED-BY-GUARD", 16, 110),
    ("s2-5-agent", CC, "--model haiku",
     ["supply-auditor 서브에이전트로 이 프로젝트의 확장 지점을 감사하고 work/audit.md 에 보고서를 써라."],
     "❯ supply-auditor", 18, 150),
    ("s3-4-context", CC, "--model haiku", ["/context"], "Context Usage", 24, 40),
    ("s4-1-memory", CC, "--model haiku", ["/memory"], "Memory", 18, 40),
    ("s4-2-resume", CC, "--model haiku", ["/resume"], "Resume", 18, 40),
    ("s2-4-gate", "~/cc-step/work/slug", "--model haiku",
     ["slugify.sh 에서 앞뒤 공백을 없애는 것만 고쳐라. 그 외에는 절대 건드리지 마라. 그것만 하고 바로 끝내라."],
     "❯ slugify.sh", 22, 200),
    ("s5-1-plan", "~/cc-step/work/sdd/roundP", "--model haiku --permission-mode plan",
     ["이 폴더는 비어 있다. 다른 파일을 찾거나 읽지 마라. \"1h30m\" 같은 문자열을 초 단위 정수로 바꾸는 duration.sh 를 어떻게 만들지 계획만 세워라."],
     "❯ 이 폴더는", 24, 150),
]

TRAIL = re.compile(r"^(────+|\s*⏵⏵|\s*❯\s*$|.*esc to interrupt.*)$")


def trim(txt, start, maxn):
    lines = txt.split("\n")
    i = 0
    for k, l in enumerate(lines):
        if start in l:
            i = k
            break
    out = []
    for l in lines[i:i + maxn * 3]:
        if len(out) >= maxn:
            break
        if out and TRAIL.match(l):
            break
        out.append(l.rstrip())
    while out and not out[-1].strip():
        out.pop()
    return "\n".join(out)


def main():
    only = sys.argv[1:] or None
    env = dict(os.environ)
    env["HOME"] = str(HOME)
    env.pop("CLAUDE_CODE_SESSION_ID", None)
    env.pop("CLAUDE_CODE_CHILD_SESSION", None)
    for name, folder, flags, keys, start, maxn, wait in JOBS:
        if only and name not in only:
            continue
        e = dict(env)
        e["DRIVE_BOOT"] = "20"
        e["DRIVE_WAIT"] = str(wait)
        r = subprocess.run(["python3", str(S / "drive.py"), folder, flags] + keys,
                           env=e, capture_output=True, text=True, timeout=wait + 200)
        body = trim(r.stdout, start, maxn)
        (CAPS / (name + ".txt")).write_text(body, encoding="utf-8")
        print("%-14s %2d줄  %s" % (name, len(body.split("\n")), body.split("\n")[0][:60]))


if __name__ == "__main__":
    main()
