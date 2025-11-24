"""Add datatype_has_bit_length column to process_data table

Revision ID: 096
Revises: 095
Create Date: 2025-11-24

PQA Fix #77: Track whether the original Datatype element had a bitLength attribute
to avoid adding it during reconstruction when it wasn't present in the original IODD.
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision = '096'
down_revision = '095'
branch_labels = None
depends_on = None


def upgrade():
    """Add datatype_has_bit_length column to process_data table"""
    conn = op.get_bind()
    result = conn.execute(sa.text("PRAGMA table_info(process_data)"))
    columns = [row[1] for row in result.fetchall()]

    if 'datatype_has_bit_length' not in columns:
        op.add_column('process_data',
                      sa.Column('datatype_has_bit_length', sa.INTEGER, nullable=False, server_default='0'))


def downgrade():
    """SQLite doesn't support DROP COLUMN directly"""
    pass
