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
        "cuisine": "American",
        "price": 18.50,
        "description": "Pan-seared Atlantic salmon, served with seasonal vegetables and jasmine rice.",
        "ingredients": ["salmon", "lemon", "dill", "rice", "asparagus"],
        "reason": "High protein, fits most budgets, no common allergens.",
    },
    {
        "name": "Mushroom risotto",
        "cuisine": "Italian",
        "price": 14.00,
        "description": "Creamy Arborio rice with porcini and cremini mushrooms, finished with parmesan.",
        "ingredients": ["arborio rice", "porcini", "cremini", "parmesan", "white wine"],
        "reason": "Vegetarian, comforting, no gluten.",
    },
    {
        "name": "Chicken pho",
        "cuisine": "Vietnamese",
        "price": 12.50,
        "description": "Vietnamese rice-noodle soup with poached chicken, herbs, and lime.",
        "ingredients": ["chicken", "rice noodles", "ginger", "star anise", "lime", "basil"],
        "reason": "Light, aromatic, easy on the stomach.",
    },
    {
        "name": "Lentil shepherd's pie",
        "cuisine": "British",
        "price": 11.00,
        "description": "Brown lentils and vegetables under a creamy mashed-potato crust.",
        "ingredients": ["lentils", "carrot", "onion", "potato", "tomato"],
        "reason": "Vegan, hearty, low cost.",
    },
    {
        "name": "Margherita pizza",
        "cuisine": "Italian",
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


def _pick_fallback_from_list(message: str, items: li