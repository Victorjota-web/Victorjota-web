"""
gerar_assets.py: gera os SVGs 8-bit do README (banner, divisor, 'now playing' e skill tree).
Tudo é desenhado em pixels (retângulos), com animações em CSS. Nada depende de serviço externo.
Rodar a partir da pasta do projeto:  python tools/gerar_assets.py
Para mudar níveis de skill, textos ou cores, edite as seções marcadas com  >>> EDITE AQUI
"""
import math
import random

OUT = "assets/"

# ------------------------------------------------------------------ fonte pixel 5x7
G = {
 "A": [".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
 "B": ["####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."],
 "C": [".###.", "#...#", "#....", "#....", "#....", "#...#", ".###."],
 "D": ["####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."],
 "E": ["#####", "#....", "#....", "####.", "#....", "#....", "#####"],
 "F": ["#####", "#....", "#....", "####.", "#....", "#....", "#...."],
 "G": [".###.", "#...#", "#....", "#.###", "#...#", "#...#", ".###."],
 "H": ["#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
 "I": ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "#####"],
 "J": ["..###", "...#.", "...#.", "...#.", "...#.", "#..#.", ".##.."],
 "K": ["#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"],
 "L": ["#....", "#....", "#....", "#....", "#....", "#....", "#####"],
 "M": ["#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"],
 "N": ["#...#", "##..#", "#.#.#", "#..##", "#...#", "#...#", "#...#"],
 "O": [".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
 "P": ["####.", "#...#", "#...#", "####.", "#....", "#....", "#...."],
 "Q": [".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"],
 "R": ["####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"],
 "S": [".####", "#....", "#....", ".###.", "....#", "....#", "####."],
 "T": ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."],
 "U": ["#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
 "V": ["#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."],
 "W": ["#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"],
 "X": ["#...#", "#...#", ".#.#.", "..#..", ".#.#.", "#...#", "#...#"],
 "Y": ["#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."],
 "Z": ["#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"],
 "0": [".###.", "#...#", "#..##", "#.#.#", "##..#", "#...#", ".###."],
 "1": ["..#..", ".##..", "..#..", "..#..", "..#..", "..#..", ".###."],
 "2": [".###.", "#...#", "....#", "...#.", "..#..", ".#...", "#####"],
 "3": ["####.", "....#", "....#", ".###.", "....#", "....#", "####."],
 "4": ["...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."],
 "5": ["#####", "#....", "####.", "....#", "....#", "#...#", ".###."],
 "6": [".###.", "#....", "#....", "####.", "#...#", "#...#", ".###."],
 "7": ["#####", "....#", "...#.", "..#..", ".#...", ".#...", ".#..."],
 "8": [".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."],
 "9": [".###.", "#...#", "#...#", ".####", "....#", "....#", ".###."],
 ".": ["..", "..", "..", "..", "..", "##", "##"],
 ",": ["..", "..", "..", "..", "##", "#.", "#."],
 ":": ["..", "##", "##", "..", "##", "##", ".."],
 "-": ["....", "....", "....", "####", "....", "....", "...."],
 "/": ["....#", "....#", "...#.", "..#..", ".#...", "#....", "#...."],
 ">": ["#..", "#..", ".#.", "..#", ".#.", "#..", "#.."],
 "!": ["#", "#", "#", "#", "#", ".", "#"],
 " ": ["...", "...", "...", "...", "...", "...", "..."],
}


def text_width(txt, scale=1, gap=1):
    return sum(len(G[c][0]) + gap for c in txt) * scale - gap * scale


def pixel_text(txt, x, y, scale=1, color="#fff", gap=1, extra=""):
    """Desenha texto pixelado como retângulos (agrupa pixels vizinhos na mesma linha)."""
    rects, cx = [], x
    for ch in txt:
        glyph = G[ch]
        for r, row in enumerate(glyph):
            c = 0
            while c < len(row):
                if row[c] == "#":
                    start = c
                    while c < len(row) and row[c] == "#":
                        c += 1
                    rects.append(f'<rect x="{cx + start * scale}" y="{y + r * scale}" width="{(c - start) * scale}" height="{scale}"/>')
                else:
                    c += 1
        cx += (len(glyph[0]) + gap) * scale
    return f'<g fill="{color}" {extra}>' + "".join(rects) + "</g>"


def rect(x, y, w, h, fill, extra=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" {extra}/>'


def svg_wrap(w_units, h_units, scale, title, body, css, defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w_units * scale}" height="{h_units * scale}" '
            f'viewBox="0 0 {w_units} {h_units}" shape-rendering="crispEdges" role="img" aria-label="{title}">\n'
            f'<title>{title}</title>\n<defs>{defs}</defs>\n<style>{css}\n'
            '@media (prefers-reduced-motion: reduce){*{animation:none !important}}</style>\n'
            f'{body}\n</svg>\n')


# ------------------------------------------------------------------ paleta (lofi noturno)
SKY = ["#0b0720", "#120a2e", "#1a0f3d", "#25144f", "#331a5e", "#45206b",
       "#5a2874", "#733078", "#8d3a78", "#a64574", "#bf5570"]
LUA, LUA_SOMBRA = "#f4e7c5", "#d8c79f"
ROSA, LAVANDA, BRASA = "#ff9ecb", "#c9b6ff", "#f2a65a"
FOGO_VERM, FOGO_LAR, FOGO_AMA = "#e0452f", "#f08a2e", "#ffd75a"
CASCO, CASCO_ESC, MASTRO, VELA, VELA_QUEIMADA = "#6b4430", "#4a2e22", "#3a261c", "#d9c7a3", "#2b1a1a"


# ================================================================== 1) BANNER
def banner():
    W, H, HOR = 200, 64, 44          # largura, altura, linha do horizonte (unidades-pixel)
    rnd = random.Random(8)
    out, defs = [], []

    # céu em faixas com transição "dither" (xadrez) entre uma faixa e outra
    band_h = HOR // len(SKY)
    for i, cor in enumerate(SKY):
        y0 = i * band_h
        h = band_h if i < len(SKY) - 1 else HOR - y0
        out.append(rect(0, y0, W, h, cor))
        if i > 0:
            pid = f"dz{i}"
            defs.append(f'<pattern id="{pid}" width="2" height="2" patternUnits="userSpaceOnUse">'
                        f'<rect width="1" height="1" fill="{cor}"/><rect x="1" y="1" width="1" height="1" fill="{cor}"/></pattern>')
            out.append(rect(0, y0 - 1, W, 1, f"url(#{pid})"))

    # estrelas (fora da área do texto)
    def livre(x, y):
        return not (4 <= x <= 135 and 3 <= y <= 40)
    stars = []
    while len(stars) < 46:
        x, y = rnd.randint(1, W - 2), rnd.randint(1, 36)
        if livre(x, y) and (abs(x - 182) > 13 or abs(y - 14) > 13):
            stars.append((x, y))
    for i, (x, y) in enumerate(stars):
        cls = f"tw tw{i % 4}"
        cor = "#ffffff" if i % 3 else LAVANDA
        if i % 9 == 0:   # estrela maior em cruz
            out.append(f'<g class="{cls}" fill="{cor}">{rect(x, y - 1, 1, 3, cor)}{rect(x - 1, y, 3, 1, cor)}</g>')
        else:
            out.append(rect(x, y, 1, 1, cor, f'class="{cls}"'))

    # lua com brilho
    cx, cy, r = 182, 14, 8
    for rr, op in ((12, 0.07), (10, 0.10)):
        for y in range(cy - rr, cy + rr + 1):
            dx = int(math.sqrt(max(rr * rr - (y - cy) ** 2, 0)))
            out.append(rect(cx - dx, y, 2 * dx + 1, 1, LUA, f'opacity="{op}"'))
    for y in range(cy - r, cy + r + 1):
        dx = int(math.sqrt(max(r * r - (y - cy) ** 2, 0)))
        out.append(rect(cx - dx, y, 2 * dx + 1, 1, LUA))
    for (px, py, w) in ((-3, -3, 2), (2, -1, 3), (-2, 3, 2), (3, 4, 2), (-5, 0, 1)):   # crateras
        out.append(rect(cx + px, cy + py, w, 1, LUA_SOMBRA))
        out.append(rect(cx + px, cy + py + 1, max(w - 1, 1), 1, LUA_SOMBRA))

    # colinas distantes
    for x in range(W):
        h = 2 + int(1.6 * math.sin(x / 9.0) + 1.2 * math.sin(x / 4.3 + 1))
        h = max(1, min(h, 5))
        out.append(rect(x, HOR - h, 1, h, "#1d0f38"))

    # mar em faixas
    agua = ["#3a1d5e", "#2e1752", "#251245", "#1c0e38", "#150b2e", "#0f0824"]
    for i, cor in enumerate(agua):
        out.append(rect(0, HOR + i * 4, W, 4, cor))

    # ondulações que deslizam
    for i in range(34):
        y = HOR + 2 + rnd.randint(0, 17)
        x = rnd.randint(0, W - 14)
        w = rnd.randint(4, 13)
        out.append(rect(x, y, w, 1, "#5a3590", f'class="rp rp{i % 3}" opacity="0.55"'))

    # reflexo da lua
    for k, (w, dy) in enumerate(((10, 2), (7, 5), (11, 8), (5, 11), (8, 14), (4, 17))):
        out.append(rect(cx - w // 2, HOR + dy, w, 1, LUA, f'class="rp rp{k % 3}" opacity="0.45"'))

    # ---- o barco (centro da cena) ----
    bx = 150
    # brilho do fogo na água e no ar
    for rr, op in ((16, 0.05), (12, 0.07), (8, 0.09)):
        for y in range(30 - rr // 2, 30 + rr // 2 + 1):
            dx = int(rr * math.sqrt(max(1 - ((y - 30) / (rr / 2)) ** 2, 0)))
            out.append(rect(bx + 2 - dx, y, 2 * dx + 1, 1, FOGO_LAR, f'class="glow" opacity="{op}"'))
    # reflexo escuro do casco + brasas na água
    out.append(rect(bx - 11, HOR + 1, 23, 1, CASCO_ESC, 'opacity="0.55"'))
    out.append(rect(bx - 8, HOR + 2, 17, 1, CASCO_ESC, 'opacity="0.4"'))
    out.append(rect(bx - 5, HOR + 3, 11, 1, CASCO_ESC, 'opacity="0.25"'))
    for k, (w, dy) in enumerate(((9, 2), (5, 4), (11, 6), (6, 8), (9, 10), (4, 12))):
        out.append(rect(bx + 2 - w // 2, HOR + dy, w, 1, FOGO_LAR, f'class="rp rp{k % 3}" opacity="0.55"'))
    # mastro e velas
    out.append(rect(bx, 26, 1, 15, MASTRO))
    out.append(rect(bx - 7, 32, 1, 8, MASTRO, 'opacity="0"'))
    for y in range(31, 38):                      # vela de proa (triângulo)
        w = y - 30
        out.append(rect(bx - w - 1, y, w, 1, VELA))
    for y in range(29, 38):                      # vela grande
        out.append(rect(bx + 2, y, 9, 1, VELA))
    for (x, y, w) in ((bx + 2, 29, 4), (bx + 8, 29, 3), (bx + 9, 30, 2), (bx + 2, 30, 2), (bx + 6, 31, 2), (bx + 10, 33, 1), (bx + 2, 35, 1)):
        out.append(rect(x, y, w, 1, VELA_QUEIMADA))       # partes carbonizadas
    # casco
    out.append(rect(bx - 12, 40, 25, 1, "#8a5a3c"))
    out.append(rect(bx - 11, 41, 23, 1, CASCO))
    out.append(rect(bx - 9, 42, 19, 1, CASCO))
    out.append(rect(bx - 7, 43, 15, 1, CASCO_ESC))
    out.append(rect(bx - 14, 38, 3, 2, CASCO))
    out.append(rect(bx + 12, 38, 3, 2, CASCO))
    out.append(rect(bx - 4, 41, 1, 1, FOGO_AMA, 'opacity="0.8"'))   # vigias acesas
    out.append(rect(bx + 3, 41, 1, 1, FOGO_AMA, 'opacity="0.8"'))
    out.append(rect(bx + 8, 41, 1, 1, FOGO_AMA, 'opacity="0.8"'))

    # chamas: dois quadros alternando (efeito de fogo 8-bit)
    def chama(frame):
        a = frame == 0
        L = []
        # vela grande
        L += [(bx + 3, 24 if a else 25, 2, 5, FOGO_VERM), (bx + 6, 22 if a else 23, 2, 7, FOGO_VERM), (bx + 9, 25 if a else 24, 2, 4, FOGO_VERM)]
        L += [(bx + 3, 26 if a else 27, 1, 3, FOGO_LAR), (bx + 6, 24 if a else 25, 1, 5, FOGO_LAR), (bx + 9, 27 if a else 26, 1, 2, FOGO_LAR)]
        L += [(bx + 6, 27 if a else 26, 1, 2, FOGO_AMA)]
        # vela de proa
        L += [(bx - 6, 28 if a else 29, 2, 4, FOGO_VERM), (bx - 3, 27 if a else 26, 2, 5, FOGO_VERM)]
        L += [(bx - 6, 30 if a else 31, 1, 2, FOGO_LAR), (bx - 3, 29 if a else 28, 1, 3, FOGO_LAR), (bx - 3, 31, 1, 1, FOGO_AMA)]
        # convés
        L += [(bx - 9, 38 if a else 37, 2, 2, FOGO_VERM), (bx - 2, 38, 3, 2, FOGO_LAR), (bx + 5, 37 if a else 38, 2, 3, FOGO_VERM), (bx + 9, 38 if a else 39, 2, 1, FOGO_LAR)]
        L += [(bx - 1, 39, 1, 1, FOGO_AMA), (bx + 6, 39, 1, 1, FOGO_AMA)]
        return "".join(rect(*t[:4], t[4]) for t in L)
    out.append(f'<g class="fa">{chama(0)}</g><g class="fb">{chama(1)}</g>')

    # brasas subindo
    for i in range(16):
        x = bx - 8 + rnd.randint(0, 20)
        cor = (FOGO_AMA, FOGO_LAR, FOGO_VERM)[i % 3]
        out.append(rect(x, 24 + rnd.randint(0, 8), 1, 1, cor, f'class="em em{i % 5}" style="animation-delay:{-rnd.random() * 4:.2f}s"'))

    # texto
    out.append(pixel_text("VICTOR", 9, 6, 3, "#3a1d5e", 1))                       # sombra
    out.append(pixel_text("VICTOR", 8, 5, 3, ROSA, 1))
    out.append(rect(8 + text_width("VICTOR", 3, 1) + 4, 23, 9, 3, FOGO_AMA, 'class="cur"'))   # cursor piscando (sublinhado)
    out.append(pixel_text("FUTURE DATA ENGINEER", 8, 30, 1, LAVANDA, 1))           # >>> EDITE AQUI (subtítulo)
    out.append(pixel_text("BURN THE BOATS.", 8, 55, 1, BRASA, 1))                   # >>> EDITE AQUI (frase)

    # scanlines CRT sutis
    defs.append('<pattern id="scan" width="1" height="2" patternUnits="userSpaceOnUse"><rect width="1" height="1" fill="#000" opacity="0.10"/></pattern>')
    out.append(rect(0, 0, W, H, "url(#scan)"))

    css = """
.tw{animation:tw 3s ease-in-out infinite}.tw1{animation-duration:4s;animation-delay:-1s}.tw2{animation-duration:2.4s;animation-delay:-2s}.tw3{animation-duration:5s;animation-delay:-3s}
@keyframes tw{0%,100%{opacity:1}50%{opacity:.15}}
.fa{animation:fa .45s steps(1) infinite}.fb{animation:fb .45s steps(1) infinite}
@keyframes fa{0%{opacity:1}50%{opacity:0}}@keyframes fb{0%{opacity:0}50%{opacity:1}}
.glow{animation:gl 1.8s ease-in-out infinite}@keyframes gl{0%,100%{opacity:.8}50%{opacity:1}}
.em{animation:em 3.2s linear infinite}.em1{animation-duration:2.6s}.em2{animation-duration:3.8s}.em3{animation-duration:2.9s}.em4{animation-duration:4.2s}
@keyframes em{0%{transform:translate(0,0);opacity:1}100%{transform:translate(3px,-15px);opacity:0}}
.rp{animation:rp 4s ease-in-out infinite}.rp1{animation-duration:5s;animation-delay:-2s}.rp2{animation-duration:3.5s;animation-delay:-1s}
@keyframes rp{0%,100%{transform:translateX(0)}50%{transform:translateX(3px)}}
.cur{animation:cur 1s steps(1) infinite}@keyframes cur{0%{opacity:1}50%{opacity:0}}
.fb{opacity:0}
"""
    open(OUT + "banner.svg", "w", encoding="utf-8").write(
        svg_wrap(W, H, 5, "Pixel art banner: a burning boat on a night sea under the moon, with the name Victor", "\n".join(out), css, "".join(defs)))


# ================================================================== 2) DIVISOR
def divider():
    W, H = 200, 8
    out = []
    for x in range(0, W, 2):
        t = x / W
        cor = "#45206b" if t < 0.35 else ("#7b3a7a" if t < 0.5 else ("#a64574" if t < 0.65 else "#45206b"))
        if abs(x - 100) > 7:
            out.append(rect(x, 4, 1, 1, cor, f'class="dv dv{(x // 2) % 3}"'))
    # pequena chama central
    out.append(f'<g class="fa">{rect(99, 1, 2, 4, FOGO_VERM)}{rect(99, 3, 2, 2, FOGO_LAR)}{rect(100, 4, 1, 1, FOGO_AMA)}</g>')
    out.append(f'<g class="fb">{rect(99, 2, 2, 3, FOGO_VERM)}{rect(100, 1, 1, 1, FOGO_LAR)}{rect(99, 4, 2, 1, FOGO_LAR)}{rect(100, 4, 1, 1, FOGO_AMA)}</g>')
    out.append(rect(97, 5, 6, 1, CASCO))
    out.append(rect(98, 6, 4, 1, CASCO_ESC))
    css = """.fa{animation:fa .5s steps(1) infinite}.fb{opacity:0;animation:fb .5s steps(1) infinite}
@keyframes fa{0%{opacity:1}50%{opacity:0}}@keyframes fb{0%{opacity:0}50%{opacity:1}}
.dv{animation:dv 3s ease-in-out infinite}.dv1{animation-delay:-1s}.dv2{animation-delay:-2s}@keyframes dv{0%,100%{opacity:1}50%{opacity:.3}}"""
    open(OUT + "divider.svg", "w", encoding="utf-8").write(
        svg_wrap(W, H, 5, "Pixel divider with a tiny burning boat", "\n".join(out), css))


# ================================================================== 3) NOW PLAYING
def now_playing():
    W, H = 160, 36
    out = [rect(0, 0, W, H, "#120a2e"), rect(0, 0, W, 1, "#45206b"), rect(0, H - 1, W, 1, "#45206b"),
           rect(0, 0, 1, H, "#45206b"), rect(W - 1, 0, 1, H, "#45206b")]
    for (x, y) in ((0, 0), (W - 1, 0), (0, H - 1), (W - 1, H - 1)):
        out.append(rect(x, y, 1, 1, "#120a2e"))
    out.append(pixel_text("NOW PLAYING", 8, 6, 1, ROSA, 1))
    out.append(pixel_text("LOFI BEATS TO BURN BOATS", 8, 17, 1, LAVANDA, 1))           # >>> EDITE AQUI (música/frase)
    for i in range(8):                                                                   # equalizador
        out.append(rect(118 + i * 4, 4, 2, 10, "#8d3a78", f'class="eq eq{i % 4}"'))
    out.append(rect(8, 29, 144, 3, "#2a1650"))
    out.append(rect(8, 29, 144, 3, BRASA, 'class="pg"'))
    css = """.eq{transform-box:fill-box;transform-origin:50% 100%;animation:eq 1s ease-in-out infinite}
.eq1{animation-duration:.7s}.eq2{animation-duration:1.3s;animation-delay:-.4s}.eq3{animation-duration:.9s;animation-delay:-.2s}
@keyframes eq{0%,100%{transform:scaleY(.25)}50%{transform:scaleY(1)}}
.pg{transform-box:fill-box;transform-origin:0 50%;animation:pg 45s linear infinite}@keyframes pg{0%{transform:scaleX(0)}100%{transform:scaleX(1)}}"""
    open(OUT + "now_playing.svg", "w", encoding="utf-8").write(
        svg_wrap(W, H, 5, "Now playing: lofi beats to burn boats", "\n".join(out), css))


# ================================================================== 4) SKILL TREE
def skills():
    # >>> EDITE AQUI: (nome, nivel de 0 a 10, nota). Seja honesto: recrutador pergunta!
    SK = [("SQL", 6, ""), ("EXCEL", 6, ""), ("PYTHON", 2, "LEVELING UP"), ("JS/TS/REACT", 6, ""), ("GIT", 5, "")]
    W, H = 160, 16 + 9 * len(SK) + 12
    out = [rect(0, 0, W, H, "#120a2e"), rect(0, 0, W, 1, "#45206b"), rect(0, H - 1, W, 1, "#45206b"),
           rect(0, 0, 1, H, "#45206b"), rect(W - 1, 0, 1, H, "#45206b")]
    out.append(pixel_text("SKILL TREE", 8, 5, 1, ROSA, 1))
    for i, (nome, lv, nota) in enumerate(SK):
        y = 16 + i * 9
        out.append(pixel_text(nome, 8, y, 1, LAVANDA, 1))
        for s in range(10):
            x = 80 + s * 7
            if s < lv:
                out.append(rect(x, y, 6, 7, BRASA if nome != "PYTHON" else FOGO_AMA))
                out.append(rect(x, y + 5, 6, 2, "#c97a35" if nome != "PYTHON" else "#d6a93a"))
            else:
                out.append(rect(x, y, 6, 7, "#2a1650"))
                if nota and s == lv:
                    out.append(rect(x, y, 6, 7, FOGO_AMA, 'class="nx"'))
        # >>> a nota (ex.: LEVELING UP) aparece à direita se couber
    out.append(pixel_text("YELLOW: LEARNING", 8, H - 9, 1, "#5a3590", 1))
    out.append(pixel_text("LV 1-10", 110, H - 9, 1, "#5a3590", 1))
    css = ".nx{animation:nx 1s steps(1) infinite}@keyframes nx{0%{opacity:.9}50%{opacity:.1}}"
    open(OUT + "skill_tree.svg", "w", encoding="utf-8").write(
        svg_wrap(W, H, 5, "Skill tree: SQL, Excel, Python, JavaScript/React and Git as pixel level bars", "\n".join(out), css))


banner(); divider(); now_playing(); skills()
print("SVGs gerados em", OUT)
