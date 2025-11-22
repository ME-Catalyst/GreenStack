"""Add language_order column to iodd_text table for PQA reconstruction

Revision ID: 056
Revises: 055
Create Date: 2025-11-21
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '056'
down_revision = '055'
branch_labels = None
depends_on = None

def upgrade():
    # Add language_order column to preserve Language element ordering
    op.add_column('iodd_text', sa.Column('language_order', sa.INTEGER, nullable=True))


def downgrade():
    op.drop_column('iodd_text', 'language_order')
