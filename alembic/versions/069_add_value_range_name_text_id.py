"""Add value_range_name_text_id column to RecordItem tables

Revision ID: 069
Revises: 068
Create Date: 2025-11-22

PQA Fix #30: ValueRange elements can have Name child elements with textId.
This affects 42+ issues across Variable, ProcessData, and DatatypeCollection.
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '069'
down_revision = '068'
branch_labels = None
depends_on = None


def upgrade():
    """Add value_range_name_text_id column to all RecordItem tables"""
    # Variable RecordItems
    try:
        op.add_column('parameter_record_items',
                      sa.Column('value_range_name_text_id', sa.Text(), nullable=True))
    except Exception:
        pass  # Column may already exist

    # ProcessData RecordItems
    try:
        op.add_column('process_data_record_items',
                      sa.Column('value_range_name_text_id', sa.Text(), nullable=True))
    except Exception:
        pass  # Column may already exist

    # DatatypeCollection RecordItems
    try:
        op.add_column('custom_datatype_record_items',
                      sa.Column('value_range_name_text_id', sa.Text(), nullable=True))
    except Exception:
        pass  # Column may already exist


def downgrade():
    """Remove value_range_name_text_id columns"""
    try:
        op.drop_column('parameter_record_items', 'value_range_name_text_id')
    except Exception:
        pass
    try:
        op.drop_column('process_data_record_items', 'value_range_name_text_id')
    except Exception:
        pass
    try:
        op.drop_column('custom_datatype_record_items', 'value_range_name_text_id')
    except Exception:
        pass
