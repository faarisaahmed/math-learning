"""
Page furniture and the block layout engine.

A physical sheet is landscape US Letter, scored down the middle. Each half is a
5.5" x 8.5" worksheet page, so one sheet prints two consecutive pages and is cut
once. A page is a stack of blocks rendered top-down inside the content region.
"""

import math
from dataclasses import dataclass, field
from typing import Callable, List, Optional

import draw as D
from draw import (INK, ACCENT, WARM, MUTED, HAIR, FAINT, TINT,
                  SANS, SANSB, SANSO, NUM, NUMB)

PAGE_W, PAGE_H = 396.0, 612.0     # half of landscape Letter
MARGIN = 26.0
CONTENT_W = PAGE_W - 2 * MARGIN

HEAD_TOP = PAGE_H - 22
FOOT_BOTTOM = 22


# ── blocks ────────────────────────────────────────────────────────────────────

class Block:
    """Renders into (x, y, w) where y is the TOP edge. Returns the new top edge."""
    def draw(self, c, x, y, w, ctx):
        raise NotImplementedError


@dataclass
class Space(Block):
    h: float = 8

    def draw(self, c, x, y, w, ctx):
        return y - self.h


@dataclass
class Rule(Block):
    pad: float = 6
    color: object = HAIR

    def draw(self, c, x, y, w, ctx):
        D.rule(c, x, y - self.pad, x + w, 0.5, self.color)
        return y - self.pad * 2


@dataclass
class Heading(Block):
    label: str
    size: float = 10
    color: object = INK
    pad_below: float = 6

    def draw(self, c, x, y, w, ctx):
        D.text(c, x, y - self.size, self.label, SANSB, self.size, color=self.color)
        return y - self.size - self.pad_below


@dataclass
class Text(Block):
    body: str
    size: float = 8.6
    leading: float = 11
    font: str = SANS
    color: object = INK
    pad_below: float = 6
    align: str = "left"

    def draw(self, c, x, y, w, ctx):
        b = D.paragraph(c, x, y, self.body, w, self.font, self.size,
                        self.leading, self.color, self.align)
        return b - self.pad_below


@dataclass
class Bullets(Block):
    lines: List[str]
    size: float = 8.6
    leading: float = 11
    pad_below: float = 6
    bullet: str = "–"

    def draw(self, c, x, y, w, ctx):
        yy = y
        for ln in self.lines:
            if self.bullet == "arrow":
                D.arrow_glyph(c, x + 1, yy - self.size, self.size, ACCENT)
            else:
                D.text(c, x + 1, yy - self.size, self.bullet, SANS, self.size,
                       color=ACCENT)
            yy = D.paragraph(c, x + 12, yy, ln, w - 12, SANS, self.size,
                             self.leading)
            yy -= 1.5
        return yy - self.pad_below + 1.5


@dataclass
class Canvas(Block):
    """Escape hatch: an arbitrary drawing callback of fixed height."""
    h: float
    fn: Callable
    pad_below: float = 8

    def draw(self, c, x, y, w, ctx):
        self.fn(c, x, y, w)
        return y - self.h - self.pad_below


@dataclass
class Panel(Block):
    """A tinted panel wrapping child blocks. Height is measured, then filled."""
    children: List[Block]
    title: Optional[str] = None
    fill: object = TINT
    stroke: object = None
    pad: float = 8
    pad_below: float = 10
    accent_bar: bool = True

    def draw(self, c, x, y, w, ctx):
        # measure by drawing to a throwaway state, then draw for real
        c.saveState()
        c.setFillColor(D.colors.Color(1, 1, 1, 0))
        c.setStrokeColor(D.colors.Color(1, 1, 1, 0))
        probe = _MutedCanvas(c)
        yy = y - self.pad - (13 if self.title else 0)
        for ch in self.children:
            yy = ch.draw(probe, x + self.pad + 2, yy, w - 2 * self.pad - 4, ctx)
        c.restoreState()
        h = (y - yy) + self.pad

        D.panel(c, x, y, w, h, self.fill, self.stroke)
        if self.accent_bar:
            c.setFillColor(ACCENT)
            c.rect(x, y - h, 2.2, h, stroke=0, fill=1)

        yy = y - self.pad
        if self.title:
            D.text(c, x + self.pad + 2, yy - 9, self.title.upper(), SANSB, 7.2,
                   color=ACCENT, )
            yy -= 13
        for ch in self.children:
            yy = ch.draw(c, x + self.pad + 2, yy, w - 2 * self.pad - 4, ctx)
        return y - h - self.pad_below


class _MutedCanvas:
    """Proxy that swallows drawing ops so Panel can measure its children."""
    def __init__(self, real):
        self._real = real

    def __getattr__(self, name):
        if name in ("stringWidth", "beginPath"):
            return getattr(self._real, name)
        def noop(*a, **k):
            return None
        return noop


@dataclass
class Anchor(Block):
    """Drop to a fixed height above the floor, so the next block sits at the
    bottom of the page instead of floating after the grid."""
    h: float

    def draw(self, c, x, y, w, ctx):
        return min(y, ctx.get("floor", 0) + self.h)


@dataclass
class Reserve(Block):
    """Lower the available area so a later block (a footer panel) has room."""
    h: float
    release: bool = False

    def draw(self, c, x, y, w, ctx):
        ctx["floor"] = ctx.get("floor", 0) + (-self.h if self.release else self.h)
        return y


@dataclass
class Grid(Block):
    """Numbered problem grid."""
    items: List[object]
    cols: int = 2
    gutter: float = 14
    row_pad: float = 2
    pad_below: float = 8
    number: bool = True
    flow: Optional[str] = None      # "column" | "row"; auto if None
    fit: bool = False               # trim to whatever fits above ctx["floor"]
    fill: bool = False              # stretch row spacing to use the whole area

    def _flow(self):
        if self.flow:
            return self.flow
        uniform = (all(getattr(i, "span", 1) == 1 for i in self.items) and
                   len({i.H for i in self.items}) == 1)
        return "column" if uniform else "row"

    def draw(self, c, x, y, w, ctx):
        if not self.items:
            return y
        colw = (w - self.gutter * (self.cols - 1)) / self.cols
        num_w = 17 if self.number else 0
        floor = ctx.get("floor", 0) if self.fit else -1e9

        if self._flow() == "column":
            rh = self.items[0].H + self.row_pad
            rows = math.ceil(len(self.items) / self.cols)
            if self.fit:
                rows = max(1, min(rows, int((y - floor) // rh)))
            take = self.items[:rows * self.cols]
            if self.fill and self.fit and rows:
                rh = max(rh, (y - floor) / rows)
            # a short last column reads badly; rebalance so columns differ by <=1
            rows = math.ceil(len(take) / self.cols)
            for idx, it in enumerate(take):
                col, row = divmod(idx, rows)
                self._one(c, it, x + col * (colw + self.gutter),
                          y - row * rh, colw, num_w, ctx)
            out = y - rows * rh - self.pad_below
            return max(floor, out) if self.fit else out

        # row flow: pack left-to-right honouring span
        cx_i, cy, row_h = 0, y, 0
        for it in self.items:
            span = min(getattr(it, "span", 1), self.cols)
            if cx_i + span > self.cols:
                cy -= row_h + self.row_pad
                cx_i, row_h = 0, 0
            if self.fit and cy - it.H < floor:
                continue        # too tall for what is left; try a shorter one
            cw = colw * span + self.gutter * (span - 1)
            self._one(c, it, x + cx_i * (colw + self.gutter), cy, cw, num_w, ctx)
            row_h = max(row_h, it.H)
            cx_i += span
        cy -= row_h + self.row_pad
        out = cy - self.pad_below
        return max(floor, out) if self.fit else out

    def _one(self, c, it, cx, cy, cw, num_w, ctx):
        if self.number:
            ctx["n"] += 1
            D.text(c, cx + num_w - 6, cy - 12, f"{ctx['n']}", SANS, 7.5,
                   "right", MUTED)
        ctx["items"].append(it)
        it.draw(c, cx + num_w, cy, cw - num_w, key=ctx.get("key", False))


@dataclass
class Strip(Block):
    """A labelled single row of quick items — used for spaced retrieval."""
    label: str
    items: List[object]
    pad_below: float = 10

    def draw(self, c, x, y, w, ctx):
        x0, w0 = x, w
        D.text(c, x, y - 8, self.label.upper(), SANSB, 7.2, color=MUTED)
        yy = y - 15
        n = len(self.items)
        cw = w / n
        for it in self.items:
            ctx["n"] += 1
            ctx["items"].append(it)
            D.text(c, x + 1, yy - 11, f"{ctx['n']}", SANS, 6.8, "left", MUTED)
            it.draw(c, x + 10, yy, cw - 12, key=ctx.get("key", False))
            x += cw
        bot = yy - self.items[0].H
        D.rule(c, x0, bot + 3, x0 + w0, 0.4)
        return bot - self.pad_below


# ── page ──────────────────────────────────────────────────────────────────────

@dataclass
class PageSpec:
    number: int                 # 1..N within the level
    unit: int
    unit_title: str
    title: str
    blocks: List[Block]
    target_time: Optional[str] = None
    kind: str = "practice"      # practice | teach | check
    footnote: Optional[str] = None
    self_check: bool = True
    book_label: str = "BOOK ONE"
    n_items: Optional[int] = None      # filled by a prepass; prints "Score / N"


def draw_page(c, spec: PageSpec, x0: float, key: bool = False, total_pages: int = 200):
    """Render one worksheet page into the half-sheet whose left edge is x0."""
    x = x0 + MARGIN
    w = CONTENT_W
    floor = FOOT_BOTTOM + (44 if spec.self_check else 16)
    ctx = {"n": 0, "items": [], "key": key, "floor": floor}

    # ── header ───────────────────────────────────────────────────────────────
    y = HEAD_TOP
    left = f"{spec.book_label}  ·  UNIT {spec.unit}"
    D.text(c, x, y - 8, left, SANSB, 7.0, color=ACCENT)
    D.text(c, x + w, y - 8, f"{spec.number} / {total_pages}", SANS, 7.0,
           "right", MUTED)
    y -= 20
    D.text(c, x, y - 11, spec.title, SANSB, 12.5)
    if key:
        D.text(c, x + w, y - 11, "ANSWERS", SANSB, 8.5, "right", WARM)
    else:
        D.text(c, x + w, y - 10, spec.unit_title, SANSO, 7.8, "right", MUTED)
    y -= 17
    D.rule(c, x, y, x + w, 0.9, INK)
    y -= 12

    if True:
        # name / date — drawn only on the worksheet, but the space is always
        # reserved so the key and the worksheet lay out identically
        if not key:
            D.text(c, x, y - 8, "Name", SANSB, 7.0, color=MUTED)
            D.rule(c, x + 26, y - 8, x + w * 0.60, 0.5)
            D.text(c, x + w * 0.63, y - 8, "Date", SANSB, 7.0, color=MUTED)
            D.rule(c, x + w * 0.63 + 24, y - 8, x + w, 0.5)
        y -= 17
        if not key:
            # timing + score
            D.text(c, x, y - 8, "Start", SANSB, 7.0, color=MUTED)
            D.rule(c, x + 26, y - 8, x + 78, 0.5)
            D.text(c, x + 84, y - 8, "Finish", SANSB, 7.0, color=MUTED)
            D.rule(c, x + 113, y - 8, x + 165, 0.5)
            if spec.target_time:
                D.text(c, x + 172, y - 8, f"target {spec.target_time}",
                       SANSO, 7.0, color=MUTED)
            if spec.n_items:
                D.text(c, x + w - 78, y - 8, "Score", SANSB, 7.0, color=MUTED)
                D.rule(c, x + w - 52, y - 8, x + w - 22, 0.5)
                D.text(c, x + w - 19, y - 8, f"/ {spec.n_items}", SANS, 7.5,
                       color=MUTED)
            else:
                D.text(c, x + w - 62, y - 8, "Score", SANSB, 7.0, color=MUTED)
                D.rule(c, x + w - 36, y - 8, x + w, 0.5)
        y -= 14
        if not key:
            D.rule(c, x, y, x + w, 0.4)
        y -= 11
        if spec.footnote:
            if not key:
                D.text(c, x, y - 7, spec.footnote, SANSO, 7.4, color=MUTED)
            y -= 15
        else:
            y -= 3

    # ── body ─────────────────────────────────────────────────────────────────
    for b in spec.blocks:
        y = b.draw(c, x, y, w, ctx)

    # ── footer ───────────────────────────────────────────────────────────────
    if key:
        ctx["y_end"] = y
        ctx["overflow"] = 0.0
        return ctx

    vals = [v for it in ctx["items"] for v in it.values()]
    total_items = ctx["n"]
    fy = FOOT_BOTTOM + 34

    if spec.self_check and vals:
        D.rule(c, x, fy + 6, x + w, 0.4)
        D.text(c, x, fy - 3, "SELF-CHECK", SANSB, 7.0, color=ACCENT)
        D.text(c, x + 52, fy - 3,
               f"Add up every number you wrote. The total should be {sum(vals)}.",
               SANS, 7.6, color=INK)
        D.text(c, x, fy - 14, "If it does not match, one answer is wrong — "
                              "find it before you turn the page.",
               SANSO, 7.0, color=MUTED)

        if total_items:
            D.text(c, x + w, fy - 3, f"{total_items} problems", SANS, 7.0,
                   "right", MUTED)

    ctx["y_end"] = y
    ctx["overflow"] = max(0.0, floor - y)
    return ctx
