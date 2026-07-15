#!/usr/bin/env python3
"""Quick test for section assignment."""
import sys
sys.path.insert(0, 'src/upload-menu-backend')
from parser import parse_menu

text = """STARTERS

BURRATA CAPRESE $14

MAINS

GRILLED SALMON $26
"""

dishes = parse_menu(text)
for d in dishes:
    print(f'{d["name"]:30} | Section: {d.get("section")}')
