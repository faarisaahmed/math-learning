"""
The shared machinery: what a unit is, how a page is assembled, and the problem
factories every book draws on.

Two design decisions run through all of it.

1.  Each unit runs a fixed instructional arc rather than twenty identical
    pages: teach -> guided (scaffolds visible) -> practice (scaffolds fading)
    -> applied (word problems) -> interleaved review -> fluency -> mastery
    check. Fading the scaffold is the point; a support that never goes away
    becomes a crutch, and one that is never there leaves the child guessing.

2.  Practice is interleaved and spaced, not blocked. From the second unit
    onward every practice page opens with a short retrieval strip drawn from
    *earlier* units, and the review pages mix operations deliberately. Blocked
    practice produces faster in-session gains and worse retention; this trades
    a little immediate smoothness for durable recall.
"""

import random
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Tuple

import draw as D
from draw import (INK, ACCENT, WARM, MUTED, HAIR, FAINT, TINT, OP_SYM,
                  SANS, SANSB, SANSO, NUM, NUMB)
from layout import (PageSpec, Block, Space, Rule, Heading, Text, Bullets,
                    Canvas, Panel, Grid, Strip, Reserve, Anchor)
import items as I
import wordbank as W

PAGES_PER_UNIT = 20


# ── sampling ──────────────────────────────────────────────────────────────────

def distinct(n, make, tries=500):
    """n items from a generator, rejecting anything already produced."""
    out, seen = [], set()
    for _ in range(tries):
        if len(out) >= n:
            break
        it = make()
        sig = (type(it).__name__, str(it))
        if sig in seen:
            continue
        seen.add(sig)
        out.append(it)
    while len(out) < n:
        out.append(make())
    return out


def draw_n(rng, factories, pool, n, **kw):
    """Sample n distinct items from a weighted list of (weight, factory).

    Repeats are only allowed once the combined pool is genuinely exhausted:
    two identical problems on one page look like a printing error and give the
    child a free answer.
    """
    total = sum(w for w, _ in factories)

    def pick():
        r, acc = rng.random() * total, 0.0
        for w, fac in factories:
            acc += w
            if r <= acc:
                return fac
        return factories[-1][1]

    out, seen, tries = [], set(), 0
    while len(out) < n and tries < n * 150:
        tries += 1
        it = pick()(rng, pool, **kw)
        sig = (type(it).__name__, str(it))
        if sig in seen:
            continue
        seen.add(sig)
        out.append(it)
    while len(out) < n:                      # tiny pool: repeats are unavoidable
        out.append(pick()(rng, pool, **kw))
    return out


def cover_n(rng, pool, n, factories, **kw):
    """Every fact in the pool once before any fact appears twice.

    Speed pages are meant to sweep the whole table, so systematic coverage
    beats random sampling: sampling leaves holes and repeats at the same time.
    """
    facs = [f for _, f in factories]
    out, deck, seen = [], [], set()
    while len(out) < n:
        if not deck:
            deck = [(fact, f) for fact in pool for f in facs]
            rng.shuffle(deck)
        fact, f = deck.pop()
        it = f(rng, [fact], **kw)
        sig = (type(it).__name__, str(it))
        if sig in seen and len(seen) < n:
            continue
        seen.add(sig)
        out.append(it)
    return out


def cap(n, pool, formats=1):
    """Never ask for more distinct problems than the pool can actually supply."""
    return max(1, min(n, len(pool) * formats))


# ── problem factories ─────────────────────────────────────────────────────────
#
# Each takes (rng, pool, **kw) and returns an Item. A pool entry is an (a, b)
# pair read through the unit's operator: (15, 7) means 15 + 7, 15 - 7, 15 x 7
# or 15 ÷ 7 depending on the unit.

def f_plain(rng, pool, op="+", **kw):
    a, b = rng.choice(pool)
    return I.Horizontal(a, b, op)


def f_missing(rng, pool, op="+", **kw):
    a, b = rng.choice(pool)
    hide = "a" if rng.random() < 0.3 else "b"
    return I.MissingSlot(a, b, op, hide)


def f_tf(rng, pool, op="+", **kw):
    a, b = rng.choice(pool)
    r = I.value(a, op, b)
    if rng.random() < 0.5:
        return I.TrueFalse(a, b, r, op)
    offs = [o for o in _wrong_offsets(a, b, op, r) if o != r and o >= 0]
    return I.TrueFalse(a, b, rng.choice(offs or [r + 1]), op)


def _wrong_offsets(a, b, op, r):
    """Wrong answers a child would plausibly produce, not random numbers."""
    if op == "+":
        return [r - 1, r + 1, r - 2, r + 2, r + 10]
    if op == "-":
        return [a + b, r - 1, r + 1, abs(b - a) + 1]
    if op == "*":
        return [a + b, r - a, r + a, r - b]
    return [a - b, r - 1, r + 1, r * 2]


def f_error(rng, pool, op="+", **kw):
    a, b = rng.choice(pool)
    r = I.value(a, op, b)
    offs = [o for o in _wrong_offsets(a, b, op, r) if o != r and o > 0]
    return I.SpotError(a, b, rng.choice(offs or [r + 1]), op)


def f_compare(rng, pool, op="+", **kw):
    a, b = rng.choice(pool)
    c, d = rng.choice(pool)
    if rng.random() < 0.3 and op in "+*":      # guarantee some real equalities
        c, d = b, a
    return I.Compare((a, b), (c, d), op)


def f_balance(rng, pool, op="+", **kw):
    a, b = rng.choice(pool)
    total = I.value(a, op, b)
    if op == "+":
        c = rng.randint(max(0, total - 9), total)
    elif op == "-":
        c = total + rng.randint(0, 9)
    elif op == "*":
        divs = [d for d in range(1, total + 1) if total % d == 0] or [1]
        c = rng.choice(divs)
    else:
        c = total * rng.randint(1, 9)
    return I.Balance(a, b, c, op)


def f_chain(rng, pool, op="+", **kw):
    if op == "-":
        a, b = rng.choice([p for p in pool if p[0] - p[1] >= 3] or pool)
        c = rng.randint(1, max(1, a - b))
        return I.Chain((a, b, c), ("-", "-"))
    cands = [p for p in pool if p[0] + p[1] <= 15] or [(4, 6)]
    a, b = rng.choice(cands)
    c = rng.randint(1, min(9, 20 - a - b))
    nums = [a, b, c]
    rng.shuffle(nums)
    return I.Chain(tuple(nums))


def f_mixed_chain(rng, pool, **kw):
    """`a + b - c` and `a - b + c`, kept inside 0..20 at every step."""
    a, b = rng.choice([p for p in pool if 5 <= p[0] + p[1] <= 18] or [(6, 5)])
    if rng.random() < 0.5:
        c = rng.randint(1, a + b)
        return I.Chain((a, b, c), ("+", "-"))
    lo = min(a, b)
    hi = max(a, b)
    c = rng.randint(1, 20 - (hi - lo))
    return I.Chain((hi, lo, c), ("-", "+"))


def f_muldiv_chain(rng, pool, **kw):
    """`a x b ÷ c` and `a ÷ b x c`, kept whole at every step."""
    a, b = rng.choice([p for p in pool if 2 <= p[0] <= 10 and 2 <= p[1] <= 10]
                      or [(4, 6)])
    prod = a * b
    divs = [d for d in range(2, 11) if prod % d == 0]
    if divs and rng.random() < 0.5:
        return I.Chain((a, b, rng.choice(divs)), ("*", "/"))
    c = rng.randint(2, max(2, min(9, 100 // max(b, 1))))
    return I.Chain((prod, a, c), ("/", "*"))


def f_bondladder(rng, pool, **kw):
    a, b = rng.choice(pool)
    return I.BondLadder(a + b, a)


def f_column(rng, pool, op="+", **kw):
    a, b = rng.choice(pool)
    if op == "-":
        carry = (a % 10) < (b % 10)
    else:
        carry = (a % 10) + (b % 10) >= 10
    return I.Column(a, b, op, carry_box=carry)


def f_frame(rng, pool, **kw):
    a, b = rng.choice([p for p in pool if p[0] + p[1] <= 10] or pool)
    return I.Frame(a, b)


def f_takeaway(rng, pool, **kw):
    a, b = rng.choice([p for p in pool if p[0] <= 10 and p[1] <= p[0]] or pool)
    return I.TakeAwayFrame(a, b)


def f_line(rng, pool, **kw):
    cands = [p for p in pool if p[0] + p[1] <= 10 and p[1] <= 5]
    a, b = rng.choice(cands or pool)
    return I.LineHop(a, b, 10)


def f_lineback(rng, pool, **kw):
    cands = [p for p in pool if p[0] <= 10 and 1 <= p[1] <= 5]
    a, b = rng.choice(cands or pool)
    return I.LineHop(a, b, 10, "-")


def f_countup(rng, pool, **kw):
    cands = [p for p in pool if p[0] <= 20 and p[0] - p[1] <= 6 and p[1] >= 1]
    a, b = rng.choice(cands or pool)
    return I.CountUp(a, b, 20 if a > 10 else 10)


def f_bond(rng, pool, **kw):
    cands = [p for p in pool if p[0] + p[1] <= 20 and p[0] and p[1]]
    big = [p for p in cands if p[0] + p[1] >= 10]
    a, b = rng.choice(big or cands or pool)
    return I.Bond(a + b, (a, b), hide=rng.choice(["p1", "p0", "whole"]))


def f_family(rng, pool, op="+", **kw):
    """A fact-family triangle: three numbers, four facts."""
    if op in "+-":
        cands = [p for p in pool if p[0] and p[1] and p[0] != p[1]]
        a, b = rng.choice(cands or pool)
        if op == "-":
            a, b = a - b, b            # store as the two parts
        return I.FactFamily(a + b, (a, b), "+")
    cands = [p for p in pool if p[0] > 1 and p[1] > 1 and p[0] != p[1]]
    a, b = rng.choice(cands or pool)
    if op == "/":
        a, b = a // b, b
    return I.FactFamily(a * b, (a, b), "*")


def f_maketen(rng, pool, **kw):
    cands = [p for p in pool
             if p[0] + p[1] > 10 and 5 <= p[0] <= 9 and 2 <= p[1] <= 9]
    a, b = rng.choice(cands or [(9, 5)])
    return I.MakeTen(a, b)


def f_breakten(rng, pool, **kw):
    cands = [p for p in pool
             if 11 <= p[0] <= 18 and 2 <= p[1] <= 9 and p[0] - p[1] < 10]
    a, b = rng.choice(cands or [(15, 7)])
    return I.BreakTen(a, b)


def f_array(rng, pool, **kw):
    cands = [p for p in pool if 1 <= p[0] <= 6 and 1 <= p[1] <= 9] or [(3, 4)]
    a, b = rng.choice(cands)
    return I.ArrayItem(a, b)


def f_groups(rng, pool, **kw):
    cands = [p for p in pool if 2 <= p[0] <= 6 and 1 <= p[1] <= 6] or [(3, 4)]
    a, b = rng.choice(cands)
    return I.GroupsItem(a, b)


def f_areasplit(rng, pool, **kw):
    """Break the larger factor at a landmark: ten if there is one, else five."""
    cands = [p for p in pool if p[0] >= 4 and p[1] >= 2] or [(7, 6)]
    a, b = rng.choice(cands)
    split = 10 if a > 10 else 5
    if split >= a:
        split = max(1, a // 2)
    return I.AreaSplit(a, b, split)


def f_skip(rng, pool, **kw):
    steps = sorted({p[1] for p in pool if 2 <= p[1] <= 10}) or [3]
    step = rng.choice(steps)
    blanks = tuple(sorted(rng.sample(range(2, 8), 3)))
    return I.SkipCount(step, 8, blanks)


def f_share(rng, pool, **kw):
    cands = [p for p in pool if 2 <= p[1] <= 6 and p[0] // p[1] <= 6] or [(12, 3)]
    a, b = rng.choice(cands)
    return I.ShareItem(a, b)


def f_partbar(rng, pool, **kw):
    cands = [p for p in pool if 2 <= p[1] <= 8] or [(12, 3)]
    a, b = rng.choice(cands)
    return I.PartBarItem(a, b)


def f_remainder(rng, pool, **kw):
    a, b = rng.choice(pool)
    return I.Remainder(a + rng.randint(1, b - 1) if b > 1 else a + 1, b)


def f_word(rng, pool, op="+", avoid=None, **kw):
    return W.build(rng, pool, op, avoid)


def f_factors(rng, pool, **kw):
    ns = sorted({p[0] * p[1] for p in pool if p[0] > 1 and p[1] > 1
                 and p[0] * p[1] <= 60}) or [12]
    return I.AllFactors(rng.choice(ns))


def f_word3(rng, pool, avoid=None, **kw):
    cands = [p for p in pool if 1 <= p[0] and 1 <= p[1] and p[0] + p[1] <= 15]
    a, b = rng.choice(cands or [(4, 6)])
    c = rng.randint(1, min(9, 20 - a - b))
    story, unit = W.triple_story(rng, a, b, c, avoid)
    return I.Word(story, (a, b, c), unit=unit)


# ── review factories: pools of (a, b, op) triples ────────────────────────────

def r_plain(rng, pool, **kw):
    a, b, op = rng.choice(pool)
    return I.Horizontal(a, b, op)


def r_missing(rng, pool, **kw):
    a, b, op = rng.choice(pool)
    return I.MissingSlot(a, b, op, "a" if rng.random() < 0.3 else "b")


def r_tf(rng, pool, **kw):
    a, b, op = rng.choice(pool)
    return f_tf(rng, [(a, b)], op)


def r_compare(rng, pool, **kw):
    a, b, op = rng.choice(pool)
    c, d, _ = rng.choice([t for t in pool if t[2] == op] or pool)
    return I.Compare((a, b), (c, d), op)


def r_error(rng, pool, **kw):
    a, b, op = rng.choice(pool)
    return f_error(rng, [(a, b)], op)


def r_family(rng, pool, **kw):
    a, b, op = rng.choice(pool)
    return f_family(rng, [(a, b)], op)


def r_word(rng, pool, avoid=None, **kw):
    a, b, op = rng.choice(pool)
    return W.build(rng, [(a, b)], op, avoid)


REVIEW_MIX = [(3, r_plain), (1.4, r_missing), (1, r_compare), (0.8, r_tf),
              (0.5, r_error)]

MIXED_MIX = [(3.2, r_plain), (1.8, r_missing), (1.0, r_compare), (0.8, r_tf),
             (0.6, r_error)]

COMPACT = {f_plain, f_missing, f_tf, f_compare, f_balance, f_chain,
           f_bondladder, f_mixed_chain, f_remainder, f_error,
           r_plain, r_missing, r_tf, r_compare, r_error}


# ── unit and book ────────────────────────────────────────────────────────────

@dataclass
class Unit:
    n: int
    title: str
    strap: str                     # short label shown top-right on every page
    focus: str                     # one-line reminder for the Remember panel
    pool: List[Tuple[int, int]]
    scaffolds: List[Callable]
    mix: List[Tuple[float, Callable]]
    fluency: List[Tuple[float, Callable]]
    remember: Optional[Callable] = None       # (c, x, y, w) mini diagram
    remember_h: float = 0
    teach: Callable = None
    target: str = "4 min"
    fluency_target: str = "3 min"
    op: str = "+"
    kw: dict = field(default_factory=dict)
    late_pool: Optional[List[Tuple[int, int]]] = None
    late_from: int = 10           # unit page at which late_pool takes over
    word_factory: Optional[Callable] = None
    mixed: bool = False           # pool holds (a, b, op) triples, not pairs

    def triples(self):
        return (list(self.pool) if self.mixed
                else [(a, b, self.op) for a, b in self.pool])


ORDINALS = ("", "One", "Two", "Three", "Four", "Five", "Six", "Seven",
            "Eight", "Nine", "Ten")


@dataclass
class Book:
    """One book of the series.

    Books are numbered for sequence, not graded by letter. The number says
    what order to work them in; the title says what is actually inside, which
    is the opposite of hiding the content behind an opaque code.
    """
    n: int
    title: str
    cover_lines: Tuple[str, ...]    # the title, broken by hand for the cover
    slug: str
    subtitle: str
    units: List[Unit]
    blurbs: Dict[int, str]
    after_title: str
    after_body: str
    problems_estimate: str = ""
    halves: Tuple[str, str] = ("Part one", "Part two")
    diagnosis: List[Tuple[str, str]] = field(default_factory=list)
    motif: Optional[Callable] = None      # cover drawing: (c, x, y, w)

    @property
    def ordinal(self):
        return ORDINALS[self.n]

    @property
    def label(self):
        return f"BOOK {self.ordinal.upper()}"

    @property
    def total_pages(self):
        return len(self.units) * PAGES_PER_UNIT


# ── page kinds within a unit ──────────────────────────────────────────────────

def page_kind(i):
    """i is 1..20 within the unit."""
    if i == 1:
        return "teach"
    if i in (2, 3):
        return "guided"
    if 4 <= i <= 13:
        return "practice"
    if i in (14, 15):
        return "applied"
    if i in (16, 17):
        return "review"
    if i in (18, 19):
        return "fluency"
    return "check"


ARC_NOTE = {
    "teach":    "Read this page with someone. Do not time it.",
    "guided":   "The pictures are here to be used. Draw on them.",
    "practice": "Use the method in the box above before you count.",
    "applied":  "Write the number sentence before you write the answer.",
    "review":   "Mixed with earlier units on purpose — that is the point.",
    "fluency":  "Answer on sight. Circle any you had to stop and work out, "
                "then work down the left column first.",
    "check":    "Do it alone, then read the score guide at the foot of the page.",
}


def remember_panel(u: Unit):
    return Panel([Text(u.focus, size=8.6, leading=11, pad_below=4),
                  Canvas(u.remember_h, u.remember, pad_below=0)],
                 title=f"Remember — {u.strap}", fill=TINT, pad_below=11)


def review_facts(book: Book, uidx: int):
    """Every fact from every earlier unit, tagged with its operation."""
    out = []
    for u in book.units[:uidx]:
        out += u.triples()
    return out or book.units[0].triples()


def warmup_strip(rng, book, uidx, n=5):
    pool = review_facts(book, uidx)
    picks, seen = [], set()
    while len(picks) < n and len(seen) < len(pool):
        f = rng.choice(pool)
        if f in seen:
            continue
        seen.add(f)
        picks.append(f)
    return (Strip("Warm-up — from earlier units",
                  [I.Horizontal(a, b, op, size=8.5) for a, b, op in picks]),
            {(a, b) for a, b, _ in picks})


# ── page builder ──────────────────────────────────────────────────────────────

def build_page(book: Book, page_no: int) -> PageSpec:
    uidx = (page_no - 1) // PAGES_PER_UNIT
    i = (page_no - 1) % PAGES_PER_UNIT + 1
    u = book.units[uidx]
    kind = page_kind(i)
    rng = random.Random(9173 * page_no + 41 + 7919 * book.n)
    pool = u.late_pool if (u.late_pool and i >= u.late_from) else u.pool
    kw = dict(u.kw) if u.mixed else dict(u.kw, op=u.op)

    common = dict(number=page_no, unit=u.n, unit_title=u.strap, kind=kind,
                  book_label=book.label)
    # a mixed-operation unit carries (a, b, op) triples, so it needs the
    # review-style factories rather than the single-operator ones
    plain, missing = (r_plain, r_missing) if u.mixed else (f_plain, f_missing)

    def unique(its):
        seen, out = set(), []
        for it in its:
            sig = (type(it).__name__, str(it))
            if sig not in seen:
                seen.add(sig)
                out.append(it)
        return out

    def tall_first(its):
        """Group equal heights together so no grid row leaves a ragged gap."""
        return sorted(its, key=lambda it: (getattr(it, "span", 1), -it.H))

    if kind == "teach":
        return PageSpec(title=u.title, blocks=u.teach(), target_time=None,
                        self_check=False, footnote=ARC_NOTE["teach"], **common)

    if kind == "guided":
        blocks, used = [remember_panel(u)], set()
        if uidx > 0:
            strip, used = warmup_strip(rng, book, uidx, 5)
            blocks.append(strip)
        # same area budget as the practice pages: four ten-frames fit where
        # only two fact-family triangles do
        budget, sc = 150.0, []
        for cand in distinct(6, lambda: rng.choice(u.scaffolds)(rng, u.pool,
                                                                **kw)):
            cost = cand.H if getattr(cand, "span", 1) == 2 else cand.H / 2
            if cost > budget:
                continue
            sc.append(cand)
            budget -= cost
        blocks += [Heading("With a picture", 9, ACCENT, 6),
                   Grid(tall_first(sc), cols=2)]
        gp = [f for f in u.pool if f not in used] or u.pool
        pl = draw_n(rng, [(1, plain)], gp, cap(26, gp), **kw)
        blocks += [Heading("On your own", 9, ACCENT, 6),
                   Grid(pl, cols=2, fit=True)]
        return PageSpec(title=u.title, blocks=blocks, target_time=None,
                        footnote=ARC_NOTE["guided"], **common)

    if kind == "practice":
        fade = (i - 4) / 9.0          # 0 at page 4 -> 1 at page 13
        blocks, used = [], set()
        if i <= 8:
            blocks.append(remember_panel(u))
        if uidx > 0:
            strip, used = warmup_strip(rng, book, uidx, 5)
            blocks.append(strip)
        pool = [f for f in pool if f not in used] or pool
        picture = {f_frame, f_line, f_bond, f_takeaway, f_lineback, f_countup,
                   f_array, f_groups, f_share, f_partbar}
        mix = u.mix if fade < 0.7 else [(w, f) for w, f in u.mix
                                        if f not in picture]
        # budget scaffolds by the space they occupy, not by count: a fact
        # family triangle is three times the height of a ten-frame
        budget = 150 * (1 - fade) if i <= 9 else 0
        visual = []
        for cand in distinct(6, lambda: rng.choice(u.scaffolds)(rng, pool, **kw)):
            cost = cand.H if getattr(cand, "span", 1) == 2 else cand.H / 2
            if cost > budget:
                continue
            visual.append(cand)
            budget -= cost
        flat = draw_n(rng, [(w, f) for w, f in mix if f not in picture],
                      pool, 44, **kw)
        blocks.append(Grid(unique(tall_first(visual) + tall_first(flat)),
                           cols=2, fit=True))
        return PageSpec(title=u.title, blocks=blocks, target_time=u.target,
                        footnote=ARC_NOTE["practice"], **common)

    if kind == "applied":
        blocks, used = [], set()
        if uidx > 0:
            strip, used = warmup_strip(rng, book, uidx, 5)
            blocks.append(strip)
        pool = [f for f in pool if f not in used] or pool
        maker = u.word_factory or f_word
        seen_templates = set()
        words = distinct(4, lambda: maker(rng, pool, avoid=seen_templates,
                                          **kw))
        blocks += [Heading("Word problems", 9, ACCENT, 6), Grid(words, cols=2)]
        rest = tall_first(draw_n(rng, [(2, plain), (1, missing)],
                                 pool, 30, **kw))
        blocks += [Heading("Practice", 9, ACCENT, 6),
                   Grid(rest, cols=2, fit=True)]
        return PageSpec(title=u.title, blocks=blocks, target_time=u.target,
                        footnote=ARC_NOTE["applied"], **common)

    if kind == "review":
        rp = review_facts(book, uidx) + u.triples() * 2
        its = draw_n(rng, REVIEW_MIX, rp, 46)
        scope = ("Everything from Unit 1 so far, shuffled." if u.n == 1 else
                 f"Everything from Unit 1 to Unit {u.n}, shuffled.")
        blocks = [Panel([Text(scope + " Mixing topics feels harder than "
                              "practising one at a time — that extra effort "
                              "is what makes it stick.",
                              size=8.4, leading=10.5, pad_below=0)],
                        title="Mixed review", fill=FAINT, pad_below=11),
                  Grid(tall_first(its), cols=2, fit=True)]
        return PageSpec(title="Mixed Review", blocks=blocks,
                        target_time=u.target, footnote=ARC_NOTE["review"],
                        **common)

    if kind == "fluency":
        its = cover_n(rng, pool, cap(56, pool, len(u.fluency)), u.fluency, **kw)
        return PageSpec(title=u.title, blocks=[Grid(its, cols=2, fit=True)],
                        target_time=u.fluency_target,
                        footnote=ARC_NOTE["fluency"], **common)

    # ── mastery check ────────────────────────────────────────────────────────
    cmix = [(w, f) for w, f in u.mix if f in COMPACT] or [(1, plain)]
    cpool = u.late_pool or u.pool
    n_tall = 4 if f_column in [f for _, f in u.mix] else 0
    its = draw_n(rng, cmix, cpool, 20 - n_tall, **kw)
    its = [f_column(rng, cpool, **kw) for _ in range(n_tall)] + its
    its = tall_first(unique(its))

    last = u.n == len(book.units)
    rubric = [
        ("20", "Book complete — well done." if last
         else f"Start Unit {u.n + 1}."),
        ("18–19", "Fix the ones you missed, then move on."),
        ("15–17", f"Redo pages {uidx * 20 + 18}–{uidx * 20 + 19} first."),
        ("under 15", f"Work the unit again from page {uidx * 20 + 1}."),
    ]

    def _rubric(c, x, y, w):
        yy = y - 8
        for score, what in rubric:
            D.text(c, x, yy, score, NUMB, 8, color=ACCENT)
            D.text(c, x + 46, yy, what, SANS, 8)
            yy -= 11

    rh = 11 * len(rubric)
    reserve = rh + 30
    blocks = [Text("Twenty problems on this unit only. Work alone and time "
                   "yourself.", size=8.4, leading=10.5, color=MUTED,
                   pad_below=8),
              Reserve(reserve),
              Grid(its, cols=2, fit=True, fill=True, row_pad=1),
              Reserve(reserve, release=True),
              Anchor(rh + 23),
              Panel([Canvas(rh - 3, _rubric, pad_below=0)],
                    title="What your score means", fill=TINT, pad=6.5,
                    pad_below=0)]
    return PageSpec(title=f"Unit {u.n} Mastery Check", blocks=blocks,
                    target_time=u.target, footnote=ARC_NOTE["check"], **common)


def build_all(book: Book):
    return [build_page(book, p) for p in range(1, book.total_pages + 1)]
