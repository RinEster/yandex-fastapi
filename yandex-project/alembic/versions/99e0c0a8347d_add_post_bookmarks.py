"""add_post_bookmarks

Revision ID: 99e0c0a8347d
Revises: bb923cc95e02
Create Date: 2026-06-26 21:53:03.618283

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '99e0c0a8347d'
down_revision: Union[str, Sequence[str], None] = 'bb923cc95e02'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'post_bookmarks',
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('post_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['post_id'], ['public.posts.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['public.users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('user_id', 'post_id'),
        schema='public'
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('post_bookmarks', schema='public')
