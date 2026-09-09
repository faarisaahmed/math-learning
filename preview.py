#!/usr/bin/env python3
"""
Render selected worksheet pages to PNG, for checking layout without printing.

    python3 preview.py 1 221 222      # book 1, pages 221 and 222
    python3 preview.py 2 121          # book 2, page 121
"""
import sys

from reportlab.lib.pagesizes import landscape, letter
from reportlab.pdfgen import canvas

import build as B
import curriculum as C
from layout import draw_page
from books import BOOKS


def main(argv):
    n = 1
    if argv and argv[0].isdigit() and int(argv[0]) in BOOKS:
        n, argv = int(argv[0]), argv[1:]
    book = BOOKS[n]
    pages = [int(a) for a in argv] or [1, 2]
    specs = B.prepass(book, [C.build_page(book, p) for p in pages])
    rs = [(lambda c, x0, s=s: draw_page(c, s, x0,
                                        total_pages=book.total_pages))
          for s in specs]
    tmp = "preview.pdf"
    c = canvas.Canvas(tmp, pagesize=landscape(letter))
    B.emit_sheets(c, rs)
    c.save()
    try:
        import pymupdf
    except ImportError:
        print(f"wrote {tmp} (install pymupdf for PNGs)")
        return
    doc = pymupdf.open(tmp)
    for i in range(doc.page_count):
        out = f"preview-{i + 1:02d}.png"
        doc[i].get_pixmap(dpi=130).save(out)
        print("wrote", out)


main(sys.argv[1:])
