# -*- coding: utf-8 -*-
"""23개 Claude Code 실습을 순서대로 실제 실행하고, 실습마다 기대 결과를 기계로 확인한다."""
import json
import os
import pathlib
import subprocess
import sys
import time

S = pathlib.Path(__file__).resolve().parent
HOME = S / "cchome"
LOGS = S / "cclogs"
LOGS.mkdir(exist_ok=True)

CHECKS = {
    "C0-1": 'grep -q "Running: native" "$LOG" && grep -q "(Claude Code)" "$LOG"',
    "C0-2": 'grep -q "캐시읽기" "$LOG" && grep -q "세션    :" "$LOG" && test -d "$H/cc-lab"',
    "C0-3": 'grep -q "▶ 도구 호출" "$LOG" && grep -q "◀ 도구 결과" "$LOG"'
            ' && grep -q "턴 수: 1" "$LOG"',
    "C1-1": 'grep -q "스킬 도구 호출: True" "$LOG" && grep -q "마커 존재    : True" "$LOG"'
            ' && grep -q "마커 존재: False" "$LOG"'
            ' && test -f "$H/cc-lab/.claude/skills/weekly-report/SKILL.md"'
            ' && ! test -e "$H/cc-lab/.skills-parked/weekly-report"',
    "C1-2": 'grep -q "발동한 스킬 : \\[.*meeting-notes.*weekly-report" "$LOG"'
            ' && test -f "$H/cc-lab/.claude/skills/meeting-notes/SKILL.md"',
    "C1-3": 'grep -q "✔ Connected" "$LOG" && grep -q "mcp__notes__list_notes" "$LOG"'
            ' && grep -q "거부: notes 폴더 밖은" "$LOG"'
            ' && grep -q "노트 파일 목록을 돌려준다" "$LOG"',
    "C1-4": 'test "$(wc -l < "$H/cc-lab/bench/result.tsv")" -ge 3 && grep -q "통과(15점)" "$LOG"',
    "C2-1": 'test "$(grep -c "토큰유출: False" "$LOG")" -ge 4 && test -f "$H/cc-lab/a.txt"'
            ' && ! grep -q "TOKEN=abc123" "$LOG"',
    "C2-2": 'grep -q "work/ 아래 만들어짐" "$LOG"'
            ' && grep -qE "첫 줄 규칙 준수: [0-3]/3" "$LOG"'
            ' && test -f "$H/cc-lab/work/hello.txt"',
    "C2-3": 'test "$(wc -l < "$H/cc-lab/.claude/guard.log")" -ge 2'
            ' && grep -q "BLOCKED-BY-GUARD" "$LOG" && grep -q "exit 2 (2 이어야 차단)" "$LOG"',
    "C2-4": 'grep -q "5/5 통과" "$LOG"'
            ' && grep -q "rc=0" "$H/cc-lab/work/slug/.claude/gate.log"',
    "C2-5": 'grep -q "서브에이전트 수: 1" "$LOG"'
            ' && grep -q "⟪YNC-AUDIT-V1⟫" "$H/cc-lab/work/audit.md"'
            ' && grep -q "PreToolUse" "$LOG"',
    "C3-1": 'test "$(wc -l < "$H/cc-lab/loop/heartbeat.log")" -eq 4'
            ' && grep -q "exit 10" "$LOG"',
    "C3-2": 'grep -q "억제됨" "$LOG" && grep -q "모델 호출함" "$LOG"'
            ' && grep -q "억제 ·" "$H/cc-lab/loop/gate.log"',
    "C3-3": 'grep -q "할 일 없음" "$LOG"'
            ' && test "$(wc -l < "$H/cc-lab/loop/done.md")" -eq 3',
    "C3-4": 'grep -q "error_max_budget_usd" "$LOG" && grep -q "1토큰당" "$LOG"',
    "C4-1": 'grep -q "화요일 포함: True" "$LOG" && grep -q "90일 포함  : True" "$LOG"'
            ' && grep -q "## 팀 사실" "$H/cc-lab/CLAUDE.md"',
    "C4-2": 'grep -q "Skill" "$LOG" && grep -q "mcp__notes__" "$LOG" && grep -q "Agent" "$LOG"'
            ' && test -s "$H/cc-lab/journey.json"',
    "C4-3": 'grep -q "0개 실패" "$LOG" && grep -q "FAIL" "$LOG"'
            ' && grep -q "근거 없음" "$LOG"',
    "C5-1": 'test -f "$H/cc-lab/work/sdd/roundA/duration.py"'
            ' && test -f "$H/cc-lab/work/sdd/roundB/duration.py"'
            ' && grep -qE "^roundA +[0-9]+/15 통과" "$LOG"'
            ' && grep -qE "^roundB +[0-9]+/15 통과" "$LOG"',
    "C5-2": 'grep -q "마커: True" "$LOG" && test -f "$H/cc-lab/.claude/commands/clarify.md"',
    "C5-3": 'grep -q "rc=0" "$H/cc-lab/work/sdd/gated/.claude/gate.log" && grep -q "17/17 통과" "$LOG"',
    "C5-4": 'grep -q "CONFLICT" "$LOG" && grep -q "표류 0건" "$LOG" && grep -q "문제 0건" "$LOG"',
    "C-END": 'grep -q "에이전트 실습 환경" "$LOG" && test -d "$H/cc-lab/.git"',
}

labs = json.load(open("cclabcmds.json", encoding="utf-8"))
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
                       cwd=str(HOME), env=env, timeout=2400)
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
