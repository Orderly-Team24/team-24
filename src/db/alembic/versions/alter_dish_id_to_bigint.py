"""alter dish_id to bigint
Revision ID: alter_dish_id_bigint
Revises: e38340943a94, 31d0cd7df2bc
Create Date: 2026-07-17
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = 'alter_dish_id_bigint'
down_revision: Union[str, Sequence[str], None] = ('e38340943a94', '31d0cd7df2bc')
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.alter_column('order_history', 'dish_id',
                    existing_type=sa.Integer(),
                    type_=sa.BigInteger(),
                    existing_nullable=False)
    op.alter_column('dislikes', 'dish_id',
                    existing_type=sa.Integer(),
                    type_=sa.BigInteger(),
                    existing_nullable=False)

def downgrade() -> None:
    op.alter_column('dislikes', 'dish_id',
                    existing_type=sa.BigInteger(),
                    type_=sa.Integer(),
                    existing_nullable=False)
    op.alter_column('order_history', 'dish_id',
                    existing_type=sa.BigInteger(),
                    type_=sa.Integer(),
                    existing_nullable=False)
