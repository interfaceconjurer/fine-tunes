#!/usr/bin/env python3
"""Convert HTML ASCII art to SVG with light and dark mode versions"""

from html.parser import HTMLParser
import re

class AsciiArtParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.chars = []
        self.current_color = None
        self.in_pre = False

    def handle_starttag(self, tag, attrs):
        if tag == 'pre':
            self.in_pre = True
        elif tag == 'span' and self.in_pre:
            for attr, value in attrs:
                if attr == 'style':
                    color_match = re.search(r'color:rgb\((\d+),(\d+),(\d+)\)', value)
                    if color_match:
                        r, g, b = color_match.groups()
                        self.current_color = f'rgb({r},{g},{b})'

    def handle_data(self, data):
        if self.in_pre and self.current_color:
            for char in data:
                self.chars.append((char, self.current_color))

    def handle_endtag(self, tag):
        if tag == 'pre':
            self.in_pre = False

def invert_color(rgb_string):
    """Invert colors for light mode - what's bright in dark mode becomes dark in light mode"""
    match = re.search(r'rgb\((\d+),(\d+),(\d+)\)', rgb_string)
    if match:
        r, g, b = map(int, match.groups())
        # Invert each color channel
        r = 255 - r
        g = 255 - g
        b = 255 - b
        return f'rgb({r},{g},{b})'
    return rgb_string

# Read the HTML file
with open('/Users/j.wright/git-repos/ascii-image-generator/samples/fine_tunes_rainbow.html', 'r') as f:
    html_content = f.read()

# Parse it
parser = AsciiArtParser()
parser.feed(html_content)

# Convert to lines
lines = []
current_line = []
for char, color in parser.chars:
    if char == '\n':
        lines.append(current_line)
        current_line = []
    else:
        current_line.append((char, color))
if current_line:
    lines.append(current_line)

# Find non-empty lines
non_empty = []
for i, line in enumerate(lines):
    has_content = any(char != ' ' and color != 'rgb(0,0,0)' for char, color in line)
    if has_content:
        non_empty.append(i)

if non_empty:
    start_line = max(0, non_empty[0] - 2)
    end_line = min(len(lines), non_empty[-1] + 3)
    lines = lines[start_line:end_line]

# Calculate dimensions
char_width = 7.2
char_height = 12
max_width = max(len(line) for line in lines) if lines else 0
height = len(lines) * char_height
width = max_width * char_width

# Generate DARK mode SVG
svg_lines_dark = [
    f'<svg width="{int(width)}" height="{int(height)}" xmlns="http://www.w3.org/2000/svg">',
    '  <style>',
    f'    text {{ font-family: "Courier New", monospace; font-size: 12px; }}',
    '  </style>'
]

y = char_height
for line in lines:
    x = 0
    for char, color in line:
        if char != ' ' and color != 'rgb(0,0,0)':
            svg_lines_dark.append(f'  <text x="{x}" y="{y}" fill="{color}">{char}</text>')
        x += char_width
    y += char_height

svg_lines_dark.append('</svg>')

# Write DARK mode SVG
dark_path = '/Users/j.wright/git-repos/flux-tuning/docs/fine_tunes_logo_dark.svg'
with open(dark_path, 'w') as f:
    f.write('\n'.join(svg_lines_dark))

print(f"Dark mode SVG created at: {dark_path}")

# Generate LIGHT mode SVG (darker colors for visibility)
svg_lines_light = [
    f'<svg width="{int(width)}" height="{int(height)}" xmlns="http://www.w3.org/2000/svg">',
    '  <style>',
    f'    text {{ font-family: "Courier New", monospace; font-size: 12px; }}',
    '  </style>'
]

y = char_height
for line in lines:
    x = 0
    for char, color in line:
        if char != ' ' and color != 'rgb(0,0,0)':
            # Invert colors for light mode
            light_color = invert_color(color)
            svg_lines_light.append(f'  <text x="{x}" y="{y}" fill="{light_color}">{char}</text>')
        x += char_width
    y += char_height

svg_lines_light.append('</svg>')

# Write LIGHT mode SVG
light_path = '/Users/j.wright/git-repos/flux-tuning/docs/fine_tunes_logo_light.svg'
with open(light_path, 'w') as f:
    f.write('\n'.join(svg_lines_light))

print(f"Light mode SVG created at: {light_path}")
print(f"Dimensions: {int(width)}x{int(height)}")
print(f"Lines: {len(lines)}")
