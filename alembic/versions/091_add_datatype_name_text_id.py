"""Add datatype_name_text_id column to parameters table

Revision ID: 091
Revises: 090
Create Date: 2025-11-24

PQA Fix #70: Track Datatype/Name textId for Variables with direct Name children
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision = '091'
down_revision = '090'
branch_labels = None
depends_on = None


def upgrade():
    """Add datatype_name_text_id column to parameters table"""
    conn = op.get_bind()
    result = conn.execute(sa.text("PRAGMA table_info(parameters)"))
    columns = [row[1] for row in result.fetchall()]

    if 'datatype_name_text_id' not in columns:
        op.add_column('parameters',
                      sa.Column('datatype_name_text_id', sa.VARCHAR(255), nullable=True))


def downgrade():
    """SQLite doesn't support DROP COLUMN directly"""
    pass
