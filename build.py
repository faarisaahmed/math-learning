#!/usr/bin/env python3
"""
Build the worksheet books.

    python3 build.py                  # every book, plus answer keys
    python3 build.py --book 2          # one book
    python3 build.py --book 1 --pages 1-20     # a slice, for previewing
    python3 build.py --no-key

Output is landscape Letter with two worksheet pages per sheet; cut down the
middle to get 5.5" x 8.5" pages.
"""

import argparse
import io
import sys

from reportlab.lib.pagesizes import landscape, letter
from reportlab.pdfgen import canvas

import draw as D
from draw import (INK, ACCENT, WARM, MUTED, HAIR, FAINT, TINT,
                  SANS, SANSB, SANSO, NUM, NUMB)
import layout as L
from layout import PAGE_W, PAGE_H, MARGIN, CONTENT_W, draw_page
import curriculum as C
import front as F
from books import BOOKS, SERIES

SHEET_W, SHEET_H = landscape(letter)     # 792 x 612


def _score_line(c):
    """Cut guide down the centre of the sheet."""
    c.setStrokeColor(HAIR)
    c.setLineWidth(0.4)
    c.setDash([2.5, 3])
    c.line(SHEET_W / 2, 10, SHEET_W / 2, SHEET_H - 10)
    c.setDash([])
    for y in (SHEET_H - 9, 5):
        D.text(c, SHEET_W / 2, y, "c u t", SANS, 4.6, "center", HAIR)


def emit_sheets(c, renderers):
    """renderers: list of callables f(c, x0). Two per landscape sheet."""
    pad = (SHEET_W / 2 - PAGE_W) / 2
    for i in range(0, len(renderers), 2):
        _score_line(c)
        renderers[i](c, pad)
        if i + 1 < len(renderers):
            renderers[i + 1](c, SHEET_W / 2 + pad)
        c.showPage()


# ── answer key ────────────────────────────────────────────────────────────────

def prepass(book, specs):
    """Render once to a scratch canvas so each page can print "Score __ / N"."""
    scratch = canvas.Canvas(io.BytesIO(), pagesize=landscape(letter))
    for spec in specs:
        ctx = draw_page(scratch, spec, 0, total_pages=book.total_pages)
        spec.n_items = ctx["n"] or None
    return specs


def collect_answers(book, specs):
    """Replay each page on a scratch canvas to capture item order + answers."""
    scratch = canvas.Canvas(io.BytesIO(), pagesize=landscape(letter))
    out = []
    for spec in specs:
        ctx = draw_page(scratch, spec, 0, key=True,
                        total_pages=book.total_pages)
        out.append((spec, [it.answer() for it in ctx["items"]],
                    sum(v for it in ctx["items"] for v in it.values())))
    return out


def key_pages(book, answers, per_page=6):
    """Build renderer callables for the answer-key booklet."""
    chunks = [answers[i:i + per_page] for i in range(0, len(answers), per_page)]

    def make(chunk, idx, total):
        def render(c, x0):
            x, w = x0 + MARGIN, CONTENT_W
            y = PAGE_H - 34
            D.text(c, x, y, f"{book.label} — ANSWER KEY", SANSB, 8,
                   color=ACCENT)
            D.text(c, x + w, y, f"{idx + 1} / {total}", SANS, 7.5, "right", MUTED)
            y -= 6
            D.rule(c, x, y, x + w, 0.9, INK)
            y -= 20

            for spec, ans, total_sum in chunk:
                D.text(c, x, y, f"Page {spec.number}", SANSB, 10)
                D.text(c, x + 62, y, spec.title, SANSO, 7.6, color=MUTED)
                if ans and spec.self_check:
                    D.text(c, x + w, y, f"self-check total {total_sum}",
                           SANS, 7, "right", ACCENT)
                y -= 5
                D.rule(c, x, y, x + w, 0.4)
                y -= 12
                if not ans:
                    D.text(c, x, y, "teaching page — no answers", SANSO, 8,
                           color=MUTED)
                    y -= 18
                else:
                    parts = [f"{i + 1}. {a}" for i, a in enumerate(ans) if a]
                    line, cur = [], 0.0
                    colw = w
                    for p in parts:
                        pw = D.width_of(c, p, NUM, 8) + 11
                        if cur + pw > colw and line:
                            _emit(c, x, y, line)
                            y -= 11
                            line, cur = [], 0.0
                        line.append(p)
                        cur += pw
                    if line:
                        _emit(c, x, y, line)
                        y -= 11
                y -= 12
        return render

    def _emit(c, x, y, parts):
        xx = x
        for p in parts:
            num, _, val = p.partition(". ")
            D.text(c, xx, y, num + ".", SANS, 6.6, color=MUTED)
            off = D.width_of(c, num + ".", SANS, 6.6) + 2
            D.text(c, xx + off, y, val, NUMB, 8, color=INK)
            xx += off + D.width_of(c, val, NUMB, 8) + 9

    return [make(ch, i, len(chunks)) for i, ch in enumerate(chunks)]


# ── main ──────────────────────────────────────────────────────────────────────

def parse_range(s, total):
    if not s:
        return 1, total
    if "-" in s:
        a, b = s.split("-")
        return int(a), int(b)
    return int(s), int(s)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", default="all",
                    help="book number, or all (default: all)")
    ap.add_argument("--pages", default=None,
                    help="page range, e.g. 1-20 (default: whole book)")
    ap.add_argument("--out", default=None, help="override the output filename")
    ap.add_argument("--key-out", default=None)
    ap.add_argument("--no-front", action="store_true")
    ap.add_argument("--no-key", action="store_true")
    args = ap.parse_args()

    if args.book == "all":
        numbers = sorted(BOOKS)
    else:
        try:
            numbers = [int(args.book)]
        except ValueError:
            raise SystemExit(f"--book takes a number or 'all', "
                             f"not {args.book!r}")
    for n in numbers:
        if n not in BOOKS:
            raise SystemExit(f"no book {n}; have {sorted(BOOKS)}")
        build_book(BOOKS[n], args)


def build_book(book, args):
    lo, hi = parse_range(args.pages, book.total_pages)
    specs = prepass(book, [C.build_page(book, p) for p in range(lo, hi + 1)])

    renderers = []
    if not args.no_front:
        renderers += F.front_matter(book, SERIES)
    for spec in specs:
        renderers.append(lambda c, x0, s=spec:
                         draw_page(c, s, x0, total_pages=book.total_pages))

    out = args.out or f"{book.slug}.pdf"
    c = canvas.Canvas(out, pagesize=landscape(letter))
    c.setTitle(f"Book {book.ordinal} — {book.title}")
    if SERIES:
        c.setAuthor(SERIES)
    emit_sheets(c, renderers)
    c.save()
    print(f"Book {book.ordinal} worksheets → {out}  "
          f"({len(specs)} pages on {(len(renderers) + 1) // 2} sheets)")

    if not args.no_key:
        key_out = args.key_out or f"{book.slug}-answers.pdf"
        answers = collect_answers(book, specs)
        kc = canvas.Canvas(key_out, pagesize=landscape(letter))
        kc.setTitle(f"Book {book.ordinal} — Answer Key")
        emit_sheets(kc, key_pages(book, answers))
        kc.save()
        print(f"Book {book.ordinal} answer key  → {key_out}")


if __name__ == "__main__":
    main()
