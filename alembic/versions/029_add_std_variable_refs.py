"""Add std_variable_refs table for PQA reconstruction

Revision ID: 029
Revises: 028
Create Date: 2024-11-21

Stores the StdVariableRef elements from IODD VariableCollection
in their original order with all attributes for accurate reconstruction.
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '029'
down_revision = '028'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add std_variable_refs table"""
    op.create_table(
        'std_variable_refs',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('device_id', sa.Integer(), nullable=False),
        sa.Column('variable_id', sa.String(100), nullable=False),  # e.g., V_VendorName
        sa.Column('default_value', sa.Text(), nullable=True),
        sa.Column('fixed_length_restriction', sa.Integer(), nullable=True),
        sa.Column('excluded_from_data_storage', sa.Boolean(), nullable=True),
        sa.Column('order_index', sa.Integer(), nullable=False),  # Original order
        sa.ForeignKeyConstraint(['device_id'], ['devices.id'], ondelete='CASCADE'),
    )

    # Create index for faster lookups
    op.create_index('ix_std_variable_refs_device_id', 'std_variable_refs', ['device_id'])


def downgrade() -> None:
    """Remove std_variable_refs table"""
    op.drop_index('ix_std_variable_refs_device_id', table_name='std_variable_refs')
    op.drop_table('std_variable_refs')
