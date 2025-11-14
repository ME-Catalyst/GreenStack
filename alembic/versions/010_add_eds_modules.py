"""Add EDS modules table

Revision ID: 010
Revises: 009
Create Date: 2025-01-14

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '010'
down_revision = '009'
branch_labels = None
depends_on = None


def upgrade():
    # Create eds_modules table for modular device configurations
    op.create_table(
        'eds_modules',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('eds_file_id', sa.Integer(), nullable=False),
        sa.Column('module_number', sa.Integer(), nullable=False),
        sa.Column('module_name', sa.Text(), nullable=True),
        sa.Column('device_type', sa.Text(), nullable=True),
        sa.Column('catalog_number', sa.Text(), nullable=True),
        sa.Column('major_revision', sa.Integer(), nullable=True),
        sa.Column('minor_revision', sa.Integer(), nullable=True),
        sa.Column('config_size', sa.Integer(), nullable=True),
        sa.Column('config_data', sa.Text(), nullable=True),
        sa.Column('input_size', sa.Integer(), nullable=True),
        sa.Column('output_size', sa.Integer(), nullable=True),
        sa.Column('module_description', sa.Text(), nullable=True),
        sa.Column('slot_number', sa.Integer(), nullable=True),
        sa.Column('module_class', sa.Text(), nullable=True),
        sa.Column('vendor_code', sa.Integer(), nullable=True),
        sa.Column('product_code', sa.Integer(), nullable=True),
        sa.Column('raw_definition', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['eds_file_id'], ['eds_files.id'], ondelete='CASCADE')
    )

    # Create index for faster lookups by EDS file
    op.create_index('idx_eds_modules_eds_file_id', 'eds_modules', ['eds_file_id'])


def downgrade():
    op.drop_index('idx_eds_modules_eds_file_id', table_name='eds_modules')
    op.drop_table('eds_modules')
