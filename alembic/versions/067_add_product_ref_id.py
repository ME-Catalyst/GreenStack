"""Add product_ref_id column for PQA reconstruction

Revision ID: 067
Revises: 066
Create Date: 2025-11-22

PQA Fix #26: Store Connection/ProductRef@productId for reconstruction.
Fixes 24 issues across 24 devices where ProductRef productId differs from
device_variants product_id.
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '067'
down_revision = '066'
branch_labels = None
depends_on = None


def upgrade():
    """Add product_ref_id column to communication_profile table"""
    try:
        op.add_column('communication_profile', sa.Column('product_ref_id', sa.String(255), nullable=True))
    except Exception:
        pass  # Column may already exist


def downgrade():
    """Remove product_ref_id column"""
    try:
        op.drop_column('communication_profile', 'product_ref_id')
    except Exception:
        pass
