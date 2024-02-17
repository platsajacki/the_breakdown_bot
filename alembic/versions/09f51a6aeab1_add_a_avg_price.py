"""Add a avg_price.

Revision ID: 09f51a6aeab1
Revises: platsajacki
Create Date: 2024-02-16 14:35:09.641019

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '09f51a6aeab1'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    for table in ['tickers', 'unsuitable_levels', 'spent_levels']:
        op.add_column(table, sa.Column('avg_price', sa.Numeric(precision=21, scale=8), nullable=True))
        op.add_column(table, sa.Column('update_avg_price', sa.DateTime(), nullable=True))


def downgrade() -> None:
    pass
