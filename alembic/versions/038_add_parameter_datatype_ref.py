"""Add datatype_ref column to parameters table

Revision ID: 038
Revises: 037
Create Date: 2025-11-21

This migration adds a datatype_ref column to store the custom datatype ID
when a Variable uses DatatypeRef instead of inline Datatype.
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers
revision = '038'
down_revision = '037'
branch_labels = None
depends_on = None


def upgrade():
    # Add datatype_ref column to parameters table
    # This stores the datatypeId when a Variable uses DatatypeRef (e.g., D_Colors)
    # instead of inline Datatype element
    op.add_column('parameters', sa.Column('datatype_ref', sa.String(100), nullable=True))


def downgrade():
    op.drop_column('parameters', 'datatype_ref')
