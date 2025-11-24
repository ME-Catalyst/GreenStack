"""Add physics column to communication_profile for PhysicalLayer@physics attribute

Revision ID: 078
Revises: 077
Create Date: 2025-11-23

PQA Fix #44: PhysicalLayer physics and baudrate attributes
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision = '078'
down_revision = '077'
branch_labels = None
depends_on = None


def upgrade():
    """Add physics column to communication_profile table"""
    conn = op.get_bind()
    result = conn.execute(sa.text("PRAGMA table_info(communication_profile)"))
    columns = [row[1] for row in result.fetchall()]

    if 'physics' not in columns:
        op.add_column('communication_profile',
                      sa.Column('physics', sa.VARCHAR(50), nullable=True))


def downgrade():
    """SQLite doesn't support DROP COLUMN directly"""
    pass
