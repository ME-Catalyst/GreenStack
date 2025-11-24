"""Add connection_description_text_id to communication_profile

Revision ID: 072
Revises: 071
Create Date: 2025-11-23

PQA Fix #39: Connection/Description@textId missing
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision = '072'
down_revision = '071'
branch_labels = None
depends_on = None


def upgrade():
    """Add connection_description_text_id column to communication_profile table"""
    # Check if column exists first (SQLite limitation)
    conn = op.get_bind()
    result = conn.execute(sa.text("PRAGMA table_info(communication_profile)"))
    columns = [row[1] for row in result.fetchall()]

    if 'connection_description_text_id' not in columns:
        op.add_column('communication_profile',
                      sa.Column('connection_description_text_id', sa.VARCHAR(100), nullable=True))


def downgrade():
    """Remove connection_description_text_id column"""
    # SQLite doesn't support DROP COLUMN directly
    # For production, would need table recreation
    pass
