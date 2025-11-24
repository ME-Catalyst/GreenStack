"""Add std_record_item_ref_single_values table

Revision ID: 095
Revises: 094
Create Date: 2025-11-24

PQA Fix #76: Support SingleValue and StdSingleValueRef children of StdRecordItemRef
elements in StdVariableRef for proper IODD reconstruction.
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision = '095'
down_revision = '094'
branch_labels = None
depends_on = None


def upgrade():
    """Create std_record_item_ref_single_values table"""
    conn = op.get_bind()

    # Check if table already exists
    result = conn.execute(sa.text(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='std_record_item_ref_single_values'"
    ))
    if result.fetchone() is not None:
        return  # Table already exists

    op.create_table(
        'std_record_item_ref_single_values',
        sa.Column('id', sa.INTEGER, primary_key=True, autoincrement=True),
        sa.Column('std_record_item_ref_id', sa.INTEGER, nullable=False),
        sa.Column('value', sa.TEXT, nullable=False),
        sa.Column('name_text_id', sa.TEXT, nullable=True),
        sa.Column('is_std_ref', sa.INTEGER, nullable=False, default=0),  # 0=SingleValue, 1=StdSingleValueRef
        sa.Column('order_index', sa.INTEGER, nullable=True),
    )


def downgrade():
    """Drop std_record_item_ref_single_values table"""
    op.drop_table('std_record_item_ref_single_values')
