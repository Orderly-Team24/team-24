import re

_PRICE_PATTERN = r'\$?\s*(\d+(?:\.\d{1,2})?)\s*\$?'


def _find_price(line: str) -> tuple[float, str] | None:
    """Find a price in `line`. Returns (price, line_with_price_removed) or None."""
    match = re.search(_PRICE_PATTERN, line)
    if not match:
        return None
    price = float(match.group(1))
    remainder = re.sub(_PRICE_PATTERN, '', line)
    remainder = re.sub(r'[.\-–]+', '', remainder).strip()
    return price, remainder


def parse_menu_line(line: str) -> dict:
    """
    Парсит одну строку меню и извлекает название блюда и цену.
    Поддерживает форматы: $10, 10$, $10.99, 10.99$

    Для меню, где название и описание+цена лежат на разных строках
    (реальные сканы), используй parse_menu — он группирует строки в блоки.
    """
    found = _find_price(line)
    if found:
        price, name = found
        return {"name": name, "price": price, "flagged": False}
    return {"name": line.strip(), "price": None, "flagged": True}


def _split_into_blocks(raw_text: str) -> list[list[str]]:
    """Split OCR text into blocks of consecutive non-blank lines.

    Real scanned menus separate each dish (or section header) with a blank
    line — the one reliable signal for "new entry starts here".
    """
    blocks: list[list[str]] = []
    current: list[str] = []
    for raw_line in raw_text.split('\n'):
        line = raw_line.strip()
        if line:
            current.append(line)
        elif current:
            blocks.append(current)
            current = []
    if current:
        blocks.append(current)
    return blocks


def _parse_block(lines: list[str]) -> dict:
    """Parse one blank-line-delimited block into a single dish entry.

    Real menus put the dish name on its own line, then one or more
    description lines, with the price stuck onto the end of the last
    description line — e.g. "with basil aioli and creme fraiche  7".
    Line 0 is ALWAYS the name; price is only looked for in the remaining
    lines (or line 0 itself for single-line blocks), so description text
    never overwrites the real dish name (bug behind issue #283).
    """
    name_line, *rest = lines

    if not rest:
        found = _find_price(name_line)
        if found:
            price, name = found
            return {"name": name or name_line.strip(), "price": price, "description": "", "flagged": False}
        return {"name": name_line.strip(), "price": None, "description": "", "flagged": True}

    description_parts: list[str] = []
    price = None
    for line in rest:
        if price is None:
            found = _find_price(line)
            if found:
                price, remainder = found
                if remainder:
                    description_parts.append(remainder)
                continue
        description_parts.append(line)

    description = " ".join(description_parts).strip()

    return {
        "name": name_line.strip(),
        "price": price,
        "description": description,
        "flagged": price is None,
    }


def parse_menu(raw_text: str) -> list:
    """
    Принимает сырой текст меню (после OCR) и возвращает список
    структурированных блюд в формате [{name, price, description, flagged}, ...]

    Группирует строки в блоки по пустым строкам-разделителям, чтобы название
    блюда не путалось с его описанием, когда цена стоит в конце описания,
    а не рядом с названием (типичный случай для реальных сканов меню —
    см. issue #283).
    """
    blocks = _split_into_blocks(raw_text)
    return [_parse_block(block) for block in blocks]


if __name__ == "__main__":
    test_menu = """Margherita Pizza $12.99

Caesar Salad

Sundried Tomato Risotto Cakes
with basil aioli and creme fraiche 7

Sweet Onion Rings
Sweet Vidalias glazed with honey, deep fried
in beer batter 6"""

    parsed = parse_menu(test_menu)
    for item in parsed:
        print(item)