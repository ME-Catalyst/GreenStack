"""add array_count to custom_datatypes and process_data tables

Revision ID: 004_add_array_count
Revises: 003_add_array_element
Create Date: 2025-11-25

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '004_add_array_count'
down_revision = '003_add_array_element'
branch_labels = None
depends_on = None


def upgrade():
    # Add array_count column to custom_datatypes table
    # Stores the count attribute for ArrayT custom datatypes
    # Example: <Datatype id="D_foo" xsi:type="ArrayT" count="12">...</Datatype>
    with op.batch_alter_table('custom_datatypes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('array_count', sa.INTEGER, nullable=True))

    # Add array_count column to process_data table
    # Stores the count attribute for ArrayT inline datatypes in ProcessData
    # Example: <ProcessDataOut id="PD_Out"><Datatype xsi:type="ArrayT" count="8">...</Datatype></ProcessDataOut>
    with op.batch_alter_table('process_data', schema=None) as batch_op:
        batch_op.add_column(sa.Column('array_count', sa.INTEGER, nullable=True))


def downgrade():
    with op.batch_alter_table('process_data', schema=None) as batch_op:
        batch_op.drop_column('array_count')

    with op.batch_alter_table('custom_datatypes', schema=None) as batch_op:
        batch_op.drop_column('array_count')
