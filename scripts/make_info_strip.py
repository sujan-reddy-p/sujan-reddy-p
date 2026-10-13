#!/usr/bin/env python3
"""
Terminal-style info strip for the sujan-reddy-p profile README.

Spans the full README width (~720px) so it sits between the heatmap (above)
and the portrait + stats grid (below). One terminal window: title bar with
animated "typing" effect on the headline, then a static two-column body with
status (location / role / education), stack chips, and a tagged highlights
list. The body has no looping animation - the typing effect is one-shot so
the page stays calm on refresh.

ASCII monogram on the left is reusable - swap the chars glyph set without
touching layout. Goal: looks like a `neofetch` output for the human behind
the account, not a copy of anyone's bio.
"""
import html
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "info-strip.svg")
STATIC = bool(os.environ.get("STATIC"))

# ---- canvas -----------------------------------------------------------------
W = 720
H = 410
PAD = 16
TITLEBAR_H = 28
STATUS_H = 26

BG = "#0d1117"
BG2 = "#111722"
FRAME = "#30363d"
DIM = "#7d8590"
INK = "#c9d1d9"
GREEN = "#3fb950"
YELLOW = "#d29922"
BLUE = "#58a6ff"
PURPLE = "#bc8cff"

MONO = []  # monogram moved to <path> drawn letterforms below (S | R)

# ---- body content (from the user's current README; condensed) ---------------
HEADLINE = "sujan-reddy-p // Sujan Reddy"
STATUS_LINE = "based in San Francisco  //  MS Computer Science @ SUNY Buffalo"
STACK = ["TypeScript", "React", "Next.js", "Python", "FastAPI",
         "Postgres", "Docker", "Redis", "Git"]
BUILDING = [
    ("Local Lore",     "AI tour guide grounded in real venues"),
    ("FedLens",        "Fintech content sidekick"),
    ("Convergence",    "Two people, one editor - pair-coding for prose"),
    ("Local Workbench","First-pass meetups for new cities"),
]
EDUCATION = [
    ("MS Computer Science",   "University at Buffalo (SUNY)"),
    ("B.Tech Computer Science","Amrita Vishwa Vidyapeetham"),
]
AWARDS = [
    ("IBM Z Day — 1st Place",        "2024"),
    ("Hack-A-League — 1st Place",    "Within Splunk/IBM track"),
    ("Fantom Code-A-Thon — 3rd Place","Two-week build, public judging"),
]
WEBSITES = [
    ("sujanreddy.dev", "https://sujanreddy.dev"),
    ("GitHub",          "https://github.com/sujan-reddy-p"),
    ("LinkedIn",        "https://linkedin.com/in/sujanreddy-r"),
]


def chip(text, color):
    return (f'<rect x="{0}" y="0" rx="6" ry="6" '
            f'fill="{BLUE}" fill-opacity="0.10" '
            f'stroke="{color}" stroke-opacity="0.55" stroke-width="1"/>'
            # use a separate translate group; we draw at absolute coords below
            f'<text x="{0}" y="{0}" fill="{color}" font-size="11"></text>')


def bullet(text, color=INK):
    safe = html.escape(text)
    return f'<tspan fill="{color}">▸ </tspan><tspan fill="{INK}">{safe}</tspan>'


parts = []
parts.append(
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
    f'viewBox="0 0 {W} {H}" font-family="ui-monospace, SFMono-Regular, '
    f'Menlo, Consolas, monospace">'
)
parts.append('<defs>'
             f'<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">'
             f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/>'
             f'</linearGradient></defs>')
parts.append(f'<rect width="{W}" height="{H}" rx="12" fill="url(#bg)"/>')
parts.append(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" '
             f'fill="none" stroke="{FRAME}" stroke-width="1"/>')

# title bar with three traffic-light dots
parts.append(f'<line x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" '
             f'stroke="{FRAME}"/>')
for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" '
                 f'fill="{dotcol}"/>')

# type-once headline in the title bar (cursor rides the wipe)
type_y = TITLEBAR_H/2 + 4
char_w = 7.0
n_chars = len(HEADLINE)
total_typing = 2.4
per = total_typing / n_chars

# A second draw pass renders text after wipe, so we use a clip-path for the
# wipe and leave a static copy in place when done.
parts.append(f'<clipPath id="headline-clip">'
             f'<rect x="0" y="0" width="0" height="{TITLEBAR_H}">'
             f'<animate attributeName="width" from="0" to="{W}" '
             f'begin="0s" dur="{total_typing:.2f}s" fill="freeze"/>'
             f'</rect></clipPath>')
parts.append(f'<text x="{W/2}" y="{type_y}" fill="{INK}" font-size="13" '
             f'text-anchor="middle" font-weight="600" '
             f'clip-path="url(#headline-clip)">{html.escape(HEADLINE)}</text>')

# status bar at the bottom (animated typing, single line)
status_line_y = H - STATUS_H
status_y = status_line_y + 19
parts.append(f'<line x1="0" y1="{status_line_y:.1f}" x2="{W}" '
             f'y2="{status_line_y:.1f}" stroke="{FRAME}"/>')

status_n = len(STATUS_LINE)
status_per = (status_n / n_chars) * per  # proportional to headline
status_begin = max(0.05, total_typing - 0.4)
parts.append(f'<clipPath id="status-clip">'
             f'<rect x="0" y="{status_line_y:.1f}" width="0" height="{STATUS_H}">'
             f'<animate attributeName="width" from="0" to="{W}" '
             f'begin="{status_begin:.2f}s" dur="{total_typing:.2f}s" fill="freeze"/>'
             f'</rect></clipPath>')
parts.append(f'<text x="{PAD}" y="{status_y:.1f}" fill="{DIM}" font-size="12" '
             f'clip-path="url(#status-clip)">{html.escape(STATUS_LINE)}'
             f' <tspan fill="{BLUE}" font-weight="600">→ </tspan>'
             f'<tspan fill="{INK}">sujanreddy.dev</tspan></text>')

# blinking cursor at end of status bar
cursor_x = PAD + status_n * char_w
parts.append(f'<rect x="{cursor_x:.1f}" y="{status_y-12:.1f}" width="8" '
             f'height="14" fill="{INK}">'
             f'<animate attributeName="opacity" values="1;1;0;0" '
             f'keyTimes="0;0.5;0.51;1" dur="1s" repeatCount="indefinite"/>'
             f'</rect>')

# ---- body area --------------------------------------------------------------
body_top = TITLEBAR_H + 22
body_h = H - TITLEBAR_H - STATUS_H - 28
col_split = 200   # mono on left; body on right

# monogram — proper letterforms drawn as <path>s, one S and one R, sharing
# a 0–90 baseline. Cap-height matched. Drop-in block 240w x 90h.
mono_x = PAD + 6
mono_y = body_top + 6
mono_color = INK
parts.append(f'<g transform="translate({mono_x},{mono_y})">')
# S  (path fits in box 0..98 wide, 6..90 tall — bottom 6 baselines)
parts.append(
    f'<path d="M86,22 C86,12 76,6 56,6 C32,6 18,16 18,32 '
    f'C18,46 28,52 52,56 C68,59 74,62 74,72 '
    f'C74,80 66,84 54,84 C40,84 28,79 22,69 '
    f'L4,76 C12,90 28,96 52,96 C78,96 92,86 92,70 '
    f'C92,54 82,48 58,44 C42,41 36,38 36,30 '
    f'C36,24 42,20 54,20 C66,20 76,24 80,32 Z" '
    f'fill="{mono_color}"/>'
)
# R  (similar 0..96 box, 6..96 tall — net cap-height parity with S)
parts.append(
    f'<path d="M114,6 L168,6 C188,6 198,16 198,32 '
    f'C198,44 192,52 180,55 C188,58 196,64 200,76 L186,96 '
    f'L160,96 C158,84 152,78 142,78 L138,78 L138,96 L114,96 Z '
    f'M138,28 L138,54 L162,54 C170,54 176,49 176,42 '
    f'C176,35 170,28 162,28 Z" '
    f'fill="{mono_color}"/>'
)
parts.append('</g>')

# vertical divider between mono and body — pushed past R's right edge (240px)
divider_x = 252
parts.append(f'<line x1="{divider_x}" y1="{body_top}" x2="{divider_x}" '
             f'y2="{body_top + body_h - 6:.1f}" '
             f'stroke="{FRAME}" stroke-dasharray="2 4"/>')

# right column - sections
rx = divider_x + 14
ry = body_top
section_label_color = DIM
label_w = 12

def section(title, items_with_kv, y_start, *, color_map=None):
    """(unused stub - section rendering lives inline below)"""
    return y_start

# role/status
parts.append(f'<text x="{rx}" y="{ry:.1f}" fill="{BLUE}" font-size="12" '
             f'font-weight="600">who</text>')
ry += 16
parts.append(f'<text x="{rx}" y="{ry:.1f}" fill="{INK}" font-size="11.5">'
             f'<tspan fill="{DIM}">▸ </tspan>'
             f'Product-minded engineer building<tspan fill="{GREEN}" '
             f'font-weight="600"> agentic products</tspan> that</text>')
ry += 16
parts.append(f'<text x="{rx}" y="{ry:.1f}" fill="{INK}" font-size="11.5">'
             f'<tspan fill="{DIM}">  </tspan>'
             f'solve useful problems.</text>')
ry += 16
parts.append(f'<text x="{rx}" y="{ry:.1f}" fill="{INK}" font-size="11.5">'
             f'<tspan fill="{DIM}">▸ </tspan>'
             f'<tspan fill="{YELLOW}" font-weight="600">'
             f'Full-time SWE</tspan> — MS CS, US-based (F-1 OPT)</text>')
ry += 20

# stack chip strip
parts.append(f'<text x="{rx}" y="{ry:.1f}" fill="{BLUE}" font-size="12" '
             f'font-weight="600">stack</text>')
ry += 16
chip_x = rx
chip_y = ry - 11
chip_h = 18
gutter = 6
for tech in STACK:
    # width-approx: ~7px per char + 14px padding
    w = 14 + len(tech) * 6.6
    # pick a stable color per stack category
    color = (
        BLUE if tech in ("TypeScript", "React", "Next.js") else
        YELLOW if tech in ("Python", "FastAPI") else
        PURPLE if tech in ("Postgres", "Redis") else
        GREEN
    )
    parts.append(f'<g>'
                 f'<rect x="{chip_x:.1f}" y="{chip_y:.1f}" rx="5" '
                 f'height="{chip_h}" width="{w:.1f}" '
                 f'fill="{color}" fill-opacity="0.10" '
                 f'stroke="{color}" stroke-opacity="0.55" stroke-width="1"/>'
                 f'<text x="{chip_x + 7:.1f}" y="{chip_y + 13:.1f}" '
                 f'fill="{color}" font-size="10.5" '
                 f'font-weight="600">{html.escape(tech)}</text>'
                 f'</g>')
    chip_x += w + gutter
    if chip_x > W - 60:
        chip_x = rx
        chip_y += chip_h + 4
ry = chip_y + chip_h + 10

# building row
parts.append(f'<text x="{rx}" y="{ry:.1f}" fill="{BLUE}" font-size="12" '
             f'font-weight="600">building</text>')
ry_label = ry
ry += 16
for name, blurb in BUILDING:
    parts.append(f'<text x="{rx}" y="{ry:.1f}" fill="{INK}" '
                 f'font-size="11.5">'
                 f'<tspan fill="{DIM}">▸ </tspan>'
                 f'<tspan fill="{GREEN}" font-weight="600">'
                 f'{html.escape(name)}</tspan>'
                 f'<tspan fill="{DIM}"> — </tspan>'
                 f'<tspan fill="{INK}">{html.escape(blurb)}</tspan></text>')
    ry += 16
ry += 6

# awards / recognition
parts.append(f'<text x="{rx}" y="{ry:.1f}" fill="{BLUE}" font-size="12" '
             f'font-weight="600">awards</text>')
ry += 16
for name, year in AWARDS:
    parts.append(f'<text x="{rx}" y="{ry:.1f}" fill="{INK}" font-size="11.5">'
                 f'<tspan fill="{DIM}">▸ </tspan>'
                 f'<tspan fill="{YELLOW}" font-weight="600">'
                 f'{html.escape(name)}</tspan>'
                 f'<tspan fill="{DIM}">  ({html.escape(year)})</tspan></text>')
    ry += 16

# websites row at the end of right column
ry += 4
parts.append(f'<text x="{rx}" y="{ry:.1f}" fill="{BLUE}" font-size="12" '
             f'font-weight="600">links</text>')
ry += 16
for label, url in WEBSITES:
    parts.append(f'<text x="{rx}" y="{ry:.1f}" fill="{INK}" font-size="11.5">'
                 f'<tspan fill="{DIM}">▸ </tspan>'
                 f'<tspan fill="{INK}" font-weight="600">'
                 f'{html.escape(label)}:</tspan>'
                 f'<tspan fill="{BLUE}" text-decoration="underline"> '
                 f'{html.escape(url)}</tspan></text>')
    ry += 16

parts.append("</svg>")
svg = "".join(parts)
with open(OUT, "w") as f:
    f.write(svg)
print("wrote", OUT, len(svg), "bytes;", W, "x", H)
