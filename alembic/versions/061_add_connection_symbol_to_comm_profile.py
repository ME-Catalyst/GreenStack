"""Add connection_symbol column to communication_profile table

Revision ID: 061
Revises: 060
Create Date: 2025-01-21

PQA Fix #19b: Store Connection@connectionSymbol in communication_profile
for cases where Connection has no Wire children
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '061'
down_revision = '060'
branch_labels = None
depends_on = None


def upgrade():
    """Add connection_symbol column to communication_profile table"""
    op.add_column('communication_profile', sa.Column('connection_symbol', sa.String(255), nullable=True))


def downgrade():
    """Remove connection_symbol column from communication_profile table"""
    op.drop_column('communication_profile', 'connection_symbol')
