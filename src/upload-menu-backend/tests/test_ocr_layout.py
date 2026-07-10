"""Unit tests for ocr_layout.reconstruct_text — pure logic, no real
Tesseract or image needed. We build synthetic `image_to_data`-shaped dicts
directly to control word positions and block numbering precisely.

Note on `block_num`: verified against a real menu photo, Tesseract assigns
one `block_num` per dish entry (name line + description line(s) together)
— NOT one block per physical line. Test fixtures below follow that: each
dish gets its own block_num, and a dish's own multiple lines share it.
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
    ]
    data = _make_data(left_words + right_words)
    text = reconstruct_text(data, image_width=1000)

    dishes = parse_menu(text)
    names = [d["name"] for d in dishes]
    assert "Margherita Pizza" in names
    assert "Caesar Salad" in names
    assert "Tiramisu" in names
    # None of the names should contain garbled cross-column text.
    for d in dishes:
        assert "$" not in d["name"]
