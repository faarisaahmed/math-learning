"""
Book One, second half: subtraction.

The organising idea is that subtraction is not a second set of facts to learn.
It is the addition facts read backwards. A child who knows 7 + 8 = 15 as one
object — a triangle with 15, 7 and 8 at its corners — already knows 15 - 8 and
15 - 7, and does not have to be drilled into them separately.

That is why Unit 2 of this half is fact families rather than "-3", and why the
bridging unit mirrors the make-ten unit move for move.
"""

import draw as D
from draw import (INK, ACCENT, WARM, MUTED, HAIR, FAINT, TINT, OP_SYM,
                  SANS, SANSB, SANSO, NUM, NUMB)
from layout import (Block, Space, Rule, Heading, Text, Bullets, Canvas,
                    Panel, Grid, Strip)
from teach import idea, watch, worked, why, try_these
import curriculum as C
from curriculum import (Unit, f_plain, f_missing, f_tf, f_compare, f_balance,
                        f_chain, f_mixed_chain, f_column, f_takeaway,
                        f_lineback, f_countup, f_family, f_breakten, f_error,
                        f_bond)
import items as I

M = OP_SYM["-"]


# ── fact pools ────────────────────────────────────────────────────────────────

def _dedupe(pairs):
    seen, out = set(), []
    for p in pairs:
        if p not in seen:
            seen.add(p)
            out.append(p)
    return out


def pool_count_back():
    return _dedupe([(a, b) for b in (1, 2, 3) for a in range(b, 11)])


def pool_families_to_ten():
    return _dedupe([(a, b) for a in range(2, 11) for b in range(1, a)
                    if a <= 10])


def pool_from_ten():
    return _dedupe([(10, b) for b in range(0, 11)] +
                   [(w, b) for w in (8, 9, 10) for b in range(0, w + 1)])


def pool_close_differences():
    """Pairs a - b where the numbers are near each other: count up, not back."""
    return _dedupe([(a, b) for a in range(5, 21) for b in range(1, a)
                    if 1 <= a - b <= 5 and b >= 3])


def pool_within_ten():
    return _dedupe([(a, b) for a in range(0, 11) for b in range(0, a + 1)])


def pool_teen_minus_ones():
    """17 - 4 = 13: the ones digit is big enough that nothing crosses ten."""
    out = []
    for n in range(1, 10):
        for k in range(0, n + 1):
            out.append((10 + n, k))
    out += [(10 + n, 10) for n in range(0, 10)]
    return _dedupe(out)


def pool_bridge_back():
    """15 - 7: the answer is under ten, so the ten has to be broken open."""
    return _dedupe([(a, b) for a in range(11, 19) for b in range(2, 10)
                    if 0 < a - b < 10])


def pool_all_to_twenty():
    return _dedupe([(a, b) for a in range(0, 21) for b in range(0, 11)
                    if a - b >= 0])


def pool_two_digit_sub():
    out = []
    for t in range(2, 10):
        for o in range(0, 10):
            a = t * 10 + o
            for b in range(2, 10):
                if a - b >= 10:
                    out.append((a, b))
    return out


def pool_two_digit_pairs_sub():
    return [(a, b)
            for a in range(21, 100)
            for b in range(11, 60)
            if a - b >= 10 and b < a][:2400]


# ── diagrams for the teaching pages ──────────────────────────────────────────

def _dia_takeaway(c, x, y, w):
    D.text(c, x, y - 8, f"9 {M} 3   —   take three away", SANSB, 8.5)
    D.ten_frame(c, x, y - 16, 9, 13.0, fill_color=INK, cross_from=6)
    D.text(c, x + 76, y - 32, "six are left", SANSO, 8, color=MUTED)
    D.number_line(c, x + 150, y - 10, w - 160, 0, 10,
                  jumps=[(9, -3, f"{M}3")], mark=[9])
    D.text(c, x, y - 62, f"9 {M} 3 = 6", NUMB, 11, color=ACCENT)
    D.text(c, x + 90, y - 62, "nine  →  eight, seven, six", SANSO, 8.2,
           color=MUTED)


def _dia_family(c, x, y, w):
    D.fact_triangle(c, x + 44, y - 2, 15, (7, 8), "+")
    ex = x + 108
    facts = ["7 + 8 = 15", "8 + 7 = 15", f"15 {M} 7 = 8", f"15 {M} 8 = 7"]
    for i, f in enumerate(facts):
        col, row = divmod(i, 2)
        D.text(c, ex + col * 96, y - 18 - row * 18, f, NUMB, 10,
               color=ACCENT if i > 1 else INK)
    D.text(c, ex, y - 62, "One triangle. Four facts. Nothing extra to learn.",
           SANSO, 8, color=MUTED)


def _dia_fromten(c, x, y, w):
    D.ten_frame(c, x, y - 6, 10, 13.0, fill_color=INK, cross_from=6)
    D.text(c, x, y - 48, f"10 {M} 6 = 4", NUMB, 11, color=ACCENT)
    D.text(c, x + 100, y - 20, "because  6 + 4 = 10", NUM, 10, color=INK)
    D.text(c, x + 100, y - 36, "The ten pairs work backwards:", SANS, 8.2,
           color=MUTED)
    D.text(c, x + 100, y - 50,
           f"10{M}1=9   10{M}2=8   10{M}3=7   10{M}4=6   10{M}5=5",
           NUM, 8.2, color=MUTED)
    D.text(c, x + 100, y - 62,
           f"10{M}6=4   10{M}7=3   10{M}8=2   10{M}9=1", NUM, 8.2, color=MUTED)


def _dia_countup(c, x, y, w):
    D.text(c, x, y - 8, f"12 {M} 9   —   the numbers are close together",
           SANSB, 8.5)
    D.number_line(c, x + 6, y - 16, w - 40, 0, 14,
                  jumps=[(9, 3, "?")], mark=[9, 12])
    D.text(c, x, y - 74, "Count UP from 9 to 12: ten, eleven, twelve. "
                         "Three hops.", SANS, 8.4, color=ACCENT)
    D.text(c, x, y - 87, "Counting back from 12 would take nine hops and "
                         "nine chances to slip.", SANSO, 8, color=MUTED)


def _dia_subchooser(c, x, y, w):
    rows = [
        ("taking away 1, 2 or 3", "count back", f"9 {M} 2 → 8, 7"),
        ("the numbers are close", "count up", f"12 {M} 9 → 10, 11, 12"),
        ("taking from 10", "known ten pair", f"10 {M} 6 = 4"),
        ("you know the addition", "read it backwards", f"15 {M} 8 = 7"),
        ("anything else", "break the ten", f"15 {M} 7 → 10 {M} 2"),
    ]
    yy = y - 4
    D.text(c, x + 2, yy - 8, "WHEN YOU SEE", SANSB, 6.8, color=MUTED)
    D.text(c, x + 118, yy - 8, "USE", SANSB, 6.8, color=MUTED)
    D.text(c, x + 210, yy - 8, "LIKE", SANSB, 6.8, color=MUTED)
    yy -= 13
    D.rule(c, x, yy + 2, x + w, 0.5)
    for a, b, ex in rows:
        yy -= 15
        D.text(c, x + 2, yy, a, SANS, 8.4)
        D.text(c, x + 118, yy, b, SANSB, 8.4, color=ACCENT)
        D.text(c, x + 210, yy, ex, NUM, 8.4, color=MUTED)


def _dia_teenminus(c, x, y, w):
    D.text(c, x, y - 8, f"17 {M} 4", SANSB, 10)
    D.ten_frame(c, x, y - 16, 10, 12.0, fill_color=HAIR)
    D.ten_frame(c, x + 70, y - 16, 7, 12.0, fill_color=INK, cross_from=3)
    D.text(c, x + 24, y - 46, "the ten is untouched", SANSO, 7.4, "center",
           MUTED)
    D.text(c, x + 100, y - 46, "take 4 from the 7 ones", SANSO, 7.4, "center",
           MUTED)
    D.text(c, x, y - 64, f"17 {M} 4  =  10 + (7 {M} 4)  =  10 + 3  =  13",
           NUMB, 10.5, color=ACCENT)


def _dia_breakten(c, x, y, w):
    D.text(c, x, y - 8, f"15 {M} 7", SANSB, 10)
    D.ten_frame(c, x, y - 16, 10, 12.0, fill_color=INK, cross_from=8)
    D.ten_frame(c, x + 70, y - 16, 5, 12.0, fill_color=INK, cross_from=0)
    D.text(c, x, y - 46, "2 more from the ten", SANSO, 7.2, color=WARM)
    D.text(c, x + 72, y - 46, "the 5 ones first", SANSO, 7.2, color=WARM)
    yy = y - 64
    D.text(c, x, yy, "15 is 10 and 5. Take the 5 first, then 2 more.",
           SANS, 8.4)
    D.text(c, x, yy - 14, f"15 {M} 7  =  15 {M} 5 {M} 2  =  10 {M} 2  =  8",
           NUMB, 10.5, color=ACCENT)
    D.number_bond(c, x + 262, y - 58, 7, (5, 2), r=9, drop=22, spread=20,
                  size=9)


def _dia_missing(c, x, y, w):
    D.text(c, x, y - 8, f"15 {M} ? = 7   —   draw it as a bar", SANS, 8.8)
    D.bar_model(c, x, y - 22, w * 0.62, 7, 8, 18, labels=("7", "?"),
                total_label="15")
    D.text(c, x, y - 76, "The whole is 15. One part is 7. "
                         "So the other part is 8.", SANS, 8.6, color=ACCENT)
    D.text(c, x, y - 89, f"Check by adding back: 7 + 8 = 15, "
                         f"so 15 {M} 8 = 7 too.", SANSO, 8, color=MUTED)


def _dia_mixed(c, x, y, w):
    D.text(c, x, y - 8, f"8 + 5 {M} 3   —   work left to right", SANSB, 8.5)
    D.seq(c, x, y - 26, ["8 + 5 = 13", f"13 {M} 3 = 10"], NUMB, 10.5, ACCENT,
          gap=8)
    D.rule(c, x, y - 38, x + w, 0.4)
    D.text(c, x, y - 52, "Adding then subtracting the same number "
                         "gets you back where you started:", SANS, 8.4)
    D.seq(c, x, y - 68, [f"9 + 6 = 15", f"15 {M} 6 = 9"], NUMB, 10.5, INK,
          gap=8)
    D.text(c, x, y - 82, "That is why you can always check a subtraction "
                         "by adding your answer back.", SANSO, 8, color=MUTED)


def _dia_twodigitsub(c, x, y, w):
    D.text(c, x, y - 8, f"54 {M} 8", SANSB, 10)
    D.text(c, x, y - 22, "the ones are not enough — go back through 50",
           SANSO, 8, color=MUTED)
    D.text(c, x, y - 38, f"54 {M} 4 {M} 4  =  50 {M} 4  =  46", NUMB, 10.5,
           color=ACCENT)

    D.text(c, x + 186, y - 8, f"76 {M} 23", SANSB, 10)
    D.text(c, x + 186, y - 22, "tens from tens, ones from ones",
           SANSO, 8, color=MUTED)
    D.text(c, x + 186, y - 38, f"70 {M} 20 = 50,  6 {M} 3 = 3  →  53",
           NUMB, 10.5, color=ACCENT)

    D.rule(c, x, y - 52, x + w, 0.4)
    D.column_op(c, x + 62, y - 68, 54, 8, "-", 12, answer=46, carry_hint=True)
    D.column_op(c, x + 248, y - 68, 76, 23, "-", 12, answer=53)
    D.text(c, x + 76, y - 84, "one ten is broken open into ten ones",
           SANSO, 7.4, color=WARM)
    D.text(c, x + 262, y - 84, "nothing to break open here", SANSO, 7.4,
           color=MUTED)


# ── teaching pages ────────────────────────────────────────────────────────────

def unit_1():
    return [
        idea("Subtraction is addition run backwards. Where adding moved you "
             "forward along the number line, taking away moves you back — and "
             "the same counting skill does the work."),
        Canvas(74, _dia_takeaway, pad_below=7),
        worked([f"9 {M} 3 — say the first number: nine.",
                "Count back three: eight, seven, six.",
                "The last number you say is the answer: 6."]),
        watch("Counting back is only quick for 1, 2 or 3. Do not try to count "
              f"back nine hops for 12 {M} 9 — there is a much better method "
              "coming in Unit 14."),
        *try_these([I.LineHop(8, 2, 10, "-"), I.TakeAwayFrame(9, 3),
                    I.Horizontal(7, 1, "-"), I.Horizontal(10, 3, "-"),
                    I.Horizontal(6, 2, "-"), I.Horizontal(9, 1, "-")]),
    ]


def unit_2():
    return [
        idea("Three numbers that make an addition fact also make two "
             "subtraction facts. 7, 8 and 15 belong together: the two parts "
             "and the whole. Learn them as one family and subtraction stops "
             "being a second table to memorise."),
        Canvas(74, _dia_family, pad_below=7),
        worked(["The whole is 15. The parts are 7 and 8.",
                "Adding the parts gives the whole: 7 + 8 = 15.",
                f"Taking one part from the whole leaves the other: 15 {M} 7 = 8."]),
        watch("In a subtraction the whole always comes first. From the family "
              f"6, 4, 10 you can write 10 {M} 6 and 10 {M} 4 — but not "
              f"6 {M} 10."),
        *try_these([I.FactFamily(9, (4, 5)),
                    I.Horizontal(10, 3, "-"), I.Horizontal(10, 7, "-"),
                    I.MissingSlot(8, 5, "-", "b"),
                    I.MissingSlot(9, 6, "-", "a")]),
    ]


def unit_3():
    return [
        idea("You already know the pairs that make ten. Every one of them is "
             "also a subtraction fact, at no extra cost: because 6 and 4 make "
             "10, taking 6 from 10 must leave 4."),
        Canvas(74, _dia_fromten, pad_below=7),
        worked([f"10 {M} 7 — ask which number goes with 7 to make ten.",
                "3 goes with 7.",
                f"So 10 {M} 7 = 3."]),
        watch("If you find yourself counting back seven hops from ten, you are "
              "not using what you know. Recall the pair instead."),
        *try_these([I.Horizontal(10, 6, "-"), I.Horizontal(10, 2, "-"),
                    I.Horizontal(10, 9, "-"), I.Horizontal(10, 4, "-"),
                    I.MissingSlot(10, 3, "-", "b"),
                    I.MissingSlot(10, 8, "-", "b"),
                    I.Horizontal(9, 5, "-"), I.Horizontal(8, 3, "-")]),
    ]


def unit_4():
    return [
        idea("Subtraction asks two different questions. “How many are left?” "
             "means take away. “How many more?” means find the difference — "
             "and a difference is quickest found by counting UP from the "
             "smaller number."),
        Canvas(92, _dia_countup, pad_below=7),
        worked([f"13 {M} 11 — the numbers are close, so count up.",
                "Start at 11 and go up to 13: twelve, thirteen.",
                "Two hops, so the answer is 2."]),
        watch("Choose the method by looking at the numbers first. Far apart, "
              f"with a small second number (9 {M} 2)? Count back. Close "
              f"together (12 {M} 9)? Count up."),
        *try_these([I.CountUp(12, 9, 14), I.CountUp(11, 8, 14),
                    I.Horizontal(13, 10, "-"), I.Horizontal(15, 12, "-"),
                    I.Horizontal(9, 7, "-"), I.Horizontal(14, 11, "-")]),
    ]


def unit_5():
    return [
        idea("You now have four ways to subtract. A fluent child does not use "
             "one method for everything — they glance at the two numbers and "
             "pick the one that suits them."),
        Canvas(94, _dia_subchooser, pad_below=7),
        worked([f"8 {M} 2: small second number → count back → 7, 6.",
                f"10 {M} 3: taking from ten → known pair → 7.",
                f"9 {M} 7: close together → count up from 7 → 2."]),
        watch("Every one of these can also be answered by remembering the "
              "addition fact. If you know 7 + 2 = 9, you do not need any "
              f"method at all for 9 {M} 7."),
        *try_these([I.Horizontal(7, 2, "-"), I.Horizontal(10, 4, "-"),
                    I.Horizontal(9, 6, "-"), I.Horizontal(8, 5, "-"),
                    I.Horizontal(6, 1, "-"), I.Horizontal(10, 7, "-"),
                    I.Horizontal(5, 3, "-"), I.Horizontal(9, 9, "-")]),
    ]


def unit_6():
    return [
        idea("A teen number is one ten and some ones. If you are taking away "
             "no more ones than it already has, the ten never gets touched — "
             "so just subtract inside the ones and put the ten back."),
        Canvas(78, _dia_teenminus, pad_below=7),
        worked([f"18 {M} 5 — 18 is one ten and eight ones.",
                f"Take 5 from the 8 ones: 8 {M} 5 = 3.",
                "Put the ten back: 10 + 3 = 13."]),
        watch("This shortcut only works while the ones are big enough. "
              f"16 {M} 4 is fine, because 6 {M} 4 works. 16 {M} 8 is not, "
              "because 6 is smaller than 8 — that is the next unit."),
        *try_these([I.Horizontal(17, 4, "-"), I.Horizontal(19, 6, "-"),
                    I.Horizontal(15, 3, "-"), I.Horizontal(18, 8, "-"),
                    I.Horizontal(16, 10, "-"), I.Horizontal(14, 2, "-"),
                    I.MissingSlot(19, 7, "-", "b"),
                    I.MissingSlot(17, 5, "-", "b")]),
    ]


def unit_7():
    return [
        idea("When there are not enough ones, break the ten open. Take away "
             "the ones you have first, which lands you exactly on ten, then "
             "take the rest out of the ten. It is the make-ten move from "
             "Unit 7 run in reverse."),
        Canvas(104, _dia_breakten, pad_below=7),
        worked([f"14 {M} 6 — 14 is ten and four ones.",
                f"Take the 4 ones first: 14 {M} 4 = 10.",
                f"Six was needed, four is gone, so 2 are left: 10 {M} 2 = 8."]),
        watch("Split the number you are taking away, and split off exactly the "
              f"ones the first number has. For 15 {M} 7 you take 5 first "
              "(not 7, not 2), because 15 has five ones."),
        *try_these([I.BreakTen(15, 7), I.BreakTen(14, 6),
                    I.BreakTen(13, 8), I.BreakTen(16, 9)], cols=2),
    ]


def unit_8():
    return [
        idea("A missing number can sit anywhere in a subtraction. Drawing the "
             "bar shows you which number is the whole and which are the "
             "parts, and from there the question answers itself."),
        Canvas(96, _dia_missing, pad_below=7),
        worked([f"? {M} 6 = 9 — the whole is missing.",
                "The two parts are 6 and 9.",
                "The whole is 6 + 9 = 15. Check: 15 " + M + " 6 = 9."]),
        watch(f"12 {M} ? = 5 and ? {M} 5 = 12 are different questions. In the "
              "first the whole is 12, so the answer is 7. In the second the "
              "whole is missing, so the answer is 17."),
        *try_these([I.MissingSlot(15, 6, "-", "b"),
                    I.MissingSlot(13, 5, "-", "a"),
                    I.MissingSlot(17, 9, "-", "b"),
                    I.MissingSlot(11, 4, "-", "a"),
                    I.Horizontal(16, 7, "-"), I.Horizontal(14, 9, "-"),
                    I.TrueFalse(15, 8, 7, "-"), I.TrueFalse(12, 5, 8, "-")]),
    ]


def unit_9():
    return [
        idea("Adding and subtracting undo each other. That is useful twice "
             "over: it lets you work along a chain left to right, and it gives "
             "you a way to check every answer you write."),
        Canvas(94, _dia_mixed, pad_below=7),
        worked([f"7 + 8 {M} 5 — do the first step: 7 + 8 = 15.",
                f"Then the second: 15 {M} 5 = 10.",
                f"Check the subtraction by adding back: 10 + 5 = 15. Correct."]),
        watch("Work along the chain in order. Doing the subtraction first "
              f"gives a different answer, and only one of them is right."),
        *try_these([I.Chain((7, 8, 5), ("+", "-")),
                    I.Chain((14, 6, 3), ("-", "+")),
                    I.Chain((9, 4, 2), ("+", "-")),
                    I.Chain((16, 8, 5), ("-", "+")),
                    I.Chain((6, 7, 4), ("+", "-")),
                    I.Chain((15, 9, 6), ("-", "+"))]),
    ]


def unit_10():
    return [
        idea("Bigger numbers need no new trick. Take the tens from the tens "
             "and the ones from the ones. When there are not enough ones, "
             "break open one ten — exactly the move from Unit 17, at a "
             "larger size."),
        Canvas(96, _dia_twodigitsub, pad_below=7),
        worked([f"62 {M} 7 — there are only 2 ones, and 7 are needed.",
                f"Take the 2 ones first: 62 {M} 2 = 60.",
                f"Five are still to go: 60 {M} 5 = 55."]),
        watch("In column form, line the ones under the ones. And when you "
              "break open a ten, write it down — the tens digit is now one "
              "smaller, and forgetting that is the commonest slip there is."),
        *try_these([I.Horizontal(70, 30, "-"), I.Horizontal(58, 6, "-"),
                    I.Column(46, 4, "-"), I.Column(53, 8, "-"),
                    I.Column(78, 25, "-"), I.Column(62, 47, "-")], cols=2),
    ]


# ── compact reminders ─────────────────────────────────────────────────────────

def _rem_takeaway(c, x, y, w):
    D.number_line(c, x, y, w * 0.58, 0, 10, jumps=[(8, -3, f"{M}3")],
                  mark=[8], label_size=6)
    D.text(c, x + w, y - 20, f"8 {M} 3 = 5", NUMB, 10.5, "right", ACCENT)
    D.text(c, x + w, y - 33, "eight: seven, six, five", SANSO, 7.2, "right",
           MUTED)


def _rem_family(c, x, y, w):
    D.fact_triangle(c, x + 30, y + 2, 15, (7, 8), "+", size=9, h=42,
                    half_w=26)
    D.text(c, x + 76, y - 12, f"7 + 8 = 15      15 {M} 7 = 8", NUMB, 9.5,
           color=ACCENT)
    D.text(c, x + 76, y - 26, f"8 + 7 = 15      15 {M} 8 = 7", NUMB, 9.5,
           color=ACCENT)
    D.text(c, x + 76, y - 39, "the whole always comes first in a subtraction",
           SANSO, 7.4, color=MUTED)


def _rem_fromten(c, x, y, w):
    D.text(c, x, y - 9, "The ten pairs, backwards", SANSB, 8.4)
    pairs = [f"10{M}1=9", f"10{M}2=8", f"10{M}3=7", f"10{M}4=6", f"10{M}5=5"]
    pairs2 = [f"10{M}6=4", f"10{M}7=3", f"10{M}8=2", f"10{M}9=1"]
    for row, ps in enumerate((pairs, pairs2)):
        xx = x
        for p in ps:
            D.text(c, xx, y - 24 - row * 12, p, NUM, 8.6, color=ACCENT)
            xx += (w - 6) / 5


def _rem_countup(c, x, y, w):
    D.text(c, x, y - 10, "Numbers close together? Count UP from the smaller.",
           SANS, 8.4)
    D.text(c, x, y - 26, f"12 {M} 9  →  9 up to 12  →  3 hops  →  3",
           NUMB, 10, color=ACCENT)
    D.text(c, x, y - 39, "Numbers far apart with a small second number? "
                         "Count back.", SANSO, 7.4, color=MUTED)


def _rem_subchooser(c, x, y, w):
    D.text(c, x, y - 9, "Pick your method", SANSB, 8.4)
    rows = [(f"{M}1 {M}2 {M}3", "count back"), ("close", "count up"),
            ("from 10", "ten pair"), ("known sum", "read it backwards")]
    xx = x
    for a, b in rows:
        D.text(c, xx, y - 24, a, NUM, 8, color=MUTED)
        D.text(c, xx, y - 35, b, SANSB, 8, color=ACCENT)
        xx += (w - 4) / 4


def _rem_teenminus(c, x, y, w):
    D.ten_frame(c, x, y - 2, 10, 9.5, fill_color=HAIR)
    D.ten_frame(c, x + 56, y - 2, 7, 9.5, fill_color=INK, cross_from=3)
    D.text(c, x + 116, y - 15, f"17 {M} 4  =  10 + 3  =  13", NUMB, 10.5,
           color=ACCENT)
    D.text(c, x + 116, y - 28, "the ten is never touched", SANSO, 7.4,
           color=MUTED)


def _rem_breakten(c, x, y, w):
    D.text(c, x, y - 10, f"15 {M} 7", SANSB, 10)
    D.seq(c, x + 40, y - 10, ["", "15 has 5 ones", "take those first"],
          SANS, 8.2, MUTED, gap=4)
    D.text(c, x, y - 26, f"15 {M} 5 {M} 2  =  10 {M} 2  =  8", NUMB, 11,
           color=ACCENT)
    D.text(c, x, y - 39, "Take the ones you have, land on ten, "
                         "then take the rest.", SANSO, 7.4, color=MUTED)


def _rem_missing(c, x, y, w):
    D.text(c, x, y - 10, "Whole first, then the parts.", SANSB, 9,
           color=ACCENT)
    D.text(c, x, y - 25, f"15 {M} ? = 7   →   parts are 7 and 8   →   ? = 8",
           NUM, 8.4)
    D.text(c, x, y - 38, "Always check by adding your answer back in.",
           SANSO, 7.4, color=MUTED)


def _rem_mixed(c, x, y, w):
    D.text(c, x, y - 10, "Work along the chain from left to right.",
           SANS, 8.4)
    D.seq(c, x, y - 26, [f"8 + 5 {M} 3", f"13 {M} 3", "10"], NUMB, 10, ACCENT,
          gap=7)
    D.text(c, x, y - 39, "Adding and subtracting the same number undo "
                         "each other.", SANSO, 7.4, color=MUTED)


def _rem_twodigitsub(c, x, y, w):
    D.text(c, x, y - 10, f"54 {M} 8  =  54 {M} 4 {M} 4  =  50 {M} 4  =  46",
           NUMB, 10, color=ACCENT)
    D.text(c, x, y - 25, f"76 {M} 23  =  (70 {M} 20) + (6 {M} 3)  =  53",
           NUMB, 10, color=ACCENT)
    D.text(c, x, y - 38, "Not enough ones? Break open one ten and "
                         "write it down.", SANSO, 7.4, color=MUTED)


# ── the ten subtraction units ────────────────────────────────────────────────

SUB_UNITS = [
    Unit(1, "Taking Away and Counting Back", "counting back",
         "Count back from the first number. Only worth it for 1, 2 or 3.",
         pool_count_back(),
         [f_lineback, f_takeaway],
         [(4, f_plain), (1.4, f_missing), (0.8, f_takeaway), (0.8, f_lineback),
          (0.6, f_tf)],
         [(1, f_plain)],
         _rem_takeaway, 40, unit_1, "3 min", "2 min", op="-"),

    Unit(2, "Fact Families", "one triangle, four facts",
         "Two parts and a whole. The whole always comes first in a "
         "subtraction.",
         pool_families_to_ten(),
         [f_family, f_bond],
         [(2.6, f_plain), (2.0, f_missing), (1.2, f_family), (0.8, f_tf),
          (0.6, f_error)],
         [(1, f_plain)],
         _rem_family, 42, unit_2, "4 min", "2 min", op="-"),

    Unit(3, "Subtracting from Ten", "the ten pairs backwards",
         "You already know these. 10 – 6 = 4 because 6 + 4 = 10.",
         pool_from_ten(),
         [f_takeaway, f_family],
         [(3.4, f_plain), (1.8, f_missing), (1.0, f_takeaway), (0.8, f_compare),
          (0.6, f_tf)],
         [(1, f_plain)],
         _rem_fromten, 42, unit_3, "3 min", "2 min", op="-"),

    Unit(4, "Counting Up to Find a Difference", "how many more",
         "Numbers close together? Count up from the smaller one.",
         pool_close_differences(),
         [f_countup, f_family],
         [(3.4, f_plain), (1.6, f_missing), (1.0, f_countup), (0.9, f_compare),
          (0.6, f_tf), (0.5, f_error)],
         [(1, f_plain)],
         _rem_countup, 42, unit_4, "4 min", "3 min", op="-"),

    Unit(5, "All Differences Within Ten", "choose your method",
         "Look at the two numbers first, then choose how to subtract.",
         pool_within_ten(),
         [f_takeaway, f_family],
         [(4, f_plain), (1.6, f_missing), (1.0, f_compare), (0.9, f_balance),
          (0.7, f_tf), (0.5, f_error)],
         [(1, f_plain)],
         _rem_subchooser, 40, unit_5, "4 min", "3 min", op="-"),

    Unit(6, "Teen Numbers Minus Ones", "the ten stays whole",
         "Enough ones to take from? Subtract inside the ones and keep the ten.",
         pool_teen_minus_ones(),
         [f_takeaway, f_family],
         [(3.6, f_plain), (1.8, f_missing), (0.9, f_compare), (0.7, f_tf),
          (0.5, f_error)],
         [(1, f_plain)],
         _rem_teenminus, 40, unit_6, "4 min", "3 min", op="-"),

    Unit(7, "Breaking Ten to Cross Back", "bridging back",
         "Take the ones you have, land on ten, then take the rest.",
         pool_bridge_back(),
         [f_breakten, f_family],
         [(2.4, f_plain), (2.0, f_breakten), (1.4, f_missing), (0.7, f_tf),
          (0.6, f_error)],
         [(1, f_plain)],
         _rem_breakten, 44, unit_7, "5 min", "3 min", op="-"),

    Unit(8, "All Facts to Twenty; the Missing Number", "whole and parts",
         "Find the whole first. Then check by adding your answer back.",
         pool_all_to_twenty(),
         [f_family, f_breakten],
         [(3.0, f_plain), (2.2, f_missing), (1.2, f_balance), (1.0, f_compare),
          (0.8, f_tf), (0.6, f_error)],
         [(1, f_plain)],
         _rem_missing, 42, unit_8, "5 min", "3 min", op="-"),

    Unit(9, "Adding and Subtracting Together", "left to right",
         "Work along the chain in order. Each step undoes or builds on "
         "the last.",
         pool_all_to_twenty(),
         [f_family, f_breakten],
         [(4, f_mixed_chain), (1.4, f_plain), (1.0, f_missing),
          (0.8, f_balance)],
         [(1, f_mixed_chain)],
         _rem_mixed, 42, unit_9, "5 min", "4 min", op="-"),

    Unit(10, "Two-Digit Subtraction", "tens and ones",
         "Tens from tens, ones from ones. Not enough ones? Break open a ten.",
         pool_two_digit_sub(),
         [f_column, f_column],
         [(3.0, f_plain), (2.2, f_column), (1.2, f_missing), (0.8, f_compare)],
         [(1, f_plain)],
         _rem_twodigitsub, 42, unit_10, "6 min", "4 min", op="-",
         late_pool=pool_two_digit_sub() + pool_two_digit_pairs_sub(),
         late_from=10),
]
