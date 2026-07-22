"""alter dish_id to bigint
Revision ID: 0001alter_dish
Revises: 31d0cd7df2bc
Create Date: 2026-07-17
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '0001alter_dish'
down_revision: Union[str, Sequence[str], None] = ('e38340943a94', '31d0cd7df2bc')
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Plain op.alter_column(..., type_=...) emits "ALTER COLUMN ... TYPE ...",
    # which SQLite's ALTER TABLE doesn't support at all (syntax error) —
    # every local/dev/test SQLite database was failing to reach `head`.
    # batch_alter_table recreates the table under the hood on SQLite and
    # behaves like a normal ALTER COLUMN on Postgres, so it works on both.
    with op.batch_alter_table('order_history') as batch_op:
        batch_op.alter_column('dish_id',
                        existing_type=sa.Integer(),
                        type_=sa.BigInteger(),
                        existing_nullable=False)
    with op.batch_alter_table('dislikes') as batch_op:
        batch_op.alter_column('dish_id',
                        existing_type=sa.Integer(),
                        type_=sa.BigInteger(),
                        existing_nullable=False)

def downgrade() -> None:
    with op.batch_alter_table('dislikes') as batch_op:
        batch_op.alter_column('dish_id',
                        existing_type=sa.BigInteger(),
                        type_=sa.Integer(),
                        existing_nullable=False)
    with op.batch_alter_table('order_history') as batch_op:
        batch_op.alter_column('dish_id',
                        existing_type=sa.BigInteger(),
                        type_=sa.Integer(),
                        existing_nullable=False)
