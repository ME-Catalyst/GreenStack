"""Add device_name_text_id column to devices table

Revision ID: 058
Revises: 057
Create Date: 2025-01-21

PQA Fix #17: Store DeviceName@textId for accurate reconstruction
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '058'
down_revision = '057'
branch_labels = None
depends_on = None


def upgrade():
    """Add device_name_text_id column to devices table"""
    op.add_column('devices', sa.Column('device_name_text_id', sa.String(255), nullable=True))


def downgrade():
    """Remove device_name_text_id column from devices table"""
    op.drop_column('devices', 'device_name_text_id')
