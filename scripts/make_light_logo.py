#!/usr/bin/env python3
"""Derive fine_tunes_logo_light.svg from the dark logo's glyph layout.

The dark logo comes from ascii-image-generator's rainbow mode:
hue = column / 90, saturation = glyph density, value = 1. This script
keeps every glyph and position. It recolours each glyph in OKLCH:
  - hue   = the dark glyph's hue + 180deg (the light logo's existing hue order:
            blue -> violet -> magenta -> red -> orange -> green)
  - L     = deeper for dense glyphs and lighter for sparse ones, never near-black
  - C     = the most chroma that fits in sRGB gamut
L is then capped so every glyph reaches MIN_CONTRAST against each background in BGS:
GitHub white, plus the alchemist-app stage (#dedfe2) and full-screen viewer (#bebfc2).

Usage: python3 scripts/make_light_logo.py docs/fine_tunes_logo_dark.svg docs/fine_tunes_logo_light.svg
"""
import colorsys, math, re, sys

MIN_CONTRAST = float(sys.argv[3]) if len(sys.argv) > 3 else 3.0
BGS = [(0xff, 0xff, 0xff), (0xde, 0xdf, 0xe2), (0xbe, 0xbf, 0xc2)]
L_DENSE, L_SPARSE = 0.40, 0.62   # OKLab L for ◉ ... '.'
PAT = re.compile(r'(<text x="[^"]+" y="[^"]+" fill=")rgb\((\d+),(\d+),(\d+)\)(">([^<]*)</text>)')

def lin(c): c /= 255; return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
def lum(rgb): r, g, b = map(lin, rgb); return 0.2126*r + 0.7152*g + 0.0722*b
def contrast(a, b): a, b = sorted((lum(a), lum(b)), reverse=True); return (a + .05) / (b + .05)

def oklch_to_srgb(L, C, h):
    a, b = C*math.cos(h), C*math.sin(h)
    l_ = L + 0.3963377774*a + 0.2158037573*b
    m_ = L - 0.1055613458*a - 0.0638541728*b
    s_ = L - 0.0894841775*a - 1.2914855480*b
    l, m, s = l_**3, m_**3, s_**3
    rgb = (4.0767416621*l - 3.3077115913*m + 0.2309699292*s,
           -1.2684380046*l + 2.6097574011*m - 0.3413193965*s,
           -0.0041960863*l - 0.7034186147*m + 1.7076147010*s)
    return rgb

def enc(x): return 12.92*x if x <= 0.0031308 else 1.055*x**(1/2.4) - 0.055
def in_gamut(rgb): return all(-1e-6 <= c <= 1+1e-6 for c in rgb)

def max_chroma_rgb(L, h):
    lo, hi = 0.0, 0.4
    for _ in range(40):
        mid = (lo+hi)/2
        (lo, hi) = (mid, hi) if in_gamut(oklch_to_srgb(L, mid, h)) else (lo, mid)
    return tuple(round(min(max(enc(c), 0), 1)*255) for c in oklch_to_srgb(L, lo, h))

def srgb_hue_to_oklab_h(hue01):
    # The OKLab hue angle of the fully saturated sRGB colour at this HSV hue.
    r, g, b = colorsys.hsv_to_rgb(hue01, 1, 1)
    r, g, b = map(lambda c: lin(c*255), (r, g, b))
    l = (0.4122214708*r + 0.5363325363*g + 0.0514459929*b) ** (1/3)
    m = (0.2119034982*r + 0.6806995451*g + 0.1073969566*b) ** (1/3)
    s = (0.0883024619*r + 0.2817188376*g + 0.6299787005*b) ** (1/3)
    A = 1.9779984951*l - 2.4285922050*m + 0.4505937099*s
    B = 0.0259040371*l + 0.7827717662*m - 0.8086757660*s
    return math.atan2(B, A)

def recolor(m):
    head, r, g, b, tail, ch = m.group(1), *map(int, m.group(2, 3, 4)), m.group(5), m.group(6)
    x = float(re.search(r'x="([^"]+)"', head).group(1))
    hue = (round(x / 7.2) / 90 + 0.5) % 1          # complementary hue, from the column
    density = 1 - colorsys.rgb_to_hsv(r/255, g/255, b/255)[1]  # 1 = ◉, 0 = .
    density = min(max((density - 0.16) / 0.84, 0), 1)
    L = L_SPARSE + (L_DENSE - L_SPARSE) * density
    h = srgb_hue_to_oklab_h(hue)
    rgb = max_chroma_rgb(L, h)
    while min(contrast(rgb, bg) for bg in BGS) < MIN_CONTRAST:
        L -= 0.005; rgb = max_chroma_rgb(L, h)
    return f'{head}rgb({rgb[0]},{rgb[1]},{rgb[2]}){tail}'

src, dst = sys.argv[1], sys.argv[2]
out, n = PAT.subn(recolor, open(src, encoding='utf-8').read())
open(dst, 'w', encoding='utf-8').write(out)
print(f'recoloured {n} glyphs -> {dst}')
