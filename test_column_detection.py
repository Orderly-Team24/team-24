#!/usr/bin/env python3
"""Test to check column detection with realistic spacing."""

import sys
sys.path.insert(0, 'src/upload-menu-backend')

from ocr_layout import _detect_columns, _extract_words, _find_column_boundaries, _column_anchor_lefts, _gap_threshold

def test_column_detection_with_realistic_spacing():
    """Test column detection on 3-column menu with realistic Tesseract output."""
    
    # Simulating a real 3-column menu photo
    # Photo width: 1000px
    # Col 1: x=[10-240] (width 230, left margin 10, right margin 10)
    # Gutter 1: x=[240-270] (width 30)
    # Col 2: x=[270-530] (width 260)
    # Gutter 2: x=[530-560] (width 30)
    # Col 3: x=[560-990] (width 430)
    
    data = {
        "text": [
            # Column 1: STARTERS
            "STARTERS", "Margherita", "Pizza", "$12",
            "Caesar", "Salad", "$8",
            
            # Column 2: MAINS
            "MAINS", "Grilled", "Salmon", "$26",
            "Ribeye", "Steak", "$32",
            
            # Column 3: DESSERTS
            "DESSERTS", "Tiramisu", "$10",
            "Cheesecake", "$9",
        ],
        "left": [
            # Column 1 (range 10-240)
            20, 30, 100, 200,  # Prices on the right side of column
            20, 80, 200,
            
            # Column 2 (range 270-530)
            300, 320, 400, 500,  # Prices on the right side of column
            300, 350, 500,
            
            # Column 3 (range 560-990)
            600, 650, 900,  # Prices on the right side of column
            600, 900,
        ],
        "top": [
            # All headers at top
            10, 50, 50, 50,
            60, 60, 60,
            
            # Column 2
            10, 50, 50, 50,
            60, 60, 60,
            
            # Column 3
            10, 50, 50,
            60, 60,
        ],
        "height": [20] * 22,
        "width": [0] * 22,  # Will use fallback char width
        "conf": [95] * 22,
    }
    
    image_width = 1000
    gap_threshold = _gap_threshold(image_width)
    print(f"Image width: {image_width}px")
    print(f"Gap threshold: {gap_threshold}px")
    print(f"Min column gap fraction: 0.08 (8% of width)")
    print(f"Min column gap px: 40px")
    print()
    
    words = _extract_words(data)
    print(f"Extracted {len(words)} words:")
    for w in words:
        print(f"  '{w['text']:12}' @ x={w['left']:3} (right edge: {w['left'] + w['width']:3})")
    print()
    
    anchors = _column_anchor_lefts(words, image_width)
    print(f"Column anchors (left-edges of segments): {sorted(set(anchors))}")
    print()
    
    boundaries = _find_column_boundaries(anchors, image_width)
    print(f"Column boundaries (gutter positions): {boundaries}")
    print()
    
    if boundaries:
        print("Expected boundaries around:")
        print("  - 255 (between col 1 and col 2)")
        print("  - 545 (between col 2 and col 3)")
    print()
    
    columns = _detect_columns(words, image_width)
    if columns:
        print(f"✓ Detected {len(columns)} columns")
        for i, col in enumerate(columns, 1):
            col_words = sorted(col, key=lambda w: w['left'])
            min_x = min(w['left'] for w in col)
            max_x = max(w['left'] + w['width'] for w in col)
            print(f"  Column {i}: x range [{min_x}-{max_x}], {len(col)} words")
            word_names = ', '.join(w['text'] for w in sorted(col, key=lambda w: (w['top'], w['left'])))
            print(f"    Words: {word_names}")
    else:
        print("✗ No columns detected (fell back to single-column)")
        
    return columns is not None and len(columns) == 3

if __name__ == "__main__":
    success = test_column_detection_with_realistic_spacing()
    sys.exit(0 if success else 1)
