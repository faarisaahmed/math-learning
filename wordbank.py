"""
Word problems.

Two things matter here. First, variety of *structure*: a child who only ever
meets "result unknown" stories learns that the answer is always the two numbers
combined, which is a reading trick rather than arithmetic. So change-unknown,
start-unknown and comparison stories are mixed in, and for each operation both
of its real-world meanings appear — take away *and* difference for subtraction,
sharing *and* grouping for division.

Second, the numbers have to read correctly: "1 shell", never "1 shells".
No pronouns are needed anywhere, so none are used.
"""

import items as I

NAMES = ["Maya", "Ravi", "Ana", "Ben", "Kofi", "Lin", "Omar", "Sara", "Theo",
         "Nia", "Yuki", "Elias", "Priya", "Marco", "Zoe", "Ida", "Hana", "Sam",
         "Leo", "Amara", "Dara", "Ines", "Noor", "Tomas"]

# (singular, plural) — so "1 shell" never reads as "1 shells"
THINGS = [("sticker", "stickers"), ("marble", "marbles"), ("shell", "shells"),
          ("block", "blocks"), ("crayon", "crayons"), ("bead", "beads"),
          ("apple", "apples"), ("coin", "coins"), ("card", "cards"),
          ("button", "buttons"), ("pencil", "pencils"), ("grape", "grapes"),
          ("acorn", "acorns"), ("stamp", "stamps"), ("tile", "tiles"),
          ("seed", "seeds"), ("bottle cap", "bottle caps"), ("leaf", "leaves")]

CONTAINERS = [("box", "boxes"), ("bag", "bags"), ("jar", "jars"),
              ("tray", "trays"), ("basket", "baskets"), ("shelf", "shelves"),
              ("packet", "packets"), ("crate", "crates")]

# "packed into boxes of 2" reads; "packed into shelves of 2" does not
PACKS = [("box", "boxes"), ("bag", "bags"), ("packet", "packets"),
         ("crate", "crates"), ("tray", "trays")]


def qty(n, thing):
    return f"{n} {thing[0] if n == 1 else thing[1]}"


# ── addition ──────────────────────────────────────────────────────────────────

_JOIN = [
    "{n} has {qa} and then finds {b} more. How many {o} does {n} have now?",
    "There are {qa} in a jar. {n} drops in {b} more. "
    "How many {o} are in the jar now?",
    "{n} counts {qa} on the table and {qb} on the shelf. "
    "How many {o} altogether?",
    "A basket holds {qa}. A second basket holds {qb}. "
    "How many {o} in the two baskets?",
    "{n} collects {qa} on Monday and {qb} on Tuesday. "
    "How many {o} over the two days?",
    "In the box, {qa} are red and {b} are blue. "
    "How many {o} are in the box in all?",
]

_CHANGE = [
    "{n} has {qa} and wants {t} in total. How many more {o} does {n} need?",
    "There are {qa} in the box. {n} wants the box to hold {t}. "
    "How many more {o} must go in?",
    "{n} has read {a} pages of a {t}-page book. How many pages are left?",
    "A shelf fits {t} {o}. It already holds {qa}. How many more {o} will fit?",
]

_TRIPLE = [
    "{n} picks {qa} on Monday, {b} on Tuesday and {c} on Wednesday. "
    "How many {o} in the three days?",
    "Three boxes hold {a}, {b} and {c} {o}. How many {o} altogether?",
    "{n} counts {qa} in the hall, {b} in the kitchen and {c} in the garden. "
    "How many {o} in the house and garden?",
]


# ── subtraction ───────────────────────────────────────────────────────────────

_TAKE_AWAY = [
    "{n} has {qa} and gives away {b}. How many {o} are left?",
    "There are {qa} in the jar. {n} takes out {b}. How many {o} are still "
    "in the jar?",
    "A packet holds {qa}. {b} of them are used up. How many {o} are left?",
    "{n} starts with {qa} and loses {b} of them. How many {o} remain?",
]

_DIFFERENCE = [
    "{n} has {qa}. {m} has {qb}. How many more {o} does {n} have?",
    "There are {qa} on the top shelf and {qb} on the bottom shelf. "
    "How many more {o} are on the top shelf?",
    "{n} needs {qa} but only has {qb}. How many more {o} are needed?",
    "A jar holds {qa}. Another jar holds {qb}. What is the difference?",
]

_START_UNKNOWN = [
    "{n} gives away {b} {o} and has {c} left. How many {o} did {n} start with?",
    "After {b} {o} were taken out of the box, {c} were left. "
    "How many {o} were in the box to begin with?",
]


# ── multiplication ────────────────────────────────────────────────────────────

_GROUPS = [
    "There are {a} {cp}. Each one holds {b} {o}. How many {o} altogether?",
    "{n} fills {a} {cp} with {b} {o} in each. How many {o} in total?",
    "A tray has {a} rows of {b} {o}. How many {o} are on the tray?",
    "One {cs} holds {b} {o}. How many {o} are in {a} {cp}?",
    "{n} walks {b} blocks a day for {a} days. How many blocks in all?",
]

_TIMES_AS_MANY = [
    "{n} has {qb}. {m} has {a} times as many. How many {o} does {m} have?",
    "A small jar holds {qb}. A big jar holds {a} times as much. "
    "How many {o} are in the big jar?",
    "{n} ran {b} laps. {m} ran {a} times as far. How many laps did {m} run?",
]


# ── division ──────────────────────────────────────────────────────────────────

_SHARE = [
    "{a} {o} are shared equally between {b} children. How many {o} each?",
    "{n} shares {a} {o} equally among {b} plates. How many {o} on each plate?",
    "{a} {o} are put into {b} equal rows. How many {o} in each row?",
]

_GROUP_INTO = [
    "{a} {o} are packed into {cp} of {b}. How many {cp} are needed?",
    "{n} puts {a} {o} into bags with {b} in each bag. How many bags?",
    "A ribbon {a} cm long is cut into pieces {b} cm long. How many pieces?",
]

_MISSING_FACTOR = [
    "{a} {o} fill {cp} with {b} {o} in each. How many {cp} are there?",
]


# ── builders ──────────────────────────────────────────────────────────────────

def _pick(rng):
    return rng.choice(NAMES), rng.choice(THINGS), rng.choice(CONTAINERS)


def _choose(rng, templates, avoid):
    """Pick a template, preferring one this page has not used yet.

    Four stories in a row built from the same sentence pattern read like a
    misprint, and they stop the child having to parse anything.
    """
    fresh = [t for t in templates if t not in avoid] if avoid is not None \
        else list(templates)
    t = rng.choice(fresh or list(templates))
    if avoid is not None:
        avoid.add(t)
    return t


def triple_story(rng, a, b, c, avoid=None):
    """Result unknown with three addends. Returns (story, unit noun)."""
    name, thing, _ = _pick(rng)
    tpl = _choose(rng, _TRIPLE, avoid)
    return (tpl.format(n=name, a=a, b=b, c=c, o=thing[1],
                       qa=qty(a, thing)), thing[1])


def _add(rng, a, b, avoid=None):
    name, thing, _ = _pick(rng)
    if rng.random() < 0.35:
        tpl = _choose(rng, _CHANGE, avoid)
        unit = "pages" if "pages" in tpl else thing[1]
        story = tpl.format(n=name, a=a, t=a + b, o=thing[1], qa=qty(a, thing))
        return I.Word(story, (a, b), unit=unit, ask=1)
    story = _choose(rng, _JOIN, avoid).format(
        n=name, a=a, b=b, o=thing[1], qa=qty(a, thing), qb=qty(b, thing))
    return I.Word(story, (a, b), unit=thing[1])


def _sub(rng, a, b, avoid=None):
    """`a - b`. a is the larger number in every one of these structures."""
    name, thing, _ = _pick(rng)
    other = rng.choice([x for x in NAMES if x != name])
    r = rng.random()
    if r < 0.35:
        story = _choose(rng, _DIFFERENCE, avoid).format(
            n=name, m=other, a=a, b=b, o=thing[1],
            qa=qty(a, thing), qb=qty(b, thing))
        return I.Word(story, (a, b), ("-",), unit=thing[1])
    if r < 0.5:
        story = _choose(rng, _START_UNKNOWN, avoid).format(
            n=name, b=b, c=a - b, o=thing[1])
        return I.Word(story, (a, b), ("-",), unit=thing[1], ask=0)
    story = _choose(rng, _TAKE_AWAY, avoid).format(
        n=name, a=a, b=b, o=thing[1], qa=qty(a, thing))
    return I.Word(story, (a, b), ("-",), unit=thing[1])


def _mul(rng, a, b, avoid=None):
    """`a x b` read as a groups of b."""
    name, thing, cont = _pick(rng)
    other = rng.choice([x for x in NAMES if x != name])
    if rng.random() < 0.25 and a >= 2:
        tpl = _choose(rng, _TIMES_AS_MANY, avoid)
        story = tpl.format(n=name, m=other, a=a, b=b, o=thing[1],
                           qb=qty(b, thing))
        return I.Word(story, (a, b), ("*",),
                      unit="laps" if "laps" in tpl else thing[1])
    tpl = _choose(rng, _GROUPS, avoid)
    unit = "blocks" if "blocks" in tpl else thing[1]
    story = tpl.format(n=name, a=a, b=b, o=thing[1],
                       cs=cont[0], cp=cont[1])
    return I.Word(story, (a, b), ("*",), unit=unit)


def _div(rng, a, b, avoid=None):
    """`a ÷ b`, exact. Sharing and grouping are both represented."""
    name, thing, _ = _pick(rng)
    pack = rng.choice(PACKS)
    r = rng.random()
    if r < 0.4:
        story = _choose(rng, _SHARE, avoid).format(n=name, a=a, b=b,
                                                   o=thing[1])
        return I.Word(story, (a, b), ("/",), unit=thing[1])
    if r < 0.75:
        tpl = _choose(rng, _GROUP_INTO, avoid)
        unit = "pieces" if "ribbon" in tpl else (
            "bags" if "bags" in tpl else pack[1])
        story = tpl.format(n=name, a=a, b=b, o=thing[1], cp=pack[1])
        return I.Word(story, (a, b), ("/",), unit=unit)
    story = _choose(rng, _MISSING_FACTOR, avoid).format(
        a=a, b=b, o=thing[1], cp=pack[1])
    return I.Word(story, (a, b), ("/",), unit=pack[1])


_BUILDERS = {"+": _add, "-": _sub, "*": _mul, "/": _div}


def build(rng, pool, op="+", avoid=None):
    """Pick a fact from `pool` and dress it as a story for the given operation.

    `avoid` is a mutable set of already-used templates, so the four stories on
    one page come out structurally different from each other.
    """
    if op == "-":
        cands = [p for p in pool if p[0] > p[1] >= 1] or pool
    elif op == "/":
        cands = [p for p in pool if p[1] >= 2 and p[0] // p[1] >= 2] or pool
    elif op == "*":
        cands = [p for p in pool if p[0] >= 2 and p[1] >= 2] or pool
    else:
        cands = [p for p in pool if p[0] >= 1 and p[1] >= 1] or pool
    a, b = rng.choice(cands)
    return _BUILDERS[op](rng, a, b, avoid)
