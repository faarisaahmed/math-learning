"""
Problem item types.

Every item knows three things: how to draw itself in a grid cell, what the
correct answer is, and which numbers a child would physically write down (used
for the self-check total at the foot of each page).

A drill book typically has one item type per operation. Varying the *format* is
what stops a child pattern-matching their way through a page without
understanding it, and several of the formats here — fact families,
spot-the-error, arrays, area models — exist specifically to make the structure
visible rather than the procedure repeatable.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Tuple

import draw as D
from draw import (INK, ACCENT, WARM, MUTED, HAIR, FAINT, TINT, OP_SYM,
                  SANS, SANSB, SANSO, NUM, NUMB)


def value(a, op, b):
    """The result of `a op b`. Division here is always exact."""
    if op == "+":
        return a + b
    if op == "-":
        return a - b
    if op == "*":
        return a * b
    if op == "/":
        return a // b
    raise ValueError(op)


def expr(a, op, b):
    return f"{a} {OP_SYM[op]} {b}"


class Item:
    """Base class. `y` passed to draw() is the TOP edge of the row."""
    H = 19          # nominal row height in points
    span = 1        # grid columns consumed
    tag = "fact"    # skill tag

    def draw(self, c, x, y, w, key=False):
        raise NotImplementedError

    def values(self) -> List[int]:
        """Numbers the child writes (for the page self-check)."""
        return []

    def answer(self) -> str:
        """Compact answer string for the answer key."""
        return ""


# ── plain horizontal ──────────────────────────────────────────────────────────

@dataclass
class Horizontal(Item):
    a: int
    b: int
    op: str = "+"
    size: float = 11
    tag: str = "fact"
    H = 19

    @property
    def result(self):
        return value(self.a, self.op, self.b)

    def draw(self, c, x, y, w, key=False):
        base = y - self.size - 1
        adv = D.text(c, x, base, expr(self.a, self.op, self.b) + " =",
                     NUM, self.size)
        bx = x + adv + 5
        if key:
            D.text(c, bx, base, str(self.result), NUMB, self.size, color=ACCENT)
        else:
            D.blank(c, bx, base, min(26, max(14, w - adv - 8)))

    def values(self):
        return [self.result]

    def answer(self):
        return str(self.result)


# ── a blank in any slot: the inverse question ────────────────────────────────

@dataclass
class MissingSlot(Item):
    """`a op b = c` with one of the three numbers replaced by a box.

    Hiding the first or second operand turns a computation into the inverse
    question, which is the same thing as solving an equation. Meeting it here,
    rather than in an algebra class years later, is the point.
    """
    a: int
    b: int
    op: str = "+"
    hide: str = "b"        # "a" | "b" | "c"
    size: float = 11
    tag: str = "missing"
    H = 19

    @property
    def c_(self):
        return value(self.a, self.op, self.b)

    @property
    def result(self):
        return {"a": self.a, "b": self.b, "c": self.c_}[self.hide]

    def draw(self, c, x, y, w, key=False):
        base = y - self.size - 1
        parts = [str(self.a), OP_SYM[self.op], str(self.b), "=", str(self.c_)]
        slot = {"a": 0, "b": 2, "c": 4}[self.hide]
        cx = x
        for i, part in enumerate(parts):
            if i == slot:
                if key:
                    D.text(c, cx, base, part, NUMB, self.size, color=ACCENT)
                    cx += D.width_of(c, part, NUMB, self.size) + 5
                else:
                    D.boxed_blank(c, cx, base, 17, self.size + 3, ACCENT)
                    cx += 22
            else:
                cx += D.text(c, cx, base, part, NUM, self.size) + 5

    def values(self):
        return [self.result]

    def answer(self):
        return str(self.result)


def missing_addend(a, total, first=False):
    """`a + ? = total`, or `? + a = total` when first is set."""
    return (MissingSlot(total - a, a, "+", "a") if first
            else MissingSlot(a, total - a, "+", "b"))


# ── true / false ──────────────────────────────────────────────────────────────

@dataclass
class TrueFalse(Item):
    a: int
    b: int
    claim: int
    op: str = "+"
    size: float = 10
    tag: str = "judge"
    H = 19

    @property
    def ok(self):
        return value(self.a, self.op, self.b) == self.claim

    def draw(self, c, x, y, w, key=False):
        base = y - self.size - 1
        D.text(c, x, base, f"{expr(self.a, self.op, self.b)} = {self.claim}",
               NUM, self.size)
        rx = x + w - 30
        if key:
            D.text(c, rx, base, "T" if self.ok else "F", NUMB, self.size,
                   color=ACCENT)
        else:
            D.text(c, rx, base, "T", SANS, self.size, color=MUTED)
            D.text(c, rx + 12, base, "/", SANS, self.size, color=HAIR)
            D.text(c, rx + 19, base, "F", SANS, self.size, color=MUTED)

    def answer(self):
        return "T" if self.ok else "F"


# ── spot the error ────────────────────────────────────────────────────────────

@dataclass
class SpotError(Item):
    """Someone else's wrong working, to be corrected.

    Finding a mistake in a worked line requires understanding the method, not
    just running it — and the wrong answers here are the specific ones the
    method actually invites, not random numbers.
    """
    a: int
    b: int
    wrong: int
    op: str = "+"
    size: float = 10
    tag: str = "error"
    H = 22

    @property
    def right(self):
        return value(self.a, self.op, self.b)

    def draw(self, c, x, y, w, key=False):
        base = y - self.size - 2
        s = f"{expr(self.a, self.op, self.b)} = {self.wrong}"
        adv = D.text(c, x, base, s, NUM, self.size, color=MUTED)
        D.rule(c, x, base + self.size * 0.32, x + adv, 0.7, WARM)
        bx = x + adv + 8
        if key:
            D.text(c, bx, base, str(self.right), NUMB, self.size, color=ACCENT)
        else:
            D.boxed_blank(c, bx, base, 20, self.size + 3, ACCENT)

    def values(self):
        return [self.right]

    def answer(self):
        return str(self.right)


# ── compare two expressions ───────────────────────────────────────────────────

@dataclass
class Compare(Item):
    left: Tuple[int, ...]
    right: Tuple[int, ...]
    op: str = "+"
    size: float = 10
    tag: str = "compare"
    H = 19

    def _val(self, t):
        out = t[0]
        for v in t[1:]:
            out = value(out, self.op, v)
        return out

    @property
    def sym(self):
        l, r = self._val(self.left), self._val(self.right)
        return "<" if l < r else (">" if l > r else "=")

    def _fmt(self, t):
        return f" {OP_SYM[self.op]} ".join(str(v) for v in t)

    def draw(self, c, x, y, w, key=False):
        base = y - self.size - 1
        adv = D.text(c, x, base, self._fmt(self.left), NUM, self.size)
        cx = x + adv + 13
        if key:
            D.text(c, cx, base, self.sym, NUMB, self.size, "center", ACCENT)
        else:
            c.setStrokeColor(ACCENT)
            c.setLineWidth(0.7)
            c.circle(cx, base + self.size * 0.32, 7.2, stroke=1, fill=0)
        D.text(c, cx + 13, base, self._fmt(self.right), NUM, self.size)

    def answer(self):
        return self.sym


# ── chain of three or more numbers ────────────────────────────────────────────

@dataclass
class Chain(Item):
    nums: Tuple[int, ...]
    ops: Optional[Tuple[str, ...]] = None
    size: float = 10.5
    tag: str = "chain"
    H = 19

    def _ops(self):
        return self.ops or ("+",) * (len(self.nums) - 1)

    @property
    def result(self):
        out = self.nums[0]
        for op, n in zip(self._ops(), self.nums[1:]):
            out = value(out, op, n)
        return out

    def _fmt(self):
        s = str(self.nums[0])
        for op, n in zip(self._ops(), self.nums[1:]):
            s += f" {OP_SYM[op]} {n}"
        return s

    def draw(self, c, x, y, w, key=False):
        base = y - self.size - 1
        adv = D.text(c, x, base, self._fmt() + " =", NUM, self.size)
        bx = x + adv + 5
        if key:
            D.text(c, bx, base, str(self.result), NUMB, self.size, color=ACCENT)
        else:
            D.blank(c, bx, base, 22)

    def values(self):
        return [self.result]

    def answer(self):
        return str(self.result)


# ── balance / equivalence ─────────────────────────────────────────────────────

@dataclass
class Balance(Item):
    a: int
    b: int
    c_: int
    op: str = "+"
    size: float = 10.5
    tag: str = "balance"
    H = 19

    @property
    def missing(self):
        """Both sides use the same operator, so the inverse differs per op."""
        total = value(self.a, self.op, self.b)
        if self.op == "+":
            return total - self.c_
        if self.op == "-":
            return self.c_ - total
        if self.op == "*":
            return total // self.c_
        return self.c_ // total

    def draw(self, c, x, y, w, key=False):
        base = y - self.size - 1
        adv = D.text(c, x, base,
                     f"{expr(self.a, self.op, self.b)} = {self.c_} "
                     f"{OP_SYM[self.op]}",
                     NUM, self.size)
        bx = x + adv + 5
        if key:
            D.text(c, bx, base, str(self.missing), NUMB, self.size, color=ACCENT)
        else:
            D.boxed_blank(c, bx, base, 17, self.size + 3, ACCENT)

    def values(self):
        return [self.missing]

    def answer(self):
        return str(self.missing)


# ── number bond ───────────────────────────────────────────────────────────────

@dataclass
class Bond(Item):
    whole: int
    parts: Tuple[int, int]
    hide: str = "p1"          # "whole" | "p0" | "p1"
    tag: str = "bond"
    H = 60
    span = 1

    def draw(self, c, x, y, w, key=False):
        cx = x + w / 2 - 4
        if key:
            D.number_bond(c, cx, y - 2, self.whole, self.parts, blank_slots=())
        else:
            whole = None if self.hide == "whole" else self.whole
            p0 = None if self.hide == "p0" else self.parts[0]
            p1 = None if self.hide == "p1" else self.parts[1]
            D.number_bond(c, cx, y - 2, whole, (p0, p1), blank_slots=(self.hide,))

    def values(self):
        return [self._val()]

    def _val(self):
        return {"whole": self.whole, "p0": self.parts[0],
                "p1": self.parts[1]}[self.hide]

    def answer(self):
        return str(self._val())


# ── fact family ───────────────────────────────────────────────────────────────

@dataclass
class FactFamily(Item):
    """Three numbers, four facts.

    Writing all four from one triangle is the moment subtraction stops being a
    new set of facts to learn and becomes addition read backwards. The same
    item, with op="*", ties division to the times tables.
    """
    whole: int
    parts: Tuple[int, int]
    op: str = "+"             # "+" -> +/- family, "*" -> x/÷ family
    tag: str = "family"
    H = 62
    span = 2

    @property
    def inverse(self):
        return "-" if self.op == "+" else "/"

    def _facts(self):
        p, q, w = self.parts[0], self.parts[1], self.whole
        return [(p, self.op, q, w), (q, self.op, p, w),
                (w, self.inverse, p, q), (w, self.inverse, q, p)]

    def draw(self, c, x, y, w, key=False):
        D.fact_triangle(c, x + 40, y - 1, self.whole, self.parts, self.op)
        ex = x + 96
        colw = (w - 100) / 2
        for i, (a, op, b, r) in enumerate(self._facts()):
            col, row = divmod(i, 2)
            bx = ex + col * colw
            base = y - 16 - row * 22
            adv = D.text(c, bx, base, f"{expr(a, op, b)} =", NUM, 10)
            if key:
                D.text(c, bx + adv + 5, base, str(r), NUMB, 10, color=ACCENT)
            else:
                D.blank(c, bx + adv + 5, base, 22)

    def values(self):
        return [f[3] for f in self._facts()]

    def answer(self):
        return ", ".join(str(f[3]) for f in self._facts())


# ── ten-frames ────────────────────────────────────────────────────────────────

@dataclass
class Frame(Item):
    a: int
    b: int
    tag: str = "frame"
    H = 48

    def draw(self, c, x, y, w, key=False):
        cell = 12.0
        fw = D.ten_frame_width(cell)
        fx = x + max(0, (w - fw) / 2 - 8)
        bot = D.ten_frame(c, fx, y - 2, min(10, self.a + self.b), cell,
                          fill_color=INK, second_color=ACCENT, split_at=self.a)
        extra = self.a + self.b - 10
        base = bot - 12
        adv = D.text(c, fx, base, f"{self.a} + {self.b} =", NUM, 10)
        if key:
            D.text(c, fx + adv + 5, base, str(self.a + self.b), NUMB, 10,
                   color=ACCENT)
        else:
            D.blank(c, fx + adv + 5, base, 20)
        if extra > 0:
            D.text(c, fx + fw + 5, y - 16, f"+{extra}", NUMB, 8, color=WARM)

    def values(self):
        return [self.a + self.b]

    def answer(self):
        return str(self.a + self.b)


@dataclass
class TakeAwayFrame(Item):
    """A full ten-frame with the subtrahend struck out."""
    a: int
    b: int
    tag: str = "frame"
    H = 48

    def draw(self, c, x, y, w, key=False):
        cell = 12.0
        fw = D.ten_frame_width(cell)
        fx = x + max(0, (w - fw) / 2 - 8)
        bot = D.ten_frame(c, fx, y - 2, min(10, self.a), cell,
                          fill_color=INK, cross_from=max(0, self.a - self.b))
        base = bot - 12
        adv = D.text(c, fx, base, f"{self.a} {OP_SYM['-']} {self.b} =", NUM, 10)
        if key:
            D.text(c, fx + adv + 5, base, str(self.a - self.b), NUMB, 10,
                   color=ACCENT)
        else:
            D.blank(c, fx + adv + 5, base, 20)

    def values(self):
        return [self.a - self.b]

    def answer(self):
        return str(self.a - self.b)


# ── number line hops ──────────────────────────────────────────────────────────

@dataclass
class LineHop(Item):
    a: int
    b: int
    hi: int = 10
    op: str = "+"
    tag: str = "line"
    H = 50
    span = 1

    @property
    def result(self):
        return value(self.a, self.op, self.b)

    def draw(self, c, x, y, w, key=False):
        lw = w - 18
        length = self.b if self.op == "+" else -self.b
        bot = D.number_line(c, x, y - 2, lw, 0, self.hi,
                            jumps=[(self.a, length,
                                    f"{'+' if self.op == '+' else OP_SYM['-']}"
                                    f"{self.b}")],
                            label_every=1, mark=[self.a])
        base = bot - 10
        adv = D.text(c, x, base, expr(self.a, self.op, self.b) + " =", NUM, 10)
        if key:
            D.text(c, x + adv + 5, base, str(self.result), NUMB, 10, color=ACCENT)
        else:
            D.blank(c, x + adv + 5, base, 20)

    def values(self):
        return [self.result]

    def answer(self):
        return str(self.result)


@dataclass
class CountUp(Item):
    """`a - b` shown as the gap from b up to a.

    Subtraction has two meanings. Taking away is the one children meet first;
    difference is the one that makes 12 - 9 quick. Showing the hop from 9 up to
    12 is what makes the second meaning available at all.
    """
    a: int
    b: int
    hi: int = 20
    tag: str = "countup"
    H = 50
    span = 1

    def draw(self, c, x, y, w, key=False):
        lw = w - 18
        bot = D.number_line(c, x, y - 2, lw, 0, self.hi,
                            jumps=[(self.b, self.a - self.b, "?")],
                            label_every=2 if self.hi > 12 else 1,
                            mark=[self.b, self.a])
        base = bot - 10
        adv = D.text(c, x, base, expr(self.a, "-", self.b) + " =", NUM, 10)
        if key:
            D.text(c, x + adv + 5, base, str(self.a - self.b), NUMB, 10,
                   color=ACCENT)
        else:
            D.blank(c, x + adv + 5, base, 20)

    def values(self):
        return [self.a - self.b]

    def answer(self):
        return str(self.a - self.b)


# ── bridging scaffolds ────────────────────────────────────────────────────────

@dataclass
class MakeTen(Item):
    """`a + b` routed through ten, written out in full."""
    a: int
    b: int
    tag: str = "maketen"
    H = 21
    span = 2

    @property
    def to_ten(self):
        return 10 - self.a

    @property
    def rest(self):
        return self.b - self.to_ten

    def draw(self, c, x, y, w, key=False):
        base = y - 12
        cx = x + D.text(c, x, base, f"{self.a} + {self.b}", NUM, 11) + 8
        cx += D.text(c, cx, base, "=", NUM, 11) + 6
        cx += D.text(c, cx, base, f"{self.a} + {self.to_ten} +", NUM, 11,
                     color=MUTED) + 5
        cx = _slot(c, cx, base, self.rest, key) + 7
        cx += D.text(c, cx, base, "=  10 +", NUM, 11, color=MUTED) + 5
        cx = _slot(c, cx, base, self.rest, key) + 7
        cx += D.text(c, cx, base, "=", NUM, 11) + 6
        if key:
            D.text(c, cx, base, str(self.a + self.b), NUMB, 11, color=ACCENT)
        else:
            D.blank(c, cx, base, 22)

    def values(self):
        return [self.rest, self.rest, self.a + self.b]

    def answer(self):
        return f"{self.rest},{self.rest},{self.a + self.b}"


@dataclass
class BreakTen(Item):
    """`a - b` routed back through ten: 15 - 7 = 15 - 5 - 2 = 10 - 2 = 8."""
    a: int
    b: int
    tag: str = "breakten"
    H = 21
    span = 2

    @property
    def to_ten(self):
        return self.a - 10

    @property
    def rest(self):
        return self.b - self.to_ten

    def draw(self, c, x, y, w, key=False):
        m = OP_SYM["-"]
        base = y - 12
        cx = x + D.text(c, x, base, f"{self.a} {m} {self.b}", NUM, 11) + 8
        cx += D.text(c, cx, base, "=", NUM, 11) + 6
        cx += D.text(c, cx, base, f"{self.a} {m} {self.to_ten} {m}", NUM, 11,
                     color=MUTED) + 5
        cx = _slot(c, cx, base, self.rest, key) + 7
        cx += D.text(c, cx, base, f"=  10 {m}", NUM, 11, color=MUTED) + 5
        cx = _slot(c, cx, base, self.rest, key) + 7
        cx += D.text(c, cx, base, "=", NUM, 11) + 6
        if key:
            D.text(c, cx, base, str(self.a - self.b), NUMB, 11, color=ACCENT)
        else:
            D.blank(c, cx, base, 22)

    def values(self):
        return [self.rest, self.rest, self.a - self.b]

    def answer(self):
        return f"{self.rest},{self.rest},{self.a - self.b}"


def _slot(c, cx, base, val, key, size=11):
    if key:
        D.text(c, cx, base, str(val), NUMB, size, color=ACCENT)
        return cx + D.width_of(c, str(val), NUMB, size)
    D.boxed_blank(c, cx, base, 16, size + 3, ACCENT)
    return cx + 16


# ── column / vertical form ────────────────────────────────────────────────────

@dataclass
class Column(Item):
    a: int
    b: int
    op: str = "+"
    carry_box: bool = False
    tag: str = "column"
    H = 50
    span = 1

    @property
    def result(self):
        return value(self.a, self.op, self.b)

    def draw(self, c, x, y, w, key=False):
        rx = x + min(w - 12, 58)
        D.column_op(c, rx, y - 20, self.a, self.b, self.op, 12,
                    answer=self.result if key else None,
                    carry_hint=self.carry_box)

    def values(self):
        return [self.result]

    def answer(self):
        return str(self.result)


# ── multiplication pictures ───────────────────────────────────────────────────

@dataclass
class ArrayItem(Item):
    """rows x cols of dots, then the number sentence."""
    rows: int
    cols: int
    tag: str = "array"
    H = 74
    span = 1

    def draw(self, c, x, y, w, key=False):
        cell = min(10.0, (w - 30) / max(self.cols, 1))
        aw, _ = D.array_size(self.cols, self.rows, cell)
        ax = x + max(0, (w - aw) / 2 - 10)
        bot = D.array(c, ax, y - 2, self.cols, self.rows, cell)
        base = bot - 13
        adv = D.text(c, x, base, f"{self.rows} {OP_SYM['*']} {self.cols} =",
                     NUM, 10)
        if key:
            D.text(c, x + adv + 5, base, str(self.rows * self.cols), NUMB, 10,
                   color=ACCENT)
        else:
            D.blank(c, x + adv + 5, base, 22)

    def values(self):
        return [self.rows * self.cols]

    def answer(self):
        return str(self.rows * self.cols)


@dataclass
class GroupsItem(Item):
    """n rings of `per` counters, then the number sentence."""
    n: int
    per: int
    tag: str = "groups"
    H = 62
    span = 1

    def draw(self, c, x, y, w, key=False):
        ring = 12.0
        bot = D.groups(c, x + 2, y - 2, self.n, self.per, ring=ring, gap=5,
                       per_row=4)
        base = bot - 13
        adv = D.text(c, x, base, f"{self.n} {OP_SYM['*']} {self.per} =",
                     NUM, 10)
        if key:
            D.text(c, x + adv + 5, base, str(self.n * self.per), NUMB, 10,
                   color=ACCENT)
        else:
            D.blank(c, x + adv + 5, base, 22)

    def values(self):
        return [self.n * self.per]

    def answer(self):
        return str(self.n * self.per)


@dataclass
class AreaSplit(Item):
    """`a x b` broken into two easier products, with the picture above it."""
    a: int
    b: int
    split: int = 5
    tag: str = "distribute"
    H = 70
    span = 2

    def draw(self, c, x, y, w, key=False):
        bw = min(150, w * 0.42)
        bot = D.area_model(c, x + 14, y - 6, bw, 40, self.a, self.b, self.split)
        base = bot - 13
        m = OP_SYM['*']
        cx = x + D.text(c, x, base, f"{self.a} {m} {self.b}  =", NUM, 11) + 7
        cx += D.text(c, cx, base, f"({self.split} {m} {self.b})  +  "
                                  f"({self.a - self.split} {m} {self.b})",
                     NUM, 11, color=MUTED) + 9
        cx += D.text(c, cx, base, "=", NUM, 11) + 6
        cx = _slot(c, cx, base, self.split * self.b, key) + 6
        cx += D.text(c, cx, base, "+", NUM, 11, color=MUTED) + 6
        cx = _slot(c, cx, base, (self.a - self.split) * self.b, key) + 6
        cx += D.text(c, cx, base, "=", NUM, 11) + 6
        if key:
            D.text(c, cx, base, str(self.a * self.b), NUMB, 11, color=ACCENT)
        else:
            D.blank(c, cx, base, 24)

    def values(self):
        return [self.split * self.b, (self.a - self.split) * self.b,
                self.a * self.b]

    def answer(self):
        return (f"{self.split * self.b},{(self.a - self.split) * self.b},"
                f"{self.a * self.b}")


@dataclass
class SkipCount(Item):
    """A skip-counting run with gaps to fill."""
    step: int
    n: int = 8
    blanks: Tuple[int, ...] = (3, 5, 7)
    tag: str = "skip"
    H = 30
    span = 2

    def _vals(self):
        return [self.step * (i + 1) for i in range(self.n)]

    def draw(self, c, x, y, w, key=False):
        vals = self._vals()
        box = min(26, (w - 30) / self.n - 6)
        D.text(c, x, y - 11, f"count in {self.step}s", SANSO, 7.6, color=MUTED)
        D.skip_track(c, x + 62, y, vals,
                     blanks=() if key else self.blanks, box_w=box, gap=5)
        if key:
            return

    def values(self):
        return [self._vals()[i] for i in self.blanks]

    def answer(self):
        return ",".join(str(self._vals()[i]) for i in self.blanks)


@dataclass
class AllFactors(Item):
    """Every number that divides n exactly.

    Factors are where multiplication stops being a table to recite and starts
    being a property of a number, which is the ground everything from
    simplifying fractions to prime factorisation stands on.
    """
    n: int
    tag: str = "factors"
    H = 21
    span = 2

    def _factors(self):
        return [d for d in range(1, self.n + 1) if self.n % d == 0]

    def draw(self, c, x, y, w, key=False):
        base = y - 12
        cx = x + D.text(c, x, base, f"Every factor of {self.n}:", SANS, 9.5,
                        color=MUTED) + 9
        for f in self._factors():
            if key:
                D.text(c, cx, base, str(f), NUMB, 10, color=ACCENT)
                cx += D.width_of(c, str(f), NUMB, 10) + 12
            else:
                D.boxed_blank(c, cx, base, 18, 14, ACCENT)
                cx += 24

    def values(self):
        return self._factors()

    def answer(self):
        return " ".join(str(f) for f in self._factors())


# ── division pictures ─────────────────────────────────────────────────────────

@dataclass
class ShareItem(Item):
    """`total` counters to be dealt into `parts` equal groups.

    The rings are drawn empty so the child does the sharing. A picture that
    already contains the answer is not a question.
    """
    total: int
    parts: int
    tag: str = "share"
    H = 66
    span = 1

    def draw(self, c, x, y, w, key=False):
        per = self.total // self.parts
        D.text(c, x + 2, y - 8, f"share {self.total} equally", SANSO, 7.4,
               color=MUTED)
        bot = D.groups(c, x + 2, y - 12, self.parts, per, ring=12.0, gap=5,
                       per_row=4, empty=not key)
        base = bot - 11
        adv = D.text(c, x, base, f"{self.total} {OP_SYM['/']} {self.parts} =",
                     NUM, 10)
        if key:
            D.text(c, x + adv + 5, base, str(per), NUMB, 10, color=ACCENT)
        else:
            D.blank(c, x + adv + 5, base, 22)

    def values(self):
        return [self.total // self.parts]

    def answer(self):
        return str(self.total // self.parts)


@dataclass
class PartBarItem(Item):
    """A bar of `total` cut into `parts` equal pieces."""
    total: int
    parts: int
    tag: str = "share"
    H = 54
    span = 1

    def draw(self, c, x, y, w, key=False):
        per = self.total // self.parts
        bot = D.part_bar(c, x + 4, y - 14, w - 20, self.parts, 17,
                         label=self.total,
                         part_label=per if key else None,
                         unknown=not key)
        base = bot - 13
        adv = D.text(c, x, base, f"{self.total} {OP_SYM['/']} {self.parts} =",
                     NUM, 10)
        if key:
            D.text(c, x + adv + 5, base, str(per), NUMB, 10, color=ACCENT)
        else:
            D.blank(c, x + adv + 5, base, 22)

    def values(self):
        return [self.total // self.parts]

    def answer(self):
        return str(self.total // self.parts)


@dataclass
class Remainder(Item):
    """`a ÷ b` with a remainder, written as quotient and remainder."""
    a: int
    b: int
    tag: str = "remainder"
    size: float = 10.5
    H = 19

    @property
    def q(self):
        return self.a // self.b

    @property
    def r(self):
        return self.a % self.b

    def draw(self, c, x, y, w, key=False):
        base = y - self.size - 1
        cx = x + D.text(c, x, base, f"{self.a} {OP_SYM['/']} {self.b} =",
                        NUM, self.size) + 5
        if key:
            D.text(c, cx, base, str(self.q), NUMB, self.size, color=ACCENT)
            cx += D.width_of(c, str(self.q), NUMB, self.size) + 5
        else:
            D.blank(c, cx, base, 18)
            cx += 22
        cx += D.text(c, cx, base, "r", SANSO, self.size - 1, color=MUTED) + 4
        if key:
            D.text(c, cx, base, str(self.r), NUMB, self.size, color=ACCENT)
        else:
            D.blank(c, cx, base, 16)

    def values(self):
        return [self.q, self.r]

    def answer(self):
        return f"{self.q} r {self.r}"


# ── word problem ──────────────────────────────────────────────────────────────

@dataclass
class Word(Item):
    """A story problem with a number-sentence scaffold and an answer line.

    `ask` names which number the question actually wants: None for the result,
    or an index into `nums` when the unknown sits inside the sentence ("how
    many more are needed?", "how many were there to start with?"). Mixing the
    structures is deliberate — a child who only ever meets result-unknown
    stories learns to combine the two visible numbers on sight, which is a
    reading habit, not arithmetic.
    """
    story: str
    nums: Tuple[int, ...]
    ops: Optional[Tuple[str, ...]] = None
    unit: str = ""
    ask: Optional[int] = None    # None -> the answer is the result; else an index
    tag: str = "word"
    H = 58
    span = 2

    def _ops(self):
        return self.ops or ("+",) * (len(self.nums) - 1)

    @property
    def total(self):
        out = self.nums[0]
        for op, n in zip(self._ops(), self.nums[1:]):
            out = value(out, op, n)
        return out

    @property
    def result(self):
        return self.total if self.ask is None else self.nums[self.ask]

    def _sentence(self):
        s = str(self.nums[0])
        for op, n in zip(self._ops(), self.nums[1:]):
            s += f" {OP_SYM[op]} {n}"
        return s + f" = {self.total}"

    def draw(self, c, x, y, w, key=False):
        bot = D.paragraph(c, x, y - 1, self.story, w - 24, SANS, 8.5, 10.5)
        base = bot - 13
        cx = x + D.text(c, x, base, "Number sentence", SANSB, 7.5,
                        color=MUTED) + 7
        if key:
            D.text(c, cx, base, self._sentence(), NUMB, 9, color=ACCENT)
        else:
            for i, op in enumerate((None,) + self._ops()):
                if op:
                    D.text(c, cx, base, OP_SYM[op], NUM, 9, color=HAIR)
                    cx += 11
                D.blank(c, cx, base, 24)
                cx += 27
            D.text(c, cx, base, "=", NUM, 9, color=HAIR)
            D.blank(c, cx + 9, base, 28)

        base -= 13
        cx = x + D.text(c, x, base, "Answer", SANSB, 7.5, color=MUTED) + 7
        if key:
            D.text(c, cx, base, f"{self.result} {self.unit}".strip(),
                   NUMB, 9, color=ACCENT)
        else:
            D.blank(c, cx, base, 30)
            if self.unit:
                D.text(c, cx + 34, base, self.unit, SANSO, 7.6, color=MUTED)

    def values(self):
        return list(self.nums) + [self.total, self.result]

    def answer(self):
        return f"{self._sentence()}, ans {self.result}"


# ── decomposition ladder ──────────────────────────────────────────────────────

@dataclass
class BondLadder(Item):
    total: int
    known: int
    tag: str = "bond"
    H = 19

    def draw(self, c, x, y, w, key=False):
        base = y - 12
        adv = D.text(c, x, base, f"{self.known} +", NUM, 11)
        bx = x + adv + 5
        bx = _slot(c, bx, base, self.total - self.known, key) + 5
        D.text(c, bx, base, f"= {self.total}", NUM, 11)

    def values(self):
        return [self.total - self.known]

    def answer(self):
        return str(self.total - self.known)


# ── back-compatible alias ─────────────────────────────────────────────────────

def MissingAddend(a, total, first=False, **kw):
    return missing_addend(a, total, first)
