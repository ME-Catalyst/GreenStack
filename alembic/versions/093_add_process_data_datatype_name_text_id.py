"""Add datatype_name_text_id column to process_data table

Revision ID: 093
Revises: 092
Create Date: 2025-11-24

PQA Fix #72: Support ProcessData/Datatype/Name textId for devices that have
Name elements directly inside the Datatype element.
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision = '093'
down_revision = '092'
branch_labels = None
depends_on = None


def upgrade():
    """Add datatype_name_text_id column to process_data table"""
    conn = op.get_bind()
    result = conn.execute(sa.text("PRAGMA table_info(process_data)"))
    columns = [row[1] for row in result.fetchall()]

    if 'datatype_name_text_id' not in columns:
        op.add_column('process_data',
                      sa.Column('datatype_name_text_id', sa.TEXT, nullable=True))


def downgrade():
    """SQLite doesn't support DROP COLUMN directly"""
    pass
