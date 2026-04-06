#!/usr/bin/env python3
"""Convert HTML ASCII art to SVG"""

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

# Read the HTML file
with open('/Users/j.wright/git-repos/ascii-image-generator/samples/fine_tunes_stars.html', 'r') as f:
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

# Find non-empty lines (where content actually is)
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

# Generate SVG
svg_lines = [
    f'<svg width="{int(width)}" height="{int(height)}" xmlns="http://www.w3.org/2000/svg">',
    '  <style>',
    f'    text {{ font-family: "Courier New", monospace; font-size: 12px; }}',
    '  </style>'
]

y = char_height
bright_pink = '#FF1493'  # Bright pink with no transparency
for line in lines:
    x = 0
    for char, color in line:
        if char != ' ' and color != 'rgb(0,0,0)':
            # Use bright pink for all non-black characters
            svg_lines.append(f'  <text x="{x}" y="{y}" fill="{bright_pink}">{char}</text>')
        x += char_width
    y += char_height

svg_lines.append('</svg>')

# Write SVG
svg_path = '/Users/j.wright/git-repos/flux-tuning/docs/fine_tunes_logo.svg'
with open(svg_path, 'w') as f:
    f.write('\n'.join(svg_lines))

print(f"SVG created at: {svg_path}")
print(f"Dimensions: {int(width)}x{int(height)}")
print(f"Lines: {len(lines)}")
