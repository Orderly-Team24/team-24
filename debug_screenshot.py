#!/usr/bin/env python3
"""Debug the exact menu reconstruction issue."""

import sys
sys.path.insert(0, 'src/upload-menu-backend')

from ocr_layout import (
    _extract_words, _detect_columns, _cluster_rows,
    _column_rows_to_text, reconstruct_text
)

def debug_screenshot_menu():
    """Debug the exact issue with the screenshot menu."""
    
    # Simplified test with just 2 rows to see the issue
    col1 = [
        ("STARTERS", 20, 10, 0, 0),
        ("BURRATA", 20, 50, 1, 0),
        ("$14", 150, 50, 1, 0),
    ]
    
    col2 = [
        ("MAINS", 320, 10, 2, 0),
        ("GRILLED", 320, 50, 3, 0),
        ("$26", 480, 50, 3, 0),
    ]
    
    col3 = [
        ("DESSERTS", 620, 10, 4, 0),
        ("TIRAMISU", 620, 50, 5, 0),
        ("$10", 750, 50, 5, 0),
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
    words = _extract_words(data)
    
    print("1. Extracted words:")
    for w in words:
        print(f"   {w['text']:12} @ (x={w['left']:3}, y={w['top']:3})")
    print()
    
    columns = _detect_columns(words, image_width)
    if columns:
        print(f"2. Column detection: Found {len(columns)} columns")
        for i, col in enumerate(columns, 1):
            print(f"   Column {i}: {len(col)} words")
            for w in sorted(col, key=lambda x: (x['top'], x['left'])):
                print(f"     {w['text']:12} @ (x={w['left']:3}, y={w['top']:3})")
        print()
        
        print("3. Row clustering within each column:")
        for i, col in enumerate(columns, 1):
            rows = _cluster_rows(col)
            print(f"   Column {i}: {len(rows)} rows")
            for r_idx, row in enumerate(rows, 1):
                row_words = sorted(row, key=lambda x: x['left'])
                row_text = ' '.join(w['text'] for w in row_words)
                print(f"     Row {r_idx}: {row_text}")
        print()
        
        print("4. Text reconstruction per column:")
        parts = []
        for i, col in enumerate(columns, 1):
            text = _column_rows_to_text(_cluster_rows(col))
            parts.append(text)
            print(f"   Column {i}:")
            for line in text.split('\n'):
                print(f"     {repr(line)}")
        print()
        
        print("5. Final reconstructed text:")
        final_text = "\n\n".join(parts)
        for line in final_text.split('\n'):
            print(f"   {repr(line)}")
    else:
        print("2. No columns detected - single column mode")

if __name__ == "__main__":
    debug_screenshot_menu()
