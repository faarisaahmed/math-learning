"""Cover, how-to-use guide, unit map, progress record and diagnostics."""

import draw as D
from draw import (INK, ACCENT, WARM, MUTED, HAIR, FAINT, TINT,
                  SANS, SANSB, SANSO, NUM, NUMB)
from layout import PAGE_W, PAGE_H, MARGIN, CONTENT_W
from curriculum import PAGES_PER_UNIT


def _frame(x0):
    return x0 + MARGIN, CONTENT_W


def cover(book, series=""):
    def render(c, x0):
        x, w = _frame(x0)
        cx = x + w / 2

        c.setFillColor(ACCENT)
        c.rect(x0, PAGE_H - 6, PAGE_W, 6, stroke=0, fill=1)

        y = PAGE_H - 132
        D.text(c, cx, y, "  ".join(book.label), SANSB, 11.5, "center", ACCENT)
        y -= 42
        for line in book.cover_lines:
            D.text(c, cx, y, line, SANSB, 27, "center", INK)
            y -= 32
        y += 6
        D.rule(c, cx - 40, y, cx + 40, 1.0, INK)
        y -= 26
        D.paragraph(c, x + 20, y, book.subtitle, w - 40, SANS, 9.5, 13.5,
                    MUTED, align="center")

        y -= 92
        if book.motif:
            book.motif(c, x, y, w)
        else:
            D.number_line(c, x + 40, y, w - 80, 0, 10, jumps=[(6, 3, "+3")],
                          mark=[6])

        y -= 122
        D.rule(c, x, y, x + w, 0.5)
        y -= 20
        for label, val in [("Units", str(len(book.units))),
                           ("Worksheets", str(book.total_pages)),
                           ("Problems", book.problems_estimate)]:
            D.text(c, x, y, label, SANSB, 8, color=MUTED)
            D.text(c, x + w, y, val, NUM, 9, "right", INK)
            y -= 15
        D.rule(c, x, y + 5, x + w, 0.5)

        if series:
            D.text(c, cx, 62, f"{series.lower()}  ·  "
                              f"book {book.ordinal.lower()}",
                   SANSO, 7.4, "center", MUTED)
        D.text(c, cx, 46, "Print landscape, single-sided. Cut each sheet down "
                          "the middle.", SANSO, 7.6, "center", MUTED)
    return render


def how_to_use(book):
    def render(c, x0):
        x, w = _frame(x0)
        y = PAGE_H - 58

        D.text(c, x, y, "How to use this book", SANSB, 17)
        y -= 8
        D.rule(c, x, y, x + w, 0.9, INK)
        y -= 18

        y = D.paragraph(c, x, y, "One page a day is enough. Ten minutes of "
                                 "daily practice beats an hour once a week, "
                                 "and a child who is still fresh at the end of "
                                 "a page will come back to the next one "
                                 "willingly.",
                        w, SANS, 8.8, 11.5, INK) - 13

        sections = [
            ("Do the pages in order",
             "Each unit assumes the one before it. The second half of this "
             "book is built directly on the first — it teaches the inverse "
             "operation out of facts already learned, not as a new table."),
            ("Time the page, but do not rush the child",
             "The target time is printed on each page. It is a signal of "
             "fluency, not a deadline. A child who is accurate but slow needs "
             "more repetitions, not more pressure."),
            ("Use the self-check",
             "Every practice page tells you what all the answers add up to. "
             "The child adds their own answers and compares. This closes the "
             "feedback loop the same day instead of a week later, and it "
             "makes finding an error the child's job, not yours."),
            ("Do not correct mid-page",
             "Let the page finish. Interrupting turns practice into "
             "dictation."),
            ("Ask “why” on the teaching pages",
             "Those pages are meant to be read aloud together. If a child can "
             "say why the method works, the method survives; if they can only "
             "copy the steps, it will not."),
            ("Repeat a page when the check says so",
             "The mastery check on page 20 of each unit tells you exactly "
             "what to do with each score. Repeating is normal and expected."),
            ("Fingers are fine at the start",
             "They are a real strategy, just a slow one. The strategy pages "
             "exist to make fingers unnecessary, not forbidden. They fall "
             "away on their own once the faster method is quicker."),
        ]
        for title, body in sections:
            D.text(c, x, y, title, SANSB, 9.2, color=ACCENT)
            y -= 11.5
            y = D.paragraph(c, x, y, body, w, SANS, 8.3, 10.5, INK) - 10

        y -= 2
        D.rule(c, x, y, x + w, 0.5)
        y -= 15
        D.text(c, x, y, "What a page looks like", SANSB, 9.2, color=ACCENT)
        y -= 11.5
        D.paragraph(c, x, y, "Page 1 of each unit teaches. Pages 2–3 give the "
                             "same problems with pictures. Pages 4–13 fade the "
                             "pictures out. Pages 14–15 are word problems, "
                             "16–17 mix in everything learned so far, 18–19 "
                             "are speed pages, and page 20 is the mastery "
                             "check.",
                    w, SANS, 8.3, 10.5, INK)
    return render


def unit_map(book, half):
    """Half is 0 or 1: twenty units do not fit legibly on one page."""
    def render(c, x0):
        x, w = _frame(x0)
        y = PAGE_H - 56

        n = len(book.units)
        lo, hi = (0, n // 2) if half == 0 else (n // 2, n)
        units = book.units[lo:hi]

        D.text(c, x, y, book.halves[half], SANSB, 17)
        D.text(c, x + w, y, f"units {lo + 1}–{hi}", SANS, 8, "right", MUTED)
        y -= 8
        D.rule(c, x, y, x + w, 0.9, INK)
        y -= 20

        for u in units:
            start = (u.n - 1) * PAGES_PER_UNIT + 1
            D.text(c, x, y, str(u.n), NUMB, 12, color=ACCENT)
            D.text(c, x + 22, y, u.title, SANSB, 9.2)
            D.text(c, x + w, y, f"{start}–{u.n * PAGES_PER_UNIT}", NUM, 7.6,
                   "right", MUTED)
            y -= 11
            y = D.paragraph(c, x + 22, y + 2, book.blurbs[u.n], w - 22,
                            SANS, 8.2, 10.2, MUTED) - 11
            D.rule(c, x + 22, y + 4, x + w, 0.3)
            y -= 2

        if half == 1:
            y -= 10
            D.text(c, x, y, book.after_title, SANSB, 9.4, color=ACCENT)
            y -= 12
            D.paragraph(c, x, y, book.after_body, w, SANS, 8.4, 10.8, INK)
    return render


def diagnosis(book):
    """A parent-facing table: what a specific mistake means, and where to go.

    A drill programme leans on an instructor to read a child's errors. Since
    there is no instructor here, the reading has to be written down.
    """
    def render(c, x0):
        x, w = _frame(x0)
        y = PAGE_H - 56

        D.text(c, x, y, "If they get stuck", SANSB, 17)
        y -= 8
        D.rule(c, x, y, x + w, 0.9, INK)
        y -= 14
        y = D.paragraph(c, x, y, "Errors are rarely random. Most of them are a "
                                 "specific missing idea, and the idea has a "
                                 "page number. Match what you are seeing to "
                                 "the left column, then go back to the unit on "
                                 "the right and work it again.",
                        w, SANS, 8.6, 11, INK) - 16

        D.text(c, x, y, "WHAT YOU SEE", SANSB, 6.8, color=MUTED)
        D.text(c, x + w * 0.56, y, "WHAT IT MEANS, AND WHERE TO GO", SANSB,
               6.8, color=MUTED)
        y -= 5
        D.rule(c, x, y, x + w, 0.5)
        y -= 12

        for symptom, action in book.diagnosis:
            lw = w * 0.53
            b1 = D.paragraph(c, x, y + 8, symptom, lw, SANS, 8.2, 10.2, INK)
            b2 = D.paragraph(c, x + w * 0.56, y + 8, action, w * 0.44,
                             SANS, 8.2, 10.2, ACCENT)
            y = min(b1, b2) - 8
            D.rule(c, x, y + 4, x + w, 0.3)
            y -= 3

        y -= 10
        D.rule(c, x, y + 6, x + w, 0.5)
        D.text(c, x, y - 5, "One more thing", SANSB, 9.4, color=ACCENT)
        y -= 18
        D.paragraph(c, x, y, "Ask a child to explain how they got an answer, "
                             "even a correct one. A child who says “I counted "
                             "on from eight” or “I took it off the ten” is "
                             "secure. A child who says “I just did it” or goes "
                             "quiet may have a method that works on this page "
                             "and will not survive the next book.",
                    w, SANS, 8.4, 10.8, INK)
    return render


def progress_record(book):
    def render(c, x0):
        x, w = _frame(x0)
        y = PAGE_H - 56

        D.text(c, x, y, "Progress record", SANSB, 17)
        y -= 8
        D.rule(c, x, y, x + w, 0.9, INK)
        y -= 12
        y = D.paragraph(c, x, y, "Shade a square each time a page is finished "
                                 "correctly.", w, SANS, 8.2, 10.5, MUTED) - 10

        n_units = len(book.units)
        cell = min(14.0, w / 20.0)
        gx = x + (w - cell * 20) / 2
        for r in range(n_units):
            D.text(c, gx - 4, y - cell * 0.68, f"U{r + 1}", SANS, 5.6, "right",
                   MUTED)
            for cnum in range(20):
                px = gx + cnum * cell
                py = y - cell
                page = r * 20 + cnum + 1
                special = cnum in (0, 19)
                c.setStrokeColor(HAIR)
                c.setLineWidth(0.4)
                c.setFillColor(TINT if special else D.colors.white)
                c.rect(px, py, cell - 1.5, cell - 1.5, stroke=1, fill=1)
                D.text(c, px + (cell - 1.5) / 2, py + cell * 0.30, str(page),
                       SANS, 4.2, "center", MUTED)
            y -= cell + 0.8

        y -= 8
        D.text(c, gx, y, "shaded squares = teaching page and mastery check",
               SANSO, 6.6, color=MUTED)
        y -= 16

        D.rule(c, x, y + 6, x + w, 0.5)
        D.text(c, x, y - 5, "Mastery checks", SANSB, 9.2, color=ACCENT)
        y -= 18

        colw = w / 2
        rows = (n_units + 1) // 2
        for col in range(2):
            cx = x + col * colw
            D.text(c, cx, y, "UNIT", SANSB, 6.2, color=MUTED)
            D.text(c, cx + 26, y, "PAGE", SANSB, 6.2, color=MUTED)
            D.text(c, cx + 56, y, "DATE", SANSB, 6.2, color=MUTED)
            D.text(c, cx + 118, y, "SCORE", SANSB, 6.2, color=MUTED)
        yy = y - 4
        D.rule(c, x, yy, x + w, 0.5)
        yy -= 12
        for r in range(rows):
            for col in range(2):
                n = col * rows + r + 1
                if n > n_units:
                    continue
                cx = x + col * colw
                D.text(c, cx, yy, str(n), NUM, 7.6)
                D.text(c, cx + 26, yy, str(n * 20), NUM, 7.6, color=MUTED)
                D.rule(c, cx + 54, yy - 2, cx + 112, 0.4)
                D.rule(c, cx + 116, yy - 2, cx + 142, 0.4)
                D.text(c, cx + 145, yy, "/ 20", SANS, 7, color=MUTED)
            yy -= 13
    return render


def front_matter(book, series=""):
    return [cover(book, series), how_to_use(book),
            unit_map(book, 0), unit_map(book, 1),
            progress_record(book), diagnosis(book)]
