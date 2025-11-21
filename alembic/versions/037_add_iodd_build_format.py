"""Add IODD build format metadata table

Revision ID: 037
Revises: 036
Create Date: 2024-11-21

Adds a table to store original IODD file formatting metadata for accurate
reconstruction. This enables the reconstructor to preserve the original
indentation style, namespace prefixes, and other formatting details that
have no semantic impact but are important for exact file reproduction.
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '037'
down_revision = '036'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create iodd_build_format table for storing formatting metadata"""
    op.create_table(
        'iodd_build_format',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('device_id', sa.Integer(), sa.ForeignKey('devices.id', ondelete='CASCADE'),
                  nullable=False, unique=True),

        # Indentation settings
        sa.Column('indent_char', sa.String(10), nullable=False, default='tab',
                  comment="Indentation character: 'tab' or 'space'"),
        sa.Column('indent_size', sa.Integer(), nullable=False, default=1,
                  comment="Number of indent_char per level (e.g., 1 tab or 2 spaces)"),

        # XML declaration and namespace settings
        sa.Column('xml_declaration', sa.Text(), nullable=True,
                  comment="Original XML declaration line (e.g., <?xml version='1.0'?>)"),
        sa.Column('namespace_prefix', sa.String(50), nullable=True,
                  comment="Namespace prefix used (e.g., 'iodd:' or empty for default)"),
        sa.Column('schema_location', sa.Text(), nullable=True,
                  comment="Original xsi:schemaLocation value"),

        # Line ending style
        sa.Column('newline_style', sa.String(10), nullable=False, default='lf',
                  comment="Line ending style: 'lf' (Unix), 'crlf' (Windows), or 'cr' (old Mac)"),

        # Additional formatting hints
        sa.Column('has_trailing_newline', sa.Boolean(), nullable=False, default=True,
                  comment="Whether original file had trailing newline"),
        sa.Column('attribute_quoting', sa.String(10), nullable=False, default='double',
                  comment="Attribute quote style: 'double' or 'single'"),

        # Metadata
        sa.Column('extracted_at', sa.DateTime(), nullable=True,
                  comment="When format metadata was extracted"),
    )

    # Create index for faster lookups
    op.create_index('ix_iodd_build_format_device_id', 'iodd_build_format', ['device_id'])


def downgrade() -> None:
    """Remove iodd_build_format table"""
    op.drop_index('ix_iodd_build_format_device_id', table_name='iodd_build_format')
    op.drop_table('iodd_build_format')
