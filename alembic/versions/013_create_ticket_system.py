"""Create ticket system tables

Revision ID: 013
Revises: 012
Create Date: 2025-11-14

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '013'
down_revision = '012'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create ticket system tables."""

    # Create tickets table
    op.create_table(
        'tickets',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('ticket_number', sa.Text(), nullable=False, unique=True),
        sa.Column('device_type', sa.Text(), nullable=False),  # 'EDS' or 'IODD'
        sa.Column('device_id', sa.Integer(), nullable=True),
        sa.Column('device_name', sa.Text(), nullable=True),
        sa.Column('vendor_name', sa.Text(), nullable=True),
        sa.Column('product_code', sa.Integer(), nullable=True),
        sa.Column('title', sa.Text(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('eds_reference', sa.Text(), nullable=True),
        sa.Column('status', sa.Text(), nullable=False, default='open'),  # open, in_progress, resolved, closed, wont_fix
        sa.Column('priority', sa.Text(), nullable=False, default='medium'),  # low, medium, high, critical
        sa.Column('category', sa.Text(), nullable=True),  # data_issue, parser_bug, feature_request, etc.
        sa.Column('created_at', sa.Text(), nullable=False),
        sa.Column('updated_at', sa.Text(), nullable=False),
        sa.Column('resolved_at', sa.Text(), nullable=True),
        sa.Column('created_by', sa.Text(), nullable=True),
        sa.Column('assigned_to', sa.Text(), nullable=True),
    )

    # Create ticket_comments table
    op.create_table(
        'ticket_comments',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('ticket_id', sa.Integer(), nullable=False),
        sa.Column('comment_text', sa.Text(), nullable=False),
        sa.Column('created_at', sa.Text(), nullable=False),
        sa.Column('created_by', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['ticket_id'], ['tickets.id'], ondelete='CASCADE'),
    )

    # Create ticket_attachments table
    op.create_table(
        'ticket_attachments',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('ticket_id', sa.Integer(), nullable=False),
        sa.Column('filename', sa.Text(), nullable=False),
        sa.Column('file_path', sa.Text(), nullable=False),
        sa.Column('file_size', sa.Integer(), nullable=True),
        sa.Column('content_type', sa.Text(), nullable=True),
        sa.Column('uploaded_at', sa.Text(), nullable=False),
        sa.Column('uploaded_by', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['ticket_id'], ['tickets.id'], ondelete='CASCADE'),
    )


def downgrade() -> None:
    """Drop ticket system tables."""
    op.drop_table('ticket_attachments')
    op.drop_table('ticket_comments')
    op.drop_table('tickets')
