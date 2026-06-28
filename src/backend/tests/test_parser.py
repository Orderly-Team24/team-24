from parser import parse_menu_line, parse_menu


def test_price_with_dollar_before():
    result = parse_menu_line("Margherita Pizza $12.99")
    assert result["name"] == "Margherita Pizza"
    assert result["price"] == 12.99
    assert result["flagged"] == False
    print("PASSED: price with $ before number")


def test_price_with_dollar_after():
    result = parse_menu_line("Soup of the Day 5$")
    assert result["name"] == "Soup of the Day"
    assert result["price"] == 5.0
    assert result["flagged"] == False
    print("PASSED: price with $ after number")


def test_price_with_dots_separator():
    result = parse_menu_line("Pasta Carbonara.....15$")
    assert result["name"] == "Pasta Carbonara"
    assert result["price"] == 15.0
    assert result["flagged"] == False
    print("PASSED: price with dots separator")


def test_no_price_flagged():
    result = parse_menu_line("Caesar Salad")
    assert result["name"] == "Caesar Salad"
    assert result["price"] is None
    assert result["flagged"] == True
    print("PASSED: no price gets flagged")


def test_price_no_decimal():
    result = parse_menu_line("Soup $5")
    assert result["price"] == 5.0
    print("PASSED: price without decimal")


def test_full_menu_parsing():
    menu_text = """Margherita Pizza $12.99
Caesar Salad
Soup of the Day 5$
Pasta Carbonara.....15$"""

    results = parse_menu(menu_text)

    assert len(results) == 4
    assert results[0]["price"] == 12.99
    assert results[1]["flagged"] == True
    assert results[2]["price"] == 5.0
    assert results[3]["price"] == 15.0
    print("PASSED: full menu parsing")


def test_empty_lines_skipped():
    menu_text = """Pizza $10

Salad $5

"""
    results = parse_menu(menu_text)
    assert len(results) == 2
    print("PASSED: empty lines are skipped")


if __name__ == "__main__":
    test_price_with_dollar_before()
    test_price_with_dollar_after()
    test_price_with_dots_separator()
    test_no_price_flagged()
    test_price_no_decimal()
    test_full_menu_parsing()
    test_empty_lines_skipped()
    print("\nALL TESTS PASSED")