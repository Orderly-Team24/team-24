#!/usr/bin/env python3
"""Test with correct multi-row 3-column structure."""

import sys
sys.path.insert(0, 'src/upload-menu-backend')

from ocr_layout import reconstruct_text
from parser import parse_menu

def test_correct_3col_rows():
    """Test where words across columns are at same Y (same row)."""
    
    data = {
        "text": [
            # Row 1: All headers at y=20
            "STARTERS",                  # x=30, y=20 (Col 1)
            "MAINS",                     # x=330, y=20 (Col 2)
            "DESSERTS",                  # x=600, y=20 (Col 3)
            
            # Row 2: First item in each column at y=80
            "Margherita", "Pizza", "$14",  # Col 1
            "Grilled", "Salmon", "$26",    # Col 2
            "Tiramisu", "$10",             # Col 3
            
            # Row 3: Second item in each column at y=140
            "Caesar", "Salad", "$8",       # Col 1
            "Ribeye", "Steak", "$32",      # Col 2
            "Cheesecake", "$9",            # Col 3
        ],
        "left": [
            # Row 1
            30, 330, 600,
            
            # Row 2
            30, 80, 160,           # Col 1
            330, 380, 460,         # Col 2
            600, 720,              # Col 3
            
            # Row 3
            30, 80, 160,           # Col 1
            330, 380, 460,         # Col 2
            600, 720,              # Col 3
        ],
        "top": [
            # Row 1
            20, 20, 20,
            
            # Row 2
            80, 80, 80,   # Col 1
            80, 80, 80,   # Col 2
            80, 80,       # Col 3
            
            # Row 3
            140, 140, 140,   # Col 1
            140, 140, 140,   # Col 2
            140, 140,        # Col 3
        ],
        "height": [20] * 22,
        "width": [0] * 22,
        "conf": [95] * 22,
    }
    
    image_width = 1000
    text = reconstruct_text(data, image_width=image_width)
    
    print("Reconstructed text:")
    print("=" * 60)
    print(text)
    print("=" * 60)
    print()
    
    # Parse the menu
    dishes = parse_menu(text)
    
    print("Parsed dishes:")
    for dish in dishes:
        section = dish.get('section') or "None"
        name = dish['name']
        price = dish.get('price', 'N/A')
        print(f"  {name:30} | Sect: {section:12} | Price: {price}")
    
    print("\nFiltered by section:")
    starters = [d for d in dishes if d.get("section") == "STARTERS" and d.get("price") is not None]
    mains = [d for d in dishes if d.get("section") == "MAINS" and d.get("price") is not None]
    desserts = [d for d in dishes if d.get("section") == "DESSERTS" and d.get("price") is not None]
    
    print(f"  STARTERS ({len(starters)} items):")
    for d in starters:
        print(f"    - {d['name']:25} ${d['price']}")
    
    print(f"  MAINS ({len(mains)} items):")
    for d in mains:
        print(f"    - {d['name']:25} ${d['price']}")
    
    print(f"  DESSERTS ({len(desserts)} items):")
    for d in desserts:
        print(f"    - {d['name']:25} ${d['price']}")
    
    # Verify
    errors = []
    
    ribeye = next((d for d in mains if "Ribeye" in d["name"]), None)
    if not ribeye:
        errors.append("ERROR: Ribeye not found in MAINS section")
    elif ribeye.get("price") != 32:
        errors.append(f"ERROR: Ribeye price is {ribeye.get('price')}, expected 32")
    
    tiramisu = next((d for d in desserts if "Tiramisu" in d["name"]), None)
    if not tiramisu:
        errors.append("ERROR: Tiramisu not found in DESSERTS section")
    elif tiramisu.get("price") != 10:
        errors.append(f"ERROR: Tiramisu price is {tiramisu.get('price')}, expected 10")
    
    margherita = next((d for d in starters if "Margherita" in d["name"]), None)
    if not margherita:
        errors.append("ERROR: Margherita not found in STARTERS section")
    elif margherita.get("price") != 14:
        errors.append(f"ERROR: Margherita price is {margherita.get('price')}, expected 14")
    
    if errors:
        print("\n❌ ERRORS:")
        for error in errors:
            print(f"  {error}")
        return False
    else:
        print("\n✅ All checks passed!")
        return True

if __name__ == "__main__":
    success = test_correct_3col_rows()
    sys.exit(0 if success else 1)
