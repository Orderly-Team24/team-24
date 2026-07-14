"""Turn Tesseract word-level OCR data into ordered menu text.

Plain ``pytesseract.image_to_string`` reads left-to-right across the full
image width. On a multi-column menu that interleaves words from different
columns on the same output line, so ``parser.py`` sees garbled text.

``image_to_data`` gives bounding boxes per word. We detect column layouts
by clustering non-price word left-edges across large horizontal gaps
(gutters), assign each word to a column *before* row clustering (so same-Y
rows from different columns do not merge), cluster words into horizontal
rows by Y coordinate, then group rows into blocks that ``parse_menu()``
understands.

Known limitation: if two rows from different columns share the exact same Y
coordinate, they are merged into one row before column splitting and may get
interleaved. Real menu photos usually have a few pixels of vertical offset.
Handwritten specials boards are still out of scope.
"""
from __future__ import annotations

import re

# Minimum horizontal gap (as a fraction of image width) between word boxes on
# the same row that starts a new column segment (a gutter, not word spacing).
_MIN_COLUMN_GAP_FRACTION = 0.08

# Floor for the column gutter in pixels (small images / unit tests).
_MIN_COLUMN_GAP_PX = 40

# Approx. px per character when Tesseract width is missing (unit tests).
_FALLBACK_CHAR_WIDTH = 7

# Minimum rows required in each column before we treat the page as multi-column.
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

    columns = _detect_columns(words, image_width)
    if columns is None:
        rows = _cluster_rows(words)
        return _column_rows_to_text(rows)

    parts = [
        _column_rows_to_text(_cluster_rows(col_words))
        for col_words in columns
    ]
    return "\n\n".join(part for part in parts if part)


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


def _word_center_x(word: dict) -> float:
    return word["left"] + word["width"] / 2


def _word_right(word: dict) -> float:
    width = word["width"]
    if width <= 0:
        width = max(len(word["text"]) * _FALLBACK_CHAR_WIDTH, 12)
    return word["left"] + width


def _is_price_word(text: str) -> bool:
    return bool(_PRICE_RE.search(text))


def _gap_threshold(image_width: int) -> float:
    return max(image_width * _MIN_COLUMN_GAP_FRACTION, _MIN_COLUMN_GAP_PX)


def _row_segment_anchors(row: list[dict], gap_threshold: float) -> list[float]:
    """Left-edges of each non-price segment in a row, split on gutters."""
    non_price = [w for w in row if not _is_price_word(w["text"])]
    if not non_price:
        return []

    ordered = sorted(non_price, key=lambda w: w["left"])
    anchors = [float(ordered[0]["left"])]
    prev_right = _word_right(ordered[0])
    for word in ordered[1:]:
        if word["left"] - prev_right >= gap_threshold:
            anchors.append(float(word["left"]))
        prev_right = max(prev_right, _word_right(word))
    return anchors


def _column_anchor_lefts(words: list[dict], image_width: int) -> list[float]:
    """Collect column-start X positions from provisional Y rows.

    Using per-row segment starts (not every word left-edge) avoids treating
    normal word spacing — e.g. "Margherita Pizza" or "MAIN COURSE" — as
    column gutters.
    """
    threshold = _gap_threshold(image_width)
    anchors: list[float] = []
    for row in _cluster_rows(words):
        anchors.extend(_row_segment_anchors(row, threshold))
    return anchors


def _find_column_boundaries(anchors: list[float], image_width: int) -> list[float]:
    """Return gutter X positions between columns, left-to-right."""
    if len(anchors) < 2:
        return []

    sorted_anchors = sorted(anchors)
    gap_threshold = _gap_threshold(image_width)

    boundaries: list[float] = []
    for i in range(len(sorted_anchors) - 1):
        left_a = sorted_anchors[i]
        left_b = sorted_anchors[i + 1]
        if left_b - left_a >= gap_threshold:
            boundaries.append((left_a + left_b) / 2)

    return boundaries


def _assign_words_to_columns(
    words: list[dict], boundaries: list[float]
) -> list[list[dict]]:
    """Split words into columns using gutter X boundaries (left → right)."""
    columns: list[list[dict]] = [[] for _ in range(len(boundaries) + 1)]
    for word in words:
        x = _word_center_x(word)
        col_idx = 0
        while col_idx < len(boundaries) and x >= boundaries[col_idx]:
            col_idx += 1
        columns[col_idx].append(word)
    return columns


def _detect_columns(words: list[dict], image_width: int) -> list[list[dict]] | None:
    """Return word lists per column (left → right), or None for single-column.

    Detects gutters from per-row non-price segment starts so right-aligned
    prices and intra-line word spacing are not mistaken for extra columns.
    Falls back to single-column when a candidate column lacks enough rows.
    """
    if image_width <= 0 or not words:
        return None

    anchors = _column_anchor_lefts(words, image_width)
    if len(anchors) < _MIN_ROWS_PER_COLUMN * 2:
        return None

    boundaries = _find_column_boundaries(anchors, image_width)
    if not boundaries:
        return None

    columns = _assign_words_to_columns(words, boundaries)
    if any(len(_cluster_rows(col)) < _MIN_ROWS_PER_COLUMN for col in columns):
        return None
    if any(not col for col in columns):
        return None

    return columns


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
