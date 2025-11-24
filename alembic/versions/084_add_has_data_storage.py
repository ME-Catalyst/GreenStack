"""Add has_data_storage column to device_features table

Revision ID: 084
Revises: 083
Create Date: 2025-11-23

PQA Fix #57: Track whether dataStorage attribute was present in original IODD
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision = '084'
down_revision = '083'
branch_labels = None
depends_on = None


def upgrade():
    """Add has_data_storage column to device_features table"""
    conn = op.get_bind()
    result = conn.execute(sa.text("PRAGMA table_info(device_features)"))
    columns = [row[1] for row in result.fetchall()]

    if 'has_data_storage' not in columns:
        op.add_column('device_features',
                      sa.Column('has_data_storage', sa.INTEGER, nullable=True, server_default='0'))


def downgrade():
    """SQLite doesn't support DROP COLUMN directly"""
    pass
