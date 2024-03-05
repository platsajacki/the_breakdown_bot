"""Rename a avg_price.

Revision ID: 6484cbc21ca2
Revises: 09f51a6aeab1
Create Date: 2024-03-05 15:45:35.245913

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '6484cbc21ca2'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    for table in ['tickers', 'unsuitable_levels', 'spent_levels']:
        op.alter_column(table, 'avg_price', new_column_name='median_price')
        op.alter_column(table, 'update_avg_price', new_column_name='update_median_price')


def downgrade() -> None:
    for table in ['tickers', 'unsuitable_levels', 'spent_levels']:
        op.alter_column(table, 'median_price', new_column_name='avg_price')
        op.alter_column(table, 'update_median_price', new_column_name='update_avg_price')
