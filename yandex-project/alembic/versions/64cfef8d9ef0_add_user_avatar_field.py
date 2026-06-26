"""add_user_avatar_field

Revision ID: 64cfef8d9ef0
Revises: f57a8bdee863
Create Date: 2026-06-26 21:03:20.492127

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '64cfef8d9ef0'
down_revision: Union[str, Sequence[str], None] = 'f57a8bdee863'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Оставляем только команду добавления колонки в таблицу users
    op.add_column(
        'users', 
        sa.Column('avatar', sa.String(length=500), nullable=True), 
        schema='public'
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Оставляем только команду удаления колонки avatar в случае отката
    op.drop_column('users', 'avatar', schema='public')
