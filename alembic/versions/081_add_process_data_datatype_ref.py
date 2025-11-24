"""Add uses_datatype_ref and datatype_ref_id columns to process_data table

Revision ID: 081
Revises: 080
Create Date: 2025-11-23

PQA Fix #53: Track whether original IODD uses DatatypeRef vs inline Datatype
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision = '081'
down_revision = '080'
branch_labels = None
depends_on = None


def upgrade():
    """Add uses_datatype_ref and datatype_ref_id columns to process_data table"""
    conn = op.get_bind()
    result = conn.execute(sa.text("PRAGMA table_info(process_data)"))
    columns = [row[1] for row in result.fetchall()]

    if 'uses_datatype_ref' not in columns:
        op.add_column('process_data',
                      sa.Column('uses_datatype_ref', sa.INTEGER, nullable=True, server_default='0'))

    if 'datatype_ref_id' not in columns:
        op.add_column('process_data',
                      sa.Column('datatype_ref_id', sa.VARCHAR(100), nullable=True))


def downgrade():
    """SQLite doesn't support DROP COLUMN directly"""
    pass
