"""create posts table

Revision ID: 0213b3cd8156
Revises: 
Create Date: 2026-10-07 07:30:29.171831

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '0213b3cd8156'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False,
                                       primary_key=True), sa.Column('title', sa.String(), nullable=False))
pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
