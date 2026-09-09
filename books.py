"""
The book registry: what each book covers and in what order to work them.

Books are numbered rather than lettered. A letter code hides what is inside
and turns progress into a grade; a number plus a plain title says where you
are in the sequence and what you are actually learning.
"""

import draw as D
from curriculum import Book, PAGES_PER_UNIT
import content_add as ADD
import content_sub as SUB
import content_mul as MUL
import content_div as DIV


def _motif_number_line(c, x, y, w):
    """Book One: a hop along the line — putting together, taking apart."""
    D.number_line(c, x + 40, y, w - 80, 0, 10, jumps=[(6, 3, "+3")], mark=[6])


def _motif_array(c, x, y, w):
    """Book Two: an array with the first two columns picked out, which is both
    the picture of multiplication and the cut that Unit 8 teaches."""
    cell = 15.0
    aw, _ = D.array_size(6, 4, cell)
    ax = x + (w - aw) / 2
    D.array(c, ax, y + 4, 6, 4, cell, highlight_cols=2,
            second_color=D.ACCENT)
    D.vrule(c, ax + 2 * cell, y + 4 - 4 * cell, y + 4, 0.9, D.HAIR)


def _renumber(units, offset):
    for k, u in enumerate(units):
        u.n = offset + k + 1
    return units


# The series name goes here and nowhere else: it feeds the PDF metadata, the
# cover footer and the README. Leave it empty and none of those appear.
SERIES = ""


BOOK_ONE = Book(
    n=1,
    title="Putting Together and Taking Apart",
    cover_lines=("Putting Together", "and Taking Apart"),
    slug="book-one-putting-together",
    subtitle="Four hundred worksheets that take a child from counting on "
             "their fingers to adding and subtracting two-digit numbers in "
             "their head.",
    units=_renumber(ADD.ADD_UNITS, 0) + _renumber(SUB.SUB_UNITS, 10),
    blurbs={
        1: "Addition as counting forward on a number line.",
        2: "a + b = b + a, so always count on from the bigger number.",
        3: "Splitting numbers into parts. The six pairs that make ten.",
        4: "Doubles as memory landmarks; near doubles from them.",
        5: "Every fact to ten, and choosing the fastest method for each.",
        6: "Teen numbers read as one ten plus some ones.",
        7: "Crossing ten by filling the ten first — taught explicitly.",
        8: "All facts to twenty, plus missing addends and true equations.",
        9: "Three addends; reordering to find a ten.",
        10: "Two-digit addition, with and without regrouping.",
        11: "Subtraction as counting backward; taking away.",
        12: "Fact families: three numbers, four facts, nothing extra to learn.",
        13: "The pairs that make ten, read backwards.",
        14: "The second meaning of subtraction: difference, found by "
            "counting up.",
        15: "Every difference within ten, and choosing a method.",
        16: "Teen minus ones, where the ten is never touched.",
        17: "Crossing back over ten by breaking the ten open.",
        18: "All facts to twenty; the missing number in any position.",
        19: "Adding and subtracting together, and checking by adding back.",
        20: "Two-digit subtraction, with and without regrouping.",
    },
    halves=("Part one — addition", "Part two — subtraction"),
    diagnosis=[
        ("Answers come out one too small, or one too big.",
         "The number they start on is being counted as a hop. Unit 1."),
        ("Still counting on fingers for four or five hops.",
         "The ten-pairs are not automatic yet. Units 3 and 7."),
        ("Stalls on facts that cross ten, like 8 + 5.",
         "Make-ten has not taken hold. Unit 7."),
        ("Writes 10 + 6 = 106.",
         "A teen is one ten and some ones, not two digits placed side by "
         "side. Unit 6."),
        ("Answers 7 + □ = 15 with 22.",
         "The equals sign is being read as “write the answer here”. Unit 8."),
        ("Counts back nine hops to do 12 – 9.",
         "Only one meaning of subtraction is available. Unit 14."),
        ("Gets 15 – 8 wrong but 7 + 8 right.",
         "Subtraction is being stored as a separate table. Unit 12."),
        ("Takes the smaller digit from the larger whatever the order "
         "(54 – 8 giving 46 via 8 – 4).",
         "No ten is being broken open. Units 17 and 20."),
        ("Forgets the ten that was borrowed in column subtraction.",
         "The regrouping is not being written down. Unit 20."),
        ("Adds whenever a word problem says “more”.",
         "The story is being read for key words rather than structure. "
         "Units 14–15."),
    ],
    after_title="After Book One",
    after_body="Book Two: multiplication as equal groups and arrays, then "
               "division as its inverse. A child who leaves this book knowing "
               "the ten-pairs, the make-ten move and the fact families by "
               "heart has the whole of Book Two's foundation already.",
    problems_estimate="about 10,300",
    motif=_motif_number_line,
)


BOOK_TWO = Book(
    n=2,
    title="Groups and Sharing",
    cover_lines=("Groups", "and Sharing"),
    slug="book-two-groups-and-sharing",
    subtitle="Four hundred worksheets that build the times tables out of "
             "equal groups and arrays, then read them backwards to get "
             "division for free.",
    units=_renumber(MUL.MUL_UNITS, 0) + _renumber(DIV.DIV_UNITS, 10),
    blurbs={
        1: "Multiplication as equal groups, and as repeated addition.",
        2: "Arrays: why a × b and b × a are one fact, not two.",
        3: "The 2s, 5s and 10s — doubling, tens, and half of tens.",
        4: "Multiplying by one and by zero, and why they differ.",
        5: "The 3s and 4s, built by doubling.",
        6: "The middle of the table; ×9 as ×10 less a group; squares.",
        7: "The whole table as one object, and what it really contains.",
        8: "Breaking a product apart — the distributive law, seen.",
        9: "Multiplying by tens, and two-digit by one-digit.",
        10: "Factors and multiples: what a number is made of.",
        11: "The two meanings of division: sharing and grouping.",
        12: "Fact families: division as multiplication read backwards.",
        13: "Halving, and dividing by 5 and 10.",
        14: "Dividing by one and by itself — and why not by zero.",
        15: "The 3s, 4s and 6s, by asking the multiplication question.",
        16: "Every division fact to a hundred, from the table you know.",
        17: "Remainders, and why one is always smaller than the divisor.",
        18: "Dividing bigger numbers by splitting them into easy pieces.",
        19: "Multiplying and dividing together; checking by the inverse.",
        20: "Choosing the operation: all four, and how to tell them apart.",
    },
    halves=("Part one — multiplication", "Part two — division"),
    diagnosis=[
        ("Recites the table fluently but cannot do 17 × 6.",
         "The facts are memorised without the structure under them. Unit 8."),
        ("Answers 0 × 7 with 7.",
         "Multiplying by zero is being confused with adding zero. Unit 4."),
        ("Writes 23 × 4 = 812.",
         "The two partial products are being placed side by side instead of "
         "added. Unit 9."),
        ("Counts up in ones to reach a fact.",
         "No landmark is being used — squares, tens, or the turnaround. "
         "Units 6 and 7."),
        ("Learns 7 × 4 and 4 × 7 as two separate facts.",
         "The array has not been connected to the symbols. Unit 2."),
        ("Knows 6 × 7 = 42 but cannot answer 42 ÷ 6.",
         "Division is being treated as a new table. Unit 12."),
        ("Answers “how many groups” when the question asked “how many each”.",
         "Only one meaning of division is available. Unit 11."),
        ("Gives a remainder as large as, or larger than, the divisor.",
         "Another whole group still fits. Unit 17."),
        ("Says 7 ÷ 0 is 0, or 7.",
         "It has been learned as a rule rather than seen as unanswerable. "
         "Unit 14."),
        ("Chooses the operation by hunting for a word in the question.",
         "The structure of the story is not being read. Unit 20."),
    ],
    after_title="After Book Two",
    after_body="Fractions, which are division written a different way, and "
               "long multiplication, which is Unit 8's cut made twice. A "
               "child who leaves this book able to break a product apart and "
               "check a division by multiplying back has the machinery for "
               "both.",
    problems_estimate="about 10,300",
    motif=_motif_array,
)


BOOKS = {1: BOOK_ONE, 2: BOOK_TWO}
