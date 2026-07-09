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
import re
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


def _preference_value(preferences: Any, key: str, default: Any = None) -> Any:
    if preferences is None:
        return default
    if isinstance(preferences, dict):
        return preferences.get(key, default)
    return getattr(preferences, key, default)


def _clean_list(value: Any) -> list[str]:
    if not value:
        return []
    if isinstance(value, str):
        value = [value]
    return [str(item).strip() for item in value if str(item).strip()]


_NEGATION_PATTERNS = [
    re.compile(r"\b(?:don'?t|do not|doesn'?t|does not)\s+want\s+(.+?)(?:[.,;!?]|$)", re.IGNORECASE),
    re.compile(r"\bnot\s+(?:in the mood for|feeling)\s+(.+?)(?:[.,;!?]|$)", re.IGNORECASE),
    re.compile(r"\bwithout\s+(.+?)(?:[.,;!?]|$)", re.IGNORECASE),
    re.compile(r"\bno\s+(.+?)(?:[.,;!?]|$)", re.IGNORECASE),
]

_NEGATION_TRAILING_STOPWORDS = re.compile(
    r"\s+(?:and|or|but|today|tonight|please|thanks|thank you)\b.*$", re.IGNORECASE
)


def extract_negated_terms(message: str) -> list[str]:
    """Best-effort extraction of foods the user says they don't want, e.g.
    "I don't want steak today" -> ["steak"].

    This is a heuristic (regex, not real NLP) — it won't catch every possible
    phrasing. What it does catch gets merged into `exclude_ingredients` by
    the caller, so the existing hard exclude filter and post-hoc check
    (see `filter_fallback_pool_by_preferences` / `get_recommendation_struct`)
    apply to it exactly like an allergy: never recommend a matching dish.
    """
    if not message:
        return []

    terms: list[str] = []
    for pattern in _NEGATION_PATTERNS:
        for match in pattern.finditer(message):
            term = _NEGATION_TRAILING_STOPWORDS.sub("", match.group(1)).strip()
            if term and len(term.split()) <= 4:
                terms.append(term)
    return terms


def _format_preferences(preferences: Any) -> str:
    likes = _clean_list(
        _preference_value(
            preferences,
            "favorite_ingredients",
            _preference_value(preferences, "likes", []),
        )
    )
    excludes = _clean_list(
        _preference_value(
            preferences,
            "exclude_ingredients",
            _preference_value(preferences, "excludes", []),
        )
    )
    return (
        "User preferences:\n"
        f"- Likes: {', '.join(likes) if likes else 'None'}\n"
        f"- Excludes: {', '.join(excludes) if excludes else 'None'}\n\n"
        "Recommend a single dish matching these preferences."
    )


def _format_menu(menu: list[dict] | None) -> str:
    valid_items = [m for m in (menu or []) if not m.get("flagged")]
    if not valid_items:
        return ""

    lines = []
    for item in valid_items:
        price = item.get("price")
        price_str = f" (${price})" if price is not None else ""
        ingredients = item.get("ingredients") or []
        ingredients_str = f" — {', '.join(ingredients)}" if ingredients else ""
        lines.append(f"- {item.get('name', 'Unnamed dish')}{price_str}{ingredients_str}")

    return (
        "Available menu (recommend ONLY one dish from this list, copying its "
        "name and price exactly):\n" + "\n".join(lines) + "\n"
    )


def filter_fallback_pool_by_preferences(
    pool: list[dict[str, Any]],
    preferences: Any,
) -> list[dict[str, Any]]:
    """Filter the stub pool by excludes.

    Excludes (allergies and dislikes) are a hard safety constraint: if every
    dish contains an excluded ingredient, the result is an empty list — we
    never fall back to recommending an excluded dish just to have *something*
    to show.
    """
    candidates = list(pool)
    excludes = [item.lower() for item in _clean_list(_preference_value(preferences, "exclude_ingredients"))]
    if excludes:
        candidates = [
            dish
            for dish in candidates
            if not any(
                excluded in str(ingredient).lower()
                for excluded in excludes
                for ingredient in dish.get("ingredients", [])
            )
        ]
        if not candidates:
            return []

    return candidates


# --- backend: stub ------------------------------------------------------


def _stub(
    user_message: str,
    preferences: Any = None,
    menu: list[dict] | None = None,
) -> dict[str, Any] | None:
    if menu:
        valid_items = [m for m in menu if not m.get("flagged")]
        if valid_items:
            item = pick_from_pool(valid_items, user_message)
            return {
                "name": item["name"],
                "price": item["price"],
                "description": item.get("description", ""),
                "ingredients": item.get("ingredients", []),
                "reason": "Picked from your uploaded menu.",
            }

    pool = filter_fallback_pool_by_preferences(FALLBACK_POOL, preferences)
    if not pool:
        # Every fallback dish contains an excluded (e.g. allergen) ingredient —
        # no safe recommendation exists, so return none rather than picking
        # one anyway.
        return None
    return pick_from_pool(pool, user_message)


# --- backend: OpenAI / LM Studio ---------------------------------------
#
# Both expose the same OpenAI Chat Completions API, so we share the call.
# The prompt asks for a *single* JSON object matching our frontend schema,
# which keeps parsing simple and reliable.

_OPENAI_SYSTEM_PROMPT = (
    "You are Orderly, a food recommendation AI. "
    "If the user's request says they don't want, dislike, or aren't in the "
    'mood for something (e.g. "I don\'t want steak", "no seafood"), treat '
    "that exactly like an excluded ingredient in the preferences below — "
    "never recommend a dish containing it, even if nothing else matches as "
    "well. Excluded ingredients always take priority over liked ingredients. "
    "Always reply with exactly ONE JSON object, no prose, no markdown, "
    "matching this schema: "
    '{"name": str, "price": number, "description": str, '
    '"ingredients": [str], "reason": str}'
)

_OPENAI_USER_TEMPLATE = """User request: {message}

{menu}
{preferences}

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
    preferences: Any = None,
    menu: list[dict] | None = None,
    *,
    base_url: str,
    api_key: str,
    model: str,
) -> dict[str, Any]:
    """Call any OpenAI-compatible Chat Completions endpoint."""
    from openai import OpenAI

    client = OpenAI(base_url=base_url, api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": _OPENAI_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": _OPENAI_USER_TEMPLATE.format(
                    message=user_message or "",
                    menu=_format_menu(menu),
                    preferences=_format_preferences(preferences),
                ),
            },
        ],
        temperature=0.7,
    )
    content = response.choices[0].message.content or ""
    return _extract_json_object(content)


def _openai_backend(
    user_message: str,
    preferences: Any = None,
    menu: list[dict] | None = None,
) -> dict[str, Any]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("AI_BACKEND=openai but OPENAI_API_KEY is not set")
    return _openai_compatible(
        user_message,
        preferences,
        menu,
        base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
        api_key=api_key,
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
    )


def _lmstudio_backend(
    user_message: str,
    preferences: Any = None,
    menu: list[dict] | None = None,
) -> dict[str, Any]:
    base_url = os.getenv("LMSTUDIO_BASE_URL", "http://localhost:1234/v1")
    return _openai_compatible(
        user_message,
        preferences,
        menu,
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


class AIServiceUnavailableError(RuntimeError):
    """Raised when the configured AI backend is unreachable or returns an error.

    Callers must surface this as HTTP 503 — never silently fall back to a stub,
    because stub dishes ignore user allergens and preferences.
    """


def _call_backend(
    user_message: str,
    preferences: Any = None,
    menu: list[dict] | None = None,
) -> tuple[str, dict[str, Any]]:
    """Call the configured backend. Raises AIServiceUnavailableError on failure."""
    backend_name, fn = _resolve_backend()
    try:
        return backend_name, fn(user_message, preferences, menu)
    except AIServiceUnavailableError:
        raise
    except Exception as exc:
        logging.warning("AI backend %r failed: %s", backend_name, exc)
        raise AIServiceUnavailableError(str(exc)) from exc


def get_recommendation(user_message: str) -> str:
    """Free-form one-line recommendation (legacy /recommend endpoint)."""
    _, pick = _call_backend(user_message)
    return f"{pick['name']} — ${float(pick['price']):.2f}. {pick['reason']}"


def get_recommendation_struct(
    user_message: str,
    preferences: Any = None,
    menu: list[dict] | None = None,
) -> dict[str, Any] | None:
    """Structured recommendation for /display/recommendations.

    Raises AIServiceUnavailableError when the AI backend fails — callers must
    convert this to HTTP 503 and must not substitute a stub dish. Returns
    None when no dish satisfies the user's preferences (e.g. every candidate
    contains an excluded/allergen ingredient) — callers must treat this as
    "no recommendation", never substitute an unfiltered dish.
    """
    _, pick = _call_backend(user_message, preferences, menu)
    if not pick:
        return None

    # Defense in depth for LLM backends: the candidate pool passed to the
    # prompt is already excludes-free, but nothing stops a model from
    # ignoring the "pick only from this list" instruction. Never let an
    # excluded (e.g. allergen) ingredient reach the user regardless of which
    # backend produced the pick.
    excludes = [item.lower() for item in _clean_list(_preference_value(preferences, "exclude_ingredients"))]
    if excludes:
        pick_ingredients = [str(i).lower() for i in (pick.get("ingredients") or [])]
        if any(excluded in ingredient for excluded in excludes for ingredient in pick_ingredients):
            raise AIServiceUnavailableError(
                "AI recommendation contained an excluded ingredient"
            )

    return {
        "name":        str(pick.get("name", "Chef's special")),
        "price":       float(pick.get("price", 0) or 0),
        "description": str(pick.get("description", "")),
        "ingredients": list(pick.get("ingredients", []) or []),
        "reason":      str(pick.get("reason", "Recommended by AI")),
    }
