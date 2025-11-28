"""add_direct_parameter_overlay_tables

Revision ID: e60240139ccc
Revises: b593adb623e2
Create Date: 2025-11-28 12:47:59.997627

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e60240139ccc'
down_revision = 'b593adb623e2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create direct_parameter_overlays table
    op.create_table(
        'direct_parameter_overlays',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('device_id', sa.Integer(), nullable=False),
        sa.Column('overlay_id', sa.String(100), nullable=False),
        sa.Column('access_rights', sa.String(10), nullable=True),
        sa.Column('dynamic', sa.Boolean(), nullable=True),
        sa.Column('modifies_other_variables', sa.Boolean(), nullable=True),
        sa.Column('excluded_from_data_storage', sa.Boolean(), nullable=True),
        sa.Column('name_text_id', sa.String(255), nullable=True),
        sa.Column('datatype_xsi_type', sa.String(50), nullable=True),
        sa.Column('datatype_bit_length', sa.Integer(), nullable=True),
        sa.Column('xml_order', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['device_id'], ['devices.id'], ondelete='CASCADE')
    )

    # Create direct_parameter_overlay_record_items table
    op.create_table(
        'direct_parameter_overlay_record_items',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('overlay_id', sa.Integer(), nullable=False),
        sa.Column('subindex', sa.Integer(), nullable=True),
        sa.Column('bit_offset', sa.Integer(), nullable=True),
        sa.Column('bit_length', sa.Integer(), nullable=True),
        sa.Column('datatype_ref', sa.String(100), nullable=True),
        sa.Column('simple_datatype', sa.String(50), nullable=True),
        sa.Column('name', sa.Text(), nullable=True),
        sa.Column('name_text_id', sa.String(255), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('description_text_id', sa.String(255), nullable=True),
        sa.Column('access_right_restriction', sa.String(50), nullable=True),
        sa.Column('order_index', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['overlay_id'], ['direct_parameter_overlays.id'], ondelete='CASCADE')
    )

    # Create direct_parameter_overlay_record_item_info table
    op.create_table(
        'direct_parameter_overlay_record_item_info',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('overlay_id', sa.Integer(), nullable=False),
        sa.Column('subindex', sa.Integer(), nullable=True),
        sa.Column('default_value', sa.Text(), nullable=True),
        sa.Column('modifies_other_variables', sa.Boolean(), nullable=True),
        sa.Column('order_index', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['overlay_id'], ['direct_parameter_overlays.id'], ondelete='CASCADE')
    )

    # Create direct_parameter_overlay_record_item_single_values table
    op.create_table(
        'direct_parameter_overlay_record_item_single_values',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('record_item_id', sa.Integer(), nullable=False),
        sa.Column('value', sa.String(255), nullable=True),
        sa.Column('name', sa.Text(), nullable=True),
        sa.Column('name_text_id', sa.String(255), nullable=True),
        sa.Column('order_index', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['record_item_id'], ['direct_parameter_overlay_record_items.id'], ondelete='CASCADE')
    )


def downgrade() -> None:
    op.drop_table('direct_parameter_overlay_record_item_single_values')
    op.drop_table('direct_parameter_overlay_record_item_info')
    op.drop_table('direct_parameter_overlay_record_items')
    op.drop_table('direct_parameter_overlays')
