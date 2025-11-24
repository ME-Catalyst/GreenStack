"""Add pd_ref_order column to process_data_ui_info for preserving ProcessDataRef order

Revision ID: 077
Revises: 076
Create Date: 2025-11-23

PQA Fix #42: ProcessDataRef@processDataId ordering - preserve original ProcessDataRef order
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision = '077'
down_revision = '076'
branch_labels = None
depends_on = None


def upgrade():
    """Add pd_ref_order column to process_data_ui_info table"""
    conn = op.get_bind()
    result = conn.execute(sa.text("PRAGMA table_info(process_data_ui_info)"))
    columns = [row[1] for row in result.fetchall()]

    if 'pd_ref_order' not in columns:
        op.add_column('process_data_ui_info',
                      sa.Column('pd_ref_order', sa.INTEGER, nullable=True))


def downgrade():
    """SQLite doesn't support DROP COLUMN directly"""
    pass
