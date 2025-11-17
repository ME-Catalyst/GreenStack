"""Add wiring and test configuration tables

Revision ID: 022
Revises: 021
Create Date: 2025-11-17

This migration adds support for wire configurations and device test configurations.
Enables display of wiring diagrams and manufacturing test procedures.
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '022'
down_revision = '021'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add wiring and test configuration tables."""

    # Create wire_configurations table
    op.create_table(
        'wire_configurations',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('device_id', sa.Integer(), nullable=False),
        sa.Column('connection_type', sa.Text(), nullable=True),
        sa.Column('wire_number', sa.Integer(), nullable=True),
        sa.Column('wire_color', sa.Text(), nullable=True),
        sa.Column('wire_function', sa.Text(), nullable=True),
        sa.Column('wire_description', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['device_id'], ['devices.id'],
                               name='fk_wire_configurations_device_id',
                               ondelete='CASCADE')
    )

    # Create device_test_config table
    op.create_table(
        'device_test_config',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('device_id', sa.Integer(), nullable=False),
        sa.Column('config_type', sa.Text(), nullable=True),
        sa.Column('param_index', sa.Integer(), nullable=True),
        sa.Column('test_value', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['device_id'], ['devices.id'],
                               name='fk_device_test_config_device_id',
                               ondelete='CASCADE')
    )

    # Create device_test_event_triggers table
    op.create_table(
        'device_test_event_triggers',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('test_config_id', sa.Integer(), nullable=False),
        sa.Column('appear_value', sa.Text(), nullable=True),
        sa.Column('disappear_value', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['test_config_id'], ['device_test_config.id'],
                               name='fk_device_test_event_triggers_test_config_id',
                               ondelete='CASCADE')
    )

    # Create indexes for faster lookups
    op.create_index('idx_wire_configurations_device_id',
                    'wire_configurations', ['device_id'])
    op.create_index('idx_device_test_config_device_id',
                    'device_test_config', ['device_id'])
    op.create_index('idx_device_test_event_triggers_test_config_id',
                    'device_test_event_triggers', ['test_config_id'])


def downgrade() -> None:
    """Remove wiring and test configuration tables."""

    # Drop indexes
    op.drop_index('idx_device_test_event_triggers_test_config_id',
                  table_name='device_test_event_triggers')
    op.drop_index('idx_device_test_config_device_id',
                  table_name='device_test_config')
    op.drop_index('idx_wire_configurations_device_id',
                  table_name='wire_configurations')

    # Drop tables
    op.drop_table('device_test_event_triggers')
    op.drop_table('device_test_config')
    op.drop_table('wire_configurations')
