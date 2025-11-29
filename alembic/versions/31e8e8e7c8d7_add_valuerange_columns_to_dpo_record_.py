"""add_valuerange_columns_to_dpo_record_items

Revision ID: 31e8e8e7c8d7
Revises: 3080af74c43e
Create Date: 2025-11-28 23:16:56.557579

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '31e8e8e7c8d7'
down_revision = '3080af74c43e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # PQA Fix #137: Add missing ValueRange and SimpleDatatype columns
    # to direct_parameter_overlay_record_items table

    # ValueRange columns
    op.add_column('direct_parameter_overlay_record_items',
                  sa.Column('min_value', sa.String(255), nullable=True))
    op.add_column('direct_parameter_overlay_record_items',
                  sa.Column('max_value', sa.String(255), nullable=True))
    op.add_column('direct_parameter_overlay_record_items',
                  sa.Column('value_range_xsi_type', sa.String(255), nullable=True))
    op.add_column('direct_parameter_overlay_record_items',
                  sa.Column('value_range_name_text_id', sa.Text(), nullable=True))

    # Other SimpleDatatype attribute columns
    op.add_column('direct_parameter_overlay_record_items',
                  sa.Column('default_value', sa.Text(), nullable=True))
    op.add_column('direct_parameter_overlay_record_items',
                  sa.Column('fixed_length', sa.Integer(), nullable=True))
    op.add_column('direct_parameter_overlay_record_items',
                  sa.Column('encoding', sa.String(50), nullable=True))
    op.add_column('direct_parameter_overlay_record_items',
                  sa.Column('datatype_id', sa.String(100), nullable=True))


def downgrade() -> None:
    # Remove all added columns
    op.drop_column('direct_parameter_overlay_record_items', 'datatype_id')
    op.drop_column('direct_parameter_overlay_record_items', 'encoding')
    op.drop_column('direct_parameter_overlay_record_items', 'fixed_length')
    op.drop_column('direct_parameter_overlay_record_items', 'default_value')
    op.drop_column('direct_parameter_overlay_record_items', 'value_range_name_text_id')
    op.drop_column('direct_parameter_overlay_record_items', 'value_range_xsi_type')
    op.drop_column('direct_parameter_overlay_record_items', 'max_value')
    op.drop_column('direct_parameter_overlay_record_items', 'min_value')
