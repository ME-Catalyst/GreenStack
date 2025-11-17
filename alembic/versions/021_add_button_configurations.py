"""Add button configurations for system commands

Revision ID: 021
Revises: 020
Create Date: 2025-11-17

This migration adds support for UI button configurations with action messages.
Enables system commands like factory reset, self-test, and firmware update operations.
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '021'
down_revision = '020'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add button configurations table."""

    # Create ui_menu_buttons table
    op.create_table(
        'ui_menu_buttons',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('menu_item_id', sa.Integer(), nullable=False),
        sa.Column('button_value', sa.Text(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('action_started_message', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['menu_item_id'], ['ui_menu_items.id'],
                               name='fk_ui_menu_buttons_menu_item_id',
                               ondelete='CASCADE')
    )

    # Create index for faster lookups
    op.create_index('idx_ui_menu_buttons_menu_item_id',
                    'ui_menu_buttons', ['menu_item_id'])


def downgrade() -> None:
    """Remove button configurations table."""

    # Drop index
    op.drop_index('idx_ui_menu_buttons_menu_item_id',
                  table_name='ui_menu_buttons')

    # Drop table
    op.drop_table('ui_menu_buttons')
