#!/usr/bin/env python3
"""Test menu parsing for the exact menu from the user's screenshot."""

import sys
import os
sys.path.insert(0, 'src/upload-menu-backend')

# Load parser from upload-menu-backend, not the built-in parser module
ocr_backend_path = os.path.join(os.getcwd(), 'src/upload-menu-backend')
if ocr_backend_path not in sys.path:
    sys.path.insert(0, ocr_backend_path)

from ocr_layout import reconstruct_text
# Import parser from the correct location
import importlib.util
parser_spec = importlib.util.spec_from_file_location("menu_parser", os.path.join(ocr_backend_path, 'parser.py'))
menu_parser = importlib.util.module_from_spec(parser_spec)
parser_spec.loader.exec_module(menu_parser)
parse_menu = menu_parser.parse_menu

def test_exact_menu_from_screenshot():
    """Parse the exact 3-column menu from the user's screenshot."""
    
    # Column 1: STARTERS
    col1 = [
        ("STARTERS", 20, 10, 0, 0),
        ("BURRATA", 20, 50, 1, 0),
        ("CAPRESE", 80, 50, 1, 0),
        ("$14", 150, 50, 1, 0),
        ("TUNA", 20, 100, 2, 0),
        ("TARTARE", 80, 100, 2, 0),
        ("$16", 150, 100, 2, 0),
        ("CRISPY", 20, 150, 3, 0),
        ("CALAMARI", 80, 150, 3, 0),
        ("$13", 150, 150, 3, 0),
        ("WILD", 20, 200, 4, 0),
        ("MUSHROOM", 80, 200, 4, 0),
        ("SOUP", 120, 200, 4, 0),
        ("$10", 150, 200, 4, 0),
        ("CAESAR", 20, 250, 5, 0),
        ("SALAD", 80, 250, 5, 0),
        ("$11", 150, 250, 5, 0),
    ]
    
    # Column 2: MAINS
    col2 = [
        ("MAINS", 320, 10, 6, 0),
        ("GRILLED", 320, 50, 7, 0),
        ("SALMON", 400, 50, 7, 0),
        ("$26", 480, 50, 7, 0),
        ("RIBEYE", 320, 100, 8, 0),
        ("STEAK", 400, 100, 8, 0),
        ("$32", 480, 100, 8, 0),
        ("CHICKEN", 320, 150, 9, 0),
        ("PICCATA", 400, 150, 9, 0),
        ("$22", 480, 150, 9, 0),
        ("SEAFOOD", 320, 200, 10, 0),
        ("LINGUINE", 400, 200, 10, 0),
        ("$24", 480, 200, 10, 0),
        ("VEGETABLE", 320, 250, 11, 0),
        ("RISOTTO", 400, 250, 11, 0),
        ("$20", 480, 250, 11, 0),
    ]
    
    # Column 3: DESSERTS
    col3 = [
        ("DESSERTS", 620, 10, 12, 0),
        ("TIRAMISU", 620, 50, 13, 0),
        ("$10", 750, 50, 13, 0),
        ("NEW", 620, 100, 14, 0),
        ("YORK", 650, 100, 14, 0),
        ("CHEESECAKE", 700, 100, 14, 0),
        ("$9", 750, 100, 14, 0),
        ("CHOCOLATE", 620, 150, 15, 0),
        ("LAVA", 700, 150, 15, 0),
        ("CAKE", 740, 150, 15, 0),
        ("$11", 750, 150, 15, 0),
        ("LEMON", 620, 200, 16, 0),
        ("SORBET", 700, 200, 16, 0),
        ("$8", 750, 200, 16, 0),
        ("CRÈME", 620, 250, 17, 0),
        ("BRÛLÉE", 700, 250, 17, 0),
        ("$10", 750, 250, 17, 0),
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
    print("=" * 70)
    print(text)
    print("=" * 70)
    print()
    
    # Parse the menu
    dishes = parse_menu(text)
    
    print("Debug: First 3 dishes with actual section values:")
    for i, dish in enumerate(dishes[:3]):
        print(f"  {i}: name={dish['name']!r}, section={dish.get('section')!r}, price={dish.get('price')}")
    print()
    
    print("All dishes:")
    print("-" * 70)
    for dish in dishes:
        section = dish.get('section') or "None"
        name = dish['name'].strip()
        price = dish.get('price', 'N/A')
        print(f"  {name:30} | Sect: {section:12} | Price: {price}")
    
    print("\nDesserts only:")
    print("-" * 70)
    desserts = [d for d in dishes if d.get("section") == "DESSERTS"]
    for dish in desserts:
        name = dish['name'].strip()
        price = dish.get('price')
        print(f"  {name:30} | ${price}")
    
    print(f"\nTotal desserts found: {len(desserts)}")
    
    # Check budget filtering
    budget = 20.0
    desserts_in_budget = [d for d in desserts if d.get('price') is not None and d['price'] <= budget]
    print(f"Desserts under ${budget}: {len(desserts_in_budget)}")
    for dish in desserts_in_budget:
        print(f"  - {dish['name'].strip():30} ${dish['price']}")
    
    # Check mains
    mains = [d for d in dishes if d.get("section") == "MAINS"]
    print(f"\nTotal mains found: {len(mains)}")
    for dish in mains:
        name = dish['name'].strip()
        price = dish.get('price')
        print(f"  - {name:30} | ${price}")
    
    # Ribeye check
    ribeye = next((d for d in mains if "RIBEYE" in d['name'].upper()), None)
    if ribeye:
        print(f"\n❌ RIBEYE found in MAINS section at ${ribeye['price']}")
        if ribeye['price'] > budget:
            print(f"   RIBEYE exceeds budget of ${budget} — should NOT be recommended!")
    
    # Verify we have enough desserts
    if len(desserts_in_budget) < 1:
        print(f"\n❌ ERROR: No desserts found within ${budget} budget!")
        return False
    else:
        print(f"\n✅ Found {len(desserts_in_budget)} desserts within ${budget} budget")
        return True

if __name__ == "__main__":
    success = test_exact_menu_from_screenshot()
    sys.exit(0 if success else 1)
