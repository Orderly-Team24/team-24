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


def test_mid_line_quantity_is_not_a_price():
    """Regression: '12 oz ribeye' must not parse as $12."""
    result = parse_menu_line("12 oz ribeye, mashed potatoes")
    assert result["price"] is None
    assert result["flagged"] is True


def test_trailing_price_with_comma_after_currency():
    result = parse_menu_line("RIBEYE STEAK $32,")
    assert result["name"] == "RIBEYE STEAK"
    assert result["price"] == 32.0


def test_ocr_dollar_b_is_treated_as_eight():
    result = parse_menu_line("TIRAMISU $B")
    assert result["name"] == "TIRAMISU"
    assert result["price"] == 8.0


def test_merged_ocr_price_87_is_not_accepted():
    result = parse_menu_line("YORK CHEESECAKE 87")
    assert result["price"] is None
    assert result["flagged"] is True


def test_garbage_single_word_lowercase_is_flagged():
    results = parse_menu("DESSERTS\n\ngraham $8\n")
    graham = next(d for d in results if d["name"] == "graham")
    assert graham["flagged"] is True


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


# --- Currency symbols and European decimal comma --------------------------


def test_euro_symbol_before_and_after():
    assert parse_menu_line("Tiramisu €6.50")["price"] == 6.50
    assert parse_menu_line("Tiramisu 6.50€")["price"] == 6.50


def test_pound_and_ruble_symbols():
    assert parse_menu_line("Fish and Chips £9")["price"] == 9.0
    assert parse_menu_line("Borscht ₽350")["price"] == 350.0


def test_european_decimal_comma():
    result = parse_menu_line("Classic Italian dessert 6,50€")
    assert result["price"] == 6.50
    assert "6,50" not in result["name"]
    assert "€" not in result["name"]


def test_currency_symbol_stripped_from_name():
    result = parse_menu_line("Soup $5")
    assert "$" not in result["name"]


# --- Section context --------------------------------------------------


def test_section_attached_to_dishes_that_follow_a_header():
    menu_text = """STARTERS

Margherita Pizza $12.99

Caesar Salad

DESSERTS

Tiramisu
Classic Italian dessert 6,50€"""

    results = parse_menu(menu_text)

    headers = [r for r in results if r["name"] in ("STARTERS", "DESSERTS")]
    assert [h["section"] for h in headers] == [None, "STARTERS"]

    pizza = next(r for r in results if r["name"] == "Margherita Pizza")
    salad = next(r for r in results if r["name"] == "Caesar Salad")
    tiramisu = next(r for r in results if r["name"] == "Tiramisu")

    assert pizza["section"] == "STARTERS"
    assert salad["section"] == "STARTERS"
    assert tiramisu["section"] == "DESSERTS"


def test_section_is_none_before_any_header():
    menu_text = """Margherita Pizza $12.99

STARTERS

Caesar Salad"""

    results = parse_menu(menu_text)
    assert results[0]["section"] is None
    assert results[2]["section"] == "STARTERS"


def test_dish_with_missing_price_does_not_reset_section():
    """A dish whose price OCR failed to catch (e.g. "Caesar Salad" with no
    price on the photo) must NOT be mistaken for a new section header —
    only genuine ALL-CAPS section titles should do that."""
    menu_text = """STARTERS

Margherita Pizza $12.99

Caesar Salad

DESSERTS

Tiramisu $6"""

    results = parse_menu(menu_text)
    salad = next(r for r in results if r["name"] == "Caesar Salad")
    tiramisu = next(r for r in results if r["name"] == "Tiramisu")

    assert salad["section"] == "STARTERS"
    assert tiramisu["section"] == "DESSERTS"


def test_price_on_name_line_with_description_below():
    """Some menus put the price right next to the name, with the
    description on the following line(s) instead — the opposite order
    from the #283 layout. The price must still be found, and the name
    must not get swallowed by the description in either direction."""
    menu_text = """Dish Name $10
with basil aioli and creme fraiche"""

    results = parse_menu(menu_text)
    assert len(results) == 1
    assert results[0]["name"] == "Dish Name"
    assert results[0]["price"] == 10.0
    assert results[0]["description"] == "with basil aioli and creme fraiche"
    assert results[0]["flagged"] is False