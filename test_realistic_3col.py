#!/usr/bin/env python3
"""Test with realistic multi-row 3-column menu structure."""

import sys
sys.path.insert(0, 'src/upload-menu-backend')

from ocr_layout import reconstruct_text
from parser import parse_menu

def test_realistic_3col_menu():
    """Simulate realistic Tesseract output for a 3-column menu.
    
    Each column has its own rows, with proper spacing.
    """
    
    data = {
        "text": [
            # Column 1: STARTERS section
            "STARTERS",                    # Row 1: header
            "Margherita", "Pizza", "$14",  # Row 2: item + price
            "Caesar", "Salad", "$8",       # Row 3: item + price
            
            # Column 2: MAINS section  
            "MAINS",                       # Row 1: header
            "Grilled", "Salmon", "$26",    # Row 2: item + price
            "Ribeye", "Steak", "$32",      # Row 3: item + price
            
            # Column 3: DESSERTS section
            "DESSERTS",                    # Row 1: header
            "Tiramisu", "$10",             # Row 2: item + price
            "Cheesecake", "$9",            # Row 3: item + price
        ],
        "left": [
            # Col 1 column-starts at 30px
            30, 30, 80, 160,
            30, 80, 160,
            
            # Col 2: column starts at 330px  
            330, 330, 380, 460,
            330, 380, 460,
            
            # Col 3: column starts at 600px
            600, 600, 720,
            600, 720,
        ],
        "top": [
            # Row 1 (headers) - all at top=20
            20, 20, 20, 20,
            20, 20, 20,
            
            # Row 2 (first items)
            80, 80, 80, 80,
            80, 80, 80,
            
            # Row 3 (second items)
            140, 140, 140,
            140, 140,
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
    
    # Check that ribeye is NOT in desserts
    ribeye_in_desserts = next((d for d in desserts if "Ribeye" in d["name"]), None)
    if ribeye_in_desserts:
        errors.append("ERROR: Ribeye incorrectly assigned to DESSERTS")
    
    if errors:
        print("\n❌ ERRORS:")
        for error in errors:
            print(f"  {error}")
        return False
    else:
        print("\n✅ All checks passed!")
        return True

if __name__ == "__main__":
    success = test_realistic_3col_menu()
    sys.exit(0 if success else 1)
