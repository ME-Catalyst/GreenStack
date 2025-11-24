"""Add hardware_revision and firmware_revision columns to device_variants table

Revision ID: 085
Revises: 084
Create Date: 2025-11-23

PQA Fix #58: Store DeviceVariant hardware/firmware revision attributes
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision = '085'
down_revision = '084'
branch_labels = None
depends_on = None


def upgrade():
    """Add hardware_revision and firmware_revision columns to device_variants table"""
    conn = op.get_bind()
    result = conn.execute(sa.text("PRAGMA table_info(device_variants)"))
    columns = [row[1] for row in result.fetchall()]

    if 'hardware_revision' not in columns:
        op.add_column('device_variants',
                      sa.Column('hardware_revision', sa.VARCHAR(50), nullable=True))

    if 'firmware_revision' not in columns:
        op.add_column('device_variants',
                      sa.Column('firmware_revision', sa.VARCHAR(50), nullable=True))


def downgrade():
    """SQLite doesn't support DROP COLUMN directly"""
    pass
