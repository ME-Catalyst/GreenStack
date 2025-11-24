"""Add is_custom, name_text_id, description_text_id to error_types

Revision ID: 073
Revises: 072
Create Date: 2025-11-23

PQA Fix #37: Distinguish ErrorType (custom) vs StdErrorTypeRef (standard)
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision = '073'
down_revision = '072'
branch_labels = None
depends_on = None


def upgrade():
    """Add columns to error_types table"""
    conn = op.get_bind()
    result = conn.execute(sa.text("PRAGMA table_info(error_types)"))
    columns = [row[1] for row in result.fetchall()]

    if 'is_custom' not in columns:
        op.add_column('error_types',
                      sa.Column('is_custom', sa.BOOLEAN, nullable=True, default=0))

    if 'name_text_id' not in columns:
        op.add_column('error_types',
                      sa.Column('name_text_id', sa.VARCHAR(255), nullable=True))

    if 'description_text_id' not in columns:
        op.add_column('error_types',
                      sa.Column('description_text_id', sa.VARCHAR(255), nullable=True))


def downgrade():
    """SQLite doesn't support DROP COLUMN directly"""
    pass
