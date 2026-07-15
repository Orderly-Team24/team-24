#!/usr/bin/env python3
"""Test menu parsing with proper imports."""

import sys
import os
import importlib.util

# Load parser from upload-menu-backend
ocr_backend_path = os.path.join(os.getcwd(), 'src/upload-menu-backend')
sys.path.insert(0, ocr_backend_path)

from ocr_layout import reconstruct_text

# Import parser module
parser_spec = importlib.util.spec_from_file_location("menu_parser", os.path.join(ocr_backend_path, 'parser.py'))
menu_parser = importlib.util.module_from_spec(parser_spec)
parser_spec.loader.exec_module(menu_parser)
parse_menu = menu_parser.parse_menu

# Simple 3-column test
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

text = reconstruct_text(data, image_width=1000)
dishes = parse_menu(text)

print("Parsed dishes with sections:")
for i, dish in enumerate(dishes):
    print(f"{i}: {dish['name']:20} | section={dish.get('section')} | price={dish.get('price')}")
