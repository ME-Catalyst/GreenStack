"""Add condition columns to ui_menu_items table

Revision ID: 043
Revises: 042
Create Date: 2025-11-21

This migration adds condition_variable_id and condition_value columns
to store MenuRef Condition elements for accurate PQA reconstruction.
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers
revision = '043'
down_revision = '042'
branch_labels = None
depends_on = None


def upgrade():
    # Add condition columns for MenuRef Condition elements
    op.add_column('ui_menu_items',
                  sa.Column('condition_variable_id', sa.String(255), nullable=True))
    op.add_column('ui_menu_items',
                  sa.Column('condition_value', sa.String(255), nullable=True))


def downgrade():
    op.drop_column('ui_menu_items', 'condition_value')
    op.drop_column('ui_menu_items', 'condition_variable_id')
