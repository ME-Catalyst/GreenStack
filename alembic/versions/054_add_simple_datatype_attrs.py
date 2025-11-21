"""Add SimpleDatatype attributes to record_items tables

Revision ID: 054
Revises: 053
Create Date: 2025-11-21
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '054'
down_revision = '053'
branch_labels = None
depends_on = None

def upgrade():
    # Add columns to parameter_record_items
    op.add_column('parameter_record_items', sa.Column('fixed_length', sa.INTEGER, nullable=True))
    op.add_column('parameter_record_items', sa.Column('encoding', sa.VARCHAR(50), nullable=True))
    op.add_column('parameter_record_items', sa.Column('datatype_id', sa.VARCHAR(100), nullable=True))
    
    # Add columns to process_data_record_items
    op.add_column('process_data_record_items', sa.Column('fixed_length', sa.INTEGER, nullable=True))
    op.add_column('process_data_record_items', sa.Column('encoding', sa.VARCHAR(50), nullable=True))
    op.add_column('process_data_record_items', sa.Column('datatype_id', sa.VARCHAR(100), nullable=True))
    
    # Add columns to custom_datatype_record_items
    op.add_column('custom_datatype_record_items', sa.Column('fixed_length', sa.INTEGER, nullable=True))
    op.add_column('custom_datatype_record_items', sa.Column('encoding', sa.VARCHAR(50), nullable=True))
    op.add_column('custom_datatype_record_items', sa.Column('datatype_id', sa.VARCHAR(100), nullable=True))


def downgrade():
    for table in ['parameter_record_items', 'process_data_record_items', 'custom_datatype_record_items']:
        op.drop_column(table, 'fixed_length')
        op.drop_column(table, 'encoding')
        op.drop_column(table, 'datatype_id')
