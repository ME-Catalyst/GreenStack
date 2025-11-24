"""Add gradient_str and offset_str columns to process_data_ui_info table

Revision ID: 087
Revises: 086
Create Date: 2025-11-24

PQA Fix #60b: Store original string format for gradient/offset attributes
to preserve exact formatting (e.g., "24" vs "24.0")
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision = '087'
down_revision = '086'
branch_labels = None
depends_on = None


def upgrade():
    """Add gradient_str and offset_str columns to process_data_ui_info table"""
    conn = op.get_bind()
    result = conn.execute(sa.text("PRAGMA table_info(process_data_ui_info)"))
    columns = [row[1] for row in result.fetchall()]

    if 'gradient_str' not in columns:
        op.add_column('process_data_ui_info',
                      sa.Column('gradient_str', sa.VARCHAR(50), nullable=True))

    if 'offset_str' not in columns:
        op.add_column('process_data_ui_info',
                      sa.Column('offset_str', sa.VARCHAR(50), nullable=True))


def downgrade():
    """SQLite doesn't support DROP COLUMN directly"""
    pass
