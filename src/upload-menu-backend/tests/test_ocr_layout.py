"""Unit tests for ocr_layout.reconstruct_text — pure logic, no real
Tesseract or image needed. We build synthetic ``image_to_data``-shaped dicts
with word positions; the layout module clusters by Y coordinate and
detects columns from horizontal position, not Tesseract block_num.
"""
from __future__ import annotations

from ocr_layout import reconstruct_text


def _make_data(words: list[tuple[str, int, int, int, int]]) -> dict:
    """Build a Tesseract-style `image_to_data` dict from
    (text, left, top, block, line) tuples. par_num fixed at 0, height
    fixed at 20, confidence fixed at high (95) for all words.
    """
    data = {
        "text": [], "left": [], "top": [], "height": [],
        "block_num": [], "par_num": [], "line_num": [], "conf": [],
    }
    for text, left, top, block, line in words:
        data["text"].append(text)
        data["left"].append(left)
        data["top"].append(top)
        data["height"].append(20)
        data["block_num"].append(block)
        data["par_num"].append(0)
        data["line_num"].append(line)
        data["conf"].append(95)
    return data


def test_empty_data_returns_empty_string():
    data = _make_data([])
    assert reconstruct_text(data, image_width=1000) == ""


def test_single_column_reconstructs_reading_order():
    # Two separate dishes (distinct block_num), all comfortably in the left
    # half — should NOT be treated as two columns, and should come back in
    # normal top-to-bottom order.
    words = [
        ("Margherita", 10, 10, 0, 0),
        ("Pizza", 100, 10, 0, 0),
        ("$12.99", 180, 10, 0, 0),
        ("Caesar", 10, 40, 1, 0),
        ("Salad", 90, 40, 1, 0),
    ]
    data = _make_data(words)
    text = reconstruct_text(data, image_width=1000)
    lines = [l for l in text.split("\n") if l]
    assert lines == ["Margherita Pizza $12.99", "Caesar Salad"]


def test_multiline_dish_within_one_block_uses_single_newline():
    # Same block_num, two lines — a dish name + its description, exactly
    # like a real Tesseract block for a two-line menu entry.
    words = [
        ("Dish", 10, 10, 0, 0),
        ("Name", 60, 10, 0, 0),
        ("with", 10, 30, 0, 1),
        ("basil", 60, 30, 0, 1),
    ]
    data = _make_data(words)
    text = reconstruct_text(data, image_width=1000)
    assert text == "Dish Name\nwith basil"


def test_blank_line_inserted_between_separate_blocks():
    words = [
        ("Dish", 10, 10, 0, 0),
        ("One", 60, 10, 0, 0),
        ("Dish", 10, 100, 1, 0),
        ("Two", 60, 100, 1, 0),
    ]
    data = _make_data(words)
    text = reconstruct_text(data, image_width=1000)
    assert "\n\n" in text
    assert text.split("\n\n") == ["Dish One", "Dish Two"]


def test_two_column_layout_is_split_and_reordered():
    # Left column: two dishes, each its own block, stacked vertically, all
    # left of the midline (image width 1000 -> midpoint 500).
    left_words = [
        ("Margherita", 10, 10, 0, 0),
        ("Pizza", 110, 10, 0, 0),
        ("Caesar", 10, 40, 1, 0),
        ("Salad", 90, 40, 1, 0),
    ]
    # Right column: two more dishes, clearly right of the midline.
    right_words = [
        ("Tiramisu", 800, 10, 2, 0),
        ("Cannoli", 800, 40, 3, 0),
    ]
    data = _make_data(left_words + right_words)
    text = reconstruct_text(data, image_width=1000)

    # Left column's dishes both come before either right-column dish —
    # no interleaving of dishes from different columns.
    assert (
        text.index("Margherita Pizza")
        < text.index("Caesar Salad")
        < text.index("Tiramisu")
        < text.index("Cannoli")
    )


def test_words_near_midline_prevent_false_column_split():
    # Words smeared roughly evenly across the width, including right at
    # the midpoint — this is single-column text, not two columns, even
    # though some words happen to fall on both sides of width/2.
    words = [
        ("The", 10, 10, 0, 0),
        ("quick", 200, 10, 0, 0),
        ("brown", 490, 10, 0, 0),  # sits right on the midline (500)
        ("fox", 700, 10, 0, 0),
        ("jumps", 900, 10, 0, 0),
    ]
    data = _make_data(words)
    text = reconstruct_text(data, image_width=1000)
    # If this were (incorrectly) split into columns, "brown" would be
    # ambiguous and the sentence would break apart. It shouldn't split.
    assert text == "The quick brown fox jumps"


def test_single_text_column_with_right_aligned_prices():
    """Regression: text column + decorative right half (no right-column text).

    Tesseract can assign every item to one block_num; row clustering must
    still recover one dish per line.
    """
    words = [
        ("MAIN", 80, 100, 0, 0), ("COURSE", 200, 100, 0, 0),
        ("Steak", 80, 150, 0, 0), ("$3.90", 480, 150, 0, 0),
        ("Tofu", 80, 200, 0, 0), ("$3.90", 480, 200, 0, 0),
        ("DRINKS", 80, 300, 0, 0),
        ("Lemonade", 80, 350, 0, 0), ("$4.90", 480, 350, 0, 0),
    ]
    data = _make_data(words)
    text = reconstruct_text(data, image_width=1200)
    from parser import parse_menu

    dishes = parse_menu(text)
    names = [d["name"] for d in dishes]
    assert "Steak" in names
    assert "Tofu" in names
    assert "Lemonade" in names
    assert len([d for d in dishes if d["price"] is not None]) == 3


def test_column_split_feeds_cleanly_into_parse_menu():
    """End-to-end sanity check: column-reconstructed text should parse
    into distinct, correctly-named dishes via the existing parser."""
    from parser import parse_menu

    left_words = [
        ("Margherita", 10, 10, 0, 0), ("Pizza", 110, 10, 0, 0),
        ("$12.99", 200, 10, 0, 0),
        ("Caesar", 10, 80, 1, 0), ("Salad", 90, 80, 1, 0),
        ("$8.00", 160, 80, 1, 0),
    ]
    right_words = [
        ("Tiramisu", 800, 10, 2, 0), ("$6.50", 900, 10, 2, 0),
        ("Cannoli", 800, 80, 3, 0), ("$4.00", 900, 80, 3, 0),
    ]
    data = _make_data(left_words + right_words)
    text = reconstruct_text(data, image_width=1000)

    dishes = parse_menu(text)
    names = [d["name"] for d in dishes]
    assert "Margherita Pizza" in names
    assert "Caesar Salad" in names
    assert "Tiramisu" in names
    assert "Cannoli" in names
    # None of the names should contain garbled cross-column text.
    for d in dishes:
        assert "$" not in d["name"]


def test_three_column_layout_is_read_column_first():
    # Three side-by-side columns; without gap clustering these would be
    # forced into a single midline split and interleaved incorrectly.
    col1 = [
        ("Soup", 20, 10, 0, 0),
        ("Bread", 20, 50, 1, 0),
    ]
    col2 = [
        ("Steak", 360, 10, 2, 0),
        ("Pasta", 360, 50, 3, 0),
    ]
    col3 = [
        ("Cake", 700, 10, 4, 0),
        ("Pie", 700, 50, 5, 0),
    ]
    data = _make_data(col1 + col2 + col3)
    text = reconstruct_text(data, image_width=1000)

    assert (
        text.index("Soup")
        < text.index("Bread")
        < text.index("Steak")
        < text.index("Pasta")
        < text.index("Cake")
        < text.index("Pie")
    )


def test_uneven_two_column_sidebar_and_main():
    # Narrow left sidebar (~15% width) + wide main column starting well
    # left of the image midline — the old midpoint heuristic often missed
    # this and fell back to single-column reading order.
    sidebar = [
        ("Wines", 30, 10, 0, 0),
        ("Beers", 30, 50, 1, 0),
    ]
    main = [
        ("Margherita", 280, 10, 2, 0),
        ("Pizza", 400, 10, 2, 0),
        ("Caesar", 280, 50, 3, 0),
        ("Salad", 380, 50, 3, 0),
    ]
    data = _make_data(sidebar + main)
    text = reconstruct_text(data, image_width=1000)

    assert (
        text.index("Wines")
        < text.index("Beers")
        < text.index("Margherita Pizza")
        < text.index("Caesar Salad")
    )


def test_three_column_menu_with_section_headers():
    """Three-column menu where each column has a section header and dishes.
    
    This tests the real-world scenario where a menu has STARTERS | MAINS | DESSERTS
    as separate columns, and ensures that dishes are correctly assigned to their
    section and that section headers from different columns don't interfere.
    """
    from parser import parse_menu

    # Column 1: STARTERS
    col1 = [
        ("STARTERS", 30, 20, 0, 0),
        ("Margherita", 30, 80, 1, 0),
        ("Pizza", 80, 80, 1, 0),
        ("$14", 160, 80, 1, 0),
        ("Caesar", 30, 140, 2, 0),
        ("Salad", 80, 140, 2, 0),
        ("$8", 160, 140, 2, 0),
    ]
    
    # Column 2: MAINS
    col2 = [
        ("MAINS", 330, 20, 3, 0),
        ("Grilled", 330, 80, 4, 0),
        ("Salmon", 380, 80, 4, 0),
        ("$26", 460, 80, 4, 0),
        ("Ribeye", 330, 140, 5, 0),
        ("Steak", 380, 140, 5, 0),
        ("$32", 460, 140, 5, 0),
    ]
    
    # Column 3: DESSERTS
    col3 = [
        ("DESSERTS", 600, 20, 6, 0),
        ("Tiramisu", 600, 80, 7, 0),
        ("$10", 720, 80, 7, 0),
        ("Cheesecake", 600, 140, 8, 0),
        ("$9", 720, 140, 8, 0),
    ]
    
    data = _make_data(col1 + col2 + col3)
    text = reconstruct_text(data, image_width=1000)

    # Verify that columns are read in the correct order (left to right, then down within each column)
    assert (
        text.index("STARTERS")
        < text.index("Margherita Pizza")
        < text.index("Caesar Salad")
        < text.index("MAINS")
        < text.index("Grilled Salmon")
        < text.index("Ribeye Steak")
        < text.index("DESSERTS")
        < text.index("Tiramisu")
        < text.index("Cheesecake")
    )

    # Verify section assignment via the parser
    dishes = parse_menu(text)
    
    # Find dishes by name
    margherita = next((d for d in dishes if "Margherita" in d["name"]), None)
    ribeye = next((d for d in dishes if "Ribeye" in d["name"]), None)
    tiramisu = next((d for d in dishes if "Tiramisu" in d["name"]), None)
    
    assert margherita is not None, "Margherita not found"
    assert ribeye is not None, "Ribeye not found"
    assert tiramisu is not None, "Tiramisu not found"
    
    # Verify sections
    assert margherita["section"] == "STARTERS", f"Margherita section is {margherita['section']}, expected STARTERS"
    assert ribeye["section"] == "MAINS", f"Ribeye section is {ribeye['section']}, expected MAINS"
    assert tiramisu["section"] == "DESSERTS", f"Tiramisu section is {tiramisu['section']}, expected DESSERTS"
    
    # Verify prices
    assert margherita["price"] == 14.0
    assert ribeye["price"] == 32.0
    assert tiramisu["price"] == 10.0


def test_orphan_price_row_merges_with_dish_above():
    """Right-aligned prices OCR'd on their own row must join the dish name."""
    words = [
        ("TIRAMISU", 600, 80, 7, 0),
        ("$10", 720, 110, 7, 1),
        ("CHEESECAKE", 600, 140, 8, 0),
        ("$9", 720, 170, 8, 1),
    ]
    data = _make_data(words)
    text = reconstruct_text(data, image_width=1000)

    from parser import parse_menu

    dishes = parse_menu(text)
    tiramisu = next((d for d in dishes if "TIRAMISU" in d["name"]), None)
    cheesecake = next((d for d in dishes if "CHEESECAKE" in d["name"]), None)
    assert tiramisu is not None
    assert cheesecake is not None
    assert tiramisu["price"] == 10.0
    assert cheesecake["price"] == 9.0


def test_price_fragment_column_merges_into_previous():
    """A pseudo-column of only prices must fold back into the dish column."""
    from parser import parse_menu

    names = [
        ("DESSERTS", 600, 20, 0, 0),
        ("TIRAMISU", 600, 80, 1, 0),
        ("CHEESECAKE", 600, 140, 2, 0),
    ]
    prices = [
        ("$10", 1050, 80, 3, 0),
        ("$9", 1050, 140, 4, 0),
    ]
    data = _make_data(names + prices)
    text = reconstruct_text(data, image_width=1200)
    dishes = parse_menu(text)
    desserts = [d for d in dishes if d.get("section") == "DESSERTS" and d.get("price")]
    assert len(desserts) >= 2
    assert any("TIRAMISU" in d["name"] for d in desserts)
    assert any("CHEESECAKE" in d["name"] for d in desserts)

