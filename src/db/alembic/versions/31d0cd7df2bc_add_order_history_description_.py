"""add order_history description ingredients reason
Revision ID: 31d0cd7df2bc
Revises: cb41d1f4ba75
Create Date: 2026-07-14 22:48:01.275254
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

revision: str = '31d0cd7df2bc'
down_revision: Union[str, Sequence[str], None] = 'cb41d1f4ba75'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)
    existing_columns = [col['name'] for col in inspector.get_columns('order_history')]
    
    if 'description' not in existing_columns:
        op.add_column("order_history", sa.Column("description", sa.String(), nullable=True))
    if 'ingredients' not in existing_columns:
        op.add_column("order_history", sa.Column("ingredients", sa.JSON(), nullable=True))
    if 'reason' not in existing_columns:
        op.add_column("order_history", sa.Column("reason", sa.String(), nullable=True))

def downgrade() -> None:
    op.drop_column("order_history", "reason")
    op.drop_column("order_history", "ingredients")
    op.drop_column("order_history", "description")
