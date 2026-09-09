"""
Low-level drawing primitives and the visual models the curriculum teaches with.

Coordinate convention
---------------------
ReportLab's origin is bottom-left and `y` grows upward. Every *block* helper in
this module takes ``y`` as the TOP edge of the block it draws and returns the
y-coordinate of the bottom edge, so callers can stack blocks by writing::

    y = ten_frame(c, x, y, ...)
    y = number_line(c, x, y, ...)

Inline helpers (``text``, ``rule``) take a baseline, as ReportLab does.
"""

from reportlab.lib import colors

# ── design tokens ─────────────────────────────────────────────────────────────

INK    = colors.Color(0.09, 0.09, 0.11)   # body text / problem digits
ACCENT = colors.Color(0.11, 0.32, 0.55)   # teaching cues, strategy highlights
WARM   = colors.Color(0.72, 0.34, 0.10)   # "watch out" / the tricky step
MUTED  = colors.Color(0.45, 0.46, 0.50)   # captions, numbering
HAIR   = colors.Color(0.72, 0.73, 0.76)   # rules, blanks, frames
FAINT  = colors.Color(0.94, 0.95, 0.965)  # panel fills
TINT   = colors.Color(0.90, 0.93, 0.965)  # accent panel fills

SANS   = "Helvetica"
SANSB  = "Helvetica-Bold"
SANSO  = "Helvetica-Oblique"
NUM    = "Helvetica"        # digits: sans is more legible for early learners
NUMB   = "Helvetica-Bold"


# ── text & lines ──────────────────────────────────────────────────────────────

def text(c, x, y, s, font=SANS, size=9, align="left", color=INK):
    """Draw a single line of text at baseline `y`. Returns the advance width."""
    c.setFillColor(color)
    c.setFont(font, size)
    if align == "center":
        c.drawCentredString(x, y, s)
    elif align == "right":
        c.drawRightString(x, y, s)
    else:
        c.drawString(x, y, s)
    return c.stringWidth(s, font, size)


def width_of(c, s, font=SANS, size=9):
    return c.stringWidth(s, font, size)


def rule(c, x1, y, x2, w=0.5, color=HAIR, dash=None):
    c.setStrokeColor(color)
    c.setLineWidth(w)
    c.setDash(dash or [])
    c.line(x1, y, x2, y)
    c.setDash([])


def vrule(c, x, y1, y2, w=0.5, color=HAIR, dash=None):
    c.setStrokeColor(color)
    c.setLineWidth(w)
    c.setDash(dash or [])
    c.line(x, y1, x, y2)
    c.setDash([])


def panel(c, x, y, w, h, fill=FAINT, stroke=None, radius=3, lw=0.6):
    """Rounded panel. `y` is the TOP edge. Returns bottom edge."""
    c.setFillColor(fill) if fill else None
    if stroke:
        c.setStrokeColor(stroke)
        c.setLineWidth(lw)
    c.roundRect(x, y - h, w, h, radius,
                stroke=1 if stroke else 0, fill=1 if fill else 0)
    return y - h


def blank(c, x, y, w=26, color=HAIR, lw=0.8):
    """The answer line students write on. `y` is the writing baseline."""
    rule(c, x, y - 2.5, x + w, lw, color)
    return x + w


def boxed_blank(c, x, y, w=20, h=15, color=HAIR, lw=0.7, fill=None):
    """An empty box to write a single number in. `y` is the text baseline."""
    if fill:
        c.setFillColor(fill)
    c.setStrokeColor(color)
    c.setLineWidth(lw)
    c.rect(x, y - 3.5, w, h, stroke=1, fill=1 if fill else 0)
    return x + w


# ── glyphs ────────────────────────────────────────────────────────────────────

def plus_sign(c, cx, cy, r=4.5, w=1.0, color=INK):
    c.setStrokeColor(color)
    c.setLineWidth(w)
    c.line(cx - r, cy, cx + r, cy)
    c.line(cx, cy - r, cx, cy + r)


def arrow(c, x0, y0, x1, y1, head=3.4, w=0.9, color=INK):
    import math
    c.setStrokeColor(color)
    c.setLineWidth(w)
    c.line(x0, y0, x1, y1)
    a = math.atan2(y1 - y0, x1 - x0)
    for s in (+1, -1):
        b = a + s * 2.5
        c.line(x1, y1, x1 + head * math.cos(b), y1 + head * math.sin(b))


def arrow_glyph(c, x, y, size=9, color=INK):
    """A right arrow sitting on the text baseline. Returns its width.

    The base-14 fonts do not carry U+2192, and a viewer that substitutes for
    it can print the wrong glyph entirely, so arrows are drawn, not typed.
    """
    w = size * 0.95
    cy = y + size * 0.28
    c.setStrokeColor(color)
    c.setLineWidth(max(0.55, size * 0.072))
    c.line(x, cy, x + w, cy)
    c.line(x + w, cy, x + w - size * 0.26, cy + size * 0.18)
    c.line(x + w, cy, x + w - size * 0.26, cy - size * 0.18)
    return w


def seq(c, x, y, parts, font=SANS, size=9, color=INK, gap=5, arrow_color=None):
    """Draw text fragments joined by drawn arrows. Returns the end x."""
    for i, part in enumerate(parts):
        if i:
            x += gap
            x += arrow_glyph(c, x, y, size, arrow_color or MUTED)
            x += gap
        x += text(c, x, y, part, font, size, color=color)
    return x


def dot(c, x, y, r=3.0, color=INK):
    c.setFillColor(color)
    c.circle(x, y, r, stroke=0, fill=1)


def dot_row(c, cx, cy, n, r=3.2, gap=11, color=INK):
    """A horizontal row of n dots centred on cx."""
    sx = cx - (n - 1) * gap / 2.0
    for i in range(n):
        dot(c, sx + i * gap, cy, r, color)


def dot_cluster(c, cx, cy, n, r=3.0, gap=10, per_row=5, color=INK):
    """n dots arranged in rows of `per_row`, centred on (cx, cy)."""
    rows = [min(per_row, n - i * per_row) for i in range((n + per_row - 1) // per_row)]
    total_h = (len(rows) - 1) * gap
    y = cy + total_h / 2.0
    for cnt in rows:
        dot_row(c, cx, y, cnt, r, gap, color)
        y -= gap
    return len(rows) * gap


# ── visual model: ten-frame ───────────────────────────────────────────────────

def ten_frame(c, x, y, filled, cell=13.5, color=INK, frame=HAIR,
              fill_color=None, second_color=None, split_at=None,
              cross_from=None):
    """
    A 5x2 ten-frame. `y` is the TOP edge; returns the bottom edge.

    filled      -- how many counters to draw (0..10)
    split_at    -- if given, counters at index >= split_at use `second_color`,
                   which is how we show decomposition (e.g. 9 dark + 1 blue).
    cross_from  -- if given, counters at index >= cross_from are struck out,
                   which is how taking away is shown.
    """
    w, h = cell * 5, cell * 2
    c.setStrokeColor(frame)
    c.setLineWidth(0.7)
    c.rect(x, y - h, w, h, stroke=1, fill=0)
    c.setLineWidth(0.4)
    for i in range(1, 5):
        c.line(x + i * cell, y - h, x + i * cell, y)
    c.line(x, y - cell, x + w, y - cell)

    r = cell * 0.30
    for i in range(min(filled, 10)):
        row, col = divmod(i, 5)
        cx = x + col * cell + cell / 2.0
        cy = y - row * cell - cell / 2.0
        struck = cross_from is not None and i >= cross_from
        col_ = (second_color if (split_at is not None and i >= split_at
                                 and second_color)
                else (fill_color or color))
        dot(c, cx, cy, r, HAIR if struck else col_)
        if struck:
            c.setStrokeColor(WARM)
            c.setLineWidth(1.0)
            d = cell * 0.30
            c.line(cx - d, cy - d, cx + d, cy + d)
            c.line(cx - d, cy + d, cx + d, cy - d)
    return y - h


def ten_frame_width(cell=13.5):
    return cell * 5


# ── visual model: number line ─────────────────────────────────────────────────

def number_line(c, x, y, w, lo, hi, jumps=(), label_every=1, tick_size=3.5,
                label_size=6.5, color=INK, hide_labels=False, mark=()):
    """
    Number line from `lo` to `hi` spanning width `w`. `y` is the TOP edge of the
    whole block (jump arcs live above the axis). Returns the bottom edge.

    jumps -- iterable of (start, length, label) drawn as hop arcs above the axis.
    mark  -- iterable of values to emphasise with a filled dot on the axis.
    """
    n = hi - lo
    step = w / float(n)
    hop_h = 13 if jumps else 0
    axis_y = y - hop_h - 4

    c.setStrokeColor(color)
    c.setLineWidth(0.8)
    c.line(x, axis_y, x + w, axis_y)
    for i in range(n + 1):
        nx = x + i * step
        big = (i % label_every == 0)
        c.setLineWidth(0.8 if big else 0.5)
        c.line(nx, axis_y - (tick_size if big else tick_size * 0.6), nx, axis_y)
        if big and not hide_labels:
            text(c, nx, axis_y - tick_size - label_size - 1.5, str(lo + i),
                 NUM, label_size, "center", MUTED)

    for v in mark:
        dot(c, x + (v - lo) * step, axis_y, 2.4, ACCENT)

    for start, length, lab in jumps:
        # one small hop per unit, so a child can literally count the jumps;
        # a negative length hops backwards, which is how taking away reads
        back = length < 0
        col = WARM if back else ACCENT
        for k in range(abs(length)):
            hx0 = x + (start - lo + (-k if back else k)) * step
            hx1 = hx0 + (-step if back else step)
            _hop(c, hx0, hx1, axis_y, 9, col)
        if lab:
            mid = x + (start - lo + length / 2.0) * step
            text(c, mid, axis_y + 12.5, lab, NUMB, 7, "center", col)

    bottom = axis_y - tick_size - (0 if hide_labels else label_size + 3)
    return bottom


def _hop(c, x0, x1, y, h, color):
    c.setStrokeColor(color)
    c.setLineWidth(0.8)
    p = c.beginPath()
    p.moveTo(x0, y + 1)
    p.curveTo(x0 + (x1 - x0) * 0.2, y + h, x1 - (x1 - x0) * 0.2, y + h, x1, y + 1)
    c.drawPath(p, stroke=1, fill=0)
    d = 2.2 if x1 > x0 else -2.2
    arrow(c, x1 - d, y + 3.4, x1, y + 1, 2.6, 0.7, color)


# ── visual model: number bond ─────────────────────────────────────────────────

def number_bond(c, cx, y, whole, parts, r=11, drop=30, spread=27,
                size=10, color=INK, blank_slots=()):
    """
    Part-part-whole bond. `y` is the TOP edge; returns bottom edge.
    Values may be None (or listed in blank_slots by name) to render an empty
    circle for the student to fill.

    blank_slots -- subset of {"whole", "p0", "p1"} rendered as empty circles.
    """
    wy = y - r
    c.setLineWidth(0.8)

    def circle(ccx, ccy, val, is_blank):
        c.setStrokeColor(ACCENT if is_blank else HAIR)
        c.setFillColor(colors.white)
        c.circle(ccx, ccy, r, stroke=1, fill=1)
        if not is_blank and val is not None:
            text(c, ccx, ccy - size * 0.35, str(val), NUM, size, "center", color)

    px_l, px_r = cx - spread, cx + spread
    py = wy - drop
    c.setStrokeColor(HAIR)
    c.setLineWidth(0.8)
    c.line(cx - r * 0.55, wy - r * 0.8, px_l + r * 0.4, py + r * 0.85)
    c.line(cx + r * 0.55, wy - r * 0.8, px_r - r * 0.4, py + r * 0.85)

    circle(cx, wy, whole, "whole" in blank_slots)
    circle(px_l, py, parts[0], "p0" in blank_slots)
    circle(px_r, py, parts[1], "p1" in blank_slots)
    return py - r


def number_bond_width(r=11, spread=27):
    return 2 * (spread + r)


# ── visual model: bar model ───────────────────────────────────────────────────

def bar_model(c, x, y, w, a, b, h=17, size=9, labels=None, total_label=None):
    """
    Part-part-whole bar. `y` is TOP edge; returns bottom edge.
    `a`/`b` size the two segments proportionally; labels may be strings or None.
    """
    total = float(a + b) or 1.0
    wa = w * (a / total)
    c.setStrokeColor(HAIR)
    c.setLineWidth(0.7)
    c.setFillColor(TINT)
    c.rect(x, y - h, wa, h, stroke=1, fill=1)
    c.setFillColor(colors.white)
    c.rect(x + wa, y - h, w - wa, h, stroke=1, fill=1)

    la, lb = (labels or (str(a), str(b)))
    for lab, sx, sw in ((la, x, wa), (lb, x + wa, w - wa)):
        if not lab:
            continue
        need = c.stringWidth(str(lab), NUM, size) + 4
        if sw >= need:
            text(c, sx + sw / 2, y - h / 2 - size * 0.35, str(lab), NUM, size,
                 "center")
        else:
            # too narrow to hold the number: label it above with a tick
            text(c, sx + sw / 2, y + 3, str(lab), NUM, size - 0.5, "center",
                 ACCENT)
            vrule(c, sx + sw / 2, y, y + 2, 0.5, ACCENT)

    # total brace underneath
    by = y - h - 6
    c.setStrokeColor(MUTED)
    c.setLineWidth(0.6)
    c.line(x, by, x + w, by)
    c.line(x, by, x, by + 3)
    c.line(x + w, by, x + w, by + 3)
    if total_label:
        text(c, x + w / 2, by - 9, total_label, NUM, size, "center", MUTED)
        return by - 12
    return by - 2


# ── column (vertical) addition ────────────────────────────────────────────────

DIGIT_W = 8.0

# WinAnsi carries all four of these, so they are safe to typeset directly
OP_SYM = {"+": "+", "-": "\u2013", "*": "\u00d7", "/": "\u00f7"}

def column_op(c, right_x, y, a, b, op="+", size=12, answer=None,
              carry_hint=False, slot_w=DIGIT_W, color=INK):
    """
    Vertical arithmetic aligned on `right_x`. `y` is the baseline of the top
    row. Returns the baseline of the answer row.

    `carry_hint` draws a dotted box over the tens column: for addition that is
    where the regrouped ten is written, for subtraction it is where the ten
    that was broken open is recorded.
    """
    def digits(n, slots):
        s = str(n).rjust(slots)
        return s

    result = {"+": a + b, "-": a - b, "*": a * b}[op]
    slots = max(len(str(a)), len(str(b)), len(str(result)))
    gap = size + 3

    for i, ch in enumerate(digits(a, slots)):
        if ch != " ":
            text(c, right_x - (slots - 1 - i) * slot_w - slot_w / 2, y, ch,
                 NUM, size, "center", color)
    y2 = y - gap
    for i, ch in enumerate(digits(b, slots)):
        if ch != " ":
            text(c, right_x - (slots - 1 - i) * slot_w - slot_w / 2, y2, ch,
                 NUM, size, "center", color)
    text(c, right_x - slots * slot_w - 7, y2, OP_SYM[op], NUM, size, "left",
         color)

    ly = y2 - 5
    rule(c, right_x - slots * slot_w - 9, ly, right_x, 0.9, INK)

    y3 = ly - gap + 3
    if answer is not None:
        for i, ch in enumerate(str(answer).rjust(slots)):
            if ch != " ":
                text(c, right_x - (slots - 1 - i) * slot_w - slot_w / 2, y3, ch,
                     NUM, size, "center", color)
    if carry_hint:
        # a box over the tens column, where the regrouped ten is written
        c.setStrokeColor(HAIR)
        c.setDash([1, 1.6])
        c.setLineWidth(0.5)
        bw = min(slot_w, 9)
        bx = right_x - 2 * slot_w + (slot_w - bw) / 2
        c.rect(bx, y + size * 0.74, bw, 9.0, stroke=1, fill=0)
        c.setDash([])
    return y3


def column_sum(c, right_x, y, a, b, size=12, answer=None, carry_hint=False,
               slot_w=DIGIT_W, color=INK):
    """Backwards-compatible alias for addition in vertical form."""
    return column_op(c, right_x, y, a, b, "+", size, answer, carry_hint,
                     slot_w, color)


def column_width(a, b, op="+", slot_w=DIGIT_W):
    result = {"+": a + b, "-": a - b, "*": a * b}[op]
    slots = max(len(str(a)), len(str(b)), len(str(result)))
    return slots * slot_w + 9


# ── misc ──────────────────────────────────────────────────────────────────────

def wrap(c, s, font, size, max_w):
    """Greedy word wrap -> list of lines."""
    words, lines, cur = s.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if c.stringWidth(trial, font, size) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def paragraph(c, x, y, s, w, font=SANS, size=8.5, leading=11, color=INK,
              align="left"):
    """Wrapped text block. `y` is the TOP edge; returns bottom edge."""
    lines = wrap(c, s, font, size, w)
    yy = y - size
    for ln in lines:
        if align == "center":
            text(c, x + w / 2, yy, ln, font, size, "center", color)
        else:
            text(c, x, yy, ln, font, size, "left", color)
        yy -= leading
    return yy + leading - size - 2


# ── visual model: array ───────────────────────────────────────────────────────

def array(c, x, y, cols, rows, cell=10.0, color=INK, r=None,
          highlight_cols=None, second_color=None):
    """
    A rows x cols array of dots. `y` is the TOP edge; returns the bottom edge.

    An array is the honest picture of multiplication: it makes commutativity
    obvious (turn it a quarter turn) and it is the same picture the area model
    and, later, long multiplication are built on.

    highlight_cols -- draw the first n columns in `second_color`, used to show
                      a product being broken apart (7 x 6 as 5 x 6 plus 2 x 6).
    """
    r = r or cell * 0.28
    for i in range(rows):
        for j in range(cols):
            col = (second_color if (highlight_cols is not None
                                    and j < highlight_cols and second_color)
                   else color)
            dot(c, x + j * cell + cell / 2, y - i * cell - cell / 2, r, col)
    return y - rows * cell


def array_size(cols, rows, cell=10.0):
    return cols * cell, rows * cell


# ── visual model: equal groups ────────────────────────────────────────────────

def groups(c, x, y, n, per, ring=17.0, gap=6.0, color=INK, per_row=4,
           empty=False):
    """
    `n` rings of `per` dots each. `y` is the TOP edge; returns the bottom edge.
    Equal groups is the first meaning of multiplication a child meets, and the
    one word problems almost always use.
    """
    rows = (n + per_row - 1) // per_row
    yy = y
    for row in range(rows):
        count = min(per_row, n - row * per_row)
        for k in range(count):
            cx = x + k * (ring * 2 + gap) + ring
            cy = yy - ring
            c.setStrokeColor(ACCENT if empty else HAIR)
            c.setLineWidth(0.7)
            if empty:
                c.setDash([1.6, 1.6])
            c.circle(cx, cy, ring, stroke=1, fill=0)
            c.setDash([])
            if not empty:
                dot_cluster(c, cx, cy, per, r=min(2.6, ring * 0.16),
                            gap=min(8, ring * 0.52),
                            per_row=3 if per > 4 else 2, color=color)
        yy -= ring * 2 + gap
    return yy + gap


def groups_size(n, per, ring=17.0, gap=6.0, per_row=4):
    cols = min(n, per_row)
    rows = (n + per_row - 1) // per_row
    return cols * (ring * 2 + gap) - gap, rows * (ring * 2 + gap) - gap


# ── visual model: area model / partial products ──────────────────────────────

def area_model(c, x, y, w, h, a, b, split, size=8.5):
    """
    A rectangle a wide and b tall, cut vertically at `split`, labelled with the
    two partial products. `y` is the TOP edge; returns the bottom edge.

    This is the distributive law made visible, and it is the single idea that
    makes multi-digit multiplication something to understand rather than a
    ritual to copy.
    """
    wa = w * (split / float(a))
    c.setStrokeColor(HAIR)
    c.setLineWidth(0.7)
    c.setFillColor(TINT)
    c.rect(x, y - h, wa, h, stroke=1, fill=1)
    c.setFillColor(colors.white)
    c.rect(x + wa, y - h, w - wa, h, stroke=1, fill=1)

    text(c, x + wa / 2, y - h / 2 - size * 0.35, f"{split} × {b}",
         NUMB, size, "center", ACCENT)
    text(c, x + wa + (w - wa) / 2, y - h / 2 - size * 0.35,
         f"{a - split} × {b}", NUMB, size, "center", INK)

    # edge labels
    text(c, x + wa / 2, y + 2.5, str(split), NUM, size - 0.5, "center", MUTED)
    text(c, x + wa + (w - wa) / 2, y + 2.5, str(a - split), NUM, size - 0.5,
         "center", MUTED)
    text(c, x - 5, y - h / 2 - size * 0.35, str(b), NUM, size - 0.5, "right",
         MUTED)
    return y - h - 4


# ── visual model: bar split into equal parts (division) ──────────────────────

def part_bar(c, x, y, w, parts, h=17, label=None, part_label=None, size=9,
             unknown=False):
    """
    A bar cut into `parts` equal pieces. `y` is the TOP edge; returns bottom.
    Sharing and grouping both land on this picture, which is why it is the one
    used to tie division to multiplication.
    """
    seg = w / float(parts)
    c.setStrokeColor(HAIR)
    c.setLineWidth(0.7)
    c.setFillColor(colors.white)
    c.rect(x, y - h, w, h, stroke=1, fill=1)
    for i in range(1, parts):
        vrule(c, x + i * seg, y - h, y, 0.5)
    for i in range(parts):
        lab = "?" if unknown else (part_label if part_label is not None else "")
        if lab != "":
            text(c, x + i * seg + seg / 2, y - h / 2 - size * 0.35, str(lab),
                 NUM, size, "center", ACCENT if unknown else INK)

    by = y + 5
    c.setStrokeColor(MUTED)
    c.setLineWidth(0.6)
    c.line(x, by, x + w, by)
    c.line(x, by, x, by - 3)
    c.line(x + w, by, x + w, by - 3)
    if label is not None:
        text(c, x + w / 2, by + 3, str(label), NUM, size, "center", MUTED)
    return y - h - 3


# ── visual model: fact-family triangle ───────────────────────────────────────

def fact_triangle(c, cx, y, whole, parts, op="+", size=10, h=52, half_w=34,
                  hide=None):
    """
    The three numbers of a fact family at the corners of a triangle: the whole
    at the apex, the two parts below. `y` is the TOP edge; returns bottom.

    One triangle carries four facts. Seeing them as one object rather than four
    things to memorise is what makes subtraction fall out of addition.
    """
    ax, ay = cx, y - 9
    lx, ly = cx - half_w, y - h
    rx, ry = cx + half_w, y - h

    c.setStrokeColor(HAIR)
    c.setLineWidth(0.8)
    # the edges run corner to corner and are masked by the number discs, so
    # the numbers sit on the triangle rather than beside it
    p = c.beginPath()
    p.moveTo(ax, ay)
    p.lineTo(lx, ly)
    p.lineTo(rx, ry)
    p.close()
    c.drawPath(p, stroke=1, fill=0)

    sym = OP_SYM[op]
    text(c, cx, (ay + ly) / 2 - 4, sym, NUM, size - 1.5, "center", MUTED)

    for name, (px, py), val in (("whole", (ax, ay), whole),
                                ("p0", (lx, ly), parts[0]),
                                ("p1", (rx, ry), parts[1])):
        blankslot = (hide == name)
        c.setFillColor(colors.white)
        c.setStrokeColor(colors.white)
        c.circle(px, py, 11, stroke=1, fill=1)
        if blankslot:
            c.setStrokeColor(ACCENT)
            c.setLineWidth(0.8)
            c.circle(px, py, 10, stroke=1, fill=0)
        if not blankslot:
            text(c, px, py - size * 0.35, str(val), NUMB, size, "center", INK)
    return ly - 12


# ── visual model: skip-count track ───────────────────────────────────────────

def skip_track(c, x, y, values, blanks=(), size=9, box_w=22, gap=6):
    """
    A run of skip-counted numbers with some left blank. `y` is the TOP edge;
    returns the bottom edge. Skip counting is the bridge from repeated addition
    to a recalled multiplication fact.
    """
    xx = x
    for i, v in enumerate(values):
        if i in blanks:
            c.setStrokeColor(ACCENT)
            c.setLineWidth(0.7)
            c.rect(xx, y - size - 6, box_w, size + 6, stroke=1, fill=0)
        else:
            text(c, xx + box_w / 2, y - size - 1, str(v), NUM, size, "center")
        xx += box_w + gap
    return y - size - 8


def skip_track_width(n, box_w=22, gap=6):
    return n * (box_w + gap) - gap


# ── visual model: the times table as one object ──────────────────────────────

def times_grid(c, x, y, n=10, cell=15.0, size=5.6, shade_upper=True,
               mark_diagonal=True, highlight=()):
    """
    An n x n multiplication grid. `y` is the TOP edge; returns the bottom edge.

    Shading the half above the diagonal shows what commutativity is actually
    worth: the table looks like a hundred facts and is really about fifty-five,
    with the squares along the diagonal as landmarks between them.
    """
    hx, hy = x + cell, y - cell
    colors_ = colors

    c.setFont(SANSB, size + 0.4)
    for j in range(1, n + 1):
        text(c, hx + (j - 1) * cell + cell / 2, y - cell * 0.66, str(j),
             SANSB, size + 0.4, "center", ACCENT)
        text(c, x + cell * 0.5, hy - (j - 1) * cell - cell * 0.66, str(j),
             SANSB, size + 0.4, "center", ACCENT)

    for i in range(1, n + 1):
        for j in range(1, n + 1):
            cx = hx + (j - 1) * cell
            cy = hy - i * cell
            upper = j > i
            if (i, j) in highlight or (j, i) in highlight:
                c.setFillColor(TINT)
            elif mark_diagonal and i == j:
                c.setFillColor(colors_.Color(0.88, 0.91, 0.95))
            elif shade_upper and upper:
                c.setFillColor(colors_.Color(0.965, 0.97, 0.978))
            else:
                c.setFillColor(colors_.white)
            c.setStrokeColor(HAIR)
            c.setLineWidth(0.3)
            c.rect(cx, cy, cell, cell, stroke=1, fill=1)
            col = MUTED if (shade_upper and upper) else INK
            text(c, cx + cell / 2, cy + cell * 0.34, str(i * j),
                 NUMB if i == j else NUM, size, "center", col)
    return hy - n * cell


def times_grid_size(n=10, cell=15.0):
    return cell * (n + 1), cell * (n + 1)
