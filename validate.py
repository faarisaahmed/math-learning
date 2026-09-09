#!/usr/bin/env python3
"""
Render every page of every book to a scratch canvas and check the material
holds together: nothing overflows its page, no page repeats a problem, every
mastery check has exactly twenty problems, no answer is out of range, and the
answer key agrees with the worksheets.
"""
import io
import sys
from collections import Counter, defaultdict

from reportlab.lib.pagesizes import landscape, letter
from reportlab.pdfgen import canvas

from layout import draw_page
import curriculum as C
from books import BOOKS


def check(book, c):
    bad, dupes, thin, wrong, oor = [], [], [], [], []
    per_kind = defaultdict(list)
    total = 0
    for p in range(1, book.total_pages + 1):
        spec = C.build_page(book, p)
        ctx = draw_page(c, spec, 0, total_pages=book.total_pages)
        per_kind[spec.kind].append(ctx["n"])
        total += ctx["n"]
        if ctx["overflow"] > 0.5:
            bad.append((p, spec.kind, round(ctx["overflow"], 1), ctx["n"]))

        sigs = [(type(i).__name__, str(i)) for i in ctx["items"]]
        if any(v > 1 for v in Counter(sigs).values()):
            dupes.append((p, spec.kind))
        if spec.kind == "check" and ctx["n"] != 20:
            wrong.append((p, ctx["n"]))
        slack = ctx["y_end"] - ctx["floor"]
        if (spec.kind in ("practice", "fluency", "review")
                and ctx["n"] < 15 and slack > 25):
            thin.append((p, spec.kind, ctx["n"], round(slack)))
        if spec.kind == "teach" and ctx["n"] < 3:
            thin.append((p, "teach", ctx["n"], round(slack)))

        limit = 100 if book.n == 1 else 250
        for it in ctx["items"]:
            if it.answer() in (None, ""):
                oor.append((p, repr(it), "no answer"))
            for v in it.values():
                if not 0 <= v <= limit:
                    oor.append((p, repr(it)[:60], v))

    mismatch = 0
    for p in range(1, book.total_pages + 1):
        a = draw_page(c, C.build_page(book, p), 0, key=False,
                      total_pages=book.total_pages)
        b = draw_page(c, C.build_page(book, p), 0, key=True,
                      total_pages=book.total_pages)
        if [str(i) for i in a["items"]] != [str(i) for i in b["items"]]:
            mismatch += 1

    print(f"\n{book.label} — {book.title}  "
          f"({book.total_pages} pages, {total} problems)")
    for k in ("teach", "guided", "practice", "applied", "review",
              "fluency", "check"):
        v = per_kind[k]
        if v:
            print(f"  {k:9s} {len(v):3d} pages   problems min {min(v):3d} "
                  f"max {max(v):3d} mean {sum(v) / len(v):5.1f}")
    problems = [("overflowing pages", bad), ("duplicate problems", dupes),
                ("mastery checks not at 20", wrong), ("under-filled", thin),
                ("out-of-range answers", oor),
                ("key/worksheet mismatches", [1] * mismatch)]
    ok = True
    for label, rows in problems:
        if rows:
            ok = False
            print(f"  !! {label}: {len(rows)}  {rows[:5]}")
    if ok:
        print("  all checks pass")
    return ok


def main():
    c = canvas.Canvas(io.BytesIO(), pagesize=landscape(letter))
    good = all([check(BOOKS[n], c) for n in sorted(BOOKS)])
    return 0 if good else 1


sys.exit(main())
