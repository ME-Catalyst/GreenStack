"""Add textId and order columns to events table for PQA

Revision ID: 040
Revises: 039
Create Date: 2025-11-21

This migration adds columns to store the original textId values and order
for Events, enabling accurate reconstruction without reverse-lookup.
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers
revision = '040'
down_revision = '039'
branch_labels = None
depends_on = None


def upgrade():
    # Add columns to events table for accurate PQA reconstruction
    op.add_column('events', sa.Column('name_text_id', sa.String(255), nullable=True))
    op.add_column('events', sa.Column('description_text_id', sa.String(255), nullable=True))
    op.add_column('events', sa.Column('order_index', sa.Integer(), nullable=True))


def downgrade():
    op.drop_column('events', 'order_index')
    op.drop_column('events', 'description_text_id')
    op.drop_column('events', 'name_text_id')
