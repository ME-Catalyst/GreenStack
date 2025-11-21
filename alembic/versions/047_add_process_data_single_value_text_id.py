"""Add name_text_id column to process_data_single_values

Revision ID: 047
Revises: 046
Create Date: 2025-01-21

Adds name_text_id column to process_data_single_values for PQA reconstruction.
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '047'
down_revision = '046'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('process_data_single_values',
                  sa.Column('name_text_id', sa.VARCHAR(255), nullable=True))


def downgrade():
    op.drop_column('process_data_single_values', 'name_text_id')
