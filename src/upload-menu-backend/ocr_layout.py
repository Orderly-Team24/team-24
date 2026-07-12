"""Turn Tesseract word-level OCR data into ordered menu text.

Plain ``pytesseract.image_to_string`` reads left-to-right across the full
image width. On a 2-column menu that interleaves words from both columns on
the same output line, so ``parser.py`` sees garbled text.

``image_to_data`` gives bounding boxes per word. We detect true two-column
layouts from word positions, assign each word to a column *before* row
clustering (so same-Y rows from different columns do not merge), cluster
words into horizontal rows by Y coordinate, then group rows into blocks that
``parse_menu()`` understands.

Known limitation: if two rows from different columns share the exact same Y
coordinate, they are merged into one row before column splitting and may get
interleaved. Real menu photos usually have a few pixels of vertical offset.
"""
from __future__ import annotations

import re

# Fraction of image width: words/rows starting left of this are "left column".
_LEFT_COLUMN_MAX_FRACTION = 0.35
# Words/rows starting right of this are "right column".
_RIGHT_COLUMN_MIN_FRACTION = 0.45

# Minimum rows required on each side before we treat the page as two columns.
_MIN_ROWS_PER_COLUMN = 2

# Vertical gap between rows (× median line height) that starts a new block
# when price-based heuristics do not apply.
_LARGE_ROW_GAP_FACTOR = 1.8

_PRICE_RE = re.compile(r'[$€£₽]\s*\d|^\d+(?:[.,]\d{1,2})?\s*[$€£₽]')


def reconstruct_text(data: dict, image_width: int) -> str:
    """Rebuild menu text from Tesseract ``image_to_data`` output."""
    words = _extract_words(data)
    if not words:
        return ""

    split_x = _detect_column_split(words, image_width)
    if split_x is None:
        rows = _cluster_rows(words)
        return _column_rows_to_text(rows)

    left_words = [w for w in words if (w["left"] + w["width"] / 2) < split_x]
    right_words = [w for w in words if w not in left_words]

    left_text = _column_rows_to_text(_cluster_rows(left_words))
    right_text = _column_rows_to_text(_cluster_rows(right_words))
    parts = [t for t in (left_text, right_text) if t]
    return "\n\n".join(parts)


def _extract_words(data: dict) -> list[dict]:
    texts = data.get("text", [])
    n = len(texts)
    confs = data.get("conf", [None] * n)
    heights = data.get("height", [20] * n)
    widths = data.get("width", [0] * n)

    words = []
    for i in range(n):
        text = (texts[i] or "").strip()
        if not text:
            continue
        conf = confs[i] if i < len(confs) else None
        try:
            if conf is not None and 0 <= float(conf) < 10:
                continue
        except (TypeError, ValueError):
            pass
        words.append(
            {
                "text": text,
                "left": data["left"][i],
                "top": data["top"][i],
                "width": widths[i] if i < len(widths) else 0,
                "height": heights[i] if i < len(heights) else 20,
            }
        )
    return words


def _cluster_rows(words: list[dict]) -> list[list[dict]]:
    """Group words that share roughly the same baseline into one row."""
    if not words:
        return []

    heights = sorted(w["height"] for w in words)
    median_h = heights[len(heights) // 2]
    tolerance = max(int(median_h * 0.6), 8)

    sorted_words = sorted(words, key=lambda w: (w["top"], w["left"]))
    rows: list[list[dict]] = []
    current = [sorted_words[0]]
    anchor_y = sorted_words[0]["top"]

    for word in sorted_words[1:]:
        if abs(word["top"] - anchor_y) <= tolerance:
            current.append(word)
        else:
            rows.append(current)
            current = [word]
            anchor_y = word["top"]
    rows.append(current)
    return rows


def _detect_column_split(words: list[dict], image_width: int) -> float | None:
    """Return an X coordinate to split left/right columns, or None."""
    if image_width <= 0 or not words:
        return None

    left_thresh = image_width * _LEFT_COLUMN_MAX_FRACTION
    right_thresh = image_width * _RIGHT_COLUMN_MIN_FRACTION

    left_count = sum(1 for w in words if w["left"] < left_thresh)
    right_count = sum(1 for w in words if w["left"] > right_thresh)
    if left_count < _MIN_ROWS_PER_COLUMN or right_count < _MIN_ROWS_PER_COLUMN:
        return None

    split_x = image_width / 2
    left_words = [w for w in words if (w["left"] + w["width"] / 2) < split_x]
    right_words = [w for w in words if w not in left_words]
    if not left_words or not right_words:
        return None

    # Both columns must span multiple horizontal rows — a single full-width
    # sentence that happens to have a couple of words past the midpoint is
    # not a two-column menu.
    if len(_cluster_rows(left_words)) < _MIN_ROWS_PER_COLUMN:
        return None
    if len(_cluster_rows(right_words)) < _MIN_ROWS_PER_COLUMN:
        return None

    return split_x


def _row_to_text(row: list[dict]) -> str:
    ordered = sorted(row, key=lambda w: w["left"])
    return " ".join(w["text"] for w in ordered)


def _row_top_and_height(row: list[dict]) -> tuple[int, int]:
    top = min(w["top"] for w in row)
    height = max(w["height"] for w in row)
    return top, height


def _line_has_price(line: str) -> bool:
    return bool(_PRICE_RE.search(line))


def _looks_like_section_header(line: str) -> bool:
    letters = [c for c in line if c.isalpha()]
    return bool(letters) and all(c.isupper() for c in letters) and not _line_has_price(line)


def _should_start_new_block(
    current_block: list[str],
    new_line: str,
    *,
    large_vertical_gap: bool,
) -> bool:
    if not current_block:
        return False
    if large_vertical_gap:
        return True
    if _looks_like_section_header(new_line):
        return True
    if _line_has_price(new_line):
        if len(current_block) == 1 and _looks_like_section_header(current_block[0]):
            return True
        if any(_line_has_price(line) for line in current_block):
            return True
    if _line_has_price(current_block[-1]):
        return True
    return False


def _rows_to_blocks(rows: list[list[dict]]) -> list[list[str]]:
    blocks: list[list[str]] = []
    current: list[str] = []
    prev_bottom: int | None = None
    median_h = 20
    if rows:
        all_heights = sorted(w["height"] for row in rows for w in row)
        median_h = all_heights[len(all_heights) // 2]

    for row in rows:
        line = _row_to_text(row)
        top, height = _row_top_and_height(row)
        large_gap = (
            prev_bottom is not None
            and (top - prev_bottom) > median_h * _LARGE_ROW_GAP_FACTOR
        )

        if _should_start_new_block(current, line, large_vertical_gap=large_gap):
            blocks.append(current)
            current = [line]
        else:
            current.append(line)

        prev_bottom = top + height

    if current:
        blocks.append(current)
    return blocks


def _column_rows_to_text(rows: list[list[dict]]) -> str:
    blocks = _rows_to_blocks(rows)
    return "\n\n".join("\n".join(block) for block in blocks)
