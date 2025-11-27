"""add_array_element_columns_to_process_data

Revision ID: 0280051d178a
Revises: 30e4d0b53871
Create Date: 2025-11-27 02:19:16.920789

Adds array_element_* columns to process_data table to support ArrayT process data
with SimpleDatatype children and ValueRange attributes.
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0280051d178a'
down_revision = '30e4d0b53871'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add array element columns to process_data table"""
    with op.batch_alter_table('process_data', schema=None) as batch_op:
        # ArrayT SimpleDatatype child attributes
        batch_op.add_column(sa.Column('array_element_type', sa.VARCHAR(50), nullable=True))
        batch_op.add_column(sa.Column('array_element_bit_length', sa.INTEGER, nullable=True))
        batch_op.add_column(sa.Column('array_element_fixed_length', sa.INTEGER, nullable=True))

        # ArrayT SimpleDatatype ValueRange attributes
        batch_op.add_column(sa.Column('array_element_min_value', sa.TEXT, nullable=True))
        batch_op.add_column(sa.Column('array_element_max_value', sa.TEXT, nullable=True))
        batch_op.add_column(sa.Column('array_element_value_range_xsi_type', sa.VARCHAR(100), nullable=True))
        batch_op.add_column(sa.Column('array_element_value_range_name_text_id', sa.TEXT, nullable=True))


def downgrade() -> None:
    """Remove array element columns from process_data table"""
    with op.batch_alter_table('process_data', schema=None) as batch_op:
        batch_op.drop_column('array_element_value_range_name_text_id')
        batch_op.drop_column('array_element_value_range_xsi_type')
        batch_op.drop_column('array_element_max_value')
        batch_op.drop_column('array_element_min_value')
        batch_op.drop_column('array_element_fixed_length')
        batch_op.drop_column('array_element_bit_length')
        batch_op.drop_column('array_element_type')
