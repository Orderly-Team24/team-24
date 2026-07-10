"""Turns Tesseract's word-level OCR data into ordered menu text, handling
the common 2-column menu layout.

Plain `pytesseract.image_to_string` reads left-to-right across the full
image width. On a 2-column menu that means words from the left and right
columns can end up interleaved on the same output "line", so `parser.py`
sees garbled text instead of two clean columns of dishes — this is the
"random symbols" symptom reported for multi-column menus.

`image_to_data` gives us each word's bounding box AND Tesseract's own
`block_num`/`line_num` segmentation, which (verified against a real menu
photo) already groups each dish's name + description into a single block.
So instead of inventing pixel-gap heuristics to detect where one dish ends
and another begins, we lean on Tesseract's own block boundaries directly,
and only add a layer on top to figure out which *column* each block
belongs to (by its horizontal position) and re-order blocks column-first
instead of Tesseract's raw top-to-bottom-across-the-whole-page order.

Scope note: this handles the common 2-column case (roughly left half /
right half of the page). 3+ columns, or columns that aren't roughly even
left/right splits, aren't handled by this heuristic and would need real
column clustering (e.g. k-means on block left-edges) — tracked as separate
follow-up work.
"""
from __future__ import annotations

# How close a block's left edge needs to be to the page midline before we
# stop trusting a left/right split (as a fraction of image width).
_MIDLINE_MARGIN_FRACTION = 0.06

# Fraction of blocks allowed to sit right on the midline before we conclude
# there's no real column gap there (i.e. it's actually single-column text).
_MIDLINE_DENSITY_THRESHOLD = 0.08


def reconstruct_text(data: dict, image_width: int) -> str:
    """Rebuild menu text from Tesseract `image_to_data` output.

    `data` is the dict `pytesseract.image_to_data(..., output_type=Output.DICT)`
    returns: parallel lists keyed by 'text', 'left', 'top', 'width',
    'height', 'block_num', 'par_num', 'line_num', and optionally 'conf'.
    """
    words = _extract_words(data)
    if not words:
        return ""

    blocks = _group_into_blocks(words)

    if not _looks_two_column(blocks, image_width):
        ordered = sorted(blocks, key=lambda b: b["top"])
        return _blocks_to_text(ordered)

    midpoint = image_width / 2
    left_blocks = sorted((b for b in blocks if b["left"] < midpoint), key=lambda b: b["top"])
    right_blocks = sorted((b for b in blocks if b["left"] >= midpoint), key=lambda b: b["top"])

    left_text = _blocks_to_text(left_blocks)
    right_text = _blocks_to_text(right_blocks)

    parts = [t for t in (left_text, right_text) if t]
    return "\n\n".join(parts)


def _extract_words(data: dict) -> list[dict]:
    texts = data.get("text", [])
    n = len(texts)
    confs = data.get("conf", [None] * n)
    heights = data.get("height", [20] * n)
    block_nums = data.get("block_num", [0] * n)
    par_nums = data.get("par_num", [0] * n)
    line_nums = data.get("line_num", [0] * n)

    words = []
    for i in range(n):
        text = (texts[i] or "").strip()
        if not text:
            continue
        # Skip explicit low-confidence noise; don't require a conf field.
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
                "height": heights[i] if i < len(heights) else 20,
                "block": block_nums[i] if i < len(block_nums) else 0,
                "par": par_nums[i] if i < len(par_nums) else 0,
                "line": line_nums[i] if i < len(line_nums) else 0,
            }
        )
    return words


def _group_into_blocks(words: list[dict]) -> list[dict]:
    """Group words by Tesseract's own block_num, and within each block by
    line_num — Tesseract already segments the page into paragraph-like
    blocks, which (per real-menu testing) line up with individual dish
    entries (name line + description line(s) sharing one block_num).

    Returns a list of {"left": ..., "top": ..., "lines": [[word, ...], ...]}
    — one entry per block, `lines` ordered top-to-bottom.
    """
    raw: dict[int, dict[int, list[dict]]] = {}
    for w in words:
        raw.setdefault(w["block"], {}).setdefault(w["line"], []).append(w)

    blocks = []
    for block_num, lines_by_num in raw.items():
        ordered_lines = [lines_by_num[ln] for ln in sorted(lines_by_num.keys())]
        all_words_in_block = [w for line in ordered_lines for w in line]
        blocks.append(
            {
                "left": min(w["left"] for w in all_words_in_block),
                "top": min(w["top"] for w in all_words_in_block),
                "lines": ordered_lines,
            }
        )
    return blocks


def _looks_two_column(blocks: list[dict], image_width: int) -> bool:
    """Only split into columns if there's a real visual gap around the
    page's horizontal midline AND blocks actually appear on both sides —
    otherwise a single-column menu would get needlessly (and incorrectly)
    chopped in half down the middle of its text.
    """
    if image_width <= 0 or not blocks:
        return False

    midpoint = image_width / 2
    has_left = any(b["left"] < midpoint for b in blocks)
    has_right = any(b["left"] >= midpoint for b in blocks)
    if not (has_left and has_right):
        return False

    margin = image_width * _MIDLINE_MARGIN_FRACTION
    near_midline = [b for b in blocks if abs(b["left"] - midpoint) < margin]
    return (len(near_midline) / len(blocks)) < _MIDLINE_DENSITY_THRESHOLD


def _blocks_to_text(blocks: list[dict]) -> str:
    """Render ordered blocks to text: lines within a block joined by a
    single newline, blocks separated by a blank line (the boundary
    parse_menu()'s block splitter expects).
    """
    rendered_blocks = []
    for block in blocks:
        line_texts = []
        for line_words in block["lines"]:
            ordered = sorted(line_words, key=lambda w: w["left"])
            line_texts.append(" ".join(w["text"] for w in ordered))
        rendered_blocks.append("\n".join(line_texts))
    return "\n\n".join(rendered_blocks)
