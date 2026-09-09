"""
Shared furniture for teaching pages.

Every teaching page in every book has the same four parts: the idea stated in
words, a picture of it, one example worked all the way through, and the mistake
that method invites. The last of these is the part a drill book leaves out, and
it is usually the reason a child's answers go wrong in a predictable direction.
"""

import draw as D
from draw import (INK, ACCENT, WARM, MUTED, HAIR, FAINT, TINT,
                  SANS, SANSB, SANSO, NUM, NUMB)
from layout import Heading, Text, Bullets, Panel, Grid


def idea(body):
    return Panel([Text(body, size=8.9, leading=11, pad_below=0)],
                 title="The idea", fill=TINT, pad=6.5, pad_below=8)


def watch(body):
    return Panel([Text(body, size=8.2, leading=10.2, pad_below=0)],
                 title="Watch out", fill=D.colors.Color(0.99, 0.955, 0.91),
                 pad=6.5, pad_below=8)


def worked(lines):
    return Panel([Bullets(lines, size=8.3, leading=10.2, pad_below=0,
                          bullet="arrow")],
                 title="Worked example", fill=FAINT, pad=6.5, pad_below=8)


def why(body):
    """An optional fifth panel: why the method works, not just that it does."""
    return Panel([Text(body, size=8.2, leading=10.2, pad_below=0)],
                 title="Why it works", fill=FAINT, pad=6.5, pad_below=8)


def try_these(items, cols=2):
    return [Heading("Now you try", 9.5, ACCENT, pad_below=5),
            Grid(items, cols=cols, fit=True, row_pad=1)]
