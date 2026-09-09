"""
Book Two, first half: multiplication.

The organising idea is that multiplication is *equal groups*, and that an array
is the picture which makes its properties visible rather than assertable. From
the array, commutativity is a quarter turn; from the array cut in two, the
distributive law is obvious; and from the distributive law, two-digit
multiplication is the same idea at a larger size rather than a new ritual.

A child drilled only on the table can recite 7 x 6 = 42 and still be helpless
at 17 x 6. That gap is what these ten units are built to close.
"""

import draw as D
from draw import (INK, ACCENT, WARM, MUTED, HAIR, FAINT, TINT, OP_SYM,
                  SANS, SANSB, SANSO, NUM, NUMB)
from layout import (Block, Space, Rule, Heading, Text, Bullets, Canvas,
                    Panel, Grid, Strip)
from teach import idea, watch, worked, why, try_these
import curriculum as C
from curriculum import (Unit, f_plain, f_missing, f_tf, f_compare, f_balance,
                        f_column, f_family, f_error, f_array, f_groups,
                        f_areasplit, f_skip, f_factors)
import items as I

X = OP_SYM["*"]
M = OP_SYM["-"]


# ── fact pools ────────────────────────────────────────────────────────────────

def _dedupe(pairs):
    seen, out = set(), []
    for p in pairs:
        if p not in seen:
            seen.add(p)
            out.append(p)
    return out


def pool_equal_groups():
    return _dedupe([(n, per) for n in range(2, 7) for per in range(2, 7)])


def pool_arrays():
    return _dedupe([(r, c) for r in range(1, 7) for c in range(2, 10)])


def pool_2_5_10():
    out = []
    for b in (2, 5, 10):
        for a in range(1, 11):
            out += [(a, b), (b, a)]
    return _dedupe(out)


def pool_one_zero():
    out = []
    for a in range(0, 11):
        out += [(a, 1), (1, a), (a, 0), (0, a)]
    return _dedupe(out)


def pool_3_4():
    out = []
    for b in (3, 4):
        for a in range(1, 11):
            out += [(a, b), (b, a)]
    return _dedupe(out)


def pool_6_to_9():
    out = []
    for b in (6, 7, 8, 9):
        for a in range(2, 11):
            out += [(a, b), (b, a)]
    return _dedupe(out)


def pool_all_tables():
    return _dedupe([(a, b) for a in range(0, 11) for b in range(0, 11)])


def pool_distribute():
    return _dedupe([(a, b) for a in range(6, 10) for b in range(3, 10)])


def pool_two_digit_mul():
    return _dedupe([(a, b) for a in range(11, 30) for b in range(2, 10)
                    if a * b <= 200])


def pool_times_tens():
    out = [(a, 10) for a in range(2, 21)] + [(10, a) for a in range(2, 21)]
    out += [(a, b) for a in (20, 30, 40, 50) for b in range(2, 6)
            if a * b <= 200]
    return _dedupe(out)


def pool_factors():
    return _dedupe([(a, b) for a in range(2, 11) for b in range(2, 11)
                    if a * b <= 60])


# ── diagrams ──────────────────────────────────────────────────────────────────

def _dia_groups(c, x, y, w):
    D.text(c, x, y - 8, f"4 groups of 3", SANSB, 9)
    D.groups(c, x, y - 14, 4, 3, ring=15.0, gap=7, per_row=4)
    D.text(c, x + 190, y - 26, "3 + 3 + 3 + 3  =  12", NUM, 10, color=MUTED)
    D.text(c, x + 190, y - 42, f"4 {X} 3  =  12", NUMB, 13, color=ACCENT)
    D.rule(c, x, y - 60, x + w, 0.4)
    D.text(c, x, y - 72, "Four threes. Writing it as a multiplication is "
                         "shorter, and says the same thing.",
           SANSO, 8.2, color=MUTED)


def _dia_array(c, x, y, w):
    D.text(c, x, y - 8, f"3 {X} 4", SANSB, 9.5)
    D.array(c, x, y - 14, 4, 3, cell=11.0)
    D.text(c, x, y - 62, "3 rows of 4", SANSO, 7.6, color=MUTED)

    D.text(c, x + 120, y - 8, f"4 {X} 3", SANSB, 9.5)
    D.array(c, x + 120, y - 14, 3, 4, cell=11.0)
    D.text(c, x + 120, y - 62, "4 rows of 3", SANSO, 7.6, color=MUTED)

    D.text(c, x + 232, y - 34, "both are 12", NUMB, 12, color=ACCENT)
    D.text(c, x, y - 78, "The same dots, turned a quarter turn. That is why "
                         "the table only has half as much in it as it looks.",
           SANSO, 8.2, color=MUTED)


def _dia_2510(c, x, y, w):
    rows = [(2, "double it"), (10, "a ten for each one"),
            (5, "half of the ten")]
    yy = y - 2
    for step, note in rows:
        D.text(c, x, yy - 10, f"{step}s", SANSB, 9, color=ACCENT)
        D.skip_track(c, x + 22, yy, [step * (i + 1) for i in range(10)],
                     box_w=20, gap=2, size=7.6)
        D.text(c, x + 258, yy - 10, note, SANSO, 7.6, color=MUTED)
        yy -= 24
    D.rule(c, x, yy - 2, x + w, 0.4)
    D.text(c, x, yy - 14, f"6 {X} 10 = 60, so 6 {X} 5 = 30 — exactly half.",
           NUMB, 9.5, color=ACCENT)


def _dia_onezero(c, x, y, w):
    D.text(c, x, y - 8, f"1 {X} 6", SANSB, 9.5)
    D.groups(c, x, y - 14, 1, 6, ring=15.0, gap=6, per_row=4)
    D.text(c, x + 44, y - 26, "one group of six  =  6", NUM, 9.5, color=INK)

    D.text(c, x, y - 52, f"0 {X} 6", SANSB, 9.5)
    for k in range(3):
        c.setStrokeColor(HAIR)
        c.setDash([1.5, 1.5])
        c.setLineWidth(0.7)
        c.circle(x + 40 + k * 36, y - 64, 12, stroke=1, fill=0)
        c.setDash([])
    D.text(c, x + 150, y - 68, "no groups at all  =  0", NUM, 9.5, color=INK)
    D.text(c, x, y - 88, f"6 {X} 1 = 6        6 {X} 0 = 0        "
                         f"0 {X} 6 = 0", NUMB, 10, color=ACCENT)


def _dia_34(c, x, y, w):
    D.text(c, x, y - 8, f"7 {X} 4   —   double, then double again", SANSB, 9)
    D.array(c, x, y - 16, 4, 7, cell=9.5, highlight_cols=2,
            second_color=ACCENT)
    D.vrule(c, x + 19, y - 16 - 66.5, y - 16, 1.0, WARM)
    D.text(c, x + 78, y - 30, f"7 {X} 2  =  14", NUMB, 10, color=ACCENT)
    D.text(c, x + 78, y - 46, f"14 {X} 2  =  28", NUMB, 10, color=INK)
    D.text(c, x + 78, y - 62, f"so 7 {X} 4  =  28", NUMB, 10, color=INK)
    D.text(c, x + 190, y - 30, f"3 {X} n  =  double n, then add n", SANS, 8.4,
           color=MUTED)
    D.text(c, x + 190, y - 44, f"7 {X} 3  =  14 + 7  =  21", NUM, 9,
           color=MUTED)


def _dia_hard(c, x, y, w):
    D.text(c, x, y - 8, f"9 {X} 7   —   a ten of them, less one of them",
           SANSB, 9)
    D.array(c, x, y - 16, 10, 7, cell=9.0, highlight_cols=9,
            second_color=INK, color=HAIR)
    D.text(c, x + 86, y - 74, "the last column is the one to give back",
           SANSO, 7.2, color=WARM)
    D.text(c, x + 106, y - 26, f"10 {X} 7  =  70", NUMB, 10, color=MUTED)
    D.text(c, x + 106, y - 40, f"70 {M} 7  =  63", NUMB, 10, color=ACCENT)
    D.text(c, x + 200, y - 26, "Squares are landmarks:", SANS, 8.2,
           color=MUTED)
    D.text(c, x + 200, y - 40, f"6{X}6=36   7{X}7=49   8{X}8=64", NUM, 8.4)
    D.text(c, x + 200, y - 54, f"so 6{X}7 = 36 + 6 = 42", NUM, 8.4,
           color=ACCENT)


def _dia_table(c, x, y, w):
    D.times_grid(c, x, y - 2, 10, cell=14.0, size=5.4)
    tx = x + 172
    D.text(c, tx, y - 14, "One hundred squares.", SANSB, 8.8, color=INK)
    D.text(c, tx, y - 27, "About fifty-five facts.", SANSB, 8.8, color=ACCENT)
    lines = [
        "The pale half repeats the other half:",
        f"7 {X} 4 and 4 {X} 7 are one fact, not two.",
        "",
        "The shaded diagonal is the squares.",
        "They are the easiest to remember and",
        "the handiest landmarks: any fact next",
        "to a square is that square plus or",
        "minus one row.",
        "",
        f"The 1s, 2s, 5s and 10s rows are",
        "already done. What is really left is",
        f"the 3s, 4s, 6s, 7s, 8s and 9s —",
        "and half of those repeat too.",
    ]
    yy = y - 44
    for ln in lines:
        D.text(c, tx, yy, ln, SANS, 7.8, color=MUTED if ln else INK)
        yy -= 10


def _dia_distribute(c, x, y, w):
    D.text(c, x, y - 8, f"7 {X} 6   —   cut it at five", SANSB, 9)
    D.area_model(c, x + 14, y - 22, 150, 38, 7, 6, 5)
    D.text(c, x + 186, y - 26, f"5 {X} 6  =  30", NUMB, 10, color=ACCENT)
    D.text(c, x + 186, y - 40, f"2 {X} 6  =  12", NUMB, 10, color=INK)
    D.rule(c, x + 186, y - 46, x + 254, 0.6, INK)
    D.text(c, x + 186, y - 58, f"7 {X} 6  =  42", NUMB, 10, color=INK)
    D.text(c, x, y - 74, "A rectangle cut in two: the two pieces must add "
                         "back to the whole.", SANSO, 8.2, color=MUTED)


def _dia_twodigitmul(c, x, y, w):
    D.text(c, x, y - 8, f"13 {X} 4   —   the same cut, at ten", SANSB, 9)
    D.area_model(c, x + 14, y - 22, 160, 36, 13, 4, 10)
    D.text(c, x + 194, y - 26, f"10 {X} 4  =  40", NUMB, 10, color=ACCENT)
    D.text(c, x + 194, y - 40, f"3 {X} 4  =  12", NUMB, 10, color=INK)
    D.rule(c, x + 194, y - 46, x + 262, 0.6, INK)
    D.text(c, x + 194, y - 58, f"13 {X} 4  =  52", NUMB, 10, color=INK)
    D.rule(c, x, y - 70, x + w, 0.4)
    D.column_op(c, x + 62, y - 84, 13, 4, "*", 12, answer=52, carry_hint=True)
    D.text(c, x + 84, y - 98, "the column method is the same two pieces, "
                              "added in one go", SANSO, 7.4, color=MUTED)


def _dia_factors(c, x, y, w):
    D.text(c, x, y - 8, "Twelve, made into rectangles", SANSB, 9)
    specs = [(1, 12), (2, 6), (3, 4)]
    xx = x
    for r, cc in specs:
        D.array(c, xx, y - 16, cc, r, cell=7.5)
        D.text(c, xx, y - 22 - r * 7.5 - 8, f"{r} {X} {cc}", NUM, 8,
               color=ACCENT)
        xx += cc * 7.5 + 22
    D.rule(c, x, y - 62, x + w, 0.4)
    D.text(c, x, y - 74, "The factors of 12 are 1, 2, 3, 4, 6 and 12 — "
                         "every number that makes a whole rectangle.",
           SANS, 8.4)
    D.text(c, x, y - 87, "5 is not a factor: twelve dots will not go into "
                         "rows of five without a gap.", SANSO, 8, color=MUTED)


# ── teaching pages ────────────────────────────────────────────────────────────

def unit_1():
    return [
        idea("Multiplication is a short way of writing equal groups. "
             f"4 {X} 3 means four groups with three in each, and the answer is "
             "what you get when you put them all together."),
        Canvas(80, _dia_groups, pad_below=7),
        worked([f"3 {X} 5 — three groups, five in each.",
                "Count them as 5, 10, 15 rather than one at a time.",
                f"So 3 {X} 5 = 15."]),
        watch("The groups have to be equal. Four groups of three and one group "
              "of two is not a multiplication — you cannot write it as "
              f"5 {X} something."),
        *try_these([I.GroupsItem(3, 4), I.GroupsItem(2, 5),
                    I.Horizontal(4, 2, "*"), I.Horizontal(3, 3, "*"),
                    I.Horizontal(2, 6, "*"), I.Horizontal(5, 2, "*")]),
    ]


def unit_2():
    return [
        idea("Draw the groups in neat rows and you have an array. Turn the "
             "array a quarter turn and the number of dots cannot change — so "
             f"3 {X} 4 and 4 {X} 3 are the same fact seen from two sides."),
        Canvas(84, _dia_array, pad_below=7),
        worked([f"2 {X} 8 — two rows of eight, which is 16.",
                "Turn it: eight rows of two, still 16.",
                f"So 8 {X} 2 = 16 as well, with nothing new to learn."]),
        watch("The turnaround does not change the answer, but it can change "
              f"how easy the work is. 2 {X} 9 is easier thought of as nine "
              "doubled than as two counted nine times."),
        *try_these([I.ArrayItem(3, 4), I.ArrayItem(4, 3),
                    I.Compare((3, 6), (6, 3), "*"),
                    I.Compare((2, 7), (7, 2), "*"),
                    I.Horizontal(6, 2, "*"), I.Horizontal(2, 6, "*")]),
    ]


def unit_3():
    return [
        idea("Three of the tables are already yours. Multiplying by 2 is "
             "doubling, which you have done since Book One. Multiplying by 10 "
             "gives that many tens. And multiplying by 5 is just half of "
             "multiplying by 10."),
        Canvas(96, _dia_2510, pad_below=7),
        worked([f"8 {X} 5 — first do the easy one: 8 {X} 10 = 80.",
                "Halve it: 40.",
                f"So 8 {X} 5 = 40."]),
        watch(f"7 {X} 10 is 70, not 710. The zero appears because seven tens "
              "is seventy — it is not a digit being stuck on the end for no "
              "reason."),
        *try_these([I.SkipCount(5, 8, (2, 4, 6)),
                    I.Horizontal(7, 2, "*"), I.Horizontal(9, 10, "*"),
                    I.Horizontal(6, 5, "*"), I.Horizontal(8, 2, "*"),
                    I.Horizontal(4, 5, "*"), I.Horizontal(3, 10, "*")]),
    ]


def unit_4():
    return [
        idea("One group of something is just that something. And no groups at "
             "all is nothing, however big the groups would have been."),
        Canvas(92, _dia_onezero, pad_below=7),
        worked([f"1 {X} 9 — one group of nine is nine.",
                f"0 {X} 9 — no groups, so nothing: 0.",
                f"9 {X} 0 — nine groups of nothing, also 0."]),
        watch(f"0 {X} 7 = 0, not 7. This is the opposite of adding zero, where "
              "the number survives untouched. Multiplying by zero destroys it."),
        *try_these([I.Horizontal(7, 1, "*"), I.Horizontal(1, 8, "*"),
                    I.Horizontal(6, 0, "*"), I.Horizontal(0, 9, "*"),
                    I.TrueFalse(5, 0, 5, "*"), I.TrueFalse(1, 6, 6, "*"),
                    I.Horizontal(10, 1, "*"), I.Horizontal(0, 0, "*")]),
    ]


def unit_5():
    return [
        idea("The 4s come free from the 2s: multiplying by 4 is doubling "
             "twice. And the 3s are the 2s plus one more group."),
        Canvas(80, _dia_34, pad_below=7),
        worked([f"6 {X} 4 — double 6 to get 12.",
                "Double again to get 24.",
                f"So 6 {X} 4 = 24."]),
        watch("Double twice, not three times. Doubling 6 twice gives 24, which "
              f"is 6 {X} 4. Doubling a third time would give 48, which is "
              f"6 {X} 8 — a different fact."),
        *try_these([I.Horizontal(7, 4, "*"), I.Horizontal(6, 3, "*"),
                    I.Horizontal(8, 4, "*"), I.Horizontal(9, 3, "*"),
                    I.Horizontal(4, 6, "*"), I.Horizontal(3, 8, "*"),
                    I.MissingSlot(4, 7, "*", "b"),
                    I.MissingSlot(3, 9, "*", "b")]),
    ]


def unit_6():
    return [
        idea("What is left is the middle of the table, and none of it has to "
             "be memorised cold. Nine of something is ten of them with one "
             "given back. And every fact sits one row away from a square you "
             "already know."),
        Canvas(88, _dia_hard, pad_below=7),
        worked([f"9 {X} 6 — ten sixes is 60.",
                "Give one six back: 60 " + M + " 6 = 54.",
                f"So 9 {X} 6 = 54."]),
        watch("Give back one *group*, not one. For nine sevens you subtract "
              "seven from seventy, not one."),
        *try_these([I.Horizontal(9, 7, "*"), I.Horizontal(9, 4, "*"),
                    I.Horizontal(7, 7, "*"), I.Horizontal(6, 8, "*"),
                    I.Horizontal(8, 8, "*"), I.Horizontal(7, 6, "*"),
                    I.Horizontal(6, 6, "*"), I.Horizontal(8, 9, "*")]),
    ]


def unit_7():
    return [
        idea("Here is the whole table at once. It is worth looking at as one "
             "object, because it contains far less than it appears to: the two "
             "halves are the same, and most of the rows you already own."),
        Canvas(178, _dia_table, pad_below=8),
        watch("If you find yourself counting up in ones to reach a fact, stop "
              "and find the nearest thing you do know — a square, a ten, or "
              "the turnaround."),
        *try_these([I.Horizontal(6, 7, "*"), I.Horizontal(8, 6, "*"),
                    I.Horizontal(7, 9, "*"), I.Horizontal(4, 8, "*"),
                    I.Horizontal(9, 8, "*"), I.Horizontal(6, 9, "*"),
                    I.Horizontal(7, 8, "*"), I.Horizontal(8, 8, "*")]),
    ]


def unit_8():
    return [
        idea("A hard fact can always be cut into two easy ones. Split one "
             "factor, multiply each piece, add the pieces back."),
        Canvas(80, _dia_distribute, pad_below=6),
        worked([f"8 {X} 7 — split the 8 into 5 and 3.",
                f"5 {X} 7 = 35 and 3 {X} 7 = 21.",
                "Add them: 35 + 21 = 56."]),
        watch(f"Split one factor only. 8 {X} 7 is not 4 {X} 3 doubled."),
        *try_these([I.AreaSplit(7, 6, 5),
                    I.Horizontal(8, 7, "*"), I.Horizontal(6, 9, "*"),
                    I.Horizontal(9, 7, "*"), I.Horizontal(8, 6, "*")]),
    ]


def unit_9():
    return [
        idea("Two-digit multiplication is last unit's cut, made at ten instead "
             "of five. The column method does exactly this."),
        Canvas(94, _dia_twodigitmul, pad_below=6),
        worked([f"16 {X} 3 — split 16 into 10 and 6.",
                f"10 {X} 3 = 30, 6 {X} 3 = 18, and 30 + 18 = 48."]),
        watch(f"23 {X} 4 is not 8 followed by 12. The pieces are 80 and 12, "
              "and they must be added: 92."),
        *try_these([I.AreaSplit(13, 4, 10),
                    I.Column(14, 3, "*"), I.Column(23, 4, "*"),
                    I.Horizontal(12, 4, "*"), I.Horizontal(21, 3, "*")]),
    ]


def unit_10():
    return [
        idea("A factor of a number is anything that divides into it exactly — "
             "anything that makes a whole rectangle with no dots left over. "
             "Knowing a number's factors is knowing what it is made of."),
        Canvas(92, _dia_factors, pad_below=7),
        worked(["Is 4 a factor of 20? Try to make rows of 4.",
                "Five rows of 4 uses all twenty dots exactly.",
                f"Yes: 5 {X} 4 = 20, so 4 is a factor of 20."]),
        watch("Factors come in pairs, and 1 and the number itself always "
              "count. Every list of factors starts at 1 and ends at the "
              "number."),
        *try_these([I.AllFactors(18), I.AllFactors(20),
                    I.MissingSlot(6, 7, "*", "a"),
                    I.MissingSlot(8, 4, "*", "b")]),
    ]


# ── compact reminders ─────────────────────────────────────────────────────────

def _rem_groups(c, x, y, w):
    D.groups(c, x, y, 3, 4, ring=11.0, gap=5, per_row=3)
    D.text(c, x + 96, y - 14, f"3 {X} 4  =  12", NUMB, 11, color=ACCENT)
    D.text(c, x + 96, y - 27, "three groups of four", SANSO, 7.4, color=MUTED)
    D.text(c, x + 200, y - 14, "4 + 4 + 4 = 12", NUM, 9, color=MUTED)


def _rem_array(c, x, y, w):
    D.array(c, x, y, 4, 3, cell=9.0)
    D.array(c, x + 52, y, 3, 4, cell=9.0)
    D.text(c, x + 106, y - 14, f"3 {X} 4  =  4 {X} 3  =  12", NUMB, 11,
           color=ACCENT)
    D.text(c, x + 106, y - 28, "turn the array — the dots do not change",
           SANSO, 7.4, color=MUTED)


def _rem_2510(c, x, y, w):
    D.text(c, x, y - 10, f"{X}2 is doubling", SANSB, 8.4, color=ACCENT)
    D.text(c, x + 80, y - 10, f"{X}10 is that many tens", SANSB, 8.4,
           color=ACCENT)
    D.text(c, x + 196, y - 10, f"{X}5 is half of {X}10", SANSB, 8.4,
           color=ACCENT)
    D.text(c, x, y - 25, "2  4  6  8  10  12  14  16  18  20", NUM, 8.2,
           color=MUTED)
    D.text(c, x, y - 37, "5  10  15  20  25  30  35  40  45  50", NUM, 8.2,
           color=MUTED)


def _rem_onezero(c, x, y, w):
    D.text(c, x, y - 11, f"n {X} 1  =  n", NUMB, 11, color=ACCENT)
    D.text(c, x + 90, y - 11, f"n {X} 0  =  0", NUMB, 11, color=ACCENT)
    D.text(c, x, y - 27, "One group of it is it. No groups is nothing.",
           SANS, 8.2)
    D.text(c, x, y - 39, "Careful: adding 0 keeps the number, "
                         "multiplying by 0 does not.", SANSO, 7.4, color=MUTED)


def _rem_34(c, x, y, w):
    D.text(c, x, y - 11, f"{X}4  =  double, then double again", SANSB, 8.6,
           color=ACCENT)
    D.text(c, x, y - 25, f"7 {X} 4  →  14  →  28", NUMB, 10)
    D.text(c, x + 150, y - 11, f"{X}3  =  double, then add one more group",
           SANSB, 8.6, color=ACCENT)
    D.text(c, x + 150, y - 25, f"7 {X} 3  →  14 + 7  =  21", NUMB, 10)


def _rem_hard(c, x, y, w):
    D.text(c, x, y - 10, f"{X}9  =  {X}10 with one group given back",
           SANSB, 8.6, color=ACCENT)
    D.text(c, x, y - 24, f"9 {X} 7  =  70 {M} 7  =  63", NUMB, 10.5)
    D.text(c, x, y - 39, f"Squares:  6{X}6=36   7{X}7=49   8{X}8=64   "
                         f"9{X}9=81", NUM, 8.2, color=MUTED)


def _rem_table(c, x, y, w):
    D.text(c, x, y - 10, "Nearest thing you know, then adjust.", SANSB, 8.6,
           color=ACCENT)
    D.text(c, x, y - 25, f"6{X}7  →  6{X}6 = 36, add one 6  →  42", NUMB, 9.5)
    D.text(c, x, y - 38, f"Turnaround, squares, {X}10 and halving cover "
                         "almost everything.", SANSO, 7.4, color=MUTED)


def _rem_distribute(c, x, y, w):
    D.text(c, x, y - 10, "Split one factor. Multiply each piece. Add them "
                         "back.", SANS, 8.4)
    D.text(c, x, y - 26, f"8 {X} 7  =  (5 {X} 7) + (3 {X} 7)  =  35 + 21  "
                         f"=  56", NUMB, 10, color=ACCENT)
    D.text(c, x, y - 39, "Split one factor only — never both.", SANSO, 7.4,
           color=MUTED)


def _rem_twodigitmul(c, x, y, w):
    D.text(c, x, y - 10, f"13 {X} 4  =  (10 {X} 4) + (3 {X} 4)  =  40 + 12  "
                         f"=  52", NUMB, 10, color=ACCENT)
    D.text(c, x, y - 25, f"23 {X} 4  =  80 + 12  =  92", NUMB, 10,
           color=ACCENT)
    D.text(c, x, y - 38, "Tens piece, ones piece, then add. "
                         "The two pieces are never just written side by side.",
           SANSO, 7.4, color=MUTED)


def _rem_factors(c, x, y, w):
    D.text(c, x, y - 10, "A factor divides in exactly, with nothing left over.",
           SANS, 8.4)
    D.text(c, x, y - 26, f"12  =  1{X}12  =  2{X}6  =  3{X}4", NUMB, 10,
           color=ACCENT)
    D.text(c, x, y - 39, "Factors of 12: 1, 2, 3, 4, 6, 12. "
                         "Always starts at 1 and ends at the number.",
           SANSO, 7.4, color=MUTED)


# ── the ten multiplication units ─────────────────────────────────────────────

MUL_UNITS = [
    Unit(1, "Equal Groups", "groups of",
         "a × b means a groups with b in each. Count the groups, not the dots.",
         pool_equal_groups(),
         [f_groups, f_array],
         [(3.4, f_plain), (1.4, f_missing), (1.0, f_groups), (0.8, f_array),
          (0.6, f_tf)],
         [(1, f_plain)],
         _rem_groups, 42, unit_1, "4 min", "3 min", op="*"),

    Unit(2, "Arrays and the Turnaround", "turn it round",
         "a × b = b × a. The same array, a quarter turn on.",
         pool_arrays(),
         [f_array, f_groups],
         [(3.0, f_plain), (1.4, f_compare), (1.2, f_missing), (1.0, f_array),
          (0.6, f_tf)],
         [(1, f_plain)],
         _rem_array, 42, unit_2, "4 min", "3 min", op="*"),

    Unit(3, "Twos, Fives and Tens", "the easy tables",
         "×2 is doubling. ×10 gives that many tens. ×5 is half of ×10.",
         pool_2_5_10(),
         [f_array, f_groups],
         [(3.4, f_plain), (1.6, f_missing), (1.0, f_skip), (0.8, f_compare),
          (0.6, f_tf)],
         [(1, f_plain)],
         _rem_2510, 42, unit_3, "4 min", "3 min", op="*"),

    Unit(4, "Ones and Zeros", "identity and nothing",
         "One group of it is it. No groups at all is nothing.",
         pool_one_zero(),
         [f_groups, f_array],
         [(3.4, f_plain), (1.4, f_missing), (1.0, f_tf), (0.8, f_compare),
          (0.5, f_error)],
         [(1, f_plain)],
         _rem_onezero, 42, unit_4, "3 min", "2 min", op="*"),

    Unit(5, "Threes and Fours", "double and double again",
         "×4 is doubling twice. ×3 is doubling, then one more group.",
         pool_3_4(),
         [f_array, f_family],
         [(3.6, f_plain), (1.6, f_missing), (0.9, f_compare), (0.7, f_tf),
          (0.5, f_error)],
         [(1, f_plain)],
         _rem_34, 42, unit_5, "4 min", "3 min", op="*"),

    Unit(6, "Sixes, Sevens, Eights and Nines", "the middle of the table",
         "×9 is ×10 with one group given back. Squares are landmarks.",
         pool_6_to_9(),
         [f_array, f_areasplit],
         [(3.4, f_plain), (1.6, f_missing), (1.0, f_areasplit),
          (0.8, f_compare), (0.6, f_tf), (0.6, f_error)],
         [(1, f_plain)],
         _rem_hard, 42, unit_6, "5 min", "4 min", op="*"),

    Unit(7, "All Facts to Ten Times Ten", "the whole table",
         "Work from the nearest fact you know, then adjust by one row.",
         pool_all_tables(),
         [f_array, f_areasplit],
         [(3.4, f_plain), (1.8, f_missing), (1.2, f_balance), (1.0, f_compare),
          (0.8, f_tf), (0.5, f_error)],
         [(1, f_plain)],
         _rem_table, 42, unit_7, "5 min", "4 min", op="*"),

    Unit(8, "Breaking a Product Apart", "split and add back",
         "Split one factor, multiply each piece, add the pieces back.",
         pool_distribute(),
         [f_areasplit, f_array],
         [(2.4, f_plain), (2.0, f_areasplit), (1.4, f_missing),
          (0.8, f_balance), (0.6, f_error)],
         [(1, f_plain)],
         _rem_distribute, 44, unit_8, "5 min", "4 min", op="*"),

    Unit(9, "Tens, and Two-Digit Multiplication", "cut it at ten",
         "Multiply the tens, multiply the ones, then add the two answers.",
         pool_times_tens(),
         [f_areasplit, f_column],
         [(2.6, f_plain), (2.0, f_column), (1.6, f_areasplit),
          (1.0, f_missing), (0.6, f_compare)],
         [(1, f_plain)],
         _rem_twodigitmul, 42, unit_9, "6 min", "4 min", op="*",
         late_pool=pool_two_digit_mul(), late_from=8),

    Unit(10, "Factors, Multiples and Missing Factors", "what a number is made of",
         "A factor divides in exactly. Factors come in pairs.",
         pool_factors(),
         [f_array, f_areasplit],
         [(2.6, f_missing), (2.0, f_plain), (1.2, f_factors), (1.0, f_skip),
          (0.8, f_compare), (0.5, f_error)],
         [(1, f_plain)],
         _rem_factors, 42, unit_10, "5 min", "4 min", op="*"),
]
