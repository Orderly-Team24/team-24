"""Budget filtering for recommendations.

Pulled out of `display_recommendations.py` so it's easy to unit-test in
isolation. The recommender returns a single dish from the stub pool (or
parser.py output once US-004-4 lands); this module decides which dishes
are eligible given the user's `max_budget`.
"""

from __future__ import annotations

import logging
from typing import Any, Iterable

logger = logging.getLogger(__name__)


def filter_by_budget(
    dishes: Iterable[dict[str, Any]],
    max_budget: float | None,
) -> list[dict[str, Any]]:
    """Return only dishes with `price <= max_budget`.

    Rules:
      - `max_budget` is None or <= 0 → no filtering, return the input as a list.
      - Dishes without a price (price is None or missing) are dropped when
        a budget is active — we can't tell if they fit, so we don't include
        them.
      - Dishes with `price == 0` are kept (they fit any budget).
      - Order is preserved from the input.

    Logs a warning when filtering returns an empty list.
    """
    dishes_list = list(dishes)
    if max_budget is None or max_budget <= 0:
        return dishes_list

    filtered = [d for d in dishes_list if d.get("price") is not None and float(d["price"]) <= max_budget]
    if not filtered:
        logger.warning("no dishes within budget=%s", max_budget)
    return filtered