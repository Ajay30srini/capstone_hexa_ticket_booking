"""add event status

Revision ID: 309882a5b204
Revises: 2f71cf737727
Create Date: 2026-02-28 14:37:15.940007

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '309882a5b204'
down_revision: Union[str, None] = '2f71cf737727'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "events",
        sa.Column("status", sa.String(length=20), nullable=False, server_default="draft"),
    )

    # If you want existing events to become visible immediately:
    op.execute("UPDATE events SET status='published' WHERE status='draft'")

    # optional: remove server_default so future inserts rely on app/model default
    op.alter_column("events", "status", server_default=None)

def downgrade() -> None:
    op.drop_column("events", "status")
