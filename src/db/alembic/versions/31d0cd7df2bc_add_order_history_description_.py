"""add order_history description ingredients reason

Revision ID: 31d0cd7df2bc
Revises: cb41d1f4ba75
Create Date: 2026-07-14 22:48:01.275254

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '31d0cd7df2bc'
down_revision: Union[str, Sequence[str], None] = 'cb41d1f4ba75'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("order_history", sa.Column("description", sa.String(), nullable=True))
    op.add_column("order_history", sa.Column("ingredients", sa.JSON(), nullable=True))
    op.add_column("order_history", sa.Column("reason", sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("order_history", "reason")
    op.drop_column("order_history", "ingredients")
    op.drop_column("order_history", "description")
