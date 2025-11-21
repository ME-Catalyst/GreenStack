"""Add has_supported_access_locks column to device_features table

Revision ID: 039
Revises: 038
Create Date: 2025-11-21

This migration adds a flag to track whether the SupportedAccessLocks element
was present in the original IODD file. This is needed for PQA Phase 1 to
avoid generating extra elements that weren't in the original.
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers
revision = '039'
down_revision = '038'
branch_labels = None
depends_on = None


def upgrade():
    # Add has_supported_access_locks column to device_features table
    # This tracks whether the SupportedAccessLocks element was present in the original IODD
    # If absent, reconstruction should not generate it (to avoid extra_element PQA issues)
    op.add_column('device_features', sa.Column('has_supported_access_locks', sa.Boolean(), nullable=True, server_default='0'))


def downgrade():
    op.drop_column('device_features', 'has_supported_access_locks')
