"""Add gradient_str and offset_str columns for preserving original format

Revision ID: 051
Revises: 050
Create Date: 2025-11-21
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '051'
down_revision = '050'
branch_labels = None
depends_on = None

def upgrade():
    # Add string columns to preserve original format
    op.add_column('ui_menu_items', sa.Column('gradient_str', sa.VARCHAR(50), nullable=True))
    op.add_column('ui_menu_items', sa.Column('offset_str', sa.VARCHAR(50), nullable=True))


def downgrade():
    op.drop_column('ui_menu_items', 'gradient_str')
    op.drop_column('ui_menu_items', 'offset_str')
