# -*- coding: utf-8 -*-
"""S 트랙(한 줄씩) 실습을 문서에 적힌 순서 그대로 실행하고 기계로 확인한다.

쓰는 법
    python3 extract_s.py          # lab-cc-steps.md → slabcmds.json
    python3 runs.py               # 24개 구간 전부
    python3 runs.py S2-4 S5-3     # 일부만

격리 환경
    이 스크립트는 같은 폴더의 `shome/` 을 HOME 으로 삼아 실행한다.
    실행 전에 아래처럼 만들어 둔다. (`.claude` 는 심볼릭 링크라 로그인 정보를 공유하고,
    `.claude.json` 은 복사본이라 MCP 등록이 실제 홈을 오염시키지 않는다.)

        mkdir -p shome
        ln -s ~/.claude shome/.claude
        cp ~/.claude.json shome/.claude.json

    지울 때는 반드시 심볼릭 링크를 먼저 지운다.

        rm shome/.claude && rm -rf shome

판정
    구간마다 CHECKS 의 셸 조건을 돌린다. $LOG 는 그 구간의 출력, $H 는 격리 HOME 이다.
"""
import json
import os
import pathlib
import subprocess
import sys
import time

S = pathlib.Path(__file__).resolve().parent
HOME = S / "shome"
LOGS = S / "slogs"
LOGS.mkdir(exist_ok=True)
P = '"$H/cc-step'          # 프로젝트 폴더 접두사

CHECKS = {
    "S0-1": 'grep -q "(Claude Code)" "$LOG" && grep -q "cc-step" "$LOG"'
            ' && test -d ' + P + '"',
    "S0-2": 'grep -q "cache_read_input_tokens" "$LOG"'
            ' && grep -q "total_cost_usd" "$LOG"'
            ' && grep -q \'"result":"\' "$LOG"'
            ' && grep -q "num_turns" "$LOG"',
    "S0-3": 'grep -qE "^(Read|Bash|Glob|Grep)$" "$LOG"'
            ' && grep -q \'"num_turns":2\' "$LOG"'
            ' && grep -q \'"num_turns":1\' "$LOG"',
    "S1-1": 'grep -q "^Skill$" "$LOG" && grep -q \'"skill":"weekly-report"\' "$LOG"'
            ' && test -f ' + P + '/.claude/skills/weekly-report/SKILL.md"'
            ' && ! test -e ' + P + '/.skills-parked/weekly-report"'
            ' && ! grep -q "YNC-REPORT-V1" ' + P + '/noskill.txt"',
    "S1-2": 'grep -q \'"skill":"meeting-notes"\' "$LOG"'
            ' && grep -q \'"skill":"weekly-report"\' "$LOG"'
            ' && test -f ' + P + '/.claude/skills/meeting-notes/SKILL.md"',
    "S1-3": 'grep -q "Connected" "$LOG" && grep -q "mcp__notes__" "$LOG"'
            ' && grep -q "거부: notes 폴더 밖은" "$LOG"'
            ' && grep -q "노트 파일 목록을 돌려준다" "$LOG"'
            ' && test -f ' + P + '/notes_server.py"',
    "S1-4": 'test "$(ls ' + P + '/bench"/haiku-*.txt ' + P + '/bench"/sonnet-*.txt'
            ' 2>/dev/null | wc -l)" -eq 4 && grep -q "마커1" "$LOG"',
    "S2-1": 'test "$(grep -c "토큰유출 0" "$LOG")" -ge 4'
            ' && test -f ' + P + '/a.txt" && ! grep -q "abc123" "$LOG"'
            ' && grep -q "문법 OK" "$LOG"',
    "S2-2": 'grep -q "규칙 준수" "$LOG" && test -f ' + P + '/work/hello.txt"'
            ' && grep -q "YNC-RULES-V1" ' + P + '/CLAUDE.md"',
    "S2-3": 'grep -q "BLOCKED-BY-GUARD" "$LOG"'
            ' && grep -q "exit 2 (2 이어야 차단)" "$LOG"'
            ' && test "$(wc -l < ' + P + '/.claude/guard.log")" -ge 2'
            ' && test -x ' + P + '/.claude/hooks/guard-bash.sh"',
    "S2-4": 'grep -q "5/5 통과" "$LOG"'
            ' && grep -q "rc=0" ' + P + '/work/slug/.claude/gate.log"',
    "S2-5": 'grep -qE "[0-9]+ Agent" "$LOG" && grep -q "guard-bash.sh" "$LOG"'
            ' && grep -q "⟪YNC-AUDIT-V1⟫" ' + P + '/work/audit.md"',
    "S3-1": 'test "$(wc -l < ' + P + '/loop/heartbeat.log")" -eq 4'
            ' && grep -q "exit 10" "$LOG"',
    "S3-2": 'grep -q "억제됨" "$LOG" && grep -q "모델 호출함" "$LOG"'
            ' && grep -q "억제 ·" ' + P + '/loop/gate.log"'
            ' && test -s ' + P + '/loop/digest.md"',
    "S3-3": 'grep -q "할 일 없음" "$LOG"'
            ' && test "$(grep -c . ' + P + '/loop/done.md")" -eq 3'
            ' && test "$(cat ' + P + '/loop/cursor.txt")" = "3"',
    "S3-4": 'grep -q "입력 토큰 합계:" "$LOG" && grep -q "캐시 읽기 합계:" "$LOG"'
            ' && grep -q "budget_exhausted" "$LOG"',
    "S4-1": 'grep -q "## 팀 사실" ' + P + '/CLAUDE.md"'
            ' && grep -q "YNC-RULES-V1" ' + P + '/CLAUDE.md"'
            ' && grep -q "화요일" ' + P + '/mem3.txt"'
            ' && grep -q "90" ' + P + '/mem3.txt"'
            ' && grep -q "3주\\|3 주" ' + P + '/mem5.txt"',
    "S4-2": 'test -s ' + P + '/tools.txt" && grep -q "Skill" "$LOG"'
            ' && grep -q "mcp__notes__" "$LOG" && grep -q "Agent" "$LOG"',
    "S4-3": 'grep -q "0개 실패" "$LOG" && grep -q "2개 실패" "$LOG"'
            ' && grep -q "근거 없음" "$LOG" && test -s ' + P + '/claims.json"',
    "S5-1": 'test -f ' + P + '/work/sdd/roundA/duration.sh"'
            ' && test -f ' + P + '/work/sdd/roundB/duration.sh"'
            ' && grep -qE "^roundA +[0-9]+/16 통과" "$LOG"'
            ' && grep -qE "^roundB +16/16 통과" "$LOG"',
    "S5-2": 'grep -q "⟪YNC-CLARIFY-V1⟫" "$LOG"'
            ' && test -f ' + P + '/.claude/commands/clarify.md"',
    "S5-3": 'grep -q "17/17 통과" "$LOG"'
            ' && grep -q "rc=0" ' + P + '/work/sdd/gated/.claude/gate.log"',
    "S5-4": 'grep -q "CONFLICT" "$LOG" && grep -q "표류 0건" "$LOG"'
            ' && grep -q "문제 0건" "$LOG"',
    "S-END": 'grep -q "에이전트 실습 환경" "$LOG" && test -d ' + P + '/.git"',
}

labs = json.load(open("slabcmds.json", encoding="utf-8"))
only = sys.argv[1:] or None

env = dict(os.environ)
env["HOME"] = str(HOME)
env.pop("CLAUDE_CODE_SESSION_ID", None)
env.pop("CLAUDE_CODE_CHILD_SESSION", None)

results = []
t_all = time.time()
for lab in labs:
    name = lab["lab"]
    if only and name not in only:
        continue
    if not lab["blocks"]:
        continue
    script = "set +e\n" + "\n\n".join(lab["blocks"]) + "\n"
    sp = LOGS / (name + ".sh")
    sp.write_text(script, encoding="utf-8")
    log = LOGS / (name + ".log")
    t0 = time.time()
    with log.open("w", encoding="utf-8") as fh:
        subprocess.run(["bash", str(sp)], stdout=fh, stderr=subprocess.STDOUT,
                       cwd=str(HOME), env=env, timeout=2700)
    dt = time.time() - t0

    chk = CHECKS.get(name)
    ok = None
    if chk:
        cenv = dict(env); cenv["LOG"] = str(log); cenv["H"] = str(HOME)
        ok = subprocess.run(["bash", "-c", chk], env=cenv,
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0
    results.append((name, lab["title"], dt, ok, log.stat().st_size))
    print("%-6s %5.0f초  %-6s  %6d bytes  %s"
          % (name, dt, "PASS" if ok else ("FAIL" if ok is False else "—"),
             log.stat().st_size, lab["title"][:40]), flush=True)

print("\n════════ 요약  (총 %.0f분)" % ((time.time() - t_all) / 60))
bad = [r for r in results if r[3] is False]
print("실습 %d개 실행 · PASS %d · FAIL %d"
      % (len(results), sum(1 for r in results if r[3]), len(bad)))
for r in bad:
    print("  FAIL %s — %s" % (r[0], r[1]))
sys.exit(1 if bad else 0)
