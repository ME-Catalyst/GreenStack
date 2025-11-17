"""Add all missing IODD tables

Revision ID: 017
Revises: 016
Create Date: 2025-11-17

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '017'
down_revision = '016'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create all missing IODD-related tables."""

    # Document info table
    op.create_table(
        'document_info',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('device_id', sa.Integer(), nullable=True),
        sa.Column('copyright', sa.Text(), nullable=True),
        sa.Column('release_date', sa.Text(), nullable=True),
        sa.Column('version', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['device_id'], ['devices.id'], name='fk_document_info_device_id')
    )

    # Device features table
    op.create_table(
        'device_features',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('device_id', sa.Integer(), nullable=True),
        sa.Column('block_parameter', sa.Integer(), nullable=True),
        sa.Column('data_storage', sa.Integer(), nullable=True),
        sa.Column('profile_characteristic', sa.Text(), nullable=True),
        sa.Column('access_locks_data_storage', sa.Integer(), nullable=True),
        sa.Column('access_locks_local_parameterization', sa.Integer(), nullable=True),
        sa.Column('access_locks_local_user_interface', sa.Integer(), nullable=True),
        sa.Column('access_locks_parameter', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['device_id'], ['devices.id'], name='fk_device_features_device_id')
    )

    # Communication profile table
    op.create_table(
        'communication_profile',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('device_id', sa.Integer(), nullable=True),
        sa.Column('iolink_revision', sa.Text(), nullable=True),
        sa.Column('compatible_with', sa.Text(), nullable=True),
        sa.Column('bitrate', sa.Text(), nullable=True),
        sa.Column('min_cycle_time', sa.Text(), nullable=True),
        sa.Column('msequence_capability', sa.Text(), nullable=True),
        sa.Column('sio_supported', sa.Integer(), nullable=True),
        sa.Column('connection_type', sa.Text(), nullable=True),
        sa.Column('wire_config', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['device_id'], ['devices.id'], name='fk_communication_profile_device_id')
    )

    # UI menus table
    op.create_table(
        'ui_menus',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('device_id', sa.Integer(), nullable=True),
        sa.Column('menu_id', sa.Text(), nullable=True),
        sa.Column('name', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['device_id'], ['devices.id'], name='fk_ui_menus_device_id')
    )

    # UI menu items table
    op.create_table(
        'ui_menu_items',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('menu_id', sa.Integer(), nullable=True),
        sa.Column('variable_id', sa.Text(), nullable=True),
        sa.Column('record_item_ref', sa.Text(), nullable=True),
        sa.Column('subindex', sa.Integer(), nullable=True),
        sa.Column('access_right_restriction', sa.Text(), nullable=True),
        sa.Column('display_format', sa.Text(), nullable=True),
        sa.Column('unit_code', sa.Text(), nullable=True),
        sa.Column('button_value', sa.Text(), nullable=True),
        sa.Column('menu_ref', sa.Text(), nullable=True),
        sa.Column('item_order', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['menu_id'], ['ui_menus.id'], name='fk_ui_menu_items_menu_id')
    )

    # UI menu roles table
    op.create_table(
        'ui_menu_roles',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('device_id', sa.Integer(), nullable=True),
        sa.Column('role_type', sa.Text(), nullable=True),
        sa.Column('menu_type', sa.Text(), nullable=True),
        sa.Column('menu_id', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['device_id'], ['devices.id'], name='fk_ui_menu_roles_device_id')
    )


def downgrade() -> None:
    """Drop all IODD-related tables."""

    op.drop_table('ui_menu_roles')
    op.drop_table('ui_menu_items')
    op.drop_table('ui_menus')
    op.drop_table('communication_profile')
    op.drop_table('device_features')
    op.drop_table('document_info')
