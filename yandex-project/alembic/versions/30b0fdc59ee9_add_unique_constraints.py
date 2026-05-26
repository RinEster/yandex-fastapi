"""add unique constraints

Revision ID: 30b0fdc59ee9
Revises: d3b702079020
Create Date: 2026-05-26 05:37:10.540625

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '30b0fdc59ee9'
down_revision: Union[str, Sequence[str], None] = 'd3b702079020'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_unique_constraint(
        "uq_locations_name",
        "locations",
        ["name"],
        schema="public",
    )

    op.create_unique_constraint(
        "uq_categories_title",
        "categories",
        ["title"],
        schema="public",
    )

    op.create_unique_constraint(
        "uq_categories_slug",
        "categories",
        ["slug"],
        schema="public",
    )


def downgrade():
    op.drop_constraint(
        "uq_locations_name",
        "locations",
        schema="public",
        type_="unique",
    )

    op.drop_constraint(
        "uq_categories_title",
        "categories",
        schema="public",
        type_="unique",
    )

    op.drop_constraint(
        "uq_categories_slug",
        "categories",
        schema="public",
        type_="unique",
    )
