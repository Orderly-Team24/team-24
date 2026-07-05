from __future__ import annotations

import sys
from types import SimpleNamespace

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
            "cuisine": "Italian",
            "favorite_ingredients": ["tomato", "basil"],
            "exclude_ingredients": ["nuts", "shellfish"],
        },
        base_url="http://example.test/v1",
        api_key="test",
        model="qwen-test",
    )

    user_prompt = captured["messages"][1]["content"]
    assert "User preferences:" in user_prompt
    assert "- Cuisine: Italian" in user_prompt
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


def test_stub_filters_by_exclude_ingredients():
    pick = ai_service._stub(
        "",
        {"exclude_ingredients": ["salmon"]},
    )
    assert "salmon" not in [item.lower() for item in pick["ingredients"]]


def test_stub_filters_by_cuisine_when_possible():
    pick = ai_service._stub(
        "",
        {"cuisine": "Italian"},
    )
    assert pick["cuisine"] == "Italian"


def test_stub_falls_back_to_full_pool_when_preferences_filter_everything():
    pick = ai_service._stub(
        "",
        {
            "cuisine": "Martian",
            "exclude_ingredients": [
                "salmon",
                "mushroom",
                "chicken",
                "lentils",
                "tomato",
            ],
        },
    )
    assert pick in ai_service.FALLBACK_POOL


def test_endpoint_honors_preferences_in_stub_mode():
    resp = client.post(
        "/display/recommendations",
        json={
            "message": "",
            "preferences": {
                "cuisine": "Italian",
                "exclude_ingredients": ["tomato"],
            },
        },
    )
    assert resp.status_code == 200
    dish = resp.json()["recommendations"][0]
    assert dish["name"] == "Mushroom risotto"
    assert "tomato" not in [item.lower() for item in dish["ingredients"]]
