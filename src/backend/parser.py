import re


def parse_menu_line(line: str) -> dict:
    """
    Парсит одну строку меню и извлекает название блюда и цену.
    Поддерживает форматы: $10, 10$, $10.99, 10.99$
    """
    price_pattern = r'\$?\s*(\d+(?:\.\d{1,2})?)\s*\$?'
    match = re.search(price_pattern, line)

    if match:
        price = float(match.group(1))
        # Убираем найденную цену из строки, чтобы получить название
        name = re.sub(price_pattern, '', line)
        # Убираем мусорные символы (точки-разделители, тире)
        name = re.sub(r'[.\-–]+', '', name).strip()
        return {
            "name": name,
            "price": price,
            "flagged": False
        }
    else:
        # Цена не найдена — помечаем блюдо флагом
        return {
            "name": line.strip(),
            "price": None,
            "flagged": True
        }


def parse_menu(raw_text: str) -> list:
    """
    Принимает сырой текст меню (после OCR) и возвращает список
    структурированных блюд в формате [{name, price, flagged}, ...]
    """
    lines = raw_text.strip().split('\n')
    results = []
    for line in lines:
        if line.strip():  # пропускаем пустые строки
            results.append(parse_menu_line(line))
    return results


if __name__ == "__main__":
    # Быстрый тест парсера
    test_menu = """Margherita Pizza $12.99
Caesar Salad
Soup of the Day 5$
Pasta Carbonara.....15$"""

    parsed = parse_menu(test_menu)
    for item in parsed:
        print(item)