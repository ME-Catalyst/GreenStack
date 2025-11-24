"""Add xml_order column to custom_datatype_record_item_single_values table

Revision ID: 094
Revises: 093
Create Date: 2025-11-24

PQA Fix #74: Support xml_order for RecordItem SingleValues in DatatypeCollection
to preserve original XML element order during reconstruction.
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision = '094'
down_revision = '093'
branch_labels = None
depends_on = None


def upgrade():
    """Add xml_order column to custom_datatype_record_item_single_values table"""
    conn = op.get_bind()
    result = conn.execute(sa.text("PRAGMA table_info(custom_datatype_record_item_single_values)"))
    columns = [row[1] for row in result.fetchall()]

    if 'xml_order' not in columns:
        op.add_column('custom_datatype_record_item_single_values',
                      sa.Column('xml_order', sa.INTEGER, nullable=True))


def downgrade():
    """SQLite doesn't support DROP COLUMN directly"""
    pass
