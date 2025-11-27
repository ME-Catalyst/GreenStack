"""add_has_event_collection_to_devices

Revision ID: 30e4d0b53871
Revises: 005_add_performance_indexes
Create Date: 2025-11-27 02:14:28.088498

Adds has_event_collection column to devices table to track presence of EventCollection element.
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '30e4d0b53871'
down_revision = '005_add_performance_indexes'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add has_event_collection column to devices table"""
    with op.batch_alter_table('devices', schema=None) as batch_op:
        batch_op.add_column(sa.Column('has_event_collection', sa.Integer(), nullable=True, server_default='0'))


def downgrade() -> None:
    """Remove has_event_collection column from devices table"""
    with op.batch_alter_table('devices', schema=None) as batch_op:
        batch_op.drop_column('has_event_collection')
