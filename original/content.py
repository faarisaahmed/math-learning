from reportlab.lib import colors

TOPIC = "Addition"   # shown as the title on every half-page

MATH  = "Times-Roman"
MATHB = "Times-Bold"
BODY  = "Helvetica"
BODYB = "Helvetica-Bold"

TOTAL_PAGES = 10   # 10 "pages" = 5 landscape sheets (left=teach, right=practice)


# ── helpers ───────────────────────────────────────────────────────────────────

def text(c, x, y, s, font=BODY, size=10, align="left"):
    c.setFont(font, size)
    if align == "center":
        c.drawCentredString(x, y, s)
    elif align == "right":
        c.drawRightString(x, y, s)
    else:
        c.drawString(x, y, s)

def rule(c, x1, y, x2, width=0.35):
    c.setLineWidth(width)
    c.line(x1, y, x2, y)

def dot_row(c, cx, y, n, r=3.5, gap=12):
    sx = cx - (n * gap) / 2 + gap / 2
    for i in range(n):
        c.circle(sx + i * gap, y, r, fill=1, stroke=0)


# ── LEFT — teaching ───────────────────────────────────────────────────────────

def draw_left(c, x_offset, col_w, margin, content_top, content_bottom):
    cx = x_offset + col_w / 2
    lx = x_offset + margin
    rx = x_offset + col_w - margin
    y  = content_top - 4

    # ── What is addition ─────────────────────────────────────────────────────
    text(c, cx, y, "What is Addition?", font=BODYB, size=12, align="center")
    y -= 13
    text(c, cx, y, "Combining two groups to find the total.",
         font=BODY, size=9, align="center")
    y -= 26

    # Dot groups: 3 + 4 = 7
    c.setFillColor(colors.black)
    dot_row(c, cx - 54, y, 3)
    # plus
    hw = 5
    c.setLineWidth(1.0)
    c.line(cx - hw, y, cx + hw, y)
    c.line(cx, y - hw, cx, y + hw)
    dot_row(c, cx + 54, y, 4)
    y -= 20

    text(c, cx - 54, y, "3",  font=MATH,  size=14, align="center")
    text(c, cx,      y, "+",  font=MATH,  size=14, align="center")
    text(c, cx + 54, y, "4",  font=MATH,  size=14, align="center")

    # equals bar + answer
    rule(c, cx - 16, y - 4, cx + 16, 0.7)
    y -= 18
    text(c, cx, y, "7", font=MATHB, size=18, align="center")
    y -= 28

    rule(c, lx, y, rx)
    y -= 20

    # ── Number line ──────────────────────────────────────────────────────────
    text(c, cx, y, "Number Line", font=BODYB, size=11, align="center")
    y -= 18

    nl_x0 = lx + 8
    nl_x1 = rx - 8
    nl_y  = y
    span  = nl_x1 - nl_x0
    step  = span / 10

    c.setLineWidth(0.7)
    c.line(nl_x0, nl_y, nl_x1, nl_y)
    for i in range(11):
        nx = nl_x0 + i * step
        c.line(nx, nl_y - 3, nx, nl_y + 3)
        text(c, nx, nl_y - 14, str(i), font=MATH, size=8, align="center")

    # jump arrow: 3 + 4
    a, b = 3, 4
    ax0  = nl_x0 + a * step
    ax1  = nl_x0 + (a + b) * step
    ah   = 18

    c.setLineWidth(0.8)
    c.line(ax0, nl_y + 3, ax0, nl_y + ah)
    c.line(ax0, nl_y + ah, ax1, nl_y + ah)
    c.line(ax1, nl_y + ah, ax1, nl_y + 3)
    c.line(ax1, nl_y + 3, ax1 - 3, nl_y + 9)
    c.line(ax1, nl_y + 3, ax1 + 3, nl_y + 9)
    text(c, (ax0 + ax1) / 2, nl_y + ah + 3, f"+{b}", font=MATH, size=8, align="center")

    y = nl_y - 22
    text(c, cx, y, f"Start at {a},  jump {b}  →  land on {a+b}",
         font=BODY, size=8, align="center")

    y -= 22
    rule(c, lx, y, rx)
    y -= 20

    # ── Key idea ─────────────────────────────────────────────────────────────
    text(c, cx, y, "Key Ideas", font=BODYB, size=11, align="center")
    y -= 16

    ideas = [
        ("Order doesn't matter:",   "3 + 4  =  4 + 3"),
        ("Adding zero:",             "5 + 0  =  5"),
        ("Doubles:",                 "4 + 4  =  8"),
    ]
    for label, example in ideas:
        text(c, lx, y, label, font=BODYB, size=9)
        text(c, rx,  y, example, font=MATH, size=11, align="right")
        y -= 18


# ── RIGHT — practice ──────────────────────────────────────────────────────────

# Small number problems only (sums ≤ 10)
PROBLEMS = [
    (1, 2), (2, 3), (3, 1), (4, 0), (2, 2),
    (1, 4), (3, 3), (0, 5), (4, 1), (2, 4),
    (5, 0), (1, 5), (3, 2), (4, 2), (0, 4),
    (2, 5), (3, 4), (1, 6), (4, 3), (5, 2),
]

NOTES = {
    4:  "Adding 0 keeps the number the same.",
    7:  "Doubles — both numbers are equal.",
    8:  "Adding 0 again — same rule applies.",
    17: "Try counting up from the bigger number.",
}

def draw_right(c, x_offset, col_w, margin, content_top, content_bottom):
    lx = x_offset + margin
    rx = x_offset + col_w - margin
    cx = x_offset + col_w / 2
    y  = content_top - 4

    text(c, cx, y, "Practice", font=BODYB, size=12, align="center")
    y -= 18

    notes_height = 14 + len(NOTES) * 13
    usable = y - content_bottom - notes_height - 10
    half   = len(PROBLEMS) // 2
    row_h  = min(usable / half, 21)

    col2_x = cx + 4

    for col_i in range(2):
        probs  = PROBLEMS[:half] if col_i == 0 else PROBLEMS[half:]
        bx     = lx if col_i == 0 else col2_x
        py     = y

        for i, (a, b) in enumerate(probs):
            n = col_i * half + i + 1

            text(c, bx,      py, f"{n:2}.",      font=BODY, size=8)
            text(c, bx + 18, py, f"{a} + {b} =", font=MATH, size=11)
            rule(c, bx + 62, py - 2, bx + 85,   0.5)

            if n in NOTES:
                text(c, bx + 88, py, "\u2020", font=BODYB, size=8)

            py -= row_h

    # Notes at bottom
    ny = content_bottom + notes_height
    rule(c, lx, ny, rx, 0.5)
    ny -= 13
    text(c, lx, ny, "Notes", font=BODYB, size=9)
    ny -= 13

    for n, note in NOTES.items():
        text(c, lx, ny, f"\u2020 #{n}  {note}", font=BODY, size=8)
        ny -= 13


# ── conclusion on page 10 (last left side) ───────────────────────────────────

def draw_conclusion(c, x_offset, col_w, margin, content_top, content_bottom):
    cx = x_offset + col_w / 2
    lx = x_offset + margin
    rx = x_offset + col_w - margin
    y  = content_top - 4

    text(c, cx, y, "Why Addition Matters", font=BODYB, size=12, align="center")
    y -= 14
    rule(c, lx, y, rx, 0.5)
    y -= 20

    text(c, cx, y, "Addition is the foundation of all mathematics.",
         font=BODY, size=9, align="center")
    y -= 24

    real_world = [
        ("Counting items",     "3 apples + 5 apples  =  8 apples"),
        ("Tracking time",      "12 min + 8 min  =  20 min"),
        ("Managing money",     "$4 + $3  =  $7"),
        ("Measuring distance", "2 km + 6 km  =  8 km"),
    ]
    for label, ex in real_world:
        text(c, lx, y, label, font=BODYB, size=9)
        text(c, rx,  y, ex,   font=MATH,  size=10, align="right")
        y -= 20

    y -= 6
    rule(c, lx, y, rx, 0.5)
    y -= 18

    text(c, cx, y, "What comes next?", font=BODYB, size=11, align="center")
    y -= 14
    nexts = [
        "Adding larger numbers (tens and hundreds)",
        "Understanding subtraction as reverse addition",
        "Building toward multiplication",
    ]
    for line in nexts:
        text(c, lx + 6, y, "–  " + line, font=BODY, size=9)
        y -= 14


# ── entry point ───────────────────────────────────────────────────────────────

def fill_content(c, page_num, side, x_offset, col_w, margin, content_top, content_bottom):
    c.setFillColor(colors.black)
    if side == "left":
        if page_num == TOTAL_PAGES - 1:   # page 9 = last left = conclusion
            draw_conclusion(c, x_offset, col_w, margin, content_top, content_bottom)
        else:
            draw_left(c, x_offset, col_w, margin, content_top, content_bottom)
    else:
        draw_right(c, x_offset, col_w, margin, content_top, content_bottom)