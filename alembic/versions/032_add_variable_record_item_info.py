"""Add variable_record_item_info table for RecordItemInfo reconstruction

Revision ID: 032
Revises: 031
Create Date: 2024-11-21

Stores RecordItemInfo elements from Variable elements
for accurate PQA reconstruction.
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '032'
down_revision = '031'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add variable_record_item_info table"""
    op.create_table(
        'variable_record_item_info',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('parameter_id', sa.Integer(), nullable=False),
        sa.Column('subindex', sa.Integer(), nullable=False),
        sa.Column('default_value', sa.Text(), nullable=True),
        sa.Column('order_index', sa.Integer(), nullable=False),  # Original order
        sa.ForeignKeyConstraint(['parameter_id'], ['parameters.id'], ondelete='CASCADE'),
    )

    # Create index for faster lookups
    op.create_index('ix_variable_record_item_info_parameter_id', 'variable_record_item_info', ['parameter_id'])


def downgrade() -> None:
    """Remove variable_record_item_info table"""
    op.drop_index('ix_variable_record_item_info_parameter_id', table_name='variable_record_item_info')
    op.drop_table('variable_record_item_info')
