"""Add is_text_redefine column to iodd_text table

Revision ID: 090
Revises: 089
Create Date: 2025-11-24

PQA Fix #66: Track TextRedefine vs Text elements in ExternalTextCollection
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision = '090'
down_revision = '089'
branch_labels = None
depends_on = None


def upgrade():
    """Add is_text_redefine column to iodd_text table"""
    conn = op.get_bind()
    result = conn.execute(sa.text("PRAGMA table_info(iodd_text)"))
    columns = [row[1] for row in result.fetchall()]

    if 'is_text_redefine' not in columns:
        op.add_column('iodd_text',
                      sa.Column('is_text_redefine', sa.INTEGER, nullable=True, server_default='0'))


def downgrade():
    """SQLite doesn't support DROP COLUMN directly"""
    pass
