"""Add event_type column to events table

Revision ID: 015
Revises: 014
Create Date: 2025-11-17

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '015'
down_revision = '014'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add event_type column to events table."""

    # Add event_type column to events table
    op.add_column('events', sa.Column('event_type', sa.Text(), nullable=True))


def downgrade() -> None:
    """Remove event_type column from events table."""

    # Remove event_type column
    op.drop_column('events', 'event_type')
