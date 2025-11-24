"""Add has_error_type_collection column to devices table

Revision ID: 083
Revises: 082
Create Date: 2025-11-23

PQA Fix #56: Track whether original IODD has ErrorTypeCollection (even if empty)
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision = '083'
down_revision = '082'
branch_labels = None
depends_on = None


def upgrade():
    """Add has_error_type_collection column to devices table"""
    conn = op.get_bind()
    result = conn.execute(sa.text("PRAGMA table_info(devices)"))
    columns = [row[1] for row in result.fetchall()]

    if 'has_error_type_collection' not in columns:
        op.add_column('devices',
                      sa.Column('has_error_type_collection', sa.INTEGER, nullable=True, server_default='0'))


def downgrade():
    """SQLite doesn't support DROP COLUMN directly"""
    pass
