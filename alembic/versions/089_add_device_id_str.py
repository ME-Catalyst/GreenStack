"""Add device_id_str column to devices table

Revision ID: 089
Revises: 088
Create Date: 2025-11-24

PQA Fix #62: Store original deviceId string format (preserves leading zeros like "005")
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision = '089'
down_revision = '088'
branch_labels = None
depends_on = None


def upgrade():
    """Add device_id_str column to devices table"""
    conn = op.get_bind()
    result = conn.execute(sa.text("PRAGMA table_info(devices)"))
    columns = [row[1] for row in result.fetchall()]

    if 'device_id_str' not in columns:
        op.add_column('devices',
                      sa.Column('device_id_str', sa.VARCHAR(50), nullable=True))


def downgrade():
    """SQLite doesn't support DROP COLUMN directly"""
    pass
