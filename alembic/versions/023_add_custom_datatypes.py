"""Add custom datatypes and advanced parameter attributes

Revision ID: 023
Revises: 022
Create Date: 2025-11-17

This migration adds support for custom datatypes, arrays, strings, and advanced
parameter attributes. Also adds vendor logo, stamp metadata, and text categorization.
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '023'
down_revision = '022'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add custom datatypes tables and extend existing tables."""

    # Create custom_datatypes table
    op.create_table(
        'custom_datatypes',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('device_id', sa.Integer(), nullable=False),
        sa.Column('datatype_id', sa.Text(), nullable=False),
        sa.Column('datatype_xsi_type', sa.Text(), nullable=True),
        sa.Column('bit_length', sa.Integer(), nullable=True),
        sa.Column('subindex_access_supported', sa.Integer(), nullable=True, default=0),
        sa.ForeignKeyConstraint(['device_id'], ['devices.id'],
                               name='fk_custom_datatypes_device_id',
                               ondelete='CASCADE')
    )

    # Create custom_datatype_single_values table
    op.create_table(
        'custom_datatype_single_values',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('datatype_id', sa.Integer(), nullable=False),
        sa.Column('value', sa.Text(), nullable=False),
        sa.Column('name', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['datatype_id'], ['custom_datatypes.id'],
                               name='fk_custom_datatype_single_values_datatype_id',
                               ondelete='CASCADE')
    )

    # Create custom_datatype_record_items table
    op.create_table(
        'custom_datatype_record_items',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('datatype_id', sa.Integer(), nullable=False),
        sa.Column('subindex', sa.Integer(), nullable=True),
        sa.Column('bit_offset', sa.Integer(), nullable=True),
        sa.Column('bit_length', sa.Integer(), nullable=True),
        sa.Column('datatype_ref', sa.Text(), nullable=True),
        sa.Column('name', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['datatype_id'], ['custom_datatypes.id'],
                               name='fk_custom_datatype_record_items_datatype_id',
                               ondelete='CASCADE')
    )

    # Add array columns to parameters table
    op.add_column('parameters', sa.Column('is_array', sa.Integer(), nullable=True, default=0))
    op.add_column('parameters', sa.Column('array_count', sa.Integer(), nullable=True))
    op.add_column('parameters', sa.Column('array_element_type', sa.Text(), nullable=True))

    # Add string columns to parameters table
    op.add_column('parameters', sa.Column('string_encoding', sa.Text(), nullable=True))
    op.add_column('parameters', sa.Column('string_fixed_length', sa.Integer(), nullable=True))

    # Add subindex access support to parameters table
    op.add_column('parameters', sa.Column('subindex_access_supported', sa.Integer(), nullable=True, default=0))

    # Add vendor logo to devices table
    op.add_column('devices', sa.Column('vendor_logo_filename', sa.Text(), nullable=True))

    # Add stamp/validation metadata to iodd_files table (if it exists)
    # Using try/except to handle case where iodd_files table might not exist
    try:
        op.add_column('iodd_files', sa.Column('stamp_crc', sa.Text(), nullable=True))
        op.add_column('iodd_files', sa.Column('checker_name', sa.Text(), nullable=True))
        op.add_column('iodd_files', sa.Column('checker_version', sa.Text(), nullable=True))
    except:
        pass  # Table doesn't exist or columns already exist

    # Add text categorization to iodd_text table (if it exists)
    try:
        op.add_column('iodd_text', sa.Column('text_category', sa.Text(), nullable=True))
        op.add_column('iodd_text', sa.Column('context', sa.Text(), nullable=True))
    except:
        pass  # Table doesn't exist or columns already exist

    # Create indexes for faster lookups
    op.create_index('idx_custom_datatypes_device_id',
                    'custom_datatypes', ['device_id'])
    op.create_index('idx_custom_datatypes_datatype_id',
                    'custom_datatypes', ['datatype_id'])
    op.create_index('idx_custom_datatype_single_values_datatype_id',
                    'custom_datatype_single_values', ['datatype_id'])
    op.create_index('idx_custom_datatype_record_items_datatype_id',
                    'custom_datatype_record_items', ['datatype_id'])


def downgrade() -> None:
    """Remove custom datatypes tables and columns."""

    # Drop indexes
    op.drop_index('idx_custom_datatype_record_items_datatype_id',
                  table_name='custom_datatype_record_items')
    op.drop_index('idx_custom_datatype_single_values_datatype_id',
                  table_name='custom_datatype_single_values')
    op.drop_index('idx_custom_datatypes_datatype_id',
                  table_name='custom_datatypes')
    op.drop_index('idx_custom_datatypes_device_id',
                  table_name='custom_datatypes')

    # Drop columns from iodd_text table
    try:
        op.drop_column('iodd_text', 'context')
        op.drop_column('iodd_text', 'text_category')
    except:
        pass

    # Drop columns from iodd_files table
    try:
        op.drop_column('iodd_files', 'checker_version')
        op.drop_column('iodd_files', 'checker_name')
        op.drop_column('iodd_files', 'stamp_crc')
    except:
        pass

    # Drop columns from devices table
    op.drop_column('devices', 'vendor_logo_filename')

    # Drop columns from parameters table
    op.drop_column('parameters', 'subindex_access_supported')
    op.drop_column('parameters', 'string_fixed_length')
    op.drop_column('parameters', 'string_encoding')
    op.drop_column('parameters', 'array_element_type')
    op.drop_column('parameters', 'array_count')
    op.drop_column('parameters', 'is_array')

    # Drop tables
    op.drop_table('custom_datatype_record_items')
    op.drop_table('custom_datatype_single_values')
    op.drop_table('custom_datatypes')
