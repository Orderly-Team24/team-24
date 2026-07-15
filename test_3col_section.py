#!/usr/bin/env python3
"""Test to reproduce the 3-column menu with section headers issue."""

import sys
sys.path.insert(0, 'src/upload-menu-backend')

from ocr_layout import reconstruct_text
from parser import parse_menu

def test_three_column_menu_with_sections():
    """Simulate OCR output for a 3-column menu: STARTERS | MAINS | DESSERTS"""
    
    # Simulate Tesseract image_to_data for 3 columns side-by-side
    # Image width: 1000px
    # Col 1: 10-250px (STARTERS)
    # Col 2: 350-650px (MAINS)  
    # Col 3: 750-990px (DESSERTS)
    
    data = {
        "text": [
            # Column 1: STARTERS section
            "STARTERS", "Burrata", "Caprese", "$14",
            "Tuna", "Tartare", "$16",
            
            # Column 2: MAINS section
            "MAINS", "Grilled", "Salmon", "$26",
            "Ribeye", "Steak", "$32",
            
            # Column 3: DESSERTS section
            "DESSERTS", "Tiramisu", "$10",
            "New", "York", "Cheesecake", "$9",
        ],
        "left": [
            # Column 1
            10, 10, 60, 150,
            10, 60, 140,
            
            # Column 2
            350, 350, 380, 480,
            350, 380, 480,
            
            # Column 3
            750, 750, 850,
            750, 800, 850, 920,
        ],
        "top": [
            # Column 1
            10, 50, 50, 50,
            100, 100, 100,
            
            # Column 2
            10, 50, 50, 50,
            100, 100, 100,
            
            # Column 3
            10, 50, 50,
            100, 100, 100, 100,
        ],
        "height": [20] * 21,
        "width": [0] * 21,
        "conf": [95] * 21,
    }
    
    # Reconstruct text with column detection
    text = reconstruct_text(data, image_width=1000)
    print("Reconstructed text:")
    print(repr(text))
    print("\n" + "="*50 + "\n")
    print(text)
    print("\n" + "="*50 + "\n")
    
    # Parse the menu
    dishes = parse_menu(text)
    
    print("Parsed dishes:")
    for dish in dishes:
        section = dish['section'] or "None"
        print(f"  {dish['name']:30} | Section: {section:12} | Price: {dish.get('price', 'N/A')}")
    
    # Check sections
    print("\nSection assignments:")
    starters = [d for d in dishes if d.get("section") == "STARTERS"]
    mains = [d for d in dishes if d.get("section") == "MAINS"]
    desserts = [d for d in dishes if d.get("section") == "DESSERTS"]
    
    print(f"  STARTERS: {len(starters)} dishes")
    for d in starters:
        print(f"    - {d['name']}")
    
    print(f"  MAINS: {len(mains)} dishes")
    for d in mains:
        print(f"    - {d['name']}")
        
    print(f"  DESSERTS: {len(desserts)} dishes")
    for d in desserts:
        print(f"    - {d['name']}")
    
    # Verify correctness
    errors = []
    
    # Check that Ribeye is in MAINS, not somewhere else
    ribeye = next((d for d in dishes if "Ribeye" in d["name"]), None)
    if ribeye and ribeye.get("section") != "MAINS":
        errors.append(f"ERROR: Ribeye should be in MAINS, but is in {ribeye.get('section')}")
    
    # Check that Tiramisu is in DESSERTS
    tiramisu = next((d for d in dishes if "Tiramisu" in d["name"]), None)
    if tiramisu and tiramisu.get("section") != "DESSERTS":
        errors.append(f"ERROR: Tiramisu should be in DESSERTS, but is in {tiramisu.get('section')}")
    
    # Check that Burrata is in STARTERS
    burrata = next((d for d in dishes if "Burrata" in d["name"]), None)
    if burrata and burrata.get("section") != "STARTERS":
        errors.append(f"ERROR: Burrata should be in STARTERS, but is in {burrata.get('section')}")
    
    if errors:
        print("\n" + "="*50)
        for error in errors:
            print(error)
        return False
    else:
        print("\n✓ All sections assigned correctly!")
        return True

if __name__ == "__main__":
    success = test_three_column_menu_with_sections()
    sys.exit(0 if success else 1)
