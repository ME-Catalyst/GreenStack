"""Add Wire xsi:type column for PQA reconstruction

Revision ID: 066
Revises: 065
Create Date: 2025-11-22

PQA Fix #25: Store xsi:type for Wire elements (Wire1T, Wire3T, Wire4T, etc.)
to enable accurate reconstruction (33 issues across 10 devices).
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '066'
down_revision = '065'
branch_labels = None
depends_on = None


def upgrade():
    """Add xsi_type column to wire_configurations table"""
    try:
        op.add_column('wire_configurations', sa.Column('xsi_type', sa.String(50), nullable=True))
    except Exception:
        pass  # Column may already exist


def downgrade():
    """Remove xsi_type column"""
    try:
        op.drop_column('wire_configurations', 'xsi_type')
    except Exception:
        pass
