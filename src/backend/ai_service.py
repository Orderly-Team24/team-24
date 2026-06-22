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


# --- backend: stub ------------------------------------------------------


def _stub(user_message: str) -> dict[str, Any]:
    return _pick_fallback(user_message)


# --- backend: OpenAI / LM Studio ---------------------------------------
#
# Both expose the same OpenAI Chat Completions API, so we share the call.
# The prompt asks for a *single* JSON object matching our frontend schema,
# which keeps parsing simple and reliable.

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


def _openai_compatible(user_message: str, *, base_url: str, api_key: str, model: str) -> dict[str, Any]:
    """Call any OpenAI-compatible Chat Completions endpoint."""
    from openai import OpenAI

    client = OpenAI(base_url=base_url, api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": _OPENAI_SYSTEM_PROMPT},
            {"role": "user", "content": _OPENAI_USER_TEMPLATE.format(message=user_message or "")},
        ],
        temperature=0.7,
    )
    content = response.choices[0].message.content or ""
    return _extract_json_object(content)


def _openai_backend(user_message: str) -> dict[str, Any]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("AI_BACKEND=openai but OPENAI_API_KEY is not set")
    return _openai_compatible(
        user_message,
        base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
        api_key=api_key,
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
    )


def _lmstudio_backend(user_message: str) -> dict[str, Any]:
    base_url = os.getenv("LMSTUDIO_BASE_URL", "http://localhost:1234/v1")
    return _openai_compatible(
        user_message,
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


def _call_backend(user_message: str) -> tuple[str, dict[str, Any]]:
    """Call the configured backend with graceful fallback to the stub."""
    backend_name, fn = _resolve_backend()
    try:
        return backend_name, fn(user_message)
    except Exception as exc:
        logging.warning("AI backend %r failed: %s. Falling back to stub.", backend_name, exc)
        return "stub", _stub(user_message)


def get_recommendation(user_message: str) -> str:
    """Free-form one-line recommendation (legacy /recommend endpoint)."""
    _, pick = _call_backend(user_message)
    return f"{pick['name']} — ${float(pick['price']):.2f}. {pick['reason']}"


def get_recommendation_struct(user_message: str) -> dict[str, Any]:
    """Structured recommendation for /display/recommendations."""
    _, pick = _call_backend(user_message)
    return {
        "name":        str(pick.get("name", "Chef's special")),
        "price":       float(pick.get("price", 0) or 0),
        "description": str(pick.get("description", "")),
        "ingredients": list(pick.get("ingredients", []) or []),
        "reason":      str(pick.get("reason", "Recommended by AI")),
    }