"""Expand parameter schema with units and scaling fields

Revision ID: 012
Revises: 011
Create Date: 2025-11-14

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '012'
down_revision = '011'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add new parameter fields for units, scaling, and decimal places."""

    with op.batch_alter_table('eds_parameters') as batch_op:
        batch_op.add_column(sa.Column('units', sa.Text, nullable=True))
        batch_op.add_column(sa.Column('scaling_multiplier', sa.Text, nullable=True))
        batch_op.add_column(sa.Column('scaling_divisor', sa.Text, nullable=True))
        batch_op.add_column(sa.Column('scaling_base', sa.Text, nullable=True))
        batch_op.add_column(sa.Column('scaling_offset', sa.Text, nullable=True))
        batch_op.add_column(sa.Column('link_scaling_multiplier', sa.Text, nullable=True))
        batch_op.add_column(sa.Column('link_scaling_divisor', sa.Text, nullable=True))
        batch_op.add_column(sa.Column('link_scaling_base', sa.Text, nullable=True))
        batch_op.add_column(sa.Column('link_scaling_offset', sa.Text, nullable=True))
        batch_op.add_column(sa.Column('decimal_places', sa.Integer, nullable=True))


def downgrade() -> None:
    """Remove new parameter fields."""

    with op.batch_alter_table('eds_parameters') as batch_op:
        batch_op.drop_column('decimal_places')
        batch_op.drop_column('link_scaling_offset')
        batch_op.drop_column('link_scaling_base')
        batch_op.drop_column('link_scaling_divisor')
        batch_op.drop_column('link_scaling_multiplier')
        batch_op.drop_column('scaling_offset')
        batch_op.drop_column('scaling_base')
        batch_op.drop_column('scaling_divisor')
        batch_op.drop_column('scaling_multiplier')
        batch_op.drop_column('units')
