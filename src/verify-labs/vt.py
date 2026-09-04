# -*- coding: utf-8 -*-
"""아주 작은 터미널 화면 모형. TUI 가 커서를 옮겨 가며 다시 그리는 화면을
사람이 보는 모양 그대로 재구성한다. 캡처 전용이라 색·서체는 버린다."""
import re


def wide(ch):
    """터미널에서 두 칸을 차지하는 글자인가. 한글·한자·전각 기호."""
    o = ord(ch)
    return (0x1100 <= o <= 0x115F or 0x2E80 <= o <= 0xA4CF or
            0xAC00 <= o <= 0xD7A3 or 0xF900 <= o <= 0xFAFF or
            0xFE30 <= o <= 0xFE6F or 0xFF00 <= o <= 0xFF60 or
            0xFFE0 <= o <= 0xFFE6 or 0x20000 <= o <= 0x3FFFD)


class Screen(object):
    def __init__(self, cols=100, rows=44):
        self.cols, self.rows = cols, rows
        self.buf = [[" "] * cols for _ in range(rows)]
        self.x = self.y = 0
        self.log = []                      # 화면 밖으로 밀려난 줄

    # ---------------------------------------------------------------- 내부
    def _scroll(self):
        self.log.append("".join(self.buf[0]).rstrip())
        self.buf.pop(0)
        self.buf.append([" "] * self.cols)
        self.y = self.rows - 1

    def _put(self, ch):
        w = 2 if wide(ch) else 1
        if self.x + w > self.cols:
            self.x = 0
            self.y += 1
        while self.y >= self.rows:
            self._scroll()
        self.buf[self.y][self.x] = ch
        if w == 2 and self.x + 1 < self.cols:
            self.buf[self.y][self.x + 1] = ""      # 넓은 글자의 뒤 칸은 비운다
        self.x += w

    def _erase_line(self, mode):
        if mode == 0:
            for i in range(self.x, self.cols):
                self.buf[self.y][i] = " "
        elif mode == 1:
            for i in range(0, min(self.x + 1, self.cols)):
                self.buf[self.y][i] = " "
        else:
            self.buf[self.y] = [" "] * self.cols

    def _erase_disp(self, mode):
        if mode == 0:
            self._erase_line(0)
            for r in range(self.y + 1, self.rows):
                self.buf[r] = [" "] * self.cols
        elif mode == 1:
            for r in range(0, self.y):
                self.buf[r] = [" "] * self.cols
            self._erase_line(1)
        else:
            for r in range(self.rows):
                self.buf[r] = [" "] * self.cols

    # ---------------------------------------------------------------- 입력
    def feed(self, data):
        i, n = 0, len(data)
        while i < n:
            c = data[i]
            if c == "\x1b":
                m = re.match(r"\x1b\[([0-9;?]*)([A-Za-z@])", data[i:])
                if m:
                    self._csi(m.group(1), m.group(2))
                    i += m.end()
                    continue
                m = re.match(r"\x1b\][^\x07\x1b]*(\x07|\x1b\\)", data[i:])
                if m:
                    i += m.end()
                    continue
                m = re.match(r"\x1b[()][A-Za-z0-9]", data[i:])
                if m:
                    i += m.end()
                    continue
                i += 2
                continue
            if c == "\n":
                self.y += 1
                self.x = 0
                while self.y >= self.rows:
                    self._scroll()
            elif c == "\r":
                self.x = 0
            elif c == "\b":
                self.x = max(0, self.x - 1)
            elif c == "\t":
                self.x = min(self.cols - 1, (self.x // 8 + 1) * 8)
            elif c >= " ":
                self._put(c)
            i += 1

    def _csi(self, params, final):
        ps = [int(p) for p in params.split(";") if p.isdigit()]
        a = ps[0] if ps else 0
        if final == "H" or final == "f":
            self.y = (ps[0] - 1) if len(ps) > 0 and ps[0] else 0
            self.x = (ps[1] - 1) if len(ps) > 1 and ps[1] else 0
            self.y = max(0, min(self.y, self.rows - 1))
            self.x = max(0, min(self.x, self.cols - 1))
        elif final == "A":
            self.y = max(0, self.y - max(1, a))
        elif final == "B":
            self.y = min(self.rows - 1, self.y + max(1, a))
        elif final == "C":
            self.x = min(self.cols - 1, self.x + max(1, a))
        elif final == "D":
            self.x = max(0, self.x - max(1, a))
        elif final == "G":
            self.x = max(0, min((a or 1) - 1, self.cols - 1))
        elif final == "d":
            self.y = max(0, min((a or 1) - 1, self.rows - 1))
        elif final == "J":
            self._erase_disp(a)
        elif final == "K":
            self._erase_line(a)
        elif final == "L":
            for _ in range(max(1, a)):
                self.buf.insert(self.y, [" "] * self.cols)
                self.buf.pop()
        elif final == "M":
            for _ in range(max(1, a)):
                self.buf.pop(self.y)
                self.buf.append([" "] * self.cols)

    # ---------------------------------------------------------------- 출력
    def text(self, scrollback=True):
        rows = (self.log if scrollback else []) + \
               ["".join(r).rstrip() for r in self.buf]
        out, blank = [], 0
        for r in rows:
            if not r.strip():
                blank += 1
                if blank > 1:
                    continue
            else:
                blank = 0
            out.append(r)
        while out and not out[0].strip():
            out.pop(0)
        while out and not out[-1].strip():
            out.pop()
        return "\n".join(out)
