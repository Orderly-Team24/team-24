#!/usr/bin/env python3
"""Debug section header recognition."""

import sys
sys.path.insert(0, 'src/upload-menu-backend')

from parser import (
    _split_into_blocks, _parse_block, _looks_like_section_header,
    parse_menu
)

def debug_section_parsing():
    """Debug why section headers aren't being recognized."""
    
    text = """STARTERS

BURRATA CAPRESE $14

MAINS

GRILLED SALMON $26

RIBEYE STEAK $32

DESSERTS

TIRAMISU $10

CHEESECAKE $9
"""
    
    print("1. Original text:")
    print(repr(text))
    print()
    
    blocks = _split_into_blocks(text)
    print(f"2. Split into {len(blocks)} blocks:")
    for i, block in enumerate(blocks):
        print(f"   Block {i}: {block}")
    print()
    
    print("3. Parse each block:")
    for i, block in enumerate(blocks):
        dish = _parse_block(block)
        is_header = _looks_like_section_header(dish["name"])
        price_str = str(dish['price']) if dish['price'] is not None else "None"
        print(f"   Block {i}: {dish['name']:25} | Price: {price_str:5} | Flagged: {dish['flagged']!s:5} | Header: {is_header}")
    print()
    
    print("4. Full menu parse:")
    dishes = parse_menu(text)
    for dish in dishes:
        section = dish.get('section') or "None"
        name = dish['name']
        price = dish.get('price', 'N/A')
        print(f"   {name:30} | Section: {section:12} | Price: {price}")
    
    print("\n5. Dishes by section:")
    for section_name in ["STARTERS", "MAINS", "DESSERTS"]:
        section_dishes = [d for d in dishes if d.get("section") == section_name and d.get("price") is not None]
        print(f"   {section_name}: {len(section_dishes)} dishes")
        for d in section_dishes:
            print(f"     - {d['name']:30} ${d['price']}")

if __name__ == "__main__":
    debug_section_parsing()
