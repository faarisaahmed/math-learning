"""
Book One, first half: addition.

Ten units taking a child from counting on to two-digit addition with
regrouping. A drill book's model is that a page of examples is enough to induce
the method. It often is, for the arithmetic; it is not enough for the
*strategy*, and strategy is what separates a child who computes 8 + 5 from one
who counts to it.
"""

import draw as D
from draw import (INK, ACCENT, WARM, MUTED, HAIR, FAINT, TINT,
                  SANS, SANSB, SANSO, NUM, NUMB)
from layout import (Block, Space, Rule, Heading, Text, Bullets, Canvas,
                    Panel, Grid, Strip)
from teach import idea, watch, worked, why, try_these
import curriculum as C
from curriculum import (Unit, f_plain, f_missing, f_tf, f_compare, f_balance,
                        f_chain, f_bondladder, f_column, f_frame, f_line,
                        f_bond, f_maketen, f_family, f_error, f_word)
import items as I


# ── diagrams ──────────────────────────────────────────────────────────────────

def _dia_counton(c, x, y, w):
    D.text(c, x, y - 8, "5 + 3   —   start at 5, then hop 3 times",
           SANSB, 8.5, color=INK)
    D.number_line(c, x + 6, y - 16, w - 30, 0, 10,
                  jumps=[(5, 3, "+3")], mark=[5])
    D.seq(c, x, y - 78, ["five", "six,  seven,  eight"],
          SANSO, 8.2, MUTED)
    D.text(c, x + w, y - 78, "5 + 3 = 8", NUMB, 10, "right", ACCENT)


def _dia_commute(c, x, y, w):
    cy = y - 20
    D.text(c, x, y - 6, "2 + 7", SANSB, 9)
    D.dot_row(c, x + 34, cy, 2, 3.0, 9, INK)
    D.plus_sign(c, x + 58, cy, 3.5, 0.9, MUTED)
    D.dot_row(c, x + 100, cy, 7, 3.0, 9, ACCENT)
    D.text(c, x + w, cy - 3, "= 9", NUMB, 10, "right", INK)

    cy2 = y - 48
    D.text(c, x, cy2 + 4, "7 + 2", SANSB, 9)
    D.dot_row(c, x + 60, cy2, 7, 3.0, 9, ACCENT)
    D.plus_sign(c, x + 100, cy2, 3.5, 0.9, MUTED)
    D.dot_row(c, x + 122, cy2, 2, 3.0, 9, INK)
    D.text(c, x + w, cy2 - 3, "= 9", NUMB, 10, "right", INK)

    D.rule(c, x, y - 64, x + w, 0.4)
    D.text(c, x, y - 76, "Same dots, same total — so start from 7 "
                         "and take only 2 hops, not 7.",
           SANSO, 8.2, color=MUTED)


def _dia_bond(c, x, y, w):
    D.number_bond(c, x + 46, y - 2, 10, (6, 4))
    D.text(c, x + 46, y - 74, "whole 10, parts 6 and 4", SANSO, 7.4,
           "center", MUTED)

    fx = x + 120
    D.ten_frame(c, fx, y - 8, 10, 13.0, fill_color=INK,
                second_color=ACCENT, split_at=6)
    D.text(c, fx, y - 48, "6 + 4 = 10        4 + 6 = 10", NUM, 9.5, color=INK)
    D.text(c, fx, y - 62, "10 – 6 = 4       10 – 4 = 6",
           NUM, 9.5, color=MUTED)
    D.text(c, fx, y - 76, "one picture, four facts", SANSO, 7.6, color=MUTED)


def _dia_doubles(c, x, y, w):
    D.text(c, x, y - 8, "6 + 6 = 12", SANSB, 9.5)
    D.ten_frame(c, x, y - 16, 10, 12.0, fill_color=INK)
    D.text(c, x + 66, y - 46, "+2", NUMB, 8.5, color=WARM)

    D.text(c, x + 150, y - 8, "6 + 7 = 6 + 6 + 1 = 13", SANSB, 9.5, color=ACCENT)
    D.text(c, x + 150, y - 24, "One more than a double.", SANSO, 8.2, color=MUTED)
    for k, (lhs, rhs) in enumerate([("5 + 6", "5 + 5 + 1  =  11"),
                                    ("8 + 7", "7 + 7 + 1  =  15"),
                                    ("4 + 3", "3 + 3 + 1  =  7")]):
        D.seq(c, x + 150, y - 40 - k * 14, [lhs, rhs], NUM, 9)


def _dia_chooser(c, x, y, w):
    rows = [
        ("adding 0, 1 or 2",       "count on",        "7 + 2, then 8, 9"),
        ("both numbers the same",  "double",          "4 + 4 = 8"),
        ("numbers one apart",      "near double",     "4 + 5 = 4 + 4 + 1"),
        ("they make 10",           "known bond",      "3 + 7 = 10"),
        ("anything else",          "make ten first",  "8 + 5 is 10 + 3"),
    ]
    yy = y - 4
    D.text(c, x + 2, yy - 8, "WHEN YOU SEE", SANSB, 6.8, color=MUTED)
    D.text(c, x + 118, yy - 8, "USE", SANSB, 6.8, color=MUTED)
    D.text(c, x + 200, yy - 8, "LIKE", SANSB, 6.8, color=MUTED)
    yy -= 13
    D.rule(c, x, yy + 2, x + w, 0.5)
    for a, b, ex in rows:
        yy -= 15
        D.text(c, x + 2, yy, a, SANS, 8.4)
        D.text(c, x + 118, yy, b, SANSB, 8.4, color=ACCENT)
        D.text(c, x + 200, yy, ex, NUM, 8.4, color=MUTED)


def _dia_teens(c, x, y, w):
    D.ten_frame(c, x, y - 6, 10, 13.0, fill_color=INK)
    D.plus_sign(c, x + 78, y - 20, 4.5, 1.0, MUTED)
    D.ten_frame(c, x + 92, y - 6, 6, 13.0, fill_color=ACCENT)
    D.text(c, x + 32, y - 46, "10", NUMB, 11, "center", INK)
    D.text(c, x + 124, y - 46, "6", NUMB, 11, "center", ACCENT)
    D.text(c, x + w, y - 24, "16", NUMB, 20, "right", INK)
    D.text(c, x + w, y - 40, "1 ten, 6 ones", SANSO, 7.6, "right", MUTED)
    D.rule(c, x, y - 56, x + w, 0.4)
    D.text(c, x, y - 68, "10 + 3 = 13      10 + 7 = 17      10 + 9 = 19",
           NUM, 9.5)


def _dia_maketen(c, x, y, w):
    D.text(c, x, y - 8, "8 + 5", SANSB, 10)
    D.ten_frame(c, x, y - 16, 8, 13.0, fill_color=INK)
    D.ten_frame(c, x + 92, y - 16, 5, 13.0, fill_color=ACCENT)
    # the two counters that move
    c.setStrokeColor(WARM)
    c.setDash([1.5, 1.5]); c.setLineWidth(0.8)
    c.rect(x + 92, y - 42, 26, 13, stroke=1, fill=0)
    c.setDash([])
    D.arrow(c, x + 90, y - 34, x + 66, y - 34, 3.2, 0.9, WARM)
    D.text(c, x + 60, y - 52, "move 2 across to fill the ten",
           SANSO, 7.6, "center", WARM)

    yy = y - 66
    D.text(c, x, yy, "8 needs 2 more to make 10.", SANS, 8.6)
    D.text(c, x, yy - 12, "So split the 5 into 2 and 3.", SANS, 8.6)
    D.text(c, x, yy - 26, "8 + 5  =  8 + 2 + 3  =  10 + 3  =  13",
           NUMB, 10.5, color=ACCENT)
    D.number_bond(c, x + 250, y - 60, 5, (2, 3), r=9, drop=24, spread=22, size=9)


def _dia_balance(c, x, y, w):
    D.text(c, x, y - 8, "The = sign means “the same as”, not "
                        "“write the answer here”.", SANS, 8.8)
    D.bar_model(c, x, y - 22, w * 0.42, 7, 8, 18,
                labels=("7", "8"), total_label="15")
    D.text(c, x + w * 0.46, y - 36, "=", NUMB, 13, "center", MUTED)
    D.bar_model(c, x + w * 0.52, y - 22, w * 0.42, 9, 6, 18,
                labels=("9", "?"), total_label="15")
    D.text(c, x, y - 78, "7 + 8 = 9 + ?   —   both sides are 15, "
                         "so ? is 6.", SANS, 8.6, color=ACCENT)


def _dia_three(c, x, y, w):
    D.text(c, x, y - 8, "7 + 4 + 3", SANSB, 11)
    D.text(c, x + 74, y - 8, "—  hunt for the pair that makes 10",
           SANSO, 8.4, color=MUTED)
    yy = y - 30
    D.text(c, x, yy, "7", NUMB, 13, color=ACCENT)
    D.text(c, x + 22, yy, "+", NUM, 11, color=MUTED)
    D.text(c, x + 38, yy, "4", NUMB, 13, color=MUTED)
    D.text(c, x + 58, yy, "+", NUM, 11, color=MUTED)
    D.text(c, x + 74, yy, "3", NUMB, 13, color=ACCENT)
    c.setStrokeColor(ACCENT); c.setLineWidth(0.9)
    p = c.beginPath()
    p.moveTo(x + 4, yy - 6); p.curveTo(x + 20, yy - 20, x + 62, yy - 20,
                                       x + 78, yy - 6)
    c.drawPath(p, stroke=1, fill=0)
    D.text(c, x + 41, yy - 26, "10", NUMB, 9, "center", ACCENT)
    D.seq(c, x + 110, yy, ["", "10 + 4  =  14"], NUMB, 11, INK, gap=4)
    D.rule(c, x, y - 74, x + w, 0.4)
    D.text(c, x, y - 86, "You may add three numbers in any order. "
                         "Pick the order that is easiest.",
           SANSO, 8.2, color=MUTED)


def _dia_twodigit(c, x, y, w):
    D.text(c, x, y - 8, "34 + 5", SANSB, 10)
    D.text(c, x, y - 24, "tens stay,   ones grow", SANSO, 8, color=MUTED)
    D.text(c, x, y - 40, "30 + 4 + 5  =  30 + 9  =  39", NUMB, 10.5, color=ACCENT)

    D.text(c, x + 176, y - 8, "28 + 7", SANSB, 10)
    D.text(c, x + 176, y - 24, "ones pass ten — make ten first",
           SANSO, 8, color=MUTED)
    D.text(c, x + 176, y - 40, "28 + 2 + 5  =  30 + 5  =  35",
           NUMB, 10.5, color=ACCENT)

    D.rule(c, x, y - 54, x + w, 0.4)
    D.column_sum(c, x + 62, y - 70, 34, 5, 12, answer=39)
    D.column_sum(c, x + 238, y - 70, 28, 7, 12, answer=35, carry_hint=True)
    D.text(c, x + 76, y - 84, "line the ones up under the ones",
           SANSO, 7.6, color=MUTED)
    D.text(c, x + 252, y - 84, "the extra ten is carried", SANSO, 7.6, color=WARM)


# ── the ten teaching pages ────────────────────────────────────────────────────

def unit_1():
    return [
        idea("Adding is counting forward. To work out 5 + 3, you do not start "
             "at one and count everything again — you start at 5 and count "
             "on three more."),
        Canvas(88, _dia_counton, pad_below=7),
        worked(["Say the first number out loud: five.",
                "Count on three: six, seven, eight.",
                "The last number you say is the answer: 8."]),
        watch("The number you start on does not count as a hop. Starting at 5, "
              "your first hop lands on 6 — not on 5. Counting the start is "
              "the reason answers come out one too small."),
        *try_these([I.LineHop(4, 1), I.Frame(5, 2),
                    I.Horizontal(8, 1), I.Horizontal(3, 2),
                    I.Horizontal(9, 1), I.Horizontal(7, 2)]),
    ]


def unit_2():
    return [
        idea("Two numbers can be added in either order and the total does not "
             "change. That is not just a curiosity — it halves your work, "
             "because you can always count on from the bigger number."),
        Canvas(88, _dia_commute, pad_below=7),
        worked(["3 + 8 looks like eight hops from 3.",
                "Swap it: 8 + 3 — now it is three hops from 8.",
                "Nine, ten, eleven. The answer is 11 either way."]),
        watch("Adding 0 changes nothing at all: 0 + 8 = 8 and 8 + 0 = 8. "
              "A zero is not a signal that the answer is zero."),
        *try_these([I.Compare((3, 8), (8, 3)), I.Compare((5, 2), (2, 5)),
                    I.Horizontal(2, 9), I.Horizontal(1, 7),
                    I.Horizontal(6, 3), I.Horizontal(3, 6),
                    I.Horizontal(4, 0), I.Horizontal(0, 9)]),
    ]


def unit_3():
    return [
        idea("Every number is made of smaller parts. 10 is 6 and 4; it is also "
             "7 and 3, and 5 and 5. Knowing the pairs that make 10 by heart is "
             "the single most useful thing in this book — everything after "
             "Unit 6 leans on it."),
        Canvas(88, _dia_bond, pad_below=7),
        worked(["Ask: 6 and how many more make 10?",
                "Fill the ten-frame — four empty squares are left.",
                "6 + 4 = 10, and therefore 4 + 6 = 10 too."]),
        watch("Learn each bond in both directions. If you know 3 + 7 = 10 but "
              "stall on 7 + 3, you only half know it."),
        *try_these([I.Bond(10, (6, 4)), I.Bond(10, (3, 7)),
                    I.BondLadder(10, 8), I.BondLadder(10, 5),
                    I.BondLadder(10, 2), I.BondLadder(10, 9),
                    I.BondLadder(10, 1), I.BondLadder(10, 6)]),
    ]


def unit_4():
    return [
        idea("Doubles stick in the memory far faster than other facts, so they "
             "make good landmarks. Once you know 6 + 6 = 12, you get 6 + 7 free: "
             "it is one more."),
        Canvas(84, _dia_doubles, pad_below=7),
        worked(["7 + 8 — the numbers are one apart, so it is a near double.",
                "Take the smaller one and double it: 7 + 7 = 14.",
                "Add the one extra: 15."]),
        watch("Add the extra one once, not twice. 7 + 8 is 14 + 1 = 15, "
              "not 14 + 2."),
        *try_these([I.Horizontal(4, 4), I.Horizontal(4, 5),
                    I.Horizontal(7, 7), I.Horizontal(7, 8),
                    I.Horizontal(9, 9), I.Horizontal(8, 9),
                    I.Horizontal(6, 6), I.Horizontal(5, 6)]),
    ]


def unit_5():
    return [
        idea("You now know four ways to add. A fluent adder does not use one "
             "method for everything — they glance at the numbers and pick "
             "the method that suits them."),
        Canvas(94, _dia_chooser, pad_below=7),
        worked(["4 + 5: the numbers are one apart, so use the near "
                "double. 4 + 4 = 8, and one more is 9.",
                "3 + 7: that pair makes ten, so the answer is 10.",
                "6 + 2: the second number is small, so count on: 7, 8."]),
        watch("Counting on works for everything, but it gets slow and error-prone "
              "past two or three hops. If you are counting five hops on your "
              "fingers, there is a faster route."),
        *try_these([I.Horizontal(3, 7), I.Horizontal(6, 2),
                    I.Horizontal(4, 4), I.Horizontal(5, 4),
                    I.Horizontal(8, 2), I.Horizontal(1, 6),
                    I.Horizontal(3, 3), I.Horizontal(2, 7)]),
    ]


def unit_6():
    return [
        idea("A teen number is simply a ten with some ones beside it. 16 is one "
             "ten and six ones. Say it that way and 10 + 6 stops being a sum you "
             "work out and becomes a name you read."),
        Canvas(84, _dia_teens, pad_below=7),
        worked(["10 + 7 — one full ten-frame and seven more.",
                "One ten and seven ones.",
                "That number is called seventeen: 17."]),
        watch("10 + 6 is 16, not 106. The 1 and the 6 are not written "
              "side by side as separate numbers — the 1 means one ten."),
        *try_these([I.Horizontal(10, 4), I.Horizontal(10, 8),
                    I.Horizontal(6, 10), I.Horizontal(10, 10),
                    I.Bond(15, (10, 5)), I.Bond(18, (10, 8)),
                    I.MissingAddend(10, 13), I.MissingAddend(10, 19)]),
    ]


def unit_7():
    return [
        idea("When a sum crosses ten, fill the ten first. Take just enough from "
             "the second number to complete the ten, then add whatever is left "
             "over. Ten plus something is easy — you learned it last unit."),
        Canvas(104, _dia_maketen, pad_below=7),
        worked(["9 + 6 — 9 needs 1 more to reach 10.",
                "Split the 6 into 1 and 5.",
                "9 + 1 = 10, then 10 + 5 = 15."]),
        watch("Split the second number, and split off exactly the amount the "
              "first number is short by. For 8 + 5 you take 2 (not 1, not 5), "
              "because 8 is two short of ten."),
        *try_these([I.MakeTen(9, 4), I.MakeTen(8, 5),
                    I.MakeTen(7, 6), I.MakeTen(9, 7)], cols=2),
    ]


def unit_8():
    return [
        idea("An equals sign says the two sides weigh the same. That is why "
             "7 + ? = 15 makes sense: you are asked what keeps the balance, "
             "which is the same as asking how far 7 is from 15."),
        Canvas(92, _dia_balance, pad_below=7),
        worked(["7 + ? = 15. How far is 7 from 15?",
                "7 needs 3 to reach 10, and 10 needs 5 more to reach 15.",
                "3 + 5 = 8, so the box is 8. Check: 7 + 8 = 15."]),
        watch("A missing-addend question is not asking you to add the two "
              "numbers you can see. 7 + ? = 15 has the answer 8, not 22."),
        *try_these([I.MissingAddend(7, 15), I.MissingAddend(6, 13),
                    I.MissingAddend(9, 16), I.MissingAddend(8, 14),
                    I.Balance(7, 8, 9), I.Balance(6, 5, 4),
                    I.TrueFalse(8, 7, 15), I.TrueFalse(9, 6, 14)]),
    ]


def unit_9():
    return [
        idea("Three numbers can be added in any order you like. Scan them first "
             "and see whether two of them make ten — if they do, add that "
             "pair first and the rest is easy."),
        Canvas(100, _dia_three, pad_below=7),
        worked(["6 + 9 + 4 — scan for a ten. 6 and 4 make 10.",
                "Add those first: 10.",
                "Then add the 9 that is left: 19."]),
        watch("Reordering is allowed, but every number must be used exactly "
              "once. It is easy to add the pair that makes ten and then forget "
              "the third number entirely."),
        *try_these([I.Chain((6, 9, 4)), I.Chain((3, 5, 7)),
                    I.Chain((8, 2, 6)), I.Chain((4, 4, 6)),
                    I.Chain((5, 1, 5)), I.Chain((7, 3, 8)),
                    I.Chain((2, 9, 8)), I.Chain((6, 6, 4))]),
    ]


def unit_10():
    return [
        idea("Bigger numbers need no new tricks. Add the tens to the tens and "
             "the ones to the ones. When the ones pass ten, use exactly the "
             "make-ten move from Unit 7 — it works at any size."),
        Canvas(96, _dia_twodigit, pad_below=7),
        worked(["46 + 8 — the ones are 6 and 8, which passes ten.",
                "46 needs 4 to reach 50. Split the 8 into 4 and 4.",
                "46 + 4 = 50, then 50 + 4 = 54."]),
        watch("In column form, line the ones digit up under the ones digit. "
              "Writing 34 + 5 with the 5 under the 3 turns it into 34 + 50."),
        *try_these([I.Horizontal(30, 40), I.Horizontal(52, 6),
                    I.Column(43, 5), I.Column(27, 8),
                    I.Column(36, 22), I.Column(48, 27)], cols=2),
    ]




# ── fact pools ────────────────────────────────────────────────────────────────

def _dedupe(pairs):
    seen, out = set(), []
    for p in pairs:
        if p not in seen:
            seen.add(p)
            out.append(p)
    return out


def pool_counting_on():
    out = []
    for a in range(0, 10):
        for b in (1, 2):
            out += [(a, b), (b, a)]
    return _dedupe(out)


def pool_three_and_zero():
    out = []
    for a in range(0, 10):
        out += [(a, 3), (3, a), (a, 0), (0, a)]
    return _dedupe([p for p in out if p[0] + p[1] <= 12])


def pool_bonds_to_ten():
    return _dedupe([(a, 10 - a) for a in range(0, 11)])


def pool_bonds_small():
    out = []
    for whole in range(5, 11):
        for a in range(0, whole + 1):
            out.append((a, whole - a))
    return _dedupe(out)


def pool_doubles():
    return [(a, a) for a in range(1, 11)]


def pool_near_doubles():
    out = []
    for a in range(1, 10):
        out += [(a, a + 1), (a + 1, a)]
    return _dedupe(out)


def pool_sums_to_ten():
    return _dedupe([(a, b) for a in range(0, 11) for b in range(0, 11)
                    if a + b <= 10])


def pool_teens():
    out = []
    for n in range(0, 11):
        out += [(10, n), (n, 10)]
    return _dedupe(out)


def pool_bridging():
    """Facts that cross ten — the hard core of the addition table."""
    return _dedupe([(a, b) for a in range(2, 10) for b in range(2, 10)
                    if 10 < a + b <= 18])


def pool_all_to_twenty():
    return _dedupe([(a, b) for a in range(0, 11) for b in range(0, 11)
                    if a + b <= 20])


def pool_two_digit():
    out = []
    for t in range(1, 9):
        for o in range(0, 10):
            a = t * 10 + o
            for b in range(2, 10):
                if a + b <= 99:
                    out.append((a, b))
    return out


def pool_two_digit_pairs():
    return [(t1 * 10 + o1, t2 * 10 + o2)
            for t1 in range(1, 6) for o1 in range(0, 10)
            for t2 in range(1, 4) for o2 in range(0, 10)
            if t1 * 10 + o1 + t2 * 10 + o2 <= 99]


# ── the compact reminder printed on practice pages ───────────────────────────

def _rem_counting(c, x, y, w):
    D.number_line(c, x, y, w * 0.62, 0, 10, jumps=[(6, 2, "+2")], mark=[6],
                  label_size=6)
    D.text(c, x + w, y - 20, "6 + 2 = 8", NUMB, 10.5, "right", ACCENT)
    D.text(c, x + w, y - 33, "start at 6:  seven, eight", SANSO, 7.2,
           "right", MUTED)


def _rem_commute(c, x, y, w):
    D.text(c, x, y - 10, "2 + 7  =  7 + 2  =  9", NUMB, 11, color=ACCENT)
    D.text(c, x, y - 24, "Start from the bigger number — fewer hops.",
           SANS, 8.2, color=INK)
    D.text(c, x, y - 36, "0 + 8 = 8        8 + 0 = 8", NUM, 8.6, color=MUTED)


def _rem_bonds(c, x, y, w):
    pairs = ["0+10", "1+9", "2+8", "3+7", "4+6", "5+5"]
    D.text(c, x, y - 9, "The pairs that make 10", SANSB, 8.4, color=INK)
    xx = x
    for p in pairs:
        D.text(c, xx, y - 25, p, NUMB, 10, color=ACCENT)
        xx += (w - 6) / 6
    D.text(c, x, y - 38, "and each one backwards too", SANSO, 7.4, color=MUTED)


def _rem_doubles(c, x, y, w):
    D.text(c, x, y - 9, "Doubles", SANSB, 8.4)
    D.text(c, x + 44, y - 9, "3+3=6   4+4=8   5+5=10   6+6=12   7+7=14   8+8=16",
           NUM, 8.2, color=MUTED)
    D.text(c, x, y - 25, "Near double", SANSB, 8.4)
    D.text(c, x + 60, y - 25, "6 + 7  =  6 + 6 + 1  =  13", NUMB, 10,
           color=ACCENT)


def _rem_chooser(c, x, y, w):
    D.text(c, x, y - 9, "Pick your method", SANSB, 8.4)
    rows = [("+0 +1 +2", "count on"), ("same", "double"),
            ("one apart", "near double"), ("makes 10", "you know it")]
    xx = x
    for a, b in rows:
        D.text(c, xx, y - 24, a, NUM, 8, color=MUTED)
        D.text(c, xx, y - 35, b, SANSB, 8, color=ACCENT)
        xx += (w - 4) / 4


def _rem_teens(c, x, y, w):
    D.ten_frame(c, x, y - 2, 10, 9.5, fill_color=INK)
    D.ten_frame(c, x + 56, y - 2, 4, 9.5, fill_color=ACCENT)
    D.text(c, x + 110, y - 15, "10 + 4  =  14", NUMB, 11, color=ACCENT)
    D.text(c, x + 110, y - 28, "one ten and four ones", SANSO, 7.4, color=MUTED)


def _rem_maketen(c, x, y, w):
    D.text(c, x, y - 10, "8 + 5", SANSB, 10)
    D.seq(c, x + 30, y - 10, ["", "8 needs 2", "5 splits into 2 and 3"],
          SANS, 8.2, MUTED, gap=4)
    D.text(c, x, y - 26, "8 + 2 + 3  =  10 + 3  =  13", NUMB, 11, color=ACCENT)
    D.text(c, x, y - 39, "9 needs 1.   8 needs 2.   7 needs 3.   6 needs 4.",
           NUM, 8, color=MUTED)


def _rem_balance(c, x, y, w):
    D.text(c, x, y - 10, "=  means  “the same as”", SANSB, 9, color=ACCENT)
    D.seq(c, x, y - 25, ["7 + ? = 15", "7 needs 3 to make 10, then 5 more",
                         "? = 8"], NUM, 8.4, INK, gap=6)
    D.text(c, x, y - 38, "Always check by adding your answer back in.",
           SANSO, 7.4, color=MUTED)


def _rem_three(c, x, y, w):
    D.text(c, x, y - 10, "Scan for a pair that makes 10, add it first.",
           SANS, 8.4)
    D.seq(c, x, y - 26, ["7 + 4 + 3", "(7 + 3) + 4   =   10 + 4   =   14"],
          NUMB, 10, ACCENT, gap=7)
    D.text(c, x, y - 39, "Use every number exactly once.", SANSO, 7.4,
           color=MUTED)


def _rem_twodigit(c, x, y, w):
    D.text(c, x, y - 10, "34 + 5  =  30 + (4 + 5)  =  39", NUMB, 10,
           color=ACCENT)
    D.text(c, x, y - 25, "28 + 7  =  (28 + 2) + 5  =  30 + 5  =  35",
           NUMB, 10, color=ACCENT)
    D.text(c, x, y - 38, "Tens with tens, ones with ones. "
                         "Ones past ten? Make the ten first.",
           SANSO, 7.4, color=MUTED)


# ── the ten addition units ───────────────────────────────────────────────────

ADD_UNITS = [
    Unit(1, "Counting On: +1 and +2", "counting on",
         "Start at the bigger number and count on. The start does not count "
         "as a hop.",
         pool_counting_on(),
         [f_line, f_frame],
         [(4, f_plain), (1.4, f_missing), (0.8, f_frame), (0.8, f_line),
          (0.6, f_tf)],
         [(1, f_plain)],
         _rem_counting, 40, unit_1, "3 min", "2 min"),

    Unit(2, "Counting On: +3, +0, and Order", "order doesn't matter",
         "a + b = b + a. Count on from the bigger number. Adding 0 changes "
         "nothing.",
         pool_three_and_zero(),
         [f_line, f_frame],
         [(4, f_plain), (1.2, f_missing), (1.2, f_compare), (0.7, f_frame),
          (0.6, f_tf)],
         [(1, f_plain)],
         _rem_commute, 40, unit_2, "3 min", "2 min"),

    Unit(3, "Number Bonds and Pairs That Make Ten", "part, part, whole",
         "Every number splits into parts. Know the ten pairs both ways.",
         pool_bonds_small(),
         [f_bond, f_frame],
         [(2.6, f_bondladder), (2.0, f_plain), (1.6, f_missing),
          (1.0, f_bond), (0.7, f_frame)],
         [(1.4, f_bondladder), (1, f_plain)],
         _rem_bonds, 42, unit_3, "4 min", "2 min"),

    Unit(4, "Doubles and Near Doubles", "landmark facts",
         "Doubles are landmarks. One apart? Double the smaller, add one.",
         pool_doubles() + pool_near_doubles(),
         [f_frame, f_bond],
         [(4, f_plain), (1.2, f_missing), (1.0, f_compare), (0.8, f_tf),
          (0.6, f_bond)],
         [(1, f_plain)],
         _rem_doubles, 42, unit_4, "4 min", "2 min"),

    Unit(5, "All Sums to Ten", "choose your method",
         "Look at the numbers first, then choose the quickest method.",
         pool_sums_to_ten(),
         [f_frame, f_bond],
         [(4, f_plain), (1.4, f_missing), (1.0, f_compare), (0.9, f_balance),
          (0.7, f_tf), (0.5, f_error)],
         [(1, f_plain)],
         _rem_chooser, 40, unit_5, "4 min", "3 min"),

    Unit(6, "Ten and the Teens", "10 + n",
         "A teen number is one ten and some ones. 10 + 6 = 16.",
         pool_teens(),
         [f_frame, f_bond],
         [(3.6, f_plain), (1.6, f_missing), (1.2, f_bond), (0.8, f_compare),
          (0.6, f_tf)],
         [(1, f_plain)],
         _rem_teens, 40, unit_6, "4 min", "2 min"),

    Unit(7, "Making Ten to Cross Ten", "bridging",
         "Fill the ten first, then add what is left over.",
         pool_bridging(),
         [f_maketen, f_bond],
         [(2.4, f_plain), (2.0, f_maketen), (1.4, f_missing), (0.8, f_bond),
          (0.6, f_tf), (0.6, f_error)],
         [(1, f_plain)],
         _rem_maketen, 44, unit_7, "5 min", "3 min"),

    Unit(8, "All Facts to Twenty", "fluency and balance",
         "The equals sign means both sides match. Check by adding back.",
         pool_all_to_twenty(),
         [f_bond, f_maketen],
         [(3.4, f_plain), (2.0, f_missing), (1.2, f_balance), (1.0, f_compare),
          (0.8, f_tf), (0.5, f_error)],
         [(1, f_plain)],
         _rem_balance, 42, unit_8, "5 min", "3 min"),

    Unit(9, "Three Numbers at Once", "look for the ten",
         "Add in any order. Find the pair that makes ten and start there.",
         pool_all_to_twenty(),
         [f_bond, f_maketen],
         [(4, f_chain), (1.4, f_plain), (1.0, f_missing), (0.8, f_balance)],
         [(1, f_chain)],
         _rem_three, 42, unit_9, "5 min", "4 min",
         word_factory=C.f_word3),

    Unit(10, "Two-Digit Addition", "tens and ones",
         "Tens with tens, ones with ones. Past ten? Make the ten first.",
         pool_two_digit(),
         [f_column, f_column],
         [(3.0, f_plain), (2.2, f_column), (1.2, f_missing), (0.8, f_compare)],
         [(1, f_plain)],
         _rem_twodigit, 42, unit_10, "6 min", "4 min",
         late_pool=pool_two_digit() + pool_two_digit_pairs(), late_from=10),
]
