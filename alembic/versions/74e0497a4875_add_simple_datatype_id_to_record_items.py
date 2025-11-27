"""add_simple_datatype_id_to_record_items

Revision ID: 74e0497a4875
Revises: e785a3a7c71b
Create Date: 2025-11-27 12:26:43.576992

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '74e0497a4875'
down_revision = 'e785a3a7c71b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # PQA Fix: Add simple_datatype_id column to store SimpleDatatype@id attribute
    # This attribute is used in RecordItem/SimpleDatatype elements within custom datatypes
    # Example: <SimpleDatatype id="DT_6751acd8-dc8b-4bd3-a328-e58efed5d634" xsi:type="UIntegerT">
    with op.batch_alter_table('custom_datatype_record_items') as batch_op:
        batch_op.add_column(sa.Column('simple_datatype_id', sa.String(255), nullable=True))


def downgrade() -> None:
    with op.batch_alter_table('custom_datatype_record_items') as batch_op:
        batch_op.drop_column('simple_datatype_id')
