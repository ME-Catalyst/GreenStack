"""Add file_type column to pqa_quality_metrics

Revision ID: 025
Revises: 024
Create Date: 2025-01-20

Adds file_type discriminator to pqa_quality_metrics table to enable
separate tracking and querying of IODD vs EDS quality metrics.
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '025'
down_revision = '024'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add file_type column to pqa_quality_metrics."""

    # Add file_type column to pqa_quality_metrics table
    op.add_column('pqa_quality_metrics',
                  sa.Column('file_type', sa.Text(), nullable=True))

    # Populate existing records by joining with pqa_file_archive
    op.execute("""
        UPDATE pqa_quality_metrics
        SET file_type = (
            SELECT pqa_file_archive.file_type
            FROM pqa_file_archive
            WHERE pqa_file_archive.id = pqa_quality_metrics.archive_id
        )
        WHERE archive_id IS NOT NULL
    """)

    # Make file_type NOT NULL after populating existing data
    # Note: SQLite doesn't support ALTER COLUMN, so we need to handle this differently
    # For now, we'll leave it nullable but enforce it in application code

    # Create index on file_type for efficient filtering
    op.create_index('idx_pqa_metrics_file_type', 'pqa_quality_metrics', ['file_type'])


def downgrade() -> None:
    """Remove file_type column from pqa_quality_metrics."""

    # Drop index first
    op.drop_index('idx_pqa_metrics_file_type', 'pqa_quality_metrics')

    # Drop column
    op.drop_column('pqa_quality_metrics', 'file_type')
