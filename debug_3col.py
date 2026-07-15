#!/usr/bin/env python3
"""Debug 3-column detection with proper row structure."""

import sys
sys.path.insert(0, 'src/upload-menu-backend')

from ocr_layout import _extract_words, _detect_columns, _cluster_rows, _column_rows_to_text

def debug_3col_detection():
    """Debug the 3-column detection and reconstruction."""
    
    data = {
        "text": [
            # Column 1: STARTERS section
            "STARTERS", "Margherita", "Pizza", "$14",
            "Caesar", "Salad", "$8",
            
            # Column 2: MAINS section  
            "MAINS", "Grilled", "Salmon", "$26",
            "Ribeye", "Steak", "$32",
            
            # Column 3: DESSERTS section
            "DESSERTS", "Tiramisu", "$10",
            "Cheesecake", "$9",
        ],
        "left": [
            # Col 1
            30, 30, 80, 160,
            30, 80, 160,
            
            # Col 2
            330, 330, 380, 460,
            330, 380, 460,
            
            # Col 3
            600, 600, 720,
            600, 720,
        ],
        "top": [
            # Row 1 (headers)
            20, 20, 20, 20,
            20, 20, 20,
            
            # Row 2
            80, 80, 80, 80,
            80, 80, 80,
            
            # Row 3
            140, 140, 140,
            140, 140,
        ],
        "height": [20] * 22,
        "width": [0] * 22,
        "conf": [95] * 22,
    }
    
    image_width = 1000
    words = _extract_words(data)
    
    print("STEP 1: Words extracted")
    print(f"  Total: {len(words)} words")
    for w in words:
        print(f"    {w['text']:12} @ (x={w['left']:3}, y={w['top']:3})")
    print()
    
    columns = _detect_columns(words, image_width)
    if columns:
        print(f"STEP 2: Columns detected - {len(columns)} columns")
        for i, col in enumerate(columns, 1):
            print(f"  Column {i}: {len(col)} words")
            for w in sorted(col, key=lambda x: (x['top'], x['left'])):
                print(f"    {w['text']:12} @ (x={w['left']:3}, y={w['top']:3})")
        print()
        
        print("STEP 3: Row clustering within each column")
        for i, col in enumerate(columns, 1):
            rows = _cluster_rows(col)
            print(f"  Column {i}: {len(rows)} rows")
            for row_idx, row in enumerate(rows):
                row_text = ' '.join(w['text'] for w in sorted(row, key=lambda x: x['left']))
                top_vals = [w['top'] for w in row]
                print(f"    Row {row_idx+1} (y={top_vals[0]}): {row_text}")
        print()
        
        print("STEP 4: Converting to text")
        for i, col in enumerate(columns, 1):
            text = _column_rows_to_text(_cluster_rows(col))
            print(f"  Column {i} text:")
            print(f"    {repr(text)}")
        print()
    else:
        print("STEP 2: No columns detected - using single column mode")
        rows = _cluster_rows(words)
        print(f"  Rows: {len(rows)}")
        for row in rows:
            print(f"    {' '.join(w['text'] for w in row)}")

if __name__ == "__main__":
    debug_3col_detection()
