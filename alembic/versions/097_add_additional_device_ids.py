"""Add additional_device_ids column to devices table

Revision ID: 097
Revises: 096
Create Date: 2025-11-24

PQA Fix #85: Store additionalDeviceIds attribute from DeviceIdentity element.
This attribute contains space-separated additional device IDs.
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision = '097'
down_revision = '096'
branch_labels = None
depends_on = None


def upgrade():
    """Add additional_device_ids column to devices table"""
    conn = op.get_bind()
    result = conn.execute(sa.text("PRAGMA table_info(devices)"))
    columns = [row[1] for row in result.fetchall()]

    if 'additional_device_ids' not in columns:
        op.add_column('devices',
                      sa.Column('additional_device_ids', sa.TEXT, nullable=True))


def downgrade():
    """SQLite doesn't support DROP COLUMN directly"""
    pass
