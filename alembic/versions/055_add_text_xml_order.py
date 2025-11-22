"""Add xml_order column to iodd_text table for PQA reconstruction

Revision ID: 055
Revises: 054
Create Date: 2025-11-21
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '055'
down_revision = '054'
branch_labels = None
depends_on = None

def upgrade():
    # Add xml_order column to preserve original Text element ordering
    op.add_column('iodd_text', sa.Column('xml_order', sa.INTEGER, nullable=True))


def downgrade():
    op.drop_column('iodd_text', 'xml_order')
