"""Add xsi_type column to process_data_single_values and record_item_single_values tables

Revision ID: 088
Revises: 087
Create Date: 2025-11-24

PQA Fix #61: Store SingleValue xsi:type attribute (e.g., BooleanValueT)
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision = '088'
down_revision = '087'
branch_labels = None
depends_on = None


def upgrade():
    """Add xsi_type column to single value tables"""
    conn = op.get_bind()

    # Add to process_data_single_values
    result = conn.execute(sa.text("PRAGMA table_info(process_data_single_values)"))
    columns = [row[1] for row in result.fetchall()]
    if 'xsi_type' not in columns:
        op.add_column('process_data_single_values',
                      sa.Column('xsi_type', sa.VARCHAR(100), nullable=True))

    # Add to record_item_single_values
    result = conn.execute(sa.text("PRAGMA table_info(record_item_single_values)"))
    columns = [row[1] for row in result.fetchall()]
    if 'xsi_type' not in columns:
        op.add_column('record_item_single_values',
                      sa.Column('xsi_type', sa.VARCHAR(100), nullable=True))


def downgrade():
    """SQLite doesn't support DROP COLUMN directly"""
    pass
