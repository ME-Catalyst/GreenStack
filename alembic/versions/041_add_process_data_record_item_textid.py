"""Add name_text_id column to process_data_record_items table

Revision ID: 041
Revises: 040
Create Date: 2025-11-21

This migration adds name_text_id column to store the original textId value
for RecordItem Name elements, enabling accurate PQA reconstruction.
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers
revision = '041'
down_revision = '040'
branch_labels = None
depends_on = None


def upgrade():
    # Add name_text_id column for PQA reconstruction
    op.add_column('process_data_record_items',
                  sa.Column('name_text_id', sa.String(255), nullable=True))


def downgrade():
    op.drop_column('process_data_record_items', 'name_text_id')
