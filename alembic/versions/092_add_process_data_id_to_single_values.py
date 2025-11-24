"""Add process_data_id column to process_data_single_values table

Revision ID: 092
Revises: 091
Create Date: 2025-11-24

PQA Fix #71: Support SingleValue elements that are direct children of
ProcessData/Datatype (not inside RecordItem)
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision = '092'
down_revision = '091'
branch_labels = None
depends_on = None


def upgrade():
    """Add process_data_id column to process_data_single_values table"""
    conn = op.get_bind()
    result = conn.execute(sa.text("PRAGMA table_info(process_data_single_values)"))
    columns = [row[1] for row in result.fetchall()]

    if 'process_data_id' not in columns:
        op.add_column('process_data_single_values',
                      sa.Column('process_data_id', sa.INTEGER, nullable=True))


def downgrade():
    """SQLite doesn't support DROP COLUMN directly"""
    pass
