"""Add name_text_id column to ui_menus table

Revision ID: 042
Revises: 041
Create Date: 2025-11-21

This migration adds name_text_id column to store the original textId value
for Menu Name elements, enabling accurate PQA reconstruction without
reverse lookups that can match wrong textIds.
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers
revision = '042'
down_revision = '041'
branch_labels = None
depends_on = None


def upgrade():
    # Add name_text_id column for PQA reconstruction
    op.add_column('ui_menus',
                  sa.Column('name_text_id', sa.String(255), nullable=True))


def downgrade():
    op.drop_column('ui_menus', 'name_text_id')
