"""Add ValueRange columns to custom_datatypes table

Revision ID: 070
Revises: 069
Create Date: 2025-11-22

PQA Fix #30b: Datatype elements in DatatypeCollection can have ValueRange
child elements with lowerValue, upperValue, xsi:type, and Name@textId.
This affects 35 issues.
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '070'
down_revision = '069'
branch_labels = None
depends_on = None


def upgrade():
    """Add ValueRange columns to custom_datatypes table"""
    try:
        op.add_column('custom_datatypes',
                      sa.Column('min_value', sa.Text(), nullable=True))
    except Exception:
        pass  # Column may already exist
    try:
        op.add_column('custom_datatypes',
                      sa.Column('max_value', sa.Text(), nullable=True))
    except Exception:
        pass
    try:
        op.add_column('custom_datatypes',
                      sa.Column('value_range_xsi_type', sa.Text(), nullable=True))
    except Exception:
        pass
    try:
        op.add_column('custom_datatypes',
                      sa.Column('value_range_name_text_id', sa.Text(), nullable=True))
    except Exception:
        pass


def downgrade():
    """Remove ValueRange columns"""
    try:
        op.drop_column('custom_datatypes', 'min_value')
    except Exception:
        pass
    try:
        op.drop_column('custom_datatypes', 'max_value')
    except Exception:
        pass
    try:
        op.drop_column('custom_datatypes', 'value_range_xsi_type')
    except Exception:
        pass
    try:
        op.drop_column('custom_datatypes', 'value_range_name_text_id')
    except Exception:
        pass
