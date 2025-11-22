"""Add wrapper_id column to process_data table

Revision ID: 059
Revises: 058
Create Date: 2025-01-21

PQA Fix #18: Store ProcessData wrapper ID for accurate reconstruction
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '059'
down_revision = '058'
branch_labels = None
depends_on = None


def upgrade():
    """Add wrapper_id column to process_data table"""
    op.add_column('process_data', sa.Column('wrapper_id', sa.String(255), nullable=True))


def downgrade():
    """Remove wrapper_id column from process_data table"""
    op.drop_column('process_data', 'wrapper_id')
