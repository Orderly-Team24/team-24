import re

# $, €, £, ₽ before or after the number — see "Currencies и форматы цены"
# improvement note. The number itself accepts either a dot or a comma as
# the decimal separator ("12.50" or European-style "12,50").
_CURRENCY = r'[$€£₽]'
_PRICE_PATTERN = rf'{_CURRENCY}?\s*(\d+(?:[.,]\d{{1,2}})?)\s*{_CURRENCY}?'


def _find_price(line: str) -> tuple[float, str] | None:
    """Find a price in `line`. Returns (price, line_with_price_removed) or None."""
    match = re.search(_PRICE_PATTERN, line)
    if not match:
        return None
    price = float(match.group(1).replace(',', '.'))
    remainder = re.sub(_PRICE_PATTERN, '', line)
    remainder = re.sub(r'[.\-–]+', '', remainder).strip()
    return price, remainder


def parse_menu_line(line: str) -> dict:
    """
    Парсит одну строку меню и извлекает название блюда и цену.
    Поддерживает форматы: $10, 10$, $10.99, 10.99$, €10, £10, ₽350, 12,50€

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

    Real menus put the price in one of two places relative to the name:
      (a) stuck onto the end of the last description line, e.g.
          "Dish Name\nwith basil aioli and creme fraiche  7"
      (b) right next to the name itself, description below, e.g.
          "Dish Name  $10\nwith basil aioli and creme fraiche"
    We check the name line for a price first (case b) — if found, the rest
    of the block is pure description. Otherwise we fall back to searching
    the description lines for it (case a). Either way the name never gets
    overwritten by description text (the bug behind issue #283).
    """
    name_line, *rest = lines

    if not rest:
        found = _find_price(name_line)
        if found:
            price, name = found
            return {"name": name or name_line.strip(), "price": price, "description": "", "flagged": False}
        return {"name": name_line.strip(), "price": None, "description": "", "flagged": True}

    name_found = _find_price(name_line)
    if name_found:
        price, name = name_found
        description = " ".join(rest).strip()
        return {"name": name or name_line.strip(), "price": price, "description": description, "flagged": False}

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


def _looks_like_section_header(name: str) -> bool:
    """Heuristic: real menu section titles (STARTERS, DESSERTS, MAINS) are
    conventionally printed in caps. A dish whose OCR simply failed to catch
    a price (e.g. "Caesar Salad") keeps normal capitalization, so it won't
    get mistaken for a new section and silently swallow the real one.
    """
    letters = [c for c in name if c.isalpha()]
    return bool(letters) and all(c.isupper() for c in letters)


def parse_menu(raw_text: str) -> list:
    """
    Принимает сырой текст меню (после OCR) и возвращает список
    структурированных блюд в формате:
    [{name, price, description, flagged, section}, ...]

    Группирует строки в блоки по пустым строкам-разделителям, чтобы название
    блюда не путалось с его описанием, когда цена стоит в конце описания,
    а не рядом с названием (типичный случай для реальных сканов меню —
    см. issue #283).

    Также отслеживает разделы меню: блок без цены, состоящий из КАПСА
    (например "STARTERS", "DESSERTS"), становится активным разделом для
    всех следующих за ним блюд, пока не встретится следующий такой блок.
    Это позволяет AI-рекомендателю использовать раздел как доп. контекст
    (естественно сочетается с существующим meal-type фильтром в
    ai_service.py — десерт с большей вероятностью не предложат на завтрак).
    КАПС-эвристика специально отличает настоящий заголовок раздела от
    блюда, для которого OCR просто не распознал цену (например "Caesar
    Salad" без цены — это не новый раздел, а просто блюдо с пропуском).
    """
    blocks = _split_into_blocks(raw_text)
    results = []
    current_section: str | None = None
    for block in blocks:
        dish = _parse_block(block)
        dish["section"] = current_section
        results.append(dish)
        if dish["flagged"] and dish["price"] is None and _looks_like_section_header(dish["name"]):
            current_section = dish["name"]
    return results


if __name__ == "__main__":
    test_menu = """STARTERS

Margherita Pizza $12.99

Caesar Salad

Sundried Tomato Risotto Cakes
with basil aioli and creme fraiche 7

DESSERTS

Tiramisu
Classic Italian dessert 6,50€"""

    parsed = parse_menu(test_menu)
    for item in parsed:
        print(item)