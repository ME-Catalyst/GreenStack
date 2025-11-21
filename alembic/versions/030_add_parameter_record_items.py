"""Add parameter_record_items table for Variable RecordT reconstruction

Revision ID: 030
Revises: 029
Create Date: 2024-11-21

Stores RecordItem elements from Variable/Datatype/RecordT structures
for accurate PQA reconstruction.
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '030'
down_revision = '029'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add parameter_record_items table"""
    op.create_table(
        'parameter_record_items',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('parameter_id', sa.Integer(), nullable=False),
        sa.Column('subindex', sa.Integer(), nullable=False),
        sa.Column('bit_offset', sa.Integer(), nullable=True),
        sa.Column('bit_length', sa.Integer(), nullable=True),
        sa.Column('datatype_ref', sa.String(100), nullable=True),  # DatatypeRef datatypeId
        sa.Column('simple_datatype', sa.String(50), nullable=True),  # SimpleDatatype xsi:type
        sa.Column('name', sa.Text(), nullable=True),
        sa.Column('name_text_id', sa.String(255), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('description_text_id', sa.String(255), nullable=True),
        sa.Column('default_value', sa.Text(), nullable=True),
        sa.Column('order_index', sa.Integer(), nullable=False),  # Original order
        sa.ForeignKeyConstraint(['parameter_id'], ['parameters.id'], ondelete='CASCADE'),
    )

    # Create index for faster lookups
    op.create_index('ix_parameter_record_items_parameter_id', 'parameter_record_items', ['parameter_id'])


def downgrade() -> None:
    """Remove parameter_record_items table"""
    op.drop_index('ix_parameter_record_items_parameter_id', table_name='parameter_record_items')
    op.drop_table('parameter_record_items')
