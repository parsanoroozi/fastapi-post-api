"""add content comlumn

Revision ID: 2aad4409abf5
Revises: 0213b3cd8156
Create Date: 2026-10-07 07:34:25.915853

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2aad4409abf5'
down_revision: Union[str, Sequence[str], None] = '0213b3cd8156'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
