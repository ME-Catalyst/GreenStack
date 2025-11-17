"""Add IODD text table for multi-language support

Revision ID: 018
Revises: 017
Create Date: 2025-01-17

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '018'
down_revision = '14aafab5b863'  # Changed to depend on the performance indexes migration
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create iodd_text table for storing multi-language text."""

    # Create iodd_text table
    op.create_table(
        'iodd_text',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('device_id', sa.Integer(), nullable=False),
        sa.Column('text_id', sa.Text(), nullable=False),  # e.g., "TN_DeviceName", "TN_M_Ident"
        sa.Column('language_code', sa.Text(), nullable=False),  # e.g., "en", "de", "fr", "es"
        sa.Column('text_value', sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(['device_id'], ['devices.id'], name='fk_iodd_text_device_id', ondelete='CASCADE'),
        sa.UniqueConstraint('device_id', 'text_id', 'language_code', name='uq_device_text_language')
    )

    # Create indexes for efficient lookups
    op.create_index('idx_iodd_text_device_language', 'iodd_text', ['device_id', 'language_code'])
    op.create_index('idx_iodd_text_text_id', 'iodd_text', ['text_id'])
    op.create_index('idx_iodd_text_device_id', 'iodd_text', ['device_id'])


def downgrade() -> None:
    """Drop iodd_text table and its indexes."""

    op.drop_index('idx_iodd_text_device_id', table_name='iodd_text')
    op.drop_index('idx_iodd_text_text_id', table_name='iodd_text')
    op.drop_index('idx_iodd_text_device_language', table_name='iodd_text')
    op.drop_table('iodd_text')
