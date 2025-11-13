"""Add EDS tables

Revision ID: 004
Revises: 003
Create Date: 2025-11-13

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '004'
down_revision = '003'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create EDS-related tables."""

    # Create eds_files table
    op.create_table(
        'eds_files',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('vendor_code', sa.Integer(), nullable=True),
        sa.Column('vendor_name', sa.Text(), nullable=True),
        sa.Column('product_code', sa.Integer(), nullable=True),
        sa.Column('product_type', sa.Integer(), nullable=True),
        sa.Column('product_type_str', sa.Text(), nullable=True),
        sa.Column('product_name', sa.Text(), nullable=True),
        sa.Column('catalog_number', sa.Text(), nullable=True),
        sa.Column('major_revision', sa.Integer(), nullable=True),
        sa.Column('minor_revision', sa.Integer(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('icon_filename', sa.Text(), nullable=True),
        sa.Column('icon_data', sa.LargeBinary(), nullable=True),  # Store icon binary data
        sa.Column('eds_content', sa.Text(), nullable=True),  # Store full EDS file content
        sa.Column('home_url', sa.Text(), nullable=True),
        sa.Column('import_date', sa.DateTime(), nullable=True),
        sa.Column('file_checksum', sa.Text(), nullable=True),
        sa.UniqueConstraint('file_checksum', name='uq_eds_files_checksum')
    )

    # Create eds_parameters table (for EDS parameter definitions)
    op.create_table(
        'eds_parameters',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('eds_file_id', sa.Integer(), nullable=True),
        sa.Column('param_number', sa.Integer(), nullable=True),
        sa.Column('param_name', sa.Text(), nullable=True),
        sa.Column('param_type', sa.Text(), nullable=True),
        sa.Column('data_type', sa.Integer(), nullable=True),
        sa.Column('data_size', sa.Integer(), nullable=True),
        sa.Column('default_value', sa.Text(), nullable=True),
        sa.Column('min_value', sa.Text(), nullable=True),
        sa.Column('max_value', sa.Text(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['eds_file_id'], ['eds_files.id'], name='fk_eds_parameters_eds_file_id', ondelete='CASCADE')
    )

    # Create eds_connections table (for EDS connection definitions)
    op.create_table(
        'eds_connections',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('eds_file_id', sa.Integer(), nullable=True),
        sa.Column('connection_number', sa.Integer(), nullable=True),
        sa.Column('connection_name', sa.Text(), nullable=True),
        sa.Column('trigger_transport', sa.Text(), nullable=True),
        sa.Column('connection_params', sa.Text(), nullable=True),
        sa.Column('output_assembly', sa.Text(), nullable=True),
        sa.Column('input_assembly', sa.Text(), nullable=True),
        sa.Column('help_string', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['eds_file_id'], ['eds_files.id'], name='fk_eds_connections_eds_file_id', ondelete='CASCADE')
    )

    # Create indexes for better query performance
    op.create_index('ix_eds_files_vendor_code', 'eds_files', ['vendor_code'])
    op.create_index('ix_eds_files_product_code', 'eds_files', ['product_code'])
    op.create_index('ix_eds_files_vendor_name', 'eds_files', ['vendor_name'])
    op.create_index('ix_eds_parameters_eds_file_id', 'eds_parameters', ['eds_file_id'])
    op.create_index('ix_eds_connections_eds_file_id', 'eds_connections', ['eds_file_id'])


def downgrade() -> None:
    """Drop EDS-related tables."""

    # Drop indexes
    op.drop_index('ix_eds_connections_eds_file_id', table_name='eds_connections')
    op.drop_index('ix_eds_parameters_eds_file_id', table_name='eds_parameters')
    op.drop_index('ix_eds_files_vendor_name', table_name='eds_files')
    op.drop_index('ix_eds_files_product_code', table_name='eds_files')
    op.drop_index('ix_eds_files_vendor_code', table_name='eds_files')

    # Drop tables
    op.drop_table('eds_connections')
    op.drop_table('eds_parameters')
    op.drop_table('eds_files')
