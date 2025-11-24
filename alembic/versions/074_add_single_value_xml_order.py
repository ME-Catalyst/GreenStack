"""Add xml_order to custom_datatype_single_values

Revision ID: 074
Revises: 073
Create Date: 2025-11-23

PQA Fix #38: DatatypeCollection/SingleValue ordering
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision = '074'
down_revision = '073'
branch_labels = None
depends_on = None


def upgrade():
    """Add xml_order column to custom_datatype_single_values table"""
    conn = op.get_bind()
    result = conn.execute(sa.text("PRAGMA table_info(custom_datatype_single_values)"))
    columns = [row[1] for row in result.fetchall()]

    if 'xml_order' not in columns:
        op.add_column('custom_datatype_single_values',
                      sa.Column('xml_order', sa.INTEGER, nullable=True))


def downgrade():
    """SQLite doesn't support DROP COLUMN directly"""
    pass
