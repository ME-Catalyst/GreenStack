"""Add condition_subindex column to process_data_conditions

Revision ID: 052
Revises: 051
Create Date: 2025-11-21
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '052'
down_revision = '051'
branch_labels = None
depends_on = None

def upgrade():
    # Add subindex column for Condition elements
    op.add_column('process_data_conditions', sa.Column('condition_subindex', sa.VARCHAR(50), nullable=True))


def downgrade():
    op.drop_column('process_data_conditions', 'condition_subindex')
