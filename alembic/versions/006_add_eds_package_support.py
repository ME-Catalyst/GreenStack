"""Add EDS package support with version and variant tracking

Revision ID: 006
Revises: 005
Create Date: 2025-11-13

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '006'
down_revision = '005'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add EDS package tables and tracking fields."""

    # Create eds_packages table
    op.create_table(
        'eds_packages',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('package_name', sa.Text(), nullable=False),
        sa.Column('package_checksum', sa.Text(), nullable=False, unique=True),
        sa.Column('upload_date', sa.DateTime(), nullable=False),
        sa.Column('readme_content', sa.Text(), nullable=True),
        sa.Column('total_eds_files', sa.Integer(), nullable=True),
        sa.Column('total_versions', sa.Integer(), nullable=True),
        sa.Column('vendor_name', sa.Text(), nullable=True),
        sa.Column('product_name', sa.Text(), nullable=True),
    )

    # Create eds_package_metadata table for supporting files
    op.create_table(
        'eds_package_metadata',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('package_id', sa.Integer(), nullable=False),
        sa.Column('file_path', sa.Text(), nullable=False),
        sa.Column('file_type', sa.Text(), nullable=True),  # readme, changelog, iolm_xml, image
        sa.Column('content', sa.LargeBinary(), nullable=True),
        sa.ForeignKeyConstraint(['package_id'], ['eds_packages.id'],
                                name='fk_eds_package_metadata_package_id', ondelete='CASCADE')
    )

    # Add package tracking columns to eds_files
    # SQLite doesn't support adding foreign keys after creation, so we just add columns
    op.add_column('eds_files', sa.Column('package_id', sa.Integer(), nullable=True))
    op.add_column('eds_files', sa.Column('variant_type', sa.Text(), nullable=True))
    op.add_column('eds_files', sa.Column('version_folder', sa.Text(), nullable=True))
    op.add_column('eds_files', sa.Column('is_latest_version', sa.Boolean(), nullable=True, default=False))
    op.add_column('eds_files', sa.Column('file_path_in_package', sa.Text(), nullable=True))

    # Create indexes
    op.create_index('ix_eds_packages_package_name', 'eds_packages', ['package_name'])
    op.create_index('ix_eds_package_metadata_package_id', 'eds_package_metadata', ['package_id'])
    op.create_index('ix_eds_files_package_id', 'eds_files', ['package_id'])
    op.create_index('ix_eds_files_variant_type', 'eds_files', ['variant_type'])
    op.create_index('ix_eds_files_is_latest_version', 'eds_files', ['is_latest_version'])


def downgrade() -> None:
    """Remove EDS package support."""

    # Drop indexes
    op.drop_index('ix_eds_files_is_latest_version', table_name='eds_files')
    op.drop_index('ix_eds_files_variant_type', table_name='eds_files')
    op.drop_index('ix_eds_files_package_id', table_name='eds_files')
    op.drop_index('ix_eds_package_metadata_package_id', table_name='eds_package_metadata')
    op.drop_index('ix_eds_packages_package_name', table_name='eds_packages')

    # Drop columns from eds_files
    op.drop_column('eds_files', 'file_path_in_package')
    op.drop_column('eds_files', 'is_latest_version')
    op.drop_column('eds_files', 'version_folder')
    op.drop_column('eds_files', 'variant_type')
    op.drop_column('eds_files', 'package_id')

    # Drop tables
    op.drop_table('eds_package_metadata')
    op.drop_table('eds_packages')
