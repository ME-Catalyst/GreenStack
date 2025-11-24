"""Add has_test_element column to communication_profile table

Revision ID: 098
Revises: 097
Create Date: 2025-11-24

PQA Fix #84: Track whether Test element was present in original IODD
(even if empty) to ensure accurate reconstruction.
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision = '098'
down_revision = '097'
branch_labels = None
depends_on = None


def upgrade():
    """Add has_test_element column to communication_profile table"""
    conn = op.get_bind()
    result = conn.execute(sa.text("PRAGMA table_info(communication_profile)"))
    columns = [row[1] for row in result.fetchall()]

    if 'has_test_element' not in columns:
        op.add_column('communication_profile',
                      sa.Column('has_test_element', sa.INTEGER, nullable=False, server_default='0'))


def downgrade():
    """SQLite doesn't support DROP COLUMN directly"""
    pass
