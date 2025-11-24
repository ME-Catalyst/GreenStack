"""Add mode column to events table

Revision ID: 079
Revises: 078
Create Date: 2025-11-23

PQA Fix #46: Event@mode attribute (e.g., AppearDisappear)
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision = '079'
down_revision = '078'
branch_labels = None
depends_on = None


def upgrade():
    """Add mode column to events table"""
    conn = op.get_bind()
    result = conn.execute(sa.text("PRAGMA table_info(events)"))
    columns = [row[1] for row in result.fetchall()]

    if 'mode' not in columns:
        op.add_column('events',
                      sa.Column('mode', sa.VARCHAR(100), nullable=True))


def downgrade():
    """SQLite doesn't support DROP COLUMN directly"""
    pass
