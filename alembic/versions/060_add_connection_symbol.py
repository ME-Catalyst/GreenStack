"""Add connection_symbol column to wire_configurations table

Revision ID: 060
Revises: 059
Create Date: 2025-01-21

PQA Fix #19: Store Connection@connectionSymbol attribute for accurate reconstruction
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '060'
down_revision = '059'
branch_labels = None
depends_on = None


def upgrade():
    """Add connection_symbol column to wire_configurations table"""
    op.add_column('wire_configurations', sa.Column('connection_symbol', sa.String(255), nullable=True))


def downgrade():
    """Remove connection_symbol column from wire_configurations table"""
    op.drop_column('wire_configurations', 'connection_symbol')
