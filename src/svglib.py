# -*- coding: utf-8 -*-
"""Small helpers for hand-authoring consistent, theme-aware inline SVG diagrams.

All colors come from CSS classes defined in the page stylesheet so the drawings
follow the page theme (light / dark) and the per-module accent (--mc).
"""

FS_H = 13.5   # diagram internal heading
FS_T = 12.5   # box title
FS_S = 11.0   # box sub-line
FS_L = 10.5   # edge / axis label
R = 7         # corner radius


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;"))


def tw(s, size):
    """Rough text width estimate that handles Hangul (full width) vs Latin."""
    w = 0.0
    for ch in s:
        o = ord(ch)
        if o >= 0x1100:
            w += size * 1.0
        elif ch in " .,:;'|!ilj()[]":
            w += size * 0.31
        elif ch.isdigit():
            w += size * 0.56
        elif ch.isupper():
            w += size * 0.65
        else:
            w += size * 0.54
    return w


def wrap(s, size, maxw):
    """Wrap a string into lines that fit maxw at the given font size."""
    if tw(s, size) <= maxw:
        return [s]
    words, lines, cur = s.split(" "), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if tw(trial, size) <= maxw or not cur:
            # a single word longer than the box: hard-break it
            if tw(trial, size) > maxw and not cur:
                buf = ""
                for ch in word:
                    if tw(buf + ch, size) > maxw and buf:
                        lines.append(buf)
                        buf = ch
                    else:
                        buf += ch
                cur = buf
                continue
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text(x, y, s, size=FS_S, anchor="middle", cls="d-t", weight=None, halo=False):
    a = ' text-anchor="%s"' % anchor if anchor != "start" else ""
    w = ' font-weight="%s"' % weight if weight else ""
    c = cls + (" d-halo" if halo else "")
    return ('<text x="%g" y="%g" font-size="%g"%s%s class="%s">%s</text>'
            % (x, y, size, a, w, c, esc(s)))


def lines_block(cx, y0, items, size=FS_S, cls="d-t", anchor="middle", lh=1.45, weight=None):
    out = []
    for i, s in enumerate(items):
        out.append(text(cx, y0 + i * size * lh, s, size, anchor, cls, weight))
    return "".join(out)


def box(x, y, w, h, title=None, subs=(), cls="d-box", dash=False, r=R,
        tsize=FS_T, ssize=FS_S, tweight="700", pad=11, tcls=None, scls="d-t d-dim"):
    """Rounded box with a centered title and optional sub-lines, vertically centered."""
    d = ' stroke-dasharray="5 4"' if dash else ""
    parts = ['<rect x="%g" y="%g" width="%g" height="%g" rx="%g" class="%s"%s/>'
             % (x, y, w, h, r, cls, d)]
    tlines = wrap(title, tsize, w - 2 * pad) if title else []
    slines = []
    for s in subs:
        slines.extend(wrap(s, ssize, w - 2 * pad))
    total = len(tlines) * tsize * 1.35 + (len(slines) * ssize * 1.4 if slines else 0)
    if tlines and slines:
        total += 3
    cy = y + h / 2 - total / 2 + tsize * 0.92
    cx = x + w / 2
    for ln in tlines:
        parts.append(text(cx, cy, ln, tsize, "middle", tcls or "d-t", tweight))
        cy += tsize * 1.35
    if slines:
        cy += 3
        for ln in slines:
            parts.append(text(cx, cy - 1, ln, ssize, "middle", scls))
            cy += ssize * 1.4
    return "".join(parts)


def arrow(x1, y1, x2, y2, uid, label=None, dash=False, cls="d-line", lab_dy=-6,
          lab_anchor="middle", lab_dx=0, size=FS_L):
    d = ' stroke-dasharray="5 4"' if dash else ""
    out = ['<line x1="%g" y1="%g" x2="%g" y2="%g" class="%s"%s marker-end="url(#ar-%s)"/>'
           % (x1, y1, x2, y2, cls, d, uid)]
    if label:
        mx, my = (x1 + x2) / 2 + lab_dx, (y1 + y2) / 2 + lab_dy
        out.append(text(mx, my, label, size, lab_anchor, "d-t d-dim", halo=True))
    return "".join(out)


def path(d, uid, cls="d-line", dash=False, marker=True):
    ds = ' stroke-dasharray="5 4"' if dash else ""
    m = ' marker-end="url(#ar-%s)"' % uid if marker else ""
    return '<path d="%s" class="%s" fill="none"%s%s/>' % (d, cls, ds, m)


def line(x1, y1, x2, y2, cls="d-rule", dash=False):
    d = ' stroke-dasharray="5 4"' if dash else ""
    return '<line x1="%g" y1="%g" x2="%g" y2="%g" class="%s"%s/>' % (x1, y1, x2, y2, cls, d)


def chip(x, y, label, size=FS_L, cls="d-chip", tcls="d-chip-t", pad=9, h=20):
    w = tw(label, size) + pad * 2
    return ('<rect x="%g" y="%g" width="%g" height="%g" rx="%g" class="%s"/>%s'
            % (x, y, w, h, h / 2, cls, text(x + w / 2, y + h / 2 + size * 0.36, label, size,
                                            "middle", tcls, "700")), w)


def chip_c(cx, y, label, size=FS_L, cls="d-chip", tcls="d-chip-t", pad=9, h=20):
    """Chip centered horizontally on cx."""
    w = tw(label, size) + pad * 2
    s, _ = chip(cx - w / 2, y, label, size, cls, tcls, pad, h)
    return s


def banner(x, y, w, h, label, size=FS_H, cls="d-banner", tcls="d-banner-t"):
    return ('<rect x="%g" y="%g" width="%g" height="%g" rx="%g" class="%s"/>%s'
            % (x, y, w, h, R, cls,
               text(x + w / 2, y + h / 2 + size * 0.36, label, size, "middle", tcls, "700")))


def arrow_a(x1, y1, x2, y2, uid, label=None, dash=False, lab_dy=-6, lab_dx=0,
            lab_anchor="middle", size=FS_L):
    """Accent-colored arrow (the one edge the figure is arguing about)."""
    d = ' stroke-dasharray="5 4"' if dash else ""
    out = ['<line x1="%g" y1="%g" x2="%g" y2="%g" class="d-line-a"%s marker-end="url(#ara-%s)"/>'
           % (x1, y1, x2, y2, d, uid)]
    if label:
        mx, my = (x1 + x2) / 2 + lab_dx, (y1 + y2) / 2 + lab_dy
        out.append(text(mx, my, label, size, lab_anchor, "d-t d-acc", halo=True, weight="700"))
    return "".join(out)


def path_a(d, uid, dash=False, marker=True):
    ds = ' stroke-dasharray="5 4"' if dash else ""
    m = ' marker-end="url(#ara-%s)"' % uid if marker else ""
    return '<path d="%s" class="d-line-a" fill="none"%s%s/>' % (d, ds, m)


def svg(uid, w, h, aria, body, cls="dia"):
    mk = ('<marker id="%s-%s" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6.5" '
          'markerHeight="6.5" orient="auto-start-reverse">'
          '<path d="M 0 0.8 L 10 5 L 0 9.2 z" class="%s"/></marker>')
    return (
        '<svg viewBox="0 0 %g %g" role="img" aria-label="%s" class="%s" '
        'xmlns="http://www.w3.org/2000/svg" style="width:%gpx;max-width:100%%">'
        '<defs>%s%s</defs>%s</svg>'
        % (w, h, esc(aria), cls, w,
           mk % ("ar", uid, "d-arrowhead"), mk % ("ara", uid, "d-arrowhead-a"), body))


# ---------------------------------------------------------------- containers

def panel(x, y, w, h, title=None, sub=None, cls="d-panel", dash=False,
          pad=14, tsize=FS_H, chip=None, chip_cls="d-chip"):
    """Titled container. Returns (svg, ix, iy, iw, ih) for the inner content area."""
    d = ' stroke-dasharray="6 5"' if dash else ""
    out = ['<rect x="%g" y="%g" width="%g" height="%g" rx="%g" class="%s"%s/>'
           % (x, y, w, h, R + 2, cls, d)]
    iy = y + pad
    if title:
        out.append(text(x + pad, y + pad + tsize * 0.9, title, tsize, "start", "d-t", "700"))
        iy = y + pad + tsize * 1.5
        if sub:
            out.append(text(x + pad, iy + FS_L * 0.9, sub, FS_L, "start", "d-t d-dim"))
            iy += FS_L * 1.7
        if chip:
            cw = tw(chip, FS_L) + 18
            out.append(chip_c(x + w - pad - cw / 2, y + pad - 2, chip, cls=chip_cls))
        out.append(line(x + pad, iy + 2, x + w - pad, iy + 2, "d-rule"))
        iy += 12
    return "".join(out), x + pad, iy, w - 2 * pad, y + h - pad - iy


def note(cx, y, s, w=None, size=FS_L, cls="d-t d-dim", anchor="middle", lh=1.5):
    """Centered note text, auto-wrapped to width w."""
    lines = wrap(s, size, w) if w else [s]
    return lines_block(cx, y, lines, size, cls, anchor, lh)


def hdr(cx, y, s, size=FS_H, cls="d-t"):
    return text(cx, y, s, size, "middle", cls, "700")


def numchip(cx, cy, n, r=10, cls="d-numchip", tcls="d-numchip-t"):
    return ('<circle cx="%g" cy="%g" r="%g" class="%s"/>%s'
            % (cx, cy, r, cls, text(cx, cy + 3.9, str(n), 11, "middle", tcls, "700")))


def cross(cx, cy, r=7, cls="d-bad-s"):
    return ('<line x1="%g" y1="%g" x2="%g" y2="%g" class="%s"/><line x1="%g" y1="%g" x2="%g" y2="%g" class="%s"/>'
            % (cx - r, cy - r, cx + r, cy + r, cls, cx - r, cy + r, cx + r, cy - r, cls))


def check(cx, cy, r=7, cls="d-ok-s"):
    return '<path d="M %g %g L %g %g L %g %g" class="%s" fill="none"/>' % (
        cx - r, cy, cx - r * 0.25, cy + r * 0.7, cx + r, cy - r * 0.8, cls)


def toggle(x, y, on=True, w=34, h=18):
    cls = "d-tog-on" if on else "d-tog-off"
    knob = x + w - h / 2 if on else x + h / 2
    return ('<rect x="%g" y="%g" width="%g" height="%g" rx="%g" class="%s"/>'
            '<circle cx="%g" cy="%g" r="%g" class="d-tog-knob"/>'
            % (x, y, w, h, h / 2, cls, knob, y + h / 2, h / 2 - 3))
