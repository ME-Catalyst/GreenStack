"""Add string_fixed_length and string_encoding columns to custom_datatypes table

Revision ID: 086
Revises: 085
Create Date: 2025-11-23

PQA Fix #59: Store StringT/OctetStringT fixedLength and encoding attributes
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision = '086'
down_revision = '085'
branch_labels = None
depends_on = None


def upgrade():
    """Add string_fixed_length and string_encoding columns to custom_datatypes table"""
    conn = op.get_bind()
    result = conn.execute(sa.text("PRAGMA table_info(custom_datatypes)"))
    columns = [row[1] for row in result.fetchall()]

    if 'string_fixed_length' not in columns:
        op.add_column('custom_datatypes',
                      sa.Column('string_fixed_length', sa.INTEGER, nullable=True))

    if 'string_encoding' not in columns:
        op.add_column('custom_datatypes',
                      sa.Column('string_encoding', sa.VARCHAR(50), nullable=True))


def downgrade():
    """SQLite doesn't support DROP COLUMN directly"""
    pass
