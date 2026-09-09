from reportlab.lib.pagesizes import landscape, letter
from reportlab.pdfgen import canvas
from content import fill_content, TOPIC

# ── Configuration ─────────────────────────────────────────────────────────────
OUTPUT_FILE = "worksheet.pdf"
NUM_SHEETS  = 2       # landscape sheets; each sheet = 2 pages (front + back)
LEVEL       = "LA"    # LA, LB, LC, ...
# ─────────────────────────────────────────────────────────────────────────────

FONT_R = "Helvetica"
FONT_B = "Helvetica-Bold"


def page_label(half_index):
    """
    Each landscape sheet has a front (odd) and back (even) page.
    half_index 0 → sheet 1 front → page 1
    half_index 1 → sheet 1 back  → page 2
    half_index 2 → sheet 2 front → page 3  etc.
    """
    return half_index + 1


def draw_half(c, W, H, x_offset, side, half_index):
    col_w  = W / 2
    M      = 24
    page_n = page_label(half_index)

    # Level — left
    c.setFont(FONT_R, 9)
    c.drawString(x_offset + M, H - 19, LEVEL)

    # Title (topic) — centre
    c.setFont(FONT_B, 13)
    c.drawCentredString(x_offset + col_w / 2, H - 19, TOPIC)

    # Page number — right
    c.setFont(FONT_R, 9)
    c.drawRightString(x_offset + col_w - M, H - 19, f"Page {page_n}")

    # Divider
    c.setLineWidth(0.7)
    c.line(x_offset + M, H - 25, x_offset + col_w - M, H - 25)

    # Name / Date / Time
    c.setFont(FONT_R, 9)
    field_y = H - 38
    c.drawString(x_offset + M, field_y, "Name: _______________________________")
    c.drawString(x_offset + M, field_y - 14,
                 "Date: _______________, ______   Time: __:__ \u2013 __:__")

    # Divider under fields
    c.setLineWidth(0.4)
    c.line(x_offset + M, field_y - 23, x_offset + col_w - M, field_y - 23)

    # Content
    content_top    = field_y - 31
    content_bottom = 18
    fill_content(c, page_n, side, x_offset, col_w, M, content_top, content_bottom)


def draw_sheet(c, sheet_num):
    W, H = landscape(letter)

    c.setLineWidth(1.1)
    c.line(W / 2, H - 8, W / 2, 8)

    left_idx  = (sheet_num - 1) * 2
    right_idx = left_idx + 1

    draw_half(c, W, H, x_offset=0,     side="left",  half_index=left_idx)
    draw_half(c, W, H, x_offset=W / 2, side="right", half_index=right_idx)


c = canvas.Canvas(OUTPUT_FILE, pagesize=landscape(letter))
c.setTitle(TOPIC)

for s in range(1, NUM_SHEETS + 1):
    draw_sheet(c, s)
    c.showPage()

c.save()
print(f"Saved → {OUTPUT_FILE}")