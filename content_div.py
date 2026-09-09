"""
Book Two, second half: division.

Division is introduced as the inverse of multiplication, in the same way
subtraction was introduced as the inverse of addition — as a fact family read
in a different direction rather than a fresh table to memorise.

Two things get explicit attention that drill books usually skip. The first is
that division has *two* meanings: sharing 12 between 3 and packing 12 into
groups of 3 are different questions with the same answer, and a child who has
only met one of them is lost the moment a word problem uses the other. The
second is division by zero — not as a rule to obey but as a question with no
answer, which a child can see for themselves.
"""

import draw as D
from draw import (INK, ACCENT, WARM, MUTED, HAIR, FAINT, TINT, OP_SYM,
                  SANS, SANSB, SANSO, NUM, NUMB)
from layout import (Block, Space, Rule, Heading, Text, Bullets, Canvas,
                    Panel, Grid, Strip)
from teach import idea, watch, worked, why, try_these
import curriculum as C
from curriculum import (Unit, f_plain, f_missing, f_tf, f_compare, f_balance,
                        f_family, f_error, f_share, f_partbar, f_remainder,
                        f_array, f_muldiv_chain, MIXED_MIX)
import items as I

X = OP_SYM["*"]
V = OP_SYM["/"]
M = OP_SYM["-"]


# ── fact pools ────────────────────────────────────────────────────────────────

def _dedupe(pairs):
    seen, out = set(), []
    for p in pairs:
        if p not in seen:
            seen.add(p)
            out.append(p)
    return out


def pool_share_small():
    return _dedupe([(b * q, b) for b in range(2, 7) for q in range(1, 7)])


def pool_div_families():
    return _dedupe([(a * b, b) for a in range(2, 11) for b in range(2, 11)
                    if a * b <= 100])


def pool_div_2_5_10():
    return _dedupe([(q * b, b) for b in (2, 5, 10) for q in range(1, 11)])


def pool_div_one_self():
    out = [(n, 1) for n in range(1, 21)]
    out += [(n, n) for n in range(1, 11)]
    out += [(0, n) for n in range(1, 11)]
    return _dedupe(out)


def pool_div_3_4_6():
    return _dedupe([(q * b, b) for b in (3, 4, 6) for q in range(1, 11)])


def pool_all_div():
    return _dedupe([(q * b, b) for b in range(1, 11) for q in range(1, 11)])


def pool_remainder_base():
    return _dedupe([(q * b, b) for b in range(2, 10) for q in range(1, 11)
                    if q * b <= 90])


def pool_div_tens():
    out = []
    for b in range(2, 10):
        for q in range(10, 50):
            if q * b <= 99:
                out.append((q * b, b))
    return _dedupe(out)


def pool_muldiv():
    return _dedupe([(a, b) for a in range(2, 11) for b in range(2, 11)])


def pool_four_operations():
    """(a, b, op) triples spanning everything in Levels A and B."""
    out = []
    out += [(a, b, "+") for a in range(8, 20) for b in range(3, 10)
            if a + b <= 20]
    out += [(a, b, "-") for a in range(10, 21) for b in range(3, 10)
            if a - b >= 0]
    out += [(a, b, "*") for a in range(2, 11) for b in range(2, 11)]
    out += [(q * b, b, "/") for b in range(2, 11) for q in range(2, 11)
            if q * b <= 100]
    return out


# ── diagrams ──────────────────────────────────────────────────────────────────

def _dia_sharegroup(c, x, y, w):
    D.text(c, x, y - 8, "“Share 12 between 3”", SANSB, 8.6, color=ACCENT)
    D.groups(c, x, y - 14, 3, 4, ring=13.0, gap=5, per_row=3)
    D.text(c, x, y - 50, "3 groups made. 4 in each.", SANSO, 7.4, color=MUTED)
    D.text(c, x, y - 63, "The answer is how many EACH.", SANS, 8)

    D.text(c, x + 176, y - 8, "“Put 12 into groups of 3”", SANSB, 8.6,
           color=ACCENT)
    D.groups(c, x + 176, y - 14, 4, 3, ring=13.0, gap=5, per_row=4)
    D.text(c, x + 176, y - 50, "3 in each. 4 groups made.", SANSO, 7.4,
           color=MUTED)
    D.text(c, x + 176, y - 63, "The answer is how many GROUPS.", SANS, 8)

    D.rule(c, x, y - 72, x + w, 0.4)
    D.text(c, x, y - 84, f"Both are written 12 {V} 3 = 4. Same sum, two "
                         "different questions.", NUMB, 9, color=INK)


def _dia_divfamily(c, x, y, w):
    D.fact_triangle(c, x + 44, y - 2, 12, (3, 4), "*")
    ex = x + 108
    facts = [f"3 {X} 4 = 12", f"4 {X} 3 = 12",
             f"12 {V} 3 = 4", f"12 {V} 4 = 3"]
    for i, f in enumerate(facts):
        col, row = divmod(i, 2)
        D.text(c, ex + col * 96, y - 18 - row * 18, f, NUMB, 10,
               color=ACCENT if i > 1 else INK)
    D.text(c, ex, y - 62, "The same three numbers. Nothing extra to learn.",
           SANSO, 8, color=MUTED)


def _dia_div2510(c, x, y, w):
    D.text(c, x, y - 10, f"{V}2 is halving", SANSB, 8.8, color=ACCENT)
    D.text(c, x, y - 24, f"18 {V} 2 = 9", NUMB, 10)
    D.text(c, x + 108, y - 10, f"{V}10 takes off a ten", SANSB, 8.8,
           color=ACCENT)
    D.text(c, x + 108, y - 24, f"60 {V} 10 = 6", NUMB, 10)
    D.text(c, x + 230, y - 10, f"{V}5 is {V}10, doubled", SANSB, 8.8,
           color=ACCENT)
    D.text(c, x + 230, y - 24, f"60 {V} 5 = 12", NUMB, 10)
    D.rule(c, x, y - 36, x + w, 0.4)
    D.part_bar(c, x + 10, y - 48, w - 40, 5, 16, label=60, part_label=12)
    D.text(c, x, y - 92, "Sixty split into five equal parts: twelve in each. "
                         "Half as many parts as tens, so twice as big.",
           SANSO, 8, color=MUTED)


def _dia_divone(c, x, y, w):
    D.text(c, x, y - 10, f"7 {V} 1 = 7", NUMB, 11, color=ACCENT)
    D.text(c, x + 84, y - 10, "groups of one: seven of them", SANSO, 8,
           color=MUTED)
    D.text(c, x, y - 26, f"7 {V} 7 = 1", NUMB, 11, color=ACCENT)
    D.text(c, x + 84, y - 26, "groups of seven: just the one", SANSO, 8,
           color=MUTED)
    D.text(c, x, y - 42, f"0 {V} 7 = 0", NUMB, 11, color=ACCENT)
    D.text(c, x + 84, y - 42, "nothing to share out", SANSO, 8, color=MUTED)
    D.rule(c, x, y - 54, x + w, 0.4)
    D.text(c, x, y - 68, f"But 7 {V} 0 has no answer at all.", SANSB, 9,
           color=WARM)
    for k in range(5):
        c.setStrokeColor(HAIR)
        c.setDash([1.5, 1.5])
        c.setLineWidth(0.7)
        c.circle(x + 12 + k * 26, y - 88, 9, stroke=1, fill=0)
        c.setDash([])
    D.text(c, x + 146, y - 92, "How many empty groups make seven? "
                               "No number of them ever will.", SANS, 8.2)


def _dia_div346(c, x, y, w):
    D.text(c, x, y - 8, f"28 {V} 4   —   ask the multiplication question",
           SANSB, 9)
    D.text(c, x, y - 26, f"“How many 4s make 28?”", SANS, 9, color=MUTED)
    D.seq(c, x + 130, y - 26, [f"4 {X} ? = 28", "? = 7"], NUMB, 9.5, ACCENT,
          gap=6)
    D.rule(c, x, y - 38, x + w, 0.4)
    D.part_bar(c, x + 10, y - 50, w - 40, 7, 16, label=28, part_label=4)
    D.text(c, x, y - 94, f"Twenty-eight cut into fours: seven pieces. "
                         f"So 28 {V} 4 = 7, and 4 {X} 7 = 28 says the same "
                         "thing.", SANSO, 8, color=MUTED)


def _dia_alldiv(c, x, y, w):
    D.times_grid(c, x, y - 2, 10, cell=13.0, size=5.2, shade_upper=False,
                 highlight=[(6, j) for j in range(1, 11)])
    tx = x + 162
    D.text(c, tx, y - 14, "Read the table backwards.", SANSB, 8.8,
           color=ACCENT)
    lines = [
        f"To do 54 {V} 6, run along the",
        "6 row until you reach 54.",
        "",
        "It is under the 9.",
        f"So 54 {V} 6 = 9.",
        "",
        "Every division fact you will",
        "ever need in this book is",
        "already somewhere in this",
        "grid. There is no second",
        "table to learn.",
    ]
    yy = y - 30
    for ln in lines:
        D.text(c, tx, yy, ln, SANS, 7.8, color=INK if ln else MUTED)
        yy -= 10.5


def _dia_remainder(c, x, y, w):
    D.text(c, x, y - 8, f"17 {V} 5   —   pack them into fives", SANSB, 9)
    D.groups(c, x, y - 16, 3, 5, ring=14.0, gap=6, per_row=3)
    for k in range(2):
        D.dot(c, x + 128 + k * 12, y - 30, 3.0, WARM)
    c.setStrokeColor(WARM)
    c.setDash([1.5, 1.5])
    c.setLineWidth(0.8)
    c.circle(x + 134, y - 30, 15, stroke=1, fill=0)
    c.setDash([])
    D.text(c, x + 134, y - 52, "2 left over", SANSO, 7.4, "center", WARM)
    D.text(c, x + 176, y - 26, f"17 {V} 5  =  3 remainder 2", NUMB, 10.5,
           color=ACCENT)
    D.text(c, x + 176, y - 42, f"check:  3 {X} 5 + 2  =  17", NUM, 9,
           color=MUTED)
    D.rule(c, x, y - 62, x + w, 0.4)
    D.text(c, x, y - 74, "Three full fives, and two left that will not make "
                         "a fourth.", SANS, 8.4)
    D.text(c, x, y - 86, "The answer has two parts, and both of them have "
                         "to be written down.", SANSO, 8, color=MUTED)


def _dia_divtens(c, x, y, w):
    D.text(c, x, y - 8, f"84 {V} 4   —   split it into easy pieces", SANSB, 9)
    D.text(c, x, y - 26, f"84  =  80 + 4", NUM, 10, color=MUTED)
    D.text(c, x, y - 42, f"80 {V} 4 = 20      4 {V} 4 = 1", NUMB, 10,
           color=ACCENT)
    D.text(c, x, y - 58, f"20 + 1  =  21", NUMB, 11, color=INK)
    D.bar_model(c, x + 176, y - 18, 150, 80, 4, 18, labels=("80", "4"),
                total_label="84")
    D.text(c, x + 176, y - 62, "twenty fours in the 80, one more in the 4",
           SANSO, 7.4, color=MUTED)
    D.rule(c, x, y - 74, x + w, 0.4)
    D.text(c, x, y - 86, f"Check by multiplying back: 21 {X} 4 = 84.",
           SANS, 8.4)


def _dia_muldiv(c, x, y, w):
    D.text(c, x, y - 8, f"6 {X} 4 {V} 3   —   work left to right", SANSB, 9)
    D.seq(c, x, y - 26, [f"6 {X} 4 = 24", f"24 {V} 3 = 8"], NUMB, 10.5,
          ACCENT, gap=8)
    D.rule(c, x, y - 38, x + w, 0.4)
    D.text(c, x, y - 52, "Multiplying then dividing by the same number "
                         "gets you back where you started:", SANS, 8.4)
    D.seq(c, x, y - 68, [f"7 {X} 5 = 35", f"35 {V} 5 = 7"], NUMB, 10.5, INK,
          gap=8)
    D.text(c, x, y - 82, "That is why every division can be checked by "
                         "multiplying the answer back.", SANSO, 8, color=MUTED)


def _dia_choose(c, x, y, w):
    cw = (w - 60) / 2
    D.text(c, x + 62 + cw / 2, y - 8, "PARTS NOT EQUAL", SANSB, 6.8, "center",
           MUTED)
    D.text(c, x + 66 + cw + cw / 2, y - 8, "PARTS ALL EQUAL", SANSB, 6.8,
           "center", MUTED)
    cells = [("putting\ntogether", f"add   +", f"multiply   {X}"),
             ("taking\napart", f"subtract   {M}", f"divide   {V}")]
    yy = y - 14
    for label, left, right in cells:
        c.setStrokeColor(HAIR)
        c.setLineWidth(0.5)
        for k, txt in enumerate((left, right)):
            bx = x + 62 + k * (cw + 4)
            c.setFillColor(TINT if k else FAINT)
            c.rect(bx, yy - 30, cw, 30, stroke=1, fill=1)
            D.text(c, bx + cw / 2, yy - 19, txt, SANSB, 10, "center", ACCENT)
        for k, ln in enumerate(label.split("\n")):
            D.text(c, x + 56, yy - 12 - k * 9, ln, SANSB, 7.8, "right", INK)
        yy -= 34
    D.rule(c, x, yy - 2, x + w, 0.4)
    D.text(c, x, yy - 14, "Ask those two questions of the story before you "
                          "write anything down.", SANS, 8.4)
    D.text(c, x, yy - 26, "Do not choose by hunting for a word. "
                          "“Altogether” appears in addition and in "
                          "multiplication alike.", SANSO, 7.8, color=WARM)


# ── teaching pages ────────────────────────────────────────────────────────────

def unit_1():
    return [
        idea("Division asks one of two questions, and they are not the same "
             "question. Sharing asks how many each will get. Grouping asks how "
             "many groups you can make. Both are written the same way."),
        Canvas(92, _dia_sharegroup, pad_below=7),
        worked([f"20 {V} 5, read as sharing: 20 shared between 5, so 4 each.",
                f"20 {V} 5, read as grouping: 20 packed in fives, so 4 groups.",
                "The answer is 4 either way — but it counts different things."]),
        watch("Read the story carefully before you write the answer. "
              "“4 sweets each” and “4 bags” are not the same statement, even "
              "though the arithmetic is identical."),
        *try_these([I.ShareItem(12, 3), I.ShareItem(20, 4),
                    I.Horizontal(15, 5, "/"), I.Horizontal(18, 3, "/"),
                    I.Horizontal(16, 4, "/"), I.Horizontal(10, 2, "/")]),
    ]


def unit_2():
    return [
        idea("Division undoes multiplication, exactly as subtraction undoes "
             "addition. Three numbers that make a multiplication fact also "
             "make two division facts, and you already know all of them."),
        Canvas(74, _dia_divfamily, pad_below=7),
        worked([f"The family is 3, 4 and 12.",
                f"Multiplying the parts gives the whole: 3 {X} 4 = 12.",
                f"Dividing the whole by one part gives the other: "
                f"12 {V} 3 = 4."]),
        watch("The whole always comes first in a division. From 3, 4, 12 you "
              f"can write 12 {V} 3 and 12 {V} 4 — but not 3 {V} 12."),
        *try_these([I.FactFamily(12, (3, 4), "*"),
                    I.Horizontal(20, 5, "/"), I.Horizontal(20, 4, "/"),
                    I.MissingSlot(18, 3, "/", "b"),
                    I.MissingSlot(24, 6, "/", "a")]),
    ]


def unit_3():
    return [
        idea("The three easy times tables give three easy division tables. "
             "Dividing by 2 is halving. Dividing by 10 takes a ten off the "
             "end. Dividing by 5 is dividing by 10 and then doubling, because "
             "half as many parts must each be twice as big."),
        Canvas(96, _dia_div2510, pad_below=7),
        worked([f"70 {V} 5 — first the easy one: 70 {V} 10 = 7.",
                "Five parts instead of ten, so each is twice as big.",
                f"Double it: 70 {V} 5 = 14."]),
        watch(f"80 {V} 10 = 8, not 80. Taking off a zero is what dividing by "
              "ten looks like on paper, but what it means is making ten equal "
              "groups."),
        *try_these([I.PartBarItem(20, 5), I.PartBarItem(18, 2),
                    I.Horizontal(16, 2, "/"), I.Horizontal(90, 10, "/"),
                    I.Horizontal(35, 5, "/"), I.Horizontal(14, 2, "/")]),
    ]


def unit_4():
    return [
        idea("Three easy cases, and one that has no answer. Dividing by 1 "
             "leaves the number alone. Dividing a number by itself gives 1. "
             "Dividing nothing gives nothing. Dividing BY nothing is not a "
             "question arithmetic can answer."),
        Canvas(100, _dia_divone, pad_below=7),
        worked([f"9 {V} 1 — groups of one, so there are nine of them: 9.",
                f"9 {V} 9 — groups of nine, and there is exactly one: 1.",
                f"0 {V} 9 — nothing to share out, so 0."]),
        watch(f"9 {V} 0 is not 0, and it is not 9. It has no answer. Ask "
              "yourself how many empty groups you would need to hold nine "
              "things — you can keep adding empty groups forever and never "
              "get there."),
        *try_these([I.Horizontal(8, 1, "/"), I.Horizontal(6, 6, "/"),
                    I.Horizontal(0, 4, "/"), I.Horizontal(15, 1, "/"),
                    I.TrueFalse(7, 7, 1, "/"), I.TrueFalse(0, 5, 5, "/"),
                    I.Horizontal(9, 9, "/"), I.Horizontal(12, 1, "/")]),
    ]


def unit_5():
    return [
        idea("For the rest of the tables, turn the division into the "
             "multiplication question you already know how to answer. "
             f"28 {V} 4 is asking: how many fours make 28?"),
        Canvas(96, _dia_div346, pad_below=7),
        worked([f"24 {V} 6 — ask: how many sixes make 24?",
                f"Run up the sixes: 6, 12, 18, 24. That is four of them.",
                f"So 24 {V} 6 = 4."]),
        watch("Count the groups, not the numbers you said. Saying "
              "“6, 12, 18, 24” is four sixes, not five — the starting 6 is "
              "already one group."),
        *try_these([I.Horizontal(21, 3, "/"), I.Horizontal(32, 4, "/"),
                    I.Horizontal(42, 6, "/"), I.Horizontal(27, 3, "/"),
                    I.MissingSlot(36, 4, "/", "b"),
                    I.MissingSlot(30, 6, "/", "a"),
                    I.Horizontal(24, 4, "/"), I.Horizontal(18, 6, "/")]),
    ]


def unit_6():
    return [
        idea("There is no division table. There is only the multiplication "
             "table, read in the other direction — and you already have the "
             "whole of it."),
        Canvas(160, _dia_alldiv, pad_below=8),
        watch("If a number is not in the row you are searching, the division "
              "does not come out exactly. That is not a mistake; it means "
              "there is a remainder, which is the next unit but one."),
        *try_these([I.Horizontal(56, 7, "/"), I.Horizontal(63, 9, "/"),
                    I.Horizontal(48, 8, "/"), I.Horizontal(45, 5, "/"),
                    I.Horizontal(72, 8, "/"), I.Horizontal(54, 6, "/"),
                    I.Horizontal(36, 9, "/"), I.Horizontal(49, 7, "/"),
                    I.Horizontal(42, 6, "/"), I.Horizontal(64, 8, "/")]),
    ]


def unit_7():
    return [
        idea("Not everything shares out evenly. What is left over when no "
             "more whole groups can be made is called the remainder, and "
             "saying it is part of giving the answer."),
        Canvas(90, _dia_remainder, pad_below=7),
        worked([f"23 {V} 4 — how many fours fit into 23?",
                f"Five fours is 20, and six fours would be 24, which is too "
                "many.",
                f"So 23 {V} 4 = 5 remainder 3. Check: 5 {X} 4 + 3 = 23."]),
        watch("The remainder must be smaller than the number you are dividing "
              f"by. If you write 23 {V} 4 = 4 remainder 7, look again — "
              "another four still fits inside that 7."),
        *try_these([I.Remainder(17, 5), I.Remainder(23, 4),
                    I.Remainder(19, 3), I.Remainder(30, 7),
                    I.Remainder(25, 6), I.Remainder(13, 2),
                    I.Remainder(29, 5), I.Remainder(22, 6)]),
    ]


def unit_8():
    return [
        idea("Big numbers divide the same way big numbers multiply: split "
             "them into friendly pieces, divide each piece, and add the "
             "answers."),
        Canvas(96, _dia_divtens, pad_below=7),
        worked([f"96 {V} 3 — split 96 into 90 and 6.",
                f"90 {V} 3 = 30 and 6 {V} 3 = 2.",
                f"Add them: 32. Check: 32 {X} 3 = 96."]),
        watch("Split into pieces that each divide exactly. For 84 " + V +
              " 4, splitting into 80 and 4 works; splitting into 50 and 34 "
              "does not help at all."),
        *try_these([I.Horizontal(60, 3, "/"), I.Horizontal(84, 4, "/"),
                    I.Horizontal(96, 3, "/"), I.Horizontal(75, 5, "/"),
                    I.MissingSlot(90, 6, "/", "b"),
                    I.MissingSlot(64, 4, "/", "a")]),
    ]


def unit_9():
    return [
        idea("Multiplying and dividing undo each other. That gives you a way "
             "to work along a chain, and — more useful — a way to check every "
             "answer you write without asking anybody."),
        Canvas(92, _dia_muldiv, pad_below=7),
        worked([f"8 {X} 6 {V} 4 — first step: 8 {X} 6 = 48.",
                f"Second step: 48 {V} 4 = 12.",
                f"Check the division by multiplying back: 12 {X} 4 = 48."]),
        watch("Work along the chain in order. Doing the division first gives "
              "a different answer, and only one of them is right."),
        *try_these([I.Chain((8, 6, 4), ("*", "/")),
                    I.Chain((36, 6, 5), ("/", "*")),
                    I.Chain((7, 4, 2), ("*", "/")),
                    I.Chain((48, 8, 7), ("/", "*")),
                    I.Chain((9, 4, 6), ("*", "/")),
                    I.Chain((54, 9, 8), ("/", "*"))]),
    ]


def unit_10():
    return [
        idea("The last thing to learn is which operation a question wants. "
             "Two questions decide it every time: are you putting together or "
             "taking apart, and are the parts equal?"),
        Canvas(122, _dia_choose, pad_below=7),
        worked(["“6 bags with 4 apples in each — how many apples?” "
                "Putting together, equal parts: multiply.",
                "“24 apples shared between 6 — how many each?” "
                "Taking apart, equal parts: divide.",
                "“24 apples, 6 are eaten — how many left?” "
                "Taking apart, unequal: subtract."]),
        watch("Key words are a hint, never a rule. “How many altogether?” is "
              "an addition question in one story and a multiplication question "
              "in the next. The two questions above are what actually decide "
              "it."),
        *try_these([I.Horizontal(7, 8, "+"), I.Horizontal(15, 6, "-"),
                    I.Horizontal(7, 6, "*"), I.Horizontal(42, 7, "/"),
                    I.Horizontal(9, 9, "*"), I.Horizontal(56, 8, "/")]),
    ]


# ── compact reminders ─────────────────────────────────────────────────────────

def _rem_sharegroup(c, x, y, w):
    D.text(c, x, y - 10, f"12 {V} 3 = 4", NUMB, 11, color=ACCENT)
    D.text(c, x + 76, y - 10, "shared between 3   →   4 EACH", SANS, 8.4)
    D.text(c, x + 76, y - 24, "put into groups of 3   →   4 GROUPS", SANS, 8.4)
    D.text(c, x, y - 38, "Same sum, two different questions. "
                         "Read the story to see which.", SANSO, 7.4,
           color=MUTED)


def _rem_divfamily(c, x, y, w):
    D.fact_triangle(c, x + 30, y + 2, 12, (3, 4), "*", size=9, h=42,
                    half_w=26)
    D.text(c, x + 76, y - 12, f"3 {X} 4 = 12      12 {V} 3 = 4", NUMB, 9.5,
           color=ACCENT)
    D.text(c, x + 76, y - 26, f"4 {X} 3 = 12      12 {V} 4 = 3", NUMB, 9.5,
           color=ACCENT)
    D.text(c, x + 76, y - 39, "the whole always comes first in a division",
           SANSO, 7.4, color=MUTED)


def _rem_div2510(c, x, y, w):
    D.text(c, x, y - 10, f"{V}2 is halving", SANSB, 8.4, color=ACCENT)
    D.text(c, x + 92, y - 10, f"{V}10 takes off a ten", SANSB, 8.4,
           color=ACCENT)
    D.text(c, x + 216, y - 10, f"{V}5 is {V}10 doubled", SANSB, 8.4,
           color=ACCENT)
    D.text(c, x, y - 26, f"18 {V} 2 = 9        60 {V} 10 = 6        "
                         f"60 {V} 5 = 12", NUMB, 10)
    D.text(c, x, y - 39, "Fewer parts means bigger parts.", SANSO, 7.4,
           color=MUTED)


def _rem_divone(c, x, y, w):
    D.text(c, x, y - 11, f"n {V} 1 = n", NUMB, 10.5, color=ACCENT)
    D.text(c, x + 78, y - 11, f"n {V} n = 1", NUMB, 10.5, color=ACCENT)
    D.text(c, x + 156, y - 11, f"0 {V} n = 0", NUMB, 10.5, color=ACCENT)
    D.text(c, x + 240, y - 11, f"n {V} 0  has no answer", NUMB, 9, color=WARM)
    D.text(c, x, y - 27, "No number of empty groups will ever hold "
                         "anything.", SANS, 8.2)
    D.text(c, x, y - 39, "Careful: 0 divided by 7 is 0, but 7 divided by 0 "
                         "is not a question with an answer.", SANSO, 7.4,
           color=MUTED)


def _rem_div346(c, x, y, w):
    D.text(c, x, y - 10, "Turn it into the multiplication you know.",
           SANSB, 8.6, color=ACCENT)
    D.seq(c, x, y - 26, [f"28 {V} 4", "how many 4s make 28?", "7"], NUMB, 9.5,
          INK, gap=6)
    D.text(c, x, y - 39, "Count the groups, not the numbers you say aloud.",
           SANSO, 7.4, color=MUTED)


def _rem_alldiv(c, x, y, w):
    D.text(c, x, y - 10, "There is no division table — only the times table, "
                         "read backwards.", SANS, 8.4)
    D.seq(c, x, y - 26, [f"54 {V} 6", "run along the 6 row to 54",
                         "it is under the 9"], NUMB, 9, ACCENT, gap=5)
    D.text(c, x, y - 39, "Not in the row? Then it does not divide exactly.",
           SANSO, 7.4, color=MUTED)


def _rem_remainder(c, x, y, w):
    D.text(c, x, y - 10, f"17 {V} 5  =  3 remainder 2", NUMB, 11,
           color=ACCENT)
    D.text(c, x + 170, y - 10, f"check:  3 {X} 5 + 2 = 17", NUM, 9,
           color=MUTED)
    D.text(c, x, y - 26, "The remainder is always smaller than the number "
                         "you divide by.", SANS, 8.4)
    D.text(c, x, y - 39, "If it is not, another whole group still fits.",
           SANSO, 7.4, color=MUTED)


def _rem_divtens(c, x, y, w):
    D.text(c, x, y - 10, f"84 {V} 4  =  (80 {V} 4) + (4 {V} 4)  =  20 + 1  "
                         f"=  21", NUMB, 10, color=ACCENT)
    D.text(c, x, y - 25, f"96 {V} 3  =  30 + 2  =  32", NUMB, 10,
           color=ACCENT)
    D.text(c, x, y - 38, "Split into pieces that each divide exactly, "
                         "then add the answers.", SANSO, 7.4, color=MUTED)


def _rem_muldiv(c, x, y, w):
    D.text(c, x, y - 10, "Work along the chain from left to right.",
           SANS, 8.4)
    D.seq(c, x, y - 26, [f"6 {X} 4 {V} 3", f"24 {V} 3", "8"], NUMB, 10,
          ACCENT, gap=7)
    D.text(c, x, y - 39, "Check any division by multiplying the answer back.",
           SANSO, 7.4, color=MUTED)


def _rem_choose(c, x, y, w):
    D.text(c, x, y - 10, "Two questions decide the operation:", SANSB, 8.6,
           color=ACCENT)
    D.text(c, x, y - 24, "Putting together or taking apart?    "
                         "Are the parts equal?", SANS, 8.4)
    D.text(c, x, y - 38, f"together+unequal  +      together+equal  {X}      "
                         f"apart+unequal  {M}      apart+equal  {V}",
           NUM, 8, color=MUTED)


# ── the ten division units ───────────────────────────────────────────────────

DIV_UNITS = [
    Unit(1, "Sharing and Grouping", "two questions",
         "Sharing asks how many each. Grouping asks how many groups.",
         pool_share_small(),
         [f_share, f_partbar],
         [(3.2, f_plain), (1.4, f_missing), (1.0, f_share), (0.8, f_partbar),
          (0.6, f_tf)],
         [(1, f_plain)],
         _rem_sharegroup, 42, unit_1, "4 min", "3 min", op="/"),

    Unit(2, "Division Undoes Multiplication", "one triangle, four facts",
         "Two parts and a whole. The whole always comes first in a division.",
         pool_div_families(),
         [f_family, f_partbar],
         [(2.8, f_plain), (2.0, f_missing), (1.2, f_family), (0.8, f_tf),
          (0.6, f_error)],
         [(1, f_plain)],
         _rem_divfamily, 42, unit_2, "4 min", "3 min", op="/"),

    Unit(3, "Halving, Fifths and Tenths", "the easy divisions",
         "÷2 is halving. ÷10 takes off a ten. ÷5 is ÷10 doubled.",
         pool_div_2_5_10(),
         [f_partbar, f_share],
         [(3.4, f_plain), (1.6, f_missing), (1.0, f_partbar), (0.8, f_compare),
          (0.6, f_tf)],
         [(1, f_plain)],
         _rem_div2510, 42, unit_3, "4 min", "3 min", op="/"),

    Unit(4, "Ones, Itself, and Zero", "the special cases",
         "n ÷ 1 = n. n ÷ n = 1. 0 ÷ n = 0. Nothing divides by zero.",
         pool_div_one_self(),
         [f_partbar, f_family],
         [(3.4, f_plain), (1.4, f_missing), (1.2, f_tf), (0.8, f_compare),
          (0.5, f_error)],
         [(1, f_plain)],
         _rem_divone, 42, unit_4, "3 min", "2 min", op="/"),

    Unit(5, "Threes, Fours and Sixes", "ask the multiplication",
         "How many 4s make 28? Turn the division into a times-table question.",
         pool_div_3_4_6(),
         [f_partbar, f_family],
         [(3.6, f_plain), (1.8, f_missing), (0.9, f_compare), (0.7, f_tf),
          (0.5, f_error)],
         [(1, f_plain)],
         _rem_div346, 42, unit_5, "4 min", "3 min", op="/"),

    Unit(6, "All Division Facts to a Hundred", "the table backwards",
         "There is no division table — only the times table, read the other "
         "way.",
         pool_all_div(),
         [f_family, f_partbar],
         [(3.4, f_plain), (1.8, f_missing), (1.2, f_balance), (1.0, f_compare),
          (0.8, f_tf), (0.5, f_error)],
         [(1, f_plain)],
         _rem_alldiv, 42, unit_6, "5 min", "4 min", op="/"),

    Unit(7, "Remainders", "what is left over",
         "The remainder is always smaller than the number you divide by.",
         pool_remainder_base(),
         [f_share, f_partbar],
         [(3.0, f_remainder), (2.0, f_plain), (1.2, f_missing), (0.6, f_tf)],
         [(1, f_remainder)],
         _rem_remainder, 42, unit_7, "5 min", "4 min", op="/"),

    Unit(8, "Dividing Bigger Numbers", "split into easy pieces",
         "Split the number into pieces that each divide exactly, then add.",
         pool_div_tens(),
         [f_partbar, f_family],
         [(3.2, f_plain), (1.8, f_missing), (1.0, f_compare), (0.8, f_tf),
          (0.5, f_error)],
         [(1, f_plain)],
         _rem_divtens, 42, unit_8, "6 min", "4 min", op="/"),

    Unit(9, "Multiplying and Dividing Together", "left to right",
         "Work along the chain in order. Check a division by multiplying back.",
         pool_muldiv(),
         [f_family, f_array],
         [(4, f_muldiv_chain), (1.4, f_plain), (1.0, f_missing),
          (0.8, f_balance)],
         [(1, f_muldiv_chain)],
         _rem_muldiv, 42, unit_9, "6 min", "5 min", op="*"),

    Unit(10, "Choosing the Operation", "all four",
         "Together or apart? Equal parts or not? Those two questions decide it.",
         pool_four_operations(),
         [C.r_family, C.r_family],
         MIXED_MIX,
         [(1, C.r_plain)],
         _rem_choose, 42, unit_10, "6 min", "5 min",
         mixed=True, word_factory=C.r_word),
]
