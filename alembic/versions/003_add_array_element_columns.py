"""add array_element columns to custom_datatypes

Revision ID: 003_add_array_element
Revises: 002_add_simpledatatype
Create Date: 2025-11-25

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '003_add_array_element'
down_revision = '002_add_simpledatatype'
branch_labels = None
depends_on = None


def upgrade():
    # Add array_element_type and array_element_bit_length columns to custom_datatypes table
    # These store the SimpleDatatype child element attributes for ArrayT custom datatypes
    # Example: <Datatype id="D_foo" xsi:type="ArrayT"><SimpleDatatype xsi:type="UIntegerT" bitLength="8"/></Datatype>
    with op.batch_alter_table('custom_datatypes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('array_element_type', sa.VARCHAR(50), nullable=True))
        batch_op.add_column(sa.Column('array_element_bit_length', sa.INTEGER, nullable=True))


def downgrade():
    with op.batch_alter_table('custom_datatypes', schema=None) as batch_op:
        batch_op.drop_column('array_element_bit_length')
        batch_op.drop_column('array_element_type')
