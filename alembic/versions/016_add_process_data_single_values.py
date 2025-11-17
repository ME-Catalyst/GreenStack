"""Add process_data_single_values table

Revision ID: 016
Revises: 015
Create Date: 2025-11-17

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '016'
down_revision = '015'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create process_data_single_values table."""

    op.create_table(
        'process_data_single_values',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('record_item_id', sa.Integer(), nullable=True),
        sa.Column('value', sa.Text(), nullable=True),
        sa.Column('name', sa.Text(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['record_item_id'], ['process_data_record_items.id'], name='fk_single_values_record_item_id')
    )


def downgrade() -> None:
    """Drop process_data_single_values table."""

    op.drop_table('process_data_single_values')
