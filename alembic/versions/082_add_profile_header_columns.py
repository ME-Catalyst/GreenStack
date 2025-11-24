"""Add ProfileHeader columns to iodd_files table

Revision ID: 082
Revises: 081
Create Date: 2025-11-23

PQA Fix #54: Store ProfileHeader values for accurate reconstruction
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision = '082'
down_revision = '081'
branch_labels = None
depends_on = None


def upgrade():
    """Add profile_identification, profile_revision, profile_name columns to iodd_files table"""
    conn = op.get_bind()
    result = conn.execute(sa.text("PRAGMA table_info(iodd_files)"))
    columns = [row[1] for row in result.fetchall()]

    if 'profile_identification' not in columns:
        op.add_column('iodd_files',
                      sa.Column('profile_identification', sa.VARCHAR(255), nullable=True))

    if 'profile_revision' not in columns:
        op.add_column('iodd_files',
                      sa.Column('profile_revision', sa.VARCHAR(50), nullable=True))

    if 'profile_name' not in columns:
        op.add_column('iodd_files',
                      sa.Column('profile_name', sa.VARCHAR(255), nullable=True))


def downgrade():
    """SQLite doesn't support DROP COLUMN directly"""
    pass
