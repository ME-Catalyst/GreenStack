"""Expand EDS schema with complete data capture

Revision ID: 005
Revises: 004
Create Date: 2025-11-13

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '005'
down_revision = '004'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add comprehensive EDS data tables."""

    # Add missing columns to eds_files for file info
    op.add_column('eds_files', sa.Column('create_date', sa.Text(), nullable=True))
    op.add_column('eds_files', sa.Column('create_time', sa.Text(), nullable=True))
    op.add_column('eds_files', sa.Column('mod_date', sa.Text(), nullable=True))
    op.add_column('eds_files', sa.Column('mod_time', sa.Text(), nullable=True))
    op.add_column('eds_files', sa.Column('file_revision', sa.Text(), nullable=True))

    # Add device classification columns
    op.add_column('eds_files', sa.Column('class1', sa.Text(), nullable=True))
    op.add_column('eds_files', sa.Column('class2', sa.Text(), nullable=True))
    op.add_column('eds_files', sa.Column('class3', sa.Text(), nullable=True))
    op.add_column('eds_files', sa.Column('class4', sa.Text(), nullable=True))

    # Add more parameter fields
    op.add_column('eds_parameters', sa.Column('link_path_size', sa.Text(), nullable=True))
    op.add_column('eds_parameters', sa.Column('link_path', sa.Text(), nullable=True))
    op.add_column('eds_parameters', sa.Column('descriptor', sa.Text(), nullable=True))
    op.add_column('eds_parameters', sa.Column('help_string_1', sa.Text(), nullable=True))
    op.add_column('eds_parameters', sa.Column('help_string_2', sa.Text(), nullable=True))
    op.add_column('eds_parameters', sa.Column('help_string_3', sa.Text(), nullable=True))

    # Add more connection fields
    op.add_column('eds_connections', sa.Column('o_to_t_params', sa.Text(), nullable=True))
    op.add_column('eds_connections', sa.Column('t_to_o_params', sa.Text(), nullable=True))
    op.add_column('eds_connections', sa.Column('config_part1', sa.Text(), nullable=True))
    op.add_column('eds_connections', sa.Column('config_part2', sa.Text(), nullable=True))
    op.add_column('eds_connections', sa.Column('path', sa.Text(), nullable=True))
    op.add_column('eds_connections', sa.Column('trigger_transport_comment', sa.Text(), nullable=True))
    op.add_column('eds_connections', sa.Column('connection_params_comment', sa.Text(), nullable=True))

    # Create eds_ports table
    op.create_table(
        'eds_ports',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('eds_file_id', sa.Integer(), nullable=True),
        sa.Column('port_number', sa.Integer(), nullable=True),
        sa.Column('port_type', sa.Text(), nullable=True),
        sa.Column('port_name', sa.Text(), nullable=True),
        sa.Column('port_path', sa.Text(), nullable=True),
        sa.Column('link_number', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['eds_file_id'], ['eds_files.id'], name='fk_eds_ports_eds_file_id', ondelete='CASCADE')
    )

    # Create eds_capacity table
    op.create_table(
        'eds_capacity',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('eds_file_id', sa.Integer(), nullable=True),
        sa.Column('max_msg_connections', sa.Integer(), nullable=True),
        sa.Column('max_io_producers', sa.Integer(), nullable=True),
        sa.Column('max_io_consumers', sa.Integer(), nullable=True),
        sa.Column('max_cx_per_config_tool', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['eds_file_id'], ['eds_files.id'], name='fk_eds_capacity_eds_file_id', ondelete='CASCADE'),
        sa.UniqueConstraint('eds_file_id', name='uq_eds_capacity_file_id')
    )

    # Create eds_tspecs table
    op.create_table(
        'eds_tspecs',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('eds_file_id', sa.Integer(), nullable=True),
        sa.Column('tspec_name', sa.Text(), nullable=True),
        sa.Column('direction', sa.Text(), nullable=True),
        sa.Column('data_size', sa.Integer(), nullable=True),
        sa.Column('rate', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['eds_file_id'], ['eds_files.id'], name='fk_eds_tspecs_eds_file_id', ondelete='CASCADE')
    )

    # Create indexes
    op.create_index('ix_eds_ports_eds_file_id', 'eds_ports', ['eds_file_id'])
    op.create_index('ix_eds_capacity_eds_file_id', 'eds_capacity', ['eds_file_id'])
    op.create_index('ix_eds_tspecs_eds_file_id', 'eds_tspecs', ['eds_file_id'])


def downgrade() -> None:
    """Remove expanded EDS schema."""

    # Drop indexes
    op.drop_index('ix_eds_tspecs_eds_file_id', table_name='eds_tspecs')
    op.drop_index('ix_eds_capacity_eds_file_id', table_name='eds_capacity')
    op.drop_index('ix_eds_ports_eds_file_id', table_name='eds_ports')

    # Drop tables
    op.drop_table('eds_tspecs')
    op.drop_table('eds_capacity')
    op.drop_table('eds_ports')

    # Drop connection columns
    op.drop_column('eds_connections', 'connection_params_comment')
    op.drop_column('eds_connections', 'trigger_transport_comment')
    op.drop_column('eds_connections', 'path')
    op.drop_column('eds_connections', 'config_part2')
    op.drop_column('eds_connections', 'config_part1')
    op.drop_column('eds_connections', 't_to_o_params')
    op.drop_column('eds_connections', 'o_to_t_params')

    # Drop parameter columns
    op.drop_column('eds_parameters', 'help_string_3')
    op.drop_column('eds_parameters', 'help_string_2')
    op.drop_column('eds_parameters', 'help_string_1')
    op.drop_column('eds_parameters', 'descriptor')
    op.drop_column('eds_parameters', 'link_path')
    op.drop_column('eds_parameters', 'link_path_size')

    # Drop eds_files columns
    op.drop_column('eds_files', 'class4')
    op.drop_column('eds_files', 'class3')
    op.drop_column('eds_files', 'class2')
    op.drop_column('eds_files', 'class1')
    op.drop_column('eds_files', 'file_revision')
    op.drop_column('eds_files', 'mod_time')
    op.drop_column('eds_files', 'mod_date')
    op.drop_column('eds_files', 'create_time')
    op.drop_column('eds_files', 'create_date')
