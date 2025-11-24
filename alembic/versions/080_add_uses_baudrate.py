"""Add uses_baudrate column to communication_profile table

Revision ID: 080
Revises: 079
Create Date: 2025-11-23

PQA Fix: Track whether original IODD used baudrate or bitrate attribute name
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision = '080'
down_revision = '079'
branch_labels = None
depends_on = None


def upgrade():
    """Add uses_baudrate column to communication_profile table"""
    conn = op.get_bind()
    result = conn.execute(sa.text("PRAGMA table_info(communication_profile)"))
    columns = [row[1] for row in result.fetchall()]

    if 'uses_baudrate' not in columns:
        op.add_column('communication_profile',
                      sa.Column('uses_baudrate', sa.INTEGER, nullable=True, server_default='1'))


def downgrade():
    """SQLite doesn't support DROP COLUMN directly"""
    pass
