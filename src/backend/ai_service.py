"""AI recommender.

Two backends, picked at import time by the ``AI_BACKEND`` env var:

- ``stub`` (default) — deterministic fake responses. Works anywhere, no setup.
- ``openai``         — real OpenAI API. Requires ``OPENAI_API_KEY``.
- ``lmstudio``       — local LM Studio OpenAI-compatible server. Requires
                       ``LMSTUDIO_BASE_URL`` (default http://localhost:1234/v1).

Switch via env:  AI_BACKEND=openai uvicorn main:app

The frontend contract is unchanged: a single recommended dish with name,
price, description, ingredients, reason.
"""

from __future__ import annotations

import logging
import os
from typing import Any

# --- shared "shape" of a recommendation ---------------------------------

# A small bank of plausible suggestions so the stub returns varied results.
FALLBACK_POOL = [
    {
        "name": "Grilled salmon with lemon-dill sauce",
        "price": 18.50,
        "description": "Pan-seared Atlantic salmon, served with seasonal vegetables and jasmine rice.",
        "ingredients": ["salmon", "lemon", "dill", "rice", "asparagus"],
        "reason": "High protein, fits most budgets, no common allergens.",
    },
    {
        "name": "Mushroom risotto",
        "price": 14.00,
        "description": "Creamy Arborio rice with porcini and cremini mushrooms, finished with parmesan.",
        "ingredients": ["arborio rice", "porcini", "cremini", "parmesan", "white wine"],
        "reason": "Vegetarian, comforting, no gluten.",
    },
    {
        "name": "Chicken pho",
        "price": 12.50,
        "description": "Vietnamese rice-noodle soup with poached chicken, herbs, and lime.",
        "ingredients": ["chicken", "rice noodles", "ginger", "star anise", "lime", "basil"],
        "reason": "Light, aromatic, easy on the stomach.",
    },
    {
        "name": "Lentil shepherd's pie",
        "price": 11.00,
        "description": "Brown lentils and vegetables under a creamy mashed-potato crust.",
        "ingredients": ["lentils", "carrot", "onion", "potato", "tomato"],
        "reason": "Vegan, hearty, low cost.",
    },
    {
        "name": "Margherita pizza",
        "price": 13.00,
        "description": "Wood-fired pizza with San Marzano tomato, fior di latte, and basil.",
        "ingredients": ["flour", "tomato", "mozzarella", "basil", "olive oil"],
        "reason": "Classic, balanced, vegetarian.",
    },
]


def _pick_fallback(message: str) -> dict[str, Any]:
    """Deterministic hash → index so the same query returns the same dish."""
    if not message:
        return FALLBACK_POOL[0]
    h = 0
    for ch in message.lower():
        h = (h * 31 + ord(ch)) & 0xFFFFFFFF
    return FALLBACK_POOL[h % len(FALLBACK_POOL)]


def pick_from_pool(pool: list[dict[str, Any]], message: str) -> dict[str, Any]:
    """Deterministic pick from a (possibly filtered) pool.

    `display_recommendations` uses this with a budget-filtered pool;
    `_stub` uses it with the full pool. Same hashing scheme as `_pick_fallback`.
    """
    if not pool:
        return _pick_fallback(message)
    if not message:
        return pool[0]
    h = 0
    for ch in message.lower():
        h = (h * 31 + ord(ch)) & 0xFFFFFFFF
    return pool[h % len(pool)]


def _pick_fallback_from_list(message: str, items: list[dict]) -> dict:
    """Same deterministic hash trick, but picks from the real uploaded menu."""
    if not message:
        return items[0]
    h = 0
    for ch in message.lower():
        h = (h * 31 + ord(ch)) & 0xFFFFFFFF
    return items[h % len(items)]

# --- backend: stub ------------------------------------------------------


def _stub(
    user_message: str,
    menu: list[dict] | None = None,
    preferences: dict | None = None
) -> dict:
    # Определяем исходный пул блюд
    if menu:
        source_pool = [m for m in menu if not m.get("flagged")]
    else:
        source_pool = _FALLBACK_POOL

    filtered_pool = source_pool

    
    if preferences and filtered_pool:
        exclude = [x.lower().strip() for x in preferences.get("exclude_ingredients", [])]
        cuisine = preferences.get("cuisine", "")

        
        if exclude:
            filtered_pool = [
                item for item in filtered_pool
                if not any(exc in [ing.lower() for ing in item.get("ingredients", [])] for exc in exclude)
                and not any(exc in item.get("name", "").lower() for exc in exclude)
            ]

        
        if cuisine:
            cuisine_lower = cuisine.lower().strip()
            filtered_pool = [
                item for item in filtered_pool
                if cuisine_lower in item.get("name", "").lower()
                or cuisine_lower in item.get("description", "").lower()
            ]

        
        if not filtered_pool:
            filtered_pool = source_pool

    if menu:
        item = _pick_fallback_from_list(user_message, filtered_pool)
        return {
            "name": item["name"],
            "price": item["price"],
            "description": item.get("description", ""),
            "ingredients": item.get("ingredients", []),
            "reason": "Picked from your uploaded menu based on preferences.",
        }

    return _pick_fallback_from_list(user_message, filtered_pool)


# --- backend: OpenAI / LM Studio ---------------------------------------

_OPENAI_SYSTEM_PROMPT = (
    "You are Orderly, a food recommendation AI. "
    "Always reply with exactly ONE JSON object, no prose, no markdown, "
    "matching this schema: "
    '{"name": str, "price": number, "description": str, '
    '"ingredients": [str], "reason": str}'
)

_OPENAI_USER_TEMPLATE = """User request: {message}

Return ONLY the JSON object, nothing else."""


def _extract_json_object(text: str) -> dict[str, Any]:
    """Best-effort JSON extraction from an LLM response."""
    text = text.strip()
    if text.startswith("```"):
        first_nl = text.find("\n")
        if first_nl != -1:
            text = text[first_nl + 1 :]
        if text.endswith("```"):
            text = text[: -3]
    start = text.find("{")
    if start == -1:
        raise ValueError(f"No JSON object in LLM response: {text!r}")
    depth = 0
    for i in range(start, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                import json
                return json.loads(text[start : i + 1])
    raise ValueError(f"Unbalanced JSON in LLM response: {text!r}")


def _openai_compatible(
    user_message: str,
    menu: list[dict] | None,
    preferences: dict | None = None,
    *,
    base_url: str,
    api_key: str,
    model: str,
) -> dict[str, Any]:
    """Call any OpenAI-compatible Chat Completions endpoint."""
    from openai import OpenAI
    import json

    client = OpenAI(base_url=base_url, api_key=api_key)
    valid_items = [m for m in (menu or []) if not m.get("flagged")]
    menu_text = json.dumps(valid_items, ensure_ascii=False) if valid_items else "[]"

    
    preferences_prompt = ""
    if preferences:
        cuisine = preferences.get("cuisine")
        exclude = preferences.get("exclude_ingredients", [])
        
        if cuisine or exclude:
            preferences_prompt = "\nUser preferences:\n"
            if cuisine:
                preferences_prompt += f"- Cuisine: {cuisine}\n"
            if exclude:
                preferences_prompt += f"- Excludes: {', '.join(exclude)}\n"

    
    user_content = _OPENAI_USER_TEMPLATE.format(message=user_message or "")
    if preferences_prompt:
        user_content += preferences_prompt
    user_content += f"\n\nMenu (only recommend dishes from this list, if non-empty): {menu_text}"

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": _OPENAI_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": user_content,
            },
        ],
        temperature=0.7,
    )
    content = response.choices[0].message.content or ""
    return _extract_json_object(content)


def _openai_backend(
    user_message: str,
    menu: list[dict] | None = None,
    preferences: dict | None = None
) -> dict[str, Any]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("AI_BACKEND=openai but OPENAI_API_KEY is not set")
    return _openai_compatible(
        user_message,
        menu,
        preferences,
        base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
        api_key=api_key,
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
    )


def _lmstudio_backend(
    user_message: str,
    menu: list[dict] | None = None,
    preferences: dict | None = None
) -> dict[str, Any]:
    base_url = os.getenv("LMSTUDIO_BASE_URL", "http://localhost:1234/v1")
    return _openai_compatible(
        user_message,
        menu,
        preferences,
        base_url=base_url,
        api_key=os.getenv("LMSTUDIO_API_KEY", "lm-studio"),
        model=os.getenv("LMSTUDIO_MODEL", "qwen/qwen3.5-9b"),
    )


# --- public API ---------------------------------------------------------


_BACKENDS = {
    "stub":     _stub,
    "openai":   _openai_backend,
    "lmstudio": _lmstudio_backend,
}


def _resolve_backend():
    name = os.getenv("AI_BACKEND", "stub").lower().strip()
    fn = _BACKENDS.get(name)
    if fn is None:
        raise RuntimeError(f"Unknown AI_BACKEND={name!r}. Choose from {list(_BACKENDS)}")
    return name, fn


def _call_backend(
    user_message: str,
    menu: list[dict] | None = None,
    preferences: dict | None = None
) -> tuple[str, dict[str, Any]]:
    """Call the configured backend with graceful fallback to the stub."""
    backend_name, fn = _resolve_backend()
    try:
        return backend_name, fn(user_message, menu, preferences)
    except Exception as exc:
        logging.warning("AI backend %r failed: %s. Falling back to stub.", backend_name, exc)
        return "stub", _stub(user_message, menu, preferences)


def get_recommendation(user_message: str) -> str:
    """Free-form one-line recommendation (legacy /recommend endpoint)."""
    _, pick = _call_backend(user_message)
    return f"{pick['name']} — ${float(pick['price']):.2f}. {pick['reason']}"


def get_recommendation_struct(
    user_message: str,
    menu: list[dict] | None = None,
    preferences: dict | None = None
) -> dict:
    """Structured recommendation for /display/recommendations."""
    _, pick = _call_backend(user_message, menu, preferences)
    return {
        "name":        str(pick.get("name", "Chef's special")),
        "price":       float(pick.get("price", 0) or 0),
        "description": str(pick.get("description", "")),
        "ingredients": list(pick.get("ingredients", []) or []),
        "reason":      str(pick.get("reason", "Recommended by AI")),
    }