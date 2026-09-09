# Arithmetic worksheet books

Generated arithmetic worksheet books, printed two pages to a landscape Letter
sheet and cut down the middle into 5.5" × 8.5" pages.

The PDFs are not in the repo — they are built from source, and the latest set
is attached to the [current release](../../releases/latest).

## Building the PDFs

```
git clone https://github.com/faarisaahmed/math-learning.git
cd math-learning
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python3 build.py
```

`python3 build.py` writes all four files into the current directory:

```
book-one-putting-together.pdf            Book One worksheets    (400 pages)
book-one-putting-together-answers.pdf    Book One answer key
book-two-groups-and-sharing.pdf          Book Two worksheets    (400 pages)
book-two-groups-and-sharing-answers.pdf  Book Two answer key
```

Other things you can run:

```
python3 build.py --book 2            # one book
python3 build.py --book 1 --pages 1-20     # a slice, for previewing
python3 build.py --book 1 --no-key         # worksheets only
python3 build.py --book 1 --no-front       # skip the front matter
python3 build.py --book 1 --out my.pdf --key-out my-answers.pdf
python3 validate.py                  # layout + content checks, every page
python3 preview.py 2 1 121 400       # render specific pages to PNG
```

`preview.py` needs one extra package to emit PNGs rather than a PDF:
`pip install -r requirements-dev.txt`.

Everything is deterministic, so a fresh build reproduces the release PDFs
byte-for-byte in content — you do not need the release to get the books.

`original/` holds the first draft this grew out of.

**Series name:** set `SERIES` in `books.py`. It feeds the PDF metadata, the
cover footer and nothing else; leave it empty and none of those appear.

## The books

| | Units | Worksheets | Problems |
|---|---|---|---|
| **Book One** — Putting Together and Taking Apart | 20 | 400 | ~10,300 |
| **Book Two** — Groups and Sharing | 20 | 400 | ~10,300 |

Books are numbered, not lettered, and titled by the idea rather than the
operation. A letter code hides what is inside a book and turns progress into a
grade; a number plus a plain title says where you are in the sequence and what
you are actually learning.

**Book One** runs from counting on to two-digit subtraction with regrouping.
Units 1–10 are addition: counting on, commutativity, number bonds and the
pairs that make ten, doubles and near doubles, teen numbers as 10 + n, the
make-ten bridge, three addends, and two-digit addition. Units 11–20 are
subtraction, introduced *as the addition facts read backwards*: counting back,
fact families, the ten-pairs inverted, difference by counting up, breaking the
ten to cross back, missing numbers in any position, and two-digit subtraction.

**Book Two** runs from equal groups to choosing between all four operations.
Units 1–10 are multiplication: equal groups, arrays and the turnaround, the
2s/5s/10s, one and zero, the 3s and 4s by doubling, the middle of the table,
the whole table as one object, breaking a product apart (the distributive law),
two-digit × one-digit, and factors. Units 11–20 are division: sharing versus
grouping, fact families, halving and ÷5 and ÷10, dividing by one and by itself
and why not by zero, the tables read backwards, remainders, dividing bigger
numbers, mixed chains with inverse checking, and a capstone on choosing the
operation.

## Design decisions

**Each operation is taught with its inverse, from a shared structure.**
Subtraction is not a second table: 7, 8 and 15 are one fact family, and a child
who knows 7 + 8 already knows 15 − 8. Division is the times table read the
other way. This is the whole reason the books are paired the way they are.

**Every unit runs an instructional arc, not twenty identical pages.**
Page 1 teaches. Pages 2–3 are guided, with a visual model on several problems.
Pages 4–13 are practice with the scaffolds fading out. Pages 14–15 are word
problems, 16–17 interleave everything learned so far, 18–19 are speed pages,
and page 20 is a mastery check. A support that never goes away becomes a
crutch; one that is never there leaves the child guessing.

**Strategies are named and taught, never left to be induced.** Counting on,
the ten-pairs, near doubles, make-ten, break-ten, difference-by-counting-up,
the turnaround, ×9 as ×10 less a group, the distributive cut, and division as a
missing factor each get a teaching page with a worked example, a visual model
(number line, ten-frame, number bond, fact triangle, array, area model, part
bar, times grid) and — the part usually missing — the specific mistake that
method invites.

**Practice is interleaved and spaced.** From the second unit onward every
practice page opens with a retrieval strip drawn from earlier units, and the
review pages mix operations deliberately. Blocked practice looks better during
the session and retains worse; this trades some immediate smoothness for
durable recall.

**Formats vary so the page cannot be pattern-matched.** Horizontal facts in all
four operations, a blank in any slot, true/false, comparisons, spot-the-error,
number bonds, fact-family triangles, ten-frames with counters struck out,
number-line hops forwards and back, make-ten and break-ten decompositions,
balance equations, chains mixing operations, arrays, equal groups, area-model
splits, skip-count tracks, sharing rings, part bars, remainders, factor lists,
column form, and word problems — including change-unknown and start-unknown
stories, and both meanings of subtraction and of division.

**Each page closes its own feedback loop.** The self-check prints the sum of
every number the child will write. If their total does not match, an answer is
wrong and finding it is their job. Same-day feedback, no instructor, and the
answers are not given away.

**Errors are diagnosed, not just marked.** Each book's front matter has an
"If they get stuck" page mapping a specific observed mistake — *answers come
out one too small*, *writes 23 × 4 = 812*, *knows 6 × 7 but not 42 ÷ 6* — to
the idea that is missing and the unit to work again.

## Files

| | |
|---|---|
| `draw.py` | Primitives and the visual models: ten-frame, number line, number bond, fact triangle, bar model, array, equal groups, area model, part bar, skip track, times grid, column form |
| `items.py` | Problem types. Each knows how to draw itself, its answer, and the numbers a child writes |
| `layout.py` | Page furniture and the block layout engine (`Grid`, `Panel`, `Strip`, `Anchor`, …) |
| `teach.py` | Shared teaching-page furniture: the idea, the picture, a worked example, the mistake it invites |
| `curriculum.py` | Book-agnostic engine: `Unit`, `Book`, the problem factories, and the page builder |
| `content_add.py` `content_sub.py` `content_mul.py` `content_div.py` | The four halves: fact pools, diagrams, teaching pages and unit definitions |
| `books.py` | Assembles Book One and Book Two, and holds `SERIES` |
| `wordbank.py` | Word-problem templates for all four operations, with number agreement |
| `front.py` | Cover, how-to-use, unit map, progress record, diagnostic page |
| `build.py` | CLI; emits the worksheets and the answer keys |
| `preview.py` | Renders chosen pages to PNG for checking layout without printing |
| `validate.py` | Checks nothing overflows, no page repeats a problem, checks are 20 problems, answers are in range, and the key matches the worksheets |
| `requirements.txt` | The one runtime dependency, `reportlab`. `requirements-dev.txt` adds `pymupdf` for `preview.py` |

## Notes for extending it

Pages are generated deterministically from the book number and page number, so
the same build always produces the same worksheets and the answer key always
matches.

Grids are fit-driven: they are handed more problems than will fit and trim to
the space available, and tall scaffolds are budgeted by the area they occupy
rather than by count. So changing a font size or a panel does not silently push
content off the page. Run `validate.py` after any layout change.

To add a book, write a content module exposing a list of `Unit`s and register a
`Book` in `books.py`. A unit with `mixed=True` takes `(a, b, op)` triples
instead of pairs, which is how Book Two's capstone mixes all four operations.

Standard PDF fonts do not carry `→`, `−` or `□`, and some viewers substitute
the *wrong* glyph rather than none, so arrows are drawn with `draw.seq()` and
those characters are kept out of the text. `+ – × ÷` are all safe.
