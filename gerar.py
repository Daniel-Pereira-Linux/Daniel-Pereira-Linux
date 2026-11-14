#!/usr/bin/env python3
"""Gera os SVGs animados do perfil. Só biblioteca padrão.

  python3 gerar.py                  tudo; a atividade vem da API do GitHub (GITHUB_TOKEN)
  python3 gerar.py --dados arq.json usa um calendário já baixado (teste local)
"""
import datetime
import html
import json
import math
import os
import random
import sys
import urllib.request

LOGIN = os.environ.get("PERFIL", "Daniel-Pereira-Linux")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")

BG0, BG1, CARD = "#05070f", "#0a1124", "#090e1c"
TEAL, BLUE, VIOLET = "#00f0c8", "#2d7ff9", "#8b5cf6"
TXT, MUT, LINE = "#e8eefc", "#7c8aa8", "#1a2542"
MONO = "ui-monospace,SFMono-Regular,'JetBrains Mono',Menlo,Consolas,'Liberation Mono',monospace"
SANS = "system-ui,-apple-system,'Segoe UI',Inter,Roboto,Helvetica,Arial,sans-serif"
MESES = "jan fev mar abr mai jun jul ago set out nov dez".split()


def esc(s):
    return html.escape(s, quote=True)


def mono_w(s, size):
    """Largura de um texto monoespaçado; fixada com textLength para ser igual em todo sistema."""
    return round(len(s) * size * 0.6, 1)


def save(name, svg):
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(svg.strip() + "\n")


def hexagon(r, rot=0):
    return " ".join(f"{r * math.cos(math.radians(60 * i + rot)):.1f},{r * math.sin(math.radians(60 * i + rot)):.1f}"
                    for i in range(6))


# ------------------------------------------------------------------ topo

def hero():
    W, H, HZ = 1200, 440, 318
    rnd = random.Random(7)
    stars = "".join(
        f'<circle class="st" cx="{rnd.uniform(20, 1180):.0f}" cy="{rnd.uniform(14, HZ - 20):.0f}" '
        f'r="{rnd.uniform(.5, 1.7):.1f}" style="animation-delay:-{rnd.uniform(0, 5):.1f}s"/>' for _ in range(54))
    rays = "".join(f'<line x1="{600 + k * 16}" y1="{HZ}" x2="{600 + k * 150}" y2="{H}"/>' for k in range(-14, 15))
    floor = "".join(f'<line class="hz" x1="0" x2="{W}" y1="{HZ}" y2="{HZ}" style="animation-delay:-{i * .5:.1f}s"/>'
                    for i in range(9))

    frases = ["mantenedor da documentação em português do kernel Linux",
              "criador do MilizOS, o Linux em que tudo é commit",
              "engenheiro de sistemas"]
    n, slot = len(frases), 4
    dur = n * slot
    typed = ""
    for i, f in enumerate(frases):
        w = mono_w(f, 22)
        kt = "0;{:.4f};{:.4f};{:.4f};1".format(.42 / n, .86 / n, .999 / n)
        typed += (
            f'<g opacity="0"><animate attributeName="opacity" values="1;1;0;0" keyTimes="0;{.999 / n:.4f};{1 / n:.4f};1" '
            f'dur="{dur}s" begin="{i * slot}s" repeatCount="indefinite"/>'
            f'<clipPath id="c{i}"><rect x="100" y="218" height="34" width="0">'
            f'<animate attributeName="width" values="0;{w};{w};0;0" keyTimes="{kt}" dur="{dur}s" begin="{i * slot}s" '
            f'repeatCount="indefinite"/></rect></clipPath>'
            f'<text x="100" y="242" class="ty" textLength="{w}" lengthAdjust="spacingAndGlyphs" clip-path="url(#c{i})">{esc(f)}</text>'
            f'<rect y="222" width="11" height="24" fill="{TEAL}" class="cur" x="100">'
            f'<animate attributeName="x" values="104;{104 + w};{104 + w};104;104" keyTimes="{kt}" dur="{dur}s" '
            f'begin="{i * slot}s" repeatCount="indefinite"/></rect></g>')

    chips, x = "", 72
    for c in ["kernel docs pt_BR", "git l10n", "CloudStack", "btrfs", "Rust", "Python", "Shell"]:
        tw = mono_w(c, 14)
        chips += (f'<rect x="{x}" y="270" width="{tw + 26}" height="28" rx="14" class="chip"/>'
                  f'<text x="{x + 13}" y="289" class="ct" textLength="{tw}" lengthAdjust="spacingAndGlyphs">{esc(c)}</text>')
        x += tw + 36

    who = "daniel@kernel:~$ whoami"
    save("hero.svg", f'''
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img"
 aria-label="Daniel Pereira: mantenedor da documentação em português do kernel Linux e criador do MilizOS">
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{BG0}"/><stop offset="1" stop-color="{BG1}"/></linearGradient>
<radialGradient id="g1" cx="18%" cy="8%" r="60%"><stop offset="0" stop-color="{TEAL}" stop-opacity=".16"/><stop offset="1" stop-color="{TEAL}" stop-opacity="0"/></radialGradient>
<radialGradient id="g2" cx="84%" cy="38%" r="46%"><stop offset="0" stop-color="{BLUE}" stop-opacity=".30"/><stop offset="1" stop-color="{BLUE}" stop-opacity="0"/></radialGradient>
<linearGradient id="hz" x1="0" x2="1"><stop offset="0" stop-color="{TEAL}" stop-opacity="0"/><stop offset=".3" stop-color="{TEAL}"/><stop offset=".65" stop-color="{BLUE}"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></linearGradient>
<linearGradient id="fade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{BG1}"/><stop offset="1" stop-color="{BG1}" stop-opacity="0"/></linearGradient>
<linearGradient id="nm" gradientUnits="userSpaceOnUse" x1="0" x2="1200" y1="0" y2="0">
<stop offset="0" stop-color="#fff"/><stop offset=".42" stop-color="#fff"/><stop offset=".5" stop-color="{TEAL}"/><stop offset=".58" stop-color="#fff"/><stop offset="1" stop-color="#fff"/>
<animateTransform attributeName="gradientTransform" type="translate" values="-640 0;460 0;460 0" keyTimes="0;.55;1" dur="7s" repeatCount="indefinite"/></linearGradient>
<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<clipPath id="r"><rect width="{W}" height="{H}" rx="20"/></clipPath>
</defs>
<style>
.st{{fill:#cfe0ff;animation:tw 5s ease-in-out infinite}}
@keyframes tw{{0%,100%{{opacity:.12}}50%{{opacity:.95}}}}
.rays line{{stroke:{BLUE};stroke-opacity:.34;stroke-width:1}}
.hz{{stroke:{TEAL};stroke-opacity:.55;stroke-width:1.2;animation:fl 4.5s cubic-bezier(.55,0,1,.45) infinite}}
@keyframes fl{{0%{{transform:translateY(0);opacity:0}}12%{{opacity:1}}100%{{transform:translateY({H - HZ + 6}px);opacity:1}}}}
.who{{font:500 16px {MONO};fill:{TEAL}}}
.nm{{font:800 78px {SANS};letter-spacing:-2.5px;fill:url(#nm)}}
.pr{{font:700 22px {MONO};fill:{TEAL}}}
.ty{{font:500 22px {MONO};fill:{TXT}}}
.cur{{animation:bl 1s steps(1) infinite}}
@keyframes bl{{50%{{opacity:0}}}}
.chip{{fill:#0c1428;stroke:{LINE};stroke-width:1.2}}
.ct{{font:500 14px {MONO};fill:#9db0d6}}
.ring{{fill:none;stroke-linejoin:round}}
.core{{animation:pu 3.2s ease-in-out infinite}}
@keyframes pu{{0%,100%{{opacity:.35}}50%{{opacity:1}}}}
</style>
<g clip-path="url(#r)">
<rect width="{W}" height="{H}" fill="url(#bg)"/>
<rect width="{W}" height="{H}" fill="url(#g1)"/><rect width="{W}" height="{H}" fill="url(#g2)"/>
{stars}
<g class="rays">{rays}</g>
{floor}
<rect y="{HZ}" width="{W}" height="{H - HZ}" fill="url(#fade)"/>
<rect y="{HZ - 1}" width="{W}" height="2" fill="url(#hz)" filter="url(#glow)"/>

<g transform="translate(1000,162)" filter="url(#glow)">
<g><animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="46s" repeatCount="indefinite"/>
<polygon class="ring" points="{hexagon(118)}" stroke="{TEAL}" stroke-width="2" stroke-dasharray="46 16"/>
<circle cx="118" cy="0" r="4.5" fill="{TEAL}"/><circle cx="-59" cy="102.2" r="3" fill="{TEAL}"/></g>
<g><animateTransform attributeName="transform" type="rotate" from="360" to="0" dur="30s" repeatCount="indefinite"/>
<polygon class="ring" points="{hexagon(88, 30)}" stroke="{BLUE}" stroke-width="2.4" stroke-dasharray="6 10"/>
<circle cx="0" cy="-88" r="4" fill="{BLUE}"/></g>
<g><animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="18s" repeatCount="indefinite"/>
<polygon class="ring" points="{hexagon(58)}" stroke="{VIOLET}" stroke-width="2"/>
<circle cx="58" cy="0" r="3.5" fill="{VIOLET}"/></g>
<polygon class="core" points="{hexagon(26, 30)}" fill="{TEAL}"/>
</g>

<text x="72" y="96" class="who" textLength="{mono_w(who, 16)}" lengthAdjust="spacingAndGlyphs">{who}</text>
<text x="68" y="180" class="nm">Daniel Pereira</text>
<text x="72" y="242" class="pr">&gt;</text>
{typed}
{chips}
</g>
</svg>''')


# ------------------------------------------------------------------ cartões

def card(name, title, lang, color, lines, foot, accent=TEAL):
    W, H = 600, 250
    per = 2 * (W - 4 + H - 4)
    body = "".join(f'<text x="34" y="{118 + i * 25}" class="d">{esc(l)}</text>' for i, l in enumerate(lines))
    lw = mono_w(lang, 14)
    fw = mono_w(foot, 14)
    save(name, f'''
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{esc(title)}">
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0b1224"/><stop offset="1" stop-color="{BG0}"/></linearGradient>
<radialGradient id="gl" cx="100%" cy="0%" r="75%"><stop offset="0" stop-color="{accent}" stop-opacity=".22"/><stop offset="1" stop-color="{accent}" stop-opacity="0"/></radialGradient>
<linearGradient id="sw" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".06"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<filter id="glow" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="3.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<clipPath id="r"><rect x="2" y="2" width="{W - 4}" height="{H - 4}" rx="18"/></clipPath>
</defs>
<style>
.t{{font:800 30px {SANS};fill:#fff;letter-spacing:-.6px}}
.d{{font:400 17px {SANS};fill:#a9b7d6}}
.l{{font:500 14px {MONO};fill:#c5d2ee}}
.f{{font:500 14px {MONO};fill:{accent}}}
.run{{fill:none;stroke:{accent};stroke-width:2.6;stroke-linecap:round;stroke-dasharray:150 {per - 150};animation:run 6s linear infinite}}
@keyframes run{{to{{stroke-dashoffset:-{per}}}}}
.sw{{animation:sw 6s ease-in-out infinite}}
@keyframes sw{{0%,55%{{transform:translateX(-320px)}}100%{{transform:translateX({W + 40}px)}}}}
.hx{{animation:pu 3s ease-in-out infinite}}
@keyframes pu{{0%,100%{{opacity:.45}}50%{{opacity:1}}}}
</style>
<rect x="2" y="2" width="{W - 4}" height="{H - 4}" rx="18" fill="url(#bg)" stroke="{LINE}" stroke-width="1.5"/>
<g clip-path="url(#r)"><rect width="{W}" height="{H}" fill="url(#gl)"/>
<rect class="sw" x="0" y="0" width="260" height="{H}" fill="url(#sw)" transform="skewX(-18)"/></g>
<rect class="run" x="2" y="2" width="{W - 4}" height="{H - 4}" rx="18" filter="url(#glow)"/>
<g transform="translate(50,56)" filter="url(#glow)"><polygon class="hx" points="{hexagon(15, 30)}" fill="none" stroke="{accent}" stroke-width="2.4"/>
<polygon points="{hexagon(6, 30)}" fill="{accent}"/></g>
<text x="80" y="67" class="t">{esc(title)}</text>
<circle cx="{W - 46 - lw}" cy="57" r="5.5" fill="{color}"/>
<text x="{W - 34 - lw}" y="62" class="l" textLength="{lw}" lengthAdjust="spacingAndGlyphs">{esc(lang)}</text>
{body}
<text x="34" y="{H - 28}" class="f" textLength="{fw}" lengthAdjust="spacingAndGlyphs">{esc(foot)}</text>
</svg>''')


def cards():
    card("card-milizos.svg", "MilizOS", "Python", "#3572a5",
         ["O Linux em que tudo é commit. Distribuição baseada",
          "em Fedora em que a máquina inteira tem histórico:",
          "sistema, arquivos e logs voltam a qualquer ponto."],
         "→ milizos.com.br", TEAL)
    card("card-maloki.svg", "maloki", "Rust", "#dea584",
         ["Transforma o Linux que está rodando, sem os dados",
          "pessoais, em um template QEMU ou em uma ISO",
          "instalável. BIOS, UEFI e Secure Boot."],
         "→ github.com/Daniel-Pereira-Linux/maloki", "#ff9d5c")
    card("card-kernelbase.svg", "Kernelbase", "HTML", "#e34c26",
         ["A documentação do kernel Linux em português,",
          "centralizada em um lugar só para quem está",
          "começando e para quem já contribui."],
         "→ github.com/Daniel-Pereira-Linux/Kernelbase", BLUE)
    card("card-upstream.svg", "Upstream", "patches", VIOLET,
         ["Linux kernel: mantenedor da documentação pt_BR.",
          "git-l10n/git-po: tradução do Git.",
          "apache/cloudstack: correções e backports."],
         "→ contribuições em outros projetos", VIOLET)


# ------------------------------------------------------------------ divisor e botões

def divider():
    W, H, Y = 1200, 70, 35
    paths = [f"M20,{Y} H1180",
             f"M250,{Y} C290,{Y} 290,12 330,12 H560 C600,12 600,{Y} 640,{Y}",
             f"M720,{Y} C760,{Y} 760,58 800,58 H980 C1020,58 1020,{Y} 1060,{Y}"]
    nodes = [(x, Y) for x in range(70, 1180, 90)] + [(x, 12) for x in (380, 470, 540)] + [(x, 58) for x in (840, 930)]
    dots = "".join(f'<circle class="n" cx="{x}" cy="{y}" r="5" style="animation-delay:{(x - 20) / 1160 * 7 - 7:.2f}s"/>'
                   for x, y in nodes)
    lines = "".join(f'<path class="p" d="{p}"/>' for p in paths)
    movers = "".join(
        f'<circle r="{r}" fill="{c}" filter="url(#glow)"><animateMotion dur="7s" repeatCount="indefinite" path="{p}" '
        f'keyPoints="{kp}" keyTimes="{kt}" calcMode="linear"/></circle>'
        for p, c, r, kp, kt in [
            (paths[0], TEAL, 5, "0;1", "0;1"),
            (paths[1], BLUE, 4, "0;0;1;1", f"0;{230 / 1160:.3f};{620 / 1160:.3f};1"),
            (paths[2], VIOLET, 4, "0;0;1;1", f"0;{700 / 1160:.3f};{1040 / 1160:.3f};1")])
    save("linha.svg", f'''
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="presentation">
<defs><filter id="glow" x="-300%" y="-300%" width="700%" height="700%"><feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
<style>
.p{{fill:none;stroke:#263765;stroke-width:2}}
.n{{fill:{BG0};stroke:#3b5391;stroke-width:2;animation:n 7s linear infinite}}
@keyframes n{{0%{{stroke:{TEAL};fill:{TEAL}}}7%{{stroke:#3b5391;fill:{BG0}}}100%{{stroke:#3b5391;fill:{BG0}}}}}
</style>
{lines}{dots}{movers}
</svg>''')


def button(name, label, accent):
    tw = mono_w(label, 16)
    W, H = tw + 64, 48
    per = 2 * (W - 4 + H - 4)
    save(name, f'''
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{esc(label)}">
<style>
.t{{font:600 16px {MONO};fill:{TXT}}}
.run{{fill:none;stroke:{accent};stroke-width:2.2;stroke-linecap:round;stroke-dasharray:60 {per - 60:.0f};animation:run 4s linear infinite}}
@keyframes run{{to{{stroke-dashoffset:-{per:.0f}}}}}
</style>
<rect x="2" y="2" width="{W - 4}" height="{H - 4}" rx="22" fill="{CARD}" stroke="{LINE}" stroke-width="1.5"/>
<rect class="run" x="2" y="2" width="{W - 4}" height="{H - 4}" rx="22"/>
<circle cx="24" cy="{H / 2}" r="4.5" fill="{accent}"/>
<text x="40" y="{H / 2 + 5.5}" class="t" textLength="{tw}" lengthAdjust="spacingAndGlyphs">{esc(label)}</text>
</svg>''')


# ------------------------------------------------------------------ atividade

QUERY = """query($login:String!){user(login:$login){contributionsCollection{contributionCalendar{
totalContributions weeks{contributionDays{date contributionCount weekday}}}}}}"""


def fetch():
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": LOGIN}}).encode(),
        headers={"Authorization": "bearer " + os.environ["GITHUB_TOKEN"], "User-Agent": "perfil"})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    if data.get("errors"):
        raise SystemExit("API do GitHub: " + json.dumps(data["errors"]))
    return data


def shade(hexc, k):
    r, g, b = (int(hexc[i:i + 2], 16) for i in (1, 3, 5))
    return "#%02x%02x%02x" % tuple(max(0, min(255, round(v * k))) for v in (r, g, b))


def activity(data):
    cal = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    weeks = cal["weeks"]
    days = [d for w in weeks for d in w["contributionDays"]]
    counts = [d["contributionCount"] for d in days]
    total, peak = cal["totalContributions"], max(counts + [1])
    active = sum(1 for c in counts if c)
    best = cur = run = 0
    for c in counts:
        run = run + 1 if c else 0
        best = max(best, run)
    tail = counts[:-1] if counts and counts[-1] == 0 else counts      # hoje ainda pode não ter commit
    for c in reversed(tail):
        if not c:
            break
        cur += 1
    pk = max(days, key=lambda d: d["contributionCount"])
    pkd = datetime.date.fromisoformat(pk["date"])

    W, H = 1200, 560
    HW, HH, OX, OY, K = 13, 6.5, 420, 122, .84
    palette = ["#13407a", "#1767c8", "#12a9cf", TEAL]

    def level(c):
        return min(3, int(4 * (c / peak) ** .55 - 1e-9))

    cells = sorted(((wi, d["weekday"], d) for wi, w in enumerate(weeks) for d in w["contributionDays"]),
                   key=lambda t: (t[0] + t[1], t[0]))
    tiles, bars, beacon = [], [], ""
    for wi, wd, d in cells:
        c = d["contributionCount"]
        cx, cy = OX + (wi - wd) * HW, OY + (wi + wd) * HH + HH
        a, b = HW * K, HH * K

        def top(h):
            return f"{cx:.1f},{cy - b - h:.1f} {cx + a:.1f},{cy - h:.1f} {cx:.1f},{cy + b - h:.1f} {cx - a:.1f},{cy - h:.1f}"
        if not c:
            tiles.append(f'<polygon points="{top(0)}"/>')
            continue
        h = 7 + 86 * (c / peak) ** .6
        col = palette[level(c)]
        def left(h):
            return f"{cx - a:.1f},{cy - h:.1f} {cx:.1f},{cy + b - h:.1f} {cx:.1f},{cy + b:.1f} {cx - a:.1f},{cy:.1f}"

        def right(h):
            return f"{cx + a:.1f},{cy - h:.1f} {cx:.1f},{cy + b - h:.1f} {cx:.1f},{cy + b:.1f} {cx + a:.1f},{cy:.1f}"

        # subida em SMIL nos próprios pontos: a animação CSS de escala sumia com barras no Chrome
        delay = .25 + wi * .03
        kt = f"0;{delay / (delay + 1.1):.3f};1"

        def poly(shape, fill, cls=""):
            return (f'<polygon{cls} points="{shape(h)}" fill="{fill}"><animate attributeName="points" '
                    f'values="{shape(0)};{shape(0)};{shape(h)}" keyTimes="{kt}" dur="{delay + 1.1:.2f}s" '
                    f'calcMode="spline" keySplines="0 0 1 1;.2 .9 .25 1" fill="freeze"/></polygon>')
        bars.append(
            f'<g><title>{d["date"]}: {c}</title>'
            + poly(left, shade(col, .62)) + poly(right, shade(col, .40)) + poly(top, col)
            + f'<polygon class="w" points="{top(h)}" style="animation-delay:{wi * .09 - 7:.2f}s"/></g>')
        if d is pk:
            ty = cy - h
            beacon = (f'<g class="bc"><line x1="{cx:.1f}" y1="{ty:.1f}" x2="{cx:.1f}" y2="{ty - 62:.1f}" stroke="url(#beam)" stroke-width="2"/>'
                      f'<circle cx="{cx:.1f}" cy="{ty - 62:.1f}" r="4" fill="{TEAL}" filter="url(#glow)"/>'
                      f'<circle class="rg" cx="{cx:.1f}" cy="{ty - 62:.1f}" r="4"/>'
                      f'<text x="{cx + 12:.1f}" y="{ty - 58:.1f}" class="pk">pico · {c} em {pkd.day} {MESES[pkd.month - 1]}</text></g>')

    months, seen = "", None
    for wi, w in enumerate(weeks):
        first = datetime.date.fromisoformat(w["contributionDays"][0]["date"])
        if first.month != seen and len(w["contributionDays"]) == 7:
            seen = first.month
            x, y = OX + (wi - 7.7) * HW, OY + (wi + 7.7) * HH + HH + 4
            months += f'<text x="{x:.1f}" y="{y:.1f}" class="mo" text-anchor="end">{MESES[first.month - 1]}</text>'
        elif seen is None:
            seen = first.month

    def stat(y, label, value):
        return (f'<text x="60" y="{y}" class="sl">{label}</text>'
                f'<text x="372" y="{y}" class="sv" text-anchor="end">{value}</text>'
                f'<line x1="60" x2="372" y1="{y + 11}" y2="{y + 11}" class="sr"/>')

    def plural(n, um, varios):
        return f"{n} {um if n == 1 else varios}"

    legend = "".join(f'<rect x="{1010 + i * 22}" y="76" width="16" height="16" rx="4" fill="{c}"/>'
                     for i, c in enumerate(["#0e1528"] + palette))
    save("atividade.svg", f'''
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img"
 aria-label="{total} contribuições nos últimos 12 meses; maior sequência de {best} dias">
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{BG0}"/><stop offset="1" stop-color="{BG1}"/></linearGradient>
<radialGradient id="g1" cx="62%" cy="55%" r="55%"><stop offset="0" stop-color="{BLUE}" stop-opacity=".20"/><stop offset="1" stop-color="{BLUE}" stop-opacity="0"/></radialGradient>
<linearGradient id="beam" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="{TEAL}" stop-opacity="0"/><stop offset="1" stop-color="{TEAL}"/></linearGradient>
<linearGradient id="num" x1="0" x2="1"><stop offset="0" stop-color="{TEAL}"/><stop offset="1" stop-color="{BLUE}"/></linearGradient>
<filter id="glow" x="-200%" y="-200%" width="500%" height="500%"><feGaussianBlur stdDeviation="5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="soft" x="-20%" y="-40%" width="140%" height="180%"><feGaussianBlur stdDeviation="9" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>
<style>
.z polygon{{fill:#0e1528}}
.w{{fill:#fff;opacity:0;animation:wv 7s linear infinite}}
@keyframes wv{{0%{{opacity:0}}4%{{opacity:.6}}10%{{opacity:0}}100%{{opacity:0}}}}
.h{{font:500 16px {MONO};fill:{TEAL}}}
.big{{font:800 96px {SANS};letter-spacing:-4px;fill:url(#num)}}
.cap{{font:500 15px {MONO};fill:{MUT}}}
.sl{{font:400 15px {MONO};fill:{MUT}}}
.sv{{font:700 15px {MONO};fill:{TXT}}}
.sr{{stroke:{LINE};stroke-width:1}}
.mo{{font:500 12px {MONO};fill:#55658c}}
.pk{{font:600 13px {MONO};fill:{TEAL}}}
.lg{{font:500 12px {MONO};fill:{MUT}}}
.bc{{animation:in 1s ease-out 1.6s both}}
@keyframes in{{from{{opacity:0}}to{{opacity:1}}}}
.rg{{fill:none;stroke:{TEAL};stroke-width:1.5;transform-box:fill-box;transform-origin:center;animation:rg 2.4s ease-out infinite}}
@keyframes rg{{from{{transform:scale(1);opacity:.9}}to{{transform:scale(5);opacity:0}}}}
</style>
<rect width="{W}" height="{H}" rx="20" fill="url(#bg)"/><rect width="{W}" height="{H}" rx="20" fill="url(#g1)"/>
<text x="60" y="74" class="h">$ git log --since="1 year ago" | wc -l</text>
<text x="1004" y="62" class="lg">menos</text><text x="1124" y="62" class="lg" text-anchor="end">mais</text>{legend}
<g class="z">{"".join(tiles)}</g>
{"".join(bars)}
{beacon}
{months}
<text x="54" y="362" class="big" filter="url(#soft)">{total}</text>
<text x="60" y="394" class="cap">contribuições nos últimos 12 meses</text>
{stat(440, "dias com atividade", active)}
{stat(474, "maior sequência", plural(best, "dia", "dias"))}
{stat(508, "sequência atual", plural(cur, "dia", "dias"))}
</svg>''')


def main():
    hero()
    cards()
    divider()
    button("btn-linkedin.svg", "LinkedIn", BLUE)
    button("btn-milizos.svg", "milizos.com.br", TEAL)
    if "--dados" in sys.argv:
        with open(sys.argv[sys.argv.index("--dados") + 1], encoding="utf-8") as f:
            data = json.load(f)
    elif os.environ.get("GITHUB_TOKEN"):
        data = fetch()
    else:
        print("sem GITHUB_TOKEN: atividade.svg não foi atualizado")
        return
    activity(data)


if __name__ == "__main__":
    main()
