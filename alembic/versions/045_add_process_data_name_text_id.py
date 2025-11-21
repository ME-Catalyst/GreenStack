"""Add name_text_id and subindex_access_supported columns to process_data table

Revision ID: 045
Revises: 044
Create Date: 2025-11-21

This migration adds columns to the process_data table:
- name_text_id: Store original textId from IODD ProcessDataIn/Out Name elements
- subindex_access_supported: Store subindexAccessSupported attribute from Datatype

These are needed for accurate PQA reconstruction.
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = '045'
down_revision = '044'
branch_labels = None
depends_on = None


def upgrade():
    """Add name_text_id and subindex_access_supported columns to process_data table"""
    # Add name_text_id column to process_data table
    op.add_column('process_data', sa.Column('name_text_id', sa.String(255), nullable=True))
    # Add subindex_access_supported column (store as integer: NULL=not present, 0=false, 1=true)
    op.add_column('process_data', sa.Column('subindex_access_supported', sa.Boolean(), nullable=True))


def downgrade():
    """Remove name_text_id and subindex_access_supported columns from process_data table"""
    op.drop_column('process_data', 'name_text_id')
    op.drop_column('process_data', 'subindex_access_supported')
