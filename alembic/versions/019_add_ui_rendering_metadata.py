"""Add UI rendering metadata tables and columns

Revision ID: 019
Revises: 018
Create Date: 2025-11-17

This migration adds critical UI rendering metadata for process data and menu items.
Includes gradient, offset, unit codes, and display formats required for proper
value scaling and display.
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '019'
down_revision = '018'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add UI rendering metadata tables and columns."""

    # Create process_data_ui_info table for ProcessDataRecordItemInfo
    op.create_table(
        'process_data_ui_info',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('process_data_id', sa.Integer(), nullable=False),
        sa.Column('subindex', sa.Integer(), nullable=False),
        sa.Column('gradient', sa.Float(), nullable=True),
        sa.Column('offset', sa.Float(), nullable=True),
        sa.Column('unit_code', sa.Text(), nullable=True),
        sa.Column('display_format', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['process_data_id'], ['process_data.id'],
                               name='fk_process_data_ui_info_process_data_id',
                               ondelete='CASCADE')
    )

    # Add gradient and offset columns to ui_menu_items for VariableRef UI attributes
    # Note: unit_code and display_format already exist in ui_menu_items
    op.add_column('ui_menu_items', sa.Column('gradient', sa.Float(), nullable=True))
    op.add_column('ui_menu_items', sa.Column('offset', sa.Float(), nullable=True))

    # Create index for faster lookups
    op.create_index('idx_process_data_ui_info_process_data_id',
                    'process_data_ui_info', ['process_data_id'])


def downgrade() -> None:
    """Remove UI rendering metadata tables and columns."""

    # Drop index
    op.drop_index('idx_process_data_ui_info_process_data_id',
                  table_name='process_data_ui_info')

    # Drop columns from ui_menu_items
    op.drop_column('ui_menu_items', 'offset')
    op.drop_column('ui_menu_items', 'gradient')

    # Drop process_data_ui_info table
    op.drop_table('process_data_ui_info')
