"""Add has_code_attr and xml_order columns to error_types

Revision ID: 053
Revises: 052
Create Date: 2025-11-21
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '053'
down_revision = '052'
branch_labels = None
depends_on = None

def upgrade():
    # Add columns for PQA reconstruction
    op.add_column('error_types', sa.Column('has_code_attr', sa.BOOLEAN, nullable=True, server_default='1'))
    op.add_column('error_types', sa.Column('xml_order', sa.INTEGER, nullable=True))


def downgrade():
    op.drop_column('error_types', 'has_code_attr')
    op.drop_column('error_types', 'xml_order')
