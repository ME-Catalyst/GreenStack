"""Add variable_id column to parameters table for IODD Variable reconstruction

Revision ID: 027
Revises: 026
Create Date: 2025-11-20

This migration adds the variable_id column to store the original IODD Variable
element 'id' attribute (e.g., V_CP_FunctionTag, V_SupplyVoltage) which is needed
for accurate IODD reconstruction in PQA.

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '027'
down_revision = '9d7556282dff'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add variable_id column to parameters table."""

    with op.batch_alter_table('parameters') as batch_op:
        batch_op.add_column(sa.Column('variable_id', sa.Text, nullable=True))


def downgrade() -> None:
    """Remove variable_id column from parameters table."""

    with op.batch_alter_table('parameters') as batch_op:
        batch_op.drop_column('variable_id')
