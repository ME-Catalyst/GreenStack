"""Add device variants and process data conditions

Revision ID: 020
Revises: 019
Create Date: 2025-11-17

This migration adds support for device variants and conditional process data.
Device variants enable proper device identification and image display per variant.
Process data conditions enable mode-specific data structures.
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '020'
down_revision = '019'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add device variants and process data conditions tables."""

    # Create device_variants table
    op.create_table(
        'device_variants',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('device_id', sa.Integer(), nullable=False),
        sa.Column('product_id', sa.Text(), nullable=False),
        sa.Column('device_symbol', sa.Text(), nullable=True),
        sa.Column('device_icon', sa.Text(), nullable=True),
        sa.Column('name', sa.Text(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['device_id'], ['devices.id'],
                               name='fk_device_variants_device_id',
                               ondelete='CASCADE')
    )

    # Create process_data_conditions table
    op.create_table(
        'process_data_conditions',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('process_data_id', sa.Integer(), nullable=False),
        sa.Column('condition_variable_id', sa.Text(), nullable=False),
        sa.Column('condition_value', sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(['process_data_id'], ['process_data.id'],
                               name='fk_process_data_conditions_process_data_id',
                               ondelete='CASCADE')
    )

    # Create indexes for faster lookups
    op.create_index('idx_device_variants_device_id',
                    'device_variants', ['device_id'])
    op.create_index('idx_device_variants_product_id',
                    'device_variants', ['product_id'])
    op.create_index('idx_process_data_conditions_process_data_id',
                    'process_data_conditions', ['process_data_id'])
    op.create_index('idx_process_data_conditions_variable_id',
                    'process_data_conditions', ['condition_variable_id'])


def downgrade() -> None:
    """Remove device variants and process data conditions tables."""

    # Drop indexes
    op.drop_index('idx_process_data_conditions_variable_id',
                  table_name='process_data_conditions')
    op.drop_index('idx_process_data_conditions_process_data_id',
                  table_name='process_data_conditions')
    op.drop_index('idx_device_variants_product_id',
                  table_name='device_variants')
    op.drop_index('idx_device_variants_device_id',
                  table_name='device_variants')

    # Drop tables
    op.drop_table('process_data_conditions')
    op.drop_table('device_variants')
