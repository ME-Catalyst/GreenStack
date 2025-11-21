"""Add parameter_single_values table for Variable SingleValue reconstruction

Revision ID: 031
Revises: 030
Create Date: 2024-11-21

Stores SingleValue elements from Variable/Datatype structures
for accurate PQA reconstruction.
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '031'
down_revision = '030'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add parameter_single_values table"""
    op.create_table(
        'parameter_single_values',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('parameter_id', sa.Integer(), nullable=False),
        sa.Column('value', sa.Text(), nullable=False),
        sa.Column('name', sa.Text(), nullable=True),
        sa.Column('text_id', sa.String(255), nullable=True),  # textId for Name element
        sa.Column('xsi_type', sa.String(100), nullable=True),  # xsi:type attribute
        sa.Column('order_index', sa.Integer(), nullable=False),  # Original order
        sa.ForeignKeyConstraint(['parameter_id'], ['parameters.id'], ondelete='CASCADE'),
    )

    # Create index for faster lookups
    op.create_index('ix_parameter_single_values_parameter_id', 'parameter_single_values', ['parameter_id'])


def downgrade() -> None:
    """Remove parameter_single_values table"""
    op.drop_index('ix_parameter_single_values_parameter_id', table_name='parameter_single_values')
    op.drop_table('parameter_single_values')
