#!/usr/bin/env python3
"""Build the animated SVGs behind the profile README.

    python3 profile/build.py

GitHub shows README images through <img>, which runs no scripts and loads no
external fonts. So every asset here is self-contained SVG: CSS keyframes for
most motion, SMIL <animateMotion> where something has to follow a path, and
system font stacks. Change the data in this file, rerun, commit the output.

Anything animated has a resting state that is the finished frame, so viewers
with reduced motion turned on still see the full picture.
"""

from __future__ import annotations

import math
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent / "assets"

BG = "#0B1220"
PANEL = "#0E1729"
RAISED = "#14223A"
LINE = "#1E2E4A"
BLUE = "#0A66C2"
SKY = "#4DA3FF"
AMBER = "#FFB020"
GREEN = "#3DDC97"
RED = "#FF5C7A"
TEXT = "#E6EDF7"
MUTED = "#8B9BB4"
DIM = "#5A6C8C"

SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"
MONO_W = 0.6  # advance width of one monospace glyph, in em


def esc(s: str) -> str:
    return escape(s, {'"': "&quot;"})


def pct(t: float, total: float) -> str:
    return f"{min(t / total, 1) * 100:.3f}%"


def document(w: int, h: int, label: str, body: str, css: str = "", defs: str = "") -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" aria-label="{esc(label)}">\n'
        f"<title>{esc(label)}</title>\n"
        "<style>\n"
        f"text{{font-family:{SANS}}}\n.mono{{font-family:{MONO}}}\n"
        f"{css.strip()}\n"
        "@media (prefers-reduced-motion:reduce){*{animation:none!important}}\n"
        "</style>\n"
        f"<defs>{defs}</defs>\n{body}\n</svg>\n"
    )


def grid(pid: str, minor: int = 24, major: int = 120) -> str:
    return (
        f'<pattern id="{pid}-m" width="{minor}" height="{minor}" patternUnits="userSpaceOnUse">'
        f'<path d="M{minor} 0H0V{minor}" fill="none" stroke="{LINE}" stroke-opacity=".5"/></pattern>'
        f'<pattern id="{pid}" width="{major}" height="{major}" patternUnits="userSpaceOnUse">'
        f'<rect width="{major}" height="{major}" fill="url(#{pid}-m)"/>'
        f'<path d="M{major} 0H0V{major}" fill="none" stroke="{LINE}"/></pattern>'
    )


def chip(x: float, y: float, label: str, size: float = 14, h: float = 32, pad: float = 12,
         fill: str = RAISED, stroke: str = LINE, color: str = TEXT, attrs: str = "") -> tuple[str, float]:
    w = len(label) * size * MONO_W + pad * 2
    return (
        f"<g {attrs}>"
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h}" rx="{h / 2}" fill="{fill}" stroke="{stroke}"/>'
        f'<text class="mono" x="{x + w / 2:.1f}" y="{y + h / 2 + size * 0.35:.1f}" text-anchor="middle" '
        f'font-size="{size}" fill="{color}">{esc(label)}</text></g>',
        w,
    )


def polyline(points: list[tuple[float, float]]) -> str:
    return "M" + " L".join(f"{x} {y}" for x, y in points)


def length(points: list[tuple[float, float]]) -> float:
    return sum(math.dist(a, b) for a, b in zip(points, points[1:]))


def polar(cx: float, cy: float, r: float, deg: float) -> tuple[float, float]:
    """Point at bearing `deg` (clockwise from north) and radius r."""
    a = math.radians(deg)
    return cx + r * math.sin(a), cy - r * math.cos(a)


# ---------------------------------------------------------------- hero

def hero() -> str:
    W, H = 1200, 420
    css = """
.rise{animation:rise 1s cubic-bezier(.16,1,.3,1) both}
@keyframes rise{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:none}}
.ping{transform-box:fill-box;transform-origin:center;animation:ping 2.6s ease-out infinite}
@keyframes ping{0%{opacity:.75;transform:scale(1)}80%,100%{opacity:0;transform:scale(3.4)}}
.route{stroke-dasharray:1;stroke-dashoffset:0;animation:route 1.6s cubic-bezier(.65,0,.35,1) both}
@keyframes route{from{stroke-dashoffset:1}}
.pop{transform-box:fill-box;transform-origin:center;animation:pop .7s cubic-bezier(.34,1.56,.64,1) both}
@keyframes pop{from{opacity:0;transform:scale(.2)}}
"""
    defs = (
        grid("g")
        + f'<clipPath id="clip"><rect width="{W}" height="{H}" rx="18"/></clipPath>'
        + '<radialGradient id="fade" cx="76%" cy="50%" r="62%"><stop offset="0" stop-color="#fff"/>'
          '<stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>'
        + f'<mask id="gm"><rect width="{W}" height="{H}" fill="url(#fade)"/></mask>'
        + f'<radialGradient id="glow" cx="76%" cy="52%" r="42%"><stop offset="0" stop-color="{BLUE}" stop-opacity=".38"/>'
          f'<stop offset="1" stop-color="{BLUE}" stop-opacity="0"/></radialGradient>'
        + f'<linearGradient id="shine" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="600" y2="0">'
          f'<stop offset="0" stop-color="{TEXT}"/><stop offset=".4" stop-color="{TEXT}"/>'
          f'<stop offset=".5" stop-color="#8CC8FF"/><stop offset=".6" stop-color="{TEXT}"/>'
          f'<stop offset="1" stop-color="{TEXT}"/>'
          '<animateTransform attributeName="gradientTransform" type="translate" values="-700 0;700 0;700 0" '
          'keyTimes="0;.3;1" dur="9s" repeatCount="indefinite"/></linearGradient>'
        + '<filter id="soft" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="4"/></filter>'
    )

    depot = (905, 215)
    # (label, node, route from depot, label dx, label dy, anchor)
    drops = [
        ("W11", (760, 110), [depot, (905, 160), (855, 110), (760, 110)], 0, -16, "middle"),
        ("NW1", (1060, 95), [depot, (1025, 95), (1060, 95)], 16, 5, "start"),
        ("WC2", (1120, 250), [depot, (1000, 215), (1035, 250), (1120, 250)], 0, 26, "middle"),
        ("SW3", (1010, 350), [depot, (905, 255), (1000, 350), (1010, 350)], 16, 5, "start"),
        ("W6", (790, 330), [depot, (845, 275), (845, 330), (790, 330)], -16, 5, "end"),
        ("W14", (720, 215), [depot, (720, 215)], -16, 5, "end"),
    ]

    net = [
        f'<path d="M680 305 C760 262 820 338 900 302 S1040 250 1100 292 S1180 322 1230 300" fill="none" '
        f'stroke="{BLUE}" stroke-opacity=".2" stroke-width="18" stroke-linecap="round"/>',
    ]
    for i, (_, _, pts, *_rest) in enumerate(drops):
        net.append(
            f'<path class="route" style="animation-delay:{.3 + i * .12:.2f}s" pathLength="1" d="{polyline(pts)}" '
            f'fill="none" stroke="{SKY}" stroke-opacity=".45" stroke-width="2.5" stroke-linejoin="round"/>'
        )
    for i, (name, (nx, ny), pts, dx, dy, anchor) in enumerate(drops):
        delay = 1.2 + i * .12
        net.append(
            f'<circle class="ping" style="animation-delay:{i * .43:.2f}s" cx="{nx}" cy="{ny}" r="6" fill="none" stroke="{SKY}"/>'
            f'<circle class="pop" style="animation-delay:{delay:.2f}s" cx="{nx}" cy="{ny}" r="6" fill="{BG}" stroke="{SKY}" stroke-width="2.5"/>'
            f'<text class="mono pop" style="animation-delay:{delay:.2f}s" x="{nx + dx}" y="{ny + dy}" '
            f'text-anchor="{anchor}" font-size="13" fill="{MUTED}">{name}</text>'
        )
    for i, (_, _, pts, *_rest) in enumerate(drops):
        dur = max(5.0, length(pts) / 26)
        motion = (
            f'<animateMotion dur="{dur:.2f}s" begin="-{i * 1.37:.2f}s" repeatCount="indefinite" path="{polyline(pts)}" '
            'keyPoints="0;1;1;0;0" keyTimes="0;.42;.5;.92;1" calcMode="spline" '
            'keySplines=".45 0 .55 1;0 0 1 1;.45 0 .55 1;0 0 1 1"/>'
        )
        net.append(
            f'<circle r="7" fill="{AMBER}" opacity=".7" filter="url(#soft)">{motion}</circle>'
            f'<circle r="4" fill="{AMBER}">{motion}</circle>'
        )
    dx, dy = depot
    net.append(
        f'<rect class="ping" x="{dx - 11}" y="{dy - 11}" width="22" height="22" rx="5" fill="none" stroke="{AMBER}"/>'
        f'<rect class="pop" style="animation-delay:.2s" x="{dx - 11}" y="{dy - 11}" width="22" height="22" rx="5" fill="{AMBER}"/>'
        f'<rect x="{dx - 4}" y="{dy - 4}" width="8" height="8" rx="1.5" fill="{BG}"/>'
    )

    chips, x = [], 64
    for i, label in enumerate(["BEng (Hons) · IMechE", "Python · SQL · MATLAB", "CAD · FEA · CFD"]):
        c, w = chip(x, 296, label, size=14, h=34, pad=14,
                    attrs=f'class="rise" style="animation-delay:{.75 + i * .1:.2f}s"')
        chips.append(c)
        x += w + 10

    body = f"""
<g clip-path="url(#clip)">
<rect width="{W}" height="{H}" fill="{BG}"/>
<rect width="{W}" height="{H}" fill="url(#g)" mask="url(#gm)"/>
<rect width="{W}" height="{H}" fill="url(#glow)"/>
{''.join(net)}
</g>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="18" fill="none" stroke="{LINE}"/>

<g class="rise" style="animation-delay:.05s">
<circle class="ping" cx="70" cy="87" r="4.5" fill="{GREEN}"/>
<circle cx="70" cy="87" r="4.5" fill="{GREEN}"/>
<text class="mono" x="86" y="92" font-size="13" letter-spacing="1.6" fill="{MUTED}">OPEN TO DATA, AUTOMATION &amp; SYSTEMS ROLES · UK-WIDE</text>
</g>
<text class="rise" style="animation-delay:.2s" x="60" y="178" font-size="70" font-weight="750" letter-spacing="-1.5" fill="url(#shine)">Jamal Lharri</text>
<text class="mono rise" style="animation-delay:.4s" x="64" y="226" font-size="21" fill="{TEXT}">Mechanical engineer<tspan fill="{AMBER}"> → </tspan><tspan fill="{SKY}">data &amp; automation</tspan></text>
<text class="rise" style="animation-delay:.55s" x="64" y="264" font-size="18" fill="{MUTED}">Regional Development Team Manager at Ocado Logistics · London</text>
{''.join(chips)}
<text class="mono rise" style="animation-delay:1s" x="64" y="388" font-size="13" letter-spacing="1" fill="{DIM}">github.com/JGit705</text>

<text class="mono rise" style="animation-delay:1.1s" x="1148" y="62" text-anchor="end" font-size="13.5" letter-spacing="1.4" fill="{MUTED}">140+ VANS · CENTRAL &amp; WEST LONDON</text>
<text class="mono rise" style="animation-delay:1.2s" x="1148" y="388" text-anchor="end" font-size="13" letter-spacing="1" fill="{DIM}">51.5072° N   0.1276° W</text>
"""
    return document(W, H, "Jamal Lharri. Mechanical engineer moving into data and automation. "
                          "Regional Development Team Manager at Ocado Logistics, London.", body, css, defs)


# ---------------------------------------------------------------- terminal

def terminal() -> str:
    W, H = 1200, 362
    T = 15.0  # loop length, seconds
    size = 16
    cw = size * MONO_W
    x0, first, lh = 36, 86, 31
    prompt_w = 4 * cw  # "~ $ "

    script = [
        ("whoami", [("Jamal Lharri. ", TEXT),
                    ("Mechanical engineer (BEng, IMechE) who builds data and automation tools.", MUTED)]),
        ("cat now.txt", [("Regional Development Team Manager @ Ocado. ", TEXT),
                         ("Daily dispatch for 140+ vans, Central & West London.", MUTED)]),
        ("ls ~/builds", [("MOTIntel/   RadarScope/   SkyTrack/   SafeSite/   Wayglow/", SKY)]),
        ("echo $OPEN_TO", [("Data, automation and systems engineering roles. ", TEXT), ("UK-wide.", AMBER)]),
    ]

    css = [
        f".loop{{animation:loop {T}s linear infinite}}",
        "@keyframes loop{0%,95%{opacity:1}98.5%,100%{opacity:0}}",
        ".blink{animation:blink 1.1s steps(1) infinite}",
        "@keyframes blink{50%{opacity:0}}",
    ]
    lines = []
    t = 0.5
    for i, (cmd, out) in enumerate(script):
        y_cmd = first + i * 2 * lh
        y_out = y_cmd + lh
        x_cmd = x0 + prompt_w
        n = len(cmd)
        shown, typed_from = t, t + .45
        typed_to = typed_from + n * .06
        out_at = typed_to + .35
        t = out_at + .8

        css += [
            f".p{i}{{animation:p{i} {T}s linear infinite both}}",
            f"@keyframes p{i}{{0%,{pct(shown, T)}{{opacity:0}}{pct(shown + .01, T)},100%{{opacity:1}}}}",
            f".k{i}{{transform:translateX({n * cw:.1f}px);animation:k{i} {T}s linear infinite both}}",
            f"@keyframes k{i}{{0%,{pct(typed_from, T)}{{transform:translateX(0);animation-timing-function:steps({n},end)}}"
            f"{pct(typed_to, T)},100%{{transform:translateX({n * cw:.1f}px)}}}}",
            f".c{i}{{opacity:0;animation:c{i} {T}s linear infinite both}}",
            f"@keyframes c{i}{{0%,{pct(shown, T)}{{opacity:0}}{pct(shown + .01, T)},{pct(out_at, T)}{{opacity:1}}"
            f"{pct(out_at + .01, T)},100%{{opacity:0}}}}",
            f".o{i}{{animation:o{i} {T}s linear infinite both}}",
            f"@keyframes o{i}{{0%,{pct(out_at, T)}{{opacity:0}}{pct(out_at + .12, T)},100%{{opacity:1}}}}",
        ]
        spans = "".join(f'<tspan fill="{color}">{esc(s)}</tspan>' for s, color in out)
        out_len = sum(len(s) for s, _ in out)
        lines.append(f"""
<g class="p{i}"><text class="mono" x="{x0}" y="{y_cmd}" font-size="{size}"><tspan fill="{GREEN}">~</tspan><tspan fill="{DIM}"> $</tspan></text></g>
<text class="mono" x="{x_cmd:.1f}" y="{y_cmd}" font-size="{size}" fill="{TEXT}" textLength="{n * cw:.1f}" lengthAdjust="spacing">{esc(cmd)}</text>
<g class="k{i}"><rect x="{x_cmd:.1f}" y="{y_cmd - 20}" width="{n * cw + 14:.1f}" height="28" fill="{PANEL}"/>
<rect class="c{i}" x="{x_cmd:.1f}" y="{y_cmd - 16}" width="{cw:.1f}" height="21" fill="{TEXT}" opacity=".85"/></g>
<text class="mono o{i}" style="white-space:pre" x="{x0}" y="{y_out}" font-size="{size}" textLength="{out_len * cw:.1f}" lengthAdjust="spacing">{spans}</text>""")

    y_last = first + len(script) * 2 * lh
    css += [
        f".pf{{animation:pf {T}s linear infinite both}}",
        f"@keyframes pf{{0%,{pct(t, T)}{{opacity:0}}{pct(t + .01, T)},100%{{opacity:1}}}}",
    ]
    lines.append(f"""
<g class="pf"><text class="mono" x="{x0}" y="{y_last}" font-size="{size}"><tspan fill="{GREEN}">~</tspan><tspan fill="{DIM}"> $</tspan></text>
<rect class="blink" x="{x0 + prompt_w:.1f}" y="{y_last - 16}" width="{cw:.1f}" height="21" fill="{TEXT}" opacity=".85"/></g>""")

    defs = f'<clipPath id="clip"><rect width="{W}" height="{H}" rx="16"/></clipPath>'
    body = f"""
<g clip-path="url(#clip)">
<rect width="{W}" height="{H}" fill="{PANEL}"/>
<rect width="{W}" height="42" fill="{RAISED}"/>
<path d="M0 42.5H{W}" stroke="{LINE}"/>
</g>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="16" fill="none" stroke="{LINE}"/>
<circle cx="26" cy="21" r="6" fill="#FF5F57" opacity=".9"/>
<circle cx="46" cy="21" r="6" fill="#FEBC2E" opacity=".9"/>
<circle cx="66" cy="21" r="6" fill="#28C840" opacity=".9"/>
<text class="mono" x="{W / 2}" y="26" text-anchor="middle" font-size="13" fill="{MUTED}">jamal@london: ~/profile</text>
<text class="mono" x="{W - 24}" y="26" text-anchor="end" font-size="12" fill="{DIM}">zsh</text>
<g class="loop">{''.join(lines)}
</g>
"""
    alt = " ".join(f"$ {cmd}: {''.join(s for s, _ in out)}" for cmd, out in script)
    return document(W, H, alt, body, "\n".join(css), defs)


# ---------------------------------------------------------------- numbers

def numbers() -> str:
    W, H = 1200, 180
    size, row = 54, 66
    cw = size * MONO_W
    base = 102
    tiles = [
        ("42.7M", "MOT tests analysed", "MOTINTEL · DVSA 2025"),
        ("140+", "vans in daily dispatch", "OCADO LOGISTICS"),
        ("24", "CAD projects modelled", "ONSHAPE · SOLIDWORKS"),
        ("14", "engineering case studies", "FEA · CFD · AUTONOMY"),
    ]
    tile_w, gap = 285, 20
    css = [
        ".bar{transform-box:fill-box;transform-origin:0 50%;animation:bar 1.2s cubic-bezier(.16,1,.3,1) both}",
        "@keyframes bar{from{transform:scaleX(0)}}",
        ".fade{animation:fade .6s ease both}",
        "@keyframes fade{from{opacity:0}}",
    ]
    defs, body = [], []
    col_id = 0
    for ti, (value, label, source) in enumerate(tiles):
        tx = ti * (tile_w + gap)
        body.append(f'<rect x="{tx + .5}" y=".5" width="{tile_w - 1}" height="{H - 1}" rx="16" fill="{PANEL}" stroke="{LINE}"/>')
        body.append(f'<rect class="bar" style="animation-delay:{.2 + ti * .15:.2f}s" x="{tx + 24}" y="24" width="30" height="3" rx="1.5" fill="{AMBER}"/>')
        for ci, ch in enumerate(value):
            x = tx + 24 + ci * cw
            delay = .15 + ti * .15 + ci * .1
            if not ch.isdigit():
                body.append(f'<text class="mono fade" style="animation-delay:{delay + 1:.2f}s" x="{x:.1f}" y="{base}" '
                            f'font-size="{size}" font-weight="700" fill="{SKY if ch in ".M+" else TEXT}">{esc(ch)}</text>')
                continue
            d = int(ch)
            strip = list(range(10)) * 2 + list(range(d + 1))
            to = -(len(strip) - 1) * row
            css += [f".r{col_id}{{animation:r{col_id} {1.9 + ci * .12:.2f}s cubic-bezier(.16,1,.3,1) {delay:.2f}s both}}",
                    f"@keyframes r{col_id}{{from{{transform:translateY(0)}}to{{transform:translateY({to}px)}}}}"]
            defs.append(f'<clipPath id="n{col_id}"><rect x="{x:.1f}" y="{base - size * .8:.1f}" width="{cw + 2:.1f}" height="{size * 1.05:.1f}"/></clipPath>')
            digits = "".join(
                f'<text class="mono" x="{x:.1f}" y="{base + k * row}" font-size="{size}" font-weight="700" fill="{TEXT}">{v}</text>'
                for k, v in enumerate(strip)
            )
            body.append(f'<g clip-path="url(#n{col_id})"><g class="r{col_id}" style="transform:translateY({to}px)">{digits}</g></g>')
            col_id += 1
        body.append(f'<text class="fade" style="animation-delay:{.6 + ti * .15:.2f}s" x="{tx + 24}" y="138" font-size="17" font-weight="600" fill="{TEXT}">{esc(label)}</text>')
        body.append(f'<text class="mono fade" style="animation-delay:{.7 + ti * .15:.2f}s" x="{tx + 24}" y="161" font-size="12.5" letter-spacing="1.2" fill="{DIM}">{esc(source)}</text>')

    alt = "By the numbers: " + "; ".join(f"{v} {l} ({s.title()})" for v, l, s in tiles)
    return document(W, H, alt, "\n".join(body), "\n".join(css), "".join(defs))


# ---------------------------------------------------------------- project cards

def card(title: str, tag: str, desc: list[str], stack: list[str], public: bool,
         visual: str, css: str = "", defs: str = "", alt: str = "") -> str:
    W, H, band = 600, 364, 160
    pill_label = "PUBLIC REPO ↗" if public else "PRIVATE BUILD"
    pill_color = GREEN if public else MUTED
    pw = len(pill_label) * 11.5 * MONO_W + 22
    chips, x = [], 28
    for i, s in enumerate(stack):
        c, w = chip(x, 312, s, size=13.5, h=30, pad=11, attrs=f'class="fade" style="animation-delay:{.3 + i * .07:.2f}s"')
        chips.append(c)
        x += w + 8

    base_css = """
.fade{animation:fade .7s ease both}
@keyframes fade{from{opacity:0}}
"""
    body = f"""
<g clip-path="url(#card)">
<rect width="{W}" height="{H}" fill="{PANEL}"/>
<rect width="{W}" height="{band}" fill="{BG}"/>
<rect width="{W}" height="{band}" fill="url(#cg)" opacity=".7"/>
<g clip-path="url(#band)">{visual}</g>
<path d="M0 {band}.5H{W}" stroke="{LINE}"/>
</g>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="16" fill="none" stroke="{LINE}"/>
<text class="mono" x="28" y="198" font-size="13" letter-spacing="1.2" fill="{SKY}">{esc(tag)}</text>
<rect x="{W - 28 - pw:.1f}" y="181" width="{pw:.1f}" height="24" rx="12" fill="{pill_color}" fill-opacity=".08" stroke="{pill_color}" stroke-opacity=".4"/>
<text class="mono" x="{W - 28 - pw / 2:.1f}" y="197" text-anchor="middle" font-size="11.5" letter-spacing=".6" fill="{pill_color}">{pill_label}</text>
<text x="28" y="238" font-size="28" font-weight="700" letter-spacing="-.4" fill="{TEXT}">{esc(title)}</text>
<text x="28" y="268" font-size="16.5" fill="{MUTED}">{esc(desc[0])}</text>
<text x="28" y="292" font-size="16.5" fill="{MUTED}">{esc(desc[1])}</text>
{''.join(chips)}
"""
    all_defs = (grid("cg", 20, 100)
                + f'<clipPath id="card"><rect width="{W}" height="{H}" rx="16"/></clipPath>'
                + f'<clipPath id="band"><rect width="{W}" height="{band}"/></clipPath>' + defs)
    return document(W, H, alt or f"{title}. {' '.join(desc)}", body, base_css + css, all_defs)


def card_motintel() -> str:
    data = [("0–3y", 11.01), ("6–9y", 20.91), ("12–15y", 37.53), ("18–21y", 42.72), ("27–30y", 33.33)]
    peak = max(v for _, v in data)
    bw, gap, x0, baseline, max_h = 72, 34, 52, 132, 82
    css = """
.grow{transform-box:fill-box;transform-origin:50% 100%;animation:grow 1.3s cubic-bezier(.16,1,.3,1) both}
@keyframes grow{from{transform:scaleY(0)}}
.ping{transform-box:fill-box;transform-origin:center;animation:ping 2.2s ease-out 2s infinite both}
@keyframes ping{0%{opacity:.8;transform:scale(1)}80%,100%{opacity:0;transform:scale(3)}}
"""
    parts = [
        f'<text class="mono" x="24" y="28" font-size="12" letter-spacing="1.2" fill="{DIM}">FAILURE RATE BY VEHICLE AGE · 2025</text>',
        f'<path d="M24 {baseline}.5H576" stroke="{LINE}"/>',
    ]
    for i, (age, v) in enumerate(data):
        x = x0 + i * (bw + gap)
        h = v / peak * max_h
        is_peak = v == peak
        fill = AMBER if is_peak else SKY
        delay = .25 + i * .12
        parts.append(
            f'<g class="grow" style="animation-delay:{delay:.2f}s">'
            f'<rect x="{x}" y="{baseline - h:.1f}" width="{bw}" height="{h:.1f}" rx="4" fill="{fill}" fill-opacity="{.85 if is_peak else .22}"/>'
            f'<rect x="{x}" y="{baseline - h:.1f}" width="{bw}" height="2.5" rx="1" fill="{fill}"/></g>'
            f'<text class="mono fade" style="animation-delay:{delay + .7:.2f}s" x="{x + bw / 2}" y="{baseline - h - 8:.1f}" '
            f'text-anchor="middle" font-size="13" font-weight="{700 if is_peak else 400}" fill="{AMBER if is_peak else TEXT}">{v:.1f}%</text>'
            f'<text class="mono" x="{x + bw / 2}" y="151" text-anchor="middle" font-size="11.5" fill="{DIM}">{age}</text>'
        )
        if is_peak:
            parts.append(f'<circle class="ping" cx="{x + bw + 10}" cy="{baseline - h + 1:.1f}" r="3.5" fill="{AMBER}"/>'
                         f'<circle cx="{x + bw + 10}" cy="{baseline - h + 1:.1f}" r="3.5" fill="{AMBER}"/>')
    return card(
        "MOTIntel", "DATA · LLM GROUNDED IN 42.7M ROWS",
        ["Should you buy that used car? One page of answers from every",
         "UK MOT test in 2025, with an LLM checked against the data."],
        ["Python", "DuckDB", "Polars", "Streamlit", "Gemini"], True, "".join(parts), css,
        alt="MOTIntel: used car reliability from 42.7 million UK MOT tests in 2025, with an LLM layer checked "
            "against the data. Chart shows failure rate peaking at 42.7% for 18 to 21 year old cars.",
    )


def card_radarscope() -> str:
    cx, cy, R, period = 116, 82, 64, 4.0
    contacts = [  # bearing, range fraction, heading, callsign, level
        (40, .62, 220, "BAW283", "FL360"),
        (145, .45, 300, "EZY84KT", "FL120"),
        (250, .8, 80, "RYR5TP", "FL090"),
        (318, .32, 140, "VIR3N", "FL240"),
    ]
    css = f"""
.sweep{{transform-box:view-box;transform-origin:{cx}px {cy}px;animation:spin {period}s linear infinite}}
@keyframes spin{{to{{transform:rotate(360deg)}}}}
.blip{{animation:blip {period}s linear infinite}}
@keyframes blip{{0%{{opacity:1}}65%,100%{{opacity:.2}}}}
.row{{animation:row {period}s linear infinite}}
@keyframes row{{0%{{fill:{AMBER}}}30%,100%{{fill:{MUTED}}}}}
"""
    parts = [f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="{SKY}" fill-opacity=".04"/>']
    for r in (R / 3, 2 * R / 3, R):
        parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r:.1f}" fill="none" stroke="{SKY}" stroke-opacity=".28"/>')
    parts.append(f'<path d="M{cx - R} {cy}H{cx + R}M{cx} {cy - R}V{cy + R}" stroke="{SKY}" stroke-opacity=".16"/>')
    for deg in range(0, 360, 30):
        (x1, y1), (x2, y2) = polar(cx, cy, R, deg), polar(cx, cy, R + 5, deg)
        parts.append(f'<path d="M{x1:.1f} {y1:.1f}L{x2:.1f} {y2:.1f}" stroke="{SKY}" stroke-opacity=".45"/>')

    slices = []
    for k in range(24):
        a1, a2 = -(k + 1) * 3, -k * 3
        (x1, y1), (x2, y2) = polar(cx, cy, R, a1), polar(cx, cy, R, a2)
        slices.append(f'<path d="M{cx} {cy}L{x1:.2f} {y1:.2f}A{R} {R} 0 0 1 {x2:.2f} {y2:.2f}Z" '
                      f'fill="{SKY}" fill-opacity="{.32 * (1 - k / 24):.3f}"/>')
    parts.append(f'<g class="sweep">{"".join(slices)}<path d="M{cx} {cy}V{cy - R}" stroke="{SKY}" stroke-width="1.5"/></g>')
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="2.5" fill="{SKY}"/>')

    cols = (236, 326, 390, 446)
    parts.append("".join(f'<text class="mono" x="{x}" y="30" font-size="11.5" letter-spacing="1" fill="{DIM}">{h}</text>'
                         for x, h in zip(cols, ("CALLSIGN", "LEVEL", "HDG", "RNG"))))
    parts.append(f'<circle cx="524" cy="26" r="3.5" fill="{GREEN}"/><text class="mono" x="576" y="30" text-anchor="end" '
                 f'font-size="11.5" letter-spacing="1" fill="{GREEN}">ADS-B</text>')
    for i, (brg, rf, hdg, callsign, level) in enumerate(contacts):
        delay = -(1 - brg / 360) * period
        bx, by = polar(cx, cy, R * rf, brg)
        parts.append(
            f'<g class="blip" style="animation-delay:{delay:.2f}s" transform="translate({bx:.1f} {by:.1f}) rotate({hdg})">'
            f'<path d="M0 -6L4.5 5L0 2.5L-4.5 5Z" fill="{AMBER}"/></g>'
        )
        y = 58 + i * 26
        values = (callsign, level, f"{hdg:03d}°", f"{round(rf * 40)}nm")
        parts.append("".join(
            f'<text class="mono row" style="animation-delay:{delay:.2f}s" x="{x}" y="{y}" font-size="14" fill="{MUTED}">{v}</text>'
            for x, v in zip(cols, values)))
    return card(
        "RadarScope", "REAL-TIME · ADS-B · NO ML ANYWHERE",
        ["A plan-position indicator for the traffic overhead: range",
         "rings, a sweep, and a glyph for every aircraft's heading."],
        ["Python", "FastAPI", "Canvas", "OpenSky"], True, "".join(parts), css,
        alt="RadarScope: a radar-style plan-position indicator for live air traffic over ADS-B, with a rotating "
            "sweep and a heading glyph per aircraft.",
    )


def card_skytrack() -> str:
    period = 10
    css = f"""
.lock{{transform-box:fill-box;transform-origin:center;animation:lock {period}s cubic-bezier(.16,1,.3,1) infinite}}
@keyframes lock{{0%,34%{{transform:scale(1.5);stroke:{AMBER}}}40%,100%{{transform:scale(1);stroke:{GREEN}}}}}
.seek{{animation:seek {period}s linear infinite}}
@keyframes seek{{0%,36%{{opacity:1}}38%,100%{{opacity:0}}}}
.found{{animation:found {period}s linear infinite}}
@keyframes found{{0%,37%{{opacity:0}}40%,100%{{opacity:1}}}}
.drift{{animation:drift 24s linear infinite}}
@keyframes drift{{to{{transform:translateX(-300px)}}}}
.rec{{animation:rec 1.4s steps(1) infinite}}
@keyframes rec{{50%{{opacity:.2}}}}
"""
    defs = ('<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">'
            '<stop offset="0" stop-color="#08101F"/><stop offset="1" stop-color="#12305A"/></linearGradient>'
            '<filter id="blur" x="-50%" y="-200%" width="200%" height="500%"><feGaussianBlur stdDeviation="6"/></filter>')
    path = "M-260 128 C80 76 360 50 700 58"
    motion = f'<animateMotion dur="{period}s" repeatCount="indefinite" path="{path}"/>'
    corners = "M-30 -12V-22H-20M20 -22H30V-12M30 12V22H20M-20 22H-30V12"
    clouds = "".join(
        f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="7" fill="#9CC4FF" opacity=".07" filter="url(#blur)"/>'
        for x, y, rx in ((90, 116, 90), (380, 92, 120), (620, 132, 100), (860, 104, 90))
    )
    stars = "".join(f'<circle cx="{x}" cy="{y}" r="1" fill="#CFE3FF" opacity=".35"/>'
                    for x, y in ((40, 40), (132, 22), (210, 60), (300, 18), (455, 34), (540, 70), (570, 20), (260, 110)))
    plane = ('<path d="M15 0L9 -1.8L2 -1.8L-4 -12L-7.5 -12L-3.5 -1.8L-10 -1.8L-13 -6L-15.5 -6L-14 0L-15.5 6L-13 6'
             f'L-10 1.8L-3.5 1.8L-7.5 12L-4 12L2 1.8L9 1.8Z" fill="{TEXT}"/>')
    parts = f"""
<rect width="600" height="160" fill="url(#sky)"/>
{stars}
<g class="drift">{clouds}</g>
<g>{motion}
{plane}
<path class="lock" d="{corners}" fill="none" stroke="{AMBER}" stroke-width="2"/>
<g class="seek"><rect x="38" y="-34" width="158" height="21" rx="4" fill="{BG}" fill-opacity=".85" stroke="{AMBER}" stroke-opacity=".6"/>
<text class="mono" x="46" y="-19" font-size="11.5" fill="{AMBER}">AIRCRAFT · CONF 0.91</text></g>
<g class="found"><rect x="38" y="-34" width="180" height="21" rx="4" fill="{BG}" fill-opacity=".85" stroke="{GREEN}" stroke-opacity=".6"/>
<text class="mono" x="46" y="-19" font-size="11.5" fill="{GREEN}">BAW283 · A350 · MATCHED</text></g>
</g>
<text class="mono" x="20" y="28" font-size="11.5" letter-spacing="1.1" fill="{MUTED}">CAM 01 · LOCAL INFERENCE</text>
<circle class="rec" cx="534" cy="24" r="4" fill="{RED}"/>
<text class="mono" x="580" y="28" text-anchor="end" font-size="11.5" letter-spacing="1.1" fill="{MUTED}">REC</text>
<text class="mono" x="20" y="148" font-size="11.5" letter-spacing="1.1" fill="{MUTED}">VISION TRACK ↔ ADS-B FLIGHT</text>
"""
    return card(
        "SkyTrack", "COMPUTER VISION · RUNS LOCALLY",
        ["Point a camera at the sky. It detects and tracks aircraft, then",
         "works out which real flights they are. No cloud, no upload."],
        ["Python", "YOLO", "OpenCV", "FastAPI", "ADS-B"], False, parts, css, defs,
        alt="SkyTrack: detects and tracks aircraft from a camera, then matches each one to a real flight using "
            "ADS-B. Runs entirely locally.",
    )


def card_safesite() -> str:
    period = 7
    xs = (100, 240, 380)
    scan_end = .42  # fraction of the loop the scan line takes to cross
    css = [
        f".scan{{animation:scan {period}s cubic-bezier(.4,0,.6,1) infinite}}",
        f"@keyframes scan{{0%{{transform:translateX(0);opacity:1}}{scan_end * 100:.0f}%{{transform:translateX(436px);opacity:1}}"
        f"{scan_end * 100 + 4:.0f}%,100%{{transform:translateX(436px);opacity:0}}}}",
    ]
    people = [  # vest colour, box colour, tag, log line
        ("#FF7A1A", GREEN, "MARSHAL ✓", "✓ marshal hi-vis"),
        (None, RED, "NO HI-VIS ✕", "✕ case 0147 opened"),
        ("driver", GREEN, "DRIVER ✓", "✓ driver logo"),
    ]
    parts = [
        f'<path d="M0 146.5H436" stroke="{LINE}"/>',
        f'<path d="M0 154H436" stroke="{AMBER}" stroke-opacity=".35" stroke-width="3" stroke-dasharray="18 12"/>',
        f'<rect x="444" y="16" width="140" height="128" rx="8" fill="{PANEL}" stroke="{LINE}"/>',
        f'<text class="mono" x="456" y="37" font-size="11" letter-spacing="1.1" fill="{DIM}">CASE LOG</text>',
    ]
    for i, (x, (vest, color, tag, log)) in enumerate(zip(xs, people)):
        seen = (x + 20) / 436 * scan_end
        start, stop = seen * 100, 93
        css += [
            f".b{i}{{animation:b{i} {period}s linear infinite both}}",
            f"@keyframes b{i}{{0%,{start:.2f}%{{opacity:0}}{start + 2:.2f}%,{stop}%{{opacity:1}}{stop + 3}%,100%{{opacity:0}}}}",
            f".l{i}{{animation:l{i} {period}s linear infinite both}}",
            f"@keyframes l{i}{{0%,{start + 4:.2f}%{{opacity:0;transform:translateY(6px)}}{start + 8:.2f}%,{stop}%"
            f"{{opacity:1;transform:none}}{stop + 3}%,100%{{opacity:0}}}}",
        ]
        shirt = "#1F4E8C" if vest == "driver" else "#2A3A57"
        parts.append(f'<circle cx="{x}" cy="68" r="10" fill="#3A4B6B"/>'
                     f'<rect x="{x - 17}" y="82" width="34" height="64" rx="12" fill="{shirt}"/>')
        if vest == "driver":
            parts.append(f'<circle cx="{x + 7}" cy="96" r="3.5" fill="{TEXT}" opacity=".85"/>')
        elif vest:
            parts.append(f'<rect x="{x - 13}" y="86" width="26" height="40" rx="5" fill="{vest}"/>'
                         f'<path d="M{x - 13} 102H{x + 13}M{x - 13} 112H{x + 13}" stroke="#E8F0FF" stroke-opacity=".8" stroke-width="2.5"/>')
        tw = len(tag) * 11 * MONO_W + 12
        parts.append(
            f'<g class="b{i}"><rect x="{x - 36}" y="48" width="72" height="98" rx="3" fill="{color}" fill-opacity=".06" '
            f'stroke="{color}" stroke-width="1.5"/>'
            f'<rect x="{x - 36}" y="30" width="{tw:.1f}" height="18" rx="2" fill="{color}"/>'
            f'<text class="mono" x="{x - 30}" y="43" font-size="11" font-weight="700" fill="{BG}">{esc(tag)}</text></g>'
        )
        parts.append(f'<text class="mono l{i}" x="456" y="{64 + i * 26}" font-size="11" fill="{color}">{esc(log)}</text>')
    parts.append(
        f'<g class="scan"><rect x="-26" y="0" width="26" height="146" fill="url(#scanfade)"/>'
        f'<path d="M0.5 0V146" stroke="{SKY}" stroke-width="1.5"/></g>'
        f'<text class="mono" x="16" y="20" font-size="11.5" letter-spacing="1.1" fill="{MUTED}">CAM 03 · BADGE FIRST, VISION SECOND</text>'
    )
    defs = (f'<linearGradient id="scanfade" x1="0" x2="1"><stop offset="0" stop-color="{SKY}" stop-opacity="0"/>'
            f'<stop offset="1" stop-color="{SKY}" stop-opacity=".25"/></linearGradient>')
    return card(
        "SafeSite", "COMPUTER VISION · WAREHOUSE OPS",
        ["Role-aware uniform compliance: vision checks each person",
         "against their badge-scan role and logs cases for review."],
        ["Python", "YOLOv8", "OpenCV", "SQLite", "Streamlit"], False, "".join(parts), "\n".join(css), defs,
        alt="SafeSite: role-aware uniform compliance for warehouse operations. Computer vision checks each person "
            "against their badge-scan role and opens a case for a supervisor when they do not comply.",
    )


# ---------------------------------------------------------------- toolbox

def toolbox() -> str:
    W = 1200
    rows = [
        ("CODE & DATA", SKY, ["Python", "SQL", "MATLAB", "C++", "TypeScript", "DuckDB", "Polars", "FastAPI"]),
        ("ML & VISION", GREEN, ["YOLOv8", "OpenCV", "scikit-learn", "XGBoost", "ResNet-18", "LLM grounding"]),
        ("CAD & DESIGN", AMBER, ["SolidWorks", "Onshape", "Fusion 360", "AutoCAD", "GD&T", "Parametric modelling"]),
        ("SIMULATION", "#B18CFF", ["ABAQUS", "Ansys Mechanical", "Ansys Fluent", "Simulink", "Mesh convergence"]),
    ]
    top, step = 30, 54
    H = top * 2 + step * (len(rows) - 1) + 34
    css = """
.in{animation:in .7s cubic-bezier(.16,1,.3,1) both}
@keyframes in{from{opacity:0;transform:translateX(-10px)}}
"""
    body = [f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="16" fill="{PANEL}" stroke="{LINE}"/>']
    for r, (label, color, items) in enumerate(rows):
        y = top + r * step
        body.append(f'<g class="in" style="animation-delay:{r * .12:.2f}s"><rect x="32" y="{y + 12}" width="10" height="10" rx="2" fill="{color}"/>'
                    f'<text class="mono" x="54" y="{y + 22}" font-size="12.5" letter-spacing="1.5" fill="{MUTED}">{esc(label)}</text></g>')
        x = 234
        for i, item in enumerate(items):
            c, w = chip(x, y, item, size=14, h=34, pad=13,
                        attrs=f'class="in" style="animation-delay:{.15 + r * .12 + i * .05:.2f}s"')
            body.append(c)
            x += w + 10
    alt = "Toolbox. " + " ".join(f"{label.title()}: {', '.join(items)}." for label, _, items in rows)
    return document(W, H, alt, "\n".join(body), css)


# ---------------------------------------------------------------- footer

def footer() -> str:
    W, H = 1200, 170
    y = 128
    route = f"M110 {y}H1090"
    css = """
.march{animation:march 1.2s linear infinite}
@keyframes march{to{stroke-dashoffset:-24}}
.ping{transform-box:fill-box;transform-origin:center;animation:ping 2.4s ease-out infinite}
@keyframes ping{0%{opacity:.8;transform:scale(1)}80%,100%{opacity:0;transform:scale(3.2)}}
"""
    motion = ('<animateMotion dur="5s" repeatCount="indefinite" path="' + route + '" '
              'keyPoints="0;1;1" keyTimes="0;.8;1" calcMode="spline" keySplines=".6 0 .4 1;0 0 1 1"/>')
    body = f"""
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="16" fill="{PANEL}" stroke="{LINE}"/>
<text x="{W / 2}" y="58" text-anchor="middle" font-size="26" font-weight="700" letter-spacing="-.3" fill="{TEXT}">Let’s build something that runs on real data.</text>
<text class="mono" x="{W / 2}" y="88" text-anchor="middle" font-size="13" letter-spacing="1" fill="{MUTED}">linkedin.com/in/jamal-lharri   ·   jamal-lharri-portfolio.vercel.app</text>
<path class="march" d="{route}" stroke="{SKY}" stroke-opacity=".45" stroke-width="2" stroke-dasharray="12 12"/>
<circle class="ping" cx="110" cy="{y}" r="6" fill="{SKY}"/>
<circle cx="110" cy="{y}" r="6" fill="{BG}" stroke="{SKY}" stroke-width="2.5"/>
<circle class="ping" style="animation-delay:1.2s" cx="1090" cy="{y}" r="6" fill="{AMBER}"/>
<rect x="1080" y="{y - 10}" width="20" height="20" rx="5" fill="{AMBER}"/>
<circle r="9" fill="{AMBER}" opacity=".5">{motion}</circle>
<circle r="4.5" fill="{AMBER}">{motion}</circle>
<text class="mono" x="110" y="{y + 30}" text-anchor="middle" font-size="11" letter-spacing="1.2" fill="{DIM}">YOUR TEAM</text>
<text class="mono" x="1090" y="{y + 30}" text-anchor="middle" font-size="11" letter-spacing="1.2" fill="{DIM}">DELIVERED</text>
"""
    return document(W, H, "Let's build something that runs on real data. linkedin.com/in/jamal-lharri", body, css)


ASSETS = {
    "hero.svg": hero,
    "terminal.svg": terminal,
    "numbers.svg": numbers,
    "card-motintel.svg": card_motintel,
    "card-radarscope.svg": card_radarscope,
    "card-skytrack.svg": card_skytrack,
    "card-safesite.svg": card_safesite,
    "toolbox.svg": toolbox,
    "footer.svg": footer,
}

if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for name, build in ASSETS.items():
        (OUT / name).write_text(build(), encoding="utf-8")
        print(f"{name:22} {(OUT / name).stat().st_size / 1024:5.1f} KB")
