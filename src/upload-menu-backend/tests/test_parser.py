from parser import parse_menu_line, parse_menu


def test_price_with_dollar_before():
    result = parse_menu_line("Margherita Pizza $12.99")
    assert result["name"] == "Margherita Pizza"
    assert result["price"] == 12.99
    assert result["flagged"] == False


def test_price_with_dollar_after():
    result = parse_menu_line("Soup of the Day 5$")
    assert result["name"] == "Soup of the Day"
    assert result["price"] == 5.0
    assert result["flagged"] == False


def test_price_with_dots_separator():
    result = parse_menu_line("Pasta Carbonara.....15$")
    assert result["name"] == "Pasta Carbonara"
    assert result["price"] == 15.0
    assert result["flagged"] == False


def test_no_price_flagged():
    result = parse_menu_line("Caesar Salad")
    assert result["name"] == "Caesar Salad"
    assert result["price"] is None
    assert result["flagged"] == True


def test_price_no_decimal():
    result = parse_menu_line("Soup $5")
    assert result["price"] == 5.0


def test_full_menu_parsing():
    # Each dish separated by a blank line — the real signal a scanned menu
    # gives for "this is a new entry".
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


def test_empty_lines_skipped():
    menu_text = """Pizza $10

Salad $5

"""
    results = parse_menu(menu_text)
    assert len(results) == 2


# --- Regression tests for issue #283 -------------------------------------
# Real scanned menus put the name on its own line, description+price on the
# next line(s). The old line-by-line parser treated the description+price
# line as the whole dish, so the "name" that came back was garbled
# description text (e.g. "with basil aioli and creme fraiche" instead of
# "Sundried Tomato Risotto Cakes"). This is the leading suspected root
# cause of #283 ("second menu photo didn't work" — a different physical
# menu layout than the first photo tipped the parser into this bug).


def test_two_line_dish_name_not_mistaken_for_description():
    menu_text = """Sundried Tomato Risotto Cakes
with basil aioli and creme fraiche 7

Potato Skins
With melty mozzarella, cheddar and bacon 7"""

    results = parse_menu(menu_text)
    assert len(results) == 2

    assert results[0]["name"] == "Sundried Tomato Risotto Cakes"
    assert results[0]["price"] == 7.0
    assert results[0]["description"] == "with basil aioli and creme fraiche"
    assert results[0]["flagged"] == False

    assert results[1]["name"] == "Potato Skins"
    assert results[1]["price"] == 7.0
    assert "mozzarella" in results[1]["description"]


def test_multiline_description_before_price():
    menu_text = """Sweet Onion Rings
Sweet Vidalias glazed with honey, deep fried
in beer batter 6"""

    results = parse_menu(menu_text)
    assert len(results) == 1
    assert results[0]["name"] == "Sweet Onion Rings"
    assert results[0]["price"] == 6.0
    assert "glazed with honey" in results[0]["description"]
    assert "in beer batter" in results[0]["description"]


def test_section_header_with_no_price_is_flagged_alone():
    menu_text = """STARTERS

Buffalo Shrimp
Two skewers of grilled marinated shrimp 7"""

    results = parse_menu(menu_text)
    assert len(results) == 2
    assert results[0]["name"] == "STARTERS"
    assert results[0]["flagged"] is True
    assert results[1]["name"] == "Buffalo Shrimp"
    assert results[1]["price"] == 7.0