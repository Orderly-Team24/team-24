from __future__ import annotations

import sys
from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient

import ai_service
from main import app

client = TestClient(app)


def test_openai_compatible_prompt_includes_preferences(monkeypatch):
    captured = {}

    class FakeChatCompletions:
        def create(self, **kwargs):
            captured["messages"] = kwargs["messages"]
            return SimpleNamespace(
                choices=[
                    SimpleNamespace(
                        message=SimpleNamespace(
                            content=(
                                '{"name":"Margherita pizza","price":13,'
                                '"description":"Classic pizza",'
                                '"ingredients":["tomato","basil"],'
                                '"reason":"Matches preferences"}'
                            )
                        )
                    )
                ]
            )

    class FakeOpenAI:
        def __init__(self, **kwargs):
            self.chat = SimpleNamespace(
                completions=FakeChatCompletions()
            )

    monkeypatch.setitem(sys.modules, "openai", SimpleNamespace(OpenAI=FakeOpenAI))

    ai_service._openai_compatible(
        "Recommend dinner",
        {
            "favorite_ingredients": ["tomato", "basil"],
            "exclude_ingredients": ["nuts", "shellfish"],
        },
        base_url="http://example.test/v1",
        api_key="test",
        model="qwen-test",
    )

    user_prompt = captured["messages"][1]["content"]
    assert "User preferences:" in user_prompt
    assert "- Likes: tomato, basil" in user_prompt
    assert "- Excludes: nuts, shellfish" in user_prompt
    assert "Recommend a single dish matching these preferences." in user_prompt


def test_openai_compatible_prompt_includes_uploaded_menu(monkeypatch):
    """A menu (e.g. OCR'd from an uploaded photo) must reach the LLM prompt —
    previously _call_backend silently dropped it for any non-stub backend,
    so recommendations ignored the user's actual uploaded menu entirely."""
    captured = {}

    class FakeChatCompletions:
        def create(self, **kwargs):
            captured["messages"] = kwargs["messages"]
            return SimpleNamespace(
                choices=[
                    SimpleNamespace(
                        message=SimpleNamespace(
                            content=(
                                '{"name":"Pizza","price":10,"description":"",'
                                '"ingredients":[],"reason":"From your menu"}'
                            )
                        )
                    )
                ]
            )

    class FakeOpenAI:
        def __init__(self, **kwargs):
            self.chat = SimpleNamespace(completions=FakeChatCompletions())

    monkeypatch.setitem(sys.modules, "openai", SimpleNamespace(OpenAI=FakeOpenAI))

    ai_service._openai_compatible(
        "Recommend dinner",
        None,
        [{"name": "Pizza", "price": 10, "ingredients": ["cheese", "tomato"]}],
        base_url="http://example.test/v1",
        api_key="test",
        model="qwen-test",
    )

    user_prompt = captured["messages"][1]["content"]
    assert "Pizza" in user_prompt
    assert "$10" in user_prompt
    assert "cheese" in user_prompt


def test_call_backend_passes_menu_to_non_stub_backends(monkeypatch):
    """End-to-end: get_recommendation_struct with AI_BACKEND=openai must not
    drop the menu on the way to the backend function."""
    received = {}

    def fake_openai_backend(user_message, preferences=None, menu=None):
        received["menu"] = menu
        return {"name": "Pizza", "price": 10, "description": "", "ingredients": [], "reason": "ok"}

    monkeypatch.setenv("AI_BACKEND", "openai")
    monkeypatch.setitem(ai_service._BACKENDS, "openai", fake_openai_backend)

    menu = [{"name": "Pizza", "price": 10}]
    ai_service.get_recommendation_struct("Recommend dinner", None, menu)

    assert received["menu"] == menu


def test_get_recommendation_struct_rejects_llm_pick_that_ignores_excludes(monkeypatch):
    """Defense in depth: even if the configured backend (e.g. an LLM) returns
    a dish containing an excluded/allergen ingredient, it must never reach
    the caller — it should surface as AIServiceUnavailableError instead."""

    def fake_backend(user_message, preferences=None, menu=None):
        return {
            "name": "Peanut noodles",
            "price": 9,
            "description": "",
            "ingredients": ["peanut", "noodles"],
            "reason": "ok",
        }

    monkeypatch.setenv("AI_BACKEND", "openai")
    monkeypatch.setitem(ai_service._BACKENDS, "openai", fake_backend)

    try:
        with pytest.raises(ai_service.AIServiceUnavailableError):
            ai_service.get_recommendation_struct(
                "",
                {"exclude_ingredients": ["peanut"]},
            )
    finally:
        monkeypatch.delenv("AI_BACKEND", raising=False)


def test_stub_filters_by_exclude_ingredients():
    pick = ai_service._stub(
        "",
        {"exclude_ingredients": ["salmon"]},
    )
    assert "salmon" not in [item.lower() for item in pick["ingredients"]]


def test_stub_returns_none_when_every_dish_is_excluded():
    """Safety property: if excludes (allergens) remove every candidate dish,
    the stub must return no recommendation at all — never fall back to an
    unfiltered dish that could contain the allergen."""
    all_ingredients = {
        ingredient.lower()
        for dish in ai_service.FALLBACK_POOL
        for ingredient in dish["ingredients"]
    }
    pick = ai_service._stub(
        "",
        {"exclude_ingredients": sorted(all_ingredients)},
    )
    assert pick is None


def test_filter_returns_empty_when_excludes_remove_every_dish():
    pool = ai_service.filter_fallback_pool_by_preferences(
        [
            {"name": "Peanut noodles", "ingredients": ["peanut", "noodles"]},
            {"name": "Almond cake", "ingredients": ["almond", "flour", "sugar"]},
        ],
        {"exclude_ingredients": ["peanut", "almond"]},
    )
    assert pool == []


def test_filter_excludes_wins_over_same_ingredient_in_likes():
    """If the same ingredient is listed as both a like and an exclude
    (e.g. user mistakenly liked something they're allergic to), the
    exclude must win — likes are never used to override a hard exclude."""
    pool = ai_service.filter_fallback_pool_by_preferences(
        ai_service.FALLBACK_POOL,
        {"exclude_ingredients": ["salmon"], "favorite_ingredients": ["salmon"]},
    )
    assert pool
    assert all(
        "salmon" not in [i.lower() for i in dish["ingredients"]] for dish in pool
    )


def test_endpoint_honors_preferences_in_stub_mode():
    resp = client.post(
        "/display/recommendations",
        json={
            "message": "",
            "preferences": {
                "exclude_ingredients": ["tomato"],
            },
        },
    )
    assert resp.status_code == 200
    dish = resp.json()["recommendations"][0]
    assert dish["name"] == "Grilled salmon with lemon-dill sauce"
    assert "tomato" not in [item.lower() for item in dish["ingredients"]]


def test_endpoint_returns_empty_recommendations_when_all_dishes_excluded():
    """End-to-end safety check: if every dish on the (uploaded) menu contains
    an excluded ingredient, the endpoint must return an empty recommendation
    list — never a dish containing that ingredient."""
    resp = client.post(
        "/display/recommendations",
        json={
            "message": "",
            "menu": [
                {"name": "Peanut noodles", "price": 9, "ingredients": ["peanut", "noodles"]},
                {"name": "Almond cake", "price": 6, "ingredients": ["almond", "flour", "sugar"]},
            ],
            "preferences": {"exclude_ingredients": ["peanut", "almond"]},
        },
    )
    assert resp.status_code == 200
    assert resp.json()["recommendations"] == []


def test_endpoint_excludes_wins_over_same_ingredient_in_likes():
    resp = client.post(
        "/display/recommendations",
        json={
            "message": "",
            "preferences": {
                "exclude_ingredients": ["salmon"],
                "favorite_ingredients": ["salmon"],
            },
        },
    )
    assert resp.status_code == 200
    recs = resp.json()["recommendations"]
    assert recs
    assert "salmon" not in [item.lower() for item in recs[0]["ingredients"]]


# --- negation in the free-text mood/craving message ----------------------


@pytest.mark.parametrize(
    "message,expected",
    [
        ("I don't want steak today", ["steak"]),
        ("I don't want steak", ["steak"]),
        ("do not want shellfish please", ["shellfish"]),
        ("I'm not in the mood for pasta", ["pasta"]),
        ("not feeling sushi tonight", ["sushi"]),
        ("something light, without dairy", ["dairy"]),
        ("no nuts please", ["nuts"]),
        ("Surprise me!", []),
        ("", []),
    ],
)
def test_extract_negated_terms(message, expected):
    assert ai_service.extract_negated_terms(message) == expected


def test_endpoint_never_recommends_a_dish_the_user_said_they_dont_want():
    """Reproduces the reported bug: typing "I don't want steak" into the
    mood field must never result in a steak recommendation, even when steak
    is on the uploaded menu."""
    resp = client.post(
        "/display/recommendations",
        json={
            "message": "I don't want steak today",
            "menu": [
                {"name": "Ribeye steak", "price": 24, "ingredients": ["steak", "butter"]},
                {"name": "Grilled chicken", "price": 15, "ingredients": ["chicken", "herbs"]},
            ],
        },
    )
    assert resp.status_code == 200
    recs = resp.json()["recommendations"]
    assert recs
    assert recs[0]["name"] == "Grilled chicken"


def test_endpoint_returns_empty_when_every_menu_dish_is_the_unwanted_food():
    resp = client.post(
        "/display/recommendations",
        json={
            "message": "I don't want steak",
            "menu": [
                {"name": "Ribeye steak", "price": 24, "ingredients": ["steak", "butter"]},
                {"name": "Steak frites", "price": 20, "ingredients": ["steak", "potato"]},
            ],
        },
    )
    assert resp.status_code == 200
    assert resp.json()["recommendations"] == []


# --- LLM-backed negation extraction (supplement to the regex heuristic) ---


def test_llm_negation_extraction_is_a_noop_in_stub_mode(monkeypatch):
    monkeypatch.delenv("AI_BACKEND", raising=False)
    assert ai_service.extract_negated_terms_via_llm("keep it away from shellfish") == []


def test_llm_negation_extraction_disabled_via_env_var(monkeypatch):
    monkeypatch.setenv("AI_BACKEND", "openai")
    monkeypatch.setenv("OPENAI_API_KEY", "test")
    monkeypatch.setenv("NEGATION_LLM_EXTRACTION", "false")
    assert ai_service.extract_negated_terms_via_llm("keep it away from shellfish") == []


def test_llm_negation_extraction_parses_excluded_foods(monkeypatch):
    class FakeChatCompletions:
        def create(self, **kwargs):
            return SimpleNamespace(
                choices=[
                    SimpleNamespace(
                        message=SimpleNamespace(content='{"excluded": ["shellfish", "peanuts"]}')
                    )
                ]
            )

    class FakeOpenAI:
        def __init__(self, **kwargs):
            self.chat = SimpleNamespace(completions=FakeChatCompletions())

    monkeypatch.setitem(sys.modules, "openai", SimpleNamespace(OpenAI=FakeOpenAI))
    monkeypatch.setenv("AI_BACKEND", "openai")
    monkeypatch.setenv("OPENAI_API_KEY", "test")

    assert ai_service.extract_negated_terms_via_llm("keep it away from shellfish and peanuts") == [
        "shellfish",
        "peanuts",
    ]


def test_llm_negation_extraction_fails_silently(monkeypatch):
    class FakeChatCompletions:
        def create(self, **kwargs):
            raise RuntimeError("network error")

    class FakeOpenAI:
        def __init__(self, **kwargs):
            self.chat = SimpleNamespace(completions=FakeChatCompletions())

    monkeypatch.setitem(sys.modules, "openai", SimpleNamespace(OpenAI=FakeOpenAI))
    monkeypatch.setenv("AI_BACKEND", "openai")
    monkeypatch.setenv("OPENAI_API_KEY", "test")

    assert ai_service.extract_negated_terms_via_llm("anything") == []


def test_endpoint_merges_llm_negation_extraction_into_excludes(monkeypatch):
    """End-to-end: a phrasing the regex extractor misses ("keep it away
    from") still excludes the dish, when the LLM-backed extractor catches
    it."""
    class FakeChatCompletions:
        def create(self, **kwargs):
            return SimpleNamespace(
                choices=[
                    SimpleNamespace(message=SimpleNamespace(content='{"excluded": ["shellfish"]}'))
                ]
            )

    class FakeOpenAI:
        def __init__(self, **kwargs):
            self.chat = SimpleNamespace(completions=FakeChatCompletions())

    monkeypatch.setitem(sys.modules, "openai", SimpleNamespace(OpenAI=FakeOpenAI))
    monkeypatch.setenv("NEGATION_LLM_EXTRACTION", "true")
    # AI_BACKEND stays "stub" (default in tests) for the actual recommendation
    # call, so the pick itself is deterministic — only the extraction helper
    # needs a configured LLM backend to run.
    monkeypatch.setattr(ai_service, "_resolve_backend", lambda: ("stub", ai_service._stub))
    monkeypatch.setenv("AI_BACKEND", "openai")
    monkeypatch.setenv("OPENAI_API_KEY", "test")

    resp = client.post(
        "/display/recommendations",
        json={
            "message": "Keep it away from shellfish",
            "menu": [
                {"name": "Shrimp scampi", "price": 20, "ingredients": ["shellfish", "garlic"]},
                {"name": "Grilled chicken", "price": 15, "ingredients": ["chicken", "herbs"]},
            ],
        },
    )
    assert resp.status_code == 200
    recs = resp.json()["recommendations"]
    assert recs
    assert recs[0]["name"] == "Grilled chicken"


# --- meal type (breakfast/lunch/dinner) recognition -----------------------


@pytest.mark.parametrize(
    "message,expected",
    [
        ("Something for breakfast please", "breakfast"),
        ("I want brunch", "brunch"),
        ("What's good for lunch today?", "lunch"),
        ("Looking for dinner", "dinner"),
        ("Surprise me!", None),
        ("", None),
    ],
)
def test_extract_meal_type(message, expected):
    assert ai_service.extract_meal_type(message) == expected


def test_filter_by_meal_type_narrows_to_breakfast_dishes():
    pool = [
        {"name": "Ribeye steak", "description": "Grilled to order", "ingredients": ["steak"]},
        {"name": "Fluffy pancakes", "description": "With maple syrup", "ingredients": ["flour", "egg", "milk"]},
    ]
    result = ai_service.filter_by_meal_type(pool, "breakfast")
    assert result == [pool[1]]


def test_filter_by_meal_type_keeps_pool_unchanged_when_nothing_matches():
    pool = [{"name": "Ribeye steak", "description": "", "ingredients": ["steak"]}]
    assert ai_service.filter_by_meal_type(pool, "breakfast") == pool


def test_filter_by_meal_type_no_op_without_a_meal_type():
    pool = [{"name": "Ribeye steak", "description": "", "ingredients": ["steak"]}]
    assert ai_service.filter_by_meal_type(pool, None) == pool


def test_endpoint_prefers_breakfast_dish_when_breakfast_is_requested():
    resp = client.post(
        "/display/recommendations",
        json={
            "message": "Something for breakfast",
            "menu": [
                {"name": "Ribeye steak", "price": 24, "ingredients": ["steak", "butter"]},
                {"name": "Fluffy pancakes", "price": 9, "ingredients": ["flour", "egg", "milk"]},
            ],
        },
    )
    assert resp.status_code == 200
    recs = resp.json()["recommendations"]
    assert recs
    assert recs[0]["name"] == "Fluffy pancakes"
