"""add_simple_datatype_id_to_overlay_record_items

Revision ID: 3080af74c43e
Revises: e60240139ccc
Create Date: 2025-11-28 19:15:38.472466

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3080af74c43e'
down_revision = 'e60240139ccc'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add simple_datatype_id column to direct_parameter_overlay_record_items
    op.add_column('direct_parameter_overlay_record_items',
                  sa.Column('simple_datatype_id', sa.String(255), nullable=True))


def downgrade() -> None:
    # Remove simple_datatype_id column from direct_parameter_overlay_record_items
    op.drop_column('direct_parameter_overlay_record_items', 'simple_datatype_id')
