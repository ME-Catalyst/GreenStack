"""Add Parser Quality Assurance (PQA) System

Revision ID: 024
Revises: 023
Create Date: 2025-01-17

This migration adds comprehensive Parser Quality Assurance tables for:
- Original file archiving
- Quality metrics tracking
- Diff detail storage
- Configurable quality thresholds
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '024'
down_revision = '023'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create PQA system tables."""

    # 1. File Archive Table - Store original IODD/EDS files for comparison
    op.create_table(
        'pqa_file_archive',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('device_id', sa.Integer(), nullable=False),
        sa.Column('file_type', sa.Text(), nullable=False),  # 'IODD' or 'EDS'
        sa.Column('filename', sa.Text(), nullable=False),
        sa.Column('file_hash', sa.Text(), nullable=False),  # SHA256
        sa.Column('file_content', sa.BLOB(), nullable=False),  # Original XML/EDS
        sa.Column('file_size', sa.Integer(), nullable=False),
        sa.Column('upload_timestamp', sa.DateTime(), server_default=sa.func.current_timestamp()),
        sa.Column('parser_version', sa.Text()),  # Version of greenstack parser
        sa.ForeignKeyConstraint(['device_id'], ['devices.id'], name='fk_pqa_archive_device_id', ondelete='CASCADE')
    )

    op.create_index('idx_pqa_archive_device', 'pqa_file_archive', ['device_id'])
    op.create_index('idx_pqa_archive_hash', 'pqa_file_archive', ['file_hash'])
    op.create_index('idx_pqa_archive_timestamp', 'pqa_file_archive', ['upload_timestamp'])

    # 2. Quality Metrics Table - Store comprehensive analysis results
    op.create_table(
        'pqa_quality_metrics',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('device_id', sa.Integer(), nullable=False),
        sa.Column('archive_id', sa.Integer(), nullable=False),
        sa.Column('analysis_timestamp', sa.DateTime(), server_default=sa.func.current_timestamp()),

        # Overall Scores (0-100)
        sa.Column('overall_score', sa.Float(), nullable=False),
        sa.Column('structural_score', sa.Float(), nullable=False),
        sa.Column('attribute_score', sa.Float(), nullable=False),
        sa.Column('value_score', sa.Float(), nullable=False),

        # Element Counts
        sa.Column('total_elements_original', sa.Integer()),
        sa.Column('total_elements_reconstructed', sa.Integer()),
        sa.Column('missing_elements', sa.Integer()),
        sa.Column('extra_elements', sa.Integer()),

        # Attribute Counts
        sa.Column('total_attributes_original', sa.Integer()),
        sa.Column('total_attributes_reconstructed', sa.Integer()),
        sa.Column('missing_attributes', sa.Integer()),
        sa.Column('incorrect_attributes', sa.Integer()),

        # Data Loss Metrics
        sa.Column('data_loss_percentage', sa.Float()),
        sa.Column('critical_data_loss', sa.Boolean(), default=False),

        # Phase Coverage (0-100 each)
        sa.Column('phase1_score', sa.Float()),  # UI Rendering Metadata
        sa.Column('phase2_score', sa.Float()),  # Variants & Conditions
        sa.Column('phase3_score', sa.Float()),  # Menu Buttons
        sa.Column('phase4_score', sa.Float()),  # Wiring & Test Config
        sa.Column('phase5_score', sa.Float()),  # Custom Datatypes

        # Performance Metrics
        sa.Column('reconstruction_time_ms', sa.Integer()),
        sa.Column('comparison_time_ms', sa.Integer()),

        # Status Flags
        sa.Column('passed_threshold', sa.Boolean(), default=False),
        sa.Column('requires_review', sa.Boolean(), default=False),
        sa.Column('ticket_generated', sa.Boolean(), default=False),

        sa.ForeignKeyConstraint(['device_id'], ['devices.id'], name='fk_pqa_metrics_device_id', ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['archive_id'], ['pqa_file_archive.id'], name='fk_pqa_metrics_archive_id', ondelete='CASCADE')
    )

    op.create_index('idx_pqa_metrics_device', 'pqa_quality_metrics', ['device_id'])
    op.create_index('idx_pqa_metrics_archive', 'pqa_quality_metrics', ['archive_id'])
    op.create_index('idx_pqa_metrics_timestamp', 'pqa_quality_metrics', ['analysis_timestamp'])
    op.create_index('idx_pqa_metrics_score', 'pqa_quality_metrics', ['overall_score'])
    op.create_index('idx_pqa_metrics_passed', 'pqa_quality_metrics', ['passed_threshold'])

    # 3. Diff Details Table - Store individual differences found
    op.create_table(
        'pqa_diff_details',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('metric_id', sa.Integer(), nullable=False),
        sa.Column('diff_type', sa.Text(), nullable=False),  # 'missing_element', 'changed_value', 'missing_attribute', etc.
        sa.Column('severity', sa.Text(), nullable=False),   # 'CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'INFO'
        sa.Column('xpath', sa.Text(), nullable=False),      # XPath to affected element
        sa.Column('expected_value', sa.Text()),             # Value in original
        sa.Column('actual_value', sa.Text()),               # Value in reconstructed
        sa.Column('description', sa.Text()),                # Human-readable description
        sa.Column('phase', sa.Text()),                      # Which phase this diff belongs to
        sa.ForeignKeyConstraint(['metric_id'], ['pqa_quality_metrics.id'], name='fk_pqa_diff_metric_id', ondelete='CASCADE')
    )

    op.create_index('idx_pqa_diff_metric', 'pqa_diff_details', ['metric_id'])
    op.create_index('idx_pqa_diff_severity', 'pqa_diff_details', ['severity'])
    op.create_index('idx_pqa_diff_type', 'pqa_diff_details', ['diff_type'])
    op.create_index('idx_pqa_diff_phase', 'pqa_diff_details', ['phase'])

    # 4. Thresholds Table - Configurable quality thresholds
    op.create_table(
        'pqa_thresholds',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('threshold_name', sa.Text(), unique=True, nullable=False),
        sa.Column('description', sa.Text()),

        # Score Thresholds
        sa.Column('min_overall_score', sa.Float(), default=95.0),
        sa.Column('min_structural_score', sa.Float(), default=98.0),
        sa.Column('min_attribute_score', sa.Float(), default=95.0),
        sa.Column('min_value_score', sa.Float(), default=90.0),

        # Data Loss Thresholds
        sa.Column('max_data_loss_percentage', sa.Float(), default=1.0),
        sa.Column('allow_critical_data_loss', sa.Boolean(), default=False),

        # Phase Thresholds
        sa.Column('min_phase1_score', sa.Float(), default=90.0),
        sa.Column('min_phase2_score', sa.Float(), default=90.0),
        sa.Column('min_phase3_score', sa.Float(), default=90.0),
        sa.Column('min_phase4_score', sa.Float(), default=90.0),
        sa.Column('min_phase5_score', sa.Float(), default=90.0),

        # Automation Settings
        sa.Column('auto_ticket_on_fail', sa.Boolean(), default=True),
        sa.Column('auto_analysis_on_import', sa.Boolean(), default=True),
        sa.Column('email_notifications', sa.Boolean(), default=False),

        # Status
        sa.Column('active', sa.Boolean(), default=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.current_timestamp()),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.current_timestamp())
    )

    op.create_index('idx_pqa_threshold_active', 'pqa_thresholds', ['active'])

    # Insert default threshold
    op.execute("""
        INSERT INTO pqa_thresholds (
            threshold_name,
            description,
            min_overall_score,
            min_structural_score,
            min_attribute_score,
            min_value_score,
            max_data_loss_percentage,
            allow_critical_data_loss,
            auto_ticket_on_fail,
            auto_analysis_on_import,
            active
        ) VALUES (
            'default',
            'Default quality threshold for all parser analyses',
            95.0,
            98.0,
            95.0,
            90.0,
            1.0,
            0,
            1,
            0,
            1
        )
    """)

    # 5. Analysis Queue Table - Track pending/running analyses
    op.create_table(
        'pqa_analysis_queue',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('device_id', sa.Integer(), nullable=False),
        sa.Column('archive_id', sa.Integer(), nullable=False),
        sa.Column('status', sa.Text(), nullable=False),  # 'pending', 'running', 'completed', 'failed'
        sa.Column('priority', sa.Integer(), default=5),  # 1-10 (10 = highest)
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.current_timestamp()),
        sa.Column('started_at', sa.DateTime()),
        sa.Column('completed_at', sa.DateTime()),
        sa.Column('error_message', sa.Text()),
        sa.Column('metric_id', sa.Integer()),  # Reference to resulting metric
        sa.ForeignKeyConstraint(['device_id'], ['devices.id'], name='fk_pqa_queue_device_id', ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['archive_id'], ['pqa_file_archive.id'], name='fk_pqa_queue_archive_id', ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['metric_id'], ['pqa_quality_metrics.id'], name='fk_pqa_queue_metric_id', ondelete='SET NULL')
    )

    op.create_index('idx_pqa_queue_status', 'pqa_analysis_queue', ['status'])
    op.create_index('idx_pqa_queue_priority', 'pqa_analysis_queue', ['priority'])
    op.create_index('idx_pqa_queue_device', 'pqa_analysis_queue', ['device_id'])


def downgrade() -> None:
    """Drop PQA system tables."""

    # Drop in reverse order due to foreign keys
    op.drop_table('pqa_analysis_queue')
    op.drop_table('pqa_thresholds')
    op.drop_table('pqa_diff_details')
    op.drop_table('pqa_quality_metrics')
    op.drop_table('pqa_file_archive')
