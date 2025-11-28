"""add_is_std_direct_parameter_ref_to_parameters

Revision ID: b593adb623e2
Revises: 74e0497a4875
Create Date: 2025-11-28 09:47:46.822275

PQA Fix #127: Add is_std_direct_parameter_ref flag to parameters table.
This column marks parameters that should be reconstructed as
StdDirectParameterRef elements instead of Variable elements.

StdDirectParameterRef is a special IODD element that's structurally similar
to Variable but with a different element name. Used for V_DirectParameters_1,
V_DirectParameters_2, and custom direct parameter blocks.
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b593adb623e2'
down_revision = '74e0497a4875'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add is_std_direct_parameter_ref column to parameters table
    with op.batch_alter_table('parameters') as batch_op:
        batch_op.add_column(sa.Column('is_std_direct_parameter_ref', sa.Boolean(), nullable=True, server_default='0'))


def downgrade() -> None:
    # Remove is_std_direct_parameter_ref column from parameters table
    with op.batch_alter_table('parameters') as batch_op:
        batch_op.drop_column('is_std_direct_parameter_ref')
