#!/usr/bin/env python3
"""Convert ASCII text to SVG"""

ascii_art = """
                          ·○○◉◉◉◉○*.     ·*○◉◉◉◉○*·     ·*○◉◉◉◉○*·     ·*○◉◉○◉○○·
                        *◉◉*·....·○◉○· ·◉◉*·....·○◉◉· ·◉◉○·....·○◉◉· ·○◉○·..·.·*◉◉*
                       ○◉*         .○◉○◉○.        .○◉○◉○.        .○◉○◉○.   ○◉○   *◉○
                      *◉○           .◉◉○            ○◉○            ○◉◉.    ·*·    ○◉*
              .○○○○○○○◉◉·     ○○     ○◉·     ○○.    *◉*     *○.    ·◉*     ·○○○○○○◉◉○
              .◉◉*......     ·◉◉·     .     .◉◉·     .     .◉◉*     .      ○◉*......
               *◉○.         .○◉◉○.         .○◉◉◉.          ○◉◉◉·          *◉○
                ·◉◉*.     .*◉◉··◉◉*.     .*◉◉··○◉*.     .*◉◉*.○◉○·     .·○◉*
                 .*○◉◉○○○◉◉○·    ·○◉◉○○○◉◉○*.   ·○◉◉○○○◉◉○*.   ·○◉◉○○○○◉◉*.
                    ..···.          .···..         .···..         .···..

                 ....  .   .        ....     ......  .        .    .   ....    ...
               .◉**** ·◉  ◉◉○  ·◉  ◉○***.    ·*○◉**..◉.   ◉· *◉◉   ◉. ○◉***· ·◉***○○
               .◉.    ·◉  ◉○◉* ·◉  ◉.          ·◉   .◉.   ◉· *◉○○  ◉· ◉○     ○◉   .*
               .◉.·◉. ·◉  ◉*.◉.·◉  ◉..◉.       ·◉   .◉.   ◉· *◉ ◉* ◉· ◉* ◉*  .○***○·
               .◉.    ·◉  ◉* *◉*◉  ◉.          ·◉   .◉.   ◉· *◉ .◉*◉· ◉○     ··   *◉
               .◉.    ·◉  ◉*  ○◉◉  ◉*···.      ·◉    ◉*··*◉. ○◉  ·◉◉. ○◉···· *◉···○○
                .      .  .    ..  ......       .     ....   ..   ..  ......  .....
"""

lines = ascii_art.strip().split('\n')

# Calculate dimensions
char_width = 7.2
char_height = 14
max_width = max(len(line) for line in lines)
height = len(lines) * char_height
width = max_width * char_width

# Generate SVG with pink color
svg_lines = [
    f'<svg width="{int(width)}" height="{int(height)}" xmlns="http://www.w3.org/2000/svg">',
    '  <rect width="100%" height="100%" fill="#000000"/>',
    '  <style>',
    '    text {',
    '      font-family: "Courier New", Courier, monospace;',
    '      font-size: 12px;',
    '      fill: #FF69B4;',
    '    }',
    '  </style>'
]

y = char_height
for line in lines:
    if line.strip():  # Only process non-empty lines
        # Escape XML special characters
        line_escaped = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        svg_lines.append(f'  <text x="0" y="{y}" xml:space="preserve">{line_escaped}</text>')
    y += char_height

svg_lines.append('</svg>')

# Write SVG
svg_path = '/Users/j.wright/git-repos/flux-tuning/docs/fine_tunes_logo.svg'
with open(svg_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(svg_lines))

print(f"SVG created at: {svg_path}")
print(f"Dimensions: {int(width)}x{int(height)}")
print(f"Lines: {len(lines)}")
