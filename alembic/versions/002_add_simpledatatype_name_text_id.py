"""add simpledatatype_name_text_id column

Revision ID: 002_add_simpledatatype
Revises: 001_consolidated
Create Date: 2025-11-25

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '002_add_simpledatatype'
down_revision = '001_consolidated'
branch_labels = None
depends_on = None


def upgrade():
    # Add simpledatatype_name_text_id column to process_data_record_items table
    # This stores the textId of Name elements inside SimpleDatatype elements
    # Example: <RecordItem><SimpleDatatype><Name textId="TI_FOO"/></SimpleDatatype></RecordItem>
    with op.batch_alter_table('process_data_record_items', schema=None) as batch_op:
        batch_op.add_column(sa.Column('simpledatatype_name_text_id', sa.VARCHAR(255), nullable=True))


def downgrade():
    with op.batch_alter_table('process_data_record_items', schema=None) as batch_op:
        batch_op.drop_column('simpledatatype_name_text_id')
