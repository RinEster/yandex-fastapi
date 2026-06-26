"""add_post_bookmarks_table

Revision ID: bb923cc95e02
Revises: 64cfef8d9ef0
Create Date: 2026-06-26 21:42:20.139283

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bb923cc95e02'
down_revision: Union[str, Sequence[str], None] = '64cfef8d9ef0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
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
    op.drop_table('post_bookmarks', schema='public')
