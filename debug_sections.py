#!/usr/bin/env python3
"""Test menu parsing for the exact menu from the user's screenshot."""

import sys
sys.path.insert(0, 'src/upload-menu-backend')

from ocr_layout import reconstruct_text
# Import from upload-menu-backend, not backend
import parser as upload_parser

# ... (same data as before)

# Column 1: STARTERS
col1 = [
    ("STARTERS", 20, 10, 0, 0),
    ("BURRATA", 20, 50, 1, 0),
    ("CAPRESE", 80, 50, 1, 0),
    ("$14", 150, 50, 1, 0),
]

col2 = [
    ("MAINS", 320, 10, 6, 0),
    ("GRILLED", 320, 50, 7, 0),
    ("SALMON", 400, 50, 7, 0),
    ("$26", 480, 50, 7, 0),
]

col3 = [
    ("DESSERTS", 620, 10, 12, 0),
    ("TIRAMISU", 620, 50, 13, 0),
    ("$10", 750, 50, 13, 0),
]

data = {
    "text": [w[0] for w in col1 + col2 + col3],
    "left": [w[1] for w in col1 + col2 + col3],
    "top": [w[2] for w in col1 + col2 + col3],
    "height": [20] * len(col1 + col2 + col3),
    "width": [0] * len(col1 + col2 + col3),
    "conf": [95] * len(col1 + col2 + col3),
}

image_width = 1000
text = reconstruct_text(data, image_width=image_width)

print("Reconstructed text:")
print(repr(text))
print()

print("Text split into blocks:")
blocks = upload_parser._split_into_blocks(text)
for i, block in enumerate(blocks):
    print(f"Block {i}: {block}")
print()

print("Parsed dishes:")
dishes = upload_parser.parse_menu(text)
for i, dish in enumerate(dishes):
    print(f"Dish {i}: name={dish['name']!r:40} section={dish.get('section')!r}")
