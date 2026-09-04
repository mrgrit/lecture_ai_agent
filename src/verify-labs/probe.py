# -*- coding: utf-8 -*-
"""세션 기록을 들여다보는 검증용 도구. 학생은 쓰지 않는다.

문서는 사람이 화면으로 확인하도록 적혀 있으므로, 기계는 화면 대신
클로드코드가 남긴 세션 기록(~/.claude/projects/...)을 읽어 판정한다.

    python3 probe.py tools   <폴더>          도구 호출 이름을 한 줄씩
    python3 probe.py skills  <폴더>          발동한 스킬 이름을 한 줄씩
    python3 probe.py text    <폴더>          모델이 낸 텍스트 전부
    python3 probe.py since   <폴더> <초>     최근 N초 안의 기록만 (같은 규칙)
"""
import json
import os
import pathlib
import sys
import time


def records(folder, within=None):
    slug = str(pathlib.Path(folder).resolve()).replace("/", "-")
    root = pathlib.Path.home() / ".claude" / "projects" / slug
    if not root.is_dir():
        return
    now = time.time()
    for f in sorted(root.glob("*.jsonl"), key=lambda x: x.stat().st_mtime):
        if within is not None and now - f.stat().st_mtime > within:
            continue
        for ln in f.open(encoding="utf-8"):
            try:
                yield json.loads(ln)
            except Exception:
                continue


def main():
    what, folder = sys.argv[1], sys.argv[2]
    within = float(sys.argv[3]) if len(sys.argv) > 3 else None
    for d in records(folder, within):
        if d.get("type") != "assistant":
            continue
        for c in (d.get("message") or {}).get("content") or []:
            if not isinstance(c, dict):
                continue
            if what == "text" and c.get("type") == "text":
                print(c.get("text", ""))
            if c.get("type") != "tool_use":
                continue
            if what == "tools":
                print(c.get("name", ""))
            elif what == "skills" and c.get("name") == "Skill":
                print((c.get("input") or {}).get("skill", ""))


main()
