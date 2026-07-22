"""add dietary_preferences and order_history detail columns

Revision ID: e38340943a94
Revises: cb41d1f4ba75
Create Date: 2026-07-17 05:20:00.000000

The SQLAlchemy models (src/db/models.py) picked up two schema changes
without a migration to match: `Preferences.dietary_preferences` and
`OrderHistory.{description,ingredients,reason}`. In production this made
every `/auth/register` call fail with a 500 (INSERT into a column that
doesn't exist in the real Postgres table), which - because it's an
unhandled exception, not an HTTPException - skipped CORS headers on the
response and surfaced to users as a generic "Something went wrong" fetch
failure in the browser.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision: str = 'e38340943a94'
down_revision: Union[str, Sequence[str], None] = 'cb41d1f4ba75'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # This migration and 31d0cd7df2bc were authored independently (same
    # down_revision) and both add the same order_history columns. Guarding
    # on existing columns, same as 31d0cd7df2bc does, makes upgrading to
    # head from scratch (or from either branch alone) idempotent instead of
    # failing with "duplicate column name" partway through the merge.
    bind = op.get_bind()
    inspector = inspect(bind)

    existing_preferences_columns = [col['name'] for col in inspector.get_columns('preferences')]
    if 'dietary_preferences' not in existing_preferences_columns:
        op.add_column("preferences", sa.Column("dietary_preferences", sa.JSON(), nullable=True))

    existing_order_history_columns = [col['name'] for col in inspector.get_columns('order_history')]
    if 'description' not in existing_order_history_columns:
        op.add_column("order_history", sa.Column("description", sa.String(), nullable=True))
    if 'ingredients' not in existing_order_history_columns:
        op.add_column("order_history", sa.Column("ingredients", sa.JSON(), nullable=True))
    if 'reason' not in existing_order_history_columns:
        op.add_column("order_history", sa.Column("reason", sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column("order_history", "reason")
    op.drop_column("order_history", "ingredients")
    op.drop_column("order_history", "description")
    op.drop_column("preferences", "dietary_preferences")
