"""Add text_id and xsi_type columns for PQA accuracy

Revision ID: 028
Revises: 027
Create Date: 2024-11-20

This migration adds columns to preserve original IODD textId references
and xsi:type attributes for accurate PQA reconstruction.
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '028'
down_revision = '027'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add text_id and xsi_type columns for PQA reconstruction accuracy"""

    # Add text_id and xsi_type to custom_datatype_single_values
    # These preserve the original textId from Name element and xsi:type from SingleValue
    with op.batch_alter_table('custom_datatype_single_values') as batch_op:
        batch_op.add_column(sa.Column('text_id', sa.String(255), nullable=True))
        batch_op.add_column(sa.Column('xsi_type', sa.String(100), nullable=True))

    # Add name_text_id and description_text_id to device_variants
    # These preserve the original textId attributes from Name and Description elements
    with op.batch_alter_table('device_variants') as batch_op:
        batch_op.add_column(sa.Column('name_text_id', sa.String(255), nullable=True))
        batch_op.add_column(sa.Column('description_text_id', sa.String(255), nullable=True))

    # Add text_id to custom_datatype_record_items for Name textId preservation
    with op.batch_alter_table('custom_datatype_record_items') as batch_op:
        batch_op.add_column(sa.Column('name_text_id', sa.String(255), nullable=True))


def downgrade() -> None:
    """Remove added columns"""

    with op.batch_alter_table('custom_datatype_single_values') as batch_op:
        batch_op.drop_column('text_id')
        batch_op.drop_column('xsi_type')

    with op.batch_alter_table('device_variants') as batch_op:
        batch_op.drop_column('name_text_id')
        batch_op.drop_column('description_text_id')

    with op.batch_alter_table('custom_datatype_record_items') as batch_op:
        batch_op.drop_column('name_text_id')
