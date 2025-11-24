"""Add ProductName/ProductText fields and element presence flags to device_variants

Revision ID: 075
Revises: 074
Create Date: 2025-11-23

PQA Fix #40: DeviceVariant elements (Name vs ProductName, Description vs ProductText)
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision = '075'
down_revision = '074'
branch_labels = None
depends_on = None


def upgrade():
    """Add columns to device_variants table"""
    conn = op.get_bind()
    result = conn.execute(sa.text("PRAGMA table_info(device_variants)"))
    columns = [row[1] for row in result.fetchall()]

    # Add ProductName/ProductText text_id columns
    if 'product_name_text_id' not in columns:
        op.add_column('device_variants',
                      sa.Column('product_name_text_id', sa.VARCHAR(255), nullable=True))

    if 'product_text_text_id' not in columns:
        op.add_column('device_variants',
                      sa.Column('product_text_text_id', sa.VARCHAR(255), nullable=True))

    # Add element presence flags
    if 'has_name' not in columns:
        op.add_column('device_variants',
                      sa.Column('has_name', sa.BOOLEAN, nullable=True, default=0))

    if 'has_description' not in columns:
        op.add_column('device_variants',
                      sa.Column('has_description', sa.BOOLEAN, nullable=True, default=0))

    if 'has_product_name' not in columns:
        op.add_column('device_variants',
                      sa.Column('has_product_name', sa.BOOLEAN, nullable=True, default=0))

    if 'has_product_text' not in columns:
        op.add_column('device_variants',
                      sa.Column('has_product_text', sa.BOOLEAN, nullable=True, default=0))


def downgrade():
    """SQLite doesn't support DROP COLUMN directly"""
    pass
