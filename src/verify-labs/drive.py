# -*- coding: utf-8 -*-
"""대화형 클로드코드 창을 유사 터미널로 띄우고, 사람이 치듯 키를 보내고,
화면에 나온 것을 그대로 받아 낸다. 문서의 '화면에 나오는 것' 블록은
전부 이걸로 실제 캡처한 것이다.

    python3 drive.py <작업폴더> <키...>

특수 키:  @down @up @enter @esc @tab @wait[초]
"""
import os
import pty
import select
import sys
import time

from vt import Screen

KEYS = {"@down": "\x1b[B", "@up": "\x1b[A", "@enter": "\r",
        "@esc": "\x1b", "@tab": "\t", "@ctrlc": "\x03", "@ctrlo": "\x0f"}


def main():
    work, keys = sys.argv[1], sys.argv[2:]
    flags = ""
    if keys and keys[0].startswith("--"):
        flags = " " + keys.pop(0)     # 예: "--model haiku" 를 한 인자로 넘긴다
    scr = Screen(100, 46)
    pid, fd = pty.fork()
    if pid == 0:
        os.environ["TERM"] = "xterm-256color"
        os.environ["COLUMNS"] = "100"
        os.environ["LINES"] = "46"
        os.environ.pop("CLAUDE_CODE_SESSION_ID", None)
        os.environ.pop("CLAUDE_CODE_CHILD_SESSION", None)
        os.execvp("bash", ["bash", "-lc", "cd %s && claude%s" % (work, flags)])
        os._exit(1)

    def pump(sec):
        end = time.time() + sec
        while time.time() < end:
            r, _, _ = select.select([fd], [], [], 0.3)
            if r:
                try:
                    d = os.read(fd, 1 << 16)
                except OSError:
                    return
                if not d:
                    return
                scr.feed(d.decode("utf-8", "replace"))

    pump(float(os.environ.get("DRIVE_BOOT", 12)))
    for k in keys:
        if k.startswith("@wait"):
            pump(float(k[5:] or 20))
            continue
        if k.startswith("@"):
            os.write(fd, KEYS[k].encode())
            pump(4)
            continue
        # 사람이 치듯 조금씩 넣고, 잠시 뒤에 따로 Enter 를 친다.
        # (한 번에 몰아 넣으면 붙여넣기로 인식돼 Enter 가 줄바꿈이 된다.)
        for i in range(0, len(k), 40):
            os.write(fd, k[i:i + 40].encode())
            pump(0.4)
        pump(1.5)
        os.write(fd, b"\r")
        pump(float(os.environ.get("DRIVE_WAIT", 35)))
    os.write(fd, b"\x03")
    pump(1)
    os.write(fd, b"\x03")
    pump(2)
    try:
        os.close(fd)
    except OSError:
        pass
    sys.stdout.write(scr.text())


main()
