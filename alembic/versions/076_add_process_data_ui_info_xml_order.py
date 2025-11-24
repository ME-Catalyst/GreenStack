"""Add xml_order column to process_data_ui_info for preserving original element order

Revision ID: 076
Revises: 075
Create Date: 2025-11-23

PQA Fix #41: ProcessDataRecordItemInfo ordering - preserve original XML element order
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision = '076'
down_revision = '075'
branch_labels = None
depends_on = None


def upgrade():
    """Add xml_order column to process_data_ui_info table"""
    conn = op.get_bind()
    result = conn.execute(sa.text("PRAGMA table_info(process_data_ui_info)"))
    columns = [row[1] for row in result.fetchall()]

    if 'xml_order' not in columns:
        op.add_column('process_data_ui_info',
                      sa.Column('xml_order', sa.INTEGER, nullable=True))


def downgrade():
    """SQLite doesn't support DROP COLUMN directly"""
    pass
