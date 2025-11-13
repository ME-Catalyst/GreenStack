"""Add EDS diagnostics support

Revision ID: 007
Revises: 006
Create Date: 2025-11-13

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '007'
down_revision = '006'
branch_labels = None
depends_on = None


def upgrade():
    # Create eds_diagnostics table to store parsing diagnostics
    op.create_table(
        'eds_diagnostics',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('eds_file_id', sa.Integer(), nullable=False),
        sa.Column('severity', sa.Text(), nullable=False),
        sa.Column('code', sa.Text(), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('section', sa.Text(), nullable=True),
        sa.Column('line', sa.Integer(), nullable=True),
        sa.Column('column', sa.Integer(), nullable=True),
        sa.Column('context', sa.Text(), nullable=True),
        sa.Column('created_at', sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['eds_file_id'], ['eds_files.id'], ondelete='CASCADE')
    )

    # Create index for faster queries
    op.create_index('idx_eds_diagnostics_eds_file_id', 'eds_diagnostics', ['eds_file_id'])
    op.create_index('idx_eds_diagnostics_severity', 'eds_diagnostics', ['severity'])

    # Add diagnostics summary to eds_files table
    op.add_column('eds_files', sa.Column('diagnostic_info_count', sa.Integer(), nullable=True, server_default='0'))
    op.add_column('eds_files', sa.Column('diagnostic_warn_count', sa.Integer(), nullable=True, server_default='0'))
    op.add_column('eds_files', sa.Column('diagnostic_error_count', sa.Integer(), nullable=True, server_default='0'))
    op.add_column('eds_files', sa.Column('diagnostic_fatal_count', sa.Integer(), nullable=True, server_default='0'))
    op.add_column('eds_files', sa.Column('has_parsing_issues', sa.Boolean(), nullable=True, server_default='0'))


def downgrade():
    # Remove diagnostics summary columns
    op.drop_column('eds_files', 'has_parsing_issues')
    op.drop_column('eds_files', 'diagnostic_fatal_count')
    op.drop_column('eds_files', 'diagnostic_error_count')
    op.drop_column('eds_files', 'diagnostic_warn_count')
    op.drop_column('eds_files', 'diagnostic_info_count')

    # Drop indices
    op.drop_index('idx_eds_diagnostics_severity')
    op.drop_index('idx_eds_diagnostics_eds_file_id')

    # Drop table
    op.drop_table('eds_diagnostics')
