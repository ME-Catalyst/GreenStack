"""Add custom_datatype_record_item_single_values table

Revision ID: 062
Revises: 061
Create Date: 2025-01-21

PQA Fix #21: Store SingleValue elements inside DatatypeCollection RecordItem/SimpleDatatype
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '062'
down_revision = '061'
branch_labels = None
depends_on = None


def upgrade():
    """Create custom_datatype_record_item_single_values table"""
    op.create_table(
        'custom_datatype_record_item_single_values',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('record_item_id', sa.Integer(), nullable=False),
        sa.Column('value', sa.String(255), nullable=True),
        sa.Column('name', sa.Text(), nullable=True),
        sa.Column('name_text_id', sa.String(255), nullable=True),
        sa.Column('xsi_type', sa.String(100), nullable=True),
        sa.ForeignKeyConstraint(['record_item_id'], ['custom_datatype_record_items.id'],
                               name='fk_cdri_sv_record_item_id',
                               ondelete='CASCADE')
    )
    op.create_index('idx_cdri_sv_record_item_id', 'custom_datatype_record_item_single_values', ['record_item_id'])


def downgrade():
    """Drop custom_datatype_record_item_single_values table"""
    op.drop_index('idx_cdri_sv_record_item_id', table_name='custom_datatype_record_item_single_values')
    op.drop_table('custom_datatype_record_item_single_values')
